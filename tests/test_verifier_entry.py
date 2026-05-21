from offline_verifier import create_demo_offline_package
from verifier_entry import verify_from_entry_point


def test_browser_verifier_entry():
    package = create_demo_offline_package("HC-BROWSER-1")

    result = verify_from_entry_point(package)

    assert result["portable"] is True
    assert result["platform"] == "BROWSER"
    assert result["verification"]["validation"]["decision"] == "VERIFIED"
