---
description: Analyse infrastructure and system costs, identify optimisation opportunities, and generate savings recommendations using parallel agents
model: sonnet
---

# /cost-analysis

Analyse infrastructure, licensing, and operational costs across systems. Uses three parallel agents to evaluate infrastructure, licensing/SaaS, and operational dimensions, then produces a prioritised list of savings opportunities with implementation roadmaps.

## When to Use This Skill

- Reviewing cloud infrastructure spend for optimisation opportunities
- Preparing cost justifications for architecture changes
- Identifying redundant tooling or under-utilised licences
- Building business cases with financial projections
- Annual budget planning for technology costs

## Usage

```
/cost-analysis <scope> [--period monthly|quarterly|annual] [--target-savings percentage]
```

### Parameters

| Parameter          | Description                                      | Required |
|--------------------|--------------------------------------------------|----------|
| `scope`            | Systems or domain to analyse                     | Yes      |
| `--period`         | Cost reporting period (default: `monthly`)       | No       |
| `--target-savings` | Target savings percentage to aim for             | No       |

## Instructions

### Phase 1: Gather Cost Data

Prompt the user for available cost information:

| Data Source          | Description                                     | Example                           |
|----------------------|-------------------------------------------------|-----------------------------------|
| **Infrastructure**   | Cloud bills, hosting costs, network costs       | AWS Cost Explorer export, invoices|
| **Licensing**        | Software licence costs and utilisation           | SAP, Oracle, Salesforce licences  |
| **Staffing**         | Team costs allocated to systems                  | 3 FTEs for System X support       |
| **Contracts**        | Vendor contracts and renewal dates               | Support contract £50k/year        |

### Phase 2: Parallel Cost Analysis — Agent Team

Launch three agents simultaneously using the Task tool.

**Agent 1: Infrastructure Cost Analyst** (Sonnet)
Task: Analyse compute, storage, and networking costs
- Break down costs by service (compute, storage, network, database, monitoring)
- Identify over-provisioned resources (CPU utilisation < 30%, memory < 40%)
- Find unused or idle resources (stopped instances, unattached volumes, idle load balancers)
- Detect cost anomalies (sudden spikes, trending increases)
- Evaluate reserved vs on-demand vs spot pricing opportunities
- Suggest rightsizing recommendations with estimated savings
- Check for missing cost allocation tags
Return: Infrastructure cost breakdown with per-item savings opportunities and confidence levels

**Agent 2: Licensing and SaaS Analyst** (Sonnet)
Task: Review software licensing and SaaS subscription costs
- Catalogue all software licences and their costs
- Calculate licence utilisation rates (assigned vs active users)
- Identify redundant tools serving similar purposes
- Check for volume discount opportunities
- Review contract renewal dates and renegotiation windows
- Identify open-source alternatives for low-utilisation tools
- Flag shelfware (purchased but unused licences)
Return: Licensing cost analysis with consolidation recommendations and savings estimates

**Agent 3: Operational Cost Analyst** (Sonnet)
Task: Analyse staffing and operational costs
- Calculate support cost per system (staff hours x rate)
- Identify high-maintenance systems consuming disproportionate support time
- Find automation opportunities (manual processes that could be automated)
- Estimate the cost of technical debt (rework, workarounds, extended support)
- Calculate the cost of incidents (downtime, recovery effort)
- Project savings from proposed improvements
Return: Operational cost analysis with automation recommendations and ROI estimates

### Phase 3: Synthesise Cost Report

Combine all agent results:

1. **Create cost dashboard** — Total spend, breakdown by category, trends
2. **Rank savings opportunities** — By estimated impact (highest first)
3. **Calculate implementation effort** — For each recommendation
4. **Build implementation roadmap** — Quick wins first, then larger initiatives
5. **Project 3-year savings** — Cumulative savings over time

## Output Format

```markdown
# Cost Analysis: <Scope>

## Cost Dashboard

| Category           | Monthly Cost | Annual Cost | % of Total | Trend     |
|--------------------|-------------|-------------|------------|-----------|
| Infrastructure     | £X          | £X          | X%         | ↑ X%      |
| Licensing / SaaS   | £X          | £X          | X%         | → stable  |
| Operational        | £X          | £X          | X%         | ↓ X%      |
| **Total**          | **£X**      | **£X**      | **100%**   |           |

## Top 10 Savings Opportunities

| Rank | Opportunity                    | Est. Annual Saving | Effort  | Confidence | Quick Win? |
|------|-------------------------------|-------------------|---------|------------|------------|
| 1    | <Description>                  | £X                | Low     | High       | Yes        |
| 2    | <Description>                  | £X                | Medium  | Medium     | No         |

**Total Potential Savings:** £X/year (X% of current spend)

## Infrastructure Analysis

### Cost by Service

| Service    | Monthly Cost | Utilisation | Recommendation        | Saving   |
|------------|-------------|-------------|------------------------|----------|
| Compute    | £X          | X%          | Rightsize to X         | £X/month |
| Storage    | £X          | X%          | Lifecycle policy       | £X/month |
| Database   | £X          | X%          | Reserved instances     | £X/month |

### Unused Resources
<List of resources that can be safely removed>

## Licensing Analysis

### Licence Utilisation

| Software     | Licences | Active Users | Utilisation | Action             |
|--------------|----------|--------------|-------------|--------------------|
| <Product>    | X        | X            | X%          | Reduce by X        |

### Consolidation Opportunities
<Tools with overlapping capabilities>

## Operational Analysis

### Support Cost by System

| System        | Monthly FTE | Monthly Cost | Incidents/Month | Automation Potential |
|---------------|-------------|-------------|-----------------|---------------------|
| <System>      | X.X         | £X          | X               | High                |

### Automation Opportunities

| Process              | Current Cost | Automation Cost | Annual Saving | Payback  |
|----------------------|-------------|-----------------|---------------|----------|
| <Process>            | £X/year     | £X one-time     | £X/year       | X months |

## Implementation Roadmap

### Phase 1: Quick Wins (0-3 months)
- [ ] <Action> — £X/year saving

### Phase 2: Medium Effort (3-6 months)
- [ ] <Action> — £X/year saving

### Phase 3: Strategic (6-12 months)
- [ ] <Action> — £X/year saving

## 3-Year Projection

| Year    | Current Trajectory | With Optimisation | Cumulative Saving |
|---------|-------------------|-------------------|-------------------|
| Year 1  | £X                | £X                | £X                |
| Year 2  | £X                | £X                | £X                |
| Year 3  | £X                | £X                | £X                |
```

## Examples

### Example 1: Cloud Cost Optimisation

```
/cost-analysis "Production AWS Account" --period monthly --target-savings 20
```

Analyses AWS costs to find 20% savings through rightsizing, reserved instances, and unused resources.

### Example 2: Licensing Review

```
/cost-analysis "Enterprise SaaS Portfolio" --period annual
```

Annual review of all SaaS subscriptions to find consolidation and utilisation improvements.

### Example 3: System Cost Comparison

```
/cost-analysis "Legacy vs Modern Stack" --period annual
```

Compares operational costs between legacy and modern systems to build a migration business case.

---

**Invoke with:** `/cost-analysis <scope>` to identify and prioritise cost savings
