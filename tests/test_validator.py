import unittest
from datetime import datetime, timezone, timedelta
from src.validator import validate_change, calculate_risk

class TestGRCValidator(unittest.TestCase):

    def setUp(self):
        self.valid_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.base_change = {
            "change_id": "CHG-TEST",
            "system": "TestSys",
            "environment": "PRODUCTION",
            "change_type": "STANDARD",
            "change_status": "IMPLEMENTED",
            "implementer": "user.a",
            "approver": "user.b",
            "approver_authorized": "TRUE",
            "approved_at": "2026-08-01T10:00:00Z",
            "implemented_at": "2026-08-01T11:00:00Z",
            "approval_evidence": "doc.pdf",
            "evidence_hash": self.valid_hash,
            "evidence_date": datetime.now(timezone.utc).isoformat(),
            "change_description": "Valid test change"
        }

    def test_01_fully_compliant_pass(self):
        result = validate_change(self.base_change)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["risk_score"], 0)

    def test_02_self_approval_fail(self):
        change = self.base_change.copy()
        change["approver"] = "user.a"
        result = validate_change(change)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(f["type"] == "SELF_APPROVAL" for f in result["findings"]))
        self.assertEqual(result["risk_score"], 100)

    def test_03_unauthorized_approver_fail(self):
        change = self.base_change.copy()
        change["approver_authorized"] = "FALSE"
        result = validate_change(change)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(f["type"] == "UNAUTHORIZED_APPROVER" for f in result["findings"]))
        self.assertEqual(result["risk_score"], 100)

    def test_04_temporal_violation_fail(self):
        change = self.base_change.copy()
        change["approved_at"] = "2026-08-01T12:00:00Z"
        change["implemented_at"] = "2026-08-01T11:00:00Z"
        result = validate_change(change)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(f["type"] == "APPROVAL_AFTER_IMPLEMENTATION" for f in result["findings"]))

    def test_05_missing_evidence_fail(self):
        change = self.base_change.copy()
        change["approval_evidence"] = ""
        result = validate_change(change)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(f["type"] == "MISSING_EVIDENCE" for f in result["findings"]))

    def test_06_stale_evidence_warning(self):
        change = self.base_change.copy()
        stale_date = (datetime.now(timezone.utc) - timedelta(days=100)).isoformat()
        change["evidence_date"] = stale_date
        result = validate_change(change)
        self.assertEqual(result["status"], "PASS_WITH_FINDINGS")
        self.assertTrue(any(f["type"] == "STALE_EVIDENCE" for f in result["findings"]))
        self.assertEqual(result["risk_score"], 40)

    def test_07_invalid_hash_format_fail(self):
        change = self.base_change.copy()
        change["evidence_hash"] = "short-hash"
        result = validate_change(change)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(f["type"] == "INVALID_EVIDENCE_HASH" for f in result["findings"]))

    def test_08_emergency_with_justification_exception(self):
        change = self.base_change.copy()
        change["change_type"] = "EMERGENCY"
        change["emergency_justification"] = "Fixing critical production bug"
        result = validate_change(change)
        self.assertEqual(result["status"], "EXCEPTION")
        self.assertTrue(any(f["type"] == "EMERGENCY_REVIEW_REQUIRED" for f in result["findings"]))

    def test_09_emergency_without_justification_fail(self):
        change = self.base_change.copy()
        change["change_type"] = "EMERGENCY"
        change["emergency_justification"] = ""
        result = validate_change(change)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(f["type"] == "EMERGENCY_MISSING_JUSTIFICATION" for f in result["findings"]))

    def test_10_non_production_not_applicable(self):
        change = self.base_change.copy()
        change["environment"] = "DEVELOPMENT"
        result = validate_change(change)
        self.assertEqual(result["status"], "NOT_APPLICABLE")
        self.assertEqual(len(result["findings"]), 0)

    def test_11_cancelled_change_not_applicable(self):
        change = self.base_change.copy()
        change["change_status"] = "CANCELLED"
        result = validate_change(change)
        self.assertEqual(result["status"], "NOT_APPLICABLE")

    def test_12_risk_logic_worst_case(self):
        # Test that Critical (100) overrides Medium (40)
        findings = [
            {"type": "SELF_APPROVAL"}, # 100
            {"type": "STALE_EVIDENCE"}  # 40
        ]
        score, level = calculate_risk(findings)
        self.assertEqual(score, 100)
        self.assertEqual(level, "CRITICAL")

if __name__ == "__main__":
    unittest.main()
