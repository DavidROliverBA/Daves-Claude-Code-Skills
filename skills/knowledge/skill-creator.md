---
description: Generate new Claude Code skill files following the standard template with agent team patterns
model: sonnet
---

# /skill-creator

Generate new Claude Code skill files following the standard skill template. Supports creating simple sequential skills and complex agent team skills with fan-out/fan-in, batch processing, or triage patterns.

## When to Use This Skill

- Creating a new Claude Code skill from scratch
- Converting a manual workflow into an automated skill
- Creating a skill with parallel agent teams
- Standardising existing skills to the template format
- Prototyping a new skill idea

## Usage

```
/skill-creator "<skill-name>" [--pattern simple|fan-out|batch|triage] [--model haiku|sonnet|opus]
```

### Parameters

| Parameter   | Description                                          | Required |
|-------------|------------------------------------------------------|----------|
| `name`      | Name for the skill (becomes the slash command)       | Yes      |
| `--pattern` | Orchestration pattern (default: `simple`)            | No       |
| `--model`   | Default model for the skill (default: `sonnet`)      | No       |

## Instructions

### Phase 1: Gather Skill Requirements

Prompt the user for:

| Field              | Description                                    | Example                               |
|--------------------|------------------------------------------------|---------------------------------------|
| **Purpose**        | What does this skill do?                       | Score RFI responses against a rubric  |
| **Trigger**        | When should someone use it?                    | Evaluating vendor submissions         |
| **Inputs**         | What does it need from the user?               | Document path, rubric, scale          |
| **Outputs**        | What does it produce?                          | Scorecard with evidence-based ratings |
| **Pattern**        | How should it execute?                         | Fan-out (4 agents score sections)     |
| **Agent count**    | How many parallel agents? (if applicable)      | 4                                     |
| **Agent purpose**  | What does each agent do? (if applicable)       | Score one section of the document     |

### Phase 2: Generate Skill File

Based on the pattern, generate the skill file:

#### Simple Pattern

```markdown
---
description: <one-line description>
model: <model>
---

# /<skill-name>

<Purpose paragraph>

## When to Use This Skill

- <Use case 1>
- <Use case 2>

## Usage

/<skill-name> <required-arg> [optional-arg]

### Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `arg1`    | What it is  | Yes      |

## Instructions

### Phase 1: <Setup>
<Steps>

### Phase 2: <Execute>
<Steps>

### Phase 3: <Output>
<Steps>

## Output Format

<Template>

## Examples

### Example 1
<Example>

---

**Invoke with:** `/<skill-name> <args>`
```

#### Fan-Out Pattern

Adds the agent team section:

```markdown
### Phase 2: Parallel Analysis — Agent Team

Launch N agents simultaneously using the Task tool.

**Agent 1: <Name>** (<Model>)
Task: <Purpose>
- <Step 1>
- <Step 2>
Return: <What this agent produces>

**Agent 2: <Name>** (<Model>)
...

### Phase 3: Synthesise Results

Combine all agent results:
1. <How to combine>
2. <How to present>
```

#### Batch Pattern

```markdown
### Phase 2: Batch Processing — Agent Team

Divide items into batches of N per agent. Launch parallel agents.

**Agent 1-N: <Name>** (<Model>)
Task: Process assigned batch
- For each item in the batch:
  1. <Step 1>
  2. <Step 2>
Return: <Output per item>
```

#### Triage Pattern

```markdown
### Phase 2: Triage — Agent Team (Parallel Haiku Agents)

**Agent 1-N: Triage Agent** (Haiku)
Task: Quick-assess items
- Score relevance (1-10)
- Categorise: must-process, worth-processing, skip
Return: Scores and categories

### Phase 3: Deep Processing — Agent Team (Selective Sonnet Agents)

Only for items scoring above threshold:

**Agent 1-N: Deep Analyst** (Sonnet)
Task: Full analysis
Return: Detailed output
```

### Phase 3: Review and Save

1. **Present the generated skill** for user review
2. **Validate** against the skill template checklist:
   - Has YAML frontmatter with `description` and `model`
   - Has When to Use, Usage, Instructions, Output Format, and Examples sections
   - Agent teams have clear inputs, steps, and return values
   - All examples are generic (no company-specific references)
   - UK English throughout
3. **Save** to the specified location

## Output Format

The generated `.md` file following the appropriate pattern template.

## Examples

### Example 1: Simple Skill

```
/skill-creator "meeting-notes" --pattern simple --model sonnet
```

Generates a simple sequential skill for creating meeting notes.

### Example 2: Fan-Out Skill

```
/skill-creator "impact-analysis" --pattern fan-out --model sonnet
```

Generates a skill with 4 parallel analysis agents.

### Example 3: Batch Processing Skill

```
/skill-creator "auto-tag" --pattern batch --model haiku
```

Generates a batch processing skill for tagging notes in parallel.

---

**Invoke with:** `/skill-creator "<name>"` to generate a new Claude Code skill file
