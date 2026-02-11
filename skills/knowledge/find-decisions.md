---
description: Extract and catalogue decisions from meetings, emails, and daily notes across a date range
model: sonnet
---

# /find-decisions

Search across meeting notes, emails, daily notes, and ADRs to find and catalogue all decisions made within a specified period. Identifies both formal (ADR) and informal (meeting/email) decisions.

## When to Use This Skill

- Creating a decision log for governance or audit purposes
- Finding decisions related to a specific project or topic
- Identifying decisions that were made but never formalised as ADRs
- Preparing for architecture reviews by gathering recent decisions
- Checking for conflicting decisions across different meetings

## Usage

```
/find-decisions [--period last-week|last-month|YYYY-MM-DD:YYYY-MM-DD] [--project "Project Name"] [--format table|detailed]
```

### Parameters

| Parameter   | Description                                          | Required |
|-------------|------------------------------------------------------|----------|
| `--period`  | Date range to search (default: `last-month`)         | No       |
| `--project` | Filter by project name                               | No       |
| `--format`  | Output format (default: `table`)                     | No       |

## Instructions

### Phase 1: Identify Sources

1. **Determine date range** from `--period` parameter
2. **Find relevant files:**
   - ADRs created or modified in the period
   - Meeting notes dated within the period
   - Email notes dated within the period
   - Daily notes within the period
3. **If `--project` specified:** Filter to files mentioning or linked to the project

### Phase 2: Extract Decisions

Scan each file for decision language:

**Decision indicators:**
- "Decided to...", "We agreed...", "Approved..."
- "Will go with...", "Selected...", "Chosen approach..."
- "Decision:", "Agreed:", "Resolution:"
- ADR status fields (accepted, proposed)
- Meeting decision sections

**For each decision found:**
- **What** was decided
- **Who** made the decision (attendees, deciders)
- **When** it was made (date)
- **Where** it was documented (source file)
- **Why** (rationale, if available)
- **Type:** Formal (ADR) / Informal (meeting) / Implied (email/daily)
- **Status:** Active / Superseded / Under review

### Phase 3: Compile Decision Log

1. **Deduplicate** — Same decision referenced in multiple files
2. **Sort by date** (most recent first)
3. **Flag** decisions that should be formalised as ADRs
4. **Flag** potential conflicts between decisions
5. **Generate output** in requested format

## Output Format

### Table Format

```markdown
# Decision Log: <Period>

**Period:** <date range> | **Decisions found:** X | **Sources scanned:** X

## Decisions

| # | Date       | Decision                         | Source              | Type    | Status |
|---|------------|----------------------------------|---------------------|---------|--------|
| 1 | YYYY-MM-DD | <What was decided>               | [[Meeting - ...]]   | Formal  | Active |
| 2 | YYYY-MM-DD | <What was decided>               | [[Meeting - ...]]   | Informal| Active |

## Needs Formalisation

These informal decisions should be documented as ADRs:

| Decision                    | Source        | Reason                        |
|-----------------------------|---------------|-------------------------------|
| <Decision>                  | <Meeting>     | Affects multiple systems      |

## Potential Conflicts

| Decision A                  | Decision B                | Conflict                    |
|-----------------------------|---------------------------|-----------------------------|
| <Decision>                  | <Decision>                | <What conflicts>            |
```

### Detailed Format

```markdown
# Decision Log: <Period>

## Decision 1: <Title>

- **Date:** YYYY-MM-DD
- **Source:** [[Meeting - YYYY-MM-DD Title]]
- **Deciders:** [[Person 1]], [[Person 2]]
- **Type:** Formal / Informal
- **Status:** Active

**Context:** <Why this decision was needed>
**Decision:** <What was decided>
**Rationale:** <Why this option was chosen>
**Impact:** <What systems, teams, or processes are affected>
```

## Examples

### Example 1: Last Month's Decisions

```
/find-decisions --period last-month
```

### Example 2: Project-Specific Decisions

```
/find-decisions --project "Platform Migration" --format detailed
```

### Example 3: Custom Date Range

```
/find-decisions --period 2026-01-01:2026-01-31 --format table
```

---

**Invoke with:** `/find-decisions` to extract and catalogue decisions from vault content
