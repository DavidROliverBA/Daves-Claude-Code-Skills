---
description: Batch auto-tag notes using parallel Haiku agents to analyse content and suggest hierarchical tags
model: haiku
---

# /auto-tag

Batch auto-tag Markdown notes by analysing their content and suggesting appropriate hierarchical tags. Uses parallel Haiku agents processing notes in batches of 15-20 for cost-effective, high-throughput tagging.

## When to Use This Skill

- Tagging a batch of newly created notes
- Applying a consistent tag taxonomy to existing notes
- Re-tagging notes after a taxonomy migration
- Ensuring all notes meet minimum tag requirements
- Filling in missing tags across the vault

## Usage

```
/auto-tag [--scope path/to/folder] [--mode suggest|apply] [--taxonomy path/to/taxonomy.md]
```

### Parameters

| Parameter     | Description                                          | Required |
|---------------|------------------------------------------------------|----------|
| `--scope`     | Folder or glob pattern (default: notes missing tags) | No       |
| `--mode`      | `suggest` shows tags; `apply` writes them (default: `suggest`) | No |
| `--taxonomy`  | Path to tag taxonomy file for reference              | No       |

## Instructions

### Phase 1: Identify Notes Needing Tags

1. **Scan notes in scope** — Find all Markdown files
2. **Parse frontmatter** — Extract existing tags
3. **Filter to candidates:**
   - Notes with no tags
   - Notes with fewer than 2 tags
   - Notes with flat (non-hierarchical) tags
4. **Load taxonomy** — If provided, use it as the tag reference. Otherwise, scan existing tags to build a frequency-based taxonomy.
5. **Divide into batches** of 15-20 notes per agent

### Phase 2: Batch Tagging — Agent Team (Parallel Haiku Agents)

Use the Batch Processing pattern. Launch N parallel agents, each processing 15-20 notes.

**Agent 1-N: Tag Analyst** (Haiku)
Task: Analyse content and suggest tags for assigned batch
- For each note in the batch:
  1. Read the note title, frontmatter, and body content
  2. Identify the note's `type` to determine minimum required tags
  3. Identify key topics, technologies, domains, and activities
  4. Match topics against the taxonomy (if provided)
  5. Suggest 2-5 hierarchical tags per note
  6. Ensure tags follow the format: `category/subcategory` (e.g., `domain/security`, `technology/aws`)
- Quality rules:
  - No `#` prefix in YAML tags
  - All lowercase
  - Hierarchical format required (e.g., `domain/data` not just `data`)
  - Minimum 2 tags per note
Return: List of `{ filename, existingTags[], suggestedTags[], reason }` per note

### Phase 3: Review and Apply

1. **Compile suggestions** from all agents
2. **Group by confidence:**
   - High: Tags match existing taxonomy entries (auto-apply safe)
   - Medium: Tags inferred from content (review recommended)
   - Low: Novel tags not in taxonomy (manual review required)
3. **Present suggestions** to user in a summary table

If `--mode apply`:
- Apply high-confidence tags automatically
- Present medium/low confidence for user review before applying

## Output Format

```markdown
# Auto-Tag Report

**Date:** YYYY-MM-DD | **Notes Processed:** X | **Tags Suggested:** X

## Summary

| Confidence | Notes | Tags Added | Action         |
|------------|-------|------------|----------------|
| High       | X     | X          | Auto-applied   |
| Medium     | X     | X          | Needs review   |
| Low        | X     | X          | Manual review  |

## Tag Suggestions

### High Confidence

| Note                   | Existing Tags          | Suggested Tags              |
|------------------------|------------------------|-----------------------------|
| `Concept - CQRS.md`   | `[domain/architecture]`| + `activity/design`, `technology/messaging` |

### Medium Confidence

| Note                   | Existing Tags | Suggested Tags       | Reason             |
|------------------------|---------------|----------------------|--------------------|
| `Meeting - 2026-01...` | `[]`          | `project/orders`, `activity/planning` | Content mentions orders project |

### New Tags Introduced

| Tag                     | Suggested For | In Taxonomy? |
|-------------------------|---------------|--------------|
| `domain/observability`  | 3 notes       | No           |
```

## Examples

### Example 1: Tag All Untagged Notes

```
/auto-tag --mode suggest
```

### Example 2: Apply to Specific Folder

```
/auto-tag --scope Meetings/2026/ --mode apply
```

### Example 3: With Custom Taxonomy

```
/auto-tag --taxonomy .claude/context/tag-taxonomy.md --mode suggest
```

---

**Invoke with:** `/auto-tag` to batch-tag notes with AI-suggested hierarchical tags
