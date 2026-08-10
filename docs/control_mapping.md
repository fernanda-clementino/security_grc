# Control Mapping & Methodology — Change Management CCM

## 1. Overview

This document outlines the formal mapping between the automated security controls implemented in the **Security GRC Change Management Validator** and regulatory compliance frameworks, specifically **PCI DSS 4.0.1 Requirement 6.5.1** [1].

---

## 2. Framework Mapping

### PCI DSS 4.0.1 — Requirement 6.5.1
> *"Changes to system components in the production environment are approved by authorized parties, tested before release, and include procedures for returning to a secure state."* [1]

To operationalize and test this requirement programmatically, the control is decomposed into automated validation checks:

| Automated Control Check | Compliance Objective | Rationale for PCI DSS 6.5.1 Support |
| :--- | :--- | :--- |
| **Mandatory Approval** (`MISSING_APPROVAL`) | Documented authorization | Verifies that no production change is implemented without a recorded approval timestamp. |
| **Segregation of Duties** (`SELF_APPROVAL`) | Independent authorized parties | Ensures the implementer cannot unilaterally approve their own changes, mitigating insider threat and accidental release. |
| **Approver Authorization** (`UNAUTHORIZED_APPROVER`) | Authorized parties | Validates that the approver possesses formal delegation of authority in the change management system. |
| **Temporal Validation** (`APPROVAL_AFTER_IMPLEMENTATION`) | Preventative control enforcement | Confirms that approval occurred *prior* to production implementation. |
| **Evidence Integrity** (`INVALID_EVIDENCE_HASH`) | Non-repudiation & Audit Trail | Verifies that attached audit evidence maintains cryptographic integrity (SHA-256). |
| **Evidence Freshness** (`STALE_EVIDENCE`) | Continuous monitoring best practice | Identifies outdated approval documentation exceeding the 90-day threshold. |
| **Emergency Exception** (`EMERGENCY_MISSING_JUSTIFICATION`) | Exception handling & Review | Isolates emergency overrides to ensure mandatory justification and retroactive CAB review. |

---

## 3. Risk Scoring Methodology

The automated risk score (0–100) and risk level (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) are designed to prioritize remediation efforts for GRC teams using a **Worst-Case Analysis** model.

### Finding Weight Matrix

| Finding Type | Severity | Assigned Score | GRC Rationale |
| :--- | :---: | :---: | :--- |
| **Self-Approval (SoD)** | HIGH | 100 | Direct violation of internal controls and segregation of duties. |
| **Unauthorized Approver** | HIGH | 100 | Lack of governance delegation for production assets. |
| **Missing Approval** | HIGH | 100 | Absence of authorization record for production release. |
| **Approval After Implementation** | HIGH | 100 | Failure of preventative control gate. |
| **Missing Evidence** | HIGH | 80 | Inability to prove compliance during audit. |
| **Invalid Evidence Hash** | HIGH | 60 | Potential evidence tampering or formatting error. |
| **Stale Evidence** | MEDIUM | 40 | Documentation exceeds acceptable validity window. |
| **Emergency Missing Justification** | HIGH | 80 | Uncontrolled emergency release. |
| **Emergency Review Required** | MEDIUM | 30 | Emergency override requiring retroactive CAB sign-off. |

### Risk Level Thresholds
*   **CRITICAL (Score 80–100):** Immediate blocking, rollback consideration, or audit escalation.
*   **HIGH (Score 50–79):** Priority remediation required by security management.
*   **MEDIUM (Score 30–49):** Documentation refresh or exception review within standard cycle.
*   **LOW (Score 0–29):** Compliant or accepted low-risk condition.

---

## 4. Assumptions and Limitations

1.  **Simulated Dataset:** The validator consumes sample CSV data representing extracted change logs from platforms such as ServiceNow, Jira, or GitHub.
2.  **Hash Verification:** The script validates the 64-character hexadecimal format of SHA-256 hashes as a prototype for evidence integrity. In full production systems, hashes would be dynamically computed against attached object storage (e.g., S3 buckets).
3.  **Scope Applicability:** Changes outside the `PRODUCTION` environment (e.g., `DEVELOPMENT`, `STAGING`) or cancelled changes are automatically designated as `NOT_APPLICABLE` to reduce false positives.

---

## References

1. [PCI Security Standards Council - PCI DSS v4.0.1 Standard](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0-PT.pdf)
