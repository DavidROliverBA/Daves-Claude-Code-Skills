#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Validate File Contains Hook

Validates that a file contains required sections or content.
Used as a Stop hook to verify skill output structure.

Exit Codes:
  0 - Validation passed
  2 - Validation failed (blocking, feeds back to Claude)

Usage in skill frontmatter:
  hooks:
    Stop:
      - type: command
        command: >-
          python3 .claude/hooks/validators/validate_file_contains.py
          --file path/to/file.md
          --contains '## Attendees'
          --contains '## Action Items'
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


def main():
    parser = argparse.ArgumentParser(description="Validate file contains required content")
    parser.add_argument("--file", help="Specific file to validate")
    parser.add_argument("--directory", help="Directory to find latest file in")
    parser.add_argument("--extension", default=".md", help="File extension when using --directory")
    parser.add_argument("--contains", action="append", required=True, help="Required content (can specify multiple)")
    parser.add_argument("--contains-regex", action="append", help="Required regex pattern (can specify multiple)")
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

    print(f"📄 Validating: {target.relative_to(vault_root)}")

    content = target.read_text(encoding="utf-8")
    errors = []

    # Check required content
    for required in args.contains:
        if required in content:
            print(f"✅ Contains '{required}'")
        else:
            print(f"❌ Missing '{required}'")
            errors.append(required)

    # Check regex patterns
    if args.contains_regex:
        for pattern in args.contains_regex:
            if re.search(pattern, content):
                print(f"✅ Matches regex '{pattern}'")
            else:
                print(f"❌ Missing pattern '{pattern}'")
                errors.append(f"regex: {pattern}")

    if errors:
        print(f"\nERROR: Missing {len(errors)} required sections:")
        for e in errors:
            print(f"  - {e}")
        print("\nPlease add these sections and try again.")
        sys.exit(2)

    print("\n✅ All content validations passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
