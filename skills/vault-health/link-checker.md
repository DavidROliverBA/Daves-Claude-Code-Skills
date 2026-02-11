---
description: Validate external URLs in Markdown notes using parallel Haiku agents to check for dead links
model: haiku
---

# /link-checker

Validate external URLs (HTTP/HTTPS) found in Markdown notes. Uses parallel Haiku agents to check batches of 10-15 URLs simultaneously, detecting dead links, redirects, and timeouts.

## When to Use This Skill

- Periodic maintenance to find dead external links
- Validating reference notes with URLs
- Checking links before publishing or sharing content
- Post-migration validation of external references

## Usage

```
/link-checker [--scope path/to/folder] [--timeout 10] [--include-redirects]
```

### Parameters

| Parameter             | Description                                       | Required |
|-----------------------|---------------------------------------------------|----------|
| `--scope`             | Folder to scan (default: entire vault)            | No       |
| `--timeout`           | Timeout per URL in seconds (default: 10)          | No       |
| `--include-redirects` | Report permanent redirects as issues (default: no)| No       |

## Instructions

### Phase 1: Extract External URLs

1. **Scan Markdown files** in scope
2. **Extract URLs** matching patterns:
   - `[text](https://...)` — Standard Markdown links
   - `url: "https://..."` — Frontmatter URL fields
   - Bare URLs in text (https://...)
3. **Deduplicate** — Same URL referenced from multiple files should only be checked once
4. **Build URL-to-files map** — Track which files reference each URL
5. **Divide into batches** of 10-15 URLs per agent

### Phase 2: Batch URL Validation — Agent Team (Parallel Haiku Agents)

Use the Batch Processing pattern. Launch N parallel agents.

**Agent 1-N: URL Checker** (Haiku)
Task: Validate assigned batch of URLs
- For each URL:
  1. Attempt to fetch with HEAD request (via WebFetch)
  2. If HEAD fails, try GET request
  3. Record response status:
     - **200-299:** OK
     - **301/302:** Redirect (note destination)
     - **403:** Forbidden (may be access-restricted)
     - **404:** Not found (broken link)
     - **5xx:** Server error (may be temporary)
     - **Timeout:** No response within timeout
  4. Record response time
- For failed URLs, attempt one retry after 2 seconds
Return: List of `{ url, status, responseTime, redirectUrl, error }` per URL

### Phase 3: Compile Report

1. **Categorise results:**
   - **Broken** (404, DNS failure) — Definitely dead
   - **Unreachable** (timeout, 5xx) — May be temporary
   - **Redirected** (301/302) — URL has moved
   - **OK** (2xx) — Working fine
2. **Map broken URLs to source files**
3. **Suggest fixes** for broken links (e.g., Wayback Machine URL, updated URL)

## Output Format

```markdown
# External Link Check Report

**Date:** YYYY-MM-DD | **Scope:** <scope> | **URLs Checked:** X

## Summary

| Status       | Count | Percentage |
|--------------|-------|------------|
| OK           | X     | X%         |
| Broken       | X     | X%         |
| Unreachable  | X     | X%         |
| Redirected   | X     | X%         |
| **Total**    | **X** | **100%**   |

## Broken Links (X found)

| URL                                   | Status | Referenced In                | Suggestion          |
|---------------------------------------|--------|------------------------------|---------------------|
| `https://example.com/old-page`        | 404    | `Reference - API Guide.md`   | Check Wayback Machine |
| `https://dead-site.com/docs`          | DNS    | `Concept - Patterns.md`      | Remove or replace   |

## Unreachable Links (X found)

| URL                                   | Status  | Referenced In               |
|---------------------------------------|---------|------------------------------|
| `https://slow-site.com/api`           | Timeout | `System - Gateway.md`        |

## Redirected Links (X found)

| Original URL                          | Redirects To                        | Referenced In          |
|---------------------------------------|-------------------------------------|------------------------|
| `https://old.example.com/docs`        | `https://new.example.com/docs`      | `Reference - Guide.md` |

## Fix Script

For broken links with available fixes:
1. In `<file>`: Replace `<old-url>` with `<new-url>`
```

## Examples

### Example 1: Full Vault Check

```
/link-checker
```

### Example 2: Reference Notes Only

```
/link-checker --scope Reference*
```

### Example 3: Include Redirects

```
/link-checker --include-redirects --timeout 15
```

---

**Invoke with:** `/link-checker` to validate all external URLs in your vault
