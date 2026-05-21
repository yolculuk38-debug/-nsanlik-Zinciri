from protocol_self_integrity import (
    REQUIRED_CORE_MODULES,
    SelfIntegrityStatus,
    build_self_integrity_manifest,
    verify_self_integrity_manifest,
)


def full_manifest():
    modules = {module: "v1" for module in REQUIRED_CORE_MODULES}
    return build_self_integrity_manifest(modules)


def test_verified_self_integrity():
    result = verify_self_integrity_manifest(full_manifest())
    assert result["status"] == SelfIntegrityStatus.VERIFIED
    assert result["verified"] is True


def test_manifest_hash_mismatch():
    manifest = full_manifest()
    manifest["module_count"] = 1

    result = verify_self_integrity_manifest(manifest)
    assert result["status"] == SelfIntegrityStatus.INVALID


def test_degraded_missing_modules():
    manifest = build_self_integrity_manifest({"verification_api": "v1"})

    result = verify_self_integrity_manifest(manifest)
    assert result["status"] == SelfIntegrityStatus.DEGRADED
    assert result["verified"] is False


def test_invalid_manifest_structure():
    result = verify_self_integrity_manifest([])
    assert result["status"] == SelfIntegrityStatus.INVALID
