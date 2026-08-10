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
    # 1. Fully compliant production change
    ["CHG-001", "Payment API", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "john.smith", "maria.silva", "TRUE", "2026-08-01T10:00:00Z", "2026-08-01T14:00:00Z", 
     "approval_CHG-001.pdf", valid_hash, "2026-08-01T10:01:00Z", "", "Deploy payment API version 2.4"],
    
    # 2. Self-approval violation (SoD)
    ["CHG-002", "Core Banking", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "john.smith", "john.smith", "TRUE", "2026-08-02T09:00:00Z", "2026-08-02T11:00:00Z", 
     "approval_CHG-002.pdf", valid_hash, "2026-08-02T09:01:00Z", "", "Database configuration change"],
    
    # 3. Unauthorized approver
    ["CHG-003", "Customer Portal", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "ana.souza", "intern.user", "FALSE", "2026-08-03T15:00:00Z", "2026-08-03T16:00:00Z", 
     "approval_CHG-003.pdf", valid_hash, "2026-08-03T15:01:00Z", "", "Update authentication module"],
    
    # 4. Approval after implementation (Temporal)
    ["CHG-004", "Mobile Banking", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "carlos.lima", "maria.silva", "TRUE", "2026-08-04T16:00:00Z", "2026-08-04T14:00:00Z", 
     "approval_CHG-004.pdf", valid_hash, "2026-08-04T16:01:00Z", "", "Mobile release"],
    
    # 5. Stale evidence & Invalid hash format
    ["CHG-005", "Pix Gateway", "PRODUCTION", "STANDARD", "IMPLEMENTED", 
     "paulo.santos", "maria.silva", "TRUE", "2026-04-01T10:00:00Z", "2026-04-01T14:00:00Z", 
     "approval_CHG-005.pdf", invalid_format, "2026-04-01T10:01:00Z", "", "Gateway configuration update"],
    
    # 6. Emergency change - No justification (Process failure)
    ["CHG-006", "Fraud Engine", "PRODUCTION", "EMERGENCY", "IMPLEMENTED", 
     "fernanda.costa", "maria.silva", "TRUE", "2026-08-05T02:00:00Z", "2026-08-05T02:15:00Z", 
     "approval_CHG-006.pdf", valid_hash, "2026-08-05T02:01:00Z", "", "Emergency fraud rule update"],
    
    # 7. Non-production environment (Not Applicable)
    ["CHG-007", "Dev Sandbox", "DEVELOPMENT", "STANDARD", "IMPLEMENTED", 
     "dev.user", "dev.user", "FALSE", "", "2026-08-06T10:00:00Z", "", "", "", "", "Test script"],
    
    # 8. Cancelled change (Not Evaluated)
    ["CHG-008", "Legacy System", "PRODUCTION", "STANDARD", "CANCELLED", 
     "old.user", "", "FALSE", "", "", "", "", "", "", "Abandoned update"]
]

with open("data/changes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(data)

print("Sample data generated successfully at data/changes.csv")
