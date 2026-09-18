### Step 9: Return Structured Result

```json
{
  "status": "SUCCESS|PARTIAL|FAILED",
  "mode": "story|standalone",
  "story_id": "STORY-XXX or null",
  "component_name": "ComponentName or null",
  "timestamp": "2025-11-05T14:30:00Z",

  "summary": {
    "title": "✅ UI Component Specification Generated",
    "body": "UI specification complete and ready for implementation.",
    "component_count": 3,
    "file_count": 12,
    "validation_issues": 0,
    "validation_warnings": 0
  },

  "components": [
    {
      "name": "LoginForm",
      "type": "Form",
      "framework": "React",
      "styling": "Tailwind CSS",
      "accessibility": "WCAG 2.1 AA",
      "responsive": true,
      "features": ["Email validation", "Password strength indicator", "Remember me"],
      "test_scenarios": 8,
      "estimated_dev_time": "3-4 hours"
    },
    {
      "name": "DataTable",
      "type": "Data Display",
      ...
    }
  ],

  "file_summary": {
    "total_files": 12,
    "by_type": {
      "component": 3,
      "style": 3,
      "test": 3,
      "spec": 3
    },
    "total_lines": 2450,
    "location": "devforgeai/specs/ui/STORY-XXX-ui-spec/"
  },

  "framework_details": {
    "framework": "React 18.2",
    "styling": "Tailwind CSS 3.3",
    "testing": "Vitest + React Testing Library",
    "state_management": "React Hooks"
  },

  "accessibility": {
    "wcag_level": "2.1 AA",
    "keyboard_navigation": true,
    "screen_reader_support": true,
    "aria_labels": true,
    "semantic_html": true,
    "color_contrast_compliant": true
  },

  "responsive_design": {
    "mobile": {
      "breakpoint": "< 640px",
      "supported": true
    },
    "tablet": {
      "breakpoint": "640px - 1024px",
      "supported": true
    },
    "desktop": {
      "breakpoint": "> 1024px",
      "supported": true
    },
    "touch_support": true
  },

  "validation": {
    "issues": [],
    "warnings": [],
    "status": "PASSED"
  },

  "design_md_validation": {
    "exists": true,
    "path": "devforgeai/specs/ui/design.md",
    "component_count": 20,
    "interaction_count": 10,
    "animation_count": 9,
    "token_normalization_pct": 72,
    "dangling_children_refs": 0,
    "uncovered_callbacks": 0,
    "props_missing_children": 0,
    "status": "PASSED"
  },

  "display": {
    "template": "story_success or standalone_success",
    "content": "... full markdown template from Step 6 ...",
    "sections": [
      {
        "title": "Generated Components",
        "subsections": ["Component Summary", "Components Generated"]
      },
      {
        "title": "Generated Files",
        "subsections": ["Summary", "File List"]
      },
      {
        "title": "Implementation Details",
        "subsections": ["Framework Details", "Accessibility", "Responsive Design"]
      }
    ]
  },

  "implementation_guidance": {
    "components_by_priority": [
      {
        "priority": 1,
        "component": "LoginForm",
        "reason": "Essential - blocks other functionality",
        "estimated_time": "3-4 hours",
        "dependencies": ["react", "react-hook-form"],
        "test_scenarios": 8,
        "accessibility_checklist": {...},
        "testing_checklist": {...}
      }
    ],
    "estimated_total_time": "20-25 hours",
    "implementation_order": "Form components → Data display → Navigation"
  },

  "next_steps": [
    "Review generated UI specification: devforgeai/specs/ui/STORY-XXX-ui-spec.md",
    "Begin implementation with TDD: `/dev STORY-XXX`",
    "Follow the spec as your acceptance criteria reference",
    "Run `/qa STORY-XXX` when Dev Complete to validate"
  ],

  "spec_file_location": "devforgeai/specs/ui/STORY-XXX-ui-spec.md",
  "generation_time_seconds": 45
}
```
