---
description: Generate weekly summary reports from vault content using five parallel agents to gather activities, tasks, meetings, decisions, and project progress
model: sonnet
---

# /weekly-summary

Generate a weekly summary report by analysing daily notes, tasks, meetings, and project updates from the past week. Uses five parallel Haiku agents to gather different data dimensions, then a Sonnet coordinator synthesises the report.

## When to Use This Skill

- End-of-week activity summaries
- Preparing for Monday stand-ups or status meetings
- Personal productivity reviews
- Generating weekly reports for line managers
- Tracking progress across multiple workstreams

## Usage

```
/weekly-summary [--week YYYY-WNN] [--focus projects|tasks|meetings|all]
```

### Parameters

| Parameter  | Description                                           | Required |
|------------|-------------------------------------------------------|----------|
| `--week`   | ISO week to report on (default: current week)         | No       |
| `--focus`  | Report focus area (default: `all`)                    | No       |

## Instructions

### Phase 1: Determine Date Range

1. **Calculate date range** for the specified week (Monday to Friday)
2. **Identify source files:**
   - Daily notes: `Daily/YYYY/Daily - YYYY-MM-DD.md`
   - Meetings: `Meetings/YYYY/Meeting - YYYY-MM-DD *.md`
   - Tasks: `Tasks/Task - *.md` (check modification dates)
   - Projects: `Projects/Project - *.md`
   - ADRs: `ADRs/ADR - *.md`

### Phase 2: Parallel Data Gathering — Agent Team

Launch five agents simultaneously using the Task tool.

**Agent 1: Daily Notes Collector** (Haiku)
Task: Extract highlights from daily notes
- Read all daily notes in the date range
- Extract: accomplishments, blockers, notes, and reflections
- Identify recurring themes or concerns
Return: Day-by-day highlights and themes

**Agent 2: Tasks Analyst** (Haiku)
Task: Analyse task progress during the week
- Find tasks created this week
- Find tasks completed this week
- Find tasks that are overdue
- Find tasks that changed status
- Calculate: created, completed, in-progress, blocked counts
Return: Task summary with status changes and overdue items

**Agent 3: Meetings Collector** (Haiku)
Task: Summarise meetings held this week
- Read all meeting notes in the date range
- Extract: attendees, key decisions, action items
- Identify follow-up actions that are still pending
Return: Meeting summary table with decisions and actions

**Agent 4: Decisions Tracker** (Haiku)
Task: Track decisions made this week
- Search ADRs created or modified this week
- Search meeting notes for decision keywords
- Search daily notes for decision references
- Categorise: formal (ADR), informal (meeting), personal (daily)
Return: Decisions log with context and status

**Agent 5: Project Progress Tracker** (Haiku)
Task: Assess project progress this week
- Read project notes modified this week
- Check for milestone completions
- Identify new risks or issues raised
- Check project status changes
Return: Project progress summary per project

### Phase 3: Synthesise Weekly Report

Combine all agent results into a cohesive weekly summary:

1. **Week highlights** — Top 3-5 accomplishments
2. **Activity metrics** — Meetings attended, tasks completed, decisions made
3. **Detailed sections** — From each agent's findings
4. **Next week preview** — Upcoming meetings, deadlines, and priorities

## Output Format

```markdown
# Weekly Summary: Week N (DD Mon - DD Mon YYYY)

## Week Highlights

1. **<Most significant accomplishment>**
2. **<Second accomplishment>**
3. **<Third accomplishment>**

## Activity Metrics

| Metric              | Count |
|---------------------|-------|
| Meetings attended   | X     |
| Tasks completed     | X     |
| Tasks created       | X     |
| Decisions made      | X     |
| ADRs written        | X     |

## Daily Highlights

### Monday
- <Key activities and outcomes>

### Tuesday
- <Key activities and outcomes>

...

## Meetings This Week

| Date       | Meeting                  | Key Decision / Outcome          |
|------------|--------------------------|----------------------------------|
| YYYY-MM-DD | <Meeting Title>          | <Decision or key outcome>        |

## Decisions Made

| Decision                    | Context     | Type    | Status   |
|-----------------------------|-------------|---------|----------|
| <Decision>                  | <Meeting>   | Formal  | Accepted |

## Task Progress

| Status      | Count | Notes                          |
|-------------|-------|--------------------------------|
| Completed   | X     | <Notable completions>          |
| In Progress | X     | <Key items being worked on>    |
| Blocked     | X     | <Blockers>                     |
| Created     | X     | <New items added>              |
| Overdue     | X     | <Items past deadline>          |

## Project Updates

### <Project Name>
**Status:** On track / At risk / Blocked
- <Progress update>
- <Key milestone or issue>

## Next Week Preview

### Upcoming Meetings
- <Meeting 1> — YYYY-MM-DD

### Deadlines
- <Deadline 1> — YYYY-MM-DD

### Priorities
1. <Priority 1>
2. <Priority 2>
```

## Examples

### Example 1: Current Week Summary

```
/weekly-summary
```

### Example 2: Previous Week

```
/weekly-summary --week 2026-W06
```

### Example 3: Projects Focus

```
/weekly-summary --focus projects
```

---

**Invoke with:** `/weekly-summary` to generate a comprehensive week-in-review report
