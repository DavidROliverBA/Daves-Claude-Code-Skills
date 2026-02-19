#!/usr/bin/env python3
"""
Filename Convention Checker Hook for Claude Code
Ensures markdown files follow vault naming conventions.

Hook Type: PostToolUse
Matcher: Edit|Write
Exit Codes:
  0 - Always (non-blocking, provides warnings via stdout)
"""

import json
import re
import sys
from pathlib import Path

# Filename patterns by note type
# Pattern: (expected_prefix, expected_location, pattern_description)
FILENAME_CONVENTIONS = {
    # Current ontology - Events (in folders)
    "Task": ("Task - ", "Tasks/", "Task - {{Title}}.md"),
    "Project": ("Project - ", "Projects/", "Project - {{Name}}.md"),
    "Meeting": ("Meeting - ", "Meetings/", "Meeting - YYYY-MM-DD {{Title}}.md"),
    "ADR": ("ADR - ", "ADRs/", "ADR - {{Title}}.md"),
    "Daily": (None, "Daily/", "YYYY-MM-DD.md"),
    "Incubator": ("Incubator - ", "Incubator/", "Incubator - {{Title}}.md"),
    "FormSubmission": ("FormSubmission - ", "Forms/", "FormSubmission - {{Type}} for {{Project}}.md"),
    "Email": ("Email - ", "Emails/", "Email - {{From}} - {{Subject}}.md"),
    "Trip": ("Trip - ", "Trips/", "Trip - {{Destination}}.md"),
    "Workstream": ("Workstream - ", "Projects/", "Workstream - {{Name}}.md"),
    "Forum": ("Forum - ", "Projects/", "Forum - {{Name}}.md"),
    "Objective": ("Objective - ", "Objectives/", "Objective - {{Title}}.md"),
    # Current ontology - Entities (root)
    "Person": (None, "People/", "{{Name}}.md"),
    "System": ("System - ", "root", "System - {{Name}}.md"),
    "Organisation": ("Organisation - ", "root", "Organisation - {{Name}}.md"),
    "DataAsset": ("DataAsset - ", "root", "DataAsset - {{Name}}.md"),
    "Location": ("Location - ", "root", "Location - {{Name}}.md"),
    "Department": ("Department - ", "root", "Department - {{Name}}.md"),
    # Current ontology - Nodes (root)
    "Concept": ("Concept - ", "root", "Concept - {{Title}}.md"),
    "Pattern": ("Pattern - ", "root", "Pattern - {{Title}}.md"),
    "Reference": ("Reference - ", "root", "Reference - {{Title}}.md"),
    "Research": ("Research - ", "root", "Research - {{Title}}.md"),
    "Threat": ("Threat - ", "root", "Threat - {{Title}}.md"),
    "Framework": ("Framework - ", "root", "Framework - {{Title}}.md"),
    "Tool": ("Tool - ", "root", "Tool - {{Title}}.md"),
    # Current ontology - Navigation (root with _ prefix)
    "MOC": ("_MOC - ", "root", "_MOC - {{Scope}}.md"),
    "Dashboard": ("_Dashboard - ", "root", "_Dashboard - {{Scope}}.md"),
    "Query": ("Query - ", "root", "Query - {{Name}}.md"),
    "ArchModel": ("ArchModel - ", "root", "ArchModel - {{ViewName}}.md"),
    # Governance (synced)
    "Policy": ("Policy - ", "Sync/Policies/", "Policy - {{Title}}.md"),
    "Guardrail": ("Guardrail - ", "Sync/Guardrails/", "Guardrail - {{Title}}.md"),
}

# Date pattern for meetings and daily notes
DATE_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2}')

# Valid date format
ISO_DATE_PATTERN = re.compile(r'^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$')


def extract_note_type(content: str) -> str:
    """Extract note type from frontmatter."""
    match = re.search(r'type:\s*(\w+)', content)
    return match.group(1) if match else ""


def get_relative_path(file_path: str) -> tuple[str, str]:
    """Get the relative path components (folder, filename)."""
    path = Path(file_path)
    filename = path.name

    # Find vault root by looking for .obsidian
    vault_root = None
    for parent in [path.parent] + list(path.parent.parents):
        if (parent / ".obsidian").exists():
            vault_root = parent
            break

    if vault_root:
        try:
            relative = path.parent.relative_to(vault_root)
            folder = str(relative) if str(relative) != "." else "root"
        except ValueError:
            folder = "unknown"
    else:
        folder = "unknown"

    return folder, filename


