---
description: Extract content from PowerPoint presentations converting slides to structured Markdown with speaker notes
model: sonnet
---

# /pptx-extract

Extract content from PowerPoint presentations, converting slides to structured Markdown with speaker notes, tables, and image references. Supports three extraction methods: basic python-pptx (zero dependencies beyond python-pptx), quick docling + python-pptx dual extraction (recommended), and visual LibreOffice rendering (highest fidelity). Preserves slide order and generates a table of contents from slide titles.

## When to Use This Skill

- Converting presentation decks into searchable Markdown notes
- Extracting key messages and data from stakeholder presentations
- Creating reference notes from training or conference slides
- Archiving presentation content in a knowledge base
- Extracting speaker notes as supplementary context
- Preserving exact slide visuals for design reviews

## Usage

```
/pptx-extract <path-to-pptx> [--include-notes] [--slides 1-10] [--method quick|visual|basic]
```

### Parameters

| Parameter        | Description                                        | Required |
|------------------|----------------------------------------------------|----------|
| `path`           | Path to the PowerPoint file                        | Yes      |
| `--include-notes`| Include speaker notes (default: yes)               | No       |
| `--slides`       | Specific slide range to extract                    | No       |
| `--method`       | Extraction method (default: `quick`)               | No       |

### Extraction Methods

| Method | When to Use | Strengths | Limitations |
|--------|-------------|-----------|-------------|
| **`basic`** | Fallback; no extra dependencies beyond python-pptx | Zero setup, works everywhere, extracts titles/bullets/tables/notes | No reading order detection, weaker table formatting, no docling enrichment |
| **`quick`** | Default; most presentations; searchable content | Fast text/table extraction via docling + speaker notes and embedded images via python-pptx, ~1 sec for 50 slides | Requires `pip install docling python-pptx` |
| **`visual`** | Design reviews; exact visual reference needed | Full slide rendering as PNG images at 200 DPI, preserves exact appearance | Requires LibreOffice + poppler, 1-2 minutes for 50 slides |

**Auto-detect behaviour:** If `--method` is not specified, check whether docling is installed. If available, use `quick`. Otherwise, fall back to `basic`.

## Instructions

### Phase 1: Assess the Presentation

1. **Verify the PPTX** exists at the specified path
   - If the user provides a partial path or just a filename, check `~/Downloads/` first
2. **Determine extraction method:**
   - If `--method basic` specified: use python-pptx only
   - If `--method quick` specified: use docling + python-pptx (fail with install instructions if not available)
   - If `--method visual` specified: use LibreOffice pipeline (fail with install instructions if not available)
   - If not specified: auto-detect (try docling import, fall back to basic)
3. **Report to user:** "This presentation has X slides. Extracting with [method]."

### Phase 2a: Extract with Basic Method (python-pptx Only)

Use this method when docling is not available or `--method basic` is specified. This is the zero-dependency fallback (beyond python-pptx itself).

```python
from pptx import Presentation
from pptx.util import Inches, Pt
import json
import sys

def extract_pptx(filepath):
    prs = Presentation(filepath)
    slides_data = []

    for i, slide in enumerate(prs.slides, 1):
        slide_data = {
            "number": i,
            "title": "",
            "content": [],
            "notes": "",
            "tables": [],
            "images": []
        }

        for shape in slide.shapes:
            if shape.has_text_frame:
                if shape.shape_id == slide.shapes.title.shape_id if slide.shapes.title else False:
                    slide_data["title"] = shape.text_frame.text
                else:
                    for para in shape.text_frame.paragraphs:
                        text = para.text.strip()
                        if text:
                            level = para.level
                            slide_data["content"].append({"text": text, "level": level})

            if shape.has_table:
                table_data = []
                for row in shape.table.rows:
                    row_data = [cell.text for cell in row.cells]
                    table_data.append(row_data)
                slide_data["tables"].append(table_data)

            if shape.shape_type == 13:  # Picture
                slide_data["images"].append(shape.name)

        if slide.has_notes_slide:
            slide_data["notes"] = slide.notes_slide.notes_text_frame.text

        slides_data.append(slide_data)

    return slides_data
```

