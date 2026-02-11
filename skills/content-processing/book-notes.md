---
description: Create book notes with parallel extraction and optional knowledge compounding via spawned Concept/Pattern/Theme notes
model: sonnet
---

# /book-notes

Create structured book notes with parallel extraction of concepts, frameworks, and actionable insights. Uses three agents to extract different dimensions simultaneously, producing a rich reference note. Optionally spawns standalone knowledge nodes for concepts, patterns, and themes worth preserving independently.

## Usage

```
/book-notes "<book-title>" --author "<author>" [options]
```

### Parameters

| Parameter      | Description                                          | Required |
|----------------|------------------------------------------------------|----------|
| `title`        | Book title                                           | Yes      |
| `--author`     | Book author                                          | Yes      |
| `--input`      | Source material type (default: user provides context) | No       |
| `--isbn`       | ISBN for metadata lookup                             | No       |
| `--spawn`      | Enable knowledge compounding — spawn standalone notes | No       |
| `--spawn-only` | Skip book note creation, only spawn from existing    | No       |

## Instructions

### Phase 1: Gather Input

Ask the user for their source material: highlights/annotations, chapter summaries, overall impressions, or key quotes. If the user has no notes, offer to create a template they can fill in, or search for the book online to gather context.

### Phase 2: Parallel Extraction — Agent Team

Launch three agents simultaneously using the Task tool.

**Agent 1: Concept Extractor** (Sonnet)
Task: Identify and describe key concepts and ideas
- Extract all distinct concepts, theories, and ideas from the input
- For each concept: name, definition, significance, related concepts
- Identify the book's central thesis or argument
- Map how concepts relate to each other
- Note which concepts are original vs building on existing work
Return: List of concepts with descriptions and relationships

**Agent 2: Framework Extractor** (Sonnet)
Task: Identify frameworks, models, and methodologies
- Extract all structured frameworks, models, and step-by-step processes
- For each: name, purpose, steps/components, when to use it
- Identify mental models the author uses or promotes
- Note practical tools or templates described
- Create visual representations where possible (tables, lists)
Return: List of frameworks with descriptions and application guidance

**Agent 3: Action Extractor** (Sonnet)
Task: Extract practical advice and recommendations
- Pull out all actionable advice and recommendations
- For each: what to do, when to do it, expected outcome
- Identify exercises, experiments, or practices suggested
- Note warnings or anti-patterns the author highlights
- Prioritise actions by impact and ease of implementation
Return: Prioritised list of actionable takeaways with context

### Phase 3: Synthesise Book Note

Combine agent outputs into a comprehensive reference note:
1. Book metadata and rating
2. One-paragraph summary
3. Key concepts (from Agent 1)
4. Frameworks and models (from Agent 2)
5. Actionable takeaways (from Agent 3)
6. Key quotes
7. Personal reflections

If `--spawn` is active, proceed to Phase 4 after writing the book note.

### Phase 4: Knowledge Compounding (Optional)

Activated by the `--spawn` flag. Default behaviour (no flag) creates only the book note.

#### Step 1: Check for Existing Spawned Nodes (Idempotent Handling)

If the book note already exists, read its frontmatter for a `spawnedNodes` field.

| Situation                    | Action                                         |
|------------------------------|-------------------------------------------------|
| No existing `spawnedNodes`   | Proceed with full analysis                     |
| Has `spawnedNodes`           | Skip existing, analyse for new candidates only |

When running incrementally, append new nodes to `spawnedNodes` rather than replacing the list.

#### Step 2: Vault Deduplication Search

Before proposing spawn candidates, search existing notes to avoid duplicates.

For each potential candidate:

1. **Exact match search** — check for files named `Concept - <candidate>`, `Pattern - <candidate>`, or `Theme - <candidate>`
2. **Partial match search** — search note contents for the candidate term

**Decision Matrix:**

| Search Result                                       | Action                                    |
|-----------------------------------------------------|-------------------------------------------|
| Exact match exists                                  | **Link** to existing note, do not spawn   |
| Partial coverage (mentioned but no dedicated note)  | Offer to spawn or enrich existing         |
| Related concept exists                              | Add to `relatedTo`, may still spawn       |
| No coverage                                         | Add to **spawn candidates**               |

Report results before proceeding.

#### Step 3: Classify and Assess Candidates

Using the extracted concepts (from Phase 2 agents), classify each candidate:

| Type        | Criteria                                             |
|-------------|------------------------------------------------------|
| **Concept** | "What is X?" — definitions, frameworks, models       |
| **Pattern** | "How to do X?" — approaches, architectures, solutions |
| **Theme**   | Cross-cutting concerns, paradigm shifts, strategic directions |

For each candidate, determine:

| Field            | Description                                         |
|------------------|-----------------------------------------------------|
| `name`           | Note title                                          |
| `type`           | Concept, Pattern, or Theme                          |
| `definition`     | 1-2 sentence definition                             |
| `sourceChapters` | Which chapters cover this                           |
| `sourcePrimary`  | Is this book THE authoritative source?              |
| `confidence`     | Derived from source quality (see Confidence table)  |

#### Step 4: Map Inter-Node Relationships

Before creating notes, map how candidates relate to each other using typed relationships:

| Relationship Type       | Meaning                                |
|-------------------------|----------------------------------------|
| "component of"          | X is a part of Y                       |
| "implements"            | X realises Y in practice               |
| "enables"               | X makes Y possible                     |
| "governs"               | X provides rules/constraints for Y     |
| "defines interface for" | X specifies how to interact with Y     |

This ensures spawned notes link to siblings, not just back to the source book.

#### Step 5: Create Spawned Notes

Create notes in this order (so earlier notes can be referenced by later ones):
1. Themes first (broadest scope)
2. Concepts second (foundational)
3. Patterns last (apply concepts)

For each node:
1. Create file using the appropriate spawned note template (see below)
2. Populate provenance fields: `sourceBook`, `sourceChapters`, `sourcePrimary`
3. Set `confidence` based on the inheritance rules
4. Include `relatedTo` linking to sibling nodes AND the source book

#### Step 6: Update Book Note

Add the `spawnedNodes` field to the book note frontmatter and append a "Spawned Knowledge" section to the body:

```markdown
## Spawned Knowledge

This book is a primary source for the following knowledge notes:

### Themes
| Note | Description |
|------|-------------|
| [[Concept - <Name>]] | <description> |

### Core Concepts
| Note | Description | Chapters |
|------|-------------|----------|
| [[Concept - <Name>]] | <description> | Ch. N |

### Implementation Patterns
| Note | Description | Chapters |
|------|-------------|----------|
| [[Pattern - <Name>]] | <description> | Ch. N |
```

## Output Format

### Book Note Template

```markdown
---
type: Reference
title: "Reference - <Book Title>"
referenceType: book
created: YYYY-MM-DD
author: "<Author>"
isbn: "<ISBN if available>"
yearPublished: YYYY
tags: [content/book, domain/relevant-tag]
rating: X/5
summary: "<One-line summary>"

# Knowledge Compounding (populated by --spawn)
spawnedNodes: []
---

# <Book Title>

> **Author:** <Author> | **Published:** YYYY | **Rating:** X/5

## One-Paragraph Summary

<The book's core message in one paragraph>

## Key Concepts
<!-- From Agent 1: name, definition, significance, relationships -->

## Frameworks and Models
<!-- From Agent 2: name, purpose, steps, when to use -->

## Actionable Takeaways
<!-- From Agent 3: prioritised by impact — High Impact / Quick Wins -->

## Key Quotes

## Personal Reflections

## Related Reading
```

### Spawned Concept Template

**Filename:** `Concept - <Name>.md`

Create for "What is X?" knowledge — definitions, frameworks, models.

```markdown
---
type: Concept
title: "<Name>"
aliases: []
created: YYYY-MM-DD
tags: []

# Source Provenance
sourceBook: "[[Reference - <Book Title>]]"
sourceChapters: [N, N]
sourcePrimary: true|false

# Relationships
relatedTo:
  - "[[Reference - <Book Title>]]"
  - "[[Concept - <Sibling>]]"

# Quality
summary: "<One-line definition>"
confidence: high|medium|low
---

# <Name>

> **Definition:** <Clear, concise definition>

## Overview

<2-3 paragraphs explaining the concept, written to be standalone>

## Key Characteristics

- <Characteristic 1>
- <Characteristic 2>

## Related Concepts

- [[Concept - <Sibling>]] — <relationship>

## Sources

- [[Reference - <Book Title>]] — Ch. N (primary|secondary source)
```

### Spawned Pattern Template

**Filename:** `Pattern - <Name>.md`

Create for "How to do X?" knowledge — approaches, architectures, solutions.

