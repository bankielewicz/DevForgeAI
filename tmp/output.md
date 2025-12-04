bryan@DESKTOP-88FARC5:/mnt/c/Projects/DevForgeAI2$ python3 -m pytest installer/tests/ --co -q 2>&1
================================================= test session starts ==================================================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.6.0
rootdir: /mnt/c/Projects/DevForgeAI2
configfile: pytest.ini
plugins: mock-3.15.0, cov-4.1.0, asyncio-0.21.2, anyio-4.10.0
asyncio: mode=Mode.STRICT
collected 562 items

<Module installer/tests/test_backup_management.py>
  <Class TestBackupCreation>
    <Function test_backup_directory_created_with_timestamp>
    <Function test_backup_copies_claude_directory>
    <Function test_backup_copies_devforgeai_directory>
    <Function test_backup_copies_claude_md_file>
    <Function test_backup_manifest_generated>
    <Function test_backup_integrity_hash_calculated>
    <Function test_backup_integrity_verification_success>
    <Function test_backup_integrity_verification_fails_missing_files>
    <Function test_backup_before_deployment_prevents_partial_install>
    <Function test_backup_manifest_contains_reason_field>
<Module installer/tests/test_backup_service.py>
  <Class TestBackupCreation>
    <Function test_create_timestamped_backup_directory>
    <Function test_backup_directory_created_before_first_file_copy>
    <Function test_backup_fails_if_directory_creation_fails>
  <Class TestDirectoryStructurePreservation>
    <Function test_preserve_directory_structure_in_backup>
    <Function test_backup_preserves_relative_paths>
  <Class TestBackupPerformance>
    <Function test_backup_completes_within_10_seconds_for_500_files>
    <Function test_backup_logs_duration_metric>
  <Class TestBackupLogging>
    <Function test_backup_logs_backup_location_to_install_logger>
    <Function test_backup_logs_file_count_statistics>
  <Class TestBackupProceedsCondition>
    <Function test_file_operations_blocked_if_backup_fails>
    <Function test_backup_success_returns_backup_directory_path>
  <Class TestBackupCleanup>
    <Function test_cleanup_backups_older_than_7_days>
    <Function test_cleanup_keeps_minimum_5_backups>
  <Class TestBackupEdgeCases>
    <Function test_backup_handles_symlinks_correctly>
    <Function test_backup_skips_nonexistent_files_with_warning>
    <Function test_backup_handles_empty_files_list>
    <Function test_backup_handles_disk_full_error>
  <Class TestBackupIntegration>
    <Function test_backup_service_used_by_error_handler>
<Module installer/tests/test_bundle.py>
  <Class TestVerifyBundleStructure>
    <Function test_complete_bundle_structure>
    <Function test_missing_claude_agents_directory>
    <Function test_missing_checksums_json>
    <Function test_missing_version_json>
    <Function test_multiple_missing_components>
  <Class TestCountBundledFiles>
    <Function test_count_files_single_directory>
    <Function test_count_files_nested_directories>
    <Function test_count_files_excludes_directories>
    <Function test_count_files_empty_bundle>
    <Function test_count_files_nonexistent_directory>
  <Class TestMeasureBundleSize>
    <Function test_measure_empty_bundle>
    <Function test_measure_small_bundle>
    <Function test_measure_nonexistent_bundle>
    <Function test_compression_fallback>
  <Class TestValidateBundlePath>
    <Function test_valid_bundle_name>
    <Function test_valid_bundle_with_hyphen>
    <Function test_valid_bundle_with_underscore>
    <Function test_valid_bundle_with_dot>
    <Function test_reject_path_traversal>
    <Function test_reject_absolute_path>
    <Function test_reject_special_characters>
    <Function test_reject_command_substitution>
    <Function test_reject_backticks>
    <Function test_nonexistent_path>
    <Function test_path_outside_base_directory>
    <Function test_default_base_path>
    <Function test_safe_path_pattern_alphanumeric>
    <Function test_safe_path_pattern_special_allowed>
    <Function test_safe_path_pattern_invalid>
<Module installer/tests/test_checksum.py>
  <Class TestCalculateSHA256>
    <Function test_calculate_empty_file>
    <Function test_calculate_small_file>
    <Function test_calculate_large_file>
    <Function test_file_not_found>
    <Function test_binary_file>
  <Class TestLoadChecksums>
    <Function test_load_valid_checksums>
    <Function test_checksums_file_missing>
    <Function test_invalid_json>
    <Function test_not_a_dict>
    <Function test_invalid_hash_length>
    <Function test_schema_validation_failure>
  <Class TestVerifyFileChecksum>
    <Function test_matching_checksum>
    <Function test_mismatching_checksum>
    <Function test_file_not_found>
  <Class TestVerifyBundleIntegrity>
    <Function test_all_checksums_valid>
    <Function test_single_checksum_failure>
    <Function test_multiple_checksum_failures_under_threshold>
    <Function test_tamper_detection_threshold>
    <Function test_missing_checksums_file>
  <Class TestVerifyAllFilesHaveChecksums>
    <Function test_all_files_have_checksums>
    <Function test_missing_checksum_entries>
    <Function test_nested_directories>
    <Function test_checksums_json_excluded>
<Module installer/tests/test_deployment_engine.py>
  <Class TestDeploymentEngine>
    <Function test_deploy_claude_files_to_target>
    <Function test_deploy_devforgeai_files_to_target>
    <Function test_exclude_backup_artifacts>
    <Function test_exclude_pycache_and_pyc>
    <Function test_exclude_generated_content>
    <Function test_set_script_permissions_755>
    <Function test_set_markdown_permissions_644>
    <Function test_set_python_permissions_644>
    <Function test_preserve_user_config_hooks_yaml>
    <Function test_preserve_user_config_feedback_yaml>
    <Function test_preserve_user_context_files>
    <Function test_do_not_touch_ai_docs_directory>
    <Function test_deployment_file_count_matches_expected>
    <Function test_deployment_report_generated>
    <Function test_directory_permissions_755>
<Module installer/tests/test_edge_cases.py>
  <Class TestDiskSpaceEdgeCase>
    <Function test_detect_insufficient_disk_space>
    <Function test_backup_fails_disk_full_during_operation>
  <Class TestCorruptedInstallationEdgeCase>
    <Function test_detect_corrupted_installation_missing_version_json>
    <Function test_repair_corrupted_installation>
  <Class TestNetworkInterruptionEdgeCase>
    <Function test_cli_installation_network_timeout>
    <Function test_cli_installation_recovery_manual>
  <Class TestConcurrentExecutionEdgeCase>
    <Function test_detect_concurrent_execution_with_lock_file>
    <Function test_lock_file_removed_on_completion>
  <Class TestSchemaChangeEdgeCase>
    <Function test_schema_v1_to_v2_migration>
    <Function test_schema_migration_preserves_existing_fields>
  <Class TestSymlinkPreservationEdgeCase>
    <Function test_detect_symlink_in_target>
    <Function test_follow_symlink_during_deployment>
  <Class TestBackupAccumulationEdgeCase>
    <Function test_warn_on_excessive_backups>
    <Function test_suggestion_to_clean_old_backups>
  <Class TestErrorHandlingAndRollback>
    <Function test_permission_denied_error_triggers_rollback>
    <Function test_deployment_failure_leaves_valid_state>
    <Function test_verify_checksum_after_rollback>
<Module installer/tests/test_error_handler.py>
  <Class TestErrorCategorization>
    <Function test_missing_source_error_returns_exit_code_1>
    <Function test_permission_denied_error_returns_exit_code_2>
    <Function test_rollback_occurred_returns_exit_code_3>
    <Function test_validation_failed_returns_exit_code_4>
    <Function test_success_returns_exit_code_0>
  <Class TestUserFriendlyMessages>
    <Function test_console_message_contains_no_stack_trace>
    <Function test_console_message_contains_plain_english_description>
    <Function test_console_message_includes_log_file_reference>
    <Function test_console_message_includes_1_to_3_resolution_steps>
  <Class TestResolutionGuidance>
    <Function test_missing_source_has_specific_resolution_steps>
    <Function test_permission_denied_has_specific_resolution_steps>
    <Function test_validation_failed_has_specific_resolution_steps>
    <Function test_resolution_steps_limited_to_3_maximum>
    <Function test_resolution_steps_under_200_chars_each>
  <Class TestErrorHandlerDependencies>
    <Function test_error_handler_triggers_rollback_service_on_error>
    <Function test_error_handler_logs_to_install_logger>
    <Function test_error_handler_uses_backup_service_for_context>
  <Class TestExitCodeHandling>
    <Function test_get_exit_code_returns_correct_code_for_each_category>
    <Function test_rollback_error_overrides_original_exit_code>
  <Class TestPathSanitization>
    <Function test_console_message_sanitizes_usernames_in_paths>
    <Function test_console_message_does_not_leak_sensitive_paths>
  <Class TestEdgeCases>
    <Function test_concurrent_installation_error_detected>
    <Function test_error_during_rollback_logged_but_does_not_crash>
    <Function test_sigint_handled_gracefully_triggers_rollback>