Transform the extracted data into Markdown:

1. **Generate table of contents** from slide titles
2. **Convert each slide** to a Markdown section:
   - Slide title becomes H2 heading
   - Bullet points preserve indentation levels
   - Tables convert to Markdown tables
   - Images noted as `[Image: <name>]` placeholders
   - Speaker notes added as blockquotes below slide content
3. **Generate summary** from overall presentation themes

### Phase 2b: Extract with Quick Method (Docling + python-pptx)

Use this method when docling is available or `--method quick` is specified. This is the recommended approach — docling handles text structure and table recognition whilst python-pptx extracts speaker notes and embedded images that docling cannot access.

1. **Run dual extraction** via Bash:

   ```python
   from pathlib import Path
   from docling.document_converter import DocumentConverter
   from pptx import Presentation
   import os

   def process_pptx_quick(pptx_path, output_dir, title):
       """Quick mode: docling + python-pptx extraction"""

       # 1. Docling for text and tables
       converter = DocumentConverter()
       result = converter.convert(pptx_path)
       doc = result.document

       markdown_content = doc.export_to_markdown()
       tables_count = len(doc.tables) if hasattr(doc, 'tables') else 0
       pictures_count = len(doc.pictures) if hasattr(doc, 'pictures') else 0

       # 2. python-pptx for speaker notes and embedded images
       prs = Presentation(pptx_path)
       speaker_notes = []
       embedded_images = []

       for slide_num, slide in enumerate(prs.slides, 1):
           # Extract speaker notes
           if slide.has_notes_slide:
               notes = slide.notes_slide.notes_text_frame.text.strip()
               if notes:
                   speaker_notes.append((slide_num, notes))

           # Extract embedded images
           for shape in slide.shapes:
               if hasattr(shape, "image"):
                   img = shape.image
                   img_filename = f"{title} - Slide {slide_num:02d} - Image {len(embedded_images)+1}.{img.ext}"
                   img_path = output_dir / img_filename
                   with open(img_path, "wb") as f:
                       f.write(img.blob)
                   embedded_images.append((slide_num, img_filename))

       return {
           'markdown': markdown_content,
           'tables_count': tables_count,
           'pictures_count': pictures_count,
           'speaker_notes': speaker_notes,
           'embedded_images': embedded_images,
           'slide_count': len(prs.slides)
       }
   ```

2. **What the quick method provides:**
   - **From docling:** Heading hierarchy, text content, table recognition with correct column alignment, reading order detection for complex layouts
   - **From python-pptx:** Speaker notes (not accessible via docling), embedded images extracted as files, slide count

3. **Post-process the output:**
   - Merge docling Markdown with speaker notes sections
   - Reference extracted images at the correct slide positions
   - Verify table formatting is clean
   - Extract metadata (title, author) from the first slide or file properties

### Phase 2c: Extract with Visual Method (LibreOffice + Poppler)

Use this method when `--method visual` is specified. This renders every slide as a full PNG image, preserving exact visual appearance. Best for design reviews and presentations with complex diagrams.

1. **Check dependencies:**

   ```bash
   # Check for LibreOffice (for PPTX to PDF conversion)
   which soffice || echo "Install with: brew install --cask libreoffice"

   # Check for poppler (for PDF to image conversion)
   which pdftoppm || echo "Install with: brew install poppler"

   # Check for Python libraries
   python3 -c "import pdf2image" 2>&1 || echo "Install with: pip install pdf2image"
   ```

2. **Convert PPTX to PDF to PNG:**

   ```bash
   # Step 1: PPTX -> PDF via LibreOffice
   soffice --headless --convert-to pdf --outdir /tmp "<pptx-path>"

   # Step 2: PDF -> PNG via pdftoppm at 200 DPI
   pdftoppm -png -r 200 "/tmp/<filename>.pdf" "/tmp/<title> - Slide"
   ```

