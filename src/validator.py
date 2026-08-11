import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path


CONTROL_ID = "CHG-001"
CONTROL_NAME = "Independent Production Change Approval"
FRAMEWORK = "PCI DSS 4.0.1"
FRAMEWORK_REQUIREMENT = "6.5.1"
FRAMEWORK_DESCRIPTION = "Production changes must follow documented change control procedures including authorization by authorized parties."

STALE_DAYS = 90

RISK_WEIGHTS = {
    "MISSING_REQUIRED_FIELD": 100,
    "SELF_APPROVAL": 100,
    "UNAUTHORIZED_APPROVER": 100,
    "MISSING_APPROVAL": 100,
    "APPROVAL_AFTER_IMPLEMENTATION": 100,
    "MISSING_EVIDENCE": 80,
    "INVALID_EVIDENCE_HASH": 60,
    "STALE_EVIDENCE": 40,
    "MISSING_DOCUMENTATION": 40,
    "EMERGENCY_MISSING_JUSTIFICATION": 80,
    "EMERGENCY_REVIEW_REQUIRED": 30
}

SHA256_REGEX = re.compile(r"^[a-fA-F0-9]{64}$")


def parse_datetime(value):
    if not value or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def calculate_risk(findings):
    if not findings:
        return 0, "LOW"
    
    max_score = 0
    for finding in findings:
        score = RISK_WEIGHTS.get(finding["type"], 20)
        if score > max_score:
            max_score = score

    if max_score >= 80:
        level = "CRITICAL"
    elif max_score >= 50:
        level = "HIGH"
    elif max_score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return max_score, level


def get_recommended_action(findings):
    if not findings:
        return "No action required. Change is fully compliant."
    
    finding_types = [f["type"] for f in findings]
    
    if "MISSING_REQUIRED_FIELD" in finding_types:
        return "Reject change record. Data quality failure: mandatory metadata is missing."
    if "SELF_APPROVAL" in finding_types:
        return "Reject change. Enforce segregation of duties (SoD) by requiring an independent approver."
    if "UNAUTHORIZED_APPROVER" in finding_types:
        return "Reject change. Approver lacks formal delegation of authority or authorization status is unverified."
    if "MISSING_APPROVAL" in finding_types or "MISSING_EVIDENCE" in finding_types:
        return "Halt deployment. Obtain formal authorization and attach audit evidence before releasing to production."
    if "APPROVAL_AFTER_IMPLEMENTATION" in finding_types:
        return "Initiate post-implementation review and enforce pre-deployment gate in CI/CD pipeline."
    if "INVALID_EVIDENCE_HASH" in finding_types:
        return "Request re-upload of integrity-verified evidence artifact (SHA-256 format check)."
    if "STALE_EVIDENCE" in finding_types:
        return "Refresh approval documentation to comply with the 90-day challenge validity window."
    if "EMERGENCY_MISSING_JUSTIFICATION" in finding_types:
        return "Require immediate retroactive documentation and management sign-off for emergency change."
    if "EMERGENCY_REVIEW_REQUIRED" in finding_types:
        return "Schedule retroactive Change Advisory Board (CAB) review for emergency override."
    
    return "Review findings and remediate control gaps."


