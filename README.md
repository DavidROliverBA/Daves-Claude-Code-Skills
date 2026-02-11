# Dave's Claude Code Skills

A curated collection of [Claude Code](https://claude.ai/code) skills for software architecture and engineering. Drop these `.md` files into your `.claude/skills/` directory and invoke them as slash commands.

## Skills

### Diagramming

Skills for generating and reviewing architecture diagrams. Based on graph drawing research (Purchase et al.) and real-world C4 modelling experience.

| Skill | Command | Description |
|-------|---------|-------------|
| [Diagram](skills/diagramming/diagram.md) | `/diagram` | Generate architecture diagrams in multiple formats (C4, system landscape, data flow, AWS). Automatically applies tier-based declaration ordering and validates readability. |
| [C4 Diagram](skills/diagramming/c4-diagram.md) | `/c4-diagram` | Specialised C4 diagram generation. Three output formats: native Mermaid C4, flowchart LR with C4 styling, and PlantUML with directional hints. Built-in antipattern avoidance. |
| [Diagram Review](skills/diagramming/diagram-review.md) | `/diagram-review` | Analyse existing diagrams for readability and architecture quality. Uses four parallel analysis agents for component extraction, relationship mapping, pattern analysis, and technology identification. |

## Examples

Worked examples with prompts, outputs, and explanations of what makes each diagram good (or bad).

### Diagramming Examples

| Example | What It Shows |
|---------|---------------|
| [Declaration Order](examples/diagramming/01-declaration-order.md) | Why element declaration order is the single most important factor for diagram readability. Side-by-side comparison of the same 9 elements in random vs. structured order. |
| [C4 Context Diagram](examples/diagramming/02-c4-context-diagram.md) | How to create a clean Level 1 C4 diagram showing actors, system boundary, and external dependencies. |
| [C4 Container Diagram](examples/diagramming/03-c4-container-diagram.md) | How to create a Level 2 C4 diagram with system boundaries, technology labels, and database shapes. Includes PlantUML alternative. |
| [C4 Component Diagram](examples/diagramming/04-c4-component-diagram.md) | How to diagram internal components (controllers, services, repositories) at C4 Level 3. |
| [Real-World Example](examples/diagramming/05-real-world-example.md) | Complete Context + Container diagrams for a real AI-powered incident management platform. |

### Example Screenshots

All examples include rendered diagram screenshots:

| | | |
|---|---|---|
| ![Bad order](examples/diagramming/images/03-bad-declaration-order.png) | ![Good order](examples/diagramming/images/04-good-declaration-order.png) | ![Context](examples/diagramming/images/05-good-context-diagram.png) |
| Bad declaration order | Good declaration order | C4 Context |
| ![Container](examples/diagramming/images/02-good-structured-container.png) | ![Component](examples/diagramming/images/06-good-component-diagram.png) | ![Real-world](examples/diagramming/images/07-dispax-context.png) |
| C4 Container | C4 Component | Real-world Context |

## Installation

1. Copy the skill files you want into your project's `.claude/skills/` directory:

```bash
# Copy all diagramming skills
mkdir -p .claude/skills
cp skills/diagramming/*.md .claude/skills/
```

2. Invoke them in Claude Code:

```
/diagram c4-context
/c4-diagram MySystem container flowchart
/diagram-review path/to/diagram.png
```

## Key Concepts

These skills are built on three key insights from graph drawing research:

1. **Declaration order controls layout.** The Dagre (Mermaid) and Sugiyama (PlantUML) algorithms position elements based on where they appear in the code. Declare elements in reading order — actors left, data stores right.

2. **Edge crossings are the strongest predictor of comprehension difficulty.** Research by Helen Purchase showed reducing crossings improves reader accuracy by 30-40%. Always set an explicit crossing target.

3. **Gestalt proximity overrides colour.** Elements placed close together are perceived as related, regardless of styling. Use subgraphs and boundaries to group related components.

## Blog Post

For a detailed writeup of the theory behind these skills, see [Why Your AI-Generated Diagrams Look Terrible (And How to Fix Them)](docs/blog-post.md).

## Contributing

Contributions welcome. To add a new skill:

1. Create a `.md` file in the appropriate `skills/<category>/` directory
2. Follow the existing skill format (usage, instructions, examples, validation)
3. Add a worked example in `examples/<category>/`
4. Update this README

## Licence

MIT
