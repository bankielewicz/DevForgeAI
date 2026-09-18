"""Execute original shipped runtime against independent retained binding fixtures."""
import unittest
import test_builder_adaptive as t
import copy

class RuntimeOriginal(unittest.TestCase):
    setUp=t.AdaptiveTests.setUp
    operational=t.AdaptiveTests.operational
    def run_cli(self,script,arguments):
        # These additional cases intentionally execute the original runtime asset;
        # the retained suite separately executes copied installation fixtures.
        return t.AdaptiveTests.run_cli(self,t.RUNTIME,arguments)
    check_binding=t.AdaptiveTests.check_binding
    test_runtime_binding_matrix=t.AdaptiveTests.test_BAT07_runtime_binding_matrix
    test_runtime_ambiguous_core_variants=t.AdaptiveTests.test_BAT07_ambiguous_core_variants
    test_runtime_portability_identity_unbound=t.AdaptiveTests.test_BAT06_portability_identity_and_unbound
    test_runtime_malformed_descriptor_extra_files=t.AdaptiveTests.test_BAT07_malformed_descriptor_and_extra_package_files

    def test_runtime_rejects_non_json_duplicate_and_nonfinite_inputs(self):
        runtime=t.a.runtime
        for raw in (b'{"x":1,"x":2}', b'NaN', b'Infinity', b'1e999', b'\xff', b'{'):
            with self.subTest(raw=repr(raw)),self.assertRaises(runtime.BindingError):
                runtime.strict_json(raw)

    def test_runtime_rejects_impossible_timestamp_and_invalid_uuid(self):
        project,skill,binding=self.operational()
        for key,value in [('updated_at_utc','2026-02-30T00:00:00Z'),('project_id','invalid-project-identity')]:
            wrong=copy.deepcopy(binding);wrong[key]=value
            self.check_binding(project,skill,wrong,'INVALID_BINDING',1)
