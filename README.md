# Security GRC – Change Management Control Validator (Advanced)

## Objective

This project demonstrates a production-grade **Continuous Control Monitoring (CCM)** automation solution for enterprise change management. It ingests change logs, validates segregation of duties (SoD) and temporal controls against **PCI DSS 4.0.1 Requirement 6.5.1**, calculates risk-prioritized scores, and outputs decision-ready reports for both machines (JSON, CSV) and compliance officers (Markdown) [1].

---

## Key Features

*   **Automated Control Engine:** Evaluates mandatory approvals, segregation of duties (SoD), approver delegation authorization, and temporal sequencing.
*   **Evidence Integrity & Freshness:** Validates SHA-256 evidence hash formats and monitors evidence age against a configurable 90-day validity window.
*   **Scope Awareness:** Automatically filters out non-production environments (`DEVELOPMENT`, `UAT`) and cancelled changes (`NOT_APPLICABLE`).
*   **Risk-Based Prioritization:** Assigns a weighted `Risk Score` (0–100) and `Risk Level` (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) using worst-case analysis.
*   **Actionable Recommendations:** Automatically populates recommended remediation steps for every finding.
*   **Comprehensive Testing:** Fully backed by a robust `unittest` test suite covering 12 distinct compliance and negative test scenarios.
*   **Multi-Format Reporting:** Generates structured JSON, CSV summaries, and human-readable Markdown executive reports.

---

## Control & Framework Mapping

*   **Control ID & Name:** `CHG-001` — Independent Production Change Approval.
*   **Regulatory Framework:** **PCI DSS 4.0.1 – Requirement 6.5.1** (*Change control procedures for production systems*) [1].

| Automated Control Check | Compliance Objective | GRC Rationale |
| :--- | :--- | :--- |
| **Mandatory Approval** (`MISSING_APPROVAL`) | Documented authorization | Ensures no production change occurs without recorded sign-off. |
| **Segregation of Duties** (`SELF_APPROVAL`) | Independent parties | Prevents implementers from approving their own changes. |
| **Approver Authorization** (`UNAUTHORIZED_APPROVER`) | Authorized delegation | Validates that approvers possess formal delegation rights. |
| **Temporal Validation** (`APPROVAL_AFTER_IMPLEMENTATION`) | Preventative gate | Confirms approval timestamp precedes implementation. |
| **Evidence Integrity** (`INVALID_EVIDENCE_HASH`) | Non-repudiation | Verifies cryptographic integrity of audit artifacts (SHA-256). |
| **Evidence Freshness** (`STALE_EVIDENCE`) | Continuous monitoring | Flags approval documentation exceeding 90 days. |
| **Emergency Exception** (`EMERGENCY_REVIEW_REQUIRED`) | Exception handling | Isolates emergency overrides for mandatory retroactive CAB review. |

---

## Project Structure

```text
security-grc-code-challenge/
│
├── README.md               # Complete project documentation
├── requirements.txt        # Dependencies (Standard Library only)
├── generate_sample_data.py # Script to generate sample change logs
│
├── data/
│   └── changes.csv         # Expanded sample input dataset (8 scenarios)
│
├── src/
│   └── validator.py        # Main validation engine & CLI
│
├── tests/
│   └── test_validator.py   # Automated unit test suite (12 tests)
│
├── docs/
│   └── control_mapping.md  # Detailed framework mapping & risk methodology
│
└── output/                 # Generated compliance reports
    ├── validation_report.json
    ├── validation_summary.csv
    └── compliance_report.md
```

---

## How to Run

No external third-party libraries are required. Standard Python 3 is fully sufficient.

### 1. Run the Validation Engine
Execute the validator using default paths:
```bash
python3 src/validator.py
```

Or specify custom input/output paths via CLI:
```bash
python3 src/validator.py --input data/changes.csv --output-dir output
```

### 2. Run the Automated Test Suite
Verify control logic integrity:
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 tests/test_validator.py
```

---

## Sample Execution Results

| Change ID | System | Environment | Status | Risk Level | Recommended Action |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **CHG-001** | Payment API | PRODUCTION | `PASS` | `LOW` | No action required. Change is fully compliant. |
| **CHG-002** | Core Banking | PRODUCTION | `FAIL` | `CRITICAL` | Reject change. Enforce segregation of duties (SoD)... |
| **CHG-003** | Customer Portal | PRODUCTION | `FAIL` | `CRITICAL` | Reject change. Approver lacks formal delegation... |
| **CHG-004** | Mobile Banking | PRODUCTION | `FAIL` | `CRITICAL` | Initiate post-implementation review and enforce gate... |
| **CHG-005** | Pix Gateway | PRODUCTION | `FAIL` | `HIGH` | Request re-upload of integrity-verified evidence... |
| **CHG-006** | Fraud Engine | PRODUCTION | `EXCEPTION` | `MEDIUM` | Schedule retroactive Change Advisory Board (CAB) review... |
| **CHG-007** | Dev Sandbox | DEVELOPMENT | `NOT_APPLICABLE` | `LOW` | Control not applicable outside production environment. |
| **CHG-008** | Legacy System | PRODUCTION | `NOT_APPLICABLE` | `LOW` | Change status is CANCELLED; evaluation bypassed. |

---

## References

1. [PCI Security Standards Council - PCI DSS v4.0.1 Standard](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0-PT.pdf)
