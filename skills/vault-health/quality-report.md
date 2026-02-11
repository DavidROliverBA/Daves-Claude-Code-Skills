---
description: Generate comprehensive content quality metrics for a Markdown vault using five parallel analysis agents
model: sonnet
---

# /quality-report

Generate comprehensive content quality metrics for a Markdown vault. Uses five parallel agents to analyse readability, link density, metadata completeness, structure, and freshness simultaneously, then produces a scored quality report with actionable improvements.

## When to Use This Skill

- Quarterly vault health reviews
- Identifying low-quality notes that need improvement
- Measuring knowledge base quality over time
- Finding notes with missing metadata or broken structure
- Prioritising vault maintenance work

## Usage

```
/quality-report [--scope path/to/folder] [--type Meeting|ADR|Concept|all] [--top-issues 20]
```

### Parameters

| Parameter      | Description                                          | Required |
|----------------|------------------------------------------------------|----------|
| `--scope`      | Folder or path to analyse (default: entire vault)    | No       |
| `--type`       | Filter by note type (default: `all`)                 | No       |
| `--top-issues` | Number of top issues to list (default: `20`)         | No       |

## Instructions

### Phase 1: Inventory

1. **Scan the vault** — List all Markdown files in scope
2. **Parse frontmatter** — Extract type, tags, dates, and metadata from each note
3. **Build file list** — Divide notes into batches for parallel processing
4. **Report to user:** "Found X notes in scope. Launching quality analysis..."

### Phase 2: Parallel Quality Analysis — Agent Team

Launch five agents simultaneously using the Task tool. Each agent analyses all notes in scope across one quality dimension.

**Agent 1: Readability Analyst** (Sonnet)
Task: Score readability of note content
- Extract body text (exclude frontmatter, code blocks, YAML)
- Calculate approximate Flesch Reading Ease score
- Calculate Flesch-Kincaid Grade Level
- Identify notes with very long paragraphs (>300 words without a break)
- Flag notes with no prose content (just bullet lists or tables)
- Normalise to 0-100 score (higher = more readable)
Return: Map of `filename → { readabilityScore, gradeLevel, issues[] }`

**Agent 2: Link Density Analyst** (Sonnet)
Task: Score interconnectedness of notes
- Count outgoing wiki-links per note
- Build backlink index (which notes link to each note)
- Count backlinks per note
- Identify orphan notes (0 backlinks and 0 outgoing links)
- Identify hub notes (>10 backlinks)
- Score: outgoing links (40pts) + backlinks (30pts) + link quality (30pts)
- Normalise to 0-100 score
Return: Map of `filename → { linkScore, outgoing, backlinks, isOrphan, isHub }`

**Agent 3: Metadata Completeness Analyst** (Sonnet)
Task: Score frontmatter completeness
- Check required fields: `type`, `title`, `created`, `tags`
- Check recommended fields by type (e.g., ADR needs `status`, Meeting needs `attendees`)
- Check for `summary` field (critical for AI triage)
- Check tag quality: hierarchical format, minimum count
- Check `relatedTo` array presence and population
- Normalise to 0-100 score
Return: Map of `filename → { metadataScore, missingRequired[], missingRecommended[] }`

**Agent 4: Structure Completeness Analyst** (Sonnet)
Task: Score document structure against expected sections by type
- Define expected sections per note type:
  - ADR: Context, Decision, Rationale, Consequences, Alternatives
  - Meeting: Attendees, Agenda, Discussion, Decisions, Actions
  - Concept: Definition, Context, Examples, Related
  - Project: Objectives, Scope, Timeline, Status
- Check for heading hierarchy (H1, H2, H3 nesting)
- Flag empty sections
- Normalise to 0-100 score
Return: Map of `filename → { structureScore, missingSections[], emptySections[] }`

**Agent 5: Freshness and Tag Analyst** (Sonnet)
Task: Score content freshness and tag quality
- Calculate days since last modification
- Categorise: current (<90 days), recent (90-365 days), stale (>365 days)
- Check tag count per note (minimum 2 expected)
- Verify tags use hierarchical format (e.g., `domain/topic`)
- Flag notes with flat tags or too few tags
- Score: freshness (60pts) + tag quality (40pts)
- Normalise to 0-100 score
Return: Map of `filename → { freshnessScore, daysSinceUpdate, freshness, tagCount, tagIssues[] }`

### Phase 3: Synthesise Quality Report

Combine all agent results:

1. **Calculate overall score per note:**
   ```
   overallScore = readability × 0.20 + linkDensity × 0.25 + metadata × 0.20 + structure × 0.20 + freshness × 0.15
   ```

2. **Assign grades:**
   - A: 90-100 (Excellent)
   - B: 80-89 (Good)
   - C: 70-79 (Acceptable)
   - D: 60-69 (Needs Improvement)
   - F: <60 (Poor)

3. **Generate report** with vault-wide statistics, distribution, and top issues

## Output Format

```markdown
# Vault Quality Report

**Date:** YYYY-MM-DD | **Scope:** <scope> | **Notes Analysed:** X

## Overall Score: X/100 (Grade: X)

| Dimension      | Score | Weight | Weighted |
|----------------|-------|--------|----------|
| Readability    | X/100 | 20%    | X        |
| Link Density   | X/100 | 25%    | X        |
| Metadata       | X/100 | 20%    | X        |
| Structure      | X/100 | 20%    | X        |
| Freshness      | X/100 | 15%    | X        |
| **Overall**    |       | 100%   | **X**    |

## Grade Distribution

| Grade | Count | Percentage |
|-------|-------|------------|
| A     | X     | X%         |
| B     | X     | X%         |
| C     | X     | X%         |
| D     | X     | X%         |
| F     | X     | X%         |

## Quality by Note Type

| Type     | Count | Avg Score | Lowest Score | Top Issue              |
|----------|-------|-----------|--------------|------------------------|
| ADR      | X     | X         | X            | <Most common issue>    |
| Meeting  | X     | X         | X            | <Most common issue>    |
| Concept  | X     | X         | X            | <Most common issue>    |

## Top X Issues (Prioritised)

| # | Note                  | Score | Grade | Primary Issue                | Fix                        |
|---|----------------------|-------|-------|------------------------------|----------------------------|
| 1 | <filename>           | X     | F     | Missing metadata + orphaned  | Add frontmatter, add links |
| 2 | <filename>           | X     | D     | Stale content, no summary    | Review and add summary     |

## Detailed Findings

### Orphaned Notes (X found)
<List of notes with 0 links in or out>

### Stale Notes (X found)
<Notes not updated in >12 months>

### Missing Summaries (X found)
<Notes without `summary` field>

## Recommendations

1. **Quick wins:** Add `summary` to X notes (improves metadata score by X points)
2. **Link building:** Connect X orphaned notes to related content
3. **Freshness:** Review X stale notes for accuracy
```

## Examples

### Example 1: Full Vault Report

```
/quality-report
```

### Example 2: ADR Quality Check

```
/quality-report --type ADR --top-issues 10
```

### Example 3: Folder-Specific Report

```
/quality-report --scope Projects/
```

---

**Invoke with:** `/quality-report` to generate a comprehensive vault quality assessment