3. **Rename output files** to match convention: `<Title> - Slide 01.png`, `<Title> - Slide 02.png`, etc.

4. **Optionally extract speaker notes** via python-pptx (speaker notes are not captured by the visual pipeline, but can be appended):

   ```python
   from pptx import Presentation
   prs = Presentation(pptx_path)
   for slide_num, slide in enumerate(prs.slides, 1):
       if slide.has_notes_slide:
           notes = slide.notes_slide.notes_text_frame.text.strip()
           if notes:
               print(f"Slide {slide_num}: {notes}")
   ```

### Phase 3: Structure Output

Generate a Markdown document with:

1. **Frontmatter** — Metadata about the source presentation
2. **Summary** — AI-generated summary of the presentation
3. **Table of contents** — Generated from slide titles (basic/quick) or slide numbers (visual)
4. **Extracted content** — Clean Markdown preserving slide structure
5. **Speaker notes** — As a separate section (quick/basic) or appended per slide
6. **Key themes** — Bullet list of themes identified across multiple slides

## Output Format

### Basic / Quick Method

```markdown
---
type: Reference
title: "<Presentation Title>"
referenceType: article
created: YYYY-MM-DD
source: "<PPTX filename>"
slideCount: X
tags: [content/presentation, domain/relevant-tag]
summary: "<One-line summary>"
processedWith: "<basic|quick>"
---

# <Presentation Title>

> **Source:** <filename> | **Slides:** X | **Tables:** Y | **Images:** Z | **Extracted:** YYYY-MM-DD | **Method:** <basic|quick>

## Summary

<AI-generated summary of the presentation's key messages>

## Table of Contents

1. [Slide Title 1](#slide-1-title)
2. [Slide Title 2](#slide-2-title)
...

---

## Slide 1: <Title>

- Bullet point 1
  - Sub-bullet
- Bullet point 2

| Header A | Header B |
|----------|----------|
| Data     | Data     |

[Image: chart_sales_q4.png]

> **Speaker Notes:** Additional context from the presenter...

---

## Slide 2: <Title>

...

---

## Embedded Images

### Slide 1
![[<title> - Slide 01 - Image 1.png]]

### Slide 4
![[<title> - Slide 04 - Image 1.jpg]]
![[<title> - Slide 04 - Image 2.png]]

---

## Key Themes

- <Theme 1 identified across multiple slides>
- <Theme 2>
- <Theme 3>
```

### Visual Method

```markdown
---
type: Reference
title: "<Presentation Title>"
referenceType: article
created: YYYY-MM-DD
source: "<PPTX filename>"
slideCount: X
tags: [content/presentation, domain/relevant-tag]
summary: "<One-line summary>"
processedWith: visual
---

# <Presentation Title>

> **Source:** <filename> | **Slides:** X | **Extracted:** YYYY-MM-DD | **Method:** visual (LibreOffice)

## Slide 1

![[<title> - Slide 01.png]]

> **Speaker Notes:** <notes if extracted>

---

## Slide 2

![[<title> - Slide 02.png]]

---

...
```

## Examples

### Example 1: Full Extraction (Auto-Detect)

```
/pptx-extract ~/Documents/architecture-review-q4.pptx
```

Auto-detects whether docling is installed. If available, uses quick mode (docling + python-pptx) for fast text extraction with speaker notes and embedded images. Otherwise falls back to basic python-pptx extraction.

### Example 2: Specific Slides

```
/pptx-extract ~/Documents/strategy-deck.pptx --slides 5-15
```

Extracts only the core strategy slides (5-15). Works with all methods.

### Example 3: Content Only

```
/pptx-extract ~/Documents/training-deck.pptx --include-notes false
```

Extracts slide content without speaker notes.

### Example 4: Visual Mode for Design Review

```
/pptx-extract ~/Documents/ui-mockups.pptx --method visual
```

Renders every slide as a 200 DPI PNG image. Best for presentations with complex diagrams, charts, or visual designs where text extraction would lose important layout context.

