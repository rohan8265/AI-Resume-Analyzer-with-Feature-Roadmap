import json
from pathlib import Path

REPORT = Path("/app/report.json")


def load_report():
    """Load and return the parsed JSON report."""
    assert REPORT.exists(), "/app/report.json was not created"
    return json.loads(REPORT.read_text())


def test_report_file_created():
    """Success Criterion 1: Read every valid request from /app/access.log."""
    report = load_report()
    assert isinstance(report, dict), "Report must be a JSON object"


def test_total_requests():
    """Success Criterion 2: Count the total number of requests."""
    report = load_report()
    assert report["total_requests"] == 6


def test_unique_ips():
    """Success Criterion 3: Count the number of unique client IP addresses."""
    report = load_report()
    assert report["unique_ips"] == 3


def test_top_path():
    """Success Criterion 4: Determine the most frequently requested path."""
    report = load_report()
    assert report["top_path"] == "/index.html"


def test_exact_field_names():
    """Success Criterion 5: Write the JSON report to /app/report.json using the exact field names shown above."""
    report = load_report()
    for field in ("total_requests", "unique_ips", "top_path"):
        assert field in report, f"Missing required field: {field}"
