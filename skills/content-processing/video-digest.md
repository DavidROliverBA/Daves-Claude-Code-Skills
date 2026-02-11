---
description: Batch-triage YouTube videos by relevance then deeply process the most valuable ones using parallel agents
model: sonnet
---

# /video-digest

Process a list of YouTube videos using a triage-then-process pattern. Parallel Haiku agents quickly score each video's relevance to your topic, then Sonnet agents deeply analyse only the must-watch videos. Saves time by filtering before investing in deep processing.

## When to Use This Skill

- Processing a playlist or list of conference talks
- Filtering a curated reading list of videos by relevance
- Researching a topic across multiple YouTube sources
- Creating a digest of the best content from a set of videos
- Preparing for a conference by pre-screening talk recordings

## Usage

```
/video-digest <topic> --urls <url1> <url2> ... [--threshold 7]
```

### Parameters

| Parameter      | Description                                          | Required |
|----------------|------------------------------------------------------|----------|
| `topic`        | Topic or question to evaluate relevance against      | Yes      |
| `--urls`       | List of YouTube URLs to process                      | Yes      |
| `--threshold`  | Minimum relevance score for deep processing (1-10, default: 7) | No |

## Instructions

### Phase 1: Collect Video List

Gather the list of videos from the user:
- Accept URLs directly as arguments
- Accept a file path containing URLs (one per line)
- Accept a YouTube playlist URL (extract individual video URLs)

### Phase 2: Triage — Agent Team (Parallel Haiku Agents)

Use the Triage + Selective Processing pattern. Launch parallel Haiku agents, each processing 3-5 videos.

**Agent 1-N: Video Triage Agent** (Haiku)
Task: Quick-assess relevance of assigned videos
- Fetch video title, description, and duration (via MCP or WebFetch)
- If transcript is quickly available, scan the first 5 minutes
- Score relevance to the user's topic on a 1-10 scale:
  - **8-10 (Must Watch):** Directly addresses the topic with depth
  - **5-7 (Worth Processing):** Partially relevant, some useful content
  - **1-4 (Skip):** Not relevant enough to warrant deep processing
- Categorise: must-watch, worth-processing, skip
- Write a one-line reason for the score
Return: List of `{ videoUrl, title, duration, score, category, reason }`

### Phase 3: Deep Processing — Agent Team (Selective Sonnet Agents)

Only for videos scoring at or above the threshold (default: 7):

**Agent 1-N: Deep Analysis Agent** (Sonnet)
Task: Fully analyse one must-watch video
- Fetch full transcript with timestamps
- Generate detailed summary (3-5 paragraphs)
- Extract key frameworks, concepts, and methodologies
- Identify actionable takeaways
- Note tools and resources mentioned
- Create timestamped topic index
Return: Full analysis document for one video

### Phase 4: Synthesise Digest

Combine all results:
1. **Triage summary table** — All videos with scores
2. **Deep analyses** — Full notes for must-watch videos
3. **Cross-video themes** — Common themes across analysed videos
4. **Recommended viewing order** — Prioritised by value and logical flow

## Output Format

```markdown
# Video Digest: <Topic>

**Videos assessed:** X | **Must-watch:** X | **Processed:** X

## Triage Summary

| # | Video Title              | Duration | Score | Category       | Reason               |
|---|--------------------------|----------|-------|----------------|-----------------------|
| 1 | <Title>                  | 45:00    | 9/10  | Must Watch     | <One-line reason>     |
| 2 | <Title>                  | 30:00    | 8/10  | Must Watch     | <One-line reason>     |
| 3 | <Title>                  | 20:00    | 5/10  | Worth Processing| <One-line reason>    |
| 4 | <Title>                  | 60:00    | 3/10  | Skip           | <One-line reason>     |

## Recommended Viewing Order

1. **<Title>** (Score: 9) — Start here because...
2. **<Title>** (Score: 8) — Builds on concepts from #1...

## Cross-Video Themes

### Theme 1: <Common theme across videos>
- Discussed in: Video 1 (15:30), Video 2 (08:45)
- Key insight: <synthesis>

### Theme 2: <Another theme>
...

---

## Detailed Analysis

### Video 1: <Title> (Score: 9/10)

> **URL:** <url> | **Duration:** 45:00 | **Channel:** <name>

#### Summary
<Detailed summary>

#### Key Takeaways
1. <Takeaway>
2. <Takeaway>

#### Frameworks and Concepts
- **<Framework>:** <Description>

#### Timestamped Topics
| Timestamp | Topic        | Key Point |
|-----------|-------------|-----------|
| 00:00     | <Topic>     | <Point>   |

---

### Video 2: <Title> (Score: 8/10)
...
```

## Examples

### Example 1: Conference Talk Digest

```
/video-digest "event-driven architecture patterns" --urls https://youtube.com/watch?v=abc https://youtube.com/watch?v=def https://youtube.com/watch?v=ghi
```

Triages 3 conference talks about event-driven architecture, then deeply processes the most relevant ones.

### Example 2: Lenient Threshold

```
/video-digest "kubernetes security" --urls <list> --threshold 5
```

Processes all videos scoring 5 or above (more inclusive).

### Example 3: Research Topic

```
/video-digest "AI in enterprise architecture" --urls <list-of-10-videos>
```

Triages 10 videos in parallel, deeply processes the top-scoring ones, and synthesises cross-video themes.

---

**Invoke with:** `/video-digest <topic> --urls <url1> <url2> ...` to triage and deeply process the most valuable videos
