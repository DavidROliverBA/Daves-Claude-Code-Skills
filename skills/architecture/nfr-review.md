---
description: Review non-functional requirements for completeness, measurability, and feasibility using parallel agents
model: sonnet
---

# /nfr-review

Review existing non-functional requirements for completeness, measurability, and feasibility. Uses three parallel agents to evaluate coverage against ISO 25010, check that every requirement has quantifiable targets, and identify conflicts or infeasible targets.

## When to Use This Skill

- Reviewing NFRs before architecture board submission
- Validating that captured requirements are testable and measurable
- Checking NFR coverage gaps for a system type
- Identifying conflicting requirements that need trade-off discussions
- Preparing NFRs for inclusion in contracts or SLAs

## Usage

```
/nfr-review <path-to-nfr-document> [--system-type web|api|batch|mobile|iot]
```

### Parameters

| Parameter       | Description                                     | Required |
|-----------------|-------------------------------------------------|----------|
| `path`          | Path to the NFR document or note                | Yes      |
| `--system-type` | System type for contextual gap analysis         | No       |

## Instructions

### Phase 1: Parse Existing NFRs

Read the specified NFR document and extract:
- All NFR statements with their IDs, categories, and targets
- Any acceptance criteria or verification methods
- Priority assignments
- Owner assignments

### Phase 2: Parallel Review — Agent Team

Launch three agents simultaneously using the Task tool.

**Agent 1: Completeness Reviewer** (Sonnet)
Task: Check NFR coverage against ISO 25010 quality model
- Map existing NFRs to ISO 25010 quality characteristics
- Identify categories with no NFRs (gaps)
- Compare coverage against expected categories for the system type:
  - Web app: Performance, Security, Usability, Accessibility required
  - API: Performance, Reliability, Security, Interoperability required
  - Batch: Performance (throughput), Reliability (recovery), Maintainability required
  - Mobile: Usability, Performance, Portability, Offline capability required
- Flag categories that are typically critical for this system type but missing
- Check for orphan NFRs that don't map to any quality characteristic
Return: Coverage matrix showing present/absent categories with gap severity ratings

**Agent 2: Measurability Reviewer** (Sonnet)
Task: Verify every NFR is quantifiable and testable
- Check each NFR for specific, numeric targets (not "fast" but "< 500ms")
- Verify acceptance criteria exist and are testable
- Flag vague language: "should be fast", "highly available", "secure", "scalable"
- Flag missing units, thresholds, or percentiles
- For each vague NFR, suggest a concrete, measurable replacement
- Check verification methods are appropriate (test, audit, review, monitoring)
Return: Measurability scorecard — each NFR rated as Measurable / Partially Measurable / Vague, with suggested improvements

**Agent 3: Feasibility Reviewer** (Sonnet)
Task: Check that NFR targets are realistic and non-conflicting
- Identify NFRs with unrealistic targets (e.g., 100% availability, 0ms latency)
- Find conflicting requirements:
  - Performance vs Security (encryption overhead vs response time)
  - Availability vs Cost (multi-region vs budget constraints)
  - Scalability vs Simplicity (distributed vs monolith)
- Check that NFRs are achievable with stated technology choices
- Identify NFRs that require clarification or stakeholder discussion
- Flag NFRs with no priority or owner assigned
Return: Feasibility assessment per NFR with conflicts and recommendations

### Phase 3: Synthesise Review Report

Combine agent results into a review report:

1. **Calculate overall NFR quality score** (0-100)
2. **List all gaps** by severity
3. **List all measurability issues** with suggested fixes
4. **List all conflicts** requiring trade-off discussions
5. **Prioritise remediation actions**

## Output Format

```markdown
# NFR Review: <System/Project Name>

## Review Summary

**Overall Score:** X/100
**Grade:** A (90+) / B (80-89) / C (70-79) / D (60-69) / F (<60)

| Dimension      | Score | Issues Found |
|----------------|-------|--------------|
| Completeness   | X/100 | X gaps       |
| Measurability  | X/100 | X vague NFRs |
| Feasibility    | X/100 | X conflicts  |

## Coverage Gaps

| Missing Category | Expected For System Type | Severity | Suggested NFR              |
|------------------|--------------------------|----------|----------------------------|
| Accessibility    | Web application          | High     | WCAG 2.1 AA compliance     |
| Data residency   | Handles PII              | Critical | EU-only data storage       |

## Measurability Issues

| NFR ID        | Current Text                    | Issue          | Suggested Improvement              |
|---------------|----------------------------------|----------------|-------------------------------------|
| NFR-PERF-003  | "Must be fast"                  | Vague          | "P95 response time < 500ms"        |
| NFR-SEC-001   | "Must be secure"                | No criteria    | "TLS 1.3, AES-256 at rest, OWASP" |

## Conflicts Requiring Resolution

| NFR A          | NFR B          | Conflict                              | Recommendation         |
|----------------|----------------|---------------------------------------|------------------------|
| NFR-PERF-001   | NFR-SEC-002    | Encryption adds 50ms latency          | Revise P95 to 550ms   |

## Feasibility Concerns

| NFR ID        | Issue                                    | Recommendation              |
|---------------|------------------------------------------|-----------------------------|
| NFR-REL-001   | 99.999% availability requires multi-region | Confirm budget for multi-AZ |

## Remediation Actions (Prioritised)

1. **Critical:** <action>
2. **High:** <action>
3. **Medium:** <action>
```

## Examples

### Example 1: Review Web Application NFRs

```
/nfr-review path/to/order-service-nfrs.md --system-type web
```

Reviews NFRs for a web application, checking for missing usability and accessibility requirements.

### Example 2: Review API NFRs

```
/nfr-review path/to/payment-api-nfrs.md --system-type api
```

Reviews API NFRs with focus on interoperability, rate limiting, and contract testing requirements.

---

**Invoke with:** `/nfr-review <path-to-nfr-document>` to get a comprehensive quality assessment