<Module installer/tests/test_error_handling_edge_cases.py>
  <Class TestRollbackFailureScenarios>
    <Function test_rollback_fails_when_backup_missing>
    <Function test_partial_rollback_when_some_files_fail>
  <Class TestConcurrentInstallationEdgeCases>
    <Function test_stale_lock_file_removed_automatically>
    <Function test_lock_file_race_condition_handling>
  <Class TestLogFileEdgeCases>
    <Function test_log_file_exists_from_previous_install_appends_with_separator>
    <Function test_log_file_rotation_at_10mb>
  <Class TestSensitiveInfoSanitization>
    <Function test_console_output_replaces_username_in_paths>
    <Function test_console_output_does_not_leak_credentials>
  <Class TestValidationFailureEdgeCase>
    <Function test_validation_fails_post_installation_no_auto_rollback>
  <Class TestBackupCreationFailureEdgeCases>
    <Function test_backup_fails_installation_halts_immediately>
    <Function test_disk_full_during_backup_halts_installation>
  <Class TestUserInterruptHandling>
    <Function test_sigint_during_backup_triggers_cleanup>
    <Function test_sigint_during_file_copy_triggers_rollback>
  <Class TestEmptyDirectoryCleanup>
    <Function test_remove_empty_directories_after_rollback>
  <Class TestMultipleErrorsSequence>
    <Function test_error_during_rollback_handled_gracefully>
  <Class TestUnicodeAndSpecialCharacters>
    <Function test_error_handler_handles_unicode_paths>
    <Function test_log_file_handles_unicode_in_error_messages>
  <Class TestVeryLongPaths>
    <Function test_error_handler_truncates_very_long_paths_in_console>
    <Function test_log_file_preserves_full_path_even_if_very_long>
<Module installer/tests/test_exit_codes.py>
  <Class TestExitCodeConstants>
    <Function test_success_constant_equals_0>
    <Function test_missing_source_constant_equals_1>
    <Function test_permission_denied_constant_equals_2>
    <Function test_rollback_occurred_constant_equals_3>
    <Function test_validation_failed_constant_equals_4>
  <Class TestExitCodeUniqueness>
    <Function test_all_exit_codes_are_unique>
  <Class TestExitCodeTypes>
    <Function test_all_exit_codes_are_integers>
  <Class TestExitCodeRange>
    <Function test_all_exit_codes_within_range_0_to_4>
  <Class TestExitCodeConstantCount>
    <Function test_exactly_5_exit_codes_defined>
  <Class TestExitCodeDocumentation>
    <Function test_exit_codes_module_has_docstring>
  <Class TestExitCodeUsage>
    <Function test_exit_code_can_be_used_in_sys_exit>
    <Function test_exit_code_can_be_compared_for_equality>
  <Class TestExitCodeNaming>
    <Function test_exit_code_names_are_uppercase>
  <Class TestExitCodeEnum>
    <Function test_exit_codes_can_be_implemented_as_class_or_enum>
<Module installer/tests/test_install_logger.py>
  <Class TestTimestampFormat>
    <Function test_log_entries_have_iso_8601_timestamps>
    <Function test_timestamp_includes_milliseconds>
    <Function test_timestamp_uses_utc_timezone>
  <Class TestStackTraces>
    <Function test_log_includes_stack_trace_on_error>
    <Function test_log_includes_file_paths_and_line_numbers>
  <Class TestAppendMode>
    <Function test_append_to_existing_log_file>
    <Function test_second_install_preserves_first_install_logs>
    <Function test_log_separates_installation_sessions>
  <Class TestLogContent>
    <Function test_log_includes_error_category_and_exit_code>
    <Function test_log_includes_file_paths_involved>
    <Function test_log_includes_system_context>
    <Function test_log_includes_rollback_actions_taken>
  <Class TestLogRotation>
    <Function test_log_rotates_when_exceeding_10mb>
    <Function test_log_keeps_3_rotations>
  <Class TestLogLevels>
    <Function test_log_info_level>
    <Function test_log_warning_level>
    <Function test_log_error_level>
  <Class TestLogFilePermissions>
    <Function test_log_file_created_with_0600_permissions>
  <Class TestLogEdgeCases>
    <Function test_log_handles_unicode_characters>
    <Function test_log_handles_multiline_messages>
    <Function test_log_handles_very_long_messages>
    <Function test_log_handles_log_file_deletion_during_operation>
<Module installer/tests/test_installation_modes.py>
  <Class TestFreshInstallMode>
    <Function test_fresh_install_complete_workflow>
    <Function test_fresh_install_creates_config_from_examples>
  <Class TestUpgradeMode>
    <Function test_upgrade_workflow_1_0_0_to_1_0_1>
    <Function test_upgrade_selective_update_for_patch>
    <Function test_upgrade_major_version_warns_breaking_changes>
  <Class TestRollbackMode>
    <Function test_rollback_complete_workflow>
  <Class TestValidateMode>
    <Function test_validate_complete_workflow>
  <Class TestUninstallMode>
    <Function test_uninstall_complete_workflow>
<Module installer/tests/test_integration_error_handling.py>
  <Class TestFullRollbackFlow>
    <Function test_error_after_file_copy_triggers_complete_rollback>
    <Function test_rollback_displays_console_messages>
    <Function test_rollback_logs_all_actions_to_install_log>
  <Class TestConcurrentInstallationPrevention>
    <Function test_lock_file_prevents_second_installation>
    <Function test_second_installation_provides_clear_error_message>
  <Class TestSigintHandling>
    <Function test_sigint_triggers_rollback>
    <Function test_sigint_displays_cancellation_message>
  <Class TestErrorDetectionLatency>
    <Function test_error_detection_latency_under_50ms>
  <Class TestBackupBeforeModification>
    <Function test_file_copy_blocked_if_backup_fails>
    <Function test_installation_proceeds_only_after_successful_backup>
  <Class TestErrorHandlerReliability>
    <Function test_all_file_operations_have_error_handlers>
  <Class TestEndToEndErrorScenarios>
    <Function test_e2e_missing_source_files>
    <Function test_e2e_permission_denied>
    <Function test_e2e_validation_failed_post_installation>
<Module installer/tests/test_lock_file_manager.py>
  <Class TestLockFileCreation>
    <Function test_create_lock_file_at_installation_start>
    <Function test_lock_file_contains_current_process_pid>
    <Function test_lock_file_contains_timestamp>
  <Class TestConcurrentInstallationDetection>
    <Function test_detect_concurrent_installation_via_pid_check>
    <Function test_lock_acquisition_succeeds_when_no_existing_lock>
    <Function test_second_install_fails_with_validation_failed_exit_code>
  <Class TestLockFileCleanup>
    <Function test_remove_lock_file_on_successful_exit>
    <Function test_remove_lock_file_on_error_exit>
    <Function test_remove_lock_file_on_keyboard_interrupt>
  <Class TestStaleLockDetection>
    <Function test_detect_stale_lock_with_dead_pid>
    <Function test_remove_stale_lock_file>
    <Function test_active_lock_is_not_considered_stale>
  <Class TestLockFileEdgeCases>
    <Function test_lock_acquisition_retries_on_race_condition>
    <Function test_lock_file_permissions_0600>
    <Function test_lock_file_survives_process_crash_simulation>
    <Function test_lock_handles_devforgeai_directory_missing>
  <Class TestLockFileTimeout>
    <Function test_lock_acquisition_fails_after_timeout>
    <Function test_lock_acquisition_succeeds_if_lock_released_before_timeout>
  <Class TestLockFileContextManager>
    <Function test_lock_manager_works_as_context_manager>
    <Function test_lock_released_even_if_exception_in_context>
