---
description: Extract structured content from PDF documents preserving headings, tables, and formatting
model: sonnet
---

# /pdf-extract

Extract structured content from PDF documents, preserving headings, tables, images, and formatting. Converts to clean Markdown with metadata frontmatter.

## When to Use This Skill

- Converting PDF reports or specifications into editable Markdown
- Extracting key content from vendor documentation
- Creating structured notes from PDF whitepapers or standards
- Capturing tables and figures from PDF documents
- Processing multi-page PDFs into searchable vault content

## Usage

```
/pdf-extract <path-to-pdf> [--pages 1-10] [--focus summary|full|tables-only]
```

### Parameters

| Parameter  | Description                                           | Required |
|------------|-------------------------------------------------------|----------|
| `path`     | Path to the PDF file                                  | Yes      |
| `--pages`  | Page range to extract (default: all, max 20 per pass) | No       |
| `--focus`  | Extraction focus (default: `full`)                    | No       |

## Instructions

### Phase 1: Assess the PDF

1. **Read the PDF** using the Read tool with the `pages` parameter for large PDFs
   - For PDFs > 10 pages, read in batches of 10-20 pages
   - Note: The Read tool natively supports PDF files
2. **Identify document structure:**
   - Title and author
   - Table of contents or section headings
   - Tables, charts, and figures
   - Page count and overall organisation
3. **Report to user:** "This PDF has X pages with Y sections, Z tables. Extracting [scope]."

### Phase 2: Extract Content

Process the PDF content systematically:

1. **Extract metadata:**
   - Title, author, date, version
   - Document type (report, specification, whitepaper, standard)
   - Key topics and themes

2. **Extract body content:**
   - Preserve heading hierarchy (H1, H2, H3)
   - Convert tables to Markdown table syntax
   - Note image/figure locations with `[Figure X: Description]` placeholders
   - Preserve lists (bulleted and numbered)
   - Maintain paragraph structure

3. **Handle special content:**
   - **Tables:** Convert to Markdown tables, noting column headers and alignment
   - **Code blocks:** Wrap in fenced code blocks with language hints
   - **Quotes/callouts:** Convert to blockquotes
   - **Footnotes:** Convert to inline references or endnotes

### Phase 3: Structure Output

Generate a Markdown document with:

1. **Frontmatter** — Metadata about the source document
2. **Summary** — AI-generated summary of the document
3. **Table of contents** — If the document has multiple sections
4. **Extracted content** — Clean Markdown preserving document structure
5. **Key takeaways** — Bullet list of the most important points

## Output Format

```markdown
---
type: Reference
title: "<Document Title>"
referenceType: article
created: YYYY-MM-DD
source: "<PDF filename>"
author: "<Author>"
tags: [content/document, domain/relevant-tag]
summary: "<One-line summary>"
---

# <Document Title>

> **Source:** <PDF filename> | **Pages:** X | **Extracted:** YYYY-MM-DD

## Summary

<2-3 paragraph AI-generated summary>

## Key Takeaways

- <Most important point 1>
- <Most important point 2>
- <Most important point 3>

## Contents

<Extracted content with preserved heading hierarchy>

### Section 1: <Heading>

<Content>

| Column A | Column B | Column C |
|----------|----------|----------|
| Data     | Data     | Data     |

[Figure 1: <Description of figure>]

### Section 2: <Heading>

<Content>

---

**Source:** `<path-to-pdf>`
```

## Examples

### Example 1: Full Extraction

```
/pdf-extract ~/Documents/cloud-migration-guide.pdf
```

Extracts the complete document with all sections, tables, and structure.

### Example 2: Specific Pages

```
/pdf-extract ~/Documents/annual-report.pdf --pages 15-30
```

Extracts only pages 15-30 (e.g., the technical appendix).

### Example 3: Tables Only

```
/pdf-extract ~/Documents/vendor-comparison.pdf --focus tables-only
```

Extracts only tables from the document, useful for comparison matrices.

---

**Invoke with:** `/pdf-extract <path-to-pdf>` to convert PDF content to structured Markdown
