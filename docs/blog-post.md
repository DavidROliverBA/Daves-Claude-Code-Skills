# Why Your AI-Generated Diagrams Look Terrible (And How to Fix Them)

*David Oliver, Solutions Architect*

You asked Claude to "generate a C4 diagram for my order processing system." It produced fifteen elements scattered randomly across the page, with relationships crossing each other like a plate of spaghetti. The diagram is technically correct. Every element is there. Every relationship is accurate. But it is completely impossible to follow.

So you try again. "Make it cleaner." The AI shuffles some things around and produces something equally unreadable. You try "simplify it" and lose half your components. Three iterations later, you give up and draw it by hand.

This is the experience of almost every architect and developer using AI tools to generate diagrams. The problem is not the AI. The problem is that you are giving it instructions the layout algorithm cannot act on.

## The Science Nobody Tells You About

There is actual peer-reviewed research on what makes diagrams readable, and almost nobody in the AI tooling space talks about it.

Helen Purchase at the University of Queensland conducted empirical studies comparing different graph aesthetics. Her finding was unambiguous: **edge crossings are the single most important factor affecting diagram comprehension**. Not alignment. Not colour. Not overall size. Crossings.

When two lines cross, the reader must pause and mentally untangle which path belongs to which connection. This measurable increase in cognitive load directly reduces comprehension speed and accuracy. Purchase's studies showed that reducing crossings improved reader accuracy by 30-40%.

Here is the part that matters for AI-generated diagrams. The layout algorithms that render your Mermaid and PlantUML code -- Dagre and Sugiyama respectively -- position elements based on **declaration order in the code**. The AI writes the code; the algorithm decides where things go. And the crossing minimisation stage of these algorithms is NP-hard, which means results depend heavily on the initial element ordering.

Put simply: if the AI declares your database first and your user last, the algorithm starts from a terrible position and produces a terrible layout. If the AI declares elements in reading order, the algorithm starts close to a good solution and produces far fewer crossings.

There is one more principle that matters. The Gestalt principle of proximity states that elements placed close together are perceived as related. This is strong enough to override colour or shape similarity. If your API Gateway is visually closer to an external system than to the services it routes to, the reader's brain groups it with the wrong things -- regardless of the colour coding.

## What NOT to Do

### Antipattern 1: Random Element Order

This is the most common failure mode. The AI declares elements in whatever order it thinks of them:

```
Database, Cache, External, Notify, Inventory, API, Orders, Web, User
```

The database is declared first but should be rightmost. The user is declared last but should be leftmost. The layout algorithm must reposition everything, and its barycentric heuristic -- which calculates average positions of connected neighbours -- struggles because neighbours appear in unexpected positions.

Now compare this with declaring elements in reading order:

```
User, Web, API, Orders, Inventory, Notify, External, DB, Cache
```

Same nine elements. Same twelve relationships. The only difference is declaration order. The second version produces a clean left-to-right flow with minimal crossings. The first produces chaos.

### Antipattern 2: Vague Refinement Requests

"Make it cleaner" -- the AI does not know what "clean" means in layout terms.

"Add more detail" -- this mixes abstraction levels. You get database table names appearing on a container diagram, which violates one of the core principles of C4 modelling.

"Simplify it" -- the AI removes elements rather than improving their arrangement.

Instead, be specific: "The diagram has a crossing between Inventory-to-Database and Orders-to-Payment. Swap the declaration order of Orders and Inventory to align with left-to-right flow." That is an instruction the AI can act on, because it maps directly to what the layout algorithm needs.

### Antipattern 3: Relationships Before Elements

Declaring connections before declaring what they connect means the layout algorithm has no starting positions to work with. It must simultaneously figure out where everything goes and how to route edges.

The fix is straightforward: declare ALL elements first, THEN all relationships.

### Antipattern 4: No Crossing Target

If you do not tell the AI to minimise crossings, it accepts any layout. It has no reason to optimise for readability unless you explicitly ask.

Set targets: "Maximum 2 edge crossings" for a simple diagram, or "Fewer than 5 crossings" for complex ones. Zero is ideal for anything with fewer than seven elements.

## What TO Do: The Structured Prompt

The fix is a structured prompt that gives the AI the information the layout algorithm needs. Here is the approach, broken into four steps.

### Step 1: Specify Elements in Tier Order

Think of your architecture in horizontal tiers, reading left to right:

- **Tier 1: Actors** (leftmost) -- the people who use the system
- **Tier 2: Presentation layer** -- web apps, UIs
- **Tier 3: API layer** -- gateways, routers
- **Tier 4: Service layer** -- business logic
- **Tier 5: Data layer** (rightmost) -- databases, caches
- **External systems** -- outside the boundary, rightmost

Tell the AI to declare elements in this exact order.

### Step 2: Declare Relationships in Flow Order

After all elements are declared, list relationships following the same left-to-right flow. Actor uses UI. UI calls API. API routes to services. Services read from databases. Services call external systems.

### Step 3: Specify Styling

Use the C4 colour scheme so the visual hierarchy reinforces the architecture:

- Persons: `#08427B` (dark blue)
- Containers: `#438DD5` (medium blue)
- External systems: `#999999` (grey)

### Step 4: Set Constraints

