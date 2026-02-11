---
description: Capture and structure non-functional requirements with measurable acceptance criteria
model: sonnet
---

# /nfr-capture

Capture and structure non-functional requirements (NFRs) across standard quality attribute categories. Generates measurable acceptance criteria, verification methods, and priority assignments based on ISO 25010 quality model.

## When to Use This Skill

- Starting a new project that needs documented NFRs
- Preparing for architecture reviews that require quality attributes
- Capturing performance, security, or scalability expectations
- Creating testable acceptance criteria for quality attributes
- Reviewing and formalising informal quality expectations

## Usage

```
/nfr-capture <system-or-project-name> [--categories performance,security,reliability] [--mode interactive|quick]
```

### Parameters

| Parameter      | Description                                          | Required |
|----------------|------------------------------------------------------|----------|
| `system`       | Name of the system or project                        | Yes      |
| `--categories` | Specific NFR categories to focus on (default: all)   | No       |
| `--mode`       | `interactive` prompts per category; `quick` generates from context | No |

## Instructions

### Phase 1: Establish Context

Gather from the user:

| Field              | Description                                   | Example                                |
|--------------------|-----------------------------------------------|----------------------------------------|
| **System name**    | What system are these NFRs for?               | OrderService                           |
| **System type**    | What kind of system?                          | Web application, API, batch process    |
| **User base**      | Who uses it and how many?                     | 500 internal users, 50k external/day   |
| **Criticality**    | How critical is this system?                  | Business-critical, customer-facing     |
| **Existing SLAs**  | Any existing service level agreements?        | 99.9% availability, <2s response time  |

### Phase 2: Walk Through NFR Categories

For each applicable category, prompt the user for specific requirements. Use the following categories based on ISO 25010:

#### Category 1: Performance

| Attribute        | Question to Ask                                    | Example Target            |
|------------------|----------------------------------------------------|---------------------------|
| Response time    | What is the acceptable response time?              | P95 < 500ms, P99 < 2s    |
| Throughput       | How many transactions per second?                  | 1,000 TPS sustained       |
| Batch processing | What batch volumes and time windows?               | 100k records in < 1 hour  |
| Concurrency      | How many concurrent users/connections?             | 500 concurrent users      |

#### Category 2: Reliability and Availability

| Attribute        | Question to Ask                                    | Example Target            |
|------------------|----------------------------------------------------|---------------------------|
| Availability     | What uptime percentage is required?                | 99.95% (21.9 min/month)  |
| Recovery time    | How quickly must the system recover from failure?  | RTO: 15 minutes           |
| Data durability  | How much data loss is acceptable?                  | RPO: 0 (zero data loss)   |
| Fault tolerance  | What failures must the system survive?             | Single AZ failure         |

#### Category 3: Security

| Attribute        | Question to Ask                                    | Example Target            |
|------------------|----------------------------------------------------|---------------------------|
| Authentication   | What auth mechanisms are required?                 | SSO with MFA              |
| Authorisation    | What access control model?                         | RBAC with least privilege |
| Data protection  | What data classification and encryption needs?     | AES-256 at rest, TLS 1.3 |
| Audit            | What must be logged and for how long?              | All access for 7 years    |

#### Category 4: Scalability

| Attribute        | Question to Ask                                    | Example Target            |
|------------------|----------------------------------------------------|---------------------------|
| Horizontal       | Can the system scale out?                          | Auto-scale 2-10 instances |
| Data growth      | Expected data growth rate?                         | 500 GB/year               |
| Peak handling    | How much above normal must it handle?              | 3x normal load            |

#### Category 5: Maintainability

| Attribute        | Question to Ask                                    | Example Target            |
|------------------|----------------------------------------------------|---------------------------|
| Deployment       | How quickly can changes be deployed?               | < 30 minutes, zero downtime |
| Monitoring       | What observability is required?                    | Metrics, logs, traces     |
| Documentation    | What documentation standards?                      | API docs, runbooks        |

#### Category 6: Usability

| Attribute        | Question to Ask                                    | Example Target            |
|------------------|----------------------------------------------------|---------------------------|
| Accessibility    | What accessibility standards?                      | WCAG 2.1 AA              |
| Responsiveness   | What devices must be supported?                    | Desktop, tablet, mobile   |
| Learnability     | How quickly should new users be productive?        | < 1 hour with training    |

#### Category 7: Compliance and Regulatory

| Attribute        | Question to Ask                                    | Example Target            |
|------------------|----------------------------------------------------|---------------------------|
| Regulations      | What regulations apply?                            | GDPR, SOX, PCI-DSS       |
| Data residency   | Where must data be stored?                         | EU only (eu-west-1)      |
| Retention        | How long must data be retained?                    | 7 years for financial     |

#### Category 8: Portability

| Attribute        | Question to Ask                                    | Example Target            |
|------------------|----------------------------------------------------|---------------------------|
| Cloud agnostic   | Must it run on multiple cloud providers?           | AWS primary, portable     |
| Containerised    | Container runtime requirements?                    | OCI-compliant containers  |

#### Category 9: Interoperability

| Attribute        | Question to Ask                                    | Example Target            |
|------------------|----------------------------------------------------|---------------------------|
| API standards    | What interface standards must be supported?         | REST/OpenAPI 3.0          |
| Data formats     | What data exchange formats?                         | JSON, Avro for streaming  |
| Protocols        | What communication protocols?                       | HTTPS, AMQP, gRPC        |

### Phase 3: Generate NFR Document

For each captured requirement, produce:

1. **Unique ID** — NFR-PERF-001, NFR-SEC-001, etc.
2. **Category** and attribute
3. **Requirement statement** — Clear, measurable text
4. **Acceptance criteria** — How to verify it's met
5. **Priority** — Must have / Should have / Could have
6. **Owner** — Who is responsible for ensuring compliance
7. **Verification method** — Test, review, monitoring, or audit

## Output Format

```markdown
# Non-Functional Requirements: <System Name>

## Summary

| Category        | Count | Must Have | Should Have | Could Have |
|-----------------|-------|-----------|-------------|------------|
| Performance     | X     | X         | X           | X          |
| Reliability     | X     | X         | X           | X          |
| Security        | X     | X         | X           | X          |
| ...             | ...   | ...       | ...         | ...        |
| **Total**       | **X** | **X**     | **X**       | **X**      |

## Performance

### NFR-PERF-001: Response Time
- **Requirement:** API responses shall complete within 500ms at P95 under normal load
- **Acceptance Criteria:** Load test demonstrates P95 < 500ms with 500 concurrent users
- **Priority:** Must have
- **Owner:** Engineering team
- **Verification:** Load testing (k6/Gatling)

### NFR-PERF-002: Throughput
...

## Reliability

### NFR-REL-001: Availability
...

## Traceability Matrix

| NFR ID        | Category    | Linked Component       | Verification Status |
|---------------|-------------|------------------------|---------------------|
| NFR-PERF-001  | Performance | API Gateway            | Not tested          |
```

## Examples

### Example 1: Full NFR Capture

```
/nfr-capture OrderService --mode interactive
```

Walks through all NFR categories interactively, prompting for specific targets per category.

### Example 2: Focused Categories

```
/nfr-capture PaymentGateway --categories performance,security,compliance
```

Focuses on performance, security, and compliance NFRs for a payment system.

### Example 3: Quick Generation

```
/nfr-capture InventoryAPI --mode quick
```

Generates sensible default NFRs based on system type and context, ready for user review and adjustment.

---

**Invoke with:** `/nfr-capture <system-name>` then answer category-specific prompts