def validate_change(change):
    findings = []
    
    environment = change.get("environment", "").strip().upper()
    change_status = change.get("change_status", "").strip().upper()
    change_id = change.get("change_id", "").strip()
    system = change.get("system", "").strip()
    
    # 0. Data Quality Check (Fail-Safe mandatory fields)
    mandatory_fields = ["change_id", "system", "environment", "change_status", "implementer"]
    missing_fields = [field for field in mandatory_fields if not change.get(field, "").strip()]
    
    if missing_fields:
        findings.append({
            "type": "MISSING_REQUIRED_FIELD",
            "severity": "HIGH",
            "message": f"Data quality failure: mandatory fields missing: {', '.join(missing_fields)}"
        })
        risk_score, risk_level = calculate_risk(findings)
        return {
            "change_id": change_id or "UNKNOWN",
            "system": system or "UNKNOWN",
            "environment": environment or "UNKNOWN",
            "status": "FAIL",
            "risk_score": risk_score,
            "risk_level": risk_level,
            "framework_impact": f"{FRAMEWORK} - Requirement {FRAMEWORK_REQUIREMENT}",
            "recommended_action": get_recommended_action(findings),
            "findings": findings
        }

    # Check applicability
    if environment != "PRODUCTION":
        return {
            "change_id": change_id,
            "system": system,
            "environment": environment,
            "status": "NOT_APPLICABLE",
            "risk_score": 0,
            "risk_level": "LOW",
            "findings": [],
            "recommended_action": "Control not applicable outside production environment."
        }
        
    if change_status in ["CANCELLED", "ABANDONED", "DRAFT"]:
        return {
            "change_id": change_id,
            "system": system,
            "environment": environment,
            "status": "NOT_APPLICABLE",
            "risk_score": 0,
            "risk_level": "LOW",
            "findings": [],
            "recommended_action": f"Change status is {change_status}; evaluation bypassed."
        }

    implemented_at = parse_datetime(change.get("implemented_at"))
    approved_at = parse_datetime(change.get("approved_at"))
    evidence_date = parse_datetime(change.get("evidence_date"))
    evidence_hash = change.get("evidence_hash", "").strip()
    implementer = change.get("implementer", "").strip().lower()
    approver = change.get("approver", "").strip().lower()
    
    # Fail-Safe: If approver_authorized is missing or not explicitly TRUE, consider unverified/unauthorized
    approver_authorized_val = change.get("approver_authorized", "").strip().upper()
    approver_authorized = (approver_authorized_val == "TRUE")
    
    change_type = change.get("change_type", "STANDARD").upper()
    emergency_justification = change.get("emergency_justification", "").strip()

    # 1. Approval evidence check
    if not change.get("approval_evidence"):
        findings.append({
            "type": "MISSING_EVIDENCE",
            "severity": "HIGH",
            "message": "Approval evidence artifact is missing."
        })
    elif evidence_hash:
        # 1.1 Evidence integrity hash check (SHA-256 format validation prototype)
        if not SHA256_REGEX.match(evidence_hash):
            findings.append({
                "type": "INVALID_EVIDENCE_HASH",
                "severity": "HIGH",
                "message": "Evidence hash format is invalid (expected 64-char SHA-256 hex)."
            })

    # 2. Approval existence check
    if not approved_at:
        findings.append({
            "type": "MISSING_APPROVAL",
            "severity": "HIGH",
            "message": "No approval timestamp was provided."
        })

    # 3. Temporal validation (Approval before implementation)
    if approved_at and implemented_at and approved_at > implemented_at:
        findings.append({
            "type": "APPROVAL_AFTER_IMPLEMENTATION",
            "severity": "HIGH",
            "message": "Change was implemented before formal approval timestamp."
        })

    # 4. Segregation of Duties (SoD) check
    if implementer and approver and implementer == approver:
        findings.append({
            "type": "SELF_APPROVAL",
            "severity": "HIGH",
            "message": "Implementer and approver are the same individual (SoD violation)."
        })

    # 5. Approver Authorization check (Fail-Safe enforcement)
    if approver and not approver_authorized:
        findings.append({
            "type": "UNAUTHORIZED_APPROVER",
            "severity": "HIGH",
            "message": "Approver authorization is missing, unverified, or explicitly unauthorized."
        })

    # 6. Evidence freshness check (Challenge demonstration threshold)
    if evidence_date:
        age_days = (datetime.now(timezone.utc) - evidence_date).days
        if age_days > STALE_DAYS:
            findings.append({
                "type": "STALE_EVIDENCE",
                "severity": "MEDIUM",
                "message": f"Evidence is {age_days} days old (exceeds challenge {STALE_DAYS}-day freshness window)."
            })

    # 7. Mandatory documentation check
    if not change.get("change_description"):
        findings.append({
            "type": "MISSING_DOCUMENTATION",
            "severity": "MEDIUM",
            "message": "Change description / business rationale is missing."
        })

    # 8. Change Type / Emergency handling
    if change_type == "EMERGENCY":
        if not emergency_justification:
            findings.append({
                "type": "EMERGENCY_MISSING_JUSTIFICATION",
                "severity": "HIGH",
                "message": "Emergency change lacks documented business justification."
            })
        else:
            findings.append({
                "type": "EMERGENCY_REVIEW_REQUIRED",
                "severity": "MEDIUM",
                "message": "Emergency change requires mandatory retroactive CAB review."
            })

    status = "PASS"
    if any(f["severity"] == "HIGH" for f in findings):
        status = "FAIL"
    elif any(f["type"] == "EMERGENCY_REVIEW_REQUIRED" for f in findings) and not any(f["severity"] == "HIGH" for f in findings):
        status = "EXCEPTION"
    elif findings:
        status = "PASS_WITH_FINDINGS"

    risk_score, risk_level = calculate_risk(findings)
    recommended_action = get_recommended_action(findings)

    return {
        "change_id": change_id,
        "system": system,
        "environment": environment,
        "status": status,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "framework_impact": f"{FRAMEWORK} - Requirement {FRAMEWORK_REQUIREMENT}",
        "recommended_action": recommended_action,
        "findings": findings
    }


