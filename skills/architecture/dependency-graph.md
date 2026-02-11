---
description: Generate system dependency graphs showing upstream/downstream relationships with colour-coded criticality
model: sonnet
---

# /dependency-graph

Generate system dependency graphs showing upstream and downstream relationships, data flows, and critical paths. Produces Mermaid diagrams with colour-coded criticality and identifies single points of failure.

## When to Use This Skill

- Visualising system dependencies before making changes
- Identifying single points of failure in an architecture
- Understanding the blast radius of a potential system outage
- Documenting integration landscapes for new team members
- Preparing dependency analysis for architecture reviews

## Usage

```
/dependency-graph <system-or-scope> [--direction upstream|downstream|both] [--depth 1|2|3] [--filter domain|team|criticality]
```

### Parameters

| Parameter     | Description                                          | Required |
|---------------|------------------------------------------------------|----------|
| `system`      | Central system or scope to map dependencies for      | Yes      |
| `--direction` | Show upstream, downstream, or both (default: `both`) | No       |
| `--depth`     | How many hops to traverse (default: `2`)             | No       |
| `--filter`    | Filter by domain, team, or criticality level         | No       |

## Instructions

### Phase 1: Gather Dependency Data

Identify the central system and search for dependency information:

1. **Read system documentation** — Look for architecture notes, ADRs, and integration docs
2. **Search for references** — Find all notes that mention the target system
3. **Extract relationships** — Identify upstream (depends on) and downstream (depended on by) systems
4. **Classify connections** — Protocol, pattern, data flow direction, criticality

For each dependency, capture:

| Field          | Description                                     | Example                    |
|----------------|-------------------------------------------------|----------------------------|
| **Source**     | System that initiates the connection            | OrderService               |
| **Target**     | System that receives the connection             | PaymentGateway             |
| **Protocol**   | Communication protocol                          | REST, Kafka, SFTP, gRPC    |
| **Pattern**    | Integration pattern                              | Sync, async, batch, event  |
| **Criticality**| How critical is this dependency?                | Critical, high, medium, low|
| **Data flow**  | What data moves across this connection?         | Order events, payment status|

### Phase 2: Analyse Dependencies

1. **Identify critical paths** — Chains of critical dependencies where a failure cascades
2. **Find single points of failure** — Systems with no redundancy that many others depend on
3. **Calculate fan-in/fan-out** — Systems with high dependency counts (hubs)
4. **Detect circular dependencies** — Systems that directly or indirectly depend on each other
5. **Assess resilience** — For each critical dependency, is there a fallback?

### Phase 3: Generate Diagram

Create a Mermaid flowchart with colour-coded nodes:

```mermaid
flowchart LR
    %% Colour coding by criticality
    classDef critical fill:#FF4444,stroke:#CC0000,color:#fff
    classDef high fill:#FF8800,stroke:#CC6600,color:#fff
    classDef medium fill:#4488FF,stroke:#2266CC,color:#fff
    classDef low fill:#88CC88,stroke:#66AA66,color:#fff
    classDef external fill:#999999,stroke:#666666,color:#fff

    %% Systems (declared in tier order)
    A["<b>System A</b><br/><i>Critical</i><br/>Fan-out: 5"]
    B["<b>System B</b><br/><i>High</i><br/>Fan-in: 3"]
    C["<b>System C</b><br/><i>Medium</i>"]

    %% Dependencies
    A -->|"Orders<br/>[REST]"| B
    B -->|"Payments<br/>[Kafka]"| C

    %% Apply styles
    class A critical
    class B high
    class C medium
```

**Diagram conventions:**
- **Red nodes** — Critical systems (failure causes major business impact)
- **Orange nodes** — High importance (failure causes significant degradation)
- **Blue nodes** — Medium importance (failure has limited impact)
- **Green nodes** — Low importance (failure has minimal impact)
- **Grey nodes** — External systems (outside your control)
- **Solid arrows** — Synchronous dependencies
- **Dashed arrows** — Asynchronous dependencies
- **Edge labels** — Show data type and protocol

### Phase 4: Output

Present:
1. **The Mermaid diagram**
2. **Dependency summary table**
3. **Critical path analysis**
4. **Single points of failure**
5. **Recommendations**

## Output Format

```markdown
# Dependency Graph: <System/Scope>

## Diagram

<Mermaid flowchart>

## Dependency Summary

| System          | Fan-In | Fan-Out | Criticality | Single Point of Failure? |
|-----------------|--------|---------|-------------|--------------------------|
| <System Name>   | X      | X       | Critical    | Yes — no failover        |

## Critical Paths

### Path 1: <Description>
`System A → System B → System C`
- **Risk:** If System B fails, Systems A and C are both affected
- **Mitigation:** <Suggestion>

## Single Points of Failure

| System         | Depends On It | Failover Exists? | Risk Level |
|----------------|---------------|------------------|------------|
| <System Name>  | X systems     | No               | Critical   |

## Circular Dependencies

| Cycle                              | Risk                              |
|------------------------------------|-----------------------------------|
| System A → System B → System A     | Deadlock risk during failures     |

## Recommendations

1. **Add failover for <System>** — X systems depend on it with no redundancy
2. **Break circular dependency between <A> and <B>** — Introduce async messaging
3. **Monitor <critical path>** — Set up alerting for the entire chain
```

## Examples

### Example 1: System-Centric Dependency Map

```
/dependency-graph OrderService --direction both --depth 2
```

Maps all systems that OrderService depends on (upstream) and all systems that depend on it (downstream), two hops deep.

### Example 2: Domain Dependency Overview

```
/dependency-graph "Payment Domain" --filter domain
```

Shows all dependencies between systems in the payment domain and their connections to external domains.

### Example 3: Critical Dependencies Only

```
/dependency-graph "Production Systems" --filter criticality --depth 3
```

Shows only critical and high-importance dependency chains across all production systems.

---

**Invoke with:** `/dependency-graph <system-name>` to visualise system dependencies with criticality analysis
