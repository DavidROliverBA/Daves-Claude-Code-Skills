---
description: Extract and structure content from any document format with automatic format detection
model: sonnet
---

# /document-extract

Extract and structure content from any document format. Auto-detects the format (PDF, PPTX, DOCX, HTML, plain text) and applies the appropriate extraction method. A general-purpose fallback when you're not sure which specific extraction skill to use.

## When to Use This Skill

- Processing a document when you're unsure of the best extraction approach
- Handling formats not covered by specific skills (DOCX, HTML, CSV, etc.)
- Batch-processing a folder of mixed document types
- Extracting content from email attachments or downloaded files

## Usage

```
/document-extract <path-to-file> [--output-type reference|concept|raw]
```

### Parameters

| Parameter       | Description                                          | Required |
|-----------------|------------------------------------------------------|----------|
| `path`          | Path to the document file                            | Yes      |
| `--output-type` | Type of note to create (default: `reference`)        | No       |

## Instructions

### Phase 1: Detect Format and Assess

1. **Identify file format** from the extension:
   - `.pdf` → Delegate to `/pdf-extract` approach
   - `.pptx` → Delegate to `/pptx-extract` approach
   - `.docx` → Use python-docx extraction
   - `.html` / `.htm` → Parse HTML to Markdown
   - `.csv` / `.xlsx` → Extract as tables
   - `.txt` / `.md` → Read directly
   - `.json` / `.yaml` → Parse and structure
2. **Assess document size** — For large documents, plan chunked processing
3. **Report to user:** "Detected <format>, <size>. Extracting as <output-type>."

### Phase 2: Extract Content

Apply format-appropriate extraction:

**For DOCX files:**
```python
from docx import Document

def extract_docx(filepath):
    doc = Document(filepath)
    content = []
    for para in doc.paragraphs:
        style = para.style.name
        text = para.text.strip()
        if text:
            content.append({"style": style, "text": text})
    for table in doc.tables:
        rows = []
        for row in table.rows:
            rows.append([cell.text for cell in row.cells])
        content.append({"type": "table", "rows": rows})
    return content
```

**For HTML files:**
- Parse with WebFetch or direct HTML-to-Markdown conversion
- Extract main content (ignore navigation, headers, footers)
- Preserve headings, links, tables, and lists

**For CSV/XLSX files:**
- Read as tabular data
- Identify column headers
- Generate Markdown tables
- Summarise data patterns and key statistics

**For JSON/YAML files:**
- Parse structure
- Present as formatted code blocks
- Summarise key fields and data patterns

### Phase 3: Structure Output

Generate a note based on `--output-type`:
- **reference** — Full reference note with frontmatter, summary, and extracted content
- **concept** — Extract key concepts and create a concept note
- **raw** — Minimal formatting, just the extracted content

## Output Format

```markdown
---
type: Reference
title: "Reference - <Document Title>"
referenceType: article
created: YYYY-MM-DD
source: "<filename>"
format: "<detected format>"
tags: [content/document, domain/relevant-tag]
summary: "<One-line summary>"
---

# <Document Title>

> **Source:** <filename> | **Format:** <format> | **Extracted:** YYYY-MM-DD

## Summary

<AI-generated summary>

## Key Points

- <Key point 1>
- <Key point 2>

## Content

<Extracted and structured content>
```

## Examples

### Example 1: Word Document

```
/document-extract ~/Documents/requirements-spec.docx
```

### Example 2: CSV Data

```
/document-extract ~/Downloads/survey-results.csv --output-type raw
```

### Example 3: HTML Page

```
/document-extract ~/Downloads/saved-page.html --output-type concept
```

---

**Invoke with:** `/document-extract <path>` to extract content from any supported document format