def load_changes(path):
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def generate_markdown_report(report, output_path):
    control = report["control"]
    summary = report["summary"]
    results = report["results"]

    lines = [
        f"# Continuous Control Monitoring - Compliance Report",
        f"",
        f"**Control ID:** {control['id']}  ",
        f"**Control Name:** {control['name']}  ",
        f"**Framework:** {control['framework']} (Requirement {control['requirement']})  ",
        f"**Objective:** {control['description']}  ",
        f"",
        f"## Executive Summary",
        f"",
        f"| Metric | Count |",
        f"| :--- | :---: |",
        f"| Total Evaluated Changes | {summary['total']} |",
        f"| Passing Controls (`PASS`) | {summary['pass']} |",
        f"| Failing Controls (`FAIL`) | {summary['fail']} |",
        f"| Passing with Findings (`PASS_WITH_FINDINGS`) | {summary['pass_with_findings']} |",
        f"| Exceptions (`EXCEPTION`) | {summary['exception']} |",
        f"| Not Applicable (`NOT_APPLICABLE`) | {summary['not_applicable']} |",
        f"",
        f"## Detailed Evaluation Results",
        f"",
        f"| Change ID | System | Env | Status | Risk | Recommended Action |",
        f"| :--- | :--- | :--- | :--- | :---: | :--- |"
    ]

    for r in results:
        lines.append(
            f"| {r['change_id']} | {r['system']} | {r.get('environment', 'N/A')} | `{r['status']}` | **{r['risk_level']}** ({r['risk_score']}) | {r['recommended_action']} |"
        )

    lines.extend([
        f"",
        f"---",
        f"*Report generated automatically by Security GRC Change Management Validator (CCM Prototype).*"
    ])

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Security GRC Change Management Control Validator")
    parser.add_argument("--input", default="data/changes.csv", help="Path to input changes CSV file")
    parser.add_argument("--output-dir", default="output", help="Directory for output reports")
    args = parser.parse_args()

    input_file = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_file.exists():
        print(f"Error: Input file {input_file} not found.")
        return

    changes = load_changes(input_file)
    results = [validate_change(change) for change in changes]

    report = {
        "control": {
            "id": CONTROL_ID,
            "name": CONTROL_NAME,
            "framework": FRAMEWORK,
            "requirement": FRAMEWORK_REQUIREMENT,
            "description": FRAMEWORK_DESCRIPTION
        },
        "summary": {
            "total": len(results),
            "pass": sum(r["status"] == "PASS" for r in results),
            "fail": sum(r["status"] == "FAIL" for r in results),
            "exception": sum(r["status"] == "EXCEPTION" for r in results),
            "pass_with_findings": sum(r["status"] == "PASS_WITH_FINDINGS" for r in results),
            "not_applicable": sum(r["status"] == "NOT_APPLICABLE" for r in results)
        },
        "results": results
    }

    # Write JSON report
    with open(output_dir / "validation_report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    # Write CSV summary
    with open(output_dir / "validation_summary.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["change_id", "system", "environment", "status", "risk_score", "risk_level", "framework_impact", "recommended_action"])
        for result in results:
            writer.writerow([
                result["change_id"],
                result["system"],
                result.get("environment", "PRODUCTION"),
                result["status"],
                result["risk_score"],
                result["risk_level"],
                result.get("framework_impact", ""),
                result.get("recommended_action", "")
            ])

    # Write Markdown human report
    generate_markdown_report(report, output_dir / "compliance_report.md")

    print("Validation completed successfully.")
    print(f"Total changes: {len(results)}")
    print(f"PASS: {report['summary']['pass']}")
    print(f"FAIL: {report['summary']['fail']}")
    print(f"EXCEPTION: {report['summary']['exception']}")
    print(f"PASS_WITH_FINDINGS: {report['summary']['pass_with_findings']}")
    print(f"NOT_APPLICABLE: {report['summary']['not_applicable']}")
    print(f"Reports saved to {output_dir}/")


if __name__ == "__main__":
    main()
