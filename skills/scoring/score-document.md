---
description: Score documents against customisable rubrics using four parallel agents, with optional SQLite persistence for querying and comparison
model: sonnet
---

# /score-document

Score a document against a customisable rubric using four parallel agents. Each agent evaluates a different section or dimension of the document, producing consistent, evidence-based scores. Optionally persist scores to a SQLite database for querying, filtering, and multi-scorer comparison.

## When to Use This Skill

- Evaluating RFI or RFP responses from vendors
- Scoring proposals against defined criteria
- Assessing technical documentation quality
- Comparing multiple submissions consistently
- Creating audit trails for procurement decisions
- Building persistent scoring databases for trend analysis

## Usage

```
/score-document <path-to-document> [--rubric path/to/rubric.md] [--scale 0-3|0-5|0-10] [--persist] [--db path/to/scores.db] [--scorer name] [--compare]
```

### Parameters

| Parameter   | Description                                          | Required |
|-------------|------------------------------------------------------|----------|
| `path`      | Path to the document to score                        | Yes      |
| `--rubric`  | Path to custom rubric (default: built-in)            | No       |
| `--scale`   | Scoring scale (default: `0-3`)                       | No       |
| `--persist` | Save scores to SQLite database for later analysis    | No       |
| `--db`      | SQLite database path (default: `.data/<doc-name>-scoring.db`) | No |
| `--scorer`  | Scorer identity column name (default: `ai_scorer`)   | No       |
| `--compare` | Compare scores across multiple scorers or runs       | No       |

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

### Phase 4: Persist Results (Optional — `--persist` flag)

When `--persist` is provided, save scores to a SQLite database for later querying, filtering, and comparison.

#### 4a. Create Database Schema

```bash
sqlite3 .data/<document-name>-scoring.db <<'SQL'
CREATE TABLE IF NOT EXISTS questions (
  id TEXT PRIMARY KEY,
  section TEXT,
  question TEXT,
  content TEXT
);

CREATE TABLE IF NOT EXISTS scores (
  id TEXT PRIMARY KEY,
  section TEXT,
  question TEXT,
  ai_scorer TEXT
);
SQL
```

If a custom `--scorer` name is provided (e.g., `--scorer jane_smith`), add the column dynamically:

```bash
sqlite3 .data/<document-name>-scoring.db \
  "ALTER TABLE scores ADD COLUMN jane_smith TEXT;"
```

#### 4b. Create FTS Index for Searching

```bash
sqlite3 .data/<document-name>-scoring.db <<'SQL'
CREATE VIRTUAL TABLE IF NOT EXISTS questions_fts
  USING fts5(id, section, question, content);

INSERT INTO questions_fts (id, section, question, content)
  SELECT id, section, question, content FROM questions;
SQL
```

#### 4c. Insert or Update Scores

All scores MUST be written in the evidence format:

```
<score> - <reason>
```

Examples:
- `3 - Comprehensive response with specific implementation examples and measurable outcomes`
- `2 - Reasonable approach but no concrete examples of prior delivery at scale`
- `1 - Generic response lacking domain-specific detail; significant capability gap`
- `0 - No response provided`

Insert scores using UPDATE statements:

```bash
sqlite3 .data/<document-name>-scoring.db \
  "UPDATE scores SET ai_scorer = '3 - Comprehensive coverage with concrete examples' WHERE id = '1';"

sqlite3 .data/<document-name>-scoring.db \
  "UPDATE scores SET ai_scorer = '1 - Generic response; no domain-specific evidence' WHERE id = '2';"
```

#### 4d. Verify Persisted Scores

```bash
sqlite3 .data/<document-name>-scoring.db -markdown -header \
  "SELECT id, section, ai_scorer FROM scores ORDER BY CAST(id AS INTEGER);"
```

#### 4e. Generate Summary Queries

**Score distribution:**

```bash
sqlite3 .data/<document-name>-scoring.db \
  "SELECT CAST(SUBSTR(ai_scorer, 1, 1) AS INTEGER) as score, COUNT(*) as count
   FROM scores GROUP BY score ORDER BY score DESC;"
```

