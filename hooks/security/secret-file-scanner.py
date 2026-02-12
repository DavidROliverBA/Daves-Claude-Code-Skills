#!/usr/bin/env python3
"""
Secret File Scanner Hook for Claude Code
Scans file content being written for potential secrets.

Hook Type: PreToolUse
Matcher: Edit|Write
Exit Codes:
  0 - Success (content is safe to write)
  2 - Block (secrets detected in content)

Usage in settings.json:
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{"type": "command", "command": "python3 hooks/security/secret-file-scanner.py"}]
      }
    ]
  }
"""

import json
import re
import sys

SECRET_PATTERNS = [
    (r"(?i)(password|passwd|pwd)\s*[:=]\s*\S+", "password"),
    (r"(?i)(secret|api_?secret)\s*[:=]\s*\S+", "secret"),
    (r"(?i)(api_?key|apikey)\s*[:=]\s*\S+", "API key"),
    (r"(?i)(token|auth_?token|access_?token)\s*[:=]\s*\S+", "token"),
    (r"(?i)(private_?key)\s*[:=]\s*\S+", "private key"),
    (r"sk-[a-zA-Z0-9]{20,}", "OpenAI API key"),
    (r"sk-ant-[a-zA-Z0-9-]{20,}", "Anthropic API key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token"),
    (r"gho_[a-zA-Z0-9]{36}", "GitHub OAuth token"),
    (r"ghs_[a-zA-Z0-9]{36}", "GitHub server token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key ID"),
    (r"(?i)aws_secret_access_key\s*[:=]\s*\S+", "AWS secret key"),
    (r"ntn_[a-zA-Z0-9]{40,}", "Notion integration token"),
    (r"secret_[a-zA-Z0-9]{40,}", "Notion internal token"),
    (r"(?i)atlassian[-_]?token\s*[:=]\s*\S+", "Atlassian token"),
    (r"(?i)confluence[-_]?token\s*[:=]\s*\S+", "Confluence token"),
    (r"(?i)jira[-_]?token\s*[:=]\s*\S+", "Jira token"),
    (r"ATATT[a-zA-Z0-9]{20,}", "Atlassian API token"),
    (r"xox[baprs]-[0-9A-Za-z\-]{10,}", "Slack token"),
    (r"AIza[0-9A-Za-z\-_]{35}", "Google API key"),
    (r"(?i)bearer\s+[a-zA-Z0-9\-_\.]{20,}", "Bearer token"),
    (r"(?i)(mongodb|postgres|mysql|redis)://[^\s]+:[^\s]+@", "database connection string"),
    (r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----", "private key (PEM)"),
    (r"-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----", "SSH private key"),
    (r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9+/=]{32,}['\"]?", "high-entropy credential"),
]

# Customise: files to skip scanning
SKIP_PATTERNS = [
    r"\.pre-commit-config\.yaml$",
    r"secret-detection\.py$",
    r"secret-file-scanner\.py$",
    r"file-protection\.py$",
    r"\.secrets\.baseline$",
    r"CLAUDE\.md$",
    r"README\.md$",
    r"docs/.*\.md$",
]


def should_skip_file(file_path: str) -> bool:
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, file_path):
            return True
    return False


def check_content_for_secrets(content: str) -> list[tuple[str, int]]:
    findings = []
    for pattern, secret_type in SECRET_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            findings.append((secret_type, len(matches)))
    return findings


def main():
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
    tool_input = input_data.get("tool_input", {})

    if tool_name not in ("Edit", "Write"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if should_skip_file(file_path):
        sys.exit(0)

    content = ""
    if tool_name == "Write":
        content = tool_input.get("content", "")
    elif tool_name == "Edit":
        content = tool_input.get("new_string", "")

    if not content:
        sys.exit(0)

    findings = check_content_for_secrets(content)

    if findings:
        secret_types = [f"{stype} ({count}x)" for stype, count in findings]
        warning = f"Potential secrets detected in file content: {', '.join(secret_types)}"
        output = {
            "decision": "block",
            "reason": f"⚠️ {warning}\n\nFile: {file_path}\n\nPlease remove sensitive data before writing."
        }
        print(json.dumps(output))
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
