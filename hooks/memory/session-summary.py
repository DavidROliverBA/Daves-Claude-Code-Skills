#!/usr/bin/env python3
"""
Session Summary Hook for Claude Code
Appends a git-based session summary to today's daily note.

Hook Type: Notification (Stop)
Exit Codes:
  0 - Always (non-blocking)
"""

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent.parent
MAX_FILES_SHOWN = 10


def run_git(*args: str) -> str:
    """Run a git command and return stdout, or empty string on failure."""
    try:
        result = subprocess.run(
            ["git", "-C", str(VAULT_ROOT), *args],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def get_session_commits() -> list[str]:
    """Get commits from the last hour as 'hash message' lines."""
    output = run_git("log", "--oneline", "--since=1 hour ago")
    return output.splitlines() if output else []


def get_diff_stat(num_commits: int) -> str:
    """Get the --stat summary for the last N commits."""
    if num_commits <= 0:
        return ""
    return run_git("diff", "--stat", f"HEAD~{num_commits}..HEAD")


def parse_diff_stat(stat_output: str) -> tuple[str, list[str]]:
    """Parse git diff --stat into a summary line and file list.

    Returns (summary_line, file_list) where summary_line is like
    '8 files changed, 217 insertions(+), 12 deletions(-)' and
    file_list is the individual file paths.
    """
    lines = stat_output.strip().splitlines()
    if not lines:
        return "", []

    # Last line is the summary (e.g. "8 files changed, 217 insertions(+)")
    summary = lines[-1].strip()
    # Earlier lines are file stats (e.g. " path/to/file.md | 4 ++++")
    files = []
    for line in lines[:-1]:
        parts = line.split("|")
        if parts:
            filepath = parts[0].strip()
            if filepath:
                files.append(filepath)

    return summary, files


def build_session_entry(commits: list[str], stat_summary: str, file_list: list[str]) -> str:
    """Build the markdown session log entry."""
    now = datetime.now()
    lines = [f"### {now.strftime('%H:%M:%S')} — Claude Code Session", ""]

    # Commits
    lines.append("**Commits:**")
    for commit in commits:
        lines.append(f"- {commit}")
    lines.append("")

    # File changes
    if stat_summary:
        lines.append(f"**Files changed:** {stat_summary}")
        shown = file_list[:MAX_FILES_SHOWN]
        for f in shown:
            lines.append(f"- {f}")
        remaining = len(file_list) - MAX_FILES_SHOWN
        if remaining > 0:
            lines.append(f"- + {remaining} more")
        lines.append("")

    return "\n".join(lines)


def get_daily_path() -> Path:
    """Return the path to today's daily note."""
    today = datetime.now()
    return VAULT_ROOT / "Daily" / str(today.year) / f"{today.strftime('%Y-%m-%d')}.md"


def create_daily_note(path: Path) -> str:
    """Create a daily note from the template structure."""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    day_name = today.strftime("%A")
    day_num = today.day
    month_name = today.strftime("%B")
    year = today.year

    return f"""---
type: Daily
title: "{date_str}"
date: "{date_str}"
created: {date_str}
modified: {date_str}
tags:
  - daily
relatedTo: []
---

# {day_name}, {day_num} {month_name} {year}

## Today's Focus

-

## Reminders

## Tasks

```dataview
TASK
FROM "/"
WHERE !completed AND (doDate = date("{date_str}") OR dueBy = date("{date_str}"))
```

## Meetings

-

## Notes

## Session Log

## Completed Today

## End of Day Review

-
"""


def insert_session_log(content: str, entry: str) -> str:
    """Insert session log entry into the daily note content.

    Three cases:
    1. '## Session Log' exists — append entry after section header (before next ##)
    2. '## End of Day Review' exists but no Session Log — insert Session Log before it
    3. Neither exists — append both sections at the end
    """
    session_log_heading = "## Session Log"
    eod_heading = "## End of Day Review"

    if session_log_heading in content:
        # Find the end of the Session Log section (next ## heading or EOF)
        header_pos = content.index(session_log_heading)
        after_header = header_pos + len(session_log_heading)

        # Find next ## heading after Session Log
        next_heading = re.search(r'\n## ', content[after_header:])
        if next_heading:
            insert_pos = after_header + next_heading.start()
        else:
            insert_pos = len(content)

        # Insert the entry before the next heading (with spacing)
        return content[:insert_pos].rstrip() + "\n\n" + entry + "\n" + content[insert_pos:]

    elif eod_heading in content:
        # Insert Session Log section before End of Day Review
        eod_pos = content.index(eod_heading)
        section = f"{session_log_heading}\n\n{entry}\n"
        return content[:eod_pos] + section + content[eod_pos:]

    else:
        # Append at end
        return content.rstrip() + f"\n\n{session_log_heading}\n\n{entry}\n"


def append_to_agenda(commits: list[str]) -> None:
    """Append a one-liner to AGENDA.md Session Notes section."""
    agenda_path = VAULT_ROOT / ".claude" / "AGENDA.md"
    if not agenda_path.exists():
        return

    content = agenda_path.read_text(encoding="utf-8")

    today = datetime.now().strftime("%Y-%m-%d")
    summaries = []
    for c in commits[:3]:
        parts = c.split(" ", 1)
        if len(parts) == 2:
            summaries.append(parts[1])

    summary_text = ", ".join(summaries)
    if len(commits) > 3:
        summary_text += f" (+{len(commits) - 3} more)"

    entry = f"- **{today}:** {len(commits)} commits — {summary_text}"

    session_notes_heading = "## Session Notes"
    if session_notes_heading not in content:
        return

    # Find end of Session Notes section
    header_pos = content.index(session_notes_heading)
    after_header = header_pos + len(session_notes_heading)

    # Append entry at the end of the section (before next ## or EOF)
    next_heading = re.search(r'\n## ', content[after_header:])
    if next_heading:
        insert_pos = after_header + next_heading.start()
    else:
        insert_pos = len(content)

    updated = content[:insert_pos].rstrip() + "\n" + entry + "\n" + content[insert_pos:]
    agenda_path.write_text(updated, encoding="utf-8")


def main():
    # Get recent commits
    commits = get_session_commits()
    if not commits:
        sys.exit(0)

    # Get file change stats
    stat_output = get_diff_stat(len(commits))
    stat_summary, file_list = parse_diff_stat(stat_output)

    # Build the entry
    entry = build_session_entry(commits, stat_summary, file_list)

    # Get or create daily note
    daily_path = get_daily_path()

    if daily_path.exists():
        content = daily_path.read_text(encoding="utf-8")
    else:
        # Ensure year directory exists
        daily_path.parent.mkdir(parents=True, exist_ok=True)
        content = create_daily_note(daily_path)

    # Insert the session log entry
    updated = insert_session_log(content, entry)

    # Write the file
    daily_path.write_text(updated, encoding="utf-8")

    # Append session summary to AGENDA.md
    append_to_agenda(commits)

    sys.exit(0)


if __name__ == "__main__":
    main()
