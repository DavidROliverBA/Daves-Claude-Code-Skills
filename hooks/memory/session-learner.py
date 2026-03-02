#!/usr/bin/env python3
"""
Session Learner Hook for Claude Code
Records session outcomes to MCP memory graph for cross-session learning.

This hook complements session-summary.py (which writes to the daily note)
by recording structured knowledge to the MCP memory graph. This enables
vault-review to surface trends, lessons, and improvement suggestions at
the start of the next session.

Hook Type: Notification (Stop)
Exit Codes:
  0 - Always (non-blocking)

Memory Graph Entity Types Written:
  SessionSummary    - What happened in this session
  VaultHealth       - Health snapshot (if health checks were run)
  SkillOutcome      - Skills executed and their results
  KnowledgeGap      - Gaps identified during the session
  LessonLearned     - Patterns observed across sessions

Design Notes:
  - This hook runs at session end alongside session-summary.py
  - Primary: reads the Session Log from today's daily note (written by session-summary.py)
  - Fallback: reads git log directly if daily note is unavailable
  - It analyses commit messages and file paths to infer skill usage and outcomes
  - It writes to MCP memory via the Claude Code MCP protocol
  - Non-blocking: failures are logged to stderr but never prevent session end

Integration with Self-Improvement Loop:
  1. This hook RECORDS (Phase 2 of the loop)
  2. vault-review READS the recorded entities (Phase 3 - Analyse)
  3. Improvement suggestions are surfaced based on accumulated patterns
  4. See HLD - Vault Self-Improvement Loop.md for the full architecture

Implemented:
  - Triage classification (Apply/Capture/Dismiss) for session observations
  - Pruning of old manifests (keeps last 20)

Future Enhancements (Phase B/C):
  - Parse hook warnings from the session to identify recurring issues
  - Compare health metrics with previous sessions for trend detection
  - Auto-create LessonLearned entities when patterns repeat 3+ times
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Triage classification for observations
# Apply   → Actionable now (fix, update rule, add to CLAUDE.md)
# Capture → Worth recording for trend analysis (may promote later)
# Dismiss → One-off, no future value
TRIAGE_RULES = {
    # Patterns that indicate one-off activity (Dismiss) — checked FIRST
    "dismiss": [
        r"daily|stand.?up|sync|catch.?up",
        r"typo|whitespace|formatting only",
    ],
    # Patterns that indicate actionable learnings (Apply)
    "apply": [
        r"hotfix|bugfix",
        r"fix.*(hook|skill|rule|convention|config|claude\.md)",
        r"hook.*fail|hook.*block|hook.*error",
        r"permission.*denied|sandbox.*block",
        r"workaround|hack|temporary",
    ],
    # Patterns that indicate recurring issues worth tracking (Capture)
    "capture": [
        r"refactor|improve|enhance",
        r"new.*skill|new.*hook|new.*script",
        r"convention|pattern|standard",
        r"migration|rename|consolidat",
    ],
}

MAX_SESSION_ENTITIES = 20  # Keep last N SessionSummary manifests

VAULT_ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_PATTERNS = {
    "Meetings/": "meeting",
    "Daily/": "daily",
    "Tasks/": "task",
    "People/": "person",
    "ADRs/": "adr",
    "Projects/": "project",
    "Emails/": "email",
    "Incubator/": "incubator",
    "Forms/": "form",
    "Objectives/": "objective",
    "HLD - ": "hld",
    "LLD - ": "lld",
    "Reference - ": "reference",
    "Concept - ": "concept",
    "Pattern - ": "pattern",
    "System - ": "system",
    "Organisation - ": "organisation",
    "Tool - ": "tool",
    "Framework - ": "framework",
    ".claude/skills/": "skill-development",
    ".claude/hooks/": "hook-development",
    ".claude/scripts/": "script-development",
}

MAINTENANCE_INDICATORS = [
    "vault-maintenance",
    "quality-report",
    "broken-links",
    "orphans",
    "archive",
    "auto-tag",
    "auto-summary",
    "rename",
    "template-sync",
]


def run_git(*args: str) -> str:
    """Run a git command and return stdout, or empty string on failure."""
    try:
        result = subprocess.run(
            ["git", "-C", str(VAULT_ROOT), *args],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def get_session_commits() -> list[dict]:
    """Get commits from the last 2 hours with hash, message, and files changed."""
    output = run_git(
        "log",
        "--oneline",
        "--name-only",
        "--since=2 hours ago",
    )
    if not output:
        return []

    commits = []
    current = None
    for line in output.splitlines():
        if line and not line.startswith(" ") and " " in line:
            parts = line.split(" ", 1)
            if len(parts[0]) >= 7 and len(parts[0]) <= 12:
                if current:
                    commits.append(current)
                current = {
                    "hash": parts[0],
                    "message": parts[1],
                    "files": [],
                }
                continue
        if current and line.strip():
            current["files"].append(line.strip())

    if current:
        commits.append(current)
    return commits


def get_daily_note_path() -> Path:
    """Return path to today's daily note."""
    today = datetime.now()
    return VAULT_ROOT / "Daily" / str(today.year) / f"{today.strftime('%Y-%m-%d')}.md"


