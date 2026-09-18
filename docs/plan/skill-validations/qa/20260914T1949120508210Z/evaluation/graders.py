"""Independent evidence checks. These never exercise or implement the QA skill."""

def metric(numerator, denominator, complete=True, floor=95, collector_ok=True):
    if type(numerator) is not int or type(denominator) is not int:
        return 'ERROR'
    if numerator < 0 or denominator < 0 or numerator > denominator:
        return 'ERROR'
    if not complete or not collector_ok or denominator == 0:
        return 'NOT_RUN'
    return 'PASS' if numerator * 100 >= max(95, floor) * denominator else 'FAIL'

def ordered_trace(events, require_launch=False):
    plan_seen = False
    stopped = False
    launches = 0
    for event in events:
        if event == 'plan_readback':
            plan_seen = True
        elif event == 'terminal_stop':
            stopped = True
        elif event == 'test_launch':
            launches += 1
            if stopped or not plan_seen:
                return 'FAIL'
    if 'finished' not in events or (require_launch and not launches):
        return 'NOT_RUN'
    return 'PASS'

def reduce_cases(rows):
    ids = [row[0] for row in rows]
    states = [row[1] for row in rows]
    if len(ids) != len(set(ids)) or any(state not in ('PASS','FAIL','ERROR','NOT_RUN','NOT_APPLICABLE') for state in states):
        return 'ERROR'
    if 'FAIL' in states:
        return 'FAIL'
    if not states or any(state in ('ERROR','NOT_RUN') for state in states):
        return 'INCOMPLETE'
    return 'PASS'

def report_contract(value):
    if set(value) != {'intent','execution','verdict','owner','fix','remaining'}:
        return 'ERROR'
    if value['intent']=='plan':
        return 'PASS' if value['verdict']=='NOT_EVALUATED' and value['execution']=='NOT_STARTED' and not value['fix'] else 'FAIL'
    if value['verdict']=='FAIL':
        return 'PASS' if value['fix'] and value['owner']=='dev' else 'FAIL'
    if value['verdict']=='INCOMPLETE':
        return 'PASS' if not value['fix'] and value['remaining'] else 'FAIL'
    return 'PASS' if value['verdict']=='PASS' and value['execution']=='COMPLETED' and not value['remaining'] and not value['fix'] else 'FAIL'