<Module installer/tests/test_main.py>
  <Class TestMainHelpText>
    <Function test_help_flag_short>
    <Function test_help_flag_long>
    <Function test_no_arguments>
  <Class TestMainCommandParsing>
    <Function test_unknown_command>
    <Function test_missing_target_path>
  <Class TestMainInstallCommand>
    <Function test_install_success>
    <Function test_install_with_force_flag>
    <Function test_install_failure>
    <Function test_install_rollback>
  <Class TestMainValidateCommand>
    <Function test_validate_success>
  <Class TestMainRollbackCommand>
    <Function test_rollback_success>
  <Class TestMainUninstallCommand>
    <Function test_uninstall_success>
  <Class TestMainErrorHandling>
    <Function test_exception_handling>
    <Function test_displays_warnings>
    <Function test_displays_errors>
    <Function test_path_resolution>
<Module installer/tests/test_network.py>
  <Class TestSocketNetworkDetector>
    <Function test_init_default_values>
    <Function test_init_custom_values>
    <Function test_check_network_availability_online>
    <Function test_check_network_availability_timeout>
    <Function test_check_network_availability_socket_error>
    <Function test_check_network_availability_os_error>
    <Function test_check_network_availability_custom_timeout>
  <Class TestCheckNetworkAvailability>
    <Function test_delegates_to_socket_detector>
    <Function test_online_returns_true>
    <Function test_offline_returns_false>
  <Class TestDisplayNetworkStatus>
    <Function test_display_online_status>
    <Function test_display_offline_status>
  <Class TestWarnNetworkFeatureUnavailable>
    <Function test_minimal_warning>
    <Function test_warning_with_impact>
    <Function test_warning_with_enable_command>
    <Function test_warning_all_fields>
  <Class TestDetectPythonVersion>
    <Function test_python_38_detected>
    <Function test_python_310_detected>
    <Function test_python_27_rejected>
    <Function test_python_37_rejected>
    <Function test_attribute_error_handled>
  <Class TestWarnMissingDependency>
    <Function test_warn_python_dependency>
    <Function test_warn_unknown_dependency>
  <Class TestCheckDiskSpace>
    <Function test_sufficient_disk_space>
    <Function test_insufficient_disk_space>
    <Function test_negative_required_mb>
    <Function test_zero_required_mb>
  <Class TestCheckGitAvailable>
    <Function test_git_available>
    <Function test_git_unavailable>
<Module installer/tests/test_offline_installer.py>
  <Class TestNetworkDetection>
    <Function test_network_detection_online_success>
    <Function test_network_detection_offline_timeout>
    <Function test_network_detection_timeout_within_2_seconds>
    <Function test_network_detection_displays_status_message>
  <Class TestNoExternalDownloads>
    <Function test_offline_install_makes_zero_http_requests>
    <Function test_offline_install_no_cdn_dependencies>
    <Function test_offline_install_no_github_api_calls>
    <Function test_offline_install_no_npm_registry_lookups>
  <Class TestBundleStructure>
    <Function test_bundled_claude_directory_exists>
    <Function test_bundled_devforgeai_directory_exists>
    <Function test_bundle_contains_all_required_files>
    <Function test_bundle_size_within_limits>
  <Class TestPythonCliBundled>
    <Function test_python_wheel_files_bundled>
    <Function test_python_cli_installs_from_local_wheels>
    <Function test_python_cli_installation_detects_python_version>
  <Class TestGracefulDegradation>
    <Function test_install_continues_without_python>
    <Function test_install_creates_missing_features_note>
    <Function test_graceful_degradation_clear_warning_message>
  <Class TestOfflineModeValidation>
    <Function test_offline_validation_checks_200_files>
    <Function test_offline_validation_git_initialization_no_remote>
    <Function test_offline_validation_claude_md_merge>
  <Class TestNetworkDependentFeatureErrors>
    <Function test_network_feature_error_displays_feature_name>
    <Function test_network_feature_error_explains_why_network_required>
    <Function test_network_feature_error_shows_impact_of_skipping>
    <Function test_network_feature_error_provides_enable_command>
    <Function test_network_feature_error_does_not_halt_installation>
  <Class TestBundleIntegrityVerification>
    <Function test_checksums_json_exists_in_bundle>
    <Function test_all_bundled_files_have_checksum_entries>
    <Function test_checksum_verification_calculates_sha256>
    <Function test_checksum_mismatch_detected>
    <Function test_checksum_verification_reports_mismatches>
  <Class TestPerformanceRequirements>
    <Function test_offline_installation_time_under_60_seconds_hdd>
    <Function test_offline_installation_time_under_30_seconds_ssd>
  <Class TestSecurityRequirements>
    <Function test_sha256_checksum_validation_for_all_files>
    <Function test_halt_on_3_checksum_failures>
  <Class TestReliabilityRequirements>
    <Function test_core_install_succeeds_without_python>
  <Class TestEdgeCases>
    <Function test_partial_network_access_treated_as_offline>
    <Function test_disk_space_check_before_extraction>
    <Function test_git_not_installed_halts_with_clear_error>
<Module installer/tests/test_rollback_manager.py>
  <Class TestRollbackManager>
    <Function test_list_backups_sorted_by_timestamp>
    <Function test_verify_backup_integrity_success>
    <Function test_verify_backup_integrity_fails_corrupted>
    <Function test_verify_backup_missing_manifest>
    <Function test_restore_all_files_from_backup>
    <Function test_restore_preserves_file_content>
    <Function test_revert_version_json_to_backup_version>
    <Function test_rollback_cleans_deployed_files>
    <Function test_rollback_selects_most_recent_backup>
    <Function test_rollback_displays_selected_backup_info>
    <Function test_rollback_on_deployment_failure_automatic>
    <Function test_rollback_exit_code_0_success>
<Module installer/tests/test_rollback_service.py>
  <Class TestFileRestoration>
    <Function test_restore_all_files_from_backup_directory>
    <Function test_restore_preserves_directory_structure>
    <Function test_restore_overwrites_modified_files>
  <Class TestPartialInstallationCleanup>
    <Function test_remove_files_created_during_failed_install>
    <Function test_remove_empty_directories_after_cleanup>
    <Function test_cleanup_does_not_remove_files_in_backup>
  <Class TestRollbackPerformance>
    <Function test_rollback_completes_within_5_seconds_for_500_files>
    <Function test_rollback_logs_duration_metric>
  <Class TestRollbackLogging>
    <Function test_rollback_logs_all_actions_to_install_logger>
    <Function test_rollback_logs_file_count_statistics>
  <Class TestRollbackExitCode>
    <Function test_rollback_returns_exit_code_3>
  <Class TestRollbackEdgeCases>
    <Function test_rollback_fails_gracefully_when_backup_missing>
    <Function test_rollback_continues_on_permission_error_for_individual_file>
    <Function test_rollback_displays_console_message>
    <Function test_rollback_handles_symlinks_correctly>
  <Class TestRollbackReliability>
    <Function test_rollback_success_rate_99_5_percent>
<Module installer/tests/test_schemas.py>
  <Class TestValidateJsonSchema>
    <Function test_valid_object_type>
    <Function test_invalid_type>
    <Function test_required_fields_present>
    <Function test_required_fields_missing>
    <Function test_pattern_validation_success>
    <Function test_pattern_validation_failure>
    <Function test_integer_minimum_validation>
    <Function test_integer_maximum_validation>
    <Function test_pattern_properties_matching>
    <Function test_pattern_properties_value_mismatch>
    <Function test_additional_properties_forbidden>
    <Function test_min_properties_validation>
  <Class TestChecksumsSchemaValidation>
    <Function test_valid_checksums>
    <Function test_invalid_hash_length>
    <Function test_invalid_hash_characters>
    <Function test_empty_checksums>
    <Function test_invalid_file_path>
  <Class TestVersionSchemaValidation>
    <Function test_valid_version>
    <Function test_missing_required_field>
    <Function test_invalid_version_format>
    <Function test_invalid_timestamp_format>
    <Function test_optional_checksum_field>
    <Function test_additional_properties_forbidden>
  <Class TestBundleManifestSchemaValidation>
    <Function test_valid_bundle_manifest>
    <Function test_missing_checksums>
    <Function test_missing_metadata>
    <Function test_invalid_file_count>
