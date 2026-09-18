"""Whole-file text candidates and conservative Markdown resource observations.

Candidates never adjudicate semantic defects. No target script is imported or
executed; network resources and renderer-specific anchors remain unresolved.
"""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit

import observe

TEXT_EXTENSIONS = {'.md','.txt','.py','.ps1','.sh','.json','.jsonl','.yaml','.yml','.toml','.xml','.html','.css','.js','.ts','.tsx','.rs','.csv','.svg','.sql','.ini','.cfg','.license'}
SPECIAL = {0x200E,0x200F,0x061C,0x200B,0x200C,0x200D,0x2060,0xFEFF,0x00AD,0x034F,0x00A0,0x202F}


import skill_format
from skill_format import frontmatter


def check(rule, subject, result, reason, applicability='applicable', required=True, discriminator=''):
    return {'schema_version':'1','run_id':'helper','check_id':rule + '-' + observe.sha256((subject+discriminator).encode())[:12], 'rule_id':rule,'subject_path':subject,'method':'deterministic','required':required,'applicability':applicability,'result':result,'reason':reason,'evidence':[]}


def redacted_excerpt(text, position):
    # Whole surrounding material can contain secrets. Candidate-only excerpts
    # retain useful escaped codepoints without emitting adjacent private values.
    return text[position].encode('unicode_escape').decode('ascii')[:160]


def protocol_value_spans(path, text):
    """Locate original JSON/JSONL schema_version scalar spans, not quoted examples."""
    if PurePosixPath(path).suffix.lower() not in ('.json', '.jsonl'):
        return []
    strings = re.finditer(r'"(?:[^"\\\x00-\x1f]|\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4}))*"', text)
    spans, previous = [], None
    for token in strings:
        if previous is not None and re.fullmatch(r'[ \t\r\n]*:[ \t\r\n]*', text[previous.end():token.start()]):
            if json.loads(previous[0]) == 'schema_version':
                spans.append((token.start() + 1, token.end() - 1))
        previous = token
    return spans


def candidates(path, text):
    result, offset, line, column = [], 0, 1, 1
    lines = text.splitlines()
    in_meta = text.startswith('---')
    protocol_spans = iter(protocol_value_spans(path, text))
    protocol_span = next(protocol_spans, None)
    for position, char in enumerate(text):
        while protocol_span is not None and position >= protocol_span[1]:
            protocol_span = next(protocol_spans, None)
        in_protocol = protocol_span is not None and protocol_span[0] <= position < protocol_span[1]
        cp = ord(char)
        current = lines[line-1] if line <= len(lines) else ''
        context = 'fixture' if any(part in ('tests','fixtures','evals') for part in PurePosixPath(path).parts) else 'prose'
        if in_meta and position < text.find('\n---', 3):
            context = 'metadata'
        elif re.search(r'`|\b(?:python|pwsh|bash|sh|cmd|node|cargo)\b', current):
            context = 'command'
        elif re.search(r'\]\(|(?:^|\s)[\w.-]+[/\\]', current):
            context = 'path'
        if in_protocol:
            context = 'unknown'
        special = (cp < 32 and cp not in (9,10,13)) or 0x7F <= cp <= 0x9F or cp in SPECIAL or 0x202A <= cp <= 0x202E or 0x2066 <= cp <= 0x2069 or 0xFE00 <= cp <= 0xFE0F or 0xE0100 <= cp <= 0xE01EF or 0xE0000 <= cp <= 0xE007F
        normalized = unicodedata.normalize('NFKC', char)
        nfkc = normalized != char and (in_protocol or context in ('metadata','command','path'))
        if special or nfkc:
            reason = 'Candidate only; inspect behavioral ambiguity and legitimate context.'
            if in_protocol:
                reason += ' Exact JSON protocol identifier (schema_version).'
            if nfkc:
                reason += ' NFKC candidate ' + char.encode('unicode_escape').decode() + ' -> ' + normalized.encode('unicode_escape').decode() + '; source unchanged; not exhaustive confusable detection.'
            result.append({'path':path,'start_byte':offset,'end_byte':offset+len(char.encode('utf-8')),'line':line,'column':column,'codepoint':f'U+{cp:04X}','unicode_name':unicodedata.name(char,'UNNAMED CONTROL'),'escaped_excerpt':redacted_excerpt(text,position),'context':context,'disposition':'unresolved','reason':reason})
        offset += len(char.encode('utf-8'))
        if char in ('\n','\v','\f','\r','\x1c','\x1d','\x1e','\x85','\u2028','\u2029') and not (char == '\r' and position+1 < len(text) and text[position+1] == '\n'):
            line, column = line+1, 1
        else:
            column += 1
    return result


