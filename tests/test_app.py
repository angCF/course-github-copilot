from fastapi.testclient import TestClient
from urllib.parse import quote

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    test_email = "testuser+pytest_clean@example.com"

    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": test_email})
    assert resp.status_code == 200
    data = resp.json()
    assert "Signed up" in data.get("message", "")

    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert test_email in data[activity]["participants"]

    resp = client.delete(f"/activities/{quote(activity)}/unregister", params={"email": test_email})
    assert resp.status_code == 200
    data = resp.json()
    assert "Unregistered" in data.get("message", "")

    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert test_email not in data[activity]["participants"]
