---
description: Score documents against customisable rubrics using four parallel agents for section-by-section analysis
model: sonnet
---

# /score-document

Score a document against a customisable rubric using four parallel agents. Each agent evaluates a different section or dimension of the document, producing consistent, evidence-based scores. Ideal for RFI/RFP responses, proposal evaluations, and vendor assessments.

## When to Use This Skill

- Evaluating RFI or RFP responses from vendors
- Scoring proposals against defined criteria
- Assessing technical documentation quality
- Comparing multiple submissions consistently
- Creating audit trails for procurement decisions

## Usage

```
/score-document <path-to-document> [--rubric path/to/rubric.md] [--scale 0-3|0-5|0-10]
```

### Parameters

| Parameter   | Description                                          | Required |
|-------------|------------------------------------------------------|----------|
| `path`      | Path to the document to score                        | Yes      |
| `--rubric`  | Path to custom rubric (default: built-in)            | No       |
| `--scale`   | Scoring scale (default: `0-3`)                       | No       |

## Instructions

### Phase 1: Prepare Scoring Framework

1. **Load the document** to be scored
2. **Load or generate rubric:**
   - If `--rubric` provided, parse the rubric file
   - Otherwise, generate a rubric from the document structure:
     - Identify sections/questions in the document
     - Create evaluation criteria per section
3. **Define scoring scale:**

   **0-3 Scale (Default):**

   | Score | Rating | Criteria                                          |
   |-------|--------|---------------------------------------------------|
   | 3     | High   | Strong evidence, detailed, domain-specific response|
   | 2     | Medium | Some capability, potential but limited evidence    |
   | 1     | Low    | Insufficient evidence, generic response            |
   | 0     | Zero   | Not demonstrated, no evidence provided             |

   **0-5 Scale:**

   | Score | Rating      | Criteria                                   |
   |-------|-------------|--------------------------------------------|
   | 5     | Exceptional | Exceeds requirements, innovative approach  |
   | 4     | Strong      | Fully meets requirements with evidence     |
   | 3     | Adequate    | Meets minimum requirements                 |
   | 2     | Partial     | Some gaps, limited evidence                |
   | 1     | Weak        | Significant gaps                           |
   | 0     | None        | Not addressed                              |

4. **Divide document** into sections for parallel evaluation

### Phase 2: Parallel Scoring — Agent Team

Launch four agents simultaneously using the Task tool. Each scores a different section group.

**Agent 1-4: Section Scorer** (Sonnet)
Task: Score assigned document sections against the rubric
- For each section:
  1. Read the section content carefully
  2. Compare against rubric criteria
  3. Assign a score on the defined scale
  4. Record evidence: specific quotes or observations supporting the score
  5. Note strengths and weaknesses
  6. Flag any red flags or concerns
- Maintain consistency:
  - Score 0 requires explicit evidence of absence
  - Score at maximum requires explicit evidence of excellence
  - Default to middle of scale when evidence is ambiguous
Return: List of `{ section, score, maxScore, evidence, strengths[], weaknesses[], redFlags[] }`

### Phase 3: Synthesise Scorecard

Combine all agent results:

1. **Calculate section scores** and overall weighted score
2. **Normalise to percentage** — Total points / Maximum possible points
3. **Generate executive summary** — Overall assessment in 2-3 sentences
4. **Create comparison-ready output** — If scoring multiple documents, ensure consistent format
5. **Highlight** top strengths, key weaknesses, and red flags

## Output Format

```markdown
# Document Scorecard: <Document Title>

**Date:** YYYY-MM-DD | **Scale:** 0-X | **Scorer:** AI-assisted

## Overall Score: X/Y (X%)

**Assessment:** <2-3 sentence overall evaluation>

### Score Summary

| Category                | Score | Max | %    | Rating  |
|-------------------------|-------|-----|------|---------|
| <Section 1>             | X     | X   | X%   | High    |
| <Section 2>             | X     | X   | X%   | Medium  |
| <Section 3>             | X     | X   | X%   | Low     |
| <Section 4>             | X     | X   | X%   | High    |
| **Total**               | **X** | **X**| **X%** |       |

## Detailed Scoring

### <Section 1> — Score: X/X (Rating)

**Evidence:** <Specific quotes or observations>

**Strengths:**
- <Strength 1>

**Weaknesses:**
- <Weakness 1>

### <Section 2> — Score: X/X (Rating)
...

## Red Flags

| Flag                        | Section   | Severity |
|-----------------------------|-----------|----------|
| <Concern>                   | <Section> | High     |

## Top Strengths

1. <Strongest area with evidence>
2. <Second strongest>

## Key Weaknesses

1. <Biggest gap with recommendation>
2. <Second biggest>

## Recommendation

**Verdict:** Accept / Accept with conditions / Reject
**Key conditions:** <If applicable>
```

## Examples

### Example 1: Score an RFI Response

```
/score-document ~/Documents/vendor-rfi-response.pdf --scale 0-3
```

Scores each section of the vendor's RFI response on a 0-3 scale with evidence.

### Example 2: Custom Rubric

```
/score-document ~/Documents/proposal.md --rubric ~/Documents/scoring-rubric.md --scale 0-5
```

Scores a proposal against a custom rubric on a 0-5 scale.

### Example 3: Technical Assessment

```
/score-document ~/Documents/architecture-review.md --scale 0-10
```

Scores an architecture review document on a 0-10 scale.

---

**Invoke with:** `/score-document <path>` to score a document against a rubric with evidence-based ratings
