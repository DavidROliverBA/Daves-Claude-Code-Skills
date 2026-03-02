#!/usr/bin/env python3
"""
Tag Taxonomy Enforcer Hook for Claude Code
Ensures tags follow the hierarchical taxonomy defined in tag-taxonomy.md.

Hook Type: PostToolUse
Matcher: Edit|Write
Exit Codes:
  0 - Always (non-blocking, provides warnings via stdout)
"""

import json
import re
import sys
from pathlib import Path

# Valid hierarchical tag prefixes
VALID_HIERARCHIES = {
    "activity": [
        "architecture", "implementation", "research", "evaluation",
        "operations", "delivery", "governance", "documentation",
        "modernisation", "integration", "compliance", "planning"
    ],
    "domain": [
        "engineering", "data", "integration", "cloud", "security",
        "aviation", "operations", "hr", "finance", "supply-chain",
        "maintenance", "planning", "documentation", "tooling",
        "platform", "identity", "analytics", "compliance", "infrastructure"
    ],
    "project": [
        "axia", "caerus", "dispax-ai", "cyber-uplift", "odie",
        "mro-pro", "777x", "rfid-scanners", "ecp", "snapon", "datasphere"
        # Note: New projects can be added - this list is not exhaustive
    ],
    "technology": [
        # Platforms & Cloud
        "aws", "azure", "sap", "btp", "ui5", "datasphere", "s4hana",
        # Data & Integration
        "kafka", "snowflake", "mq", "api", "kong", "axway",
        # AI & ML
        "bedrock", "langchain", "ai", "ml",
        # Databases
        "oracle", "postgresql", "redis", "dynamodb",
        # Infrastructure
        "kubernetes", "docker", "terraform", "lambda",
        # Applications
        "amos", "ews", "mro-software", "saas",
        # Languages/Frameworks
        "python", "javascript", "typescript", "java", "go", "rust"
    ],
    "type": [
        "adr", "system", "scenario", "integration", "data-source", "data-asset",
        "hld", "lld", "runbook", "policy", "guardrail", "diagram", "canvas"
    ],
    "status": ["draft", "review", "approved", "deprecated", "archived", "synced"],
    "workstream": [
        "rfi-scoring", "vendor-selection", "architecture", "integration",
        "data-migration", "testing", "training", "governance"
        # Note: New workstreams can be added - this list is not exhaustive
    ],
}

# Approved special flat tags (no hierarchy required)
APPROVED_FLAT_TAGS = [
    "notion-import", "pdf-import", "ecp", "moc", "daily", "video", "automation"
]

# Minimum recommended tags by note type
MINIMUM_TAGS = {
    "ADR": {"required": ["activity"], "recommended": ["technology", "domain"]},
    "Project": {"required": ["project"], "recommended": ["domain"]},
    "System": {"required": ["type"], "recommended": ["domain", "technology"]},
    "Concept": {"required": [], "recommended": ["activity", "domain"]},
    "Pattern": {"required": [], "recommended": ["activity", "domain"]},
    "Meeting": {"required": [], "recommended": ["project", "domain"]},
    "Incubator": {"required": ["activity"], "recommended": ["domain"]},
    "Research": {"required": ["activity"], "recommended": ["domain"]},
    "Reference": {"required": [], "recommended": ["domain"]},
    "Threat": {"required": ["domain"], "recommended": ["technology"]},
    "Framework": {"required": [], "recommended": ["domain"]},
    "Tool": {"required": [], "recommended": ["domain", "technology"]},
    "Objective": {"required": [], "recommended": ["domain"]},
    "Task": {"required": [], "recommended": ["project"]},
    "Email": {"required": [], "recommended": ["project"]},
    "Trip": {"required": [], "recommended": []},
    "DataAsset": {"required": ["domain"], "recommended": ["technology"]},
    "Department": {"required": [], "recommended": ["domain"]},
}


def extract_tags(content: str) -> list[str]:
    """Extract tags from frontmatter."""
    # Find frontmatter
    if not content.startswith("---"):
        return []

    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return []

    frontmatter = content[4:end_match.start() + 3]

    # Find tags line(s)
    tags = []

    # Match inline array: tags: [tag1, tag2]
    inline_match = re.search(r'tags:\s*\[(.*?)\]', frontmatter, re.DOTALL)
    if inline_match:
        tags_str = inline_match.group(1)
        # Split by comma, clean up
        for tag in tags_str.split(','):
            tag = tag.strip().strip('"\'')
            if tag:
                tags.append(tag)
        return tags

    # Match multi-line array
    multiline_match = re.search(r'tags:\s*\n((?:\s+-\s+.*\n?)+)', frontmatter)
    if multiline_match:
        for line in multiline_match.group(1).split('\n'):
            if line.strip().startswith('-'):
                tag = line.strip()[1:].strip().strip('"\'')
                if tag:
                    tags.append(tag)

    return tags


