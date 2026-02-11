---
description: Extract content from PowerPoint presentations converting slides to structured Markdown with speaker notes
model: sonnet
---

# /pptx-extract

Extract content from PowerPoint presentations, converting slides to structured Markdown with speaker notes, tables, and image references. Preserves slide order and generates a table of contents from slide titles.

## When to Use This Skill

- Converting presentation decks into searchable Markdown notes
- Extracting key messages and data from stakeholder presentations
- Creating reference notes from training or conference slides
- Archiving presentation content in a knowledge base
- Extracting speaker notes as supplementary context

## Usage

```
/pptx-extract <path-to-pptx> [--include-notes] [--slides 1-10]
```

### Parameters

| Parameter        | Description                                        | Required |
|------------------|----------------------------------------------------|----------|
| `path`           | Path to the PowerPoint file                        | Yes      |
| `--include-notes`| Include speaker notes (default: yes)               | No       |
| `--slides`       | Specific slide range to extract                    | No       |

## Instructions

### Phase 1: Extract Raw Content

Use a Python script with the `python-pptx` library to extract slide content:

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

### Phase 2: Structure Content

Transform the extracted data into Markdown:

1. **Generate table of contents** from slide titles
2. **Convert each slide** to a Markdown section:
   - Slide title becomes H2 heading
   - Bullet points preserve indentation levels
   - Tables convert to Markdown tables
   - Images noted as `[Image: <name>]` placeholders
   - Speaker notes added as blockquotes below slide content
3. **Generate summary** from overall presentation themes

### Phase 3: Output

Present the structured Markdown document to the user and offer to save it.

## Output Format

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
---

# <Presentation Title>

> **Source:** <filename> | **Slides:** X | **Extracted:** YYYY-MM-DD

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

## Key Themes

- <Theme 1 identified across multiple slides>
- <Theme 2>
- <Theme 3>
```

## Examples

### Example 1: Full Extraction

```
/pptx-extract ~/Documents/architecture-review-q4.pptx
```

Extracts all slides with speaker notes and tables.

### Example 2: Specific Slides

```
/pptx-extract ~/Documents/strategy-deck.pptx --slides 5-15
```

Extracts only the core strategy slides (5-15).

### Example 3: Content Only

```
/pptx-extract ~/Documents/training-deck.pptx --include-notes false
```

Extracts slide content without speaker notes.

---

**Invoke with:** `/pptx-extract <path-to-pptx>` to convert presentations to structured Markdown
