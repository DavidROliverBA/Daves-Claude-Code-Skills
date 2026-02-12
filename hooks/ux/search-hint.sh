#!/bin/bash
# Search Hint Hook for Claude Code
# Suggests faster search alternatives when Claude uses Grep for simple keywords.
#
# Hook Type: PreToolUse
# Matcher: Grep
# Input: JSON via stdin with tool_input.pattern
# Output: JSON with message hint (or empty {} to proceed silently)
#
# Usage in settings.json:
#   "hooks": {
#     "PreToolUse": [
#       {
#         "matcher": "Grep",
#         "hooks": [{"type": "command", "command": "bash hooks/ux/search-hint.sh"}]
#       }
#     ]
#   }
#
# CUSTOMISE: Replace the hint message with your project's preferred search tool
# (e.g. a SQLite FTS index, ripgrep wrapper, or custom search script).

# Read the tool input from stdin
INPUT=$(cat)

# Extract the search pattern from the Grep tool call
PATTERN=$(echo "$INPUT" | jq -r '.tool_input.pattern // empty')

# If pattern looks like a simple keyword search (no regex), suggest alternatives
if [[ -n "$PATTERN" && ! "$PATTERN" =~ [\[\]\(\)\{\}\*\+\?\\] ]]; then
  # Simple pattern without regex — a dedicated search tool might be faster
  # Escape the pattern for safe JSON embedding
  ESCAPED_PATTERN=$(echo "$PATTERN" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g; s/\n/\\n/g')
  cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "message": "Tip: For simple keyword searches, consider using a dedicated search index if available.\n   Pattern: ${ESCAPED_PATTERN}"
  }
}
EOF
else
  # Complex regex — let Grep proceed without comment
  echo '{}'
fi
