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

For each note:

1. Read the title, frontmatter, and first 500 words of body content
2. Generate a one-line summary following the **Writing Rules** and **Summary Patterns by Type** below
3. Return: List of `{ filename, generatedSummary }` per note

#### Writing Rules

Every generated summary must follow these constraints:

- **Length:** 10-25 words, one sentence, no period at the end
- **Voice:** Start with the subject, not "This note..." or "A document about..."
- **Tense:** Use present tense for active items, past tense for completed
- **Content:** Include the most distinctive and searchable terms
- **Avoid generic openers:** Never start with "Overview of...", "Notes on...", "Summary of...", "Document about...", "Page covering..."
- **UK English** throughout
- **No line breaks** — single sentence only

#### Summary Patterns by Type

| Type | Pattern | Example |
|------|---------|---------|
| Concept | What X is and why it matters | `Continuous integration practice ensuring code changes are validated automatically on every commit` |
| Pattern | How to apply X for Y | `Event-driven architecture pattern for decoupling services via asynchronous message passing` |
| ADR | What was decided and why | `Selected PostgreSQL over MongoDB for transactional consistency in the order management domain` |
| Meeting | What was discussed and decided | `Sprint review covering API migration progress and blockers for the Q2 release` |
| Project | What the project delivers and its current state | `Data platform modernisation delivering real-time analytics for operational dashboards` |
| Task | What needs to be done and why | `Review security findings from penetration test before production release approval` |
| Reference | What the source covers and its relevance | `AWS Well-Architected Framework covering operational excellence and reliability pillars` |
| Research | What was investigated and key findings | `Comparison of stream processing frameworks for event-driven integration workloads` |
| System | What the system does | `Enterprise MRO platform managing aircraft maintenance scheduling and compliance tracking` |
| Person | Role and context | `Solutions Architect in platform engineering, leading the data integration workstream` |
| Incubator | What idea is being explored | `Exploring voice-activated workflows for hands-free note capture during site visits` |
| Email | What the email communicates | `Proposal to programme board for adopting infrastructure-as-code across the platform team` |

#### Quality Checks

After generating each summary, validate against these rules:

- **Too long:** Flag if over 25 words — tighten the phrasing
- **Too short:** Flag if under 10 words — add meaningful context
- **Too vague:** Flag if the summary could apply to any note of that type (e.g., "Architecture decision about a technology choice")
- **Banned phrases:** Reject summaries starting with any of these:
  - "This note..."
  - "A document about..."
  - "Summary of..."
  - "Overview of..."
  - "Notes on..."
  - "Page about..."
  - "Document covering..."
- **Missing specifics:** Flag if the summary lacks any concrete nouns (technologies, processes, outcomes)

If a summary fails quality checks, regenerate it before returning.

### Phase 3: Review and Apply

1. **Compile summaries** from all agents
2. **Present for review** in a table
3. If `--mode apply`: Write summaries to frontmatter

**Frontmatter format:**
```yaml
summary: "Selected PostgreSQL over MongoDB for transactional consistency in the order domain"
```

Always quote the summary value since it may contain special YAML characters (colons, brackets).

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

## Safety

- Always use `--mode suggest` first for vault-wide operations
- Never overwrite existing non-null summaries
- Commit to git before running
- If note body is too short (<50 words), skip rather than guess
- Summary generation is additive only — never removes existing summaries

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
