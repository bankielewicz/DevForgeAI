"""Read-only package, selected-set intake and adaptive record observations."""
import argparse
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
import observe
import adaptive_contracts as contracts
import text_resources

CORE_RULES = ('AV-F01','AV-F02','AV-F03','AV-F04','AV-F05','AV-U01','AV-R01','AV-R02','AV-R03',
              'AV-I01','AV-I02','AV-I03','AV-I04','AV-C01','AV-S01','AV-S02','AV-W01','AV-W02','AV-E01')
ADAPTIVE_RULES = tuple('AV-A%02d' % i for i in range(1,11))
ALL_RULES = CORE_RULES + ADAPTIVE_RULES


def check_rows(data, root, run_id=None, complete=False):
    rows = [observe.strict_json(line) for line in data.decode('utf-8').splitlines() if line.strip()]
    contracts.require(bool(rows) or not complete, 'empty member checks')
    ids = set()
    required = {'schema_version','run_id','check_id','rule_id','subject_path','method','required','applicability','result','reason','evidence'}
    for row in rows:
        contracts.require(type(row) is dict and required <= row.keys() <= required | {'dimension'}, 'schema-1 check fields')
        contracts.require(row['schema_version'] == '1' and type(row['required']) is bool, 'schema-1 identity/type')
        contracts.require(all(type(row[k]) is str and row[k] for k in ('run_id','check_id','rule_id','subject_path','reason')), 'nonempty check identity/reason')
        contracts.require(observe.normalized_relative(row['subject_path']) and '\0' not in row['subject_path'], 'invalid schema-1 subject_path')
        contracts.require(run_id is None or row['run_id'] == run_id, 'wrong check run')
        contracts.require(row['check_id'] not in ids, 'duplicate check identity')
        ids.add(row['check_id'])
        contracts.require(row['method'] in ('deterministic','semantic','behavioral'), 'invalid check method')
        contracts.require(row['applicability'] in ('applicable','unknown','not_applicable') and row['result'] in ('PASS','FAIL','NOT_RUN','ERROR','NOT_APPLICABLE'), 'check applicability/result')
        contracts.require(row['applicability'] != 'unknown' or row['result'] == 'NOT_RUN', 'unknown applicability must be NOT_RUN')
        contracts.require((row['applicability'] == 'not_applicable') == (row['result'] == 'NOT_APPLICABLE'), 'NOT_APPLICABLE requires justified applicability')
        if 'dimension' in row:
            contracts.require(row['dimension'] in (*observe.DIMENSIONS,*observe.DIMENSION_ALIASES), 'unknown dimension')
        contracts.require(type(row['evidence']) is list, 'check evidence array')
        for ref in row['evidence']:
            contracts.require(type(ref) is dict and set(ref) == {'path','sha256'} and observe.normalized_relative(ref['path']) and '\0' not in ref['path'], 'schema-1 evidence must be run-relative')
            path = observe.safe_path(root / ref['path'])
            contracts.require(observe.within(path,root) and observe.sha256(observe.read_stable(path)) == ref['sha256'], 'schema-1 evidence mismatch')
    if complete:
        contracts.require(set(ALL_RULES) <= {row['rule_id'] for row in rows if row['required']}, 'missing required AV coverage rows (including inapplicable/unknown)')
    return rows


def reduction(rows):
    value = observe.reduce_checks(rows)
    value['unknown_applicability'] = sum(row['required'] and row['applicability'] == 'unknown' for row in rows)
    return value


def dimension(rule):
    if rule.startswith(('AV-F','AV-U','AV-R','AV-E','AV-C')):
        return 'standards'
    if rule.startswith(('AV-I','AV-S')):
        return 'instructions'
    if rule in ('AV-W02','AV-A05','AV-A10'):
        return 'behavior'
    return 'workflow'


def member_outcome(rows, source_state):
    dimensions = {name: reduction([row for row in rows if observe.DIMENSION_ALIASES.get(row.get('dimension'),row.get('dimension',dimension(row['rule_id']))) == name]) for name in observe.DIMENSIONS}
    values = [row['outcome'] for row in dimensions.values()]
    outcome = 'FAIL' if 'FAIL' in values else 'INCOMPLETE' if 'INCOMPLETE' in values or source_state != 'UNCHANGED' else 'PASS'
    return outcome, dimensions


