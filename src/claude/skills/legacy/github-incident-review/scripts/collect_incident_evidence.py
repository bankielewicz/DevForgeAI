#!/usr/bin/env python3
"""Collect a read-only, hash-addressed GitHub incident evidence bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


ISSUE_URL = re.compile(
    r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/issues/(?P<number>\d+)/?$"
)
REMOTE_PATTERNS = (
    re.compile(r"^https://github\.com/(?P<repo>[^/]+/[^/]+?)(?:\.git)?$"),
    re.compile(r"^git@github\.com:(?P<repo>[^/]+/[^/]+?)(?:\.git)?$"),
)
MUTATING_GH_VERBS = frozenset(
    {"create", "edit", "comment", "close", "reopen", "delete", "merge"}
)
ISSUE_FIELDS = (
    "assignees,author,blockedBy,blocking,body,closedAt,closedByPullRequestsReferences,"
    "comments,createdAt,labels,milestone,number,parent,projectItems,reactionGroups,state,"
    "stateReason,subIssues,subIssuesSummary,title,updatedAt,url"
)
SEARCH_ISSUE_FIELDS = "number,title,state,updatedAt,url,labels,repository"
SEARCH_PR_FIELDS = "number,title,state,updatedAt,url,repository"
PR_FIELDS = (
    "baseRefName,closingIssuesReferences,commits,files,headRefName,headRefOid,"
    "mergeable,number,state,title,updatedAt,url"
)
CHECK_FIELDS = "bucket,completedAt,description,event,link,name,startedAt,state,workflow"


class CollectionError(RuntimeError):
    """Raised when evidence cannot be collected without guessing."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _run(
    command: Sequence[str],
    *,
    cwd: Path,
    timeout: int,
    allow_empty: bool = False,
    allowed_exit_codes: frozenset[int] = frozenset({0}),
) -> dict[str, Any]:
    if command and command[0] == "gh" and MUTATING_GH_VERBS.intersection(command[1:]):
        raise CollectionError(f"refusing mutating GitHub command: {' '.join(command)}")
    try:
        result = subprocess.run(
            list(command),
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
            shell=False,
        )
    except FileNotFoundError as exc:
        raise CollectionError(f"required executable not found: {command[0]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise CollectionError(
            f"command timed out after {timeout}s: {' '.join(command)}"
        ) from exc
    if result.returncode not in allowed_exit_codes:
        detail = result.stderr.strip() or result.stdout.strip() or "no diagnostic output"
        raise CollectionError(
            f"command failed with exit {result.returncode}: {' '.join(command)}: {detail}"
        )
    if not allow_empty and not result.stdout.strip():
        raise CollectionError(f"command returned empty output: {' '.join(command)}")
    return {
        "command": list(command),
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def _json_command(
    command: Sequence[str],
    *,
    cwd: Path,
    timeout: int,
    allowed_exit_codes: frozenset[int] = frozenset({0}),
) -> dict[str, Any]:
    capture = _run(
        command, cwd=cwd, timeout=timeout, allowed_exit_codes=allowed_exit_codes
    )
    try:
        payload = json.loads(capture["stdout"])
    except json.JSONDecodeError as exc:
        raise CollectionError(
            f"command returned invalid JSON: {' '.join(command)}: {exc}"
        ) from exc
    return {"capture": capture, "payload": payload}


def _repo_from_remote(remote: str) -> str | None:
    for pattern in REMOTE_PATTERNS:
        match = pattern.match(remote.strip())
        if match:
            return match.group("repo")
    return None


def _resolve_issue(
    issue: str, repo: str | None, *, project_root: Path, timeout: int
) -> tuple[str, int, dict[str, Any] | None]:
    match = ISSUE_URL.match(issue)
    if match:
        url_repo = f"{match.group('owner')}/{match.group('repo')}"
        if repo and repo != url_repo:
            raise CollectionError(
                f"--repo {repo!r} conflicts with issue URL repository {url_repo!r}"
            )
        return url_repo, int(match.group("number")), None
    if not issue.isdigit():
        raise CollectionError(
            "--issue must be an integer or https://github.com/OWNER/REPO/issues/NUMBER"
        )
    if repo:
        return repo, int(issue), None
    remote_capture = _run(
        ["git", "remote", "get-url", "origin"], cwd=project_root, timeout=timeout
    )
    inferred = _repo_from_remote(remote_capture["stdout"])
    if not inferred:
        raise CollectionError("cannot infer GitHub OWNER/REPO from origin; pass --repo")
    return inferred, int(issue), remote_capture


def _repository_evidence(
    project_root: Path, timeout: int, prior_remote: dict[str, Any] | None
) -> dict[str, Any]:
    remote = prior_remote or _run(
        ["git", "remote", "get-url", "origin"], cwd=project_root, timeout=timeout
    )
    head = _run(["git", "rev-parse", "HEAD"], cwd=project_root, timeout=timeout)
    status = _run(
        ["git", "status", "--porcelain=v1"],
        cwd=project_root,
        timeout=timeout,
        allow_empty=True,
    )
    symbolic = _run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=project_root,
        timeout=timeout,
    )
    default_branch = symbolic["stdout"].strip().rsplit("/", 1)[-1]
    base = _run(
        ["git", "rev-parse", f"origin/{default_branch}"],
        cwd=project_root,
        timeout=timeout,
    )
    return {
        "captured_at": _utc_now(),
        "project_root": str(project_root),
        "remote": remote["stdout"].strip(),
        "default_branch": default_branch,
        "base_sha": base["stdout"].strip(),
        "head_sha": head["stdout"].strip(),
        "tree_status": "clean" if not status["stdout"].strip() else "dirty",
        "commands": [remote, head, status, symbolic, base],
    }