<Module installer/tests/test_version_detection.py>
  <Class TestVersionDetection>
    <Function test_detect_fresh_install_no_version_file>
    <Function test_read_installed_version_from_existing_file>
    <Function test_read_source_version_from_version_json>
    <Function test_version_comparison_patch_upgrade>
    <Function test_version_comparison_minor_upgrade>
    <Function test_version_comparison_major_upgrade>
    <Function test_version_comparison_reinstall_same_version>
    <Function test_version_comparison_downgrade>
    <Function test_installation_mode_detection_fresh>
    <Function test_installation_mode_detection_patch_upgrade>
    <Function test_version_file_missing_returns_none>
    <Function test_invalid_version_format_raises_error>
    <Function test_version_comparison_complex_case_1_99_vs_2_0>
    <Function test_version_comparison_complex_case_1_1_vs_1_1_0>
<Package integration>
  <Module test_claude_md_merge_with_installer.py>
    <Class TestScenario1FreshInstall>
      <Function test_fresh_install_creates_claude_md>
      <Function test_fresh_install_variables_detected>
    <Class TestScenario2ExistingProject>
      <Function test_existing_claude_md_preserved_after_merge>
      <Function test_existing_merge_performance_under_5_seconds>
    <Class TestScenario3RejectMerge>
      <Function test_reject_merge_original_unchanged>
      <Function test_reject_merge_can_retry>
    <Class TestScenario4ApproveMerge>
      <Function test_approve_merge_applies_changes>
      <Function test_approve_merge_backup_kept>
      <Function test_approve_merge_allows_rollback>
    <Class TestScenario5LargeProject>
      <Function test_large_project_merge_completes>
      <Function test_large_project_all_sections_preserved>
    <Class TestScenario6ConflictingSections>
      <Function test_conflicting_sections_detected>
      <Function test_conflicting_merge_report_generated>
    <Class TestScenario7UpgradeFromOldVersion>
      <Function test_upgrade_preserves_user_rules>
      <Function test_upgrade_can_remove_old_framework_sections>
    <Class TestFullInstallerWorkflowWithMerge>
      <Function test_upgrade_workflow_with_merge_complete>
    <Class TestDataIntegrity>
      <Function test_backup_integrity_verification>
      <Function test_merge_diff_accuracy>
      <Function test_no_data_loss_across_scenarios>
    <Class TestPerformance>
      <Function test_variable_detection_performance>
      <Function test_merge_complete_phase_timing>
  <Module test_coverage_gaps_application_layer.py>
    <Class TestOfflineInstallerErrorPaths>
      <Function test_find_bundled_wheels_handles_missing_wheels_directory>
      <Function test_install_python_cli_offline_handles_python_not_found>
      <Function test_install_python_cli_offline_handles_subprocess_timeout>
      <Function test_run_offline_installation_validates_bundle_structure>
      <Function test_offline_validation_checks_framework_file_count>
      <Function test_offline_installation_handles_network_check_exception>
    <Class TestDeployErrorHandling>
      <Function test_deploy_framework_files_handles_permission_error>
      <Function test_deploy_framework_files_preserves_user_configs>
      <Function test_set_file_permissions_handles_readonly_files>
      <Function test_deploy_handles_disk_full_error>
      <Function test_should_exclude_pattern_matching>
      <Function test_deploy_excludes_no_deploy_directories>
    <Class TestRollbackErrorHandling>
      <Function test_list_backups_handles_corrupted_manifest>
      <Function test_restore_from_backup_handles_missing_backup_dir>
      <Function test_restore_from_backup_handles_permission_error_during_copy>
      <Function test_verify_rollback_checks_backup_integrity>
    <Class TestInstallLoggerEdgeCases>
      <Function test_install_logger_creates_parent_directories>
      <Function test_install_logger_rotates_large_log_files>
      <Function test_install_logger_sets_file_permissions_0600>
      <Function test_install_logger_appends_not_overwrites>
      <Function test_install_logger_includes_stack_trace_in_error_log>
      <Function test_install_logger_iso_timestamp_format>
    <Class TestInstallPyErrorHandling>
      <Function test_install_detects_fresh_vs_upgrade_mode>
      <Function test_install_handles_version_file_read_error>
      <Function test_install_creates_backup_before_deployment>
      <Function test_update_version_file_handles_write_permission_error>
      <Function test_install_validates_source_directory_structure>
  <Module test_coverage_gaps_infrastructure_layer.py>
    <Class TestLockFileManagerEdgeCases>
      <Function test_acquire_lock_creates_lock_directory>
      <Function test_acquire_lock_detects_concurrent_installation>
      <Function test_acquire_lock_removes_stale_lock_dead_pid>
      <Function test_acquire_lock_timeout_respects_timeout_duration>
      <Function test_acquire_lock_atomic_creation_prevents_race_condition>
      <Function test_release_lock_removes_lock_file>
      <Function test_get_locked_pid_extracts_correct_pid>
    <Class TestClaudeParserErrorCases>
      <Function test_parse_empty_markdown_document>
      <Function test_parse_document_without_section_headers>
      <Function test_parse_nested_section_hierarchy>
      <Function test_parse_section_with_special_characters>
      <Function test_parse_multiline_section_content>
      <Function test_is_devforgeai_section_detection>
      <Function test_parse_section_line_numbers>
    <Class TestErrorCategorizerEdgeCases>
      <Function test_categorize_permission_error_type>
      <Function test_categorize_file_not_found_error>
      <Function test_categorize_error_with_rollback_triggered>
      <Function test_categorize_error_with_validation_phase>
      <Function test_format_user_friendly_message_excludes_stack_trace>
      <Function test_error_message_includes_resolution_steps>
      <Function test_error_message_includes_log_file_reference>
    <Class TestVersionDetectionEdgeCases>
      <Function test_get_installed_version_returns_none_when_missing>
      <Function test_get_source_version_raises_when_missing>
      <Function test_get_version_raises_on_invalid_json>
      <Function test_compare_versions_detects_patch_upgrade>
      <Function test_compare_versions_detects_minor_upgrade>
      <Function test_compare_versions_detects_major_upgrade>
      <Function test_compare_versions_detects_downgrade>
      <Function test_compare_versions_detects_reinstall>
      <Function test_version_validation_requires_semantic_versioning>
    <Class TestTemplateVariableDetectionEdgeCases>
      <Function test_detect_project_name_from_git_remote>
      <Function test_detect_python_version>
      <Function test_detect_python_path>
      <Function test_detect_tech_stack_from_package_json>
      <Function test_detect_tech_stack_from_requirements_txt>
      <Function test_substitute_variables_in_content>
      <Function test_handles_subprocess_timeout_gracefully>
  <Module test_error_handling_edge_cases.py>
    <Class TestBackupCreationFailures>
      <Function test_backup_directory_creation_failure_halts_installation>
      <Function test_disk_full_during_backup_creation_handled>
      <Function test_backup_with_large_files_handles_memory_efficiently>
    <Class TestLogFileEdgeCases>
      <Function test_log_file_permission_denied_degrades_gracefully>
      <Function test_log_rotation_when_exceeding_10mb>
      <Function test_log_contains_sanitized_paths_no_usernames>
    <Class TestPartialRollbackScenarios>
      <Function test_rollback_when_backup_missing_logs_error>
      <Function test_rollback_when_backup_partially_deleted>
      <Function test_rollback_with_corrupted_backup_manifest>
      <Function test_rollback_cleanup_with_non_empty_directories>
    <Class TestInterruptionHandling>
      <Function test_ctrl_c_during_backup_triggers_cleanup>
      <Function test_ctrl_c_during_rollback_completes_gracefully>
    <Class TestPathSanitization>
      <Function test_error_message_sanitizes_unix_home_paths>
      <Function test_console_output_sanitizes_windows_user_paths>
    <Class TestConcurrentErrors>
      <Function test_multiple_errors_during_rollback_all_logged>
      <Function test_error_handler_thread_safe_concurrent_logging>
    <Class TestDiskFullScenarios>
      <Function test_rollback_when_disk_full_logs_critical_error>
  <Module test_error_recovery.py>
    <Class TestErrorRecovery>
      <Function test_error_permission_denied_triggers_rollback>
      <Function test_error_disk_full_triggers_rollback>
      <Function test_error_corrupted_backup_prevents_rollback>
      <Function test_error_deployment_failure_no_partial_state>
      <Function test_error_recovery_messages_guide_user>
      <Function test_error_leaves_project_valid>
  <Module test_fresh_install_workflow.py>
    <Class TestFreshInstallWorkflow>
      <Function test_fresh_install_deploys_all_files>
      <Function test_fresh_install_creates_version_metadata>
      <Function test_fresh_install_sets_permissions>
      <Function test_fresh_install_creates_backups_directory>
      <Function test_fresh_install_detects_correct_mode>
      <Function test_fresh_install_completes_within_nfr_time>
      <Function test_fresh_install_to_nonexistent_directory>
      <Function test_fresh_install_leaves_valid_state>
  <Module test_integration_error_handling.py>
    <Class TestFullRollbackFlow>
      <Function test_rollback_after_file_copy_error_exit_code_3>
      <Function test_rollback_restores_backup_correctly>
      <Function test_rollback_cleanup_removes_empty_directories>
      <Function test_rollback_performance_under_5_seconds>
    <Class TestConcurrentPrevention>
      <Function test_concurrent_install_blocked_by_lock_file>
      <Function test_stale_lock_file_cleaned_up>
      <Function test_lock_release_allows_subsequent_install>
    <Class TestRealFileOperations>
      <Function test_missing_source_files_error_exit_code_1>
      <Function test_permission_denied_error_exit_code_2>
      <Function test_validation_failed_error_exit_code_4>
    <Class TestPerformanceValidation>
      <Function test_backup_creation_under_10_seconds_for_500_files>
      <Function test_log_file_creation_performance_under_100ms>
    <Class TestLogCreationAndContent>
      <Function test_log_file_created_with_correct_permissions>
      <Function test_log_contains_iso8601_timestamps_and_context>
  <Module test_offline_installation_workflow.py>
    <Class TestOfflineInstallationWorkflow>
      <Function test_network_detection_triggers_offline_mode>
      <Function test_bundle_structure_validation_before_installation>
      <Function test_checksum_verification_prevents_tampered_bundle>
      <Function test_path_validation_prevents_traversal_attacks>
      <Function test_python_detection_and_cli_installation>
      <Function test_graceful_degradation_for_missing_python>
      <Function test_network_feature_unavailable_warnings>
      <Function test_offline_validation_checks_all_requirements>
      <Function test_bundle_size_measurement_for_performance>
      <Function test_no_external_downloads_during_installation>
      <Function test_json_schema_validation_for_checksums>
      <Function test_cross_module_error_propagation>
      <Function test_installation_performance_meets_requirements>
    <Class TestOfflineInstallationEdgeCases>
      <Function test_partial_bundle_missing_files>
      <Function test_checksum_file_corrupted>
      <Function test_disk_space_check_with_negative_value>
  <Module test_performance_benchmarks.py>
    <Class TestPerformanceBenchmarks>
      <Function test_performance_fresh_install_time>
      <Function test_performance_patch_upgrade_time>
      <Function test_performance_backup_creation_time>
      <Function test_performance_rollback_time>
      <Function test_performance_validation_time>
      <Function test_performance_file_deployment_rate>
      <Function test_performance_no_memory_leaks>
  <Module test_rollback_workflow.py>
    <Class TestRollbackWorkflow>
      <Function test_rollback_restores_all_files>
      <Function test_rollback_reverts_version_metadata>
      <Function test_rollback_verifies_checksums>
      <Function test_rollback_completes_within_nfr>
      <Function test_rollback_restores_from_most_recent>
      <Function test_rollback_leaves_valid_state>
  <Module test_uninstall_workflow.py>
    <Class TestUninstallWorkflow>
      <Function test_uninstall_creates_backup>
      <Function test_uninstall_removes_framework_files>
      <Function test_uninstall_preserves_user_data>
      <Function test_uninstall_removes_version_metadata>
      <Function test_uninstall_completes_successfully>
  <Module test_upgrade_workflow.py>
    <Class TestUpgradeWorkflow>
      <Function test_upgrade_detects_patch_mode>
      <Function test_upgrade_creates_backup_before_deployment>
      <Function test_upgrade_preserves_user_configurations>
      <Function test_upgrade_selective_update>
      <Function test_upgrade_updates_version_metadata>
      <Function test_upgrade_completes_within_nfr>
      <Function test_upgrade_rollback_capability>
  <Module test_validate_workflow.py>
    <Class TestValidateWorkflow>
      <Function test_validate_healthy_installation>
      <Function test_validate_detects_missing_files>
      <Function test_validate_detects_corruption>
      <Function test_validate_completes_within_nfr>
      <Function test_validate_performs_no_modifications>

