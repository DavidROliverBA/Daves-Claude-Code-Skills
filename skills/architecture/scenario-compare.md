---
description: Compare architectural scenarios with cost, timeline, complexity, risk, and benefit analysis using parallel agents
model: sonnet
---

# /scenario-compare

Compare multiple architectural scenarios with detailed cost, timeline, complexity, risk, and benefit analysis. Uses three parallel agents to evaluate financial, technical, and risk dimensions simultaneously, then produces a weighted decision matrix with a clear recommendation.

## When to Use This Skill

- Choosing between 2-4 architectural approaches for a problem
- Comparing build vs buy vs integrate options
- Evaluating technology platform alternatives
- Preparing options papers for architecture governance boards
- Making vendor or product selection decisions

## Usage

```
/scenario-compare <scenario-1> vs <scenario-2> [vs <scenario-3>] [--criteria cost,risk,time,complexity]
```

### Parameters

| Parameter    | Description                                         | Required |
|--------------|-----------------------------------------------------|----------|
| `scenarios`  | 2-4 scenarios separated by `vs`                     | Yes      |
| `--criteria` | Comma-separated evaluation criteria (default: all)  | No       |
| `--weights`  | Custom weights for criteria (default: equal)        | No       |

## Instructions

### Phase 1: Define Scenarios

For each scenario, gather:

| Field             | Description                                    | Example                                 |
|-------------------|------------------------------------------------|-----------------------------------------|
| **Name**          | Short label for the scenario                   | Cloud-Native Rebuild                    |
| **Description**   | What this approach entails                     | Rewrite as microservices on Kubernetes  |
| **Technology**    | Key technologies involved                      | Kubernetes, PostgreSQL, Kafka           |
| **Team impact**   | What teams need to do                          | Upskill to containers, hire 2 SREs     |
| **Timeline**      | Estimated delivery timeline                    | 12-18 months                            |

Also gather evaluation context:
- **Decision deadline** — When must the decision be made?
- **Budget constraints** — Any hard budget limits?
- **Non-negotiables** — Must-have requirements that eliminate options?

### Phase 2: Parallel Scenario Analysis — Agent Team

Launch three agents simultaneously using the Task tool. Each agent evaluates all scenarios across one dimension.

**Agent 1: Cost and Financial Analyst** (Sonnet)
Task: Compare financial implications of each scenario
- Calculate setup/implementation costs per scenario
- Calculate annual operating costs per scenario (infrastructure, licensing, staffing)
- Compute 3-year and 5-year Total Cost of Ownership (TCO)
- Calculate Return on Investment (ROI) and payback period
- Run sensitivity analysis (best case, expected, worst case — ±20% variance)
- Identify hidden costs (migration, training, opportunity cost, technical debt)
Return: Financial comparison matrix with TCO, ROI, and sensitivity ranges

**Agent 2: Technical and Complexity Analyst** (Sonnet)
Task: Compare technical characteristics of each scenario
- Score technology stack maturity and ecosystem (0-10)
- Score operational complexity (deployment, monitoring, debugging) (0-10)
- Score vendor dependency and lock-in risk (0-10)
- Assess data migration complexity and approach
- Evaluate scalability potential (vertical, horizontal, elasticity)
- Assess integration effort with existing systems
- Score team skill alignment (current skills vs required skills) (0-10)
Return: Technical comparison with radar chart data (5+ dimensions per scenario)

**Agent 3: Risk and Timeline Analyst** (Sonnet)
Task: Compare risks and delivery timelines
- Estimate implementation timeline per scenario (optimistic, expected, pessimistic)
- Identify critical path and key dependencies per scenario
- Score risks per scenario across categories (technical, organisational, financial, schedule)
- Create risk probability x impact matrix per scenario
- Identify go/no-go criteria and decision gates
- Assess reversibility — how hard is it to change course after committing?
Return: Timeline comparison and risk assessment data per scenario

### Phase 3: Synthesise Comparison

Combine all agent results:

1. **Build weighted decision matrix** — Score each scenario against all criteria
2. **Create side-by-side comparison** — Visual summary of key differences
3. **Generate recommendation** — Clear recommendation with reasoning
4. **Document trade-offs** — What you gain and lose with each option
5. **Define decision criteria** — Go/no-go checklist for the recommended option

**Default Weights:**

