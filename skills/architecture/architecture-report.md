---
description: Generate comprehensive architecture reports using five parallel agents for inventory, integration, decision, risk, and financial analysis
model: sonnet
---

# /architecture-report

Generate comprehensive architecture reports for stakeholder communication, audits, and governance reviews. Uses five parallel agents to gather and analyse system inventory, integrations, decisions, risks, and costs simultaneously.

## When to Use This Skill

- Preparing for architecture governance reviews
- Creating quarterly or annual architecture reports
- Documenting the current state of a system landscape
- Onboarding new architects or technical leads
- Supporting audit and compliance activities

## Usage

```
/architecture-report <scope> [--audience exec|technical|audit] [--format summary|detailed]
```

### Parameters

| Parameter    | Description                                          | Required |
|--------------|------------------------------------------------------|----------|
| `scope`      | What to report on (system, programme, or domain)     | Yes      |
| `--audience` | Target audience — adjusts detail level (default: `technical`) | No |
| `--format`   | Report depth (default: `detailed`)                   | No       |

## Instructions

### Phase 1: Define Report Scope

Gather from the user:

| Field           | Description                                      | Example                              |
|-----------------|--------------------------------------------------|--------------------------------------|
| **Scope**       | What systems/domain to cover                     | Order Management domain              |
| **Time period** | Report period                                    | Q4 2025                              |
| **Audience**    | Who will read this report?                       | Architecture review board            |
| **Focus areas** | Any specific areas of concern?                   | Integration complexity, tech debt    |
| **Source files** | Where to find system/architecture documentation | System notes, ADRs, project files    |

### Phase 2: Parallel Data Gathering — Agent Team

Launch five agents simultaneously using the Task tool.

**Agent 1: System Inventory Analyst** (Haiku)
Task: Catalogue all systems in scope
- List all systems with name, type, technology stack, and owner
- Identify system criticality (critical/high/medium/low)
- Map deployment topology (cloud, on-premises, hybrid)
- Note system age and last major update date
- Flag systems approaching end-of-life or end-of-support
Return: System inventory table with technology, owner, criticality, and status

**Agent 2: Integration Mapper** (Haiku)
Task: Map system-to-system connections
- Catalogue all integration points between systems
- Record protocol (REST, SOAP, messaging, file transfer, database link)
- Record pattern (synchronous, asynchronous, batch, event-driven)
- Identify data flows and their direction
- Flag single points of failure in integrations
- Note integration health (stable, fragile, deprecated)
Return: Integration matrix and dependency data for diagram generation

**Agent 3: Decision Tracker** (Haiku)
Task: Summarise architecture decisions
- Find all architecture decisions (ADRs) related to the scope
- Categorise by status (proposed, accepted, deprecated, superseded)
- Identify decisions that are overdue for review
- Map decisions to the systems and projects they affect
- Highlight recently accepted decisions and their implications
Return: ADR summary table with status, age, and review dates

**Agent 4: Risk and Compliance Analyst** (Sonnet)
Task: Assess security, compliance, and technical risk
- Evaluate security posture per system (authentication, encryption, vulnerability management)
- Check compliance status against relevant standards (ISO 27001, SOC 2, GDPR, etc.)
- Identify technical debt (outdated dependencies, unsupported versions, workarounds)
- Score architecture maturity per system (ad-hoc, managed, optimised)
- Compile risk register with probability and impact scores
Return: Risk register and compliance matrix with maturity scores

**Agent 5: Financial Analyst** (Sonnet)
Task: Analyse architecture costs
- Calculate cost per system (infrastructure, licensing, staffing)
- Identify cost trends (increasing, stable, decreasing)
- Flag cost optimisation opportunities (rightsizing, consolidation, licence renegotiation)
- Calculate total architecture TCO for the scope
- Compare costs against industry benchmarks where possible
Return: Financial summary with per-system cost breakdown and optimisation opportunities

### Phase 3: Synthesise Report

Combine all agent results, tailored to the target audience:

**Executive audience:** Focus on risk, cost, and strategic alignment. Minimise technical detail.
**Technical audience:** Full detail on systems, integrations, and decisions.
**Audit audience:** Emphasise compliance, controls, and evidence.

## Output Format

```markdown
# Architecture Report: <Scope>

**Period:** <Time period>
**Prepared for:** <Audience>
**Date:** YYYY-MM-DD

## Executive Summary

<1-2 page overview with key metrics, risks, and recommendations>

### Key Metrics

| Metric                    | Value          | Trend      |
|---------------------------|----------------|------------|
| Systems in scope          | X              | —          |
| Integration points        | X              | +X vs last |
| Active ADRs               | X              | —          |
| Open risks (high+)        | X              | -X vs last |
| Total architecture TCO    | £Xk/month      | +X%        |

## System Landscape

### System Inventory

| System          | Type      | Technology    | Criticality | Owner        | Status      |
|-----------------|-----------|---------------|-------------|--------------|-------------|
| <System Name>   | <type>    | <tech stack>  | Critical    | <Team>       | Active      |

### Integration Map

| Source          | Target          | Protocol | Pattern       | Health    |
|-----------------|-----------------|----------|---------------|-----------|
| <System A>      | <System B>      | REST     | Synchronous   | Stable    |

## Architecture Decisions

| ADR              | Status   | Date       | Systems Affected    | Review Due |
|------------------|----------|------------|---------------------|------------|
| <ADR Title>      | Accepted | YYYY-MM-DD | System A, System B  | YYYY-MM-DD |

### Decisions Requiring Attention
<ADRs overdue for review or with changed context>

## Security and Compliance

### Compliance Matrix

| Standard    | System A | System B | System C |
|-------------|----------|----------|----------|
| ISO 27001   | Pass     | Partial  | N/A      |
| GDPR        | Pass     | Pass     | Fail     |

### Risk Register

| Risk                    | Probability | Impact | Score | Mitigation         |
|-------------------------|-------------|--------|-------|---------------------|
| <Risk description>      | X/5         | X/5    | X/25  | <Mitigation>        |

## Financial Analysis

### Cost by System

| System          | Infrastructure | Licensing | Staffing | Total/Month |
|-----------------|----------------|-----------|----------|-------------|
| <System Name>   | £X             | £X        | £X       | £X          |

### Optimisation Opportunities

| Opportunity              | Est. Savings | Effort | Priority |
|--------------------------|-------------|--------|----------|
| <Description>            | £X/year     | Medium | High     |

## Recommendations

1. **Priority 1:** <recommendation with rationale>
2. **Priority 2:** <recommendation with rationale>
3. **Priority 3:** <recommendation with rationale>

## Appendices

### A: System Dependency Diagram
<Mermaid or PlantUML diagram>

### B: Full Risk Register
<Expanded risk details>
```

## Examples

### Example 1: Domain Architecture Report

```
/architecture-report "Order Management domain" --audience exec --format summary
```

Generates an executive summary of the order management architecture with cost highlights and top risks.

### Example 2: Full Technical Report

```
/architecture-report "Payment Processing" --audience technical --format detailed
```

Full technical report with system details, integration maps, and all ADRs.

### Example 3: Audit Report

```
/architecture-report "Customer Data Platform" --audience audit
```

Compliance-focused report with control evidence, data residency, and audit trail coverage.

---

**Invoke with:** `/architecture-report <scope>` to generate a comprehensive architecture report
