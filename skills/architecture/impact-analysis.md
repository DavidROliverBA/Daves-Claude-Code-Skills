---
description: Analyse cascading impact of architectural changes across technical, organisational, financial, and risk dimensions using parallel agents
model: sonnet
---

# /impact-analysis

Analyse the cascading impact of architectural changes across systems, integrations, teams, and finances. Uses four parallel agents to evaluate different impact dimensions simultaneously, then synthesises findings into a comprehensive impact report.

## When to Use This Skill

- Evaluating the impact of a proposed system migration or replacement
- Assessing consequences of a technology change (e.g., switching databases, frameworks)
- Understanding blast radius of an infrastructure change
- Preparing impact assessments for architecture governance boards
- Estimating effort and risk before committing to a change

## Usage

```
/impact-analysis <change-description> [--scope system|programme|enterprise] [--depth quick|standard|deep]
```

### Parameters

| Parameter     | Description                                      | Required |
|---------------|--------------------------------------------------|----------|
| `change`      | Description of the proposed architectural change | Yes      |
| `--scope`     | Blast radius scope (default: `system`)           | No       |
| `--depth`     | Analysis depth (default: `standard`)             | No       |

## Instructions

### Phase 1: Define the Change

Gather from the user:

| Field                | Description                                           | Example                                         |
|----------------------|-------------------------------------------------------|-------------------------------------------------|
| **Change description** | What is changing?                                   | Migrate OrderService from on-premises to cloud  |
| **Current state**    | How does it work today?                               | Monolith on VMs, Oracle DB, batch integrations  |
| **Proposed state**   | How will it work after the change?                    | Microservices on Kubernetes, PostgreSQL, events  |
| **Affected systems** | Which systems are directly impacted?                  | OrderService, PaymentGateway, InventoryDB       |
| **Timeline**         | When is this expected to happen?                      | Q3 2026                                         |

### Phase 2: Parallel Impact Analysis — Agent Team

Launch four agents simultaneously using the Task tool. Each agent analyses one dimension of impact independently.

**Agent 1: Technical Impact Analyst** (Sonnet)
Task: Analyse affected systems and technical dependencies
- Map all upstream and downstream system dependencies
- Identify integration points that will change (APIs, data flows, protocols)
- Assess breaking changes and backward compatibility
- Evaluate performance implications (latency, throughput, availability)
- Check infrastructure requirements (compute, storage, networking)
- Identify data migration needs and complexity
Return: Technical impact matrix with severity ratings (critical/high/medium/low) per system

**Agent 2: Organisational Impact Analyst** (Sonnet)
Task: Assess people and process impacts
- Identify all affected teams and their roles in the change
- Assess skill gaps and training requirements
- Map process changes required (deployment, monitoring, support)
- Evaluate change management complexity (communication, adoption)
- Identify key stakeholders and their concerns
- Assess impact on existing project timelines
Return: Organisational impact summary with affected teams, training needs, and change management recommendations

**Agent 3: Financial Impact Analyst** (Sonnet)
Task: Calculate financial implications
- Estimate one-time implementation costs (development, migration, tooling)
- Calculate recurring operational cost changes (infrastructure, licensing, support)
- Identify hidden costs (productivity loss during transition, parallel running)
- Quantify benefits and savings (efficiency gains, reduced maintenance)
- Produce 3-year financial projection (Year 0 investment, Year 1-3 returns)
- Calculate break-even point
Return: Financial impact table with year-by-year breakdown and ROI calculation

**Agent 4: Risk Assessor** (Sonnet)
Task: Identify and score risks across all dimensions
- Identify technical risks (integration failures, data loss, performance degradation)
- Identify organisational risks (skill gaps, resistance to change, key person dependency)
- Identify financial risks (cost overruns, delayed benefits, vendor lock-in)
- Identify schedule risks (delays, dependency bottlenecks, resource contention)
- Score each risk: Probability (1-5) x Impact (1-5) = Risk Score (1-25)
- Propose mitigations for all risks scoring 12 or above
Return: Risk register with probability, impact, score, and mitigations

### Phase 3: Synthesise Impact Report

Combine all agent results into a unified impact report:

1. **Calculate overall impact score** (0-10) based on weighted agent findings
2. **Create executive summary** highlighting the most significant impacts
3. **Build dependency diagram** showing affected systems and relationships
4. **Compile risk matrix** with top risks and mitigations
5. **Generate implementation checklist** with sequenced actions
6. **Define rollback procedure** in case the change needs to be reversed

## Output Format

```markdown
# Impact Analysis: <Change Description>

## Executive Summary

**Impact Score:** X/10 (Low/Medium/High/Critical)
**Recommendation:** Proceed / Proceed with conditions / Defer / Do not proceed

<2-3 sentence summary of the most significant findings>

## Impact Summary

| Dimension      | Score | Key Finding                    |
|----------------|-------|--------------------------------|
| Technical      | X/10  | <one-line summary>             |
| Organisational | X/10  | <one-line summary>             |
| Financial      | X/10  | <one-line summary>             |
| Risk           | X/10  | <one-line summary>             |

## Technical Impact

### Affected Systems

| System           | Impact Level | Change Required              |
|------------------|-------------|------------------------------|
| <System Name>    | Critical    | <What changes>               |

### Integration Changes
<Details of API, data flow, and protocol changes>

### Data Migration
<Scope, complexity, and approach>

## Organisational Impact

### Affected Teams

| Team           | Impact    | Actions Required             |
|----------------|-----------|------------------------------|
| <Team Name>    | High      | <Training, process changes>  |

### Training Requirements
<Skills gaps and training plan>

## Financial Impact

| Category              | Year 0    | Year 1    | Year 2    | Year 3    |
|-----------------------|-----------|-----------|-----------|-----------|
| Implementation costs  | £X        | —         | —         | —         |
| Operational costs     | £X        | £X        | £X        | £X        |
| Savings / Benefits    | —         | £X        | £X        | £X        |
| **Net**               | **(£X)**  | **£X**    | **£X**    | **£X**    |

**Break-even:** Month X of Year Y

## Risk Matrix

| Risk                        | Prob | Impact | Score | Mitigation              |
|-----------------------------|------|--------|-------|-------------------------|
| <Risk description>          | X/5  | X/5    | XX    | <Mitigation action>     |

## Implementation Checklist

- [ ] <Sequenced action items>

## Rollback Procedure

<Steps to reverse the change if needed>
```

## Examples

### Example 1: Database Migration

```
/impact-analysis Migrate OrderService from Oracle to PostgreSQL --scope system
```

Analyses technical compatibility, team training needs, licensing savings, and migration risks for a database platform change.

### Example 2: Cloud Migration

```
/impact-analysis Move payment processing from on-premises to AWS --scope programme --depth deep
```

Deep analysis of moving a critical financial system to the cloud, including compliance, latency, and cost implications across the entire programme.

### Example 3: API Versioning Change

```
/impact-analysis Deprecate REST API v1 and migrate all consumers to v2 --scope enterprise
```

Enterprise-wide analysis of API deprecation impact across all consuming systems, teams, and third-party integrations.

---

**Invoke with:** `/impact-analysis <change-description>` then provide current state, proposed state, and affected systems