| Criterion        | Weight | Adjustable |
|------------------|--------|------------|
| Cost (TCO)       | 25%    | Yes        |
| Technical fit    | 25%    | Yes        |
| Risk             | 20%    | Yes        |
| Timeline         | 15%    | Yes        |
| Scalability      | 15%    | Yes        |

## Output Format

```markdown
# Scenario Comparison: <Context>

## Executive Summary

**Recommended:** Scenario X — <Name>
**Confidence:** High/Medium/Low

<2-3 sentence justification>

## Scenarios at a Glance

| Dimension         | Scenario A        | Scenario B        | Scenario C        |
|-------------------|-------------------|-------------------|-------------------|
| Approach          | <summary>         | <summary>         | <summary>         |
| Timeline          | X months          | X months          | X months          |
| 3-Year TCO        | £Xk               | £Xk               | £Xk               |
| Risk Level        | Low/Med/High      | Low/Med/High      | Low/Med/High      |
| Complexity        | X/10              | X/10              | X/10              |

## Cost Comparison

| Cost Category       | Scenario A  | Scenario B  | Scenario C  |
|---------------------|-------------|-------------|-------------|
| Setup costs         | £X          | £X          | £X          |
| Annual operating    | £X          | £X          | £X          |
| 3-Year TCO          | £X          | £X          | £X          |
| 5-Year TCO          | £X          | £X          | £X          |
| ROI (3-year)        | X%          | X%          | X%          |
| Payback period      | X months    | X months    | X months    |

### Sensitivity Analysis

| Scenario   | Best Case TCO | Expected TCO | Worst Case TCO |
|------------|---------------|--------------|----------------|
| A          | £X            | £X           | £X             |

## Technical Comparison

### Complexity Radar

| Dimension             | Scenario A | Scenario B | Scenario C |
|-----------------------|------------|------------|------------|
| Stack maturity        | X/10       | X/10       | X/10       |
| Operational complexity| X/10       | X/10       | X/10       |
| Vendor lock-in        | X/10       | X/10       | X/10       |
| Skill alignment       | X/10       | X/10       | X/10       |
| Scalability           | X/10       | X/10       | X/10       |

## Risk Comparison

| Risk Category    | Scenario A       | Scenario B       | Scenario C       |
|------------------|------------------|------------------|------------------|
| Technical        | <score + detail> | <score + detail> | <score + detail> |
| Organisational   | <score + detail> | <score + detail> | <score + detail> |
| Financial        | <score + detail> | <score + detail> | <score + detail> |
| Schedule         | <score + detail> | <score + detail> | <score + detail> |

## Timeline Comparison

| Milestone          | Scenario A  | Scenario B  | Scenario C  |
|--------------------|-------------|-------------|-------------|
| Planning complete  | Month X     | Month X     | Month X     |
| MVP / Phase 1      | Month X     | Month X     | Month X     |
| Full delivery      | Month X     | Month X     | Month X     |
| Benefits realised  | Month X     | Month X     | Month X     |

## Weighted Decision Matrix

| Criterion (Weight)       | Scenario A | Scenario B | Scenario C |
|--------------------------|------------|------------|------------|
| Cost — 25%               | X/10       | X/10       | X/10       |
| Technical fit — 25%      | X/10       | X/10       | X/10       |
| Risk — 20%               | X/10       | X/10       | X/10       |
| Timeline — 15%           | X/10       | X/10       | X/10       |
| Scalability — 15%        | X/10       | X/10       | X/10       |
| **Weighted Total**       | **X.X**    | **X.X**    | **X.X**    |

## Recommendation

**Go with: Scenario X — <Name>**

### Why This Scenario
<Clear reasoning>

### Key Trade-offs Accepted
- <What you give up>

### Go/No-Go Criteria
- [ ] <Criteria that must be true to proceed>
```

## Examples

### Example 1: Platform Choice

```
/scenario-compare Cloud-native rebuild vs Lift-and-shift vs Hybrid migration
```

### Example 2: Integration Approach

```
/scenario-compare REST API vs Event-driven vs Batch ETL --weights cost=30,risk=30,time=20,complexity=20
```

### Example 3: Build vs Buy

```
/scenario-compare Custom build vs Commercial platform vs Open-source solution --criteria cost,risk,time
```

---

**Invoke with:** `/scenario-compare <scenario-1> vs <scenario-2> [vs <scenario-3>]`
