---
description: Batch-generate one-line summaries for notes missing the summary frontmatter field using parallel Haiku agents
model: haiku
---

# /auto-summary

Batch-generate one-line `summary` fields for notes missing this frontmatter property. Uses parallel Haiku agents processing notes in batches of 15-20 for fast, cost-effective summary generation. The `summary` field enables AI triage, search results ranking, and quick note previews.

## When to Use This Skill

- Adding summaries to notes that lack them
- Improving search and discovery across the vault
- Preparing notes for AI-assisted triage and retrieval
- Post-migration cleanup to add summary fields
- Generating previews for index pages or dashboards

## Usage

```
/auto-summary [--scope path/to/folder] [--mode suggest|apply] [--max 100]
```

### Parameters

| Parameter  | Description                                          | Required |
|------------|------------------------------------------------------|----------|
| `--scope`  | Folder or glob pattern (default: notes missing summary) | No    |
| `--mode`   | `suggest` shows summaries; `apply` writes them (default: `suggest`) | No |
| `--max`    | Maximum number of notes to process (default: 100)    | No       |

## Instructions

### Phase 1: Identify Notes Needing Summaries

1. **Scan notes in scope** — Find all Markdown files
2. **Parse frontmatter** — Check for existing `summary` field
3. **Filter:** Keep only notes where `summary` is missing or empty
4. **Sort by priority:** ADRs and Concepts first (most benefit from summaries), then Projects, then Meetings
5. **Divide into batches** of 15-20 notes per agent

### Phase 2: Batch Summary Generation — Agent Team (Parallel Haiku Agents)

Use the Batch Processing pattern. Launch N parallel agents.

**Agent 1-N: Summary Writer** (Haiku)
Task: Generate one-line summaries for assigned batch
- For each note:
  1. Read the title, frontmatter, and first 500 words of body content
  2. Generate a one-line summary (max 120 characters) that captures:
     - What the note is about
     - Why it matters (if evident)
     - Key outcome or status (for events)
  3. Match the tone to the note type:
     - ADR: "Decision to [action] for [reason]"
     - Meeting: "[Topic] discussion with [key outcome]"
     - Concept: "[Brief definition or explanation]"
     - Project: "[Project purpose and current status]"
     - Task: "[What needs to be done and why]"
- Quality rules:
  - Single sentence, no line breaks
  - No redundant phrases ("This note is about...")
  - Include the most distinctive/searchable terms
  - UK English
Return: List of `{ filename, generatedSummary }` per note

### Phase 3: Review and Apply

1. **Compile summaries** from all agents
2. **Present for review** in a table
3. If `--mode apply`: Write summaries to frontmatter

## Output Format

```markdown
# Auto-Summary Report

**Date:** YYYY-MM-DD | **Notes Processed:** X | **Summaries Generated:** X

## Summaries

| Note                              | Generated Summary                                   | Apply? |
|-----------------------------------|-----------------------------------------------------|--------|
| `ADR - Event Sourcing.md`         | Decision to adopt event sourcing for order audit trail | Yes   |
| `Meeting - 2026-01-15 Sprint.md`  | Sprint planning covering order service backlog priorities | Yes |
| `Concept - CQRS.md`              | Command Query Responsibility Segregation pattern for read/write separation | Yes |

## Statistics

| Note Type  | Processed | With Summary | Without Summary |
|------------|-----------|--------------|-----------------|
| ADR        | X         | X            | X               |
| Meeting    | X         | X            | X               |
| Concept    | X         | X            | X               |
| Project    | X         | X            | X               |
| Other      | X         | X            | X               |
```

## Examples

### Example 1: Preview All Missing Summaries

```
/auto-summary
```

### Example 2: Apply to ADRs

```
/auto-summary --scope ADRs/ --mode apply
```

### Example 3: Limit to 50 Notes

```
/auto-summary --max 50 --mode suggest
```

---

**Invoke with:** `/auto-summary` to batch-generate summaries for notes missing them