def assess_record(value, reader, path):
    contracts.shape(value)
    reader.refs(value)
    input_value = observe.strict_json(reader.ref(value['input']))
    reader.record(input_value, value['input']['path'])
    contracts.require(input_value['schema_version'] in ('standalone-set-input-v1','set-validation-request-v1'), 'unsupported set input')
    standalone = input_value['schema_version'] == 'standalone-set-input-v1'
    for field in ('scope','omitted_member_ids','omitted_handoff_ids'):
        expected = ('full_set' if field == 'scope' else []) if standalone else input_value[field]
        contracts.require(value[field] == expected, 'assessment scope/omissions differ from immutable input')
    selected = contracts.index(input_value['members'],'member_id')
    members = contracts.index(value['members'],'member_id')
    contracts.require(members.keys() == selected.keys(), 'assessment membership mismatch')
    rows, outcomes = [], []
    seen_refs = set()
    for key, member in members.items():
        contracts.require(member['package_digest'] == selected[key]['package']['package_digest'], 'assessed member digest mismatch')
        if member['report'] is None or member['checks'] is None:
            contracts.require(member['outcome'] == 'INCOMPLETE', 'missing report/checks require INCOMPLETE')
            outcomes.append('INCOMPLETE')
            if member['checks'] is not None:
                check_path = reader.absolute(member['checks']['path'])
                contracts.require(str(check_path) not in seen_refs, 'member checks counted twice')
                seen_refs.add(str(check_path))
                rows.extend(check_rows(reader.ref(member['checks']),check_path.parent,complete=True))
            else:
                # Known catalog obligations stay unperformed; no available
                # failures or evaluated rows are discarded when only report is missing.
                rows.extend(dict(text_resources.check(rule,'members/'+key,'NOT_RUN','Member checks unavailable.','unknown'), check_id=key+'-'+rule) for rule in ALL_RULES)
            continue
        check_path = reader.absolute(member['checks']['path'])
        contracts.require(str(check_path) not in seen_refs, 'member checks counted twice')
        seen_refs.add(str(check_path))
        checks = check_rows(reader.ref(member['checks']), check_path.parent, complete=True)
        expected, _ = member_outcome(checks, member['source_state'])
        contracts.require(member['outcome'] == expected, 'member outcome reduction mismatch')
        # A report Ref binds bytes; passage support remains manual, not guessed
        # from headings or a word PASS in arbitrary Markdown.
        reader.ref(member['report'])
        outcomes.append(expected)
        rows.extend(checks)
    integration_path = reader.absolute(value['integration_checks']['path'])
    integration = check_rows(reader.ref(value['integration_checks']), integration_path.parent, value['run_id'])
    handoffs = contracts.index(input_value['handoffs'])
    for row in integration:
        prefix, _, ident = row['subject_path'].partition('/')
        contracts.require((prefix == 'handoffs' and ident in handoffs) or (prefix == 'members' and ident in selected), 'integration logical subject outside selection')
    for handoff in handoffs.values():
        contracts.require(any(row['subject_path'] == 'handoffs/'+handoff['id'] and row['required'] for row in integration), 'missing required integration coverage')
    rows.extend(integration)
    aggregate = reduction(rows)
    outcomes.append(aggregate['outcome'])
    if standalone and input_value['gaps']:
        outcomes.append('INCOMPLETE')
    expected = 'FAIL' if 'FAIL' in outcomes else 'INCOMPLETE' if 'INCOMPLETE' in outcomes else 'PASS'
    contracts.require(value['outcome'] == expected, 'set outcome reduction mismatch')
    for field in ('required_total','required_evaluated','unknown_applicability'):
        contracts.require(value[field] == aggregate[field], 'tampered '+field)
    if value['prior_assessment']:
        prior = observe.strict_json(reader.ref(value['prior_assessment']))
        contracts.shape(prior)
        contracts.require(prior['schema_version'] == 'set-assessment-v1' and prior['run_id'] != value['run_id'], 'invalid prior assessment linkage')


