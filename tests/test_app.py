from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Expect known activities exist
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    test_email = "pytest-user@example.com"

    # Ensure the test email is not present
    resp = client.get("/activities")
    assert resp.status_code == 200
    activities = resp.json()
    participants_before = list(activities[activity]["participants"])
    assert test_email not in participants_before

    # Sign up the test user
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Confirm participant was added
    resp = client.get("/activities")
    activities = resp.json()
    assert test_email in activities[activity]["participants"]

    # Unregister the test user
    resp = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")

    # Confirm participant was removed
    resp = client.get("/activities")
    activities = resp.json()
    assert test_email not in activities[activity]["participants"]