def get_session_log_from_daily() -> list[dict] | None:
    """Extract session commits from today's daily note Session Log section.

    Returns None if daily note doesn't exist or has no session log.
    Falls back to git log in that case.
    """
    daily_path = get_daily_note_path()
    if not daily_path.exists():
        return None

    content = daily_path.read_text(encoding="utf-8")

    # Find the Session Log section
    session_log_match = re.search(
        r"## Session Log\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL
    )
    if not session_log_match:
        return None

    session_text = session_log_match.group(1)

    # Parse commit lines: "- abc1234 Add meeting notes"
    # Validate hash is hex to avoid false positives from file-change lines
    hex_pattern = re.compile(r"^[0-9a-f]+$", re.IGNORECASE)
    commits = []
    for line in session_text.splitlines():
        line = line.strip()
        if line.startswith("- ") and len(line) > 10:
            parts = line[2:].split(" ", 1)
            if len(parts) == 2 and len(parts[0]) >= 7 and hex_pattern.match(parts[0]):
                commits.append(
                    {
                        "hash": parts[0],
                        "message": parts[1],
                        "files": [],
                    }
                )

    return commits if commits else None


def infer_skills_used(commits: list[dict]) -> list[str]:
    """Infer which skills were likely used based on commit messages and files."""
    skills = set()

    for commit in commits:
        msg = commit["message"].lower()
        files = commit.get("files", [])

        # Check commit message for skill indicators
        for indicator in MAINTENANCE_INDICATORS:
            if indicator in msg:
                skills.add(indicator)

        # Check file paths for skill patterns
        for filepath in files:
            for pattern, skill in SKILL_PATTERNS.items():
                if pattern in filepath:
                    skills.add(skill)
                    break

    return sorted(skills)


def infer_session_type(commits: list[dict], skills: list[str]) -> str:
    """Classify the session type based on what was done."""
    maintenance_skills = set(skills) & set(MAINTENANCE_INDICATORS)
    if maintenance_skills:
        return "maintenance"

    infra_skills = {"skill-development", "hook-development", "script-development"}
    if set(skills) & infra_skills:
        return "infrastructure"

    note_skills = {
        "meeting",
        "daily",
        "task",
        "person",
        "adr",
        "email",
        "project",
    }
    if set(skills) & note_skills:
        return "knowledge-capture"

    if any("HLD" in c["message"] or "LLD" in c["message"] for c in commits):
        return "architecture"

    return "general"


def count_files_by_type(commits: list[dict]) -> dict[str, int]:
    """Count how many files were changed by type."""
    counts: dict[str, int] = {}
    seen: set[str] = set()
    for commit in commits:
        for filepath in commit.get("files", []):
            if filepath in seen:
                continue
            seen.add(filepath)
            ext = Path(filepath).suffix
            if ext:
                counts[ext] = counts.get(ext, 0) + 1
    return counts


def build_session_entity(
    commits: list[dict],
    skills: list[str],
    session_type: str,
    file_counts: dict[str, int],
    triage_level: str = "capture",
) -> dict:
    """Build the SessionSummary entity for MCP memory."""
    today = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M")

    observations = [
        f"Session date: {today} at {time}",
        f"Session type: {session_type}",
        f"Triage: {triage_level}",
        f"Commits: {len(commits)}",
        f"Skills used: {', '.join(skills) if skills else 'none detected'}",
    ]

    # Add commit summaries (up to 10)
    for commit in commits[:10]:
        observations.append(f"Commit: {commit['hash']} - {commit['message']}")

    # Add file change summary
    total_files = sum(file_counts.values())
    if total_files:
        observations.append(f"Total files changed: {total_files}")
        md_count = file_counts.get(".md", 0)
        if md_count:
            observations.append(f"Markdown files changed: {md_count}")

    return {
        "name": f"Session-{today}-{time.replace(':', '')}",
        "entityType": "SessionSummary",
        "observations": observations,
    }


def build_skill_outcomes(skills: list[str]) -> list[dict]:
    """Build SkillOutcome entities for each skill used."""
    today = datetime.now().strftime("%Y-%m-%d")
    entities = []
    for skill in skills:
        entities.append(
            {
                "name": f"SkillRun-{skill}-{today}",
                "entityType": "SkillOutcome",
                "observations": [
                    f"Skill: {skill}",
                    f"Date: {today}",
                    "Outcome: completed (inferred from git commits)",
                ],
            }
        )
    return entities


