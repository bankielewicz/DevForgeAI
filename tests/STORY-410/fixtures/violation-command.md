---
description: "A hybrid violation command"
argument-hint: "[args]"
---

# Violation Command

Step 1:
```bash
echo "step 1"
```

Step 2:
```python
print("step 2")
```

Step 3:
```bash
echo "step 3"
```

Step 4:
```yaml
key: value
```

Step 5:
```bash
echo "step 5"
```

Step 6:
```bash
echo "step 6"
```

Now invoke skill:
Skill(command="some-skill", args="$ARGUMENTS")