def unfenced(text):
    """Preserve line numbers while excluding backtick/tilde fenced examples."""
    rows, fence = [], None
    for line in text.splitlines():
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if marker:
            token, tail = marker[1], marker[2]
            if fence is None:
                if token[0] == '`' and '`' in tail:
                    rows.append(line)
                    continue
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not tail.strip(' \t'):
                fence = None
            rows.append('')
        else:
            rows.append('' if fence else line)
    return rows, fence is not None


def anchors(text):
    rows, _ = unfenced(text)
    result, seen = set(), {}
    for i, line in enumerate(rows):
        result.update(re.findall(r'\bid\s*=\s*[\"\']([^\"\']+)[\"\']', line))
        match = re.match(r'^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$', line)
        title = match[1] if match else (rows[i-1] if i and re.match(r'^ {0,3}(?:=+|-+)\s*$',line) else None)
        if title:
            # Conservative specified slug subset. Other renderers are unresolved.
            slug = re.sub(r'[^\w\s-]', '', title.lower()).replace('_','')
            slug = re.sub(r'\s','-',slug.strip())
            count = seen.get(slug,0)
            seen[slug] = count+1
            result.add(slug + ('-' + str(count) if count else ''))
    return result


def links(text):
    rows, unmatched = unfenced(text)
    definitions = {}
    for line in rows:
        match = re.match(r'^ {0,3}\[([^\]]+)\]:\s*<?([^\s>]+)>?', line)
        if match:
            definitions[match[1].strip().lower()] = match[2]
    result = []
    for number, line in enumerate(rows,1):
        # Inline code is example data, not Markdown resource syntax.
        line = re.sub(r'(`+)(.+?)\1',lambda m:' ' * len(m[0]),line)
        if re.match(r'^ {0,3}\[[^\]]+\]:',line):
            continue
        used = []
        for match in re.finditer(r'(!?)\[([^\]]*)\]\(',line):
            start, cursor, depth = match.end(), match.end(), 1
            while cursor < len(line) and depth:
                if line[cursor] == '\\':
                    cursor += 2
                    continue
                if line[cursor] == '(':
                    depth += 1
                elif line[cursor] == ')':
                    depth -= 1
                cursor += 1
            if depth:
                result.append((number,'unresolved-reference:ambiguous-destination','image' if match[1] else 'link'))
                continue
            body = line[start:cursor-1].strip()
            target = body[1:body.find('>')] if body.startswith('<') and '>' in body else body.split()[0] if body else ''
            if target:
                result.append((number,re.sub(r'\\([()])',r'\1',target),'image' if match[1] else 'link'))
                used.append((match.start(),cursor))
        for match in re.finditer(r'(!?)\[([^\]]+)\](?:\[([^\]]*)\])?',line):
            if any(start <= match.start() < end for start,end in used):
                continue
            label = (match[3] or match[2]).strip().lower()
            if label in definitions:
                result.append((number, definitions[label], 'image' if match[1] else 'link'))
            elif match[3] is not None:
                result.append((number, 'unresolved-reference:' + label, 'image' if match[1] else 'link'))
    return result, unmatched


def resolve(source, target, texts, paths):
    if target.startswith('unresolved-reference:'):
        return 'dynamic', None
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or parsed.path.startswith('/') or '\\' in target:
        return 'outside_scope', None
    if any(x in target for x in ('${','<','>','*','{{')):
        return 'dynamic', None
    parts = list(PurePosixPath(source).parent.parts)
    if parsed.path:
        for part in unquote(parsed.path).split('/'):
            if part == '..':
                if not parts:
                    return 'outside_scope', None
                parts.pop()
            elif part not in ('','.'): 
                parts.append(part)
        destination = '/'.join(parts)
    else:
        destination = source
    if destination not in paths:
        return 'missing', destination
    if parsed.fragment and (destination not in texts or unquote(parsed.fragment) not in anchors(texts[destination])):
        return 'unsupported_anchor', destination
    return 'resolved', destination


