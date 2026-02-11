# /diagram Skill

<!-- Standalone skill file for Claude Code. Drop into .claude/skills/ and invoke with /diagram. -->

Generate architecture diagrams in multiple formats (C4, System Landscape, Data Flow, AWS).

## When to Use This Skill

Use `/diagram` when you need to create or update architecture visualisations:
- Create new C4 context/container/component diagrams
- Generate system landscape maps
- Visualise data flow architectures
- Create AWS infrastructure diagrams
- Diagram integration patterns
- Map system dependencies

## Usage

```
/diagram <type> [options]
```

### Diagram Types

| Type | Description | Use Case |
|------|-------------|----------|
| `c4-context` | C4 Level 1 - System context | Show external actors and system boundary |
| `c4-container` | C4 Level 2 - System containers | Show major components (services, databases) |
| `c4-component` | C4 Level 3 - Component level | Show detailed component interactions |
| `system-landscape` | Enterprise system map | Show all systems and connections |
| `data-flow` | Data movement diagram | Show how data moves through systems |
| `aws-architecture` | AWS infrastructure | Show EC2, RDS, S3, networking |
| `integration-pattern` | Integration architecture | Show message flows and patterns |
| `dependency-graph` | System dependencies | Show what depends on what |

## Workflow

### Phase 1: Capture Requirements
When invoked, the skill asks:

1. **Diagram type** (required)
   - Options: c4-context, c4-container, system-landscape, data-flow, aws-architecture, integration-pattern, dependency-graph
   - Default: c4-context

2. **Scope** (required)
   - For C4: Which system/product?
   - For landscape: Which programme/domain?
   - For AWS: Which account/region?
   - For data-flow: Which integration?

3. **Systems to include** (optional)
   - Comma-separated list of systems
   - Leave blank to auto-detect from context

4. **Styling preferences** (optional)
   - Colour scheme: classic, muted, vibrant
   - Icon set: simple, detailed, minimalist
   - Default: classic, simple

5. **Output format** (optional)
   - `python` — PNG via Python `diagrams` library (default for AWS/landscape types)
   - `mermaid` — Inline Mermaid (default for C4 types; renders natively in many Markdown editors)
   - `plantuml` — C4-PlantUML with directional hints (for complex C4 layouts, >15 elements)
   - For C4 types (c4-context, c4-container, c4-component), suggest Mermaid or PlantUML and cross-reference `/c4-diagram` for data-driven generation

6. **Output location** (optional)
   - Save as standalone file or embed in an existing document?
   - Default: Create standalone file

### Phase 2: Generate Diagram

The skill generates a Python script using the `diagrams` package:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EKS, EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Spark

with Diagram("System Landscape", show=False, direction="TB"):
    # Your architecture here
```

#### Layout Science (Mermaid/PlantUML formats)

When generating Mermaid or PlantUML output (not Python):

- **Declaration order matters** — declare elements in reading order (left-to-right or top-to-bottom). The Dagre/Sugiyama algorithm positions elements based on declaration sequence.
- **Tier-based ordering** — Actors, Presentation, API, Services, Data, External
- **Edge crossing targets** — <5 for complex diagrams, 0 for simple ones. Crossings are the strongest predictor of comprehension difficulty (Purchase et al.).
- **Use subgraphs/boundaries** to group related elements (Gestalt proximity principle).

For C4-specific layout guidance including iterative refinement and PlantUML directional hints, see the `/c4-diagram` skill.

### Phase 3: Render and Save

The skill:
1. Executes the Python script
2. Generates PNG image
3. Creates a Markdown note with the embedded diagram
4. Saves to the chosen output location

### Phase 4: Validation Checklist

After rendering, validate against these criteria:

| Criterion                     | Target                           | How to Check                             |
| ----------------------------- | -------------------------------- | ---------------------------------------- |
| **Edge crossings**            | <5 for complex, 0 for simple     | Trace each relationship path visually    |
| **Visual hierarchy**          | System boundary most prominent   | Is the boundary immediately identifiable? |
| **Grouping**                  | Related elements close together  | Do tiers/layers appear as distinct groups? |
| **Flow direction**            | Consistent L-to-R or T-to-B     | Does data flow follow one direction?     |
| **Relationship traceability** | Can follow each line             | Trace each connection without confusion  |
| **Abstraction level**         | One level per diagram            | No database tables on container diagrams |

If any criterion fails, revise the diagram before presenting to the user. For Mermaid: reorder declarations to match data flow. For PlantUML: add directional hints (`Rel_Down`, `Lay_Right`). See `/c4-diagram` skill for detailed refinement guidance.

## Format Selection Guide

| Scenario                               | Format         | Reason                                              |
| -------------------------------------- | -------------- | --------------------------------------------------- |
| AWS infrastructure, cloud icons        | `python`       | Rich icon library, professional PNG output           |
| System landscape, presentations        | `python`       | Best for standalone images and documentation         |
| Quick C4 diagram                       | `mermaid`      | Native rendering, Git-friendly, fast iteration       |
| Complex C4 with persistent crossings   | `plantuml`     | Directional hints fix crossings Mermaid cannot       |
| >15 elements in a C4 diagram           | `plantuml`     | Layout control prevents chaos at scale               |
| Formal documentation, PDF export       | `plantuml`     | Automatic legends, consistent server-side rendering  |

## Examples

### Example 1: C4 Context Diagram for an Order Processing Platform

```
/diagram c4-context

