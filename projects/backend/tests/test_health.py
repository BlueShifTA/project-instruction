import fastapi.testclient as ftc

import package.main as pm


def test_health() -> None:
    client = ftc.TestClient(pm.app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready() -> None:
    client = ftc.TestClient(pm.app)
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