```markdown
---
type: Pattern
title: "<Name>"
aliases: []
created: YYYY-MM-DD
tags: []

# Source Provenance
sourceBook: "[[Reference - <Book Title>]]"
sourceChapters: [N, N]
sourcePrimary: true|false

# Relationships
relatedTo:
  - "[[Reference - <Book Title>]]"
  - "[[Concept - <Related>]]"

# Quality
summary: "<One-line description>"
confidence: high|medium|low
---

# <Name>

> **Intent:** <What problem does this pattern solve?>

## Context and Problem

<When to use this pattern and what challenge it addresses>

## Solution

<How the pattern works>

## Consequences

**Benefits:** / **Trade-offs:**

## Related Patterns

- [[Pattern - <Sibling>]] — <relationship>

## Sources

- [[Reference - <Book Title>]] — Ch. N
```

### Spawned Theme Template

**Filename:** `Concept - <Name>.md` (themes use `conceptType: theme`)

Create for cross-cutting concerns, paradigm shifts, strategic directions.

```markdown
---
type: Concept
title: "<Name>"
conceptType: theme
aliases: []
created: YYYY-MM-DD
tags: []

# Source Provenance
sourceBook: "[[Reference - <Book Title>]]"
sourceChapters: [N, N]
sourcePrimary: true|false

# Relationships
relatedTo:
  - "[[Reference - <Book Title>]]"
  - "[[Concept - <Manifestation>]]"
  - "[[Pattern - <Implements theme>]]"

# Quality
summary: "<One-line description>"
confidence: high|medium|low
---

# <Name>

> **Essence:** <One sentence capturing the core of this theme>

## Overview

<2-3 paragraphs explaining the theme and its significance>

## Manifestations

- [[Concept - <X>]] — <How this concept embodies the theme>
- [[Pattern - <Y>]] — <How this pattern implements the theme>

## Tensions and Trade-offs

<What this theme trades off against, competing concerns>

## Sources

- [[Reference - <Book Title>]] — Primary exposition
```

## Knowledge Compounding Reference

### Confidence Inheritance

| Source Quality                           | Criteria                                              | Spawned Confidence |
|-----------------------------------------|-------------------------------------------------------|--------------------|
| **Authoritative**                        | Author coined or invented the term                   | `high`             |
| **Deep treatment**                       | Dedicated chapter(s), comprehensive coverage          | `high`             |
| **Substantial**                          | Multiple sections, detailed explanation               | `medium`           |
| **Referenced**                           | Mentioned, explained briefly                          | `medium`           |
| **Brief mention**                        | Passing reference, assumes prior knowledge            | `low`              |

### Typical Spawn Counts

| Book Type               | Themes | Concepts | Patterns |
|--------------------------|--------|----------|----------|
| Technical deep-dive      | 1-3    | 5-10     | 3-7      |
| Survey / "Fundamentals"  | 2-4    | 10-20    | 5-10     |
| Practical guide          | 1-2    | 3-7      | 5-15     |
| Business / strategy      | 2-4    | 3-5      | 1-3      |

### Spawn Decision Rules

**Do spawn** when the term needs standalone explanation, the book is THE primary source, or the concept/pattern will be referenced from multiple notes. **Do not spawn** when an existing note covers it (link instead), the term is too narrow or book-specific, or coverage is too brief to support a useful standalone note.

## Examples

### Example 1: From Highlights

```
/book-notes "Thinking in Systems" --author "Donella Meadows" --input highlights
```

User provides Kindle highlights; agents extract systems thinking concepts, leverage points framework, and actionable mental models.

### Example 2: With Knowledge Compounding

```
/book-notes "Team Topologies" --author "Matthew Skelton" --spawn
```

Creates the book note, then identifies candidates such as Concept - Cognitive Load, Concept - Team API, Pattern - Stream-Aligned Team, and Theme - Team-First Thinking. Searches the vault for existing coverage, presents candidates for approval, and creates standalone notes with provenance tracking.

### Example 3: Spawn from Existing Book Note

```
/book-notes "Designing Data-Intensive Applications" --author "Martin Kleppmann" --spawn-only
```

Reads the existing book note, identifies concepts and patterns not yet spawned, and creates standalone notes without recreating the book note.

---

**Invoke with:** `/book-notes "<title>" --author "<author>"` to create structured book notes with parallel extraction, or add `--spawn` to also create standalone knowledge notes
