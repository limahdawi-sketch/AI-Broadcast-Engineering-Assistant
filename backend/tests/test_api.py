import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import Base, get_db
import main as main_module


@pytest.fixture()
def client(tmp_path):
    """Fresh in-memory-ish SQLite DB per test run, isolated from any real data/app.db."""
    db_file = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    from models import knowledge, equipment  # noqa: F401
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    main_module.app.dependency_overrides[get_db] = override_get_db
    with TestClient(main_module.app) as c:
        yield c
    main_module.app.dependency_overrides.clear()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_list_categories(client):
    r = client.get("/api/diagnostic/categories")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 6
    assert any(c["id"] == "no_signal" for c in data)


def test_get_node(client):
    r = client.get("/api/diagnostic/node/ns1")
    assert r.status_code == 200
    assert r.json()["is_result"] is False
    assert len(r.json()["options"]) == 2


def test_get_unknown_node_404(client):
    r = client.get("/api/diagnostic/node/nope")
    assert r.status_code == 404


def test_integrity_endpoint(client):
    r = client.get("/api/diagnostic/_integrity")
    assert r.status_code == 200
    assert r.json()["healthy"] is True


def test_knowledge_crud_flow(client):
    # create
    r = client.post("/api/knowledge", json={
        "title": "Intermittent lock loss after ~10 minutes",
        "category": "no_signal",
        "causes": "Suspected thermal drift in the LNB LO after warm-up.",
        "fix": "Replaced LNB; issue did not recur over a 48h soak test.",
        "author": "Test Engineer",
    })
    assert r.status_code == 201
    entry = r.json()
    assert entry["validation_state"] == "pending"
    entry_id = entry["id"]

    # appears in list
    r = client.get("/api/knowledge")
    assert any(e["id"] == entry_id for e in r.json())

    # review -> approved
    r = client.post(f"/api/knowledge/{entry_id}/review", json={"decision": "approved"})
    assert r.status_code == 200
    assert r.json()["validation_state"] == "approved"

    # delete
    r = client.delete(f"/api/knowledge/{entry_id}")
    assert r.status_code == 204
    r = client.get(f"/api/knowledge/{entry_id}")
    assert r.status_code == 404


def test_knowledge_rejects_blank_title(client):
    r = client.post("/api/knowledge", json={
        "title": "   ",
        "causes": "x",
        "fix": "y",
    })
    assert r.status_code == 422


def test_equipment_profile_crud(client):
    r = client.post("/api/equipment", json={
        "category": "antenna",
        "manufacturer": "ExampleCo",
        "model": "1.2m Ku-band",
        "function": "DSNG uplink antenna",
    })
    assert r.status_code == 201
    profile_id = r.json()["id"]

    r = client.get("/api/equipment", params={"category": "antenna"})
    assert any(p["id"] == profile_id for p in r.json())