**Low scores (risks):**

```bash
sqlite3 .data/<document-name>-scoring.db -markdown -header \
  "SELECT id, SUBSTR(question, 1, 60) as question, ai_scorer
   FROM scores
   WHERE ai_scorer LIKE '1 -%' OR ai_scorer LIKE '0 -%'
   ORDER BY CAST(id AS INTEGER);"
```

**Average score:**

```bash
sqlite3 .data/<document-name>-scoring.db \
  "SELECT ROUND(AVG(CAST(SUBSTR(ai_scorer, 1, 1) AS REAL)), 2) as avg_score FROM scores;"
```

**Per-section averages:**

```bash
sqlite3 .data/<document-name>-scoring.db -markdown -header \
  "SELECT section,
          COUNT(*) as questions,
          ROUND(AVG(CAST(SUBSTR(ai_scorer, 1, 1) AS REAL)), 2) as avg_score
   FROM scores
   GROUP BY section
   ORDER BY avg_score ASC;"
```

### Phase 5: Compare Scores (Optional — `--compare` flag)

When `--compare` is provided and the database has multiple scorer columns, generate a comparison.

**Compare all scorers side by side:**

```bash
sqlite3 .data/<document-name>-scoring.db -markdown -header \
  "SELECT id, ai_scorer, jane_smith, review_panel
   FROM scores ORDER BY CAST(id AS INTEGER);"
```

**Compare average scores per scorer:**

```bash
sqlite3 .data/<document-name>-scoring.db -markdown -header \
  "SELECT
     'ai_scorer' as scorer,
     ROUND(AVG(CAST(SUBSTR(ai_scorer, 1, 1) AS REAL)), 2) as avg
   FROM scores
   UNION ALL
   SELECT
     'jane_smith' as scorer,
     ROUND(AVG(CAST(SUBSTR(jane_smith, 1, 1) AS REAL)), 2) as avg
   FROM scores;"
```

**Identify scoring disagreements (difference >= 2):**

```bash
sqlite3 .data/<document-name>-scoring.db -markdown -header \
  "SELECT id, question,
     CAST(SUBSTR(ai_scorer, 1, 1) AS INTEGER) as score_a,
     CAST(SUBSTR(jane_smith, 1, 1) AS INTEGER) as score_b,
     ABS(CAST(SUBSTR(ai_scorer, 1, 1) AS INTEGER) - CAST(SUBSTR(jane_smith, 1, 1) AS INTEGER)) as diff
   FROM scores
   WHERE diff >= 2
   ORDER BY diff DESC;"
```

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

When `--persist` is used, append:

```markdown
## Data Source

Scores stored in SQLite database: `.data/<document-name>-scoring.db`
Table: `scores` | Scorer column: `ai_scorer`
```

## Querying Scores

Once scores are persisted to SQLite, use these queries for ongoing analysis.

### Basic Queries

```bash
# All scores with full questions
sqlite3 .data/<db>.db -markdown -header \
  "SELECT id, question, ai_scorer FROM scores ORDER BY CAST(id AS INTEGER);"

# Search questions by keyword (uses FTS index)
sqlite3 .data/<db>.db -markdown -header \
  "SELECT id, question FROM questions_fts WHERE questions_fts MATCH 'security';"

# Filter by section
sqlite3 .data/<db>.db -markdown -header \
  "SELECT id, question, ai_scorer FROM scores WHERE section = 'Technical Approach';"
```

### Analysis Queries

```bash
# Score distribution
sqlite3 .data/<db>.db \
  "SELECT CAST(SUBSTR(ai_scorer, 1, 1) AS INTEGER) as score, COUNT(*) as count
   FROM scores GROUP BY score ORDER BY score DESC;"

# Per-section averages (identifies weakest areas)
sqlite3 .data/<db>.db -markdown -header \
  "SELECT section,
          COUNT(*) as questions,
          ROUND(AVG(CAST(SUBSTR(ai_scorer, 1, 1) AS REAL)), 2) as avg_score
   FROM scores GROUP BY section ORDER BY avg_score ASC;"

# Questions scoring below threshold
sqlite3 .data/<db>.db -markdown -header \
  "SELECT id, section, question, ai_scorer FROM scores
   WHERE CAST(SUBSTR(ai_scorer, 1, 1) AS INTEGER) <= 1
   ORDER BY CAST(id AS INTEGER);"

# Export scores as CSV for spreadsheet analysis
sqlite3 .data/<db>.db -csv -header \
  "SELECT * FROM scores ORDER BY CAST(id AS INTEGER);" > scores-export.csv
```