def validate_filename(file_path: str, note_type: str) -> list[str]:
    """Validate filename against conventions for note type."""
    warnings = []

    if note_type not in FILENAME_CONVENTIONS:
        return warnings  # Unknown type, skip validation

    expected_prefix, expected_location, pattern_desc = FILENAME_CONVENTIONS[note_type]
    folder, filename = get_relative_path(file_path)
    stem = Path(filename).stem

    # Check prefix
    if expected_prefix:
        if not stem.startswith(expected_prefix.rstrip(" ")):
            # Check for common variations
            alt_prefixes = {
                "CodeSnippet - ": ["CodeSnipet - "],  # Common typo
            }
            found_alt = False
            if expected_prefix in alt_prefixes:
                for alt in alt_prefixes[expected_prefix]:
                    if stem.startswith(alt.rstrip(" ")):
                        warnings.append(f"Typo in prefix: '{alt.rstrip(' ')}' should be '{expected_prefix.rstrip(' ')}'")
                        found_alt = True
                        break
            if not found_alt:
                warnings.append(f"Missing prefix: should be '{expected_prefix}{{Title}}.md'")

    # Check location
    if expected_location != "root":
        expected_folder = expected_location.rstrip("/")
        if not folder.startswith(expected_folder.lstrip("+")):
            # Allow subdirectories
            if expected_folder.lstrip("+") not in folder:
                warnings.append(f"Wrong location: should be in {expected_location}")

    # Type-specific checks
    if note_type == "Meeting":
        # Should have date after prefix
        if expected_prefix and stem.startswith(expected_prefix.rstrip(" ")):
            after_prefix = stem[len(expected_prefix.rstrip(" ")):].strip()
            if not after_prefix or not DATE_PATTERN.match(after_prefix):
                warnings.append("Meeting filename should include date: 'Meeting - YYYY-MM-DD Title'")
            elif after_prefix:
                date_str = after_prefix[:10]
                if not ISO_DATE_PATTERN.match(date_str):
                    warnings.append(f"Invalid date format in filename: '{date_str}'")

    elif note_type == "Daily":
        # Should be just YYYY-MM-DD.md
        if not ISO_DATE_PATTERN.match(stem):
            warnings.append(f"Daily note filename should be YYYY-MM-DD.md, got '{stem}'")

        # Should be in year subfolder
        if folder != "root":
            # Check if in correct year folder
            year_match = re.search(r'(\d{4})', folder)
            date_match = ISO_DATE_PATTERN.match(stem)
            if year_match and date_match:
                folder_year = year_match.group(1)
                file_year = stem[:4]
                if folder_year != file_year:
                    warnings.append(f"Daily note year mismatch: file is {file_year} but in {folder_year}/ folder")

    # General naming conventions
    # Check for underscores (should use spaces)
    if '_' in stem and note_type not in ["Daily"]:
        warnings.append("Use spaces instead of underscores in filenames")

    # Check for lowercase where Title Case expected
    if expected_prefix and stem.startswith(expected_prefix.rstrip(" ")):
        title_part = stem[len(expected_prefix.rstrip(" ")):].strip()
        if title_part and title_part[0].islower():
            warnings.append("Title should start with uppercase")

    return warnings


def main():
    # Startup guard: exit gracefully if no valid input
    try:
        raw_input = sys.stdin.read()
        if not raw_input or not raw_input.strip():
            sys.exit(0)
        input_data = json.loads(raw_input)
    except (json.JSONDecodeError, ValueError, EOFError):
        sys.exit(0)
    except Exception:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    file_path = input_data.get("tool_input", {}).get("file_path", "")

    # Only check after Edit or Write on markdown files
    if tool_name not in ("Edit", "Write"):
        sys.exit(0)

    if not file_path or not file_path.endswith(".md"):
        sys.exit(0)

    # Only validate files inside the Obsidian vault.
    # Hooks fire for ALL Edit/Write operations regardless of target repo.
    # When working cross-repo (e.g. /tmp/claude/), skip silently to avoid
    # spurious naming convention warnings on non-vault files.
    VAULT_ROOT = "."
    if not file_path.startswith(VAULT_ROOT):
        sys.exit(0)

    # Skip template files and special directories
    skip_paths = ["Templates/", ".obsidian/", "node_modules/", ".claude/"]
    if any(skip in file_path for skip in skip_paths):
        sys.exit(0)

    # Read the file to get note type
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, OSError):
        sys.exit(0)

    note_type = extract_note_type(content)
    if not note_type:
        sys.exit(0)

    # Validate filename
    warnings = validate_filename(file_path, note_type)

    # Output using additionalContext JSON format
    if warnings:
        output_text = f"Filename check for {Path(file_path).name}:\n"
        for warning in warnings:
            output_text += f"   - {warning}\n"

        # Show expected pattern
        if note_type in FILENAME_CONVENTIONS:
            _, _, pattern_desc = FILENAME_CONVENTIONS[note_type]
            output_text += f"   Expected pattern: {pattern_desc}"

        output = {"additionalContext": output_text}
        print(json.dumps(output))

    # Always exit 0 - validation is non-blocking
    sys.exit(0)


if __name__ == "__main__":
    main()
