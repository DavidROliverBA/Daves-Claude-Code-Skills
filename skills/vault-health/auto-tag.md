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
/auto-tag --type Meeting         # Only process notes of a specific type
/auto-tag --limit 50             # Process at most 50 notes
```

### Parameters

| Parameter     | Description                                          | Required |
|---------------|------------------------------------------------------|----------|
| `--scope`     | Folder or glob pattern (default: notes missing tags) | No       |
| `--mode`      | `suggest` shows tags; `apply` writes them (default: `suggest`) | No |
| `--taxonomy`  | Path to tag taxonomy file for reference              | No       |
| `--type`      | Only process notes of a specific frontmatter type    | No       |
| `--limit`     | Maximum number of notes to process                   | No       |

## Instructions

### Phase 1: Identify Notes Needing Tags

1. **Scan notes in scope** -- Find all Markdown files
2. **Parse frontmatter** -- Extract existing tags
3. **Filter to candidates:**
   - Notes with no tags field
   - Notes with empty tags (`tags: []`)
   - Notes with fewer than 2 tags
   - Notes with flat (non-hierarchical) tags
4. **Exclude directories:** `Templates/`, `.obsidian/`, `.claude/`, `Archive/`, `Attachments/`
5. **Load taxonomy** -- If `--taxonomy` provided, use it as the tag reference. Otherwise, scan existing tags across the vault to build a frequency-based taxonomy.
6. **Sort by type** for batch efficiency
7. **Divide into batches** of 15-20 notes per agent

### Phase 2: Batch Tagging -- Agent Team (Parallel Haiku Agents)

Use the Batch Processing pattern. Launch N parallel agents, each processing 15-20 notes.

**Agent 1-N: Tag Analyst** (Haiku)
Task: Analyse content and suggest tags for assigned batch

For each note in the batch:

1. **Read frontmatter** -- extract `type`, `title`, `project`, `status`
2. **Read body content** -- first 500 words
3. **Apply type-based auto-tags** -- deterministic tags from the Type-Based Auto-Tags table below
4. **Apply content keyword matching** -- use the Content Keyword-to-Tag Mapping table below
5. **Apply project field matching** -- if `project:` field exists, derive a `project/` tag
6. **Suggest 2-5 hierarchical tags** per note total
7. **Validate tags** -- check all suggested tags against the taxonomy (if provided); flag any tag not in the taxonomy as "novel"

Quality rules:
- No `#` prefix in YAML tags
- All lowercase
- Hierarchical format required (e.g., `domain/data` not just `data`)
- Hyphens for multi-word tags (e.g., `domain/supply-chain`)
- Minimum 2 tags, maximum 5 tags per note
- Prefer fewer, more accurate tags over many vague ones

Return: List of `{ filename, existingTags[], suggestedTags[], confidence, reason }` per note

---

## Tag Mapping Reference

> **Customise these tables for your vault.** The mappings below are generic starting points. Replace or extend them with your own domain-specific keywords, project names, and technology stack.

### Type-Based Auto-Tags

These deterministic tags are **always** added based on the note's `type` frontmatter field. They require no content analysis.

| Type        | Auto-tags                               | Notes                                    |
|-------------|-----------------------------------------|------------------------------------------|
| ADR         | `type/adr`, `activity/architecture`     | Architecture Decision Records            |
| Project     | `activity/delivery`                     | Also add `project/<name>` from title     |
| Meeting     | `activity/meeting`                      | Infer topic tags from title/content      |
| Task        | `activity/task`                         | Infer project from `project:` field      |
| Research    | `activity/research`                     | Research and investigation notes         |
| Incubator   | `activity/research`                     | Early-stage ideas and explorations       |
| Concept     | `type/concept`                          | Infer domain tags from content           |
| Pattern     | `type/pattern`                          | Infer domain tags from content           |
| Reference   | `type/reference`                        | Also infer from `referenceType` if set   |
| System      | `type/system`                           | Technology entity notes                  |
| Daily       | `daily`                                 | Daily journal entries                    |
| Email       | _(infer from content)_                  | No deterministic tags                    |
| Trip        | _(skip)_                                | Typically no tags needed                 |

### Content Keyword-to-Tag Mapping

When note content (title + body) contains these keywords, suggest the corresponding tag. This table is a **template** -- adapt the keywords and tags to match your vault's domain and technology stack.

