
# /check-weblinks Skill

Check all weblinks in the vault to identify dead or stale links. Part of quarterly vault maintenance.

## Usage

```
/check-weblinks
/check-weblinks --fix    # Also update frontmatter with results
```

## Instructions

This skill uses a **sub-agent** to check weblinks in parallel for efficiency.

### 1. Find All Weblinks

Search for all notes with `type: Reference`:

```bash
grep -l "type: Reference" *.md
```

Or use Glob to find weblink files:
- Pattern: `Weblink - *.md`

### 2. Launch Sub-Agent for Link Checking

Use the Task tool to spawn a sub-agent with `model: "haiku"` for efficiency:

```
Task: Check weblink health
Type: general-purpose
Model: haiku
Prompt: |
  Check the following weblinks and report their status.

  For each weblink:
  1. Read the file to get the URL from frontmatter
  2. Test the URL using curl: `curl -I -L -s -o /dev/null -w "%{http_code}" "<url>"`
  3. Classify the result:
     - 200-299: active
     - 301, 302, 308: redirected (note new URL)
     - 403, 404, 410: dead
     - 500-599: server error (may be temporary)
     - Timeout/error: unreachable

  Return a structured report with:
  - File name
  - URL
  - HTTP status code
  - Classification (active/redirected/dead/error)
  - New URL if redirected

  Files to check:
  [LIST OF WEBLINK FILES]
```

### 3. Process Results

Collect results from sub-agent and categorise:

**Active (200-299)**
- No action needed
- Update `lastChecked` if --fix flag

**Redirected (301, 302, 308)**
- Note the redirect target
- Consider updating URL in frontmatter
- Flag for user review

**Dead (403, 404, 410)**
- Mark as `linkStatus: dead`
- Candidate for archiving (if not referenced) or deletion

**Error (500+, timeout)**
- May be temporary
- Recheck before marking dead
- Mark as `linkStatus: error`

### 4. Update Frontmatter (if --fix)

For each checked weblink, update frontmatter:

```yaml
type: Reference
url: https://example.com/page
linkStatus: active | redirected | dead | error
lastChecked: 2026-01-10
redirectUrl: https://new-url.com  # If redirected
```

### 5. Generate Report

Output a summary:

```
## Weblink Health Check - 2026-01-10

### Summary
- Total weblinks: 45
- Active: 38 (84%)
- Redirected: 4 (9%)
- Dead: 2 (4%)
- Error: 1 (2%)

### Action Required

#### Dead Links
| File | URL | Status | Referenced? |
|------|-----|--------|-------------|
| Weblink - Old API Docs.md | https://old.api.com/docs | 404 | No → Archive candidate |
| Weblink - Deprecated Tool.md | https://tool.io/gone | 410 | Yes (in [[ADR - Tool Selection]]) → Review |

#### Redirected Links
| File | Original URL | Redirects To |
|------|--------------|--------------|
| Weblink - AWS Guide.md | https://old.aws.com | https://docs.aws.amazon.com/new |

### Recommendations
1. Archive: Weblink - Old API Docs.md (dead, unreferenced)
2. Update URL: Weblink - AWS Guide.md (redirected)
3. Review: Weblink - Deprecated Tool.md (dead but referenced)
```

### 6. Check for References

For dead links, check if they're referenced anywhere:

```bash
grep -l "Weblink - Old API Docs" *.md
```

- If unreferenced: Safe to archive or delete
- If referenced: Flag for review - the referencing note may need updating

## Sub-Agent Script

The sub-agent should run this check for each URL:

```bash
#!/bin/bash
# check_url.sh

URL="$1"
TIMEOUT=10

# Follow redirects, get final status code
STATUS=$(curl -I -L -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "$URL" 2>/dev/null)

if [ -z "$STATUS" ] || [ "$STATUS" = "000" ]; then
  echo "error:timeout"
else
  echo "status:$STATUS"
fi
```

## Frequency

Run quarterly as part of vault maintenance:
- January, April, July, October
- Or before major vault reviews

## Integration with Vault Maintenance

This skill is part of the `/vault-maintenance` suite:
- `/check-weblinks` - Verify external links
- `/orphans` - Find notes with no backlinks
- `/broken-links` - Find broken wiki-links
- `/archive batch tasks` - Archive old completed tasks

## Example Session

```
User: /check-weblinks

Claude: Checking 45 weblinks in the vault...

[Launches sub-agent to check URLs in parallel]

## Weblink Health Check Complete

- Active: 38 (84%)
- Redirected: 4 (9%)
- Dead: 2 (4%)
- Error: 1 (2%)

### Dead Links Found:
1. **Weblink - Old API Docs.md** - 404 Not Found
   - Not referenced anywhere
   - Recommendation: Archive

2. **Weblink - Deprecated Tool.md** - 410 Gone
   - Referenced in: [[ADR - Tool Selection]]
   - Recommendation: Review the ADR, may need updating

### Redirected Links:
1. **Weblink - AWS Guide.md**
   - Redirects to: https://docs.aws.amazon.com/new-path
   - Recommendation: Update URL

Run `/check-weblinks --fix` to update frontmatter with check results.
```

## Notes

- Uses sub-agent for parallel checking (faster for many links)
- Respects rate limits - doesn't hammer servers
- Some sites block curl - may show false errors
- Corporate firewalls may affect results (run from appropriate network)
