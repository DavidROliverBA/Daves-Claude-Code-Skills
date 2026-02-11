---
description: Create Architecture Decision Records with structured context, rationale, and consequences
model: sonnet
---

# /adr

Create Architecture Decision Records (ADRs) following a standard template with Context, Decision, Rationale, Consequences, and Alternatives Considered. Guides you through capturing the reasoning behind significant architectural choices.

## When to Use This Skill

- Recording a significant technical or architectural decision
- Documenting why a particular approach was chosen over alternatives
- Creating a decision log for governance or audit purposes
- Capturing trade-offs discussed in architecture reviews
- Updating or superseding an existing decision

## Usage

```
/adr <title> [--status proposed|accepted|deprecated|superseded]
```

### Parameters

| Parameter  | Description                                   | Required |
|------------|-----------------------------------------------|----------|
| `title`    | Short title for the decision                  | Yes      |
| `--status` | Decision status (default: `proposed`)         | No       |

## Instructions

### Phase 1: Gather Decision Context

Prompt the user for the following information. If they provide partial input, work with what's available and note assumptions.

**Required:**

| Field               | Description                                                | Example                                      |
|---------------------|------------------------------------------------------------|----------------------------------------------|
| **Title**           | Short, descriptive title                                   | Use Event-Driven Integration for Order Flow  |
| **Context**         | What is the problem or situation driving this decision?    | Orders must propagate to 5 downstream systems within 2 seconds |
| **Decision**        | What is being decided?                                     | Adopt Apache Kafka as the event broker       |
| **Rationale**       | Why this option over alternatives?                         | Kafka handles our throughput needs and supports replay |
| **Alternatives**    | What other options were considered?                        | REST polling, RabbitMQ, AWS SNS/SQS          |

**Optional:**

| Field               | Description                                                |
|---------------------|------------------------------------------------------------|
| **Deciders**        | Who participated in the decision?                          |
| **Consequences**    | What becomes easier or harder as a result?                 |
| **Related decisions**| Links to related or dependent ADRs                        |
| **Assumptions**     | What assumptions underpin this decision?                   |
| **Constraints**     | What constraints influenced the decision?                  |

### Phase 2: Generate ADR Document

Create the ADR with the following structure:

1. **Frontmatter** — title, type, status, date, deciders, tags
2. **Context** — The problem space and forces at play
3. **Decision** — The chosen approach, stated clearly
4. **Rationale** — Why this option was selected, with evidence
5. **Consequences** — What becomes easier and what becomes harder
6. **Alternatives Considered** — Each alternative with pros/cons and why it was rejected
7. **Related Decisions** — Links to ADRs this depends on, supersedes, or relates to
8. **Review Date** — When this decision should be revisited

### Phase 3: Cross-Reference

- Search the vault/repository for existing ADRs that relate to this decision
- Suggest `relatedTo`, `dependsOn`, or `supersedes` links
- If this ADR supersedes another, suggest updating the old ADR's status to `deprecated`

## Output Format

```markdown
---
type: ADR
title: "ADR - <Title>"
status: proposed
created: YYYY-MM-DD
deciders:
  - "[[Person Name]]"
tags: [domain/architecture, activity/decision]
relatedTo: []
supersedes: []
dependsOn: []
confidence: medium
summary: "<One-line summary>"
---

# ADR - <Title>

## Status

**Proposed** | YYYY-MM-DD

## Context

<What is the issue motivating this decision? What forces are at play?>

## Decision

<What is the change being proposed or decided?>

## Rationale

<Why this option? What evidence supports it?>

## Consequences

### Easier
- <What becomes simpler, faster, or cheaper>

### Harder
- <What becomes more complex, expensive, or constrained>

## Alternatives Considered

### Alternative 1: <Name>
- **Pros:** <advantages>
- **Cons:** <disadvantages>
- **Rejected because:** <specific reason>

### Alternative 2: <Name>
- **Pros:** <advantages>
- **Cons:** <disadvantages>
- **Rejected because:** <specific reason>

## Assumptions

- <Key assumptions underpinning this decision>

## Related Decisions

- Depends on: <linked ADRs>
- Related to: <linked ADRs>

## Review Date

This decision should be revisited by YYYY-MM-DD or when <trigger condition>.
```

## Examples

### Example 1: Integration Pattern Decision

```
/adr Use Event-Driven Integration for Order Processing
```

Generates an ADR capturing the decision to use Kafka for order event propagation, with REST polling and message queues as rejected alternatives.

### Example 2: Database Technology Choice

```
/adr --status accepted Adopt PostgreSQL for Transactional Data
```

Generates an accepted ADR documenting the choice of PostgreSQL over MySQL and DynamoDB for the transactional data store.

### Example 3: Superseding a Previous Decision

```
/adr --status accepted Migrate from REST to GraphQL for Client API
```

Generates an ADR that supersedes a previous REST API decision, with rationale for the migration and updated consequence analysis.

---

**Invoke with:** `/adr <title>` then answer the prompts to capture your architectural decision
