#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Validate Wiki-Links Hook

Validates that wiki-links in a file resolve to existing notes in the vault.
Used as a Stop hook to verify skill output has valid links.

Exit Codes:
  0 - Validation passed (or only warnings)
  2 - Validation failed (blocking, if --strict mode)

Usage in skill frontmatter:
  hooks:
    Stop:
      - type: command
        command: >-
          python3 .claude/hooks/validators/validate_links.py
          --directory Meetings/
          --warn-only
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


def find_latest_file(directory: Path, extension: str, within_minutes: int = 5) -> Path | None:
    """Find the most recently modified file in directory."""
    if not directory.exists():
        return None

    cutoff = datetime.now() - timedelta(minutes=within_minutes)
    recent = []

    for file in directory.rglob(f"*{extension}"):
        mtime = datetime.fromtimestamp(file.stat().st_mtime)
        if mtime > cutoff:
            recent.append((file, mtime))

    if not recent:
        return None

    return max(recent, key=lambda x: x[1])[0]


def extract_wiki_links(content: str) -> list[str]:
    """Extract all wiki-links from content."""
    # Match [[link]] and [[link|alias]]
    pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
    matches = re.findall(pattern, content)
    return list(set(matches))


def find_note(vault_root: Path, link_text: str) -> Path | None:
    """Try to find a note matching the link text."""
    # Direct match
    direct = vault_root / f"{link_text}.md"
    if direct.exists():
        return direct

    # Search in common directories
    search_dirs = [
        vault_root,
        vault_root / "Meetings",
        vault_root / "Projects",
        vault_root / "Tasks",
        vault_root / "ADRs",
        vault_root / "Incubator",
        vault_root / "Daily",
    ]

    for year in ["2024", "2025", "2026"]:
        search_dirs.append(vault_root / "Meetings" / year)
        search_dirs.append(vault_root / "Daily" / year)

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue

        target = search_dir / f"{link_text}.md"
        if target.exists():
            return target

    # Glob search for partial match
    for match in vault_root.rglob(f"*{link_text}*.md"):
        if match.stem == link_text:
            return match

    return None


def main():
    parser = argparse.ArgumentParser(description="Validate wiki-links resolve")
    parser.add_argument("--file", help="Specific file to validate")
    parser.add_argument("--directory", help="Directory to find latest file in")
    parser.add_argument("--extension", default=".md", help="File extension")
    parser.add_argument("--warn-only", action="store_true", help="Only warn, don't fail on broken links")
    parser.add_argument("--ignore", action="append", default=[], help="Patterns to ignore")
    parser.add_argument("--within-minutes", type=int, default=5, help="Check files modified within N minutes")
    args = parser.parse_args()

    vault_root = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))

    # Determine target file
    if args.file:
        target = vault_root / args.file
        if not target.exists():
            print(f"ERROR: File not found: {args.file}")
            sys.exit(2)
    elif args.directory:
        directory = vault_root / args.directory
        target = find_latest_file(directory, args.extension, args.within_minutes)
        if not target:
            print(f"ERROR: No recent {args.extension} files found in {args.directory}")
            sys.exit(2)
    else:
        print("ERROR: Must specify either --file or --directory")
        sys.exit(2)

    print(f"🔗 Validating links in: {target.relative_to(vault_root)}")

    content = target.read_text(encoding="utf-8")
    links = extract_wiki_links(content)

    if not links:
        print("✅ No wiki-links found (nothing to validate)")
        sys.exit(0)

    print(f"Found {len(links)} unique wiki-links")

    broken = []
    valid = []

    for link in links:
        # Check ignore patterns
        if any(pattern in link for pattern in args.ignore):
            print(f"⏭️  Ignored: [[{link}]]")
            continue

        found = find_note(vault_root, link)
        if found:
            print(f"✅ Valid: [[{link}]]")
            valid.append(link)
        else:
            print(f"❌ Broken: [[{link}]]")
            broken.append(link)

    print(f"\n📊 Summary: {len(valid)} valid, {len(broken)} broken")

    if broken:
        if args.warn_only:
            print(f"\n⚠️  Warning: {len(broken)} broken links (non-blocking)")
            print("Consider creating these notes or fixing the links:")
            for b in broken:
                print(f"  - [[{b}]]")
            sys.exit(0)
        else:
            print(f"\nERROR: {len(broken)} broken wiki-links found:")
            for b in broken:
                print(f"  - [[{b}]]")
            print("\nPlease create these notes or fix the links.")
            sys.exit(2)

    print("\n✅ All wiki-links resolve correctly")
    sys.exit(0)


if __name__ == "__main__":
    main()