### Example 5: Force Quick Mode

```
/pptx-extract ~/Documents/quarterly-update.pptx --method quick
```

Explicitly use docling + python-pptx for a presentation with many tables and structured content.

### Example 6: Force Basic Mode

```
/pptx-extract ~/Documents/simple-briefing.pptx --method basic
```

Use python-pptx only for a simple presentation where docling installation is not warranted.

---

## Technical Notes

### Installation

**Basic method (python-pptx only):**

```bash
pip install python-pptx
```

**Quick method (recommended):**

```bash
pip install docling python-pptx
```

- **docling size:** ~250 MB (includes ML models)
- **Platforms:** macOS (arm64), Linux (x86_64, arm64), Windows
- **Licence:** MIT
- **First run:** ~40 seconds (model loading); subsequent runs are fast

**Visual method (additional):**

```bash
# macOS
brew install --cask libreoffice
brew install poppler
pip install pdf2image

# Linux (Debian/Ubuntu)
sudo apt install libreoffice poppler-utils
pip install pdf2image
```

### Performance Comparison

| Presentation Size | Basic (python-pptx) | Quick (docling + python-pptx) | Visual (LibreOffice) |
|-------------------|---------------------|-------------------------------|----------------------|
| 10 slides         | ~0.1 sec            | ~0.2 sec                      | ~20 sec              |
| 25 slides         | ~0.2 sec            | ~0.4 sec                      | ~50 sec              |
| 50 slides         | ~0.4 sec            | ~0.8 sec                      | ~2 min               |
| 100 slides        | ~0.8 sec            | ~1.5 sec                      | ~4 min               |

### Method Comparison

| Metric | Basic | Quick | Visual |
|--------|-------|-------|--------|
| **Setup** | `pip install python-pptx` | `pip install docling python-pptx` | LibreOffice + poppler + pdf2image |
| **Speed (50 slides)** | ~0.4 sec | ~0.8 sec | ~2 min |
| **Text extraction** | Shape-by-shape parsing | Docling reading order detection | None (image only) |
| **Table extraction** | Basic cell text | Native recognition with alignment | Captured as image |
| **Speaker notes** | Yes | Yes | Optional (via python-pptx) |
| **Embedded images** | Name only | Extracted as files | Rendered in slide image |
| **Visual fidelity** | None | None | Exact slide appearance |
| **Searchable output** | Yes | Yes | No (images only) |
| **Multi-column layouts** | Manual order | Automatic detection | Preserved visually |
| **Large presentations** | Fast | Fast | Slow but faithful |

### When Each Method Excels

- **Basic** — Quick fallback when docling is not installed. Good enough for simple presentations with clear structure.
- **Quick** — Best all-round choice. Docling provides superior text and table extraction whilst python-pptx captures speaker notes and embedded images. Use for searchable archives, meeting references, and documentation.
- **Visual** — Best when exact visual appearance matters. Use for design reviews, branding presentations, or any deck where layout, colours, and typography are important.

### Error Handling

| Scenario | Basic | Quick | Visual |
|----------|-------|-------|--------|
| PPTX not found | Prompt for correct path | Prompt for correct path | Prompt for correct path |
| python-pptx missing | `pip install python-pptx` | `pip install python-pptx` | `pip install python-pptx` (for notes) |
| docling missing | N/A | `pip install docling` | N/A |
| LibreOffice missing | N/A | N/A | `brew install --cask libreoffice` |
| poppler missing | N/A | N/A | `brew install poppler` |
| Corrupted PPTX | Fails with error | Fails with error | Fails at conversion step |
| Password-protected | Cannot process (remove password first) | Cannot process (remove password first) | Cannot process (remove password first) |
| .ppt format (legacy) | Not supported (convert to .pptx first) | Not supported (convert to .pptx first) | Supported (LibreOffice handles .ppt) |

---

**Invoke with:** `/pptx-extract <path-to-pptx>` to convert presentations to structured Markdown
