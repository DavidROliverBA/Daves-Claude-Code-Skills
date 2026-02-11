# Skills Reference

Quick-reference card for all 37 skills across 8 categories. For detailed agent team patterns, see the [Agent Teams Guide](agent-teams-guide.md).

---

## Architecture (8 skills)

| Skill | Command | Agents | Model | Description |
|-------|---------|--------|-------|-------------|
| [ADR](../skills/architecture/adr.md) | `/adr` | — | Sonnet | Create Architecture Decision Records with context, rationale, and consequences |
| [Impact Analysis](../skills/architecture/impact-analysis.md) | `/impact-analysis` | 4 | Sonnet | Analyse cascading change impact across technical, organisational, financial, and risk dimensions |
| [Scenario Compare](../skills/architecture/scenario-compare.md) | `/scenario-compare` | 3 | Sonnet | Compare architectural scenarios with cost, timeline, complexity, and risk analysis |
| [NFR Capture](../skills/architecture/nfr-capture.md) | `/nfr-capture` | — | Sonnet | Capture non-functional requirements with measurable acceptance criteria (ISO 25010) |
| [NFR Review](../skills/architecture/nfr-review.md) | `/nfr-review` | 3 | Sonnet | Review NFRs for completeness, measurability, and feasibility |
| [Architecture Report](../skills/architecture/architecture-report.md) | `/architecture-report` | 5 | Sonnet | Generate comprehensive architecture reports for governance and audit |
| [Cost Analysis](../skills/architecture/cost-analysis.md) | `/cost-analysis` | 3 | Sonnet | Analyse infrastructure, licensing, and operational costs; identify savings |
| [Dependency Graph](../skills/architecture/dependency-graph.md) | `/dependency-graph` | — | Sonnet | Visualise system dependencies with colour-coded criticality in Mermaid |

## Content Processing (8 skills)

| Skill | Command | Agents | Model | Description |
|-------|---------|--------|-------|-------------|
| [PDF Extract](../skills/content-processing/pdf-extract.md) | `/pdf-extract` | — | Sonnet | Extract structured content from PDFs preserving headings, tables, and formatting |
| [PPTX Extract](../skills/content-processing/pptx-extract.md) | `/pptx-extract` | — | Sonnet | Convert PowerPoint slides to structured Markdown with speaker notes |
| [YouTube Analyze](../skills/content-processing/youtube-analyze.md) | `/youtube-analyze` | — | Sonnet | Analyse videos via transcripts with timestamped summaries and key takeaways |
| [Video Digest](../skills/content-processing/video-digest.md) | `/video-digest` | N | Sonnet | Batch-triage videos by relevance (Haiku), then deeply process the best (Sonnet) |
| [Weblink](../skills/content-processing/weblink.md) | `/weblink` | — | Haiku | Quick web page capture with AI-generated summary |
| [Article](../skills/content-processing/article.md) | `/article` | — | Haiku | Quick article capture with summary, key quotes, and relevance scoring |
| [Book Notes](../skills/content-processing/book-notes.md) | `/book-notes` | 3 | Sonnet | Create book notes with parallel concept, framework, and action extraction |
| [Document Extract](../skills/content-processing/document-extract.md) | `/document-extract` | — | Sonnet | Extract from any format (PDF, DOCX, HTML, CSV) with auto-detection |

## Diagramming (3 skills)

| Skill | Command | Agents | Model | Description |
|-------|---------|--------|-------|-------------|
| [Diagram](../skills/diagramming/diagram.md) | `/diagram` | — | Sonnet | Generate architecture diagrams (C4, system landscape, data flow, AWS) |
| [C4 Diagram](../skills/diagramming/c4-diagram.md) | `/c4-diagram` | — | Sonnet | Specialised C4 diagram generation: Mermaid C4, flowchart LR, or PlantUML |
| [Diagram Review](../skills/diagramming/diagram-review.md) | `/diagram-review` | 4 | Sonnet | Analyse existing diagrams for readability and architecture quality |

For the theory behind the diagramming skills, see [Why Your AI-Generated Diagrams Look Terrible](blog-post.md).

## Vault Health (6 skills)

| Skill | Command | Agents | Model | Description |
|-------|---------|--------|-------|-------------|
| [Quality Report](../skills/vault-health/quality-report.md) | `/quality-report` | 5 | Sonnet | Comprehensive quality metrics: readability, links, metadata, structure, freshness |
| [Broken Links](../skills/vault-health/broken-links.md) | `/broken-links` | 3 | Sonnet | Find broken wiki-links, heading anchors, and missing attachment references |
| [Orphan Finder](../skills/vault-health/orphan-finder.md) | `/orphan-finder` | 4 | Sonnet | Detect disconnected notes and suggest meaningful connections |
| [Auto-Tag](../skills/vault-health/auto-tag.md) | `/auto-tag` | N | Haiku | Batch auto-tag notes with hierarchical tags from content analysis |
| [Auto-Summary](../skills/vault-health/auto-summary.md) | `/auto-summary` | N | Haiku | Batch-generate one-line `summary` fields for notes missing them |
| [Link Checker](../skills/vault-health/link-checker.md) | `/link-checker` | N | Haiku | Validate external HTTP/HTTPS URLs for dead links, redirects, and timeouts |