def _atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect read-only GitHub incident, duplicate-search, PR, and git evidence."
    )
    parser.add_argument(
        "--issue", required=True, help="Issue number or full GitHub issue URL."
    )
    parser.add_argument("--repo", help="GitHub repository as OWNER/REPO.")
    parser.add_argument(
        "--project-root", type=Path, default=Path.cwd(), help="Repository checkout root."
    )
    parser.add_argument(
        "--output-dir", type=Path, required=True, help="New or existing evidence directory."
    )
    parser.add_argument(
        "--query", action="append", default=[], help="Duplicate-search query; repeatable."
    )
    parser.add_argument(
        "--max-queries",
        type=int,
        default=8,
        help="Maximum duplicate-search queries per run (default: 8).",
    )
    parser.add_argument("--pr", type=int, help="Linked pull request number to capture.")
    parser.add_argument("--timeout", type=int, default=30, help="Per-command timeout in seconds.")
    return parser


def collect(args: argparse.Namespace) -> dict[str, Any]:
    project_root = args.project_root.resolve()
    if not project_root.is_dir():
        raise CollectionError(f"project root is not a directory: {project_root}")
    if args.timeout <= 0:
        raise CollectionError("--timeout must be greater than zero")
    if args.max_queries <= 0:
        raise CollectionError("--max-queries must be greater than zero")
    if len(args.query) > args.max_queries:
        raise CollectionError(
            f"received {len(args.query)} queries; reduce to --max-queries={args.max_queries} "
            "high-signal queries and run first-pass and second-pass searches separately"
        )

    repo, issue_number, prior_remote = _resolve_issue(
        args.issue, args.repo, project_root=project_root, timeout=args.timeout
    )
    issue = _json_command(
        ["gh", "issue", "view", str(issue_number), "--repo", repo, "--json", ISSUE_FIELDS],
        cwd=project_root,
        timeout=args.timeout,
    )

    searches: list[dict[str, Any]] = []
    for query in args.query:
        if not query.strip():
            raise CollectionError("--query values must not be empty")
        result = _json_command(
            [
                "gh",
                "search",
                "issues",
                query,
                "--repo",
                repo,
                "--limit",
                "100",
                "--json",
                SEARCH_ISSUE_FIELDS,
            ],
            cwd=project_root,
            timeout=args.timeout,
        )
        searches.append({"kind": "issue", "state": "all", "query": query, **result})
        pr_result = _json_command(
            [
                "gh",
                "search",
                "prs",
                query,
                "--repo",
                repo,
                "--limit",
                "100",
                "--json",
                SEARCH_PR_FIELDS,
            ],
            cwd=project_root,
            timeout=args.timeout,
        )
        searches.append({"kind": "pull_request", "query": query, **pr_result})

    pull_request: dict[str, Any]
    if args.pr is None:
        pull_request = {"captured": False, "reason": "no --pr supplied"}
    else:
        view = _json_command(
            ["gh", "pr", "view", str(args.pr), "--repo", repo, "--json", PR_FIELDS],
            cwd=project_root,
            timeout=args.timeout,
        )
        checks = _json_command(
            ["gh", "pr", "checks", str(args.pr), "--repo", repo, "--json", CHECK_FIELDS],
            cwd=project_root,
            timeout=args.timeout,
            allowed_exit_codes=frozenset({0, 1, 8}),
        )
        pull_request = {
            "captured": True,
            "captured_at": _utc_now(),
            "view": view,
            "checks": checks,
        }

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "issue.json": {
            "schema_version": 1,
            "captured_at": _utc_now(),
            "repository": repo,
            "issue_number": issue_number,
            **issue,
        },
        "search.json": {
            "schema_version": 1,
            "captured_at": _utc_now(),
            "repository": repo,
            "queries": list(args.query),
            "results": searches,
        },
        "pull-request.json": {
            "schema_version": 1,
            "repository": repo,
            **pull_request,
        },
        "repository.json": {
            "schema_version": 1,
            **_repository_evidence(project_root, args.timeout, prior_remote),
        },
    }
    for name, payload in artifacts.items():
        _atomic_json(output_dir / name, payload)

    manifest = {
        "schema_version": 1,
        "captured_at": _utc_now(),
        "issue_url": f"https://github.com/{repo}/issues/{issue_number}",
        "read_only": True,
        "files": {
            name: {"sha256": _hash(output_dir / name), "bytes": (output_dir / name).stat().st_size}
            for name in sorted(artifacts)
        },
    }
    _atomic_json(output_dir / "evidence-manifest.json", manifest)
    return {
        "status": "ok",
        "issue_url": manifest["issue_url"],
        "output_dir": str(output_dir),
        "manifest": str(output_dir / "evidence-manifest.json"),
        "manifest_sha256": _hash(output_dir / "evidence-manifest.json"),
        "read_only": True,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        result = collect(args)
    except CollectionError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