Scope: Order Processing Platform
Systems: API Gateway, Payment Service, Inventory DB, Notification Service
Colour scheme: classic
```

**Result:** Creates a C4 Level 1 diagram showing:
- External actors (customers, warehouse staff)
- Order Processing Platform as central system
- API Gateway (entry point)
- Payment Service (external provider)
- Inventory DB (data store)
- Data flows between components

### Example 2: Data Flow Diagram for Real-time Integration

```
/diagram data-flow

Scope: E-Commerce to Warehouse Real-time Integration
Systems: E-Commerce App, Message Broker, Order Processor, Warehouse Management System
Styling: vibrant
```

**Result:** Creates a data flow diagram showing:
- E-Commerce App order generation
- Message broker event publishing
- Order Processor stream processing
- Warehouse Management System real-time updates
- Data quality checks at each stage
- Error handling paths

### Example 3: AWS Architecture Diagram for Production

```
/diagram aws-architecture

Scope: Production Account (eu-west-2)
Systems: EKS, RDS, S3, ALB
Colour scheme: muted
```

**Result:** Creates a production AWS architecture diagram showing:
- VPC with 3 Availability Zones
- EKS cluster nodes
- RDS (Multi-AZ)
- S3 buckets
- Network components (ALB, NLB)
- Security groups
- Cost annotations

## Smart Defaults

The skill automatically:

1. **Applies styling**
   - Critical systems: Red background
   - High priority: Orange background
   - Medium: Blue background
   - Data flows: Green (real-time), Blue (batch)

2. **Generates captions**
   - Includes latency/throughput labels
   - Shows SLA compliance status
   - Indicates criticality level

## Options

### Styling Options

```
/diagram <type> --style vibrant
```

- `classic` - Traditional blues, greys, blacks
- `muted` - Soft pastels, professional
- `vibrant` - Bright colours, high contrast
- `dark` - Dark background, light text

### Icon Sets

```
/diagram <type> --icons detailed
```

- `simple` - Minimal icons, text-based
- `minimalist` - Very simple, clean
- `detailed` - Rich icons, realistic

### Layout Direction

```
/diagram <type> --direction LR
```

- `TB` - Top to Bottom (default)
- `LR` - Left to Right
- `RL` - Right to Left
- `BT` - Bottom to Top

### Include Metrics

```
/diagram <type> --metrics yes
```

- Show latency SLAs
- Show throughput/capacity
- Show cost annotations
- Show availability targets

### Filter by Criticality

```
/diagram system-landscape --criticality critical
```

- `critical` - Critical systems only
- `high` - High + Critical
- `medium` - Medium and above
- `all` - All systems

## Output Formats

The skill generates:

1. **PNG image** - High-resolution diagram
2. **Markdown note** - With embedded image and metadata
3. **Source code** - The Mermaid, PlantUML, or Python source for future edits

## Error Handling

If diagram generation fails:

1. User is shown error message with diagnostics
2. Suggests checking:
   - System names are correct
   - Integration directions are valid
   - AWS account/region exists
3. Offers to generate with fewer systems
4. Falls back to Mermaid text diagram (if Python fails)

## Next Steps

After creating a diagram:

1. Review the PNG for accuracy
2. Adjust colours/layout if needed via `--style`, `--icons`, `--direction`
3. Add annotations as needed
4. Create scenario-specific variants for comparison
5. Include in architecture reviews and documentation

## Related Skills

- `/c4-diagram` - Data-driven C4 diagram generation (Mermaid, flowchart, or PlantUML)
- `/diagram-review` - Analyse existing diagrams for readability and architecture quality

---

**Invoke with:** `/diagram <type>`

**Example:** `/diagram c4-context` then follow the prompts for scope and options to generate your diagram
