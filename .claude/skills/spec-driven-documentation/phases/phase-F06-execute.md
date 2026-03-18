# Phase F06: Execute Fixes

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=F05 --to=F06 --workflow=doc-fix
# Exit 0: proceed | Exit 1: Phase F05 incomplete
```

## Contract

PURPOSE: Apply automated fixes without prompting, apply interactive fixes with per-fix user approval, resolve template variables for file creation actions.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Fixes applied, fix_details log populated
STEP COUNT: 3 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/audit-fix-catalog.md")
```

IF Read fails: HALT -- "Phase F06 reference file not loaded. Cannot proceed."

---

## Mandatory Steps

### Step F06.1: Apply Automated Fixes

EXECUTE: Process each automated finding and apply its fix action.
```
fix_details = []
files_created = []
files_modified = []

FOR each finding in automated_findings:
    # Load fix action from catalog
    action = finding["fix_action"]
    target = finding["affected"][0]

    # Execute the appropriate fix
    IF action == "create_file":
        # Create file from template with variable resolution
        template_content = get_fix_template(finding["type"])
        resolved = resolve_template_variables(template_content)
        Write(file_path=target, content=resolved)
        files_created.append(target)

    ELIF action == "insert_text":
        # Insert text at specific location in existing file
        content = Read(file_path=target)
        insertion = get_fix_insertion(finding)
        Edit(file_path=target, old_string=insertion_point, new_string=insertion_point + "\n" + insertion)
        files_modified.append(target)

    ELIF action == "replace_text":
        # Replace specific text pattern
        content = Read(file_path=target)
        old_text = finding.get("old_text", "")
        new_text = get_fix_replacement(finding)
        Edit(file_path=target, old_string=old_text, new_string=new_text)
        files_modified.append(target)

    ELIF action == "sync_config":
        # Sync config values between manifest and docs
        Read(file_path=manifest_path)
        Read(file_path=target)
        # Apply sync logic
        files_modified.append(target)

    ELIF action == "insert_badges":
        # Insert standard badges into README
        content = Read(file_path=target)
        badges = generate_badges(manifest_data)
        Edit(file_path=target, old_string=first_heading, new_string=first_heading + "\n\n" + badges)
        files_modified.append(target)

    fix_details.append({
        "id": finding["id"],
        "action": action,
        "status": "applied",
        "target": target
    })

    Display: "  Applied {finding['id']}: {action} -> {target}"

Display: ""
Display: "Automated fixes applied: {len(automated_findings)}"
```
VERIFY: All automated findings processed. fix_details has one entry per automated finding.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F06 --step=F06.1 --workflow=doc-fix`

---

### Step F06.2: Apply Interactive Fixes

EXECUTE: Process each interactive finding with user approval.
```
FOR each finding in interactive_findings:
    action = finding["fix_action"]
    target = finding["affected"][0]

    # Generate proposed change
    proposed = generate_proposed_fix(finding)

    # Display before/after diff or new file preview
    Display: ""
    Display: "Finding {finding['id']}: {finding['summary']}"
    Display: "  Type: {finding['type']}"
    Display: "  Target: {target}"
    Display: "  Action: {action}"
    Display: ""
    Display: "Proposed change:"
    Display: "---"
    Display: proposed
    Display: "---"

    AskUserQuestion:
        Question: "Apply fix {finding['id']}?"
        Header: "Fix"
        Options:
            - label: "Apply"
              description: "Apply the proposed fix as shown"
            - label: "Edit first"
              description: "Provide modified text, then apply"
            - label: "Skip"
              description: "Defer this fix for later"
        multiSelect: false

    IF user chooses "Apply":
        # Execute the fix
        apply_fix(finding, proposed, target)
        fix_details.append({
            "id": finding["id"],
            "action": action,
            "status": "applied",
            "target": target
        })
        IF target in files_created or target not exists before:
            files_created.append(target)
        ELSE:
            files_modified.append(target)
        Display: "  Applied {finding['id']}"

    ELIF user chooses "Edit first":
        # User provides modified content via follow-up
        AskUserQuestion:
            Question: "Provide the modified content for {finding['id']}:"
            Header: "Edit"
            Options:
                - label: "Use provided text"
                  description: "Apply the text I provide"
                - label: "Cancel this fix"
                  description: "Skip this finding"
            multiSelect: false

        # Apply user-modified version
        apply_fix(finding, user_modified_content, target)
        fix_details.append({
            "id": finding["id"],
            "action": action,
            "status": "applied",
            "target": target,
            "reason": "user-edited"
        })
        Display: "  Applied {finding['id']} (user-edited)"

    ELIF user chooses "Skip":
        fix_details.append({
            "id": finding["id"],
            "action": action,
            "status": "skipped",
            "reason": "user deferred"
        })
        Display: "  Skipped {finding['id']}"

Display: ""
applied_interactive = len([d for d in fix_details if d["status"] == "applied" and d["id"] in [f["id"] for f in interactive_findings]])
skipped_interactive = len([d for d in fix_details if d["status"] == "skipped"])
Display: "Interactive fixes: {applied_interactive} applied, {skipped_interactive} skipped"
```
VERIFY: All interactive findings processed (applied or skipped). fix_details complete.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F06 --step=F06.2 --workflow=doc-fix`

---

### Step F06.3: Resolve Template Variables (For File Creation)

EXECUTE: Ensure all newly created files have resolved template variables.
```
FOR each file in files_created:
    content = Read(file_path=file)

    # Check for unresolved variables
    unresolved = Grep(pattern="\\{\\{[a-z_]+\\}\\}", content=content)

    IF unresolved:
        Display: "  Unresolved variables in {file}: {unresolved}"

        # Resolve from manifest
        FOR each var in unresolved:
            var_name = extract_var_name(var)
            IF var_name in manifest_data:
                resolved_value = manifest_data[var_name]
            ELIF var_name == "repo_url":
                # Try git remote
                result = Bash(command="git remote get-url origin 2>/dev/null")
                resolved_value = result.output.strip() if result.exit_code == 0 else ""
            ELSE:
                # Ask user for unresolvable
                AskUserQuestion:
                    Question: "Value for {{" + var_name + "}} in {file}?"
                    Header: "Variable"
                    Options:
                        - label: "Provide value"
                          description: "Enter the value for this variable"
                        - label: "Leave placeholder"
                          description: "Keep the {{variable}} for manual editing later"
                    multiSelect: false
                resolved_value = user_response or var

            Edit(file_path=file, old_string=var, new_string=resolved_value, replace_all=true)

        Display: "  Variables resolved in {file}"
    ELSE:
        Display: "  {file}: No unresolved variables"

Display: "Template variable resolution complete"
```
VERIFY: No unresolved `{{variable}}` patterns in created files (unless user chose to keep placeholders).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F06 --step=F06.3 --workflow=doc-fix`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=F06 --checkpoint-passed --workflow=doc-fix
```

## Phase Transition Display

```
Display: "Phase F06 complete: Execute Fixes"
Display: "  Applied: {len([d for d in fix_details if d['status'] == 'applied'])}"
Display: "  Skipped: {len([d for d in fix_details if d['status'] == 'skipped'])}"
Display: "  Proceeding to Phase F07: Verify Fixes"
```