def local_tokenizer(name, encoding):
    if name is None:
        return None, None, 'Tokenizer not selected; token counts NOT_RUN.'
    if name != 'tiktoken' or not encoding:
        raise ValueError('only installed tiktoken with explicit encoding is supported')
    try:
        import tiktoken
        import tiktoken.load
        def cached_only(locator, expected_hash=None):
            cache = os.environ.get('TIKTOKEN_CACHE_DIR', os.environ.get('DATA_GYM_CACHE_DIR', str(Path(tempfile.gettempdir()) / 'data-gym-cache')))
            if not cache:
                raise OSError('local tokenizer cache disabled')
            path = Path(cache) / hashlib.sha1(locator.encode()).hexdigest()
            data = observe.read_stable(observe.safe_path(path))
            if expected_hash and hashlib.sha256(data).hexdigest() != expected_hash:
                raise OSError('local tokenizer cache hash mismatch')
            return data
        old = tiktoken.load.read_file_cached
        tiktoken.load.read_file_cached = cached_only
        try:
            tokenizer = tiktoken.get_encoding(encoding)
        finally:
            tiktoken.load.read_file_cached = old
        return tokenizer, {'name':'tiktoken','version':importlib.metadata.version('tiktoken'),'encoding':encoding}, 'Named installed tokenizer; local data only.'
    except (ImportError, ValueError, OSError, observe.ObservationError) as error:
        return None, None, 'Token counts NOT_RUN: installed tokenizer/local encoding unavailable (' + type(error).__name__ + '). No download.'


