# Dave's Claude Code Skills

A curated collection of [Claude Code](https://claude.ai/code) skills for software architecture, knowledge management, and engineering. Drop these `.md` files into your `.claude/skills/` directory and invoke them as slash commands.

**34 skills** across **8 categories** — many using **agent teams** (parallel sub-agents) for faster, more thorough execution.

## Skills

### Architecture (8 skills)

Skills for documenting decisions, analysing change impact, comparing scenarios, and managing non-functional requirements.

| Skill | Command | Agent Team | Description |
|-------|---------|------------|-------------|
| [ADR](skills/architecture/adr.md) | `/adr` | — | Create Architecture Decision Records with structured context, rationale, and consequences |
| [Impact Analysis](skills/architecture/impact-analysis.md) | `/impact-analysis` | 4 agents | Analyse cascading impact across technical, organisational, financial, and risk dimensions |
| [Scenario Compare](skills/architecture/scenario-compare.md) | `/scenario-compare` | 3 agents | Compare architectural scenarios with cost, timeline, complexity, and risk analysis |
| [NFR Capture](skills/architecture/nfr-capture.md) | `/nfr-capture` | — | Capture non-functional requirements with measurable acceptance criteria |
| [NFR Review](skills/architecture/nfr-review.md) | `/nfr-review` | 3 agents | Review NFRs for completeness, measurability, and feasibility |
| [Architecture Report](skills/architecture/architecture-report.md) | `/architecture-report` | 5 agents | Generate comprehensive architecture reports for governance and audit |
| [Cost Analysis](skills/architecture/cost-analysis.md) | `/cost-analysis` | 3 agents | Analyse costs and identify optimisation opportunities |
| [Dependency Graph](skills/architecture/dependency-graph.md) | `/dependency-graph` | — | Visualise system dependencies with colour-coded criticality |

### Content Processing (8 skills)

Skills for extracting and structuring content from PDFs, presentations, videos, web pages, articles, and books.

| Skill | Command | Agent Team | Description |
|-------|---------|------------|-------------|
| [PDF Extract](skills/content-processing/pdf-extract.md) | `/pdf-extract` | — | Extract structured content from PDFs preserving tables and formatting |
| [PPTX Extract](skills/content-processing/pptx-extract.md) | `/pptx-extract` | — | Convert PowerPoint slides to structured Markdown with speaker notes |
| [YouTube Analyze](skills/content-processing/youtube-analyze.md) | `/youtube-analyze` | — | Analyse videos via transcripts with timestamped summaries and takeaways |
| [Video Digest](skills/content-processing/video-digest.md) | `/video-digest` | N agents | Batch-triage videos by relevance, then deeply process the best ones |
| [Weblink](skills/content-processing/weblink.md) | `/weblink` | — | Quick web page capture with AI summary |
| [Article](skills/content-processing/article.md) | `/article` | — | Quick article capture with summary and relevance scoring |
| [Book Notes](skills/content-processing/book-notes.md) | `/book-notes` | 3 agents | Create book notes with parallel concept, framework, and action extraction |
| [Document Extract](skills/content-processing/document-extract.md) | `/document-extract` | — | Extract from any format (PDF, DOCX, HTML, CSV) with auto-detection |

### Diagramming (3 skills)

Skills for generating and reviewing architecture diagrams. Based on graph drawing research (Purchase et al.) and real-world C4 modelling experience.

| Skill | Command | Agent Team | Description |
|-------|---------|------------|-------------|
| [Diagram](skills/diagramming/diagram.md) | `/diagram` | — | Generate architecture diagrams in multiple formats (C4, system landscape, data flow, AWS) |
| [C4 Diagram](skills/diagramming/c4-diagram.md) | `/c4-diagram` | — | Specialised C4 diagram generation with three output formats and antipattern avoidance |
| [Diagram Review](skills/diagramming/diagram-review.md) | `/diagram-review` | 4 agents | Analyse existing diagrams for readability and architecture quality |

### Vault Health (6 skills)

Skills for measuring and improving the quality of a Markdown knowledge vault.

| Skill | Command | Agent Team | Description |
|-------|---------|------------|-------------|
| [Quality Report](skills/vault-health/quality-report.md) | `/quality-report` | 5 agents | Comprehensive quality metrics (readability, links, metadata, structure, freshness) |
| [Broken Links](skills/vault-health/broken-links.md) | `/broken-links` | 3 agents | Find broken wiki-links, heading anchors, and missing attachments |
| [Orphan Finder](skills/vault-health/orphan-finder.md) | `/orphan-finder` | 4 agents | Detect disconnected notes and suggest connections |
| [Auto-Tag](skills/vault-health/auto-tag.md) | `/auto-tag` | N agents | Batch auto-tag notes with hierarchical tags |
| [Auto-Summary](skills/vault-health/auto-summary.md) | `/auto-summary` | N agents | Batch-generate one-line summaries for notes |
| [Link Checker](skills/vault-health/link-checker.md) | `/link-checker` | N agents | Validate external URLs for dead links |

### Scoring (2 skills)

Skills for evaluating and scoring documents against rubrics.

| Skill | Command | Agent Team | Description |
|-------|---------|------------|-------------|
| [Score Document](skills/scoring/score-document.md) | `/score-document` | 4 agents | Score documents against customisable rubrics with evidence-based ratings |
| [Exec Summary](skills/scoring/exec-summary.md) | `/exec-summary` | — | Generate executive summaries for senior stakeholders |

### Reporting (2 skills)

Skills for generating periodic status reports from vault content.

| Skill | Command | Agent Team | Description |
|-------|---------|------------|-------------|
| [Weekly Summary](skills/reporting/weekly-summary.md) | `/weekly-summary` | 5 agents | Generate weekly activity reports from daily notes, tasks, and meetings |
| [Project Report](skills/reporting/project-report.md) | `/project-report` | 4 agents | Generate RAG project status reports |

### Meetings (3 skills)

Skills for capturing and structuring meeting content.

| Skill | Command | Agent Team | Description |
|-------|---------|------------|-------------|
| [Meeting Notes](skills/meetings/meeting-notes.md) | `/meeting-notes` | 3 agents | Create structured meeting notes with decision and action extraction |
| [Voice Meeting](skills/meetings/voice-meeting.md) | `/voice-meeting` | — | Process voice transcripts with speech-to-text correction |
| [Email Capture](skills/meetings/email-capture.md) | `/email-capture` | — | Capture emails as structured vault notes |

### Knowledge (5 skills)

Skills for discovering, connecting, and visualising knowledge.

| Skill | Command | Agent Team | Description |
|-------|---------|------------|-------------|
| [Summarize](skills/knowledge/summarize.md) | `/summarize` | — | Summarise notes with configurable depth and audience targeting |
| [Find Related](skills/knowledge/find-related.md) | `/find-related` | — | Discover related content via semantic and structural analysis |
| [Find Decisions](skills/knowledge/find-decisions.md) | `/find-decisions` | — | Extract and catalogue decisions across a date range |
| [Timeline](skills/knowledge/timeline.md) | `/timeline` | — | Generate visual timelines from vault events |
| [Skill Creator](skills/knowledge/skill-creator.md) | `/skill-creator` | — | Generate new Claude Code skill files from templates |

## Agent Teams

Many skills use **agent teams** — parallel sub-agents that analyse different dimensions simultaneously for faster, more thorough results. Three orchestration patterns are used:

| Pattern | Description | Skills |
|---------|-------------|--------|
| **Fan-Out/Fan-In** | 3-5 agents analyse different dimensions in parallel, results synthesised | 13 skills |
| **Batch Processing** | Same operation on many items, divided into parallel batches | 3 skills |
| **Triage + Selective** | Fast agents score items, then only high-value items get deep processing | 1 skill |

See the [Agent Teams Guide](docs/agent-teams-guide.md) for detailed patterns and model selection guidance. See the [Skills Reference](docs/skills-reference.md) for a complete quick-reference table.

## Examples

Worked examples with prompts, outputs, and explanations of what makes each diagram good (or bad).

### Diagramming Examples

| Example | What It Shows |
|---------|---------------|
| [Declaration Order](examples/diagramming/01-declaration-order.md) | Why element declaration order is the single most important factor for diagram readability |
| [C4 Context Diagram](examples/diagramming/02-c4-context-diagram.md) | How to create a clean Level 1 C4 diagram |
| [C4 Container Diagram](examples/diagramming/03-c4-container-diagram.md) | How to create a Level 2 C4 diagram with system boundaries and technology labels |
| [C4 Component Diagram](examples/diagramming/04-c4-component-diagram.md) | How to diagram internal components at C4 Level 3 |
| [Real-World Example](examples/diagramming/05-real-world-example.md) | Complete Context + Container diagrams for a real AI-powered platform |

### Example Screenshots

| | | |
|---|---|---|
| ![Bad order](examples/diagramming/images/03-bad-declaration-order.png) | ![Good order](examples/diagramming/images/04-good-declaration-order.png) | ![Context](examples/diagramming/images/05-good-context-diagram.png) |
| Bad declaration order | Good declaration order | C4 Context |
| ![Container](examples/diagramming/images/02-good-structured-container.png) | ![Component](examples/diagramming/images/06-good-component-diagram.png) | ![Real-world](examples/diagramming/images/07-dispax-context.png) |
| C4 Container | C4 Component | Real-world Context |

## Installation

1. Copy the skill files you want into your project's `.claude/skills/` directory:

```bash
# Copy all skills from a category
mkdir -p .claude/skills
cp skills/architecture/*.md .claude/skills/
cp skills/content-processing/*.md .claude/skills/

# Or copy individual skills
cp skills/architecture/adr.md .claude/skills/
cp skills/vault-health/quality-report.md .claude/skills/
```

2. Invoke them in Claude Code:

```
/adr Use Event-Driven Integration for Orders
/impact-analysis Migrate database from Oracle to PostgreSQL
/quality-report --type ADR
/weekly-summary
```

## Key Concepts

### Diagram Skills

Built on three key insights from graph drawing research:

1. **Declaration order controls layout.** The Dagre (Mermaid) and Sugiyama (PlantUML) algorithms position elements based on where they appear in the code. Declare elements in reading order — actors left, data stores right.

2. **Edge crossings are the strongest predictor of comprehension difficulty.** Research by Helen Purchase showed reducing crossings improves reader accuracy by 30-40%. Always set an explicit crossing target.

3. **Gestalt proximity overrides colour.** Elements placed close together are perceived as related, regardless of styling. Use subgraphs and boundaries to group related components.

### Agent Team Skills

Built on three orchestration principles:

1. **Fan-Out/Fan-In for multi-dimensional analysis.** When evaluating something from multiple angles (technical, financial, risk), run agents in parallel and synthesise results.

2. **Batch Processing for scale.** When the same operation applies to many items, divide into batches and process in parallel with cost-effective models (Haiku).

3. **Triage before deep processing.** When only some items are worth deep analysis, use fast agents to score first, then invest in deep processing only for high-value items.

## Documentation

| Document | Description |
|----------|-------------|
| [Agent Teams Guide](docs/agent-teams-guide.md) | How to use parallel sub-agents in skills |
| [Skills Reference](docs/skills-reference.md) | Quick-reference table of all skills |
| [Blog Post](docs/blog-post.md) | Theory behind the diagramming skills |

## Contributing

Contributions welcome. To add a new skill:

1. Create a `.md` file in the appropriate `skills/<category>/` directory
2. Follow the skill template (YAML frontmatter, When to Use, Usage, Instructions, Examples)
3. Use the `/skill-creator` skill to generate the boilerplate
4. Add a worked example in `examples/<category>/`
5. Update this README

## Licence

MIT