## Scoring (2 skills)

| Skill | Command | Agents | Model | Description |
|-------|---------|--------|-------|-------------|
| [Score Document](../skills/scoring/score-document.md) | `/score-document` | 4 | Sonnet | Score documents against customisable rubrics (0-3, 0-5, or 0-10) with evidence |
| [Exec Summary](../skills/scoring/exec-summary.md) | `/exec-summary` | — | Sonnet | Generate executive summaries tailored to CEO, CTO, board, or PM audiences |

## Reporting (2 skills)

| Skill | Command | Agents | Model | Description |
|-------|---------|--------|-------|-------------|
| [Weekly Summary](../skills/reporting/weekly-summary.md) | `/weekly-summary` | 5 | Sonnet | Generate weekly activity reports from daily notes, tasks, meetings, and projects |
| [Project Report](../skills/reporting/project-report.md) | `/project-report` | 4 | Sonnet | Generate RAG project status reports with tasks, risks, and timeline assessment |

## Meetings (3 skills)

| Skill | Command | Agents | Model | Description |
|-------|---------|--------|-------|-------------|
| [Meeting Notes](../skills/meetings/meeting-notes.md) | `/meeting-notes` | 3 | Sonnet | Create structured meeting notes with decision and action item extraction |
| [Voice Meeting](../skills/meetings/voice-meeting.md) | `/voice-meeting` | — | Sonnet | Process voice transcripts with speech-to-text correction into structured notes |
| [Email Capture](../skills/meetings/email-capture.md) | `/email-capture` | — | Haiku | Capture important emails as structured vault notes with action item extraction |

## Knowledge (5 skills)

| Skill | Command | Agents | Model | Description |
|-------|---------|--------|-------|-------------|
| [Summarize](../skills/knowledge/summarize.md) | `/summarize` | — | Sonnet | Summarise notes with configurable depth (one-liner, paragraph, page) and audience |
| [Find Related](../skills/knowledge/find-related.md) | `/find-related` | — | Sonnet | Discover related content via tag overlap, backlinks, keywords, and temporal proximity |
| [Find Decisions](../skills/knowledge/find-decisions.md) | `/find-decisions` | — | Sonnet | Extract and catalogue formal and informal decisions across a date range |
| [Timeline](../skills/knowledge/timeline.md) | `/timeline` | — | Sonnet | Generate visual timelines (Mermaid Gantt, table, or list) from vault events |
| [Skill Creator](../skills/knowledge/skill-creator.md) | `/skill-creator` | — | Sonnet | Generate new Claude Code skill files with agent team boilerplate |

---

## Agent Team Summary

### By Pattern

| Pattern | Skills | Agents per Skill | Sub-Agent Model | Typical Speedup |
|---------|--------|------------------|-----------------|-----------------|
| **Fan-Out/Fan-In** | 13 | 3-5 (fixed) | Sonnet or Haiku | 3-4× |
| **Batch Processing** | 3 | N (scales with input) | Haiku | 4-9× (scales with batch count) |
| **Triage + Selective** | 1 | N + selective | Haiku → Sonnet | 2-3× time, 60-80% cost saving |
| **No agents** | 20 | 0 | — | 1× (sequential) |

### Skills by Agent Count

| Agents | Skills |
|--------|--------|
| 0 | `/adr`, `/nfr-capture`, `/dependency-graph`, `/pdf-extract`, `/pptx-extract`, `/youtube-analyze`, `/weblink`, `/article`, `/document-extract`, `/diagram`, `/c4-diagram`, `/exec-summary`, `/voice-meeting`, `/email-capture`, `/summarize`, `/find-related`, `/find-decisions`, `/timeline`, `/skill-creator` |
| 3 | `/scenario-compare`, `/nfr-review`, `/cost-analysis`, `/broken-links`, `/book-notes`, `/meeting-notes` |
| 4 | `/impact-analysis`, `/score-document`, `/project-report`, `/diagram-review`, `/orphan-finder` |
| 5 | `/quality-report`, `/architecture-report`, `/weekly-summary` |
| N | `/video-digest`, `/auto-tag`, `/auto-summary`, `/link-checker` |

---

## Quick Installation

### All Skills (Every Category)

