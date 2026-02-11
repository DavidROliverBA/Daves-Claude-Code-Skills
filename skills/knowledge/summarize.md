---
description: Summarise any note or set of notes with configurable depth and audience targeting
model: sonnet
---

# /summarize

Summarise any note, document, or set of notes with configurable depth and audience targeting. Produces structured summaries that can be used as executive briefs, study aids, or knowledge base abstracts.

## When to Use This Skill

- Creating quick summaries of long documents
- Generating abstracts for notes missing the `summary` field
- Preparing briefing materials from multiple source notes
- Distilling complex technical content for different audiences
- Creating study guides or revision summaries

## Usage

```
/summarize <path-or-search-term> [--depth one-liner|paragraph|page] [--audience technical|exec|general]
```

### Parameters

| Parameter    | Description                                          | Required |
|--------------|------------------------------------------------------|----------|
| `source`     | Path to note, glob pattern, or search term           | Yes      |
| `--depth`    | Summary length (default: `paragraph`)                | No       |
| `--audience` | Target audience for tone (default: `general`)        | No       |

## Instructions

### Phase 1: Identify Source Content

1. **If path provided:** Read the specified file(s)
2. **If glob pattern:** Find matching files and read them
3. **If search term:** Search the vault for matching notes
4. **For multiple notes:** Read all and prepare for consolidated summary

### Phase 2: Generate Summary

Based on depth setting:

**One-liner:** Single sentence capturing the essence (max 120 characters)
**Paragraph:** 3-5 sentences covering key points
**Page:** ~500 words with structured sections (Key Points, Details, Implications)

Based on audience:
**Technical:** Include technical details, system names, architecture implications
**Exec:** Focus on business impact, costs, timelines, decisions needed
**General:** Balanced overview accessible to non-specialists

### Phase 3: Output

Present the summary and offer to:
- Add it as the `summary` field in the note's frontmatter
- Save as a standalone summary note
- Copy to clipboard

## Output Format

### One-liner
```
<Single sentence summary>
```

### Paragraph
```markdown
## Summary

<3-5 sentence summary covering key points, context, and implications>
```

### Page
```markdown
## Summary: <Title>

### Key Points
- <Point 1>
- <Point 2>
- <Point 3>

### Overview
<2-3 paragraphs of detail>

### Implications
<What this means for the reader>
```

## Examples

### Example 1: Quick Note Summary

```
/summarize "ADR - Event Sourcing.md" --depth one-liner
```

Output: "Decision to adopt event sourcing for the order audit trail, enabling full replay and temporal queries."

### Example 2: Multi-Note Summary

```
/summarize "Projects/*.md" --depth page --audience exec
```

Summarises all project notes into a single executive-level page overview.

### Example 3: Technical Summary

```
/summarize "Concept - CQRS.md" --depth paragraph --audience technical
```

Generates a technical paragraph summary of the CQRS concept note.

---

**Invoke with:** `/summarize <source>` to generate summaries at any depth for any audience
