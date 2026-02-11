---
description: Find broken wiki-links, heading anchors, and missing attachments using three parallel scanning agents
model: sonnet
---

# /broken-links

Find broken wiki-links, heading anchor references, and missing attachment references across a Markdown vault. Uses three parallel agents to scan different link types simultaneously.

## When to Use This Skill

- Regular vault maintenance to catch broken references
- After renaming or moving notes
- After bulk migrations or reorganisations
- Before publishing or sharing vault content
- Identifying dead links that need cleanup

## Usage

```
/broken-links [--scope path/to/folder] [--fix-mode report|interactive|auto]
```

### Parameters

| Parameter    | Description                                           | Required |
|--------------|-------------------------------------------------------|----------|
| `--scope`    | Folder to scan (default: entire vault)                | No       |
| `--fix-mode` | How to handle broken links (default: `report`)        | No       |

## Instructions

### Phase 1: Build File Index

1. **Scan all Markdown files** in scope using Glob
2. **Build a set of valid note names** (filenames without `.md` extension)
3. **Build a heading index** — Parse each file for headings to validate `[[Note#heading]]` links
4. **Build an attachment index** — List all files in the attachments folder(s)
5. **Divide files into three batches** for parallel processing

### Phase 2: Parallel Link Scanning — Agent Team

Launch three agents simultaneously using the Task tool.

**Agent 1: Wiki-Link Scanner** (Haiku)
Task: Find broken `[[wiki-links]]`
- Scan all Markdown files for `[[...]]` patterns
- For each link, check if the target note exists in the file index
- Handle aliases: `[[Note|Display Text]]` — check `Note` exists
- Ignore links to headings within the same file
- Categorise: broken (target doesn't exist), redirectable (close match found)
Return: List of `{ file, line, brokenLink, suggestion }`

**Agent 2: Heading Anchor Scanner** (Haiku)
Task: Find broken `[[Note#heading]]` links
- Scan all Markdown files for `[[...#...]]` patterns
- For each, verify the target note exists AND the heading exists within it
- Handle heading formats: spaces, capitalisation, special characters
- Note: Obsidian normalises headings (lowercase, hyphens for spaces)
Return: List of `{ file, line, brokenLink, targetNote, missingHeading }`

**Agent 3: Attachment Scanner** (Haiku)
Task: Find missing `![[attachment]]` references
- Scan all Markdown files for `![[...]]` patterns (embedded content)
- Also check `![alt](path)` style image references
- Verify each referenced file exists in the attachment index
- Check for common issues: wrong extension, wrong folder, URL-encoded names
Return: List of `{ file, line, brokenRef, expectedPath }`

### Phase 3: Compile Report

Combine agent results:

1. **Deduplicate** across agents
2. **Categorise** by severity: critical (content broken), warning (reference broken), info (stale link)
3. **Suggest fixes** for each broken link:
   - Close matches (fuzzy matching on filename)
   - Possible renames (if a note was recently renamed)
   - Removal suggestion (if the target was deleted)
4. **Generate summary statistics**

If `--fix-mode interactive`: Present each broken link with suggested fix and ask user to confirm.
If `--fix-mode auto`: Apply all high-confidence fixes automatically.

## Output Format

```markdown
# Broken Links Report

**Date:** YYYY-MM-DD | **Scope:** <scope> | **Files Scanned:** X

## Summary

| Link Type         | Total Found | Broken | Fix Available |
|-------------------|-------------|--------|---------------|
| Wiki-links        | X           | X      | X             |
| Heading anchors   | X           | X      | X             |
| Attachments       | X           | X      | X             |
| **Total**         | **X**       | **X**  | **X**         |

## Broken Wiki-Links (X found)

| File                  | Line | Broken Link              | Suggested Fix           |
|-----------------------|------|--------------------------|-------------------------|
| <filename>            | X    | `[[Old Note Name]]`      | `[[New Note Name]]`     |
| <filename>            | X    | `[[Deleted Note]]`       | Remove link             |

## Broken Heading Anchors (X found)

| File                  | Line | Broken Link                    | Issue                  |
|-----------------------|------|--------------------------------|------------------------|
| <filename>            | X    | `[[Note#Old Heading]]`         | Heading renamed        |

## Missing Attachments (X found)

| File                  | Line | Missing Reference              | Suggestion             |
|-----------------------|------|--------------------------------|------------------------|
| <filename>            | X    | `![[image.png]]`               | File not in Attachments|

## Fix Script

To fix all broken links with available suggestions:

<List of specific find-and-replace commands or instructions>
```

## Examples

### Example 1: Full Vault Scan

```
/broken-links
```

### Example 2: Interactive Fix Mode

```
/broken-links --fix-mode interactive
```

Presents each broken link and asks for confirmation before applying fixes.

### Example 3: Scoped Scan

```
/broken-links --scope Projects/
```

Scans only the Projects folder for broken links.

---

**Invoke with:** `/broken-links` to find and fix broken references across your vault