def write_to_memory(
    entities: list[dict], relations: list[dict], triage_level: str = "capture"
) -> None:
    """Write entities and relations to MCP memory.

    Note: This hook runs outside the MCP context, so it cannot directly
    call MCP tools. Instead, it writes a JSON manifest that vault-review
    can read and process at the start of the next session.
    """
    manifest_dir = VAULT_ROOT / ".claude" / "memory"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H%M%S")
    manifest_path = manifest_dir / f"pending-{today}-{time}.json"

    manifest = {
        "created": datetime.now().isoformat(),
        "triage": triage_level,
        "entities": entities,
        "relations": relations,
        "status": "pending",
    }

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(
        f"Session learner: wrote {len(entities)} entities to {manifest_path.name}",
        file=sys.stderr,
    )


def triage_observation(text: str) -> str:
    """Classify an observation as apply, capture, or dismiss.

    Check order: dismiss first (cheap one-offs), then apply (actionable),
    then capture (worth tracking). Default is capture.
    """
    text_lower = text.lower()
    for pattern in TRIAGE_RULES["dismiss"]:
        if re.search(pattern, text_lower):
            return "dismiss"
    for pattern in TRIAGE_RULES["apply"]:
        if re.search(pattern, text_lower):
            return "apply"
    for pattern in TRIAGE_RULES["capture"]:
        if re.search(pattern, text_lower):
            return "capture"
    return "capture"  # Default: capture for trend analysis


def triage_session(commits: list[dict], skills: list[str]) -> str:
    """Classify the entire session's triage level based on commits and skills."""
    classifications = []
    for commit in commits:
        classifications.append(triage_observation(commit["message"]))
    # Session-level: highest priority wins (apply > capture > dismiss)
    if "apply" in classifications:
        return "apply"
    if "capture" in classifications:
        return "capture"
    return "dismiss"


def prune_old_manifests() -> int:
    """Remove oldest session manifests beyond MAX_SESSION_ENTITIES.

    Returns number of pruned files.
    """
    manifest_dir = VAULT_ROOT / ".claude" / "memory"
    if not manifest_dir.exists():
        return 0

    manifests = sorted(manifest_dir.glob("pending-*.json"))
    if len(manifests) <= MAX_SESSION_ENTITIES:
        return 0

    to_prune = manifests[: len(manifests) - MAX_SESSION_ENTITIES]
    pruned = 0
    for manifest_path in to_prune:
        try:
            manifest_path.unlink()
            pruned += 1
        except OSError:
            pass

    if pruned:
        print(
            f"Session learner: pruned {pruned} old manifests (kept last {MAX_SESSION_ENTITIES})",
            file=sys.stderr,
        )
    return pruned


def cleanup_temp_storage() -> None:
    """Clean up Claude temp files older than 24 hours to prevent disk bloat.

    Parallel subagents write temp files to /private/tmp/claude-501/ and
    /tmp/claude/. Without cleanup these accumulate across sessions.
    """
    uid = os.getuid()
    tmp_dirs = [
        Path(f"/private/tmp/claude-{uid}"),
        Path("/tmp/claude"),
    ]
    now = datetime.now().timestamp()
    max_age_secs = 86400  # 24 hours
    cleaned = 0

    for tmp_dir in tmp_dirs:
        if not tmp_dir.exists():
            continue
        try:
            for item in tmp_dir.iterdir():
                # Skip the tasks/ subdirectory (managed by Claude Code)
                if item.name == "tasks" or item.is_dir():
                    continue
                try:
                    age = now - item.stat().st_mtime
                    if age > max_age_secs:
                        item.unlink()
                        cleaned += 1
                except OSError:
                    pass
        except OSError:
            pass

    if cleaned:
        print(f"Session learner: cleaned {cleaned} stale temp files", file=sys.stderr)


def main() -> None:
    """Main entry point for session learner hook."""
    # Clean up stale temp files from previous sessions
    cleanup_temp_storage()

    # Primary: read from daily note (written by session-summary.py)
    commits = get_session_log_from_daily()

    # Fallback: read git log directly if daily note unavailable
    if commits is None:
        commits = get_session_commits()

    if not commits:
        sys.exit(0)

    skills = infer_skills_used(commits)
    session_type = infer_session_type(commits, skills)
    file_counts = count_files_by_type(commits)

    # Triage: classify session importance
    triage_level = triage_session(commits, skills)

    # Dismiss sessions don't get recorded (one-off, no learning value)
    if triage_level == "dismiss":
        print("Session learner: session triaged as dismiss — skipping", file=sys.stderr)
        sys.exit(0)

    # Prune old manifests before writing new one
    prune_old_manifests()

    # Build entities
    session_entity = build_session_entity(
        commits, skills, session_type, file_counts, triage_level
    )
    skill_entities = build_skill_outcomes(skills)
    all_entities = [session_entity] + skill_entities

    # Build relations
    relations = []
    for skill_entity in skill_entities:
        relations.append(
            {
                "from": session_entity["name"],
                "relationType": "executed",
                "to": skill_entity["name"],
            }
        )

    # Write manifest for vault-review to process
    write_to_memory(all_entities, relations, triage_level)
    sys.exit(0)


if __name__ == "__main__":
    main()
