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
- Count total words, sentences, and syllables in the body text
- Calculate Flesch Reading Ease using the formula:
  ```
  Flesch Reading Ease = 206.835 - 1.015 × (words / sentences) - 84.6 × (syllables / words)
  ```
- Calculate Flesch-Kincaid Grade Level:
  ```
  Flesch-Kincaid Grade = 0.39 × (words / sentences) + 11.8 × (syllables / words) - 15.59
  ```
- Calculate additional metrics:
  - Average sentence length (words per sentence)
  - Average word length (characters per word)
  - Complex word ratio (proportion of words with >3 syllables)
- Identify notes with very long paragraphs (>300 words without a break)
- Flag notes with no prose content (just bullet lists or tables)
- Score: Clamp Flesch Reading Ease to 0-100, then use directly as the readability score
Return: Map of `filename → { readabilityScore, fleschEase, gradeLevel, avgSentenceLength, complexWordRatio, issues[] }`

**Agent 2: Link Density Analyst** (Sonnet)
Task: Score interconnectedness of notes
- Count outgoing wiki-links per note (`[[...]]` references)
- Build backlink index (which notes link to each note)
- Count backlinks per note
- Calculate link density (links per 100 words)
- Identify orphaned notes (0 backlinks)
- Identify hub notes (top 10% by backlink count)
- Check for broken links (links to non-existent notes)
- Score each note using the link density formula:
  ```
  Base points:     min(outgoing_links / 5, 1) × 40   (cap at 5 outgoing links)
  Backlink points: min(backlinks / 3, 1) × 30         (cap at 3 backlinks)
  Orphan penalty:  -20 if 0 backlinks
  Broken penalty:  -10 if note contains broken links
  Hub bonus:       +10 if note is a hub (top 10% by backlinks)
  ```
  Final score = clamp(Base + Backlinks + Penalties + Bonus, 0, 100)
Return: Map of `filename → { linkScore, outgoing, backlinks, linkDensity, isOrphan, isHub, brokenLinks[] }`

**Agent 3: Metadata Completeness Analyst** (Sonnet)
Task: Score frontmatter completeness based on note type
- Parse frontmatter from each note
- Evaluate required and recommended fields per type:

  | Type            | Required Fields                                         | Recommended Fields                        |
  |-----------------|---------------------------------------------------------|-------------------------------------------|
  | Universal (all) | `type`, `title`, `created`                              | `tags`, `summary`, `modified`             |
  | Task            | + `status`, `priority`                                  | + `completed`, `due`                      |
  | Project         | + `status`                                              | + `priority`, `category`                  |
  | ADR             | + `status`, `relatedTo`                                 | + `supersedes`, `dependsOn`, `confidence`, `freshness`, `source` |
  | Meeting         | + `date`                                                | + `attendees`, `project`                  |
  | Person          | + `role`                                                | + `organisation`, `email`                 |
  | Concept/Pattern | (universal only)                                        | + `description`, `tags`                   |

- Score calculation:
  ```
  Required fields:    1 point each (based on type-specific count)
  Recommended fields: 0.5 points each
  Quality indicators (ADRs only): confidence, freshness, source = 2 points each
  Normalise total to 0-100 scale based on maximum possible for the note's type
  ```
Return: Map of `filename → { metadataScore, missingRequired[], missingRecommended[] }`

**Agent 4: Structure Completeness Analyst** (Sonnet)
Task: Score document structure against expected sections by type
- Define expected sections per note type:

  **ADR sections** (required — 20 points each, 5 sections = 100):
  - Context (H1 or H2)
  - Decision (H1 or H2)
  - Rationale (H1 or H2)
  - Consequences (H1 or H2)
  - Alternatives Considered (recommended)

  **Meeting sections** (recommended — 25 points each, 4 sections = 100):
  - Attendees (heading or frontmatter)
  - Agenda
  - Discussion / Notes
  - Action Items / Actions / Next Steps

  **Project sections** (recommended — 33 points each, 3 sections = ~100):
  - Overview / Summary
  - Status / Progress
  - Timeline / Milestones

  **Concept/Pattern sections** (recommended — 25 points each):
  - Definition / Overview
  - Context
  - Examples
  - Related

  **Other types:** 100 points (no structure requirement)

- Check heading hierarchy (H1, H2, H3 nesting)
- Flag empty sections (heading present but no content beneath)
Return: Map of `filename → { structureScore, missingSections[], emptySections[] }`

**Agent 5: Freshness and Tag Analyst** (Sonnet)
Task: Score content freshness and tag quality
- Calculate days since last modification (from `modified` frontmatter field, falling back to file modification date)
- Categorise freshness using type-aware thresholds:

  | Note Type         | Fresh           | Recent          | Stale           |
  |-------------------|-----------------|-----------------|-----------------|
  | Task              | <7 days         | 7-30 days       | >30 days        |
  | Project           | <30 days        | 30-90 days      | >90 days        |
  | ADR               | <180 days       | 180-365 days    | >365 days       |
  | Concept / Pattern | <90 days        | 90-365 days     | >365 days       |
  | Meeting           | Always scored by completeness, not age                  |
  | Daily             | Always fresh (by definition)                            |

- Freshness scoring (60 points):
  ```
  Fresh:  60 points
  Recent: 30 points
  Stale:  0 points
  ```
  For types where age is irrelevant (Meeting, Daily): award full 60 points.

- Tag scoring (40 points):
  ```
  Has tags:             +20 points
  Optimal count (2-5):  +20 points
  Count of 1:           +10 points
  Count of 0:           +0 points
  Count >5 (excessive): +10 points
  Hierarchical format:  no additional points but flag flat tags as issues
  ```
