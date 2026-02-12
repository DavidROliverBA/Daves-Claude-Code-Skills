#!/usr/bin/env python3
"""
Secret Detection Hook for Claude Code
Detects potential secrets in user prompts and blocks them from being sent.

Hook Type: UserPromptSubmit
Exit Codes:
  0 - Success (prompt is safe or decision output provided)
  1 - Error (non-blocking)
  2 - Block (blocking error)

Usage in settings.json:
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [{"type": "command", "command": "python3 hooks/security/secret-detection.py"}]
      }
    ]
  }
"""

import json
import re
import sys

# Patterns that indicate potential secrets
SECRET_PATTERNS = [
    (r"(?i)\b(password|passwd|pwd)\s*[:=]\s*\S+", "password"),
    (r"(?i)\b(secret|api_?secret)\s*[:=]\s*\S+", "secret"),
    (r"(?i)\b(api_?key|apikey)\s*[:=]\s*\S+", "API key"),
    (r"(?i)\b(token|auth_?token|access_?token)\s*[:=]\s*\S+", "token"),
    (r"(?i)\b(private_?key)\s*[:=]\s*\S+", "private key"),
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


def check_for_secrets(prompt: str) -> list[tuple[str, str]]:
    """Check prompt for potential secrets. Returns list of (match, type) tuples."""
    findings = []
    for pattern, secret_type in SECRET_PATTERNS:
        matches = re.findall(pattern, prompt)
        if matches:
            findings.append((secret_type, len(matches)))
    return findings


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input or not raw_input.strip():
            print('{}')
            sys.exit(0)
        input_data = json.loads(raw_input)
    except (json.JSONDecodeError, ValueError, EOFError):
        print('{}')
        sys.exit(0)
    except Exception:
        print('{}')
        sys.exit(0)

    prompt = input_data.get("userPrompt", "")
    if not prompt:
        print('{}')
        sys.exit(0)

    findings = check_for_secrets(prompt)

    if findings:
        secret_types = [f"{stype} ({count}x)" for stype, count in findings]
        warning = f"Potential secrets detected: {', '.join(secret_types)}"
        output = {
            "decision": "block",
            "reason": f"⚠️ {warning}\n\nPlease remove sensitive information before sending."
        }
        print(json.dumps(output))
        sys.exit(0)

    print('{}')
    sys.exit(0)


if __name__ == "__main__":
    main()
