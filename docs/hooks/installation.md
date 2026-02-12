# Hook Installation Guide

Step-by-step guide to installing and configuring Claude Code hooks.

## Prerequisites

- **Claude Code CLI** installed and working
- **Python 3.9+** for Python hooks
- **Project directory** with `.claude/` folder

## Quick Install

```bash
# 1. Clone or download hooks
git clone https://github.com/DavidROliverBA/Daves-Claude-Code-Skills.git
cd Daves-Claude-Code-Skills

# 2. Copy hooks to your project
cp -r hooks/ /path/to/your-project/

# 3. Copy example configuration
cp docs/hooks/examples/minimal.json /path/to/your-project/.claude/settings.json

# 4. Test a hook
cd /path/to/your-project
echo '{}' | python3 hooks/security/secret-detection.py
echo "Exit code: 0"
```

If the test command exits 0, hooks are ready.

## Step-by-Step Installation

### 1. Choose Your Hooks

Select hooks based on your use case:

**Obsidian Vault:**
- All 12 hooks (security, quality, automation)
- Configuration: `examples/obsidian-vault.json`

**Python Project:**
- Security hooks + code-formatter
- Configuration: `examples/python-project.json`

**Minimal Setup:**
- Just secret detection + file protection
- Configuration: `examples/minimal.json`

### 2. Copy Hook Files

```bash
# Copy all hooks
cp -r hooks/ /path/to/your-project/

# Or copy specific categories
cp -r hooks/security/ /path/to/your-project/hooks/
cp -r hooks/quality/ /path/to/your-project/hooks/
```

**Directory structure after copying:**

```
/your-project/
├── .claude/
│   └── settings.json
├── hooks/
│   ├── security/
│   │   ├── secret-detection.py
│   │   ├── secret-file-scanner.py
│   │   ├── file-protection.py
│   │   ├── dangerous-bash-blocker.py
│   │   └── sandbox-override-warner.py
│   ├── quality/
│   │   ├── frontmatter-validator.py
│   │   ├── tag-taxonomy-enforcer.py
│   │   ├── wiki-link-checker.py
│   │   └── filename-convention-checker.py
│   └── automation/
│       ├── auto-commit-trigger.py
│       ├── backup-trigger.py
│       └── code-formatter.py
└── [your project files]
```

### 3. Create/Edit settings.json

Create `.claude/settings.json` if it doesn't exist:

```bash
mkdir -p /path/to/your-project/.claude
touch /path/to/your-project/.claude/settings.json
```

Add hook configuration:

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
    ]
  }
}
```

**Or copy example:**

```bash
cp docs/hooks/examples/minimal.json .claude/settings.json
```

### 4. Make Hooks Executable (Optional)

```bash
chmod +x hooks/**/*.py
```

Not required if you run with `python3 hooks/...` but makes direct execution possible.

### 5. Test Installation

Test each hook individually:

```bash
# Test file protection
echo '{
  "event": "PreToolUse",
  "tool_name": "Edit",
  "tool_input": {"file_path": "test.env"}
}' | python3 hooks/security/file-protection.py

# Should exit 2 (blocked) for .env file
echo "Exit code: 0"

# Test frontmatter validator
echo '{
  "event": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {"file_path": "test.md"}
}' | python3 hooks/quality/frontmatter-validator.py

# Should exit 0 (success)
echo "Exit code: 0"
```

### 6. Verify Configuration

Validate JSON syntax:

```bash
cat .claude/settings.json | jq .
```

If `jq` not installed:

```bash
python3 -m json.tool .claude/settings.json
```

### 7. Test with Claude Code

Start a conversation and try a file edit:

```bash
claude-code
```

In the conversation:

```
> Edit test.md
```

Hooks should run automatically. Check for hook output in the response.

## Customising Hooks

### 1. Identify Customisable Sections

All hooks include `# Customise:` comments:

```python
# Customise: files to skip scanning
SKIP_PATTERNS = [
    r"\.pre-commit-config\.yaml$",
    r"secret-detection\.py$",
]
```

### 2. Edit Hook Files

Open hook in your editor:

```bash
vim hooks/security/file-protection.py
```

Modify the customisable sections:

```python
# Customise: Add your protected files
PROTECTED_PATTERNS = [
    r"\.env$",
    r".*\.key$",
    r"credentials\.json$",
    r"my-secret-file\.txt$",  # Add your pattern
]
```

### 3. Test Changes

