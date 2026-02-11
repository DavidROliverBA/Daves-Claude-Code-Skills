---
description: Create book notes with parallel extraction of concepts, frameworks, and actionable insights
model: sonnet
---

# /book-notes

Create structured book notes with parallel extraction of concepts, frameworks, and actionable insights. Uses three agents to extract different dimensions simultaneously, producing a rich reference note.

## When to Use This Skill

- Creating structured notes from a book you've read or are reading
- Extracting frameworks and models from business or technical books
- Capturing actionable advice from self-improvement or leadership books
- Building a personal library of book summaries and key ideas
- Processing book highlights or notes into structured knowledge

## Usage

```
/book-notes "<book-title>" --author "<author>" [--input highlights|summary|chapter-notes]
```

### Parameters

| Parameter  | Description                                          | Required |
|------------|------------------------------------------------------|----------|
| `title`    | Book title                                           | Yes      |
| `--author` | Book author                                          | Yes      |
| `--input`  | Source material type (default: user provides context) | No       |
| `--isbn`   | ISBN for metadata lookup                             | No       |

## Instructions

### Phase 1: Gather Input

Ask the user for their source material:
- **Highlights/annotations** — Kindle highlights, marginal notes, or key passages
- **Chapter summaries** — Brief notes per chapter
- **Overall impressions** — Free-form thoughts about the book
- **Key quotes** — Specific passages they found valuable

If the user has no notes, offer to create a template they can fill in, or search for the book online to gather context.

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

### Phase 3: Synthesise Book Notes

Combine agent outputs into a comprehensive reference note:
1. Book metadata and rating
2. One-paragraph summary
3. Key concepts (from Agent 1)
4. Frameworks and models (from Agent 2)
5. Actionable takeaways (from Agent 3)
6. Key quotes
7. Personal reflections

## Output Format

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
---

# <Book Title>

> **Author:** <Author> | **Published:** YYYY | **Rating:** ★★★★☆ (X/5)

## One-Paragraph Summary

<The book's core message in one paragraph>

## Key Concepts

### <Concept 1>
**Definition:** <What it is>
**Significance:** <Why it matters>
**Related to:** <Other concepts>

### <Concept 2>
...

## Frameworks and Models

### <Framework 1>
**Purpose:** <What problem it solves>
**Steps:**
1. <Step 1>
2. <Step 2>
3. <Step 3>
**When to use:** <Situations where this applies>

### <Framework 2>
...

## Actionable Takeaways

### High Impact
- [ ] <Action 1> — <Expected outcome>
- [ ] <Action 2> — <Expected outcome>

### Quick Wins
- [ ] <Action 3> — <Expected outcome>

## Key Quotes

> "<Quote 1>" (p. XX)

> "<Quote 2>" (p. XX)

## Personal Reflections

<What resonated, what you disagree with, how it connects to your work>

## Related Reading

- [[<Related book or concept>]]
```

## Examples

### Example 1: From Highlights

```
/book-notes "Thinking in Systems" --author "Donella Meadows" --input highlights
```

User provides Kindle highlights; agents extract systems thinking concepts, leverage points framework, and actionable mental models.

### Example 2: From Memory

```
/book-notes "Team Topologies" --author "Matthew Skelton"
```

User provides their recollections and key takeaways; agents structure them into concepts (cognitive load, team types), frameworks (four team topologies), and actions.

### Example 3: Technical Book

```
/book-notes "Designing Data-Intensive Applications" --author "Martin Kleppmann" --input chapter-notes
```

User provides chapter-by-chapter notes; agents extract distributed systems concepts, consistency models, and architecture decision guidance.

---

**Invoke with:** `/book-notes "<title>" --author "<author>"` to create structured book notes with parallel extraction