| Content Keywords                           | Suggested Tag             |
|--------------------------------------------|---------------------------|
| AWS, Lambda, S3, EC2, CloudFormation       | `technology/aws`          |
| Kafka, streaming, event-driven             | `technology/kafka`        |
| API, REST, GraphQL, endpoint, OpenAPI      | `technology/api`          |
| database, SQL, migration, schema, ORM      | `technology/database`     |
| Docker, Kubernetes, container, helm        | `technology/containers`   |
| CI/CD, pipeline, deployment, GitHub Actions| `technology/cicd`        |
| Python, JavaScript, TypeScript, Go, Rust   | `technology/<language>`   |
| security, IAM, encryption, authentication  | `domain/security`         |
| data, analytics, pipeline, warehouse       | `domain/data`             |
| cloud, infrastructure, networking          | `domain/cloud`            |
| integration, middleware, message broker    | `domain/integration`      |
| architecture, design, pattern, C4          | `activity/architecture`   |
| research, investigation, POC, spike        | `activity/research`       |
| governance, compliance, policy, audit      | `activity/governance`     |
| meeting, standup, review, retrospective    | `activity/meeting`        |
| risk, threat, vulnerability, CVE           | `domain/security`         |
| documentation, guide, how-to, runbook      | `activity/documentation`  |
| planning, roadmap, strategy, vision        | `activity/planning`       |
| monitoring, observability, logging, alerts | `domain/operations`       |

### Project Field Mapping

If the note has a `project:` frontmatter field containing a wiki-link, derive a project tag:

```
project: "[[Project - Orders Platform]]"  -->  project/orders-platform
project: "[[Project - Cloud Migration]]"  -->  project/cloud-migration
```

**Rule:** Lowercase the project name, replace spaces with hyphens, strip the `Project - ` prefix.

---

### Phase 3: Synthesise and Validate

1. **Compile suggestions** from all agents
2. **Validate against taxonomy:**
   - Check every suggested tag exists in the taxonomy file (if provided)
   - Flag tags not in the taxonomy as "novel" -- these need manual review
   - Do not auto-apply novel tags
3. **Group by confidence:**
   - **High:** Tags from the type-based auto-tags table, or exact matches in the taxonomy
   - **Medium:** Tags inferred from content keyword matching against known taxonomy entries
   - **Low:** Novel tags not found in the taxonomy
4. **De-duplicate** -- remove tags already present on the note

### Phase 4: Apply Tags

If `--mode apply`:

1. Apply high-confidence tags automatically
2. Present medium/low confidence tags for user review before applying

For each note with approved tags:

1. Read current frontmatter
2. If `tags: []` -- replace with suggested tags
3. If no tags field -- add `tags:` with suggested tags
4. **Never overwrite existing non-empty tags** -- only add to them
5. Write updated file using Edit tool

#### YAML Formatting Rules

```yaml
# Inline format for 1-3 tags:
tags: [activity/research, domain/data]

# Multi-line format for 4+ tags:
tags:
  - activity/architecture
  - technology/aws
  - domain/cloud
  - project/cloud-migration
```

**Rules:**
- Use inline `[tag1, tag2]` format when there are 1-3 tags
- Switch to multi-line format (one tag per line with `- ` prefix) when there are 4 or more tags
- Match whichever format the file already uses, if tags were previously present
- No `#` prefix -- ever -- in frontmatter YAML

### Phase 5: Report

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

| Note                   | Existing Tags          | Suggested Tags                          |
|------------------------|------------------------|-----------------------------------------|
| `ADR - API Gateway.md` | `[]`                  | + `type/adr`, `activity/architecture`   |

### Medium Confidence

| Note                   | Existing Tags | Suggested Tags              | Reason                          |
|------------------------|---------------|-----------------------------|---------------------------------|
| `Meeting - 2026-01...` | `[]`          | `activity/meeting`, `domain/data` | Title mentions data review |

### New Tags Introduced

| Tag                     | Suggested For | In Taxonomy? |
|-------------------------|---------------|--------------|
| `domain/observability`  | 3 notes       | No           |

## By Type

| Type    | Tagged | Common Tags Applied         |
|---------|--------|-----------------------------|
| Meeting | 45     | `activity/meeting`, domain/* |
| ADR     | 20     | `type/adr`, technology/*     |
| Concept | 30     | `type/concept`, domain/*     |
```

## Safety

- **Always use `--mode suggest` first** for vault-wide operations
- **Never overwrite** existing non-empty tags -- tags are additive only
- **Commit to git** before running `--mode apply`
- **Review novel tags** before applying -- they may indicate taxonomy gaps
- **Validate against taxonomy** to prevent tag drift and inconsistency

## Examples

### Example 1: Preview Tags for All Untagged Notes

```
/auto-tag --mode suggest
```

### Example 2: Apply Tags to a Specific Folder

```
/auto-tag --scope Meetings/2026/ --mode apply
```

### Example 3: With Custom Taxonomy

```
/auto-tag --taxonomy .claude/context/tag-taxonomy.md --mode suggest
```

### Example 4: Process Only ADRs

```
/auto-tag --type ADR --mode suggest
```

---

**Invoke with:** `/auto-tag` to batch-tag notes with AI-suggested hierarchical tags
