#!/bin/bash
# Desktop Notification Hook for Claude Code
# Sends a desktop notification when Claude completes a task or stops.
#
# Supports macOS (osascript) and Linux (notify-send).
#
# Hook Type: PostToolUse or Stop
# Matcher: (any — typically used on Stop event)
# Exit Codes:
#   0 - Always (notification is best-effort)
#
# Usage in settings.json:
#   "hooks": {
#     "Stop": [
#       {
#         "matcher": "",
#         "hooks": [{"type": "command", "command": "bash hooks/notification/desktop-notify.sh"}]
#       }
#     ]
#   }
#
# CUSTOMISE: Change the notification title and message below.

TITLE="Claude Code"
MESSAGE="Task completed"

# Read input from stdin (Stop hook provides session context)
INPUT=$(cat 2>/dev/null || echo '{}')

# Try to extract a meaningful message from the hook input
STOP_REASON=$(echo "$INPUT" | jq -r '.stopReason // empty' 2>/dev/null)
if [[ -n "$STOP_REASON" ]]; then
    MESSAGE="Session ended: $STOP_REASON"
fi

# macOS notification
if command -v osascript &>/dev/null; then
    osascript -e "display notification "$MESSAGE" with title "$TITLE"" 2>/dev/null
    exit 0
fi

# Linux notification (requires notify-send from libnotify)
if command -v notify-send &>/dev/null; then
    notify-send "$TITLE" "$MESSAGE" --urgency=normal 2>/dev/null
    exit 0
fi

# No notification tool available — exit silently
exit 0