def package(source, tokenizer_name=None, encoding=None):
    root = observe.safe_path(source)
    import adaptive_contracts as contracts
    files, exclusions = contracts.inventory(root,allow_exclusions=True)
    texts, raw, checks, limitations, nodes = {}, {}, [], [], []
    for relative, path, info in files:
        if contracts.excluded(Path(relative)):
            exclusions.append({'path':relative,'reason':'excluded/generated boundary'})
            continue
        data = observe.read_stable(path,info)
        raw[relative] = data
        known = path.suffix.lower() in TEXT_EXTENSIONS or path.name in ('LICENSE','NOTICE','Makefile')
        try:
            text = data.decode('utf-8')
            if known or '\0' not in text:
                texts[relative] = text
        except UnicodeError:
            if known:
                checks.append(check('AV-F01',relative,'FAIL','Declared text cannot decode as UTF-8.'))
        classification = 'text (known extension)' if known else ('text (UTF-8/no NUL)' if relative in texts else 'binary')
        nodes.append({'path':relative,'role':'unknown','reachable':False,'usage':'unresolved_usage','evidence':[],'reason':classification + '; consumers require review.'})
    if exclusions:
        limitations.extend('NOT_RUN omitted: ' + row['path'] for row in exclusions)
        checks.append(check('AV-E01','capture','NOT_RUN','Excluded scope prevents whole-package observation.'))
    entry_meta = None
    if 'SKILL.md' not in texts:
        if not any(row['rule_id']=='AV-F01' and row['subject_path']=='SKILL.md' for row in checks):
            checks.append(check('AV-F01','SKILL.md','FAIL','Exact UTF-8 entrypoint missing or undecodable.'))
    else:
        try:
            meta = entry_meta = frontmatter(texts['SKILL.md'])
            checks.append(check('AV-F01','SKILL.md','PASS','Parsed unique-key YAML mapping and required strings; optional fields preserved.'))
            identity_result = 'PASS' if meta['name'] == root.name else 'NOT_RUN' if root.name == 'source' else 'FAIL'
            checks.append(check('AV-F02','SKILL.md',identity_result,'Name/directory identity; a source-named snapshot needs its original bound identity; semantic routing and selected limits require review.'))
            unknown = set(meta)-set(skill_format.SUPPORTED_FIELDS)
            if unknown:
                checks.append(check('AV-F01','metadata-extensions','NOT_RUN','Unknown optional fields need selected host guidance.','unknown'))
        except ImportError:
            checks.append(check('AV-F01','SKILL.md','NOT_RUN','Installed PyYAML unavailable.'))
        except Exception as error:
            checks.append(check('AV-F01','SKILL.md','FAIL','Metadata parse/type failure: ' + type(error).__name__))
    edges, adjacency = [], {path:set() for path in raw}
    for path,text in texts.items():
        if Path(path).suffix.lower() != '.md':
            continue
        parsed, unmatched = links(text)
        if unmatched:
            checks.append(check('AV-F05',path,'NOT_RUN','Unmatched fence candidate; inspect whether content interpretation is broken.'))
        if re.search(r'\b(?:TODO|TBD)\b|\[INSERT\b|REPLACE[_ -]ME',text):
            checks.append(check('AV-F05',path+'-placeholders','NOT_RUN','Placeholder candidates present; distinguish production gaps from quoted fixtures.'))
        for line,target,kind in parsed:
            resolution, dest = resolve(path,target,texts,set(raw))
            secret_locator = bool(re.search(r'(?i)(?:token|password|secret|api[_-]?key)=|://[^/\s]+:[^/\s]+@',target))
            safe_target = '[redacted-resource-locator]' if secret_locator else target
            edges.append({'source':path,'line':line,'target':safe_target,'kind':kind,'resolution':resolution})
            if resolution == 'resolved':
                adjacency[path].add(dest)
            elif resolution == 'missing':
                checks.append(check('AV-R01',path,'FAIL','Referenced local resource is missing; see located resource edge.',discriminator=str(line)+target))
            elif resolution in ('dynamic','unsupported_anchor'):
                checks.append(check('AV-R01',path,'NOT_RUN','Dynamic/reference syntax or renderer anchor needs manual resolution.',discriminator=str(line)+target))
    # Claude Code reads no separate configuration file: every host-read field is in
    # the SKILL.md frontmatter. AV-F04 therefore covers the optional frontmatter fields
    # rather than another host's configuration document. The entrypoint was parsed once
    # above and AV-F01 carries any parse failure, so one malformed field cannot produce
    # two required FAIL rows against the same bytes.
    if entry_meta is None:
        checks.append(check('AV-F04','SKILL.md','NOT_APPLICABLE','Entrypoint metadata did not resolve; AV-F01 carries that failure and optional fields cannot be read.','not_applicable'))
    else:
        optional = set(entry_meta) - {'name', 'description'}
        unknown = optional - set(skill_format.SUPPORTED_FIELDS)
        if unknown:
            checks.append(check('AV-F04','SKILL.md','NOT_RUN','Unknown frontmatter extensions need applicable guidance: ' + ', '.join(sorted(unknown)),'unknown'))
        elif optional:
            checks.append(check('AV-F04','SKILL.md','PASS','Supported optional frontmatter fields and value domains checked.'))
        else:
            checks.append(check('AV-F04','SKILL.md','PASS','No optional frontmatter fields declared.'))
        # A divergence between the Claude Code reference and the Agent Skills
        # specification is information for a reviewer, never a defect, and must stay out
        # of the required reduction: observe.reduce_checks treats a required row with
        # unknown applicability or a NOT_RUN result as incomplete, so emitting these as
        # required would reduce every Claude Code package that uses a YAML-list tool
        # grant to INCOMPLETE. Each divergence gets its own discriminator so several
        # cannot collide on one check identity.
        for rule_id, _, message in skill_format.advisory_checks(entry_meta):
            checks.append(check('AV-F04','SKILL.md','NOT_RUN','Recorded source divergence, not a defect: ' + message,
                                required=False, discriminator=rule_id))
    for foreign in sorted(path for path in raw if path.startswith('agents/') and path.endswith(('.yaml','.yml'))):
        checks.append(check('AV-F04',foreign,'NOT_RUN','Claude Code reads no separate metadata file; unread configuration from another host needs a disposition decision.','unknown'))
    reachable, pending = set(), [p for p in ('SKILL.md',) if p in raw]
    while pending:
        path = pending.pop()
        if path not in reachable:
            reachable.add(path)
            pending.extend(adjacency[path]-reachable)
    roles = {}
    descriptor = 'assets/devforgeai-skill.json'
    if descriptor in raw:
        try:
            value = contracts.shape(observe.strict_json(raw[descriptor]))
            contracts.Reader().descriptor(value)
            roles = {row['path']:row['role'] for row in value['resource_roles']}
            checks.append(check('AV-A04',descriptor,'PASS','Descriptor shape/role checked; identity leakage, contract/helper reachability and lineage require review.'))
        except (ValueError, TypeError, KeyError):
            checks.append(check('AV-A04',descriptor,'FAIL','Invalid adaptive descriptor.'))
    for node in nodes:
        node['reachable'] = node['path'] in reachable
        node['role'] = roles.get(node['path'],'unknown')
    encoder, identity, token_reason = local_tokenizer(tokenizer_name, encoding)
    counts = [{'path':path,'bytes':len(raw[path]),'characters':len(text),'lines':len(text.splitlines()),'tokens':len(encoder.encode(text,disallowed_special=())) if encoder else None} for path,text in sorted(texts.items())]
    unicode = [row for path,text in sorted(texts.items()) for row in candidates(path,text)]
    checks.append(check('AV-U01','text-scan','NOT_RUN' if unicode else 'PASS','Whole captured text scanned; candidate adjudication pending.' if unicode else 'Whole captured text scanned; no specified candidates. Not exhaustive confusable coverage.'))
    checks.append(check('AV-C01','text-counts','PASS','Exact bytes/code points/splitlines counts for classified text; load evidence and required budgets separate.'))
    limitations += [token_reason,'Resource roles do not establish usage; command/template/dynamic consumers need manual inspection.', 'No semantic, native activation, project-binding or security approval is inferred.']
    return checks, {'unicode_candidates':unicode,'resources':nodes,'edges':edges,'context':{'tokenizer':identity,'files':counts,'loads':[],'budget':None,'budget_result':'NOT_APPLICABLE','reason':'No budget selected. ' + token_reason}}, limitations
