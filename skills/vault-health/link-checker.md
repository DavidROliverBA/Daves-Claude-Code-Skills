---
description: Validate external URLs in Markdown notes using curl-based checking and parallel Haiku agents to detect dead links, redirects, and timeouts
model: haiku
---

# /link-checker

Validate external URLs (HTTP/HTTPS) found in Markdown notes. Uses curl for reliable bulk URL validation and parallel Haiku agents to check batches of 10-15 URLs simultaneously, detecting dead links, redirects, and timeouts.

## When to Use This Skill

- Periodic maintenance to find dead external links
- Validating reference notes with URLs
- Checking links before publishing or sharing content
- Post-migration validation of external references
- Quarterly vault health reviews

## Usage

```
/link-checker [--scope path/to/folder] [--timeout 10] [--include-redirects] [--fix] [--update]
```

### Parameters

| Parameter             | Description                                              | Required |
|-----------------------|----------------------------------------------------------|----------|
| `--scope`             | Folder to scan (default: entire vault)                   | No       |
| `--timeout`           | Timeout per URL in seconds (default: 10)                 | No       |
| `--include-redirects` | Report permanent redirects as issues (default: no)       | No       |
| `--fix`               | Update frontmatter with `linkStatus` and `lastChecked`   | No       |
| `--update`            | Offer to update URLs that have permanently redirected    | No       |

## Instructions

### Phase 1: Extract External URLs