============================================= 562 tests collected in 1.66s =============================================
bryan@DESKTOP-88FARC5:/mnt/c/Projects/DevForgeAI2$ python3 -m pytest installer/tests/ -q --tb=no
================================================= test session starts ==================================================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.6.0
rootdir: /mnt/c/Projects/DevForgeAI2
configfile: pytest.ini
plugins: mock-3.15.0, cov-4.1.0, asyncio-0.21.2, anyio-4.10.0
asyncio: mode=Mode.STRICT
collected 562 items

installer/tests/test_backup_management.py ..........                                                             [  1%]
installer/tests/test_backup_service.py ..................                                                        [  4%]
installer/tests/test_bundle.py .............................                                                     [ 10%]
installer/tests/test_checksum.py .......................                                                         [ 14%]
installer/tests/test_deployment_engine.py ...............                                                        [ 16%]
installer/tests/test_edge_cases.py .................                                                             [ 19%]
installer/tests/test_error_handler.py ........................                                                   [ 24%]
installer/tests/test_error_handling_edge_cases.py ...................                                            [ 27%]
installer/tests/test_exit_codes.py ..............                                                                [ 30%]
installer/tests/test_install_logger.py ......................                                                    [ 33%]
installer/tests/test_installation_modes.py ........                                                              [ 35%]
installer/tests/test_integration_error_handling.py ..............                                                [ 37%]
installer/tests/test_lock_file_manager.py ....................                                                   [ 41%]
installer/tests/test_main.py ................                                                                    [ 44%]
installer/tests/test_network.py .............................                                                    [ 49%]
installer/tests/test_offline_installer.py .......................................                                [ 56%]
installer/tests/test_rollback_manager.py ............                                                            [ 58%]
installer/tests/test_rollback_service.py ................                                                        [ 61%]
installer/tests/test_schemas.py ...........................                                                      [ 66%]
installer/tests/test_version_detection.py ..............                                                         [ 68%]
installer/tests/integration/test_claude_md_merge_with_installer.py F....................                         [ 72%]
installer/tests/integration/test_coverage_gaps_application_layer.py ...........................                  [ 77%]
installer/tests/integration/test_coverage_gaps_infrastructure_layer.py .....................................     [ 83%]
installer/tests/integration/test_error_handling_edge_cases.py .................                                  [ 86%]
installer/tests/integration/test_error_recovery.py ......                                                        [ 87%]
installer/tests/integration/test_fresh_install_workflow.py ........                                              [ 89%]
installer/tests/integration/test_integration_error_handling.py ..............                                    [ 91%]
installer/tests/integration/test_offline_installation_workflow.py ................                               [ 94%]
installer/tests/integration/test_performance_benchmarks.py .......                                               [ 95%]
installer/tests/integration/test_rollback_workflow.py .....F                                                     [ 96%]
installer/tests/integration/test_uninstall_workflow.py ..ss.                                                     [ 97%]
installer/tests/integration/test_upgrade_workflow.py ...s...                                                     [ 99%]
installer/tests/integration/test_validate_workflow.py .....                                                      [100%]