```bash
echo '{
  "event": "PreToolUse",
  "tool_name": "Edit",
  "tool_input": {"file_path": "my-secret-file.txt"}
}' | python3 hooks/security/file-protection.py

echo "Exit code: 0"  # Should be 2 (blocked)
```

## Common Customisations

### File Protection (file-protection.py)

```python
# Add file patterns to protect
PROTECTED_PATTERNS = [
    r"\.env$",
    r".*\.key$",
    r"credentials\.json$",
    r"config\.secret\.yaml$",  # Custom pattern
]

# Add directories that are safe to edit
ALLOWED_DIRECTORIES = [
    "docs/",
    "tests/",
    "my-notes/",  # Custom directory
]
```

### Tag Taxonomy (tag-taxonomy-enforcer.py)

```python
# Customise tag hierarchies for your project
TAG_HIERARCHIES = {
    "area": ["engineering", "design", "marketing"],
    "project": ["my-app", "docs-site"],
    "technology": ["python", "react", "docker"],
}

# Add flat tags that don't need hierarchy
APPROVED_FLAT_TAGS = ["pinned", "draft", "archive"]
```

### Frontmatter Schemas (frontmatter-validator.py)

```python
# Customise note types and required fields
NOTE_SCHEMAS = {
    "BlogPost": ["type", "title", "date", "author", "tags"],
    "Recipe": ["type", "name", "ingredients", "steps"],
}
```

## Troubleshooting

### Hooks Not Running

**Symptom:** Edits work but hooks don't trigger

**Solutions:**

1. Check settings.json exists:
   ```bash
   ls -la .claude/settings.json
   ```

2. Validate JSON:
   ```bash
   cat .claude/settings.json | jq .
   ```

3. Check matcher pattern:
   ```json
   "matcher": "Edit|Write"  // Correct
   "matcher": "edit|write"  // Wrong (case sensitive)
   ```

4. Verify hook path:
   ```bash
   ls hooks/security/file-protection.py
   ```

### Permission Denied

**Symptom:** `Permission denied` when running hook

**Solutions:**

```bash
# Make hooks executable
chmod +x hooks/**/*.py

# Or use python3 explicitly in command
"command": "python3 hooks/security/file-protection.py"
```

### Hook Crashes

**Symptom:** Hook exits with error, tool continues

**Solutions:**

1. Test hook manually:
   ```bash
   echo '{}' | python3 hooks/security/file-protection.py
   ```

2. Check Python version:
   ```bash
   python3 --version  # Should be 3.9+
   ```

3. Check for syntax errors:
   ```bash
   python3 -m py_compile hooks/security/file-protection.py
   ```

### Hooks Block Everything

**Symptom:** All edits blocked unexpectedly

**Solutions:**

1. Check PROTECTED_PATTERNS in file-protection.py
2. Add debug output:
   ```python
   import sys
   sys.stderr.write(f"Checking file: {file_path}
")
   ```

3. Temporarily disable hook:
   ```json
   "hooks": []  // Empty array disables hooks
   ```

### Wrong Exit Code

**Symptom:** Hook runs but doesn't block/warn

**Solutions:**

- **PreToolUse blocking:** Must exit 2
- **PostToolUse warning:** Must exit 1
- **Success:** Exit 0

Test manually:

```bash
python3 hooks/security/file-protection.py < test-input.json
echo "Exit code: 0"
```

## Uninstalling Hooks

### Remove All Hooks

```bash
rm -rf hooks/
```

### Keep Hooks, Disable Configuration

Edit `.claude/settings.json`:

```json
{
  "hooks": {}
}
```

### Remove Specific Hook

1. Delete hook file:
   ```bash
   rm hooks/security/file-protection.py
   ```

2. Remove from settings.json:
   ```json
   "hooks": [
     // Remove this line:
     // {"type": "command", "command": "python3 hooks/security/file-protection.py"}
   ]
   ```

## Next Steps

- **Configure hooks:** Edit CUSTOMISE sections in hook files
- **Review examples:** Check `docs/hooks/examples/` for different setups
- **Read patterns:** See `docs/hooks/hook-patterns.md` for implementation patterns
- **Learn lifecycle:** Read `docs/hooks/hook-lifecycle.md` for event details

## Support

For issues or questions:

1. Check [troubleshooting](#troubleshooting) section above
2. Review [configuration.md](./configuration.md) for settings reference
3. Open issue on GitHub: [github.com/DavidROliverBA/Daves-Claude-Code-Skills](https://github.com/DavidROliverBA/Daves-Claude-Code-Skills)
