# Memory System for Claude Code

A three-layer memory system that gives Claude Code persistent cross-session learning. Each layer serves a different purpose — use them together for comprehensive memory.

## Architecture

| Layer | Storage | Purpose | Scope |
|-------|---------|---------|-------|
| **Auto-memory** (built-in) | `~/.claude/projects/*/memory/MEMORY.md` | Free-form session learnings, user preferences, quick patterns | Per-project, shared across worktrees |
| **MCP memory** | MCP `memory` server graph (JSONL) | Typed structured entities with relationships | Cross-project, searchable |
| **Session hooks** | Automated Python hooks | Commit-level data capture at session end | Per-session, automated |

## Components

### Scripts (`scripts/memory/`)

**`memory-search.js`** — Unified search across active MCP memory and markdown archive.

```bash
node scripts/memory/memory-search.js "<query>"                      # Search both active + archive
node scripts/memory/memory-search.js "<query>" --type LessonLearned # Filter by entity type
node scripts/memory/memory-search.js --stats                        # Show memory statistics
node scripts/memory/memory-search.js --list-types                   # Show entity type breakdown
```

**`memory-prune.js`** — Prune ephemeral entities (`SessionSummary`, `SkillOutcome`) while archiving to markdown.

```bash
node scripts/memory/memory-prune.js --dry-run    # Preview what would be pruned
node scripts/memory/memory-prune.js --keep 10    # Keep last 10 of each type
```

### Hooks (`hooks/memory/`)

**`session-learner.py`** — Post-session notification hook that captures structured session data.

- Reads commit messages and file paths from the last 2 hours
- Classifies sessions as `apply` (actionable), `capture` (worth tracking), or `dismiss` (skip)
- Infers skill usage from file path patterns
- Writes JSON manifests for next session to process
- Prunes old manifests (keeps last 20)
- Cleans up stale temp files from parallel subagents

**`session-summary.py`** — Post-session notification hook that appends session log to daily notes.

- Writes git-based session summary (commits, file changes) to today's daily note
- Creates daily note from template if missing
- Updates AGENDA.md session notes section

### Configuration

Both hooks use `Path(__file__).resolve().parent.parent.parent` to locate the vault root, so they work from any installation path. No hardcoded paths.

## Entity Types

The MCP memory graph uses typed entities. Only these types should be created:

| Type | Purpose | Auto-created |
|------|---------|-------------|
| `LessonLearned` | Bugs, fixes, workarounds discovered | Manual (Claude) |
| `Convention` | Established patterns and conventions | Manual (Claude) |
| `KnowledgeGap` | Identified unknowns or missing docs | Manual (Claude) |
| `PersonInsight` | People's roles, preferences, context | Manual (Claude) |
| `Runbook` | Step-by-step procedures | Manual (Claude) |
| `SessionSummary` | What happened in a session | Auto (session-learner) |
| `SkillOutcome` | Skills executed and results | Auto (session-learner) |
| `VaultHealth` | Health check snapshots | Auto (session-learner) |

## Size Management

- **Cap:** ~200 entities total
- **Max observations:** 15 per entity (condense or split if approaching)
- **Auto-pruned:** `SessionSummary` and `SkillOutcome` (keep last 20)
- **Never pruned:** `LessonLearned`, `Convention`, `KnowledgeGap`
- **Promotion path:** Pattern observed 3+ times → promote to `.claude/rules/` file
- **Archival:** Pruned entities preserved in `Memory/memory-archive.md`

## Setup

### 1. MCP Memory Server

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/claude-code-mcp-memory"]
    }
  }
}
```

### 2. Hook Registration

Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/session-learner.py"
          },
          {
            "type": "command",
            "command": "python3 .claude/hooks/session-summary.py"
          }
        ]
      }
    ]
  }
}
```

### 3. Memory Rule

Copy `docs/ambient-memory-rules.md` to `.claude/rules/ambient-memory.md` in your project. This tells Claude when and how to write to MCP memory during sessions.

### 4. Directory Setup

Create the directories the system expects:

```bash
mkdir -p Memory .claude/memory
```

## Self-Improvement Loop

The memory system enables a continuous improvement cycle:

1. **Observe** — Claude notices patterns during work (inline via MCP memory)
2. **Capture** — `session-learner.py` records at session end (automated)
3. **Triage** — Classifications: `apply` (fix now), `capture` (track), `dismiss` (skip)
4. **Promote** — Patterns recurring 3+ times graduate to `.claude/rules/` files

## Related

- [Claude Code MCP Memory](https://github.com/anthropics/claude-code) — Built-in MCP memory server
- `hooks/memory/session-learner.py` — Session capture hook
- `hooks/memory/session-summary.py` — Daily note session log hook
- `scripts/memory/memory-search.js` — Search utility
- `scripts/memory/memory-prune.js` — Pruning utility
