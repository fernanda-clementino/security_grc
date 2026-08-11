import csv

valid_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
invalid_format = "invalid-hash-format"

headers = [
    "change_id", "system", "environment", "change_type", "change_status",
    "implementer", "approver", "approver_authorized", "approved_at",
    "implemented_at", "approval_evidence", "evidence_hash", "evidence_date",
    "emergency_justification", "change_description"
]

data = [
    # 1. Fully compliant production change (PASS)
    ["CHG-001", "Payment API", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "john.smith", "maria.silva", "TRUE", "2026-08-01T10:00:00Z", "2026-08-01T14:00:00Z", 
     "approval_CHG-001.pdf", valid_hash, "2026-08-01T10:01:00Z", "", "Deploy payment API version 2.4"],
    
    # 2. Self-approval violation (FAIL)
    ["CHG-002", "Core Banking", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "john.smith", "john.smith", "TRUE", "2026-08-02T09:00:00Z", "2026-08-02T11:00:00Z", 
     "approval_CHG-002.pdf", valid_hash, "2026-08-02T09:01:00Z", "", "Database configuration change"],
    
    # 3. Unauthorized approver (FAIL)
    ["CHG-003", "Customer Portal", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "ana.souza", "intern.user", "FALSE", "2026-08-03T15:00:00Z", "2026-08-03T16:00:00Z", 
     "approval_CHG-003.pdf", valid_hash, "2026-08-03T15:01:00Z", "", "Update authentication module"],
    
    # 4. Approval after implementation (FAIL)
    ["CHG-004", "Mobile Banking", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "carlos.lima", "maria.silva", "TRUE", "2026-08-04T16:00:00Z", "2026-08-04T14:00:00Z", 
     "approval_CHG-004.pdf", valid_hash, "2026-08-04T16:01:00Z", "", "Mobile release"],
    
    # 5. Stale evidence & Invalid hash format (FAIL)
    ["CHG-005", "Pix Gateway", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "paulo.santos", "maria.silva", "TRUE", "2026-04-01T10:00:00Z", "2026-04-01T14:00:00Z", 
     "approval_CHG-005.pdf", invalid_format, "2026-04-01T10:01:00Z", "", "Gateway configuration update"],
    
    # 6. Emergency change - Valid justification (EXCEPTION)
    ["CHG-006", "Fraud Engine", "PRODUCTION", "EMERGENCY", "IMPLEMENTED", 
     "fernanda.costa", "maria.silva", "TRUE", "2026-08-05T02:00:00Z", "2026-08-05T02:15:00Z", 
     "approval_CHG-006.pdf", valid_hash, "2026-08-05T02:01:00Z", "Critical security patch for zero-day fraud exploit", "Emergency fraud rule update"],
    
    # 7. Non-production environment (NOT_APPLICABLE)
    ["CHG-007", "Dev Sandbox", "DEVELOPMENT", "STANDARD", "IMPLEMENTED", 
     "dev.user", "dev.user", "FALSE", "", "2026-08-06T10:00:00Z", "", "", "", "", "Test script"],
    
    # 8. Data Quality Issue - Missing implementer (FAIL)
    ["CHG-008", "Legacy System", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "", "maria.silva", "TRUE", "2026-08-07T10:00:00Z", "2026-08-07T11:00:00Z", "doc.pdf", valid_hash, "2026-08-07T10:01:00Z", "", "Change with missing implementer data"],
    
    # 9. Fail-Safe Test - Missing approver_authorized (FAIL)
    ["CHG-009", "Reporting Tool", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "user.x", "user.y", "", "2026-08-08T09:00:00Z", "2026-08-08T10:00:00Z", "doc.pdf", valid_hash, "2026-08-08T09:01:00Z", "", "Change with missing authorization data"],
     
    # 10. Pass with Findings - Missing description only (PASS_WITH_FINDINGS)
    ["CHG-010", "Inventory App", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "roberto.nunes", "maria.silva", "TRUE", "2026-08-09T10:00:00Z", "2026-08-09T11:00:00Z", 
     "approval_CHG-010.pdf", valid_hash, "2026-08-09T10:01:00Z", "", ""]
]

with open("data/changes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(data)

print("Sample data updated with 10 scenarios at data/changes.csv")
