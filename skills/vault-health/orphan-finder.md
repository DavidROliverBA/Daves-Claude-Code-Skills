---
description: Detect orphaned notes with no incoming or outgoing links and suggest connections using parallel agents
model: sonnet
---

# /orphan-finder

Detect orphaned notes — files with no incoming or outgoing wiki-links — across a Markdown vault. Uses four parallel agents to scan different note categories and a Sonnet agent to suggest meaningful connections for discovered orphans.

## When to Use This Skill

- Finding disconnected notes that should be linked into the knowledge graph
- Identifying notes that may be candidates for archiving or deletion
- Improving vault interconnectedness and discoverability
- Post-migration cleanup to reconnect moved or renamed notes

## Usage

```
/orphan-finder [--scope path/to/folder] [--action report|suggest|connect]
```

### Parameters

| Parameter  | Description                                          | Required |
|------------|------------------------------------------------------|----------|
| `--scope`  | Folder to scan (default: entire vault)               | No       |
| `--action` | What to do with orphans (default: `suggest`)         | No       |

## Instructions

### Phase 1: Build Link Graph

1. **Scan all Markdown files** — Build a complete list of notes
2. **Parse all wiki-links** — For each note, extract all `[[target]]` references
3. **Build backlink index** — Map each note to the list of notes that link to it
4. **Identify orphans** — Notes with 0 outgoing links AND 0 incoming links
5. **Identify near-orphans** — Notes with only 1 link (either in or out)

### Phase 2: Parallel Orphan Scanning — Agent Team

Launch four agents simultaneously using the Task tool, each scanning a category.

**Agent 1: Entity Orphan Scanner** (Haiku)
Task: Find orphaned entity notes (System, Organisation, Person, DataAsset, Location, Department)
- Check each entity note for incoming and outgoing links
- Cross-reference against meeting notes, projects, and ADRs
- Flag entities that are referenced in prose but not wiki-linked
Return: List of orphaned entities with context

**Agent 2: Node Orphan Scanner** (Haiku)
Task: Find orphaned knowledge notes (Concept, Pattern, Reference, Research, Framework, Tool)
- Check each node note for incoming and outgoing links
- Check for keyword matches in other notes (note may be referenced without wiki-link)
- Flag notes with relevant content but no connections
Return: List of orphaned nodes with potential keyword matches

**Agent 3: Event Orphan Scanner** (Haiku)
Task: Find orphaned event notes (Meeting, Project, Task, ADR, etc.)
- Check each event note for incoming and outgoing links
- Cross-reference dates and attendees with other events
- Flag events that mention entities or concepts without wiki-linking them
Return: List of orphaned events with context

**Agent 4: Connection Suggester** (Sonnet)
Task: Suggest meaningful links for all orphans found by Agents 1-3
- For each orphaned note, read its content
- Search the vault for semantically related notes
- Suggest specific wiki-link additions with rationale
- Prioritise suggestions by relevance and confidence
- Group suggestions by effort: easy (obvious links), medium (contextual), hard (requires note edits)
Return: Map of `orphanFilename → [{ targetNote, reason, confidence, effort }]`

**Note:** Agent 4 runs after Agents 1-3 complete, using their combined output as input.

### Phase 3: Generate Report

Compile results with suggested connections.

## Output Format

```markdown
# Orphan Finder Report

**Date:** YYYY-MM-DD | **Scope:** <scope> | **Notes Scanned:** X

## Summary

| Category   | Total Notes | Orphans | Near-Orphans | % Orphaned |
|------------|-------------|---------|--------------|------------|
| Entities   | X           | X       | X            | X%         |
| Nodes      | X           | X       | X            | X%         |
| Events     | X           | X       | X            | X%         |
| **Total**  | **X**       | **X**   | **X**        | **X%**     |

## Orphaned Notes

### Entities (X orphans)

| Note                        | Suggested Connection                | Confidence |
|-----------------------------|-------------------------------------|------------|
| `System - OrderDB.md`       | → `[[Project - Orders]]`           | High       |
| `People/Jane Smith.md`      | → `[[Meeting - 2026-01-15 ...]]`   | Medium     |

### Nodes (X orphans)

| Note                        | Suggested Connection                | Confidence |
|-----------------------------|-------------------------------------|------------|
| `Concept - CQRS.md`         | → `[[ADR - Event Sourcing]]`       | High       |

### Events (X orphans)

| Note                        | Suggested Connection                | Confidence |
|-----------------------------|-------------------------------------|------------|
| `Meeting - 2026-01-20...`   | → `[[Project - Migration]]`        | High       |

## Quick Fix List

### Easy Fixes (High confidence, minimal edits)
1. In `<note>`, add link to `[[<target>]]` in relatedTo frontmatter
2. ...

### Medium Fixes (Moderate confidence, some context needed)
1. In `<note>`, mention `[[<target>]]` in the body text
2. ...

## Archival Candidates

Notes that are orphaned AND stale (>12 months old) — consider archiving:
- `<note>` — Last modified YYYY-MM-DD
```

## Examples

### Example 1: Full Vault Scan

```
/orphan-finder
```

### Example 2: Connect Mode

```
/orphan-finder --action connect
```

Automatically adds suggested connections (high-confidence only) to orphaned notes.

### Example 3: Scoped Scan

```
/orphan-finder --scope Projects/
```

---

**Invoke with:** `/orphan-finder` to detect and reconnect orphaned notes