Specify layout direction (LR for left-to-right, TB for top-to-bottom), maximum crossing count, and use subgraphs for system boundaries.

### The Copy-Paste Prompt Template

Here is a prompt template you can use directly with any AI tool:

```
Generate a Mermaid C4 Container diagram.

System: [SYSTEM NAME]

Elements (declare in this exact left-to-right order):
1. [Actor] [Person] - leftmost
2. [UI] [Container: Technology]
3. [API] [Container: Technology]
4. [Service1] [Container: Technology]
5. [Service2] [Container: Technology]
6. [Database] [Container: Technology] - rightmost
7. [External] [External System] - rightmost

Relationships (in flow order):
- Actor --> UI (Uses, HTTPS)
- UI --> API (API calls, REST)
- API --> Service1 (Routes)
- API --> Service2 (Routes)
- Service1 --> Database (Reads/writes, SQL)
- Service2 --> Database (Reads/writes, SQL)
- Service1 --> External (Calls, REST)

Requirements:
- Use flowchart LR
- Apply C4 colours (persons: #08427B, containers: #438DD5, external: #999999)
- Maximum 2 edge crossings
- Group services in a subgraph boundary
- Declare ALL elements before ANY relationships
```

This template works with Claude, ChatGPT, Copilot, and any other AI tool that generates Mermaid code. The key is that you are providing information the layout algorithm can use, not just describing what you want the output to look like.

## Fixing Crossings When They Happen

Sometimes the first result still has crossings, even with a structured prompt. Do not regenerate the entire diagram. Make targeted requests.

Instead of "make it cleaner," try:

- "The diagram has a crossing between X-to-Y and A-to-B. Swap declaration order of X and A to align with left-to-right flow."
- "Move Element adjacent to OtherElement by declaring them consecutively."
- "Reorder the relationship declarations so that Orders-to-Database appears before Orders-to-Payment."

You are speaking the layout algorithm's language. The AI understands these specific instructions because they map to concrete changes in the generated code.

For Mermaid specifically, declaration order is your only lever. Reorder elements within the same tier so the declaration sequence matches data flow. Reorder relationships to follow the same sequence as element declarations. Add subgraphs to constrain related elements together.

## When Mermaid Is Not Enough: PlantUML

Mermaid has one significant limitation: it provides **no directional hints**. You cannot force an element to appear to the right of another element. You can influence the layout through declaration order, but you cannot guarantee it.

PlantUML with C4-PlantUML macros solves this. It provides explicit layout control:

- `Rel_Down`, `Rel_Right`, `Rel_Up`, `Rel_Left` -- force specific edge directions
- `Lay_Right`, `Lay_Down` -- force element positions within a tier
- `LAYOUT_TOP_DOWN()`, `LAYOUT_LEFT_RIGHT()` -- set global flow direction
- `LAYOUT_WITH_LEGEND()` -- automatic C4 legend

When you have a crossing between two relationships in Mermaid and reordering declarations does not fix it, PlantUML lets you use `Rel_Right(orders, payment, "Charges", "REST")` to force the Payment Gateway to the right of the services tier, eliminating the crossing deterministically.

**Use Mermaid for** quick sketches, markdown-embedded diagrams, and anything with fewer than 15 elements. It renders natively in Obsidian, GitHub, and most documentation platforms.

**Use PlantUML for** formal documentation, diagrams with more than 15 elements, persistent crossings that Mermaid cannot resolve, and anything destined for PDF export.

## Automating All of This with Claude Code Skills

I have encoded all of this knowledge into three Claude Code skills that apply these principles automatically.

### /diagram

Generates architecture diagrams in multiple formats -- C4, system landscape, data flow, AWS. It automatically applies tier-based declaration ordering, includes a validation checklist (edge crossings, visual hierarchy, flow direction, grouping, abstraction level), and supports Python diagrams library (PNG), Mermaid (inline), and PlantUML output.

### /c4-diagram

Specialised for C4 architecture diagrams. Three output formats: native Mermaid C4, flowchart LR with C4 styling, and PlantUML with directional hints. It has built-in antipattern avoidance -- it declares elements before relationships and uses tier-based ordering by default. It includes iterative refinement guidance for fixing specific crossings after generation.

### /diagram-review

Analyses existing diagrams for readability and architecture quality. It uses four parallel analysis agents: Component Extraction, Relationship Mapping, Architecture Pattern Analysis, and Technology Integration. The output includes a readability assessment with edge crossing count, visual hierarchy evaluation, flow direction consistency, and grouping effectiveness. It suggests specific fixes for any issues found.

## Get the Skills

The skills are available at [github.com/DavidROliverBA/Daves-Claude-Code-Skills](https://github.com/DavidROliverBA/Daves-Claude-Code-Skills).

To install, copy the skill `.md` files to your `.claude/skills/` directory. Then invoke them with `/diagram`, `/c4-diagram`, or `/diagram-review` in Claude Code.

## The One-Line Summary

The difference between a terrible AI diagram and a good one is not asking for "cleaner." It is understanding that declaration order controls layout, and telling the AI exactly which order you want.

---

*David Oliver is a Solutions Architect at British Airways, working in Operations and Engineering IT. He builds knowledge management systems with Obsidian and Claude Code, and is unreasonably passionate about making architecture diagrams legible.*