### Multi-Scorer Comparison

```bash
# Side-by-side comparison of all scorers
sqlite3 .data/<db>.db -markdown -header \
  "SELECT id, ai_scorer, jane_smith FROM scores ORDER BY CAST(id AS INTEGER);"

# Average score per scorer
sqlite3 .data/<db>.db -markdown -header \
  "SELECT 'ai_scorer' as scorer,
     ROUND(AVG(CAST(SUBSTR(ai_scorer, 1, 1) AS REAL)), 2) as avg
   FROM scores
   UNION ALL
   SELECT 'jane_smith',
     ROUND(AVG(CAST(SUBSTR(jane_smith, 1, 1) AS REAL)), 2)
   FROM scores;"

# Largest disagreements between scorers
sqlite3 .data/<db>.db -markdown -header \
  "SELECT id, question,
     CAST(SUBSTR(ai_scorer, 1, 1) AS INTEGER) as scorer_a,
     CAST(SUBSTR(jane_smith, 1, 1) AS INTEGER) as scorer_b,
     ABS(CAST(SUBSTR(ai_scorer, 1, 1) AS INTEGER) -
         CAST(SUBSTR(jane_smith, 1, 1) AS INTEGER)) as diff
   FROM scores WHERE diff >= 2 ORDER BY diff DESC;"
```

### Multi-Document Comparison

When scoring multiple documents (e.g., competing proposals), each gets its own database. Export and compare:

```bash
# Export each document's scores for comparison
sqlite3 .data/proposal-a-scoring.db \
  "SELECT id, CAST(SUBSTR(ai_scorer, 1, 1) AS INTEGER) as score FROM scores;" > proposal-a.txt
sqlite3 .data/proposal-b-scoring.db \
  "SELECT id, CAST(SUBSTR(ai_scorer, 1, 1) AS INTEGER) as score FROM scores;" > proposal-b.txt
```

## Examples

### Example 1: Score a Technical Proposal (Document Only)

```
/score-document ~/Documents/cloud-migration-proposal.pdf --scale 0-3
```

Scores each section of the proposal on a 0-3 scale with evidence. Results output as markdown only.

### Example 2: Score with Custom Rubric and Persist

```
/score-document ~/Documents/architecture-review.md --rubric ~/rubrics/arch-review.md --scale 0-5 --persist
```

Scores an architecture review against a custom rubric on a 0-5 scale and saves results to `.data/architecture-review-scoring.db`.

### Example 3: Score with Named Scorer for Later Comparison

```
/score-document ~/Documents/vendor-response.pdf --persist --scorer initial_review
```

Scores the document and persists under the `initial_review` column, allowing a second pass or different reviewer to add scores to the same database under a different column name.

### Example 4: Compare Multiple Scorers

```
/score-document ~/Documents/vendor-response.pdf --compare --db .data/vendor-response-scoring.db
```

Generates a side-by-side comparison of all scorer columns in the database, highlighting disagreements and average differences.

### Example 5: Query Persisted Scores

After persisting, query scores directly:

```bash
# Find all low-scoring sections
sqlite3 .data/vendor-response-scoring.db -markdown -header \
  "SELECT section, question, initial_review
   FROM scores
   WHERE initial_review LIKE '0 -%' OR initial_review LIKE '1 -%';"

# Search for security-related questions
sqlite3 .data/vendor-response-scoring.db -markdown -header \
  "SELECT id, question FROM questions_fts WHERE questions_fts MATCH 'security OR compliance';"
```

---

**Invoke with:** `/score-document <path>` to score a document against a rubric with evidence-based ratings. Add `--persist` to save scores to SQLite for querying and comparison.
