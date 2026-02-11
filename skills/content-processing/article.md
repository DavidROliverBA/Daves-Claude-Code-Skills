---
description: Quick-capture articles from URLs with AI summary, key quotes, and relevance assessment
model: haiku
---

# /article

Quick-capture articles from URLs with AI-generated summary, key quotes, and relevance assessment. Designed for fast capture of articles you want to read later or reference.

## When to Use This Skill

- Saving articles from newsletters or RSS feeds
- Capturing thought-leadership pieces with key quotes
- Building a reading list with summaries and relevance scores
- Archiving paywalled articles you've already accessed

## Usage

```
/article <url> [--relevance "topic to assess against"]
```

### Parameters

| Parameter     | Description                                        | Required |
|---------------|----------------------------------------------------|----------|
| `url`         | URL of the article                                 | Yes      |
| `--relevance` | Topic to score relevance against (0-10)            | No       |

## Instructions

### Phase 1: Fetch and Extract

1. **Fetch the article** using WebFetch
2. **Extract metadata:** Title, author, publication, date, reading time estimate
3. **Extract content:** Main article body, excluding boilerplate

### Phase 2: Analyse

1. **Generate summary** — 2-3 paragraphs capturing the article's argument
2. **Extract key quotes** — 3-5 most important quotations
3. **Identify concepts** — Key terms, frameworks, or ideas introduced
4. **Assess relevance** — If `--relevance` specified, score 0-10 against the topic
5. **Suggest related reading** — If the article references other works

### Phase 3: Create Note

Generate a reference note.

## Output Format

```markdown
---
type: Reference
title: "Reference - <Article Title>"
referenceType: article
created: YYYY-MM-DD
url: "<url>"
author: "<Author>"
publication: "<Publication Name>"
publishDate: YYYY-MM-DD
readingTime: "<X min>"
tags: [content/article, domain/relevant-tag]
summary: "<One-line summary>"
---

# <Article Title>

> **Author:** <Author> | **Publication:** <Publication> | **Date:** YYYY-MM-DD
> **URL:** [Link](<url>) | **Reading Time:** ~X minutes

## Summary

<2-3 paragraph summary>

## Key Quotes

> "<Quote 1>" — <Author>

> "<Quote 2>" — <Author>

## Key Concepts

- **<Concept>** — <Brief explanation>

## Relevance Assessment

**Score:** X/10 for <topic>
**Reason:** <Why this score>

## Notes

<Personal notes or why this article matters>
```

## Examples

### Example 1: Quick Capture

```
/article https://example.com/future-of-enterprise-architecture
```

### Example 2: With Relevance Scoring

```
/article https://example.com/event-sourcing-patterns --relevance "integration architecture"
```

---

**Invoke with:** `/article <url>` to capture an article with AI summary and analysis
