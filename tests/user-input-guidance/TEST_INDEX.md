# Complete Test Index - STORY-059 Test Suite
## Quick Reference
Total Tests: 118


## Edge_Cases (test_edge_cases.py)

### TestEdgeCase1FixtureQualityVariation
- `test_should_stratify_fixtures_by_complexity`
- `test_should_document_complexity_classification`
- `test_should_analyze_results_by_complexity_level`

### TestEdgeCase2TokenCountingMethodology
- `test_should_document_token_counting_source`
- `test_should_document_token_counting_variance`
- `test_should_use_conversation_metadata_as_source_of_truth`

### TestEdgeCase3NonDeterministicGeneration
- `test_should_run_each_fixture_multiple_times`
- `test_should_use_median_for_final_values`
- `test_should_report_standard_deviation`
- `test_should_flag_high_variance_fixtures`

### TestDVR1FixturePairCompleteness
- `test_should_validate_10_baseline_enhanced_pairs_exist`
- `test_should_halt_with_clear_error_message_on_missing_pair`

### TestDVR2ResultsJsonSchema
- `test_should_have_required_fields_in_baseline_results`
- `test_should_have_required_fields_in_enhanced_results`
- `test_should_detect_and_report_invalid_schema`

### TestDVR3StatisticalSignificance
- `test_should_calculate_p_value`
- `test_should_flag_non_significant_results`
- `test_should_use_paired_t_test_for_token_savings`

## Fixtures (test_fixtures.py)

### TestFixtureContentValidation
- `test_should_validate_baseline_fixtures_not_empty`
- `test_should_validate_enhanced_fixtures_not_empty`
- `test_should_validate_baseline_fixtures_have_no_placeholder_content`
- `test_should_validate_enhanced_fixtures_have_no_placeholder_content`

### TestFixturePairDistinctness
- `test_should_have_distinct_baseline_and_enhanced_content`
- `test_should_have_meaningful_enhanced_content_difference`

### TestFixtureComplexityClassification
- `test_should_classify_simple_fixtures_correctly`
- `test_should_classify_medium_fixtures_correctly`
- `test_should_classify_complex_fixtures_correctly`

### TestFixtureMetadataValidation
- `test_should_have_valid_fixture_metadata_json`
- `test_should_have_metadata_for_all_fixtures`
- `test_should_have_description_for_all_fixtures`

## Impact_Report (test_impact_report.py)

### TestImpactReportExistence
- `test_should_generate_impact_report`
- `test_should_have_impact_report_with_content`

### TestImpactReportExecutiveSummary
- `test_should_have_executive_summary_section`
- `test_should_have_headline_metrics_in_summary`
- `test_should_limit_executive_summary_to_500_words`

### TestImpactReportFindingsByBusinessGoal
- `test_should_have_findings_by_business_goal`
- `test_should_document_incomplete_rate_findings`
- `test_should_document_token_efficiency_findings`
- `test_should_document_iteration_cycle_findings`

### TestImpactReportEvidenceTables
- `test_should_have_evidence_tables`
- `test_should_include_all_10_fixtures_in_tables`

### TestImpactReportStatisticalAnalysis
- `test_should_have_statistical_analysis_section`
- `test_should_report_confidence_intervals`
- `test_should_report_significance_testing`

### TestImpactReportRecommendations
- `test_should_have_recommendations_section`
- `test_should_have_3_to_5_actionable_recommendations`

### TestImpactReportLimitations
- `test_should_have_limitations_section`
- `test_should_acknowledge_sample_size_limitation`
- `test_should_acknowledge_fixture_selection_bias`

### TestImpactReportAppendix
- `test_should_have_appendix_with_raw_data`

### TestNFR_Performance
- `test_should_complete_test_suite_in_under_60_minutes`

### TestNFR_Reliability
- `test_should_handle_individual_fixture_failures`
- `test_should_provide_clear_error_messages`

### TestNFR_Maintainability
- `test_should_use_stdlib_only_for_core_functionality`
- `test_should_have_simple_text_fixtures`
- `test_should_output_machine_readable_json`

