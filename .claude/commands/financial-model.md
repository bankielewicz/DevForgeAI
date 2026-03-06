---
name: financial-model
description: Generate financial projections, revenue models, and break-even analysis for your business
argument-hint: "[--standalone]"
allowed_tools: Read, Write, Edit
---

# /financial-model

## Purpose

This command provides entrepreneurs with financial modeling capabilities including revenue projections, cost analysis, and break-even calculations.

## Execution

This command delegates to the managing-finances skill for all financial modeling work.

```
Skill(command="managing-finances", args="--phase=financial-model")
```

The managing-finances skill orchestrates the full workflow including context discovery, pricing strategy, revenue projection, and break-even analysis. This command is a thin invoker and contains no inline projection logic.

## Usage

```
/financial-model
/financial-model --standalone
```