def supplemental(value, reader):
    contracts.shape(value)
    reader.refs(value)
    files = contracts.index(value['context']['files'],'path')
    resources = contracts.index(value['resources'],'path')
    for candidate in value['unicode_candidates']:
        contracts.require(candidate['path'] in files and candidate['start_byte'] < candidate['end_byte'] <= files[candidate['path']]['bytes'], 'Unicode candidate interval')
        contracts.require(re.fullmatch(r'U\+[0-9A-F]{4,6}',candidate['codepoint']) is not None, 'Unicode codepoint format')
    for edge in value['edges']:
        contracts.require(edge['source'] in resources, 'edge source absent from resource inventory')
    context = value['context']
    if context['tokenizer'] is None:
        contracts.require(all(row['tokens'] is None for row in files.values()) and all(row['tokens'] is None for row in context['loads']), 'tokens without named tokenizer')
    else:
        contracts.require(context['tokenizer']['name'] == 'tiktoken', 'unsupported tokenizer')
    for load in context['loads']:
        contracts.require(load['path'] in files, 'load outside counted content')
        contracts.require(load['basis'] == 'static_estimate' or bool(load['evidence']), 'observed load lacks evidence')
    budget = context['budget']
    if budget is None:
        contracts.require(context['budget_result'] == 'NOT_APPLICABLE', 'budget result without selected budget')
    else:
        contracts.require((budget['scope'] == 'entrypoint') == (budget['case_id'] is None), 'budget case/scope')
        measured = None
        if budget['scope'] == 'entrypoint':
            measured = files.get('SKILL.md',{}).get(budget['unit'])
        else:
            loads = [row for row in context['loads'] if row['case_id'] == budget['case_id']]
            if loads:
                if budget['scope'] == 'unique_branch_content':
                    values = [files[path][budget['unit']] for path in {row['path'] for row in loads}]
                elif budget['unit'] == 'tokens':
                    values = [None if row['tokens'] is None or row['basis'] == 'static_estimate' else row['tokens'] * row['occurrences'] for row in loads]
                else:
                    values = [files[row['path']][budget['unit']] * row['occurrences'] if row['basis'] == 'observed_full_file' else None for row in loads]
                if all(item is not None for item in values):
                    measured = sum(values)
        expected = 'NOT_RUN' if measured is None else 'PASS' if measured <= budget['maximum'] else 'FAIL'
        contracts.require(context['budget_result'] == expected, 'budget measurement/result mismatch')
    for binding in value['bindings']:
        raw = observe.strict_json(reader.ref(binding['observation']))
        contracts.shape(raw)
        contracts.require(raw['schema_version'] == 'binding-observation-v1' and raw['status'] == binding['observed'] and raw['binding_sha256'] == binding['binding_sha256'], 'binding observation mismatch')


