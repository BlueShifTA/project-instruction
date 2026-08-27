import fastapi.testclient as ftc

import package.main as pm


def test_echo_endpoint() -> None:
    client = ftc.TestClient(pm.app)
    response = client.post("/api/example/echo", json={"message": "hello"})
    assert response.status_code == 200
    assert response.json() == {"message": "hello", "length": 5}
