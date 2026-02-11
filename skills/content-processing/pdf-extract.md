---
description: Extract structured content from PDF documents preserving headings, tables, and formatting
model: sonnet
---

# /pdf-extract

Extract structured content from PDF documents, preserving headings, tables, images, and formatting. Converts to clean Markdown with metadata frontmatter. Supports two extraction methods: Claude's built-in Read tool (zero dependencies) or [docling](https://github.com/docling-project/docling) (superior table recognition and reading order detection).

## When to Use This Skill

- Converting PDF reports or specifications into editable Markdown
- Extracting key content from vendor documentation
- Creating structured notes from PDF whitepapers or standards
- Capturing tables and figures from PDF documents
- Processing multi-page PDFs into searchable vault content

## Usage

```
/pdf-extract <path-to-pdf> [--pages 1-10] [--focus summary|full|tables-only] [--method read|docling]
```

### Parameters

| Parameter  | Description                                           | Required |
|------------|-------------------------------------------------------|----------|
| `path`     | Path to the PDF file                                  | Yes      |
| `--pages`  | Page range to extract (default: all, max 20 per pass) | No       |
| `--focus`  | Extraction focus (default: `full`)                    | No       |
| `--method` | Extraction method (default: auto-detect)              | No       |

### Extraction Methods

| Method | When to Use | Strengths | Limitations |
|--------|-------------|-----------|-------------|
| **`read`** | Default fallback; simple documents; no dependencies needed | Zero setup, works everywhere, handles images visually | 20-page limit per pass, weaker table extraction |
| **`docling`** | Complex documents; many tables; large PDFs; batch processing | Native table recognition, reading order detection, full document in one pass, ~0.85 sec/page | Requires `pip install docling` (~250 MB) |

**Auto-detect behaviour:** If `--method` is not specified, check whether docling is installed. If available, use docling. Otherwise, fall back to the Read tool.

## Instructions

### Phase 1: Assess the PDF

1. **Verify the PDF** exists at the specified path
2. **Determine extraction method:**
   - If `--method read` specified: use Read tool
   - If `--method docling` specified: use docling (fail with install instructions if not available)
   - If not specified: auto-detect (try docling import, fall back to Read tool)
3. **Report to user:** "This PDF has X pages. Extracting with [method]."

### Phase 2a: Extract with Read Tool

Use this method when docling is not available or `--method read` is specified.

1. **Read the PDF** using the Read tool with the `pages` parameter for large PDFs
   - For PDFs > 10 pages, read in batches of 10-20 pages
   - Note: The Read tool natively supports PDF files
2. **Identify document structure:**
   - Title and author
   - Table of contents or section headings
   - Tables, charts, and figures
   - Page count and overall organisation
3. **Extract metadata:**
   - Title, author, date, version
   - Document type (report, specification, whitepaper, standard)
   - Key topics and themes
4. **Extract body content:**
   - Preserve heading hierarchy (H1, H2, H3)
   - Convert tables to Markdown table syntax
   - Note image/figure locations with `[Figure X: Description]` placeholders
   - Preserve lists (bulleted and numbered)
   - Maintain paragraph structure
5. **Handle special content:**
   - **Tables:** Convert to Markdown tables, noting column headers and alignment
   - **Code blocks:** Wrap in fenced code blocks with language hints
   - **Quotes/callouts:** Convert to blockquotes
   - **Footnotes:** Convert to inline references or endnotes

### Phase 2b: Extract with Docling

Use this method when docling is available or `--method docling` is specified. Docling provides native table recognition, reading order detection, and processes the entire PDF in a single pass.

1. **Run docling extraction** via Bash:

   ```python
   from docling.document_converter import DocumentConverter
   import json

   converter = DocumentConverter()
   result = converter.convert("<pdf-path>")

   # Export structured outputs
   markdown_content = result.document.export_to_markdown()
   doc_dict = result.document.export_to_dict()

   # Statistics
   page_count = len(result.document.pages)
   table_count = len(result.document.tables) if hasattr(result.document, 'tables') else 0
   image_count = len(result.document.images) if hasattr(result.document, 'images') else 0
   ```

