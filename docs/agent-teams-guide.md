# Agent Teams Guide

How to use parallel sub-agents in Claude Code skills for faster, more thorough execution.

## What Are Agent Teams?

Agent teams are groups of parallel sub-agents launched via Claude Code's `Task` tool. Each agent runs independently with its own context, processes a specific piece of work, and returns structured results. A coordinator (the main skill) then synthesises all results into a unified output.

Agent teams are useful when:
- Multiple independent analyses can run simultaneously
- The same operation needs to run on many items
- Items need scoring before selective deep processing

## Orchestration Patterns

### Pattern 1: Fan-Out/Fan-In

The most common pattern. 3-5 agents analyse different dimensions of the same input in parallel, then results are synthesised.

```
Coordinator (Sonnet/Opus)
  ├── Agent 1 (Haiku/Sonnet) — Dimension A analysis
  ├── Agent 2 (Haiku/Sonnet) — Dimension B analysis
  ├── Agent 3 (Haiku/Sonnet) — Dimension C analysis
  └── Agent 4 (Haiku/Sonnet) — Dimension D analysis
       │
       ▼
  Synthesis Phase (Coordinator combines all results)
```

**When to use:** Evaluating something from multiple angles — impact analysis, quality reports, architecture reviews.

**Skills using this pattern:**
- `/impact-analysis` — 4 agents (technical, organisational, financial, risk)
- `/scenario-compare` — 3 agents (cost, technical, risk/timeline)
- `/quality-report` — 5 agents (readability, links, metadata, structure, freshness)
- `/architecture-report` — 5 agents (inventory, integration, decisions, risk, finance)
- `/nfr-review` — 3 agents (completeness, measurability, feasibility)
- `/cost-analysis` — 3 agents (infrastructure, licensing, operational)
- `/score-document` — 4 agents (section scorers)
- `/weekly-summary` — 5 agents (daily, tasks, meetings, decisions, projects)
- `/project-report` — 4 agents (tasks, meetings, risks, timeline)
- `/meeting-notes` — 3 agents (decisions, actions, topics)
- `/book-notes` — 3 agents (concepts, frameworks, actions)

### Pattern 2: Batch Processing

Used when the same operation needs to run on many items. Items are divided into equal batches and processed in parallel.

```
Coordinator
  ├── Agent 1 (Haiku) — Process items 1-20
  ├── Agent 2 (Haiku) — Process items 21-40
  ├── Agent 3 (Haiku) — Process items 41-60
  └── Agent N (Haiku) — Process items (N-1)*20+1 to N*20
```

**When to use:** Tagging, summarising, validating, or transforming many notes at once.

**Skills using this pattern:**
- `/auto-tag` — N agents, 15-20 notes per batch
- `/auto-summary` — N agents, 15-20 notes per batch
- `/link-checker` — N agents, 10-15 URLs per batch

### Pattern 3: Triage + Selective Processing

A two-phase pattern. Fast agents score items first, then only high-value items get deep processing.

```
Phase 1: Triage (Haiku agents in parallel)
  ├── Agent 1 — Score batch 1 (quick assessment)
  ├── Agent 2 — Score batch 2
  └── Agent N — Score batch N
       │
       ▼ Filter: only items scoring above threshold
Phase 2: Deep Processing (Sonnet agents for high-value items only)
  ├── Agent 1 — Deep analysis of item A
  └── Agent 2 — Deep analysis of item B
```

**When to use:** Processing a large list where only some items are worth deep analysis.

**Skills using this pattern:**
- `/video-digest` — Haiku triages videos by relevance, Sonnet deeply analyses must-watch ones

## Model Selection Guide

| Agent Purpose                     | Model  | Rationale                              |
|-----------------------------------|--------|----------------------------------------|
| File scanning, pattern matching   | Haiku  | Fast, cheap, isolated context          |
| Batch processing (tagging, summarising) | Haiku | Cost-effective at scale          |
| Content analysis, scoring         | Sonnet | Needs reasoning but not deep thinking  |
| Complex synthesis, architecture   | Sonnet | Good balance for most analysis         |
| Deep architectural reasoning      | Opus   | Only when extended thinking is needed  |

## Cost Considerations

| Model  | Input Cost  | Output Cost | Ideal For                        |
|--------|-------------|-------------|----------------------------------|
| Haiku  | ~$1/MTok    | ~$5/MTok    | High-volume, simple tasks        |
| Sonnet | ~$3/MTok    | ~$15/MTok   | Most analytical work             |
| Opus   | ~$15/MTok   | ~$75/MTok   | Complex reasoning (use sparingly)|

**Example cost for a 5-agent quality report:**
- 5 Sonnet agents reading ~50 notes each ≈ ~100k tokens input, ~20k output per agent
- Total: ~500k input + ~100k output ≈ $1.50 + $1.50 = ~$3.00

**Example cost for batch tagging 100 notes:**
- 5 Haiku agents processing 20 notes each ≈ ~30k tokens input, ~5k output per agent
- Total: ~150k input + ~25k output ≈ $0.15 + $0.13 = ~$0.28

## Writing Agent Definitions

Each agent definition should include:

```markdown
**Agent N: <Name>** (<Model>)
Task: <One-sentence purpose>
- <Step 1 — specific action>
- <Step 2 — specific action>
- <Step 3 — specific action>
Return: <What this agent produces — structured data format>
```

**Good agent definition:**
```markdown
**Agent 2: Risk Assessor** (Sonnet)
Task: Identify and score risks across all dimensions
- Identify technical risks (integration failures, data loss)
- Identify organisational risks (skill gaps, key person dependency)
- Score each risk: Probability (1-5) × Impact (1-5) = Risk Score
- Propose mitigations for all risks scoring 12 or above
Return: Risk register with probability, impact, score, and mitigations
```

**Bad agent definition:**
```markdown
**Agent 2: Risk Agent** (Sonnet)
Task: Find risks
- Look at stuff
- Score things
Return: Risk info
```

The difference: specific steps and a defined return format allow the agent to work autonomously and produce consistent, combinable output.

## MCP Tool Limitation

MCP tools (Notion, YouTube, Diagrams) are **not available** inside sub-agents launched via the Task tool. If a skill needs MCP tools, the coordinator must call them before launching agents, then pass the results as context.

**Workaround pattern:**
1. Coordinator fetches data via MCP tools
2. Coordinator passes fetched data as context to sub-agents
3. Sub-agents analyse the pre-fetched data

## Debugging Agent Teams

If an agent team skill produces poor results:

1. **Check agent scope** — Is each agent's task clearly defined and bounded?
2. **Check model selection** — Is the agent using the right model for its complexity?
3. **Check return format** — Is the expected return format specified clearly?
4. **Check context size** — Are agents receiving too much or too little context?
5. **Run one agent at a time** — Test each agent individually to isolate issues