```bash
mkdir -p .claude/skills
cp skills/**/*.md .claude/skills/
```

### By Category

```bash
# Architecture — ADRs, impact analysis, NFRs, cost analysis
cp skills/architecture/*.md .claude/skills/

# Content Processing — PDF, PPTX, YouTube, web, books
cp skills/content-processing/*.md .claude/skills/

# Diagramming — C4 diagrams, diagram review
cp skills/diagramming/*.md .claude/skills/

# Vault Health — quality reports, broken links, auto-tag
cp skills/vault-health/*.md .claude/skills/

# Scoring — document scoring, executive summaries
cp skills/scoring/*.md .claude/skills/

# Reporting — weekly summaries, project status reports
cp skills/reporting/*.md .claude/skills/

# Meetings — meeting notes, voice transcripts, email capture
cp skills/meetings/*.md .claude/skills/

# Knowledge — summarise, find related, timelines, skill creator
cp skills/knowledge/*.md .claude/skills/
```

### Individual Skills

```bash
# Just the skills you need
cp skills/architecture/adr.md .claude/skills/
cp skills/vault-health/quality-report.md .claude/skills/
cp skills/content-processing/youtube-analyze.md .claude/skills/
```

### Verify Installation

After copying, invoke any skill in Claude Code:

```
/adr Use Event-Driven Integration for Orders
/quality-report --type ADR
/youtube-analyze https://www.youtube.com/watch?v=example
```

---

## Model Cost Guide

### Per-Token Pricing

| Model | Input | Output | Cache Read | Ideal For |
|-------|-------|--------|------------|-----------|
| **Haiku** | $1.00/MTok | $5.00/MTok | $0.10/MTok | High-volume batch work, quick captures, triage scoring |
| **Sonnet** | $3.00/MTok | $15.00/MTok | $0.30/MTok | Analysis, synthesis, scoring — most skill work |
| **Opus** | $15.00/MTok | $75.00/MTok | $1.50/MTok | Deep architectural reasoning, extended thinking |

### Cost per Typical Operation

| Operation | Model | Input Tokens | Output Tokens | Est. Cost |
|-----------|-------|-------------|---------------|-----------|
| Tag 1 note | Haiku | ~3k | ~500 | $0.006 |
| Tag 100 notes (5 batch agents) | Haiku | ~150k | ~25k | $0.28 |
| Summarise 1 note | Sonnet | ~5k | ~1k | $0.03 |
| Quality report (50 notes, 5 agents) | Sonnet | ~500k | ~100k | $3.00 |
| Impact analysis (4 agents) | Sonnet | ~200k | ~60k | $1.50 |
| Score document (4 agents) | Sonnet | ~300k | ~80k | $2.10 |
| Triage 20 videos (Haiku) + deep 4 (Sonnet) | Mixed | ~260k | ~50k | $1.31 |

### When to Use Each Model

| Criterion | Use Haiku | Use Sonnet | Use Opus |
|-----------|-----------|------------|----------|
| **Task complexity** | Simple, repetitive | Analytical, comparative | Deep reasoning |
| **Input volume** | 50+ items | 1-50 items | 1-5 items |
| **Reasoning needed** | Pattern matching | Weighing trade-offs | Extended thinking |
| **Cost sensitivity** | High (batch work) | Moderate | Low (quality matters most) |
| **Speed priority** | Fastest response | Balanced | Quality over speed |
| **Skills (coordinator)** | `/weblink`, `/article`, `/email-capture`, `/auto-tag`, `/auto-summary`, `/link-checker` | All other skills | Custom deep-analysis skills |
| **Skills (sub-agent)** | Batch processing, triage scoring, file scanning | Fan-out analysis, content scoring | Rare — only for complex synthesis |

### Cost Optimisation Tips

1. **Use Haiku for batch agents** — Tagging 100 notes with Haiku costs $0.28 vs $1.40 with Sonnet
2. **Use the triage pattern** — Score 20 items with Haiku ($0.11), deeply process only 4 with Sonnet ($1.20) = $1.31 vs $6.50 for all 20
3. **Benefit from prompt caching** — Structure prompts with static instructions first; 90% cache savings after 2+ requests
4. **Limit fan-out agents to 3-5** — Beyond 5, coordinator overhead negates speedup gains
5. **Choose the right coordinator model** — Skills with simple synthesis can use Sonnet; only use Opus when the synthesis requires deep reasoning

---

## Further Reading

- [Agent Teams Guide](agent-teams-guide.md) — Comprehensive guide to agent team patterns, best practices, and anti-patterns
- [Blog Post](blog-post.md) — The graph drawing research behind the diagramming skills
- [`/skill-creator`](../skills/knowledge/skill-creator.md) — Generate new skill files with the standard template
