#!/bin/bash
# Hook: Suggest graph search before Grep
# Type: PreToolUse
# Matcher: Grep

# Read the tool input from stdin
INPUT=$(cat)

# Extract the search pattern from the Grep tool call
PATTERN=$(echo "$INPUT" | jq -r '.tool_input.pattern // empty')

# If pattern looks like a simple keyword search, suggest graph first
if [[ -n "$PATTERN" && ! "$PATTERN" =~ [\[\]\(\)\{\}\*\+\?\\] ]]; then
  # Simple pattern without regex - graph might be better
  # Escape the pattern for safe JSON embedding
  ESCAPED_PATTERN=$(echo "$PATTERN" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g; s/\n/\\n/g')
  cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "message": "💡 Tip: For keyword searches, the graph index is faster. Try:\n   node .claude/scripts/graph-query.js --search \"${ESCAPED_PATTERN}\"\n   or /graph-query ${ESCAPED_PATTERN}"
  }
}
EOF
else
  # Complex regex - let Grep proceed
  echo '{}'
fi