## Infrastructure (test_infrastructure.py)

### TestDirectoryStructure
- `test_should_have_tests_user_input_guidance_directory`
- `test_should_have_fixtures_directory_structure`
- `test_should_have_scripts_directory`

### TestBaselineFixtures
- `test_should_have_10_baseline_fixtures`
- `test_should_have_baseline_numbered_sequentially`
- `test_should_validate_baseline_fixture_content_length`
- `test_should_validate_baseline_fixture_encoding`

### TestEnhancedFixtures
- `test_should_have_10_enhanced_fixtures`
- `test_should_have_enhanced_numbered_sequentially`
- `test_should_validate_enhanced_fixture_content_length`
- `test_should_validate_enhanced_fixture_encoding`

### TestFixturePairMatching
- `test_should_have_matching_baseline_enhanced_pairs`
- `test_should_validate_fixture_pair_count_matches`

### TestFixtureMetadata
- `test_should_have_fixture_metadata_file`
- `test_should_validate_fixture_metadata_structure`
- `test_should_validate_fixture_complexity_stratification`

### TestMeasurementScripts
- `test_should_have_validate_token_savings_script`
- `test_should_have_measure_success_rate_script`
- `test_should_have_test_story_creation_without_guidance_script`
- `test_should_have_test_story_creation_with_guidance_script`

## Measurements (test_measurements.py)

### TestTokenSavingsScriptStructure
- `test_should_have_token_savings_script`
- `test_should_have_token_savings_script_with_content`
- `test_should_have_token_savings_script_with_help_documentation`
- `test_should_have_token_savings_script_with_statistical_functions`

### TestSuccessRateScriptStructure
- `test_should_have_success_rate_script`
- `test_should_have_success_rate_script_with_content`
- `test_should_have_success_rate_script_with_help_documentation`
- `test_should_have_success_rate_script_with_scoring_function`

### TestTokenSavingsReportGeneration
- `test_should_generate_token_savings_report_markdown`
- `test_should_have_token_savings_report_with_content`
- `test_should_include_savings_percentage_in_report`
- `test_should_include_statistical_significance_in_report`
- `test_should_include_confidence_level_in_report`
- `test_should_generate_token_savings_chart`

### TestSuccessRateReportGeneration
- `test_should_generate_success_rate_report_markdown`
- `test_should_have_success_rate_report_with_content`
- `test_should_include_baseline_incomplete_rate_in_report`
- `test_should_include_enhanced_incomplete_rate_in_report`
- `test_should_include_reduction_percentage_in_report`
- `test_should_include_iteration_metrics_in_report`
- `test_should_include_fixture_breakdown_in_report`

### TestMeasurementScriptDependencies
- `test_should_use_only_stdlib_in_token_savings_script`
- `test_should_use_only_stdlib_in_success_rate_script`

## Scripts (test_scripts.py)

### TestStoryCreationScriptStructure
- `test_should_have_test_story_creation_without_guidance_script_with_content`
- `test_should_have_test_story_creation_with_guidance_script_with_content`
- `test_should_have_baseline_script_with_shebang`
- `test_should_have_enhanced_script_with_shebang`
- `test_should_have_baseline_script_with_help_flag`
- `test_should_have_enhanced_script_with_help_flag`
- `test_should_have_baseline_script_with_dry_run_flag`
- `test_should_have_enhanced_script_with_dry_run_flag`

### TestScriptOutputRequirements
- `test_should_generate_baseline_results_json_structure`
- `test_should_generate_enhanced_results_json_structure`
- `test_should_have_10_baseline_story_results`
- `test_should_have_10_enhanced_story_results`

### TestScriptOutputMetrics
- `test_should_capture_token_usage_per_story_baseline`
- `test_should_capture_token_usage_per_story_enhanced`
- `test_should_capture_iteration_count_baseline`
- `test_should_capture_iteration_count_enhanced`
- `test_should_capture_ac_count_per_story`
- `test_should_capture_nfr_presence_flag`
- `test_should_capture_multiple_runs_per_fixture`
