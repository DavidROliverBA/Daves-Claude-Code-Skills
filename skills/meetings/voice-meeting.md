---
description: Process voice meeting recordings or transcripts into structured meeting notes with speech-to-text correction
model: sonnet
---

# /voice-meeting

Process voice meeting recordings or voice-to-text transcripts into structured meeting notes. Applies speech-to-text corrections for common misrecognitions and generates structured output with decisions and actions.

## When to Use This Skill

- Processing transcripts from voice recording apps
- Cleaning up speech-to-text output from meeting recordings
- Converting voice notes into structured meeting records
- Processing dictated meeting summaries

## Usage

```
/voice-meeting "<meeting-title>" [--source transcript|voicenote|dictation] [--corrections path/to/corrections.md]
```

### Parameters

| Parameter       | Description                                          | Required |
|-----------------|------------------------------------------------------|----------|
| `title`         | Meeting title                                        | Yes      |
| `--source`      | Source type (default: `transcript`)                   | No       |
| `--corrections` | Path to custom speech-to-text corrections file       | No       |

## Instructions

### Phase 1: Ingest Transcript

1. **Accept the raw transcript** from the user — this may come from:
   - Voice recording app transcript
   - Dictation software output
   - Manual transcription with errors
2. **Load correction rules** — If `--corrections` provided, load custom corrections. Otherwise, apply standard speech-to-text corrections:
   - Common homophones (their/there, your/you're)
   - Proper noun corrections (specific to the user's domain)
   - Technical term corrections
3. **Ask for context:**
   - Date and time of the meeting
   - Attendees (the transcript may not identify speakers)
   - Related project or topic

### Phase 2: Clean and Correct

Apply corrections systematically:

1. **Proper nouns** — Fix misrecognised names, system names, and project names
2. **Technical terms** — Fix misrecognised technical vocabulary
3. **Sentence boundaries** — Fix run-on sentences and paragraph breaks
4. **Speaker attribution** — If speakers are identified, format as dialogue
5. **Filler removal** — Remove "um", "uh", "like", "you know" etc.
6. **Grammar** — Fix obvious grammatical errors from speech patterns

### Phase 3: Structure into Meeting Note

Follow the same structure as `/meeting-notes`:

1. **Extract topics** — Identify distinct discussion topics from the conversation flow
2. **Extract decisions** — Find decision language
3. **Extract actions** — Find action assignments
4. **Generate summary** — Summarise the overall meeting
5. **Add metadata** — Date, attendees, project, tags

## Output Format

```markdown
---
type: Meeting
title: "Meeting - YYYY-MM-DD <Meeting Title>"
created: YYYY-MM-DD
date: YYYY-MM-DD
attendees:
  - "[[Person Name]]"
source: voice-transcript
tags: [activity/meeting, project/relevant-tag]
summary: "<One-line summary>"
---

# Meeting - YYYY-MM-DD <Meeting Title>

> **Source:** Voice transcript | **Corrections applied:** X

## Attendees

- [[Person 1]]
- [[Person 2]]

## Discussion

### <Topic 1>

<Cleaned and structured discussion summary>

### <Topic 2>

<Cleaned and structured discussion summary>

## Decisions

| # | Decision            | Deciders     |
|---|---------------------|-------------|
| 1 | <Decision>          | <Who>       |

## Action Items

| # | Action              | Owner        | Deadline    |
|---|---------------------|-------------|-------------|
| 1 | <Action>            | [[Person]]  | YYYY-MM-DD  |

## Transcript Corrections Applied

| Original               | Corrected To           | Reason             |
|------------------------|------------------------|--------------------|
| <misrecognised text>   | <corrected text>       | Proper noun        |
```

## Examples

### Example 1: Voice App Transcript

```
/voice-meeting "Sprint Retrospective" --source transcript
```

User pastes transcript from a voice recording app; skill cleans and structures it.

### Example 2: With Custom Corrections

```
/voice-meeting "Architecture Review" --corrections .claude/rules/transcript-corrections.md
```

Applies domain-specific corrections from a custom corrections file.

### Example 3: Dictated Summary

```
/voice-meeting "Quick Sync" --source dictation
```

Processes a dictated meeting summary into structured notes.

---

**Invoke with:** `/voice-meeting "<title>"` then paste the raw transcript
