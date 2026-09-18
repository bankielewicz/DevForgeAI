#!/usr/bin/env python3
"""Capture a self-contained web artifact at deterministic local viewports."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit


VIEWPORTS = (("desktop", 1440, 900), ("mobile", 390, 844))
SETUP_GUIDANCE = (
    "Install the local renderer explicitly:\n"
    "  python -m pip install playwright\n"
    "  python -m playwright install chromium"
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_request_path(root: Path, target: str) -> Path:
    """Resolve one URL target beneath root, rejecting traversal before normalization."""
    raw_path = unquote(urlsplit(target).path)
    parts = [part for part in raw_path.replace("\\", "/").split("/") if part not in {"", "."}]
    if any(part == ".." for part in parts):
        raise ValueError("request path traversal rejected")
    relative = posixpath.normpath("/".join(parts))
    candidate = (root / relative).resolve(strict=False)
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("request path traversal rejected") from exc
    return candidate


def _handler(root: Path) -> type[BaseHTTPRequestHandler]:
    class ArtifactHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            try:
                path = _resolve_request_path(root, self.path)
                if path.is_dir():
                    path = path / "index.html"
                if not path.is_file():
                    self.send_error(404)
                    return
                data = path.read_bytes()
                suffix = path.suffix.lower()
                content_type = {
                    ".html": "text/html; charset=utf-8",
                    ".css": "text/css; charset=utf-8",
                    ".js": "text/javascript; charset=utf-8",
                    ".svg": "image/svg+xml",
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".webp": "image/webp",
                    ".woff2": "font/woff2",
                }.get(suffix, "application/octet-stream")
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(data)
            except ValueError:
                self.send_error(403)
            except (BrokenPipeError, ConnectionResetError):
                return

        def log_message(self, _format: str, *_args: object) -> None:
            return

    return ArtifactHandler


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def _base_manifest(artifact: Path, output: Path, port: int) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "artifact_path": Path(os.path.relpath(artifact, output)).as_posix(),
        "artifact_sha256": _sha256(artifact),
        "server_host": "127.0.0.1",
        "server_port": port,
        "browser": "chromium",
        "browser_version": "",
        "screenshots": [],
        "console_errors": [],
        "page_errors": [],
        "failed_requests": [],
    }


def capture(
    artifact: Path,
    output: Path,
    *,
    timeout_ms: int,
) -> dict[str, Any]:
    if timeout_ms < 10:
        raise TimeoutError("render readiness timeout")
    artifact = artifact.expanduser().resolve()
    output = output.expanduser().resolve()
    if not artifact.is_file() or artifact.stat().st_size == 0:
        raise ValueError("artifact is missing or empty")
    try:
        artifact.read_text(encoding="utf-8")
    except UnicodeError as exc:
        raise ValueError("artifact must be UTF-8 HTML") from exc
    output.mkdir(parents=True, exist_ok=True)

    cleanup_error: Exception | None = None
    browser = None
    playwright = None
    server = None
    thread = None
    manifest: dict[str, Any] | None = None
    try:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError(SETUP_GUIDANCE) from exc
        playwright = sync_playwright().start()
        try:
            browser = playwright.chromium.launch(headless=True)
        except Exception as exc:
            raise RuntimeError(f"Chromium is unavailable. {SETUP_GUIDANCE}") from exc
        server = ThreadingHTTPServer(("127.0.0.1", 0), _handler(artifact.parent))
        server.daemon_threads = True
        port = int(server.server_address[1])
        manifest = _base_manifest(artifact, output, port)
        thread = threading.Thread(
            target=server.serve_forever,
            name="design-artifact-server",
            daemon=True,
        )
        thread.start()
        manifest["browser_version"] = browser.version
        url = f"http://127.0.0.1:{port}/{artifact.name}"
        for name, width, height in VIEWPORTS:
            context = browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=1,
                service_workers="block",
            )
            page = context.new_page()
            page.on(
                "console",
                lambda message: manifest["console_errors"].append(message.text)
                if message.type == "error" else None,
            )
            page.on("pageerror", lambda error: manifest["page_errors"].append(str(error)))
            page.on(
                "requestfailed",
                lambda request: manifest["failed_requests"].append(
                    {"url": request.url, "failure": request.failure or "request failed"}
                ),
            )
            page.on(
                "response",
                lambda response: manifest["failed_requests"].append(
                    {"url": response.url, "status": response.status}
                ) if response.status >= 400 else None,
            )

            def route_request(route: Any) -> None:
                parsed = urlsplit(route.request.url)
                if parsed.hostname != "127.0.0.1" or parsed.port != port:
                    manifest["failed_requests"].append(
                        {"url": route.request.url, "failure": "external request blocked"}
                    )
                    route.abort()
                    return
                route.continue_()

            page.route("**/*", route_request)
            try:
                page.goto(url, wait_until="load", timeout=timeout_ms)
                page.evaluate("document.fonts ? document.fonts.ready : Promise.resolve()")
                page.wait_for_timeout(100)
                screenshot = output / f"{name}.png"
                page.screenshot(path=str(screenshot), full_page=False, animations="disabled")
                if not screenshot.is_file() or screenshot.stat().st_size == 0:
                    raise RuntimeError(f"{name} screenshot missing or empty")
                manifest["screenshots"].append({
                    "name": name,
                    "path": screenshot.name,
                    "width": width,
                    "height": height,
                    "sha256": _sha256(screenshot),
                })
            finally:
                context.close()
        if len(manifest["screenshots"]) != len(VIEWPORTS):
            raise RuntimeError("required screenshots are missing")
        if manifest["console_errors"] or manifest["page_errors"] or manifest["failed_requests"]:
            raise RuntimeError("render emitted console, page, or request errors")
        if _sha256(artifact) != manifest["artifact_sha256"]:
            raise RuntimeError("artifact hash changed during capture")
        for record in manifest["screenshots"]:
            if _sha256(output / record["path"]) != record["sha256"]:
                raise RuntimeError("screenshot hash mismatch")
        return manifest
    except Exception as exc:
        if manifest is not None:
            setattr(exc, "render_manifest", manifest)
        raise
    finally:
        try:
            if browser is not None:
                browser.close()
            if playwright is not None:
                playwright.stop()
        except Exception as exc:  # cleanup failure is blocking
            cleanup_error = exc
        if server is not None and thread is not None:
            try:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)
                if thread.is_alive():
                    raise RuntimeError("server cleanup timeout")
            except Exception as exc:
                cleanup_error = cleanup_error or exc
        if cleanup_error is not None and sys.exc_info()[0] is None:
            raise RuntimeError(f"renderer cleanup failure: {cleanup_error}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--format", choices=["json"], default=None)
    args = parser.parse_args(argv)
    timeout_text = os.environ.get("DEVFORGEAI_CAPTURE_TIMEOUT_MS", "30000")
    try:
        timeout_ms = int(timeout_text)
        if timeout_ms <= 0:
            raise ValueError
    except ValueError:
        timeout_ms = 30000

    try:
        manifest = capture(
            Path(args.artifact),
            Path(args.output_dir),
            timeout_ms=timeout_ms,
        )
        _atomic_json(Path(args.output_dir).resolve() / "render-manifest.json", manifest)
        if args.format == "json":
            print(json.dumps(manifest, sort_keys=True, separators=(",", ":")))
        else:
            print(f"Captured desktop.png and mobile.png in {Path(args.output_dir)}")
            print(f"Manifest: {Path(args.output_dir) / 'render-manifest.json'}")
        return 0
    except Exception as exc:
        manifest = getattr(exc, "render_manifest", None)
        payload = dict(manifest or {})
        payload["error"] = str(exc)
        if args.format == "json":
            print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
            if "playwright" in str(exc).lower() or "chromium" in str(exc).lower():
                print(SETUP_GUIDANCE, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