- Final score = freshness points + tag points (0-100)
Return: Map of `filename → { freshnessScore, daysSinceUpdate, freshnessCategory, tagCount, tagIssues[] }`

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

## Scoring Algorithms

This section documents every formula used by the quality agents. Use these as the authoritative reference when implementing scoring.

### Readability Score (Agent 1)

```
Flesch Reading Ease = 206.835 - 1.015 × (total_words / total_sentences) - 84.6 × (total_syllables / total_words)
Flesch-Kincaid Grade = 0.39 × (total_words / total_sentences) + 11.8 × (total_syllables / total_words) - 15.59

Readability Score = clamp(Flesch Reading Ease, 0, 100)
```

**Interpretation:**
| Flesch Reading Ease | Interpretation           |
|---------------------|--------------------------|
| 90-100              | Very easy to read        |
| 80-89               | Easy to read             |
| 70-79               | Fairly easy              |
| 60-69               | Standard / plain English |
| 50-59               | Fairly difficult         |
| 30-49               | Difficult                |
| 0-29                | Very difficult           |

**Syllable estimation heuristic:** Count vowel groups (a, e, i, o, u, y) in each word. Subtract 1 for silent-e endings. Minimum 1 syllable per word.

### Link Density Score (Agent 2)

```
base_points     = min(outgoing_links / 5, 1) × 40
backlink_points = min(backlinks / 3, 1) × 30
orphan_penalty  = -20 if backlinks == 0
broken_penalty  = -10 if broken_link_count > 0
hub_bonus       = +10 if note is in the top 10% by backlink count

Link Density Score = clamp(base_points + backlink_points + orphan_penalty + broken_penalty + hub_bonus, 0, 100)
```

**Examples:**
| Outgoing | Backlinks | Orphan | Broken | Hub | Score |
|----------|-----------|--------|--------|-----|-------|
| 5+       | 3+        | No     | No     | No  | 70    |
| 5+       | 3+        | No     | No     | Yes | 80    |
| 2        | 1         | No     | No     | No  | 26    |
| 0        | 0         | Yes    | No     | No  | 0     |
| 3        | 0         | Yes    | Yes    | No  | 0     |

### Metadata Completeness Score (Agent 3)

```
required_score    = (present_required_fields / total_required_fields)
recommended_score = (present_recommended_fields / total_recommended_fields) × 0.5
quality_bonus     = (present_quality_indicators / total_quality_indicators) × bonus_weight

Metadata Score = normalise_to_100(required_score + recommended_score + quality_bonus)
```

**Required fields by type:**

| Type            | Required Fields                    | Count |
|-----------------|------------------------------------|-------|
| Universal       | `type`, `title`, `created`         | 3     |
| Task            | Universal + `status`, `priority`   | 5     |
| Project         | Universal + `status`               | 4     |
| ADR             | Universal + `status`, `relatedTo`  | 5     |
| Meeting         | Universal + `date`                 | 4     |
| Person          | Universal + `role`                 | 4     |
| Concept/Pattern | Universal only                     | 3     |

**Quality indicators (ADRs only):** `confidence`, `freshness`, `source` — 2 points each.

### Structure Completeness Score (Agent 4)

```
ADR:     points_per_section = 20  (5 expected sections)
Meeting: points_per_section = 25  (4 expected sections)
Project: points_per_section = 33  (3 expected sections)
Concept: points_per_section = 25  (4 expected sections)
Other:   score = 100              (no structure requirement)

Structure Score = present_sections × points_per_section
```

### Freshness Score (Agent 5)

```
freshness_points = 60 if fresh, 30 if recent, 0 if stale
tag_points       = (has_tags ? 20 : 0) + (optimal_count ? 20 : count_1 ? 10 : excessive ? 10 : 0)

Freshness Score = freshness_points + tag_points
```

**Type-aware freshness thresholds:**

| Note Type         | Fresh (60pts) | Recent (30pts) | Stale (0pts) |
|-------------------|---------------|----------------|--------------|
| Task              | <7 days       | 7-30 days      | >30 days     |
| Project           | <30 days      | 30-90 days     | >90 days     |
| ADR               | <180 days     | 180-365 days   | >365 days    |
| Concept / Pattern | <90 days      | 90-365 days    | >365 days    |
| Meeting           | N/A — full freshness points awarded (scored by completeness) |
| Daily             | N/A — always fresh by definition                             |

### Overall Quality Score

```
overallScore = readability × 0.20 + linkDensity × 0.25 + metadata × 0.20 + structure × 0.20 + freshness × 0.15
```

| Grade | Range  | Interpretation      |
|-------|--------|---------------------|
| A     | 90-100 | Excellent           |
| B     | 80-89  | Good                |
| C     | 70-79  | Acceptable          |
| D     | 60-69  | Needs Improvement   |
| F     | <60    | Poor                |

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
<List of notes with 0 backlinks>

### Stale Notes (X found)
<Notes exceeding their type-specific freshness threshold>

### Missing Summaries (X found)
<Notes without `summary` field>

### Readability Concerns (X found)
<Notes with Flesch Reading Ease below 50>

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

## Performance

- **5 parallel agents** = approximately 5x faster than sequential analysis
- **~500 notes**: 45-90 seconds
- **~2000 notes**: 2-4 minutes
- **~5000 notes**: 5-8 minutes

## Notes

- Readability scoring may not apply well to code-heavy notes or technical specifications — consider excluding or adjusting weight for these
- Freshness scoring is type-aware: ADRs can be old and still valid, tasks go stale quickly
- Structure requirements are recommendations, not strict rules
- Link density considers both quality (backlinks from other notes) and quantity (outgoing links)
- Templates and system notes are excluded from scoring
- Can be run on subsets with `--type` or `--scope` filters

---

**Invoke with:** `/quality-report` to generate a comprehensive vault quality assessment