def records(root):
    root = observe.safe_path(root)
    reader, checked, errors = contracts.Reader(), [], []
    # Evaluator authority is explicit top-level versioned records. Never descend
    # into source, inputs, trials, or a fixture named findings.json.
    for path in sorted(root.iterdir()):
        if path.suffix != '.json' or not path.is_file():
            continue
        try:
            value = observe.strict_json(reader.read(path))
            version = value.get('schema_version') if type(value) is dict else None
            if version == '1':
                continue  # Existing observe.py owns this family and its base.
            contracts.require(version in contracts.VERSIONS, 'unknown new record family')
            if version == 'set-assessment-v1':
                assess_record(value,reader,path)
            elif version == 'adaptive-observations-v1':
                supplemental(value,reader)
            elif version == 'adaptive-check-observation-v1':
                contracts.shape(value)
                rows = check_rows(('\n'.join(json.dumps(x) for x in value['checks'])).encode(),root,'helper')
                expected_keys = {'package':{'unicode_candidates','resources','edges','context'},'intake-set':{'input_kind','ordered_member_ids','member_bindings'},'records':{'checked_records','errors'}}
                contracts.require(set(value['observations']) == expected_keys[value['command']], 'helper command-specific fields')
                if any(row['required'] and row['result'] == 'FAIL' for row in rows):
                    contracts.require(value['status'] == 'MISMATCH', 'helper status hides required failure')
                if value['command'] == 'records' and value['observations']['errors']:
                    contracts.require(value['status'] == 'MISMATCH', 'helper status hides record errors')
                if value['command'] == 'package':
                    observation = value['observations']
                    files = contracts.index(observation['context']['files'],'path')
                    for candidate in observation['unicode_candidates']:
                        contracts.require(candidate['disposition'] == 'unresolved', 'raw helper cannot adjudicate Unicode')
                        contracts.require(candidate['path'] in files and candidate['start_byte'] < candidate['end_byte'] <= files[candidate['path']]['bytes'], 'raw Unicode interval')
                    contracts.require(all(node['usage'] == 'unresolved_usage' for node in observation['resources']), 'raw helper cannot adjudicate resource usage')
                    if any(row['required'] and row['result'] in ('NOT_RUN','ERROR') for row in rows) and not any(row['required'] and row['result'] == 'FAIL' for row in rows):
                        contracts.require(value['status'] == 'INCOMPLETE', 'raw package hides pending observations')
            else:
                reader.record(value,str(path))
            checked.append(path.name)
        except (ValueError,KeyError,TypeError,UnicodeError,observe.ObservationError,OSError,RecursionError) as error:
            errors.append(path.name+': '+str(error))
    try:
        reader.readback()
    except (ValueError, OSError, observe.ObservationError) as error:
        errors.append('readback: '+str(error))
    if not checked and not errors:
        errors.append('No supported new evaluator records; use observe.py for schema-1.')
    return checked,errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest='command',required=True)
    package = modes.add_parser('package')
    package.add_argument('--source',required=True)
    package.add_argument('--tokenizer',choices=['tiktoken'])
    package.add_argument('--encoding')
    intake = modes.add_parser('intake-set')
    intake.add_argument('--request',required=True)
    intake.add_argument('--request-sha256',required=True)
    mode = modes.add_parser('records')
    mode.add_argument('--run-root',required=True)
    args = parser.parse_args(argv)
    if args.command == 'package' and bool(args.tokenizer) != bool(args.encoding):
        parser.error('--tokenizer and --encoding must be selected together')
    empty_context = {'tokenizer':None,'files':[],'loads':[],'budget':None,'budget_result':'NOT_APPLICABLE','reason':'No selected budget; observation unavailable.'}
    observations = ({'unicode_candidates':[],'resources':[],'edges':[],'context':empty_context} if args.command == 'package' else {'input_kind':'set-validation-request-v1','ordered_member_ids':[],'member_bindings':[]} if args.command == 'intake-set' else {'checked_records':[],'errors':[]})
    checks, limitations, status = [], ['Development observations; semantic support and native behavior are not established.'], 'OBSERVED'
    try:
        if args.command == 'package':
            checks,observations,limitations = text_resources.package(args.source,args.tokenizer,args.encoding)
            if any(row['result'] == 'FAIL' for row in checks):
                status = 'MISMATCH'
            elif any(row['result'] in ('NOT_RUN','ERROR') for row in checks):
                status = 'INCOMPLETE'
        elif args.command == 'intake-set':
            reader = contracts.Reader()
            path = observe.safe_path(args.request)
            raw = reader.read(path)
            contracts.require(observe.sha256(raw) == args.request_sha256, 'selected input digest mismatch')
            value = observe.strict_json(raw)
            contracts.require(type(value) is dict and value.get('schema_version') in ('set-validation-request-v1','standalone-set-input-v1'), 'unsupported set input')
            observations['input_kind'] = value['schema_version']
            reader.record(value,str(path))
            sequence = reader.intake(value)
            reader.readback()
            observations.update(ordered_member_ids=sequence, member_bindings=[{'member_id':row['member_id'],'package_digest':row['package']['package_digest'],'valid':True,'reason':'Complete selected package/input readback verified.'} for row in value['members']])
            checks.append(text_resources.check('AV-A08','selected-set','PASS','Immutable membership, handoffs, topology and bytes verified; quality unassessed.'))
        else:
            checked,errors = records(args.run_root)
            observations = {'checked_records':checked,'errors':errors}
            status = 'MISMATCH' if errors else 'OBSERVED'
            checks.append(text_resources.check('AV-E01','records','FAIL' if errors else 'PASS','Integrity mismatches retained.' if errors else 'Supported record shapes, references, coverage and reductions verified.'))
    except (observe.ObservationError,OSError,ImportError) as error:
        status = 'INCOMPLETE'
        limitations.append('Unavailable bounded observation: '+type(error).__name__+'; '+str(error))
    except (ValueError,KeyError,TypeError,UnicodeError,RecursionError) as error:
        status = 'MISMATCH'
        limitations.append('Input mismatch: '+str(error))
    result = {'schema_version':'adaptive-check-observation-v1','command':args.command,'status':status,'checks':checks,'observations':observations,'limitations':limitations}
    print(json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2))
    return {'OBSERVED':0,'MISMATCH':1,'INCOMPLETE':2}[status]


if __name__ == '__main__':
    sys.exit(main())
