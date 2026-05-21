from ai_automation_audit import (
    AutomationAuditStatus,
    create_automation_audit_record,
    verify_automation_audit_record,
)


def valid_record():
    return create_automation_audit_record(
        "audit-1",
        "workflow",
        "daily-sync",
        "2026-05-21T00:00:00Z",
        metadata={"reviewed": True},
    )


def test_verified_automation_record():
    result = verify_automation_audit_record(valid_record())
    assert result["status"] == AutomationAuditStatus.VERIFIED


def test_review_required_for_auto_execute():
    record = create_automation_audit_record(
        "audit-2",
        "automation",
        "agent-runner",
        "2026-05-21T00:00:00Z",
        metadata={"auto_execute": True, "network_access": True},
    )

    result = verify_automation_audit_record(record)
    assert result["status"] == AutomationAuditStatus.REVIEW_REQUIRED


def test_invalid_hash_detection():
    record = valid_record()
    record["workflow_name"] = "tampered"

    result = verify_automation_audit_record(record)
    assert result["status"] == AutomationAuditStatus.INVALID


def test_invalid_agent_type():
    record = create_automation_audit_record(
        "audit-3",
        "unknown",
        "workflow",
        "2026-05-21T00:00:00Z",
    )

    result = verify_automation_audit_record(record)
    assert result["status"] == AutomationAuditStatus.INVALID
