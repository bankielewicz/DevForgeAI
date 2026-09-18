"""JSONL maintenance runner; unittest assertions are deterministic graders."""
import argparse
import datetime
import json
import os
import sys
import unittest
from evidence import RUN, identity, dump


def leaves(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from leaves(item)
        else:
            yield item


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    args = parser.parse_args()
    if not args.attempt.replace('-', '').isalnum():
        parser.error('attempt must be an alphanumeric/hyphen label')
    os.environ['REMEDIATION_ATTEMPT'] = args.attempt
    import test_remediation
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_remediation)
    ids = [test.id() for test in leaves(suite)]
    receipt = identity()
    folder = RUN / 'evaluations' / args.attempt
    folder.mkdir(parents=True, exist_ok=False)
    dump(folder/'expected-results.json', [{'case_id':case,'expected':'PASS','oracle':'Observable assertions in retained test_remediation.py; valid controls plus invalid-input rejection and preservation.'} for case in ids])
    dump(folder/'input-receipt.json', receipt)
    outcomes = {}

    class Result(unittest.TextTestResult):
        def addSuccess(self, test):
            super().addSuccess(test)
            outcomes[test.id()] = ('PASS', None)

        def addFailure(self, test, err):
            super().addFailure(test, err)
            outcomes[test.id()] = ('FAIL', self._exc_info_to_string(err, test))

        def addError(self, test, err):
            super().addError(test, err)
            outcomes[test.id()] = ('ERROR', self._exc_info_to_string(err, test))

        def addSkip(self, test, reason):
            super().addSkip(test, reason)
            outcomes[test.id()] = ('NOT_RUN', reason)

    result = unittest.TextTestRunner(verbosity=2, resultclass=Result).run(suite)
    rows = [{'schema_version':'maintenance-case-v1','case_id':case,'status':outcomes.get(case, ('NOT_RUN', None))[0],'detail':outcomes.get(case, ('NOT_RUN', None))[1],'package_digest':receipt['package_digest'],'method':'Python implementation regression','attempt':args.attempt} for case in ids]
    with (folder/'results.jsonl').open('x', encoding='utf-8', newline='\n') as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False)+'\n')
    passed = sum(row['status']=='PASS' for row in rows)
    dump(folder/'summary.json', {'required':len(rows),'passing':passed,'pass_percent':100*passed/len(rows),'source_unchanged':receipt==identity(),'finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authority':'Development observation; not complete BAT/native/framework acceptance'})
    print(json.dumps({'required':len(rows),'passing':passed,'package_digest':receipt['package_digest']}))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
