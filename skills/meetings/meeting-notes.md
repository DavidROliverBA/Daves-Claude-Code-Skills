---
description: Create structured meeting notes with parallel post-processing agents for decision, action, and topic extraction
model: sonnet
---

# /meeting-notes

Create structured meeting notes from raw input (transcript, bullet points, or audio summary). Uses three parallel post-processing agents to extract decisions, action items, and topic summaries from the captured content.

## When to Use This Skill

- Recording meeting outcomes from notes or transcripts
- Structuring raw meeting notes into a consistent format
- Extracting decisions and action items from meeting content
- Creating searchable, linkable meeting records

## Usage

```
/meeting-notes "<meeting-title>" [--date YYYY-MM-DD] [--attendees "Name1, Name2"]
```

### Parameters

| Parameter     | Description                                     | Required |
|---------------|-------------------------------------------------|----------|
| `title`       | Meeting title                                   | Yes      |
| `--date`      | Meeting date (default: today)                   | No       |
| `--attendees` | Comma-separated attendee names                  | No       |

## Instructions

### Phase 1: Capture Raw Content

Prompt the user for meeting content in any format:
- **Transcript** — Paste a meeting transcript
- **Bullet points** — Quick notes taken during the meeting
- **Audio summary** — Summary from a voice note or recording
- **Mixed** — Any combination of the above

Also gather:
- **Attendees** — Who was in the meeting
- **Context** — Related project or workstream
- **Agenda** — What was planned to discuss (if available)

### Phase 2: Post-Processing — Agent Team

After the raw content is captured, launch three agents simultaneously using the Task tool.

**Agent 1: Decision Extractor** (Haiku)
Task: Find all decisions made during the meeting
- Scan content for decision language ("decided", "agreed", "approved", "will go with")
- For each decision: what was decided, who decided, context, and implications
- Categorise: formal (needs ADR), informal (team agreement), action (task assignment)
- Flag decisions that need follow-up documentation
Return: List of `{ decision, deciders, category, needsFollowUp }`

**Agent 2: Action Item Extractor** (Haiku)
Task: Extract all action items and assignments
- Scan content for action language ("will do", "action:", "to-do", "by next week", names followed by verbs)
- For each action: what needs to be done, who owns it, deadline (if mentioned)
- Flag actions without clear owners
- Flag actions without deadlines
Return: List of `{ action, owner, deadline, status }`

**Agent 3: Topic Summariser** (Sonnet)
Task: Summarise each discussion topic
- Identify distinct topics discussed in the meeting
- For each topic: summarise the discussion in 2-3 sentences
- Note any unresolved questions or parking lot items
- Identify topics that need follow-up in future meetings
- Link to relevant projects, systems, or concepts mentioned
Return: List of `{ topic, summary, status, relatedNotes[] }`

### Phase 3: Generate Meeting Note

Combine raw content and agent outputs into a structured meeting note.

## Output Format

```markdown
---
type: Meeting
title: "Meeting - YYYY-MM-DD <Meeting Title>"
created: YYYY-MM-DD
date: YYYY-MM-DD
attendees:
  - "[[Person Name]]"
project: "[[Project - Name]]"
tags: [activity/meeting, project/relevant-tag]
summary: "<One-line summary of meeting outcome>"
---

# Meeting - YYYY-MM-DD <Meeting Title>

## Attendees

- [[Person 1]]
- [[Person 2]]

## Agenda

1. <Topic 1>
2. <Topic 2>
3. <Topic 3>

## Discussion

### <Topic 1>

<2-3 sentence summary of discussion>

- Key point discussed
- Alternative considered
- Conclusion reached

### <Topic 2>

<Summary>

## Decisions

| # | Decision                          | Deciders        | Follow-up Needed |
|---|-----------------------------------|-----------------|------------------|
| 1 | <What was decided>                | <Who decided>   | Yes — Create ADR |
| 2 | <What was decided>                | <Who decided>   | No               |

## Action Items

| # | Action                            | Owner           | Deadline    | Status  |
|---|-----------------------------------|-----------------|-------------|---------|
| 1 | <What needs to be done>           | [[Person]]      | YYYY-MM-DD  | Pending |
| 2 | <What needs to be done>           | [[Person]]      | YYYY-MM-DD  | Pending |

## Parking Lot

- <Topics deferred to future meetings>

## Related Notes

- [[Project - Relevant Project]]
- [[ADR - Relevant Decision]]
```

## Examples

### Example 1: From Transcript

```
/meeting-notes "Sprint Planning" --date 2026-02-10 --attendees "Alice, Bob, Charlie"
```

User pastes transcript; agents extract decisions, actions, and topic summaries.

### Example 2: From Bullet Points

```
/meeting-notes "Architecture Review"
```

User provides bullet-point notes; agents structure them into a full meeting record.

### Example 3: Quick Capture

```
/meeting-notes "1:1 with Manager" --attendees "Manager Name"
```

Minimal input for a quick meeting capture with decision and action extraction.

---

**Invoke with:** `/meeting-notes "<title>"` then paste or type the meeting content
