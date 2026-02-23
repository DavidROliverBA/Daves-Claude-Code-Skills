#!/bin/bash
# Auto-load context files based on skill commands and entity names in prompt.
# Hook Type: UserPromptSubmit
#
# Loads relevant context files when the user's prompt mentions
# skills, entities, or domain topics that have matching context files.

# Get vault root from environment or use CWD
VAULT_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CONTEXT_DIR="$VAULT_ROOT/.claude/context"

# Exit if no context directory
[[ ! -d "$CONTEXT_DIR" ]] && exit 0

# Read the user prompt from stdin
PROMPT=$(cat)

# Auto-load context based on keywords
LOADED=""

# Check for architecture-related prompts
if [[ "$PROMPT" =~ /adr|/architecture|/compliance|/hld|/nfr|ADR|architecture ]]; then
    [[ -f "$CONTEXT_DIR/architecture.md" ]] && LOADED="$LOADED architecture.md"
fi

# Check for project-specific prompts
if [[ "$PROMPT" =~ /project|project|programme ]]; then
    [[ -f "$CONTEXT_DIR/projects.md" ]] && LOADED="$LOADED projects.md"
fi

# Check for technology prompts
if [[ "$PROMPT" =~ /system|technology|platform|infrastructure ]]; then
    [[ -f "$CONTEXT_DIR/technology.md" ]] && LOADED="$LOADED technology.md"
fi

# Check for people/meeting prompts
if [[ "$PROMPT" =~ /meeting|/person|attendees|stakeholder ]]; then
    [[ -f "$CONTEXT_DIR/people.md" ]] && LOADED="$LOADED people.md"
fi

# Check for acronyms
if [[ "$PROMPT" =~ [A-Z]{3,} ]]; then
    [[ -f "$CONTEXT_DIR/acronyms.md" ]] && LOADED="$LOADED acronyms.md"
fi

# Check for organisation prompts
if [[ "$PROMPT" =~ vendor|partner|supplier|organisation ]]; then
    [[ -f "$CONTEXT_DIR/organisations.md" ]] && LOADED="$LOADED organisations.md"
fi

if [[ -n "$LOADED" ]]; then
    echo "Auto-loaded context:$LOADED"
fi

exit 0
