---
description: Capture web page content with AI-generated summary and create a structured reference note
model: haiku
---

# /weblink

Capture a web page's content, generate an AI summary, and create a structured reference note. Quick, single-step capture for bookmarking valuable web resources.

## When to Use This Skill

- Saving a web article or blog post for future reference
- Capturing documentation pages with context
- Bookmarking tools, libraries, or resources with notes
- Creating a searchable reference from a URL

## Usage

```
/weblink <url> [--title "Custom Title"]
```

### Parameters

| Parameter  | Description                                  | Required |
|------------|----------------------------------------------|----------|
| `url`      | URL of the web page to capture               | Yes      |
| `--title`  | Override the page title (default: auto-detect)| No       |

## Instructions

### Phase 1: Fetch and Analyse

1. **Fetch the page** using WebFetch tool
2. **Extract:**
   - Page title (from `<title>` or `<h1>`)
   - Author and publication date (if available)
   - Main content (article body, excluding navigation and ads)
3. **Generate:**
   - One-line summary
   - 3-5 key points
   - Suggested tags based on content topics

### Phase 2: Create Reference Note

Generate a reference note with frontmatter and structured content.

## Output Format

```markdown
---
type: Reference
title: "Reference - <Page Title>"
referenceType: weblink
created: YYYY-MM-DD
url: "<url>"
author: "<Author if available>"
tags: [content/weblink, domain/relevant-tag]
summary: "<One-line summary>"
---

# <Page Title>

> **Source:** [<domain>](<url>) | **Captured:** YYYY-MM-DD

## Summary

<2-3 sentence summary of the page content>

## Key Points

- <Key point 1>
- <Key point 2>
- <Key point 3>

## Notes

<Any additional context or why this is relevant>
```

## Examples

### Example 1: Technical Article

```
/weblink https://example.com/microservices-patterns
```

### Example 2: Custom Title

```
/weblink https://docs.example.com/api/auth --title "Auth API Documentation"
```

---

**Invoke with:** `/weblink <url>` to capture and summarise a web page
