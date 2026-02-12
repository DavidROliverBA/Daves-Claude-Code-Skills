#!/bin/bash
# Context Loader Hook for Claude Code
# Detects skill commands in user prompts and auto-loads relevant context files.
#
# Hook Type: UserPromptSubmit
# Input: JSON via stdin with "userPrompt" field
# Output: JSON with additionalContext field (or empty {} for no context)
#
# Usage in settings.json:
#   "hooks": {
#     "UserPromptSubmit": [
#       {
#         "matcher": "",
#         "hooks": [{"type": "command", "command": "bash hooks/ux/context-loader.sh"}]
#       }
#     ]
#   }
#
# CUSTOMISE: Edit the skill-to-context mappings below for your project.
# Context files should live in .claude/context/ relative to your project root.

set -e

# Auto-detect project root (walk up to find .git or .claude)
find_project_root() {
    local dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        if [[ -d "$dir/.git" ]] || [[ -d "$dir/.claude" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

PROJECT_ROOT=$(find_project_root) || exit 0
CONTEXT_DIR="$PROJECT_ROOT/.claude/context"
CONTEXTS_TO_LOAD=()

# Read JSON input from stdin
INPUT=$(cat)

# Extract the prompt from JSON input
PROMPT=$(echo "$INPUT" | jq -r '.userPrompt // empty')

# Exit early if no prompt
if [[ -z "$PROMPT" ]]; then
    echo '{}'
    exit 0
fi

# Function to queue a context file for loading
queue_context() {
    local file="$CONTEXT_DIR/$1"
    if [[ -f "$file" ]]; then
        CONTEXTS_TO_LOAD+=("$file")
    fi
}

# Map skill commands and keywords to context files
PROMPT_LOWER=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

# People-related skills
if [[ "$PROMPT_LOWER" =~ /person|/meeting|/team ]]; then
    queue_context "people.md"
fi

# Project-related skills
if [[ "$PROMPT_LOWER" =~ /project|/task|/status ]]; then
    queue_context "projects.md"
fi

# Architecture and decisions
if [[ "$PROMPT_LOWER" =~ /adr|/decision|/architecture ]]; then
    queue_context "architecture.md"
fi

# Technology-related skills
if [[ "$PROMPT_LOWER" =~ /weblink|/reference|/tool ]]; then
    queue_context "technology.md"
fi

# Search - load multiple contexts
if [[ "$PROMPT_LOWER" =~ /search|/find|/related ]]; then
    queue_context "projects.md"
    queue_context "people.md"
    queue_context "technology.md"
fi

# If no contexts to load, output empty JSON and exit
if [[ ${#CONTEXTS_TO_LOAD[@]} -eq 0 ]]; then
    echo '{}'
    exit 0
fi

# Remove duplicates from the array
UNIQUE_CONTEXTS=($(printf '%s\n' "${CONTEXTS_TO_LOAD[@]}" | sort -u))

# Build the context content
CONTEXT_CONTENT=""
for file in "${UNIQUE_CONTEXTS[@]}"; do
    if [[ -f "$file" ]]; then
        CONTEXT_CONTENT+="
<!-- Auto-loaded context: $(basename "$file") -->
$(cat "$file")
<!-- End: $(basename "$file") -->
"
    fi
done

# If we have context to add, output it as JSON
if [[ -n "$CONTEXT_CONTENT" ]]; then
    ESCAPED_CONTENT=$(echo "$CONTEXT_CONTENT" | jq -Rs .)

    cat << JSONEOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": $ESCAPED_CONTENT
  }
}
JSONEOF
fi

exit 0