2. **Save docling outputs** for reference:
   - `{pdf_dir}/docling_output/{stem}_docling.md` — extracted Markdown
   - `{pdf_dir}/docling_output/{stem}_docling.json` — structured JSON

3. **What docling provides automatically:**
   - Heading hierarchy preserved from document structure
   - Tables converted to Markdown with correct column alignment
   - Reading order detection (handles multi-column layouts)
   - Code blocks and formulas identified
   - Image position markers (`<!-- image -->`) at correct locations
   - List structure (bulleted and numbered) preserved
   - Apple Silicon acceleration (~0.85 sec/page on M-series Macs)

4. **Post-process the docling output:**
   - Extract metadata (title, author, date) from the first page content or PDF properties
   - Replace `<!-- image -->` markers with `[Figure X: Description]` placeholders
   - Verify table formatting is clean
   - Add any section context that docling may have missed

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
processedWith: "<read|docling>"
---

# <Document Title>

> **Source:** <PDF filename> | **Pages:** X | **Extracted:** YYYY-MM-DD | **Method:** <Read tool|docling>

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

### Example 1: Full Extraction (Auto-Detect)

```
/pdf-extract ~/Documents/cloud-migration-guide.pdf
```

Auto-detects whether docling is installed. If available, processes the entire document in one pass with native table recognition. Otherwise falls back to the Read tool.

### Example 2: Specific Pages

```
/pdf-extract ~/Documents/annual-report.pdf --pages 15-30
```

Extracts only pages 15-30 (e.g., the technical appendix). Works with both methods.

### Example 3: Tables Only

```
/pdf-extract ~/Documents/vendor-comparison.pdf --focus tables-only
```

Extracts only tables from the document. Docling is recommended for this — its native table recognition produces cleaner results than visual extraction.

### Example 4: Force Docling

```
/pdf-extract ~/Documents/complex-spec.pdf --method docling
```

Explicitly use docling for a complex document with many tables and multi-column layouts.

### Example 5: Force Read Tool

```
/pdf-extract ~/Documents/simple-memo.pdf --method read
```

Use the Read tool for a simple document where docling installation is not warranted.

---

## Technical Notes

### Docling Installation

```bash
pip install docling
```

- **Size:** ~250 MB (includes ML models)
- **Platforms:** macOS (arm64), Linux (x86_64, arm64), Windows
- **Licence:** MIT
- **First run:** ~40 seconds (model loading); subsequent runs ~0.85 sec/page

### Performance Comparison

| Metric | Read Tool | Docling |
|--------|-----------|---------|
| **Setup** | None (built-in) | `pip install docling` |
| **Speed (30-page PDF)** | ~60-90 sec (3 passes of 10 pages) | ~25 sec (single pass) |
| **Table extraction** | Visual interpretation (approximate) | Native recognition (precise) |
| **Multi-column layouts** | Manual reading order | Automatic detection |
| **Page limit** | 20 pages per Read call | No limit |
| **Image handling** | Visual descriptions | Position markers |
| **Large PDFs (100+ pages)** | Many passes, high token cost | Single pass, local processing |
| **Scanned PDFs (OCR)** | Not supported | Automatic OCR |

### When Docling Excels

- **Dense tables** — Financial reports, specification matrices, comparison tables
- **Multi-column layouts** — Academic papers, newsletters, annual reports
- **Large documents** — 50+ page specifications processed in one pass
- **Batch processing** — Process many PDFs locally without API costs
- **Scanned PDFs** — Automatic OCR (uses ocrmac on macOS)

### Error Handling

| Scenario | Read Tool | Docling |
|----------|-----------|---------|
| Password-protected PDF | Prompts for unlock | Fails (decrypt first with `qpdf`) |
| Scanned/image-only PDF | Visual interpretation | Automatic OCR |
| Very large PDF (100+ pages) | Multiple passes (high cost) | Single pass (~85 sec) |
| Corrupted PDF | Partial read | Fails with error |

---

**Invoke with:** `/pdf-extract <path-to-pdf>` to convert PDF content to structured Markdown