=============================================== short test summary info ================================================
FAILED installer/tests/integration/test_claude_md_merge_with_installer.py::TestScenario1FreshInstall::test_fresh_install_creates_claude_md - FileNotFoundError: Source directory structure incomplete. Missing directories: [PosixPath('/tmp/tmpb5681mi7/source/...
FAILED installer/tests/integration/test_rollback_workflow.py::TestRollbackWorkflow::test_rollback_leaves_valid_state - AssertionError: Project should be valid after rollback
================================ 2 failed, 557 passed, 3 skipped, 37 warnings in 29.38s ================================
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-76f9b046-65b0-4e54-9c31-dca04e81d217/test_backup_directory_creation0/integration_project/.devforgeai/qa:
<class 'PermissionError'>: [Errno 13] Permission denied: 'qa'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-76f9b046-65b0-4e54-9c31-dca04e81d217/test_backup_directory_creation0/integration_project/.devforgeai/specs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'specs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-76f9b046-65b0-4e54-9c31-dca04e81d217/test_backup_directory_creation0/integration_project/.devforgeai/config:
<class 'PermissionError'>: [Errno 13] Permission denied: 'config'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-76f9b046-65b0-4e54-9c31-dca04e81d217/test_backup_directory_creation0/integration_project/.devforgeai/context:
<class 'PermissionError'>: [Errno 13] Permission denied: 'context'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-76f9b046-65b0-4e54-9c31-dca04e81d217/test_backup_directory_creation0/integration_project/.devforgeai/adrs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'adrs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-76f9b046-65b0-4e54-9c31-dca04e81d217/test_backup_directory_creation0/integration_project/.devforgeai/protocols:
<class 'PermissionError'>: [Errno 13] Permission denied: 'protocols'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-76f9b046-65b0-4e54-9c31-dca04e81d217/test_backup_directory_creation0/integration_project/.devforgeai
<class 'OSError'>: [Errno 39] Directory not empty: '.devforgeai'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-76f9b046-65b0-4e54-9c31-dca04e81d217/test_backup_directory_creation0/integration_project
<class 'OSError'>: [Errno 39] Directory not empty: 'integration_project'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-76f9b046-65b0-4e54-9c31-dca04e81d217/test_backup_directory_creation0
<class 'OSError'>: [Errno 39] Directory not empty: 'test_backup_directory_creation0'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-76f9b046-65b0-4e54-9c31-dca04e81d217
<class 'OSError'>: [Errno 39] Directory not empty: '/tmp/pytest-of-bryan/garbage-76f9b046-65b0-4e54-9c31-dca04e81d217'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-1df7e1db-221f-431a-8187-0542242bb9dd/test_backup_directory_creation0/integration_project/.devforgeai/qa:
<class 'PermissionError'>: [Errno 13] Permission denied: 'qa'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-1df7e1db-221f-431a-8187-0542242bb9dd/test_backup_directory_creation0/integration_project/.devforgeai/specs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'specs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-1df7e1db-221f-431a-8187-0542242bb9dd/test_backup_directory_creation0/integration_project/.devforgeai/config:
<class 'PermissionError'>: [Errno 13] Permission denied: 'config'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-1df7e1db-221f-431a-8187-0542242bb9dd/test_backup_directory_creation0/integration_project/.devforgeai/context:
<class 'PermissionError'>: [Errno 13] Permission denied: 'context'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-1df7e1db-221f-431a-8187-0542242bb9dd/test_backup_directory_creation0/integration_project/.devforgeai/adrs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'adrs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-1df7e1db-221f-431a-8187-0542242bb9dd/test_backup_directory_creation0/integration_project/.devforgeai/protocols:
<class 'PermissionError'>: [Errno 13] Permission denied: 'protocols'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-1df7e1db-221f-431a-8187-0542242bb9dd/test_backup_directory_creation0/integration_project/.devforgeai
<class 'OSError'>: [Errno 39] Directory not empty: '.devforgeai'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-1df7e1db-221f-431a-8187-0542242bb9dd/test_backup_directory_creation0/integration_project
<class 'OSError'>: [Errno 39] Directory not empty: 'integration_project'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-1df7e1db-221f-431a-8187-0542242bb9dd/test_backup_directory_creation0
<class 'OSError'>: [Errno 39] Directory not empty: 'test_backup_directory_creation0'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-1df7e1db-221f-431a-8187-0542242bb9dd
<class 'OSError'>: [Errno 39] Directory not empty: '/tmp/pytest-of-bryan/garbage-1df7e1db-221f-431a-8187-0542242bb9dd'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-93335599-7674-46e9-8c03-476695e10716/test_backup_directory_creation0/integration_project/.devforgeai/qa:
<class 'PermissionError'>: [Errno 13] Permission denied: 'qa'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-93335599-7674-46e9-8c03-476695e10716/test_backup_directory_creation0/integration_project/.devforgeai/specs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'specs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-93335599-7674-46e9-8c03-476695e10716/test_backup_directory_creation0/integration_project/.devforgeai/config:
<class 'PermissionError'>: [Errno 13] Permission denied: 'config'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-93335599-7674-46e9-8c03-476695e10716/test_backup_directory_creation0/integration_project/.devforgeai/context:
<class 'PermissionError'>: [Errno 13] Permission denied: 'context'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-93335599-7674-46e9-8c03-476695e10716/test_backup_directory_creation0/integration_project/.devforgeai/adrs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'adrs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-93335599-7674-46e9-8c03-476695e10716/test_backup_directory_creation0/integration_project/.devforgeai/protocols:
<class 'PermissionError'>: [Errno 13] Permission denied: 'protocols'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-93335599-7674-46e9-8c03-476695e10716/test_backup_directory_creation0/integration_project/.devforgeai
<class 'OSError'>: [Errno 39] Directory not empty: '.devforgeai'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-93335599-7674-46e9-8c03-476695e10716/test_backup_directory_creation0/integration_project
<class 'OSError'>: [Errno 39] Directory not empty: 'integration_project'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-93335599-7674-46e9-8c03-476695e10716/test_backup_directory_creation0
<class 'OSError'>: [Errno 39] Directory not empty: 'test_backup_directory_creation0'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-93335599-7674-46e9-8c03-476695e10716
<class 'OSError'>: [Errno 39] Directory not empty: '/tmp/pytest-of-bryan/garbage-93335599-7674-46e9-8c03-476695e10716'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-400db1af-a044-43a9-a45e-22f7f9fed4bf/test_backup_directory_creation0/integration_project/.devforgeai/qa:
<class 'PermissionError'>: [Errno 13] Permission denied: 'qa'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-400db1af-a044-43a9-a45e-22f7f9fed4bf/test_backup_directory_creation0/integration_project/.devforgeai/specs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'specs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-400db1af-a044-43a9-a45e-22f7f9fed4bf/test_backup_directory_creation0/integration_project/.devforgeai/config:
<class 'PermissionError'>: [Errno 13] Permission denied: 'config'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-400db1af-a044-43a9-a45e-22f7f9fed4bf/test_backup_directory_creation0/integration_project/.devforgeai/context:
<class 'PermissionError'>: [Errno 13] Permission denied: 'context'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-400db1af-a044-43a9-a45e-22f7f9fed4bf/test_backup_directory_creation0/integration_project/.devforgeai/adrs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'adrs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-400db1af-a044-43a9-a45e-22f7f9fed4bf/test_backup_directory_creation0/integration_project/.devforgeai/protocols:
<class 'PermissionError'>: [Errno 13] Permission denied: 'protocols'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-400db1af-a044-43a9-a45e-22f7f9fed4bf/test_backup_directory_creation0/integration_project/.devforgeai
<class 'OSError'>: [Errno 39] Directory not empty: '.devforgeai'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-400db1af-a044-43a9-a45e-22f7f9fed4bf/test_backup_directory_creation0/integration_project
<class 'OSError'>: [Errno 39] Directory not empty: 'integration_project'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-400db1af-a044-43a9-a45e-22f7f9fed4bf/test_backup_directory_creation0
<class 'OSError'>: [Errno 39] Directory not empty: 'test_backup_directory_creation0'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-400db1af-a044-43a9-a45e-22f7f9fed4bf
<class 'OSError'>: [Errno 39] Directory not empty: '/tmp/pytest-of-bryan/garbage-400db1af-a044-43a9-a45e-22f7f9fed4bf'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-fc803a48-1a6d-4e16-8fb7-13de2e9f8478/test_backup_directory_creation0/integration_project/.devforgeai/qa:
<class 'PermissionError'>: [Errno 13] Permission denied: 'qa'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-fc803a48-1a6d-4e16-8fb7-13de2e9f8478/test_backup_directory_creation0/integration_project/.devforgeai/specs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'specs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-fc803a48-1a6d-4e16-8fb7-13de2e9f8478/test_backup_directory_creation0/integration_project/.devforgeai/config:
<class 'PermissionError'>: [Errno 13] Permission denied: 'config'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-fc803a48-1a6d-4e16-8fb7-13de2e9f8478/test_backup_directory_creation0/integration_project/.devforgeai/context:
<class 'PermissionError'>: [Errno 13] Permission denied: 'context'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-fc803a48-1a6d-4e16-8fb7-13de2e9f8478/test_backup_directory_creation0/integration_project/.devforgeai/adrs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'adrs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-fc803a48-1a6d-4e16-8fb7-13de2e9f8478/test_backup_directory_creation0/integration_project/.devforgeai/protocols:
<class 'PermissionError'>: [Errno 13] Permission denied: 'protocols'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-fc803a48-1a6d-4e16-8fb7-13de2e9f8478/test_backup_directory_creation0/integration_project/.devforgeai
<class 'OSError'>: [Errno 39] Directory not empty: '.devforgeai'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-fc803a48-1a6d-4e16-8fb7-13de2e9f8478/test_backup_directory_creation0/integration_project
<class 'OSError'>: [Errno 39] Directory not empty: 'integration_project'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-fc803a48-1a6d-4e16-8fb7-13de2e9f8478/test_backup_directory_creation0
<class 'OSError'>: [Errno 39] Directory not empty: 'test_backup_directory_creation0'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-fc803a48-1a6d-4e16-8fb7-13de2e9f8478
<class 'OSError'>: [Errno 39] Directory not empty: '/tmp/pytest-of-bryan/garbage-fc803a48-1a6d-4e16-8fb7-13de2e9f8478'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-22438892-8c9a-4e41-a7c4-639d5888895c/test_backup_directory_creation0/integration_project/.devforgeai/qa:
<class 'PermissionError'>: [Errno 13] Permission denied: 'qa'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-22438892-8c9a-4e41-a7c4-639d5888895c/test_backup_directory_creation0/integration_project/.devforgeai/specs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'specs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-22438892-8c9a-4e41-a7c4-639d5888895c/test_backup_directory_creation0/integration_project/.devforgeai/config:
<class 'PermissionError'>: [Errno 13] Permission denied: 'config'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-22438892-8c9a-4e41-a7c4-639d5888895c/test_backup_directory_creation0/integration_project/.devforgeai/context:
<class 'PermissionError'>: [Errno 13] Permission denied: 'context'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-22438892-8c9a-4e41-a7c4-639d5888895c/test_backup_directory_creation0/integration_project/.devforgeai/adrs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'adrs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-22438892-8c9a-4e41-a7c4-639d5888895c/test_backup_directory_creation0/integration_project/.devforgeai/protocols:
<class 'PermissionError'>: [Errno 13] Permission denied: 'protocols'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-22438892-8c9a-4e41-a7c4-639d5888895c/test_backup_directory_creation0/integration_project/.devforgeai
<class 'OSError'>: [Errno 39] Directory not empty: '.devforgeai'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-22438892-8c9a-4e41-a7c4-639d5888895c/test_backup_directory_creation0/integration_project
<class 'OSError'>: [Errno 39] Directory not empty: 'integration_project'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-22438892-8c9a-4e41-a7c4-639d5888895c/test_backup_directory_creation0
<class 'OSError'>: [Errno 39] Directory not empty: 'test_backup_directory_creation0'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-22438892-8c9a-4e41-a7c4-639d5888895c
<class 'OSError'>: [Errno 39] Directory not empty: '/tmp/pytest-of-bryan/garbage-22438892-8c9a-4e41-a7c4-639d5888895c'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-8274fad7-edae-4c68-98a3-8d70904f4fa8/test_backup_directory_creation0/integration_project/.devforgeai/qa:
<class 'PermissionError'>: [Errno 13] Permission denied: 'qa'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-8274fad7-edae-4c68-98a3-8d70904f4fa8/test_backup_directory_creation0/integration_project/.devforgeai/specs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'specs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-8274fad7-edae-4c68-98a3-8d70904f4fa8/test_backup_directory_creation0/integration_project/.devforgeai/config:
<class 'PermissionError'>: [Errno 13] Permission denied: 'config'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-8274fad7-edae-4c68-98a3-8d70904f4fa8/test_backup_directory_creation0/integration_project/.devforgeai/context:
<class 'PermissionError'>: [Errno 13] Permission denied: 'context'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-8274fad7-edae-4c68-98a3-8d70904f4fa8/test_backup_directory_creation0/integration_project/.devforgeai/adrs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'adrs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-8274fad7-edae-4c68-98a3-8d70904f4fa8/test_backup_directory_creation0/integration_project/.devforgeai/protocols:
<class 'PermissionError'>: [Errno 13] Permission denied: 'protocols'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-8274fad7-edae-4c68-98a3-8d70904f4fa8/test_backup_directory_creation0/integration_project/.devforgeai
<class 'OSError'>: [Errno 39] Directory not empty: '.devforgeai'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-8274fad7-edae-4c68-98a3-8d70904f4fa8/test_backup_directory_creation0/integration_project
<class 'OSError'>: [Errno 39] Directory not empty: 'integration_project'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-8274fad7-edae-4c68-98a3-8d70904f4fa8/test_backup_directory_creation0
<class 'OSError'>: [Errno 39] Directory not empty: 'test_backup_directory_creation0'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-8274fad7-edae-4c68-98a3-8d70904f4fa8
<class 'OSError'>: [Errno 39] Directory not empty: '/tmp/pytest-of-bryan/garbage-8274fad7-edae-4c68-98a3-8d70904f4fa8'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-bd8acdaf-fd29-469f-835f-44f815dc2f8c/test_backup_directory_creation0/integration_project/.devforgeai/qa:
<class 'PermissionError'>: [Errno 13] Permission denied: 'qa'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-bd8acdaf-fd29-469f-835f-44f815dc2f8c/test_backup_directory_creation0/integration_project/.devforgeai/specs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'specs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-bd8acdaf-fd29-469f-835f-44f815dc2f8c/test_backup_directory_creation0/integration_project/.devforgeai/config:
<class 'PermissionError'>: [Errno 13] Permission denied: 'config'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-bd8acdaf-fd29-469f-835f-44f815dc2f8c/test_backup_directory_creation0/integration_project/.devforgeai/context:
<class 'PermissionError'>: [Errno 13] Permission denied: 'context'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-bd8acdaf-fd29-469f-835f-44f815dc2f8c/test_backup_directory_creation0/integration_project/.devforgeai/adrs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'adrs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-bd8acdaf-fd29-469f-835f-44f815dc2f8c/test_backup_directory_creation0/integration_project/.devforgeai/protocols:
<class 'PermissionError'>: [Errno 13] Permission denied: 'protocols'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-bd8acdaf-fd29-469f-835f-44f815dc2f8c/test_backup_directory_creation0/integration_project/.devforgeai
<class 'OSError'>: [Errno 39] Directory not empty: '.devforgeai'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-bd8acdaf-fd29-469f-835f-44f815dc2f8c/test_backup_directory_creation0/integration_project
<class 'OSError'>: [Errno 39] Directory not empty: 'integration_project'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-bd8acdaf-fd29-469f-835f-44f815dc2f8c/test_backup_directory_creation0
<class 'OSError'>: [Errno 39] Directory not empty: 'test_backup_directory_creation0'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-bd8acdaf-fd29-469f-835f-44f815dc2f8c
<class 'OSError'>: [Errno 39] Directory not empty: '/tmp/pytest-of-bryan/garbage-bd8acdaf-fd29-469f-835f-44f815dc2f8c'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-ccfecb3e-4e96-43ce-9a6f-9f775412a0eb/test_backup_directory_creation0/integration_project/.devforgeai/qa:
<class 'PermissionError'>: [Errno 13] Permission denied: 'qa'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-ccfecb3e-4e96-43ce-9a6f-9f775412a0eb/test_backup_directory_creation0/integration_project/.devforgeai/specs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'specs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-ccfecb3e-4e96-43ce-9a6f-9f775412a0eb/test_backup_directory_creation0/integration_project/.devforgeai/config:
<class 'PermissionError'>: [Errno 13] Permission denied: 'config'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-ccfecb3e-4e96-43ce-9a6f-9f775412a0eb/test_backup_directory_creation0/integration_project/.devforgeai/context:
<class 'PermissionError'>: [Errno 13] Permission denied: 'context'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-ccfecb3e-4e96-43ce-9a6f-9f775412a0eb/test_backup_directory_creation0/integration_project/.devforgeai/adrs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'adrs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-ccfecb3e-4e96-43ce-9a6f-9f775412a0eb/test_backup_directory_creation0/integration_project/.devforgeai/protocols:
<class 'PermissionError'>: [Errno 13] Permission denied: 'protocols'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-ccfecb3e-4e96-43ce-9a6f-9f775412a0eb/test_backup_directory_creation0/integration_project/.devforgeai
<class 'OSError'>: [Errno 39] Directory not empty: '.devforgeai'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-ccfecb3e-4e96-43ce-9a6f-9f775412a0eb/test_backup_directory_creation0/integration_project
<class 'OSError'>: [Errno 39] Directory not empty: 'integration_project'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-ccfecb3e-4e96-43ce-9a6f-9f775412a0eb/test_backup_directory_creation0
<class 'OSError'>: [Errno 39] Directory not empty: 'test_backup_directory_creation0'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-ccfecb3e-4e96-43ce-9a6f-9f775412a0eb
<class 'OSError'>: [Errno 39] Directory not empty: '/tmp/pytest-of-bryan/garbage-ccfecb3e-4e96-43ce-9a6f-9f775412a0eb'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-8b9bd65d-1872-49bb-9a8d-48c1868e1f33/test_backup_directory_creation0/integration_project/.devforgeai/qa:
<class 'PermissionError'>: [Errno 13] Permission denied: 'qa'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-8b9bd65d-1872-49bb-9a8d-48c1868e1f33/test_backup_directory_creation0/integration_project/.devforgeai/specs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'specs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-8b9bd65d-1872-49bb-9a8d-48c1868e1f33/test_backup_directory_creation0/integration_project/.devforgeai/config:
<class 'PermissionError'>: [Errno 13] Permission denied: 'config'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-8b9bd65d-1872-49bb-9a8d-48c1868e1f33/test_backup_directory_creation0/integration_project/.devforgeai/context:
<class 'PermissionError'>: [Errno 13] Permission denied: 'context'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-8b9bd65d-1872-49bb-9a8d-48c1868e1f33/test_backup_directory_creation0/integration_project/.devforgeai/adrs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'adrs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-8b9bd65d-1872-49bb-9a8d-48c1868e1f33/test_backup_directory_creation0/integration_project/.devforgeai/protocols:
<class 'PermissionError'>: [Errno 13] Permission denied: 'protocols'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-8b9bd65d-1872-49bb-9a8d-48c1868e1f33/test_backup_directory_creation0/integration_project/.devforgeai
<class 'OSError'>: [Errno 39] Directory not empty: '.devforgeai'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-8b9bd65d-1872-49bb-9a8d-48c1868e1f33/test_backup_directory_creation0/integration_project
<class 'OSError'>: [Errno 39] Directory not empty: 'integration_project'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-8b9bd65d-1872-49bb-9a8d-48c1868e1f33/test_backup_directory_creation0
<class 'OSError'>: [Errno 39] Directory not empty: 'test_backup_directory_creation0'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-8b9bd65d-1872-49bb-9a8d-48c1868e1f33
<class 'OSError'>: [Errno 39] Directory not empty: '/tmp/pytest-of-bryan/garbage-8b9bd65d-1872-49bb-9a8d-48c1868e1f33'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-579b2441-08b2-41a8-a224-a9a1d89ab1f4/test_backup_directory_creation0/integration_project/.devforgeai/qa:
<class 'PermissionError'>: [Errno 13] Permission denied: 'qa'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-579b2441-08b2-41a8-a224-a9a1d89ab1f4/test_backup_directory_creation0/integration_project/.devforgeai/specs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'specs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-579b2441-08b2-41a8-a224-a9a1d89ab1f4/test_backup_directory_creation0/integration_project/.devforgeai/config:
<class 'PermissionError'>: [Errno 13] Permission denied: 'config'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-579b2441-08b2-41a8-a224-a9a1d89ab1f4/test_backup_directory_creation0/integration_project/.devforgeai/context:
<class 'PermissionError'>: [Errno 13] Permission denied: 'context'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-579b2441-08b2-41a8-a224-a9a1d89ab1f4/test_backup_directory_creation0/integration_project/.devforgeai/adrs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'adrs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-579b2441-08b2-41a8-a224-a9a1d89ab1f4/test_backup_directory_creation0/integration_project/.devforgeai/protocols:
<class 'PermissionError'>: [Errno 13] Permission denied: 'protocols'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-579b2441-08b2-41a8-a224-a9a1d89ab1f4/test_backup_directory_creation0/integration_project/.devforgeai
<class 'OSError'>: [Errno 39] Directory not empty: '.devforgeai'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-579b2441-08b2-41a8-a224-a9a1d89ab1f4/test_backup_directory_creation0/integration_project
<class 'OSError'>: [Errno 39] Directory not empty: 'integration_project'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-579b2441-08b2-41a8-a224-a9a1d89ab1f4/test_backup_directory_creation0
<class 'OSError'>: [Errno 39] Directory not empty: 'test_backup_directory_creation0'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-579b2441-08b2-41a8-a224-a9a1d89ab1f4
<class 'OSError'>: [Errno 39] Directory not empty: '/tmp/pytest-of-bryan/garbage-579b2441-08b2-41a8-a224-a9a1d89ab1f4'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-3a4f40f7-71b6-4a52-a1df-2da539d4d2e6/test_backup_directory_creation0/integration_project/.devforgeai/qa:
<class 'PermissionError'>: [Errno 13] Permission denied: 'qa'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-3a4f40f7-71b6-4a52-a1df-2da539d4d2e6/test_backup_directory_creation0/integration_project/.devforgeai/specs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'specs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-3a4f40f7-71b6-4a52-a1df-2da539d4d2e6/test_backup_directory_creation0/integration_project/.devforgeai/config:
<class 'PermissionError'>: [Errno 13] Permission denied: 'config'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-3a4f40f7-71b6-4a52-a1df-2da539d4d2e6/test_backup_directory_creation0/integration_project/.devforgeai/context:
<class 'PermissionError'>: [Errno 13] Permission denied: 'context'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-3a4f40f7-71b6-4a52-a1df-2da539d4d2e6/test_backup_directory_creation0/integration_project/.devforgeai/adrs:
<class 'PermissionError'>: [Errno 13] Permission denied: 'adrs'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:102: PytestWarning: (rm_rf) unknown function <built-in function lstat> when removing /tmp/pytest-of-bryan/garbage-3a4f40f7-71b6-4a52-a1df-2da539d4d2e6/test_backup_directory_creation0/integration_project/.devforgeai/protocols:
<class 'PermissionError'>: [Errno 13] Permission denied: 'protocols'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-3a4f40f7-71b6-4a52-a1df-2da539d4d2e6/test_backup_directory_creation0/integration_project/.devforgeai
<class 'OSError'>: [Errno 39] Directory not empty: '.devforgeai'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-3a4f40f7-71b6-4a52-a1df-2da539d4d2e6/test_backup_directory_creation0/integration_project
<class 'OSError'>: [Errno 39] Directory not empty: 'integration_project'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-3a4f40f7-71b6-4a52-a1df-2da539d4d2e6/test_backup_directory_creation0
<class 'OSError'>: [Errno 39] Directory not empty: 'test_backup_directory_creation0'
  warnings.warn(
/home/bryan/.local/lib/python3.12/site-packages/_pytest/pathlib.py:95: PytestWarning: (rm_rf) error removing /tmp/pytest-of-bryan/garbage-3a4f40f7-71b6-4a52-a1df-2da539d4d2e6
<class 'OSError'>: [Errno 39] Directory not empty: '/tmp/pytest-of-bryan/garbage-3a4f40f7-71b6-4a52-a1df-2da539d4d2e6'
  warnings.warn(
bryan@DESKTOP-88FARC5:/mnt/c/Projects/DevForgeAI2$