# Skills Reference

Quick reference for all available skills, organised by category.

## Architecture

| Skill | Command | Model | Agent Team | Description |
|-------|---------|-------|------------|-------------|
| [ADR](../skills/architecture/adr.md) | `/adr` | Sonnet | No | Create Architecture Decision Records |
| [Impact Analysis](../skills/architecture/impact-analysis.md) | `/impact-analysis` | Sonnet | 4 agents (fan-out) | Analyse cascading change impact |
| [Scenario Compare](../skills/architecture/scenario-compare.md) | `/scenario-compare` | Sonnet | 3 agents (fan-out) | Compare architectural scenarios |
| [NFR Capture](../skills/architecture/nfr-capture.md) | `/nfr-capture` | Sonnet | No | Capture non-functional requirements |
| [NFR Review](../skills/architecture/nfr-review.md) | `/nfr-review` | Sonnet | 3 agents (fan-out) | Review NFRs for quality |
| [Architecture Report](../skills/architecture/architecture-report.md) | `/architecture-report` | Sonnet | 5 agents (fan-out) | Generate architecture reports |
| [Cost Analysis](../skills/architecture/cost-analysis.md) | `/cost-analysis` | Sonnet | 3 agents (fan-out) | Analyse and optimise costs |
| [Dependency Graph](../skills/architecture/dependency-graph.md) | `/dependency-graph` | Sonnet | No | Visualise system dependencies |

## Content Processing

| Skill | Command | Model | Agent Team | Description |
|-------|---------|-------|------------|-------------|
| [PDF Extract](../skills/content-processing/pdf-extract.md) | `/pdf-extract` | Sonnet | No | Extract content from PDFs |
| [PPTX Extract](../skills/content-processing/pptx-extract.md) | `/pptx-extract` | Sonnet | No | Extract content from PowerPoint |
| [YouTube Analyze](../skills/content-processing/youtube-analyze.md) | `/youtube-analyze` | Sonnet | No | Analyse YouTube video transcripts |
| [Video Digest](../skills/content-processing/video-digest.md) | `/video-digest` | Sonnet | N agents (triage) | Batch-triage and process videos |
| [Weblink](../skills/content-processing/weblink.md) | `/weblink` | Haiku | No | Capture web pages |
| [Article](../skills/content-processing/article.md) | `/article` | Haiku | No | Quick-capture articles |
| [Book Notes](../skills/content-processing/book-notes.md) | `/book-notes` | Sonnet | 3 agents (fan-out) | Create book notes with extraction |
| [Document Extract](../skills/content-processing/document-extract.md) | `/document-extract` | Sonnet | No | Extract from any document format |

## Diagramming

| Skill | Command | Model | Agent Team | Description |
|-------|---------|-------|------------|-------------|
| [Diagram](../skills/diagramming/diagram.md) | `/diagram` | Sonnet | No | Generate architecture diagrams |
| [C4 Diagram](../skills/diagramming/c4-diagram.md) | `/c4-diagram` | Sonnet | No | Generate C4 diagrams |
| [Diagram Review](../skills/diagramming/diagram-review.md) | `/diagram-review` | Sonnet | 4 agents (fan-out) | Review diagram quality |

## Vault Health

| Skill | Command | Model | Agent Team | Description |
|-------|---------|-------|------------|-------------|
| [Quality Report](../skills/vault-health/quality-report.md) | `/quality-report` | Sonnet | 5 agents (fan-out) | Vault quality metrics |
| [Broken Links](../skills/vault-health/broken-links.md) | `/broken-links` | Sonnet | 3 agents (fan-out) | Find broken references |
| [Orphan Finder](../skills/vault-health/orphan-finder.md) | `/orphan-finder` | Sonnet | 4 agents (fan-out) | Detect disconnected notes |
| [Auto-Tag](../skills/vault-health/auto-tag.md) | `/auto-tag` | Haiku | N agents (batch) | Batch auto-tag notes |
| [Auto-Summary](../skills/vault-health/auto-summary.md) | `/auto-summary` | Haiku | N agents (batch) | Batch-generate summaries |
| [Link Checker](../skills/vault-health/link-checker.md) | `/link-checker` | Haiku | N agents (batch) | Validate external URLs |

## Scoring

| Skill | Command | Model | Agent Team | Description |
|-------|---------|-------|------------|-------------|
| [Score Document](../skills/scoring/score-document.md) | `/score-document` | Sonnet | 4 agents (fan-out) | Score documents against rubrics |
| [Exec Summary](../skills/scoring/exec-summary.md) | `/exec-summary` | Sonnet | No | Generate executive summaries |

## Reporting

| Skill | Command | Model | Agent Team | Description |
|-------|---------|-------|------------|-------------|
| [Weekly Summary](../skills/reporting/weekly-summary.md) | `/weekly-summary` | Sonnet | 5 agents (fan-out) | Generate weekly reports |
| [Project Report](../skills/reporting/project-report.md) | `/project-report` | Sonnet | 4 agents (fan-out) | Generate project status reports |

## Meetings

| Skill | Command | Model | Agent Team | Description |
|-------|---------|-------|------------|-------------|
| [Meeting Notes](../skills/meetings/meeting-notes.md) | `/meeting-notes` | Sonnet | 3 agents (fan-out) | Create structured meeting notes |
| [Voice Meeting](../skills/meetings/voice-meeting.md) | `/voice-meeting` | Sonnet | No | Process voice transcripts |
| [Email Capture](../skills/meetings/email-capture.md) | `/email-capture` | Haiku | No | Capture emails as notes |

## Knowledge

| Skill | Command | Model | Agent Team | Description |
|-------|---------|-------|------------|-------------|
| [Summarize](../skills/knowledge/summarize.md) | `/summarize` | Sonnet | No | Summarise notes at any depth |
| [Find Related](../skills/knowledge/find-related.md) | `/find-related` | Sonnet | No | Discover related content |
| [Find Decisions](../skills/knowledge/find-decisions.md) | `/find-decisions` | Sonnet | No | Extract decisions from vault |
| [Timeline](../skills/knowledge/timeline.md) | `/timeline` | Sonnet | No | Generate event timelines |
| [Skill Creator](../skills/knowledge/skill-creator.md) | `/skill-creator` | Sonnet | No | Generate new skill files |

## Agent Team Summary

| Pattern | Skills Using It | Total Agents | Cost Profile |
|---------|----------------|--------------|--------------|
| Fan-Out/Fan-In | 13 skills | 3-5 per skill | Medium |
| Batch Processing | 3 skills | N (scales with input) | Low |
| Triage + Selective | 1 skill | N + selective | Low-Medium |
| No agents | 17 skills | 0 | Lowest |

## Model Usage Summary

| Model | Skills | Use Case |
|-------|--------|----------|
| Haiku | 5 (primary) + many as sub-agents | Quick capture, batch processing |
| Sonnet | 29 (primary) | Analysis, synthesis, scoring |
| Opus | 0 (primary) | Reserved for deep reasoning tasks |
