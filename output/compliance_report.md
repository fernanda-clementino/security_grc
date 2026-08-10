# Continuous Control Monitoring - Compliance Report

**Control ID:** CHG-001  
**Control Name:** Independent Production Change Approval  
**Framework:** PCI DSS 4.0.1 (Requirement 6.5.1)  
**Objective:** Production changes must follow documented change control procedures including authorization by authorized parties.  

## Executive Summary

| Metric | Count |
| :--- | :---: |
| Total Evaluated Changes | 8 |
| Passing Controls (`PASS`) | 1 |
| Failing Controls (`FAIL`) | 5 |
| Passing with Findings (`PASS_WITH_FINDINGS`) | 0 |
| Exceptions (`EXCEPTION`) | 0 |
| Not Applicable (`NOT_APPLICABLE`) | 2 |

## Detailed Evaluation Results

| Change ID | System | Env | Status | Risk | Recommended Action |
| :--- | :--- | :--- | :--- | :---: | :--- |
| CHG-001 | Payment API | PRODUCTION | `PASS` | **LOW** (0) | No action required. Change is fully compliant. |
| CHG-002 | Core Banking | PRODUCTION | `FAIL` | **CRITICAL** (100) | Reject change. Enforce segregation of duties (SoD) by requiring an independent approver. |
| CHG-003 | Customer Portal | PRODUCTION | `FAIL` | **CRITICAL** (100) | Reject change. Approver lacks formal delegation of authority for production changes. |
| CHG-004 | Mobile Banking | PRODUCTION | `FAIL` | **CRITICAL** (100) | Initiate post-implementation review and enforce pre-deployment gate in CI/CD pipeline. |
| CHG-005 | Pix Gateway | PRODUCTION | `FAIL` | **HIGH** (60) | Request re-upload of integrity-verified evidence artifact (SHA-256). |
| CHG-006 | Fraud Engine | PRODUCTION | `FAIL` | **CRITICAL** (80) | Require immediate retroactive documentation and management sign-off for emergency change. |
| CHG-007 | Dev Sandbox | DEVELOPMENT | `NOT_APPLICABLE` | **LOW** (0) | Control not applicable outside production environment. |
| CHG-008 | Legacy System | PRODUCTION | `NOT_APPLICABLE` | **LOW** (0) | Change status is CANCELLED; evaluation bypassed. |

---
*Report generated automatically by Security GRC Change Management Validator.*
