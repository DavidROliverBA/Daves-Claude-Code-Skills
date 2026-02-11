---
description: Discover related content across the vault using semantic and structural analysis
model: sonnet
---

# /find-related

Discover related content across a Markdown vault by analysing semantic similarity, shared tags, backlinks, and temporal proximity. Suggests connections that may not be obvious from direct links alone.

## When to Use This Skill

- Finding notes related to a topic you're researching
- Discovering connections between seemingly unrelated content
- Building context before writing a new note
- Identifying related decisions, meetings, or projects
- Expanding the `relatedTo` field for a specific note

## Usage

```
/find-related <note-path-or-topic> [--max 15] [--method semantic|structural|all]
```

### Parameters

| Parameter   | Description                                          | Required |
|-------------|------------------------------------------------------|----------|
| `source`    | Path to a note or a topic/keyword to search for     | Yes      |
| `--max`     | Maximum related notes to return (default: 15)        | No       |
| `--method`  | Discovery method (default: `all`)                    | No       |

## Instructions

### Phase 1: Analyse Source

1. **If note path:** Read the note and extract:
   - Title, type, tags, and summary
   - Key concepts and terms from the body
   - Existing `relatedTo` links
   - Outgoing wiki-links
2. **If topic/keyword:** Use it directly as the search seed

### Phase 2: Multi-Signal Search

Search for related content using multiple signals:

**Signal 1: Tag Overlap**
- Find notes sharing 2+ tags with the source
- Weight: higher score for more shared tags
- Exclude common tags (e.g., `status/active`)

**Signal 2: Backlink Analysis**
- Find notes that link to the same targets as the source
- Notes linking to similar targets are likely related
- Weight: higher for more shared link targets

**Signal 3: Keyword/Semantic Match**
- Extract key terms from the source note
- Search vault for notes containing these terms
- Weight: higher for more term matches

**Signal 4: Temporal Proximity**
- For events (meetings, tasks): find other events within ±7 days
- For projects: find meetings and tasks during the project period
- Weight: lower than other signals (proximity != relevance)

**Signal 5: Type Affinity**
- ADRs relate to other ADRs, Projects, and Systems
- Meetings relate to Projects, People, and Tasks
- Concepts relate to Patterns, Frameworks, and ADRs
- Weight: bonus for expected type pairings

### Phase 3: Rank and Present

1. **Combine signals** into a weighted relevance score per candidate
2. **Remove duplicates** and already-linked notes
3. **Sort by relevance** score (highest first)
4. **Group by relationship type:**
   - Already linked (in `relatedTo`)
   - Strong match (high confidence)
   - Possible match (medium confidence)
   - Weak match (low confidence, may be worth investigating)

## Output Format

```markdown
# Related Content: <Source Note/Topic>

**Source:** <note title or topic> | **Results:** X notes found

## Strong Matches (X)

| Note                           | Type    | Relevance | Signals                    |
|--------------------------------|---------|-----------|----------------------------|
| [[<Note Title>]]              | ADR     | 92%       | Tags: 3, Keywords: 5, Links: 2 |
| [[<Note Title>]]              | Concept | 88%       | Tags: 2, Keywords: 4       |

## Possible Matches (X)

| Note                           | Type    | Relevance | Signals                    |
|--------------------------------|---------|-----------|----------------------------|
| [[<Note Title>]]              | Meeting | 65%       | Temporal, Keywords: 2      |

## Suggested Link Additions

To improve connectivity, consider adding these to the source note's `relatedTo`:

```yaml
relatedTo:
  - "[[Strong Match 1]]"
  - "[[Strong Match 2]]"
```

## Discovery Insights

- <Interesting connection found, e.g., "3 ADRs share the same theme but aren't cross-linked">
```

## Examples

### Example 1: Find Content Related to a Note

```
/find-related "ADR - Event Sourcing.md"
```

### Example 2: Find Content by Topic

```
/find-related "data integration patterns" --max 20
```

### Example 3: Structural Analysis Only

```
/find-related "Project - Migration.md" --method structural
```

---

**Invoke with:** `/find-related <note-or-topic>` to discover related content across your vault