def extract_note_type(content: str) -> str:
    """Extract note type from frontmatter."""
    match = re.search(r'type:\s*(\w+)', content)
    return match.group(1) if match else ""


def validate_tag(tag: str) -> tuple[bool, str]:
    """
    Validate a single tag.
    Returns (is_valid, warning_message).
    """
    # Check for # prefix (should not be in frontmatter)
    if tag.startswith('#'):
        return False, f"Tag should not have # prefix in frontmatter: {tag}"

    # Check for uppercase (should be lowercase)
    if tag != tag.lower():
        return False, f"Tag should be lowercase: {tag} → {tag.lower()}"

    # Check if it's an approved flat tag
    if tag in APPROVED_FLAT_TAGS:
        return True, ""

    # Check if it's hierarchical
    if '/' not in tag:
        return False, f"Tag should be hierarchical (use prefix/value): {tag}"

    # Parse hierarchy
    parts = tag.split('/')
    if len(parts) > 3:
        return False, f"Tag has too many levels (max 3): {tag}"

    prefix = parts[0]
    value = parts[1] if len(parts) > 1 else ""

    # Check if prefix is valid
    if prefix not in VALID_HIERARCHIES:
        valid_prefixes = ", ".join(sorted(VALID_HIERARCHIES.keys()))
        return False, f"Unknown tag prefix '{prefix}' in {tag}. Valid: {valid_prefixes}"

    # Check if value is in known list (warning only for unknown values)
    # Some hierarchies like project/ can have new values
    known_values = VALID_HIERARCHIES[prefix]
    if value and value not in known_values:
        # For project/ and technology/, unknown values are just info
        if prefix in ["project", "technology", "workstream"]:
            return True, f"Note: '{value}' is not in known {prefix}/ values (may be new)"
        else:
            return False, f"Unknown value '{value}' for {prefix}/. Known: {', '.join(known_values[:5])}..."

    return True, ""


def check_tag_coverage(tags: list[str], note_type: str) -> list[str]:
    """Check if note has recommended tag coverage."""
    warnings = []

    if note_type not in MINIMUM_TAGS:
        return warnings

    requirements = MINIMUM_TAGS[note_type]
    present_prefixes = set()

    for tag in tags:
        if '/' in tag:
            present_prefixes.add(tag.split('/')[0])

    # Check required
    for prefix in requirements.get("required", []):
        if prefix not in present_prefixes:
            warnings.append(f"Missing recommended tag prefix for {note_type}: {prefix}/")

    # Check recommended (softer warning)
    missing_recommended = []
    for prefix in requirements.get("recommended", []):
        if prefix not in present_prefixes:
            missing_recommended.append(f"{prefix}/")

    if missing_recommended:
        warnings.append(f"Consider adding tags: {', '.join(missing_recommended)}")

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
        # Any other error during startup - exit gracefully
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
    # spurious tag warnings on non-vault files.
    VAULT_ROOT = "."
    if not file_path.startswith(VAULT_ROOT):
        sys.exit(0)

    # Skip template files and special directories
    skip_paths = ["Templates/", ".obsidian/", "node_modules/", ".claude/"]
    if any(skip in file_path for skip in skip_paths):
        sys.exit(0)

    # Read the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, OSError):
        sys.exit(0)

    # Extract tags and note type
    tags = extract_tags(content)
    note_type = extract_note_type(content)

    if not tags:
        # No tags is not necessarily an error
        sys.exit(0)

    warnings = []
    infos = []

    # Validate each tag
    for tag in tags:
        is_valid, message = validate_tag(tag)
        if message:
            if message.startswith("Note:"):
                infos.append(message)
            else:
                warnings.append(message)

    # Check tag coverage
    coverage_warnings = check_tag_coverage(tags, note_type)
    warnings.extend(coverage_warnings)

    # Output using v2.1.9 additionalContext
    if warnings or infos:
        output_text = f"🏷️  Tag validation for {Path(file_path).name}:\n"
        for warning in warnings:
            output_text += f"   ⚠️  {warning}\n"
        for info in infos:
            output_text += f"   ℹ️  {info}\n"

        # Return additionalContext to inform Claude about tag issues
        output = {
            "additionalContext": output_text.strip()
        }
        print(json.dumps(output))

    # Always exit 0 - validation is non-blocking
    sys.exit(0)


if __name__ == "__main__":
    main()