1. **Scan Markdown files** in scope
2. **Extract URLs** matching patterns:
   - `[text](https://...)` -- Standard Markdown links
   - `url: "https://..."` -- Frontmatter URL fields
   - Bare URLs in text (https://...)
3. **Deduplicate** -- Same URL referenced from multiple files should only be checked once
4. **Build URL-to-files map** -- Track which files reference each URL
5. **Divide into batches** of 10-15 URLs per agent

### Phase 2: Batch URL Validation -- Agent Team (Parallel Haiku Agents)

Use the Batch Processing pattern. Launch N parallel agents.

**Agent 1-N: URL Checker** (Haiku)
Task: Validate assigned batch of URLs

For each URL, use the curl-based validation script via the Bash tool:

```bash
#!/bin/bash
# URL validation script -- run via Bash tool for each URL

URL="$1"
TIMEOUT="${2:-10}"

# Follow redirects, capture final status code
STATUS=$(curl -I -L -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "$URL" 2>/dev/null)

if [ -z "$STATUS" ] || [ "$STATUS" = "000" ]; then
  echo "error:timeout"
else
  # Also capture redirect target if applicable
  REDIRECT=$(curl -I -L -s -o /dev/null -w "%{url_effective}" --max-time $TIMEOUT "$URL" 2>/dev/null)
  echo "status:$STATUS|redirect:$REDIRECT"
fi
```

**Classify each result:**

| HTTP Status | Classification | Action                            |
|-------------|----------------|-----------------------------------|
| 200-299     | `active`       | No action needed                  |
| 301, 308    | `redirected`   | Note new URL, flag for review     |
| 302, 307    | `redirected`   | Temporary redirect, note for info |
| 403         | `error`        | Forbidden -- may be access-restricted, not necessarily dead |
| 404, 410    | `dead`         | Confirmed dead link               |
| 500-599     | `error`        | Server error -- may be temporary  |
| 000/timeout | `error`        | Unreachable -- retry once after 2s before classifying |

For failed URLs (error or dead), attempt one retry after 2 seconds before finalising the classification.

Return: List of `{ url, status, classification, redirectUrl, error }` per URL

### Phase 3: Synthesis and Cross-Reference Checking

1. **Categorise results:**
   - **Active** (200-299) -- Working fine
   - **Redirected** (301/302/307/308) -- URL has moved
   - **Dead** (404, 410, DNS failure) -- Definitely dead
   - **Error** (timeout, 403, 5xx) -- May be temporary
2. **Map broken URLs to source files**
3. **Cross-reference dead links** -- For each dead or errored link, check which other notes reference it:

```bash
# Find all notes that reference a dead link's note title
grep -rl "Reference - Old API Guide" *.md Meetings/ Projects/ ADRs/ Tasks/
```

This identifies notes that depend on the dead reference, so they can be updated or the link removed.

4. **Suggest fixes** for broken links (e.g., Wayback Machine URL, updated URL from redirect chain)

### Phase 4: Update Frontmatter (if `--fix`)

When the `--fix` flag is provided, update frontmatter on each checked note with link health metadata:

```yaml
# Frontmatter fields added/updated by --fix
url: https://example.com/page
linkStatus: active | redirected | dead | error
lastChecked: 2026-01-10
redirectUrl: https://new-location.com/page  # Only if redirected
```

**Field definitions:**

| Field         | Type   | Values                                | Description                          |
|---------------|--------|---------------------------------------|--------------------------------------|
| `linkStatus`  | string | `active`, `redirected`, `dead`, `error` | Current health of the external URL |
| `lastChecked` | date   | `YYYY-MM-DD`                          | Date the URL was last validated      |
| `redirectUrl` | string | URL                                   | Final destination if URL redirects   |

**Rules for frontmatter updates:**
- Only update notes that have a `url` field in frontmatter
- Set `lastChecked` to today's date for all checked URLs
- Set `linkStatus` based on the classification from Phase 2
- Add `redirectUrl` only when status is `redirected`; remove it if status changes to `active`
- Use the Edit tool to modify frontmatter in-place (do not rewrite the entire file)

### Phase 5: Update Redirected URLs (if `--update`)

When the `--update` flag is provided, offer to replace redirected URLs with their final destination:

1. List all redirected URLs with their original and final URLs
2. For each redirected URL:
   - Show the original URL and the redirect target
   - Update the `url` field in frontmatter to the redirect target
   - Set `linkStatus` to `active`
   - Remove `redirectUrl` (no longer needed)
3. Confirm each update with the user before applying

**Note:** `--update` implies `--fix` behaviour (frontmatter is updated regardless).

## Output Format

```markdown
# External Link Check Report

**Date:** YYYY-MM-DD | **Scope:** <scope> | **URLs Checked:** X

## Summary

| Status       | Count | Percentage |
|--------------|-------|------------|
| Active       | X     | X%         |
| Redirected   | X     | X%         |
| Dead         | X     | X%         |
| Error        | X     | X%         |
| **Total**    | **X** | **100%**   |

## Dead Links (X found)

| File | URL | Status | Referenced By | Recommendation |
|------|-----|--------|---------------|----------------|
| `Reference - Old API Guide.md` | `https://example.com/old-page` | 404 | None | Archive candidate |
| `Reference - Deprecated Tool.md` | `https://dead-site.com/docs` | 410 | `Concept - Patterns.md`, `ADR - Tool Selection.md` | Review referencing notes |

## Error Links (X found)

| File | URL | Status | Referenced By |
|------|-----|--------|---------------|
| `Reference - Slow API.md` | `https://slow-site.com/api` | Timeout | `System - Gateway.md` |

## Redirected Links (X found)

| File | Original URL | Redirects To | Referenced By |
|------|--------------|--------------|---------------|
| `Reference - Cloud Guide.md` | `https://old.example.com/docs` | `https://new.example.com/docs` | `Concept - Cloud Strategy.md` |

## Recommendations

1. **Archive:** Reference - Old API Guide.md (dead, unreferenced)
2. **Update URL:** Reference - Cloud Guide.md (redirected)
3. **Review:** Reference - Deprecated Tool.md (dead but referenced by 2 notes)
4. **Recheck:** Reference - Slow API.md (timeout, may be temporary)
```

### Frontmatter Update Summary (when `--fix` is used)

Append to the report:

```markdown
## Frontmatter Updates Applied

| File | linkStatus | lastChecked | redirectUrl |
|------|------------|-------------|-------------|
| `Reference - Old API Guide.md` | dead | 2026-01-10 | -- |
| `Reference - Cloud Guide.md` | redirected | 2026-01-10 | `https://new.example.com/docs` |
| `Reference - Active Page.md` | active | 2026-01-10 | -- |
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

### Example 3: Check and Update Frontmatter

```
/link-checker --fix
```

### Example 4: Check, Fix, and Update Redirects

```
/link-checker --fix --update
```

### Example 5: Custom Timeout with Redirect Reporting

```
/link-checker --include-redirects --timeout 15
```

## Notes

- Uses curl for URL validation (more reliable than HTTP client libraries for bulk checking)
- Uses parallel Haiku agents for batch processing (faster for large numbers of links)
- Respects rate limits -- does not hammer servers
- Some sites block curl HEAD requests -- the agent should retry with GET if HEAD returns 403/405
- Corporate firewalls or VPNs may affect results (run from an appropriate network)
- Cross-reference checking identifies downstream impact of dead links
- Run quarterly as part of vault maintenance, or before major vault reviews

---

**Invoke with:** `/link-checker` to validate all external URLs in your vault
