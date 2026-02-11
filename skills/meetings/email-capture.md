---
description: Capture email content into structured vault notes with metadata and action item extraction
model: haiku
---

# /email-capture

Capture email content into a structured vault note with metadata, summary, and extracted action items. Quick, single-step capture for important emails that need to be tracked.

## When to Use This Skill

- Archiving important emails for future reference
- Capturing email decisions and commitments
- Tracking action items from email threads
- Creating a searchable record of email communications

## Usage

```
/email-capture --from "<sender>" --subject "<subject>" [--date YYYY-MM-DD]
```

### Parameters

| Parameter   | Description                                   | Required |
|-------------|-----------------------------------------------|----------|
| `--from`    | Email sender name                             | Yes      |
| `--subject` | Email subject line                            | Yes      |
| `--date`    | Email date (default: today)                   | No       |
| `--to`      | Email recipient(s)                            | No       |
| `--thread`  | Is this part of a thread? (default: no)       | No       |

## Instructions

### Phase 1: Capture Content

1. **Prompt user** to paste the email body
2. **Extract metadata:**
   - From, To, CC (if mentioned)
   - Date and time
   - Subject line
   - Thread context (if reply or forward)
3. **Identify key elements:**
   - Decisions or commitments made
   - Action items assigned
   - Deadlines mentioned
   - Attachments referenced
   - People mentioned

### Phase 2: Generate Email Note

Create a structured email note with extracted metadata and content.

## Output Format

```markdown
---
type: Email
title: "Email - <From/To> - <Subject>"
created: YYYY-MM-DD
date: YYYY-MM-DD
from: "[[Person Name]]"
to:
  - "[[Person Name]]"
tags: [activity/email, project/relevant-tag]
summary: "<One-line summary>"
---

# Email - <From/To> - <Subject>

> **From:** [[Sender]] | **To:** [[Recipient]] | **Date:** YYYY-MM-DD

## Summary

<1-2 sentence summary of the email's purpose and key message>

## Content

<Cleaned email body content>

## Action Items

| # | Action              | Owner        | Deadline    |
|---|---------------------|-------------|-------------|
| 1 | <Action>            | [[Person]]  | YYYY-MM-DD  |

## Decisions / Commitments

- <Any decisions or commitments made in the email>

## Related Notes

- [[Project - Relevant Project]]
```

## Examples

### Example 1: Important Decision Email

```
/email-capture --from "Head of Architecture" --subject "Approved: Cloud Migration Approach"
```

### Example 2: Action-Heavy Email

```
/email-capture --from "Project Manager" --subject "Sprint 5 Actions" --date 2026-02-10
```

### Example 3: External Vendor Email

```
/email-capture --from "Vendor Contact" --subject "Contract Renewal Terms"
```

---

**Invoke with:** `/email-capture --from "<sender>" --subject "<subject>"` then paste the email content
