from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_original_frontend_exists():
    p = ROOT / "app" / "dsng-troubleshooter.html"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "homeGrid" in text
    assert "renderHomeGrid" in text
    assert "DSNG Troubleshooting Assistant" in text


def test_backend_serves_expected_contract():
    p = ROOT / "backend" / "main.py"
    text = p.read_text(encoding="utf-8")
    assert 'return FileResponse(APP_FILE)' in text
    assert 'app.include_router(diagnostic.router)' in text
