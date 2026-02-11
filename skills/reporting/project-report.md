---
description: Generate project status reports from vault content using four parallel agents for tasks, meetings, risks, and timeline analysis
model: sonnet
---

# /project-report

Generate a project status report by analysing tasks, meetings, decisions, risks, and timeline data from the vault. Uses four parallel agents to gather different project dimensions simultaneously.

## When to Use This Skill

- Preparing regular project status updates
- Creating reports for steering committees
- Summarising project health for stakeholders
- Generating RAG (Red/Amber/Green) status reports
- End-of-sprint or end-of-phase reports

## Usage

```
/project-report <project-name> [--period weekly|monthly|custom] [--format rag|detailed|exec]
```

### Parameters

| Parameter    | Description                                          | Required |
|--------------|------------------------------------------------------|----------|
| `project`    | Project name or path to project note                 | Yes      |
| `--period`   | Reporting period (default: `weekly`)                 | No       |
| `--format`   | Report format (default: `rag`)                       | No       |

## Instructions

### Phase 1: Identify Project Context

1. **Find the project note** — Search for the project by name
2. **Identify related content:**
   - Tasks linked to this project
   - Meetings mentioning this project
   - ADRs related to this project
   - Workstreams under this project
3. **Determine reporting period** — Calculate date range

### Phase 2: Parallel Data Gathering — Agent Team

Launch four agents simultaneously using the Task tool.

**Agent 1: Task Status Agent** (Haiku)
Task: Analyse task status for the project
- Find all tasks linked to or mentioning the project
- Categorise by status: completed, in-progress, blocked, not started
- Calculate completion percentage
- Identify overdue tasks
- Track velocity (tasks completed per week/sprint)
Return: Task summary with completion metrics and burndown data

**Agent 2: Meeting and Decision Agent** (Haiku)
Task: Extract project-relevant meetings and decisions
- Find meetings within the reporting period that mention the project
- Extract decisions made in those meetings
- Identify action items and their status (complete/pending)
- Find ADRs created or modified in the period
Return: Meeting summary, decision log, and pending actions

**Agent 3: Risk and Issue Agent** (Sonnet)
Task: Assess project risks and issues
- Search for risks mentioned in project notes, meetings, or tasks
- Categorise: risk (potential) vs issue (realised)
- Score risks: probability x impact
- Identify new risks raised in the period
- Check mitigation status for known risks
- Assess overall project health (RAG status)
Return: Risk/issue register with RAG assessment

**Agent 4: Timeline Agent** (Haiku)
Task: Assess timeline and milestone progress
- Extract project milestones and deadlines
- Check which milestones were hit/missed in the period
- Calculate schedule variance (ahead/behind/on track)
- Identify upcoming milestones and their readiness
- Flag dependencies that could affect timeline
Return: Timeline assessment with milestone status and forecast

### Phase 3: Synthesise Project Report

Combine agent results tailored to the requested format:

**RAG format:** Concise status with colour-coded indicators
**Detailed format:** Full analysis with all dimensions
**Exec format:** One-page summary for senior stakeholders

## Output Format

```markdown
# Project Status Report: <Project Name>

**Period:** <date range> | **Date:** YYYY-MM-DD | **Status:** 🟢/🟡/🔴

## RAG Summary

| Dimension  | Status | Trend | Comment                          |
|------------|--------|-------|----------------------------------|
| Scope      | 🟢     | →     | On track, no scope changes       |
| Schedule   | 🟡     | ↓     | 1 milestone at risk              |
| Budget     | 🟢     | →     | Within budget                    |
| Risk       | 🟡     | →     | 2 high risks being mitigated     |
| Quality    | 🟢     | ↑     | Test coverage improving          |

## Key Highlights

- **Completed:** <Major achievement this period>
- **In Progress:** <Key items being worked on>
- **At Risk:** <Items that need attention>

## Task Progress

| Metric              | This Period | Overall |
|---------------------|-------------|---------|
| Completed           | X           | X/Y     |
| In Progress         | X           | —       |
| Blocked             | X           | —       |
| Overdue             | X           | —       |
| **Completion %**    | —           | **X%**  |

## Milestones

| Milestone                | Due Date   | Status    | Notes              |
|--------------------------|------------|-----------|---------------------|
| <Milestone 1>            | YYYY-MM-DD | Complete  |                     |
| <Milestone 2>            | YYYY-MM-DD | On Track  |                     |
| <Milestone 3>            | YYYY-MM-DD | At Risk   | Dependency on X     |

## Decisions Made

| Decision                    | Date       | Impact                    |
|-----------------------------|------------|---------------------------|
| <Decision>                  | YYYY-MM-DD | <What it means>           |

## Risks and Issues

### Active Risks

| Risk                    | Prob | Impact | Score | Mitigation         | Owner    |
|-------------------------|------|--------|-------|---------------------|----------|
| <Risk>                  | X/5  | X/5    | X/25  | <Action>            | <Name>   |

### Active Issues

| Issue                   | Severity | Impact                | Resolution           |
|-------------------------|----------|-----------------------|----------------------|
| <Issue>                 | High     | <What's affected>     | <Resolution plan>    |

## Actions and Next Steps

| Action                          | Owner      | Due Date    | Status  |
|---------------------------------|------------|-------------|---------|
| <Action>                        | <Name>     | YYYY-MM-DD  | Pending |

## Next Period Focus

1. <Priority 1>
2. <Priority 2>
3. <Priority 3>
```

## Examples

### Example 1: Weekly RAG Report

```
/project-report "Order Migration" --period weekly --format rag
```

### Example 2: Monthly Detailed Report

```
/project-report "Platform Modernisation" --period monthly --format detailed
```

### Example 3: Executive Summary

```
/project-report "Data Platform" --format exec
```

---

**Invoke with:** `/project-report <project-name>` to generate a project status report from vault data
