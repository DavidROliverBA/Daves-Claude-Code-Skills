---
description: Generate executive summaries from long documents distilling key messages for senior stakeholders
model: sonnet
---

# /exec-summary

Generate concise executive summaries from long documents, distilling key messages, decisions, and action items for senior stakeholders. Single-pass synthesis optimised for clarity and brevity.

## When to Use This Skill

- Summarising long reports for senior leadership
- Creating one-page briefs from multi-page documents
- Distilling meeting minutes into decision summaries
- Preparing board-level summaries from technical documents
- Converting detailed analyses into stakeholder communications

## Usage

```
/exec-summary <path-to-document> [--length short|standard|detailed] [--audience ceo|cto|board|pm]
```

### Parameters

| Parameter    | Description                                          | Required |
|--------------|------------------------------------------------------|----------|
| `path`       | Path to the document to summarise                    | Yes      |
| `--length`   | Summary length: short (~200 words), standard (~500), detailed (~1000) | No |
| `--audience` | Target audience for tone and focus (default: `cto`)  | No       |

## Instructions

### Phase 1: Analyse Document

1. **Read the full document**
2. **Identify document type** — Report, proposal, analysis, minutes, specification
3. **Extract key elements:**
   - Main conclusions or recommendations
   - Critical decisions made or needed
   - Financial implications (costs, savings, ROI)
   - Risks and mitigations
   - Action items and owners
   - Timeline and milestones

### Phase 2: Synthesise Summary

Tailor the summary to the audience:

**CEO/Board audience:**
- Focus on business impact, financial implications, and strategic alignment
- Minimise technical detail
- Lead with the recommendation or decision needed

**CTO audience:**
- Include technical context and architecture implications
- Highlight risks and dependencies
- Include timeline and resource requirements

**PM audience:**
- Focus on scope, timeline, and resource implications
- Highlight dependencies and blockers
- Include action items and next steps

### Phase 3: Generate Output

Write the executive summary using the inverted pyramid structure:
1. **Bottom line up front (BLUF)** — The most important conclusion in one sentence
2. **Key findings** — 3-5 bullet points with the essential information
3. **Supporting detail** — Brief context for each key finding
4. **Actions required** — What decisions or actions are needed

## Output Format

```markdown
# Executive Summary: <Document Title>

> **Source:** <document> | **Date:** YYYY-MM-DD | **Prepared for:** <audience>

## Bottom Line

<One sentence capturing the most important conclusion or recommendation>

## Key Findings

1. **<Finding 1>** — <One-sentence supporting detail>
2. **<Finding 2>** — <One-sentence supporting detail>
3. **<Finding 3>** — <One-sentence supporting detail>

## Financial Impact

| Item                | Value          |
|---------------------|----------------|
| Investment required | £X             |
| Expected savings    | £X/year        |
| ROI                 | X% over Y years|
| Break-even          | Month X        |

## Risks

| Risk                    | Likelihood | Impact | Mitigation          |
|-------------------------|------------|--------|---------------------|
| <Risk>                  | Medium     | High   | <Mitigation>        |

## Actions Required

| Action                          | Owner      | Deadline    |
|---------------------------------|------------|-------------|
| <Decision or action needed>     | <Name>     | YYYY-MM-DD  |

## Next Steps

1. <Immediate next step>
2. <Follow-up action>
```

## Examples

### Example 1: Board Summary

```
/exec-summary ~/Documents/migration-analysis.md --length short --audience board
```

200-word summary focusing on business impact and investment decision.

### Example 2: CTO Brief

```
/exec-summary ~/Documents/architecture-review.md --audience cto
```

Standard-length summary with technical context and architecture implications.

### Example 3: Detailed PM Brief

```
/exec-summary ~/Documents/project-proposal.md --length detailed --audience pm
```

1000-word summary with full scope, timeline, and resource breakdown.

---

**Invoke with:** `/exec-summary <path>` to generate a stakeholder-ready executive summary
