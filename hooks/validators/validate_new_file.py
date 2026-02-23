#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Validate New File Hook

Validates that a new file was created in the expected directory with the
expected extension. Used as a Stop hook to verify skill output.

Exit Codes:
  0 - Validation passed
  2 - Validation failed (blocking, feeds back to Claude)

Usage in skill frontmatter:
  hooks:
    Stop:
      - type: command
        command: >-
          python3 .claude/hooks/validators/validate_new_file.py
          --directory Meetings/
          --extension .md
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def find_recent_files(directory: Path, extension: str, within_minutes: int = 5) -> list[Path]:
    """Find files created/modified within the last N minutes."""
    if not directory.exists():
        return []

    cutoff = datetime.now() - timedelta(minutes=within_minutes)
    recent = []

    for file in directory.rglob(f"*{extension}"):
        mtime = datetime.fromtimestamp(file.stat().st_mtime)
        if mtime > cutoff:
            recent.append(file)

    return sorted(recent, key=lambda f: f.stat().st_mtime, reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Validate new file creation")
    parser.add_argument("--directory", required=True, help="Expected directory for new file")
    parser.add_argument("--extension", default=".md", help="Expected file extension")
    parser.add_argument("--within-minutes", type=int, default=5, help="Check files modified within N minutes")
    parser.add_argument("--contains", action="append", help="Required content in file (can specify multiple)")
    args = parser.parse_args()

    # Resolve directory relative to vault root
    vault_root = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
    directory = vault_root / args.directory

    # Find recent files
    recent_files = find_recent_files(directory, args.extension, args.within_minutes)

    if not recent_files:
        print(f"ERROR: No new {args.extension} files found in {args.directory}")
        print(f"Please create a file in the {args.directory} directory.")
        sys.exit(2)

    latest = recent_files[0]
    print(f"✅ Found new file: {latest.relative_to(vault_root)}")

    # Check required content if specified
    if args.contains:
        content = latest.read_text(encoding="utf-8")
        missing = []

        for required in args.contains:
            if required not in content:
                missing.append(required)

        if missing:
            print(f"\nERROR: Missing required sections in {latest.name}:")
            for m in missing:
                print(f"  ❌ '{m}'")
            print("\nPlease add these sections and try again.")
            sys.exit(2)

        for required in args.contains:
            print(f"✅ Contains '{required}'")

    print("\n✅ All validations passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
