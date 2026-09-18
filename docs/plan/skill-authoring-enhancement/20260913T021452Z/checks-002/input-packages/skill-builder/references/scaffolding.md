# Bundled scaffolding and UI authoring

The adapted init_skill.py and generate_openai_yaml.py are bundled; resolve them relative to this loaded builder. No personal installation path is a dependency. The helpers originate from OpenAI Skill Creator; see [source notice](../assets/skill-creator-notice.md) and its preserved license.

For a new staged package only:

```text
python -B -X utf8 <builder>/scripts/init_skill.py selected-name --path <staging-parent> --resources references --interface display_name=Selected
```

Choose only useful resource directories, omit --resources for a small instruction-only skill, and request --examples only when placeholders help actual authoring. Initialization refuses an occupied directory and never silently selects a different name. Complete or remove placeholders and empty unused resources before delivery. This authoring review is not a quality checker or sample-task run.

For UI metadata, read the included [field reference](openai_yaml.md). New scaffolds include agents/openai.yaml. Focused updates can use generate_openai_yaml.py <candidate> --interface key=value. Existing unrelated interface, policy and dependencies values are preserved; YAML presentation/comments may be normalized by the helper, so use focused text editing when those bytes must remain unchanged. It accepts --allow-implicit-invocation true|false only for an explicitly requested policy change; omit the option to preserve policy. Optional icons, colors and dependency fields are authored only when requested or supplied. Preserve existing fields not selected for editing.

Default prompts should name the skill as $skill-name. Keep automatic invocation for new skills unless the user explicitly requests otherwise. The helper requires already installed PyYAML for existing YAML parsing; if unavailable, author the requested YAML with ordinary tools and mark any actual unresolved capability, without installing dependencies.
