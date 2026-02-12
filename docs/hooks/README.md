# Claude Code Hooks Guide

Hooks allow you to customise and extend Claude Code's behaviour by running custom scripts at specific lifecycle events. This guide covers the 12 production-ready hooks in this repository.

## Quick Start

1. Copy hooks to your project: `cp -r hooks/ /your-project/`
2. Add hook configuration to `.claude/settings.json`
3. Test: `echo '{}' | python3 hooks/security/secret-detection.py`

See [installation.md](./installation.md) for detailed setup instructions.

## Available Hooks

### Security (5 hooks)

| Hook | Type | Purpose | Exit Code |
|------|------|---------|-----------|
| **secret-detection.py** | PreToolUse | Scans git commits for secrets using detect-secrets | 2 = block |
| **secret-file-scanner.py** | PreToolUse | Scans file content for API keys, tokens, passwords | 2 = block |
| **file-protection.py** | PreToolUse | Blocks edits to .env, lockfiles, private keys | 2 = block |
| **dangerous-bash-blocker.py** | PreToolUse | Blocks destructive bash commands (rm -rf, dd, etc.) | 2 = block |
| **sandbox-override-warner.py** | PreToolUse | Warns when dangerouslyDisableSandbox is used | 0 = warn only |

### Quality (4 hooks)

| Hook | Type | Purpose | Exit Code |
|------|------|---------|-----------|
| **frontmatter-validator.py** | PostToolUse | Validates YAML frontmatter against note schemas | 1 = warn |
| **tag-taxonomy-enforcer.py** | PostToolUse | Enforces hierarchical tag taxonomy | 1 = warn |
| **wiki-link-checker.py** | PostToolUse | Validates [[wiki-links]] point to existing files | 1 = warn |
| **filename-convention-checker.py** | PostToolUse | Validates filenames match note type conventions | 1 = warn |

### Automation (2 hooks)

| Hook | Type | Purpose | Exit Code |
|------|------|---------|-----------|
| **auto-commit-trigger.py** | PostToolUse | Auto-creates commits after significant changes | 0 = success |
| **backup-trigger.py** | PostToolUse | Triggers backups after Edit/Write operations | 0 = success |

### Development (1 hook)

| Hook | Type | Purpose | Exit Code |
|------|------|---------|-----------|
| **code-formatter.py** | PostToolUse | Formats Python/JS/TS code with black/prettier | 0 = success |

## Hook Types

- **PreToolUse**: Runs before a tool executes (can block with exit code 2)
- **PostToolUse**: Runs after a tool executes (can warn with exit code 1)
- **UserPromptSubmit**: Runs when user submits a prompt
- **Stop**: Runs when conversation ends

See [hook-lifecycle.md](./hook-lifecycle.md) for complete event reference.

## How Hooks Work

1. **Event occurs**: Claude Code triggers an event (e.g., user calls Edit tool)
2. **Matcher checks**: Event type and tool name are matched against hook configuration
3. **Hooks execute**: All matching hooks run in sequence
4. **Decision made**: Based on exit codes (0 = allow, 1 = warn, 2 = block)

### Exit Code Behaviour

| Exit Code | Meaning | Effect |
|-----------|---------|--------|
| **0** | Success | Continue normal operation |
| **1** | Warning | Show message but continue |
| **2** | Block | Prevent tool from executing |

## Configuration

Hooks are configured in :

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {"type": "command", "command": "python3 hooks/security/file-protection.py"}
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {"type": "command", "command": "python3 hooks/quality/frontmatter-validator.py"}
        ]
      }
    ]
  }
}
```

See [configuration.md](./configuration.md) for complete reference.

## Common Patterns

- **Blocking validation**: Use PreToolUse with exit code 2
- **Post-processing**: Use PostToolUse to format/validate after tool runs
- **Warning notifications**: Exit code 1 for non-blocking warnings
- **Auto-detection**: Hooks auto-detect project root via .obsidian/.git

See [hook-patterns.md](./hook-patterns.md) for detailed patterns.

## Customisation

All hooks include `CUSTOMISE` comments marking configurable sections:

```python
# Customise: files to skip scanning
SKIP_PATTERNS = [
    r"\.pre-commit-config\.yaml$",
    r"secret-detection\.py$",
]
```

Common customisations:
- **Protected files**: file-protection.py → PROTECTED_PATTERNS
- **Tag taxonomy**: tag-taxonomy-enforcer.py → TAG_HIERARCHIES
- **Note schemas**: frontmatter-validator.py → NOTE_SCHEMAS
- **Secret patterns**: secret-file-scanner.py → SECRET_PATTERNS

## Example Configurations

- [obsidian-vault.json](./examples/obsidian-vault.json) — All 12 hooks for Obsidian vault
- [python-project.json](./examples/python-project.json) — Security + code formatting
- [minimal.json](./examples/minimal.json) — Just secret detection + file protection

## Further Reading

- [Hook Lifecycle](./hook-lifecycle.md) — Events, I/O schemas, exit codes
- [Hook Patterns](./hook-patterns.md) — Common implementation patterns
- [Configuration Reference](./configuration.md) — settings.json syntax
- [Installation Guide](./installation.md) — Setup and troubleshooting

## License

MIT License — see LICENSE file for details.
