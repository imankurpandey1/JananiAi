from backend.app import create_app
from backend.config.settings import Settings


def test_health_and_request_validation(tmp_path, monkeypatch):
    monkeypatch.setattr(Settings, "DB_PATH", tmp_path / "stories.db")
    app = create_app()
    client = app.test_client()

    health = client.get("/health")
    assert health.status_code == 200
    assert health.get_json()["status"] == "healthy"

    invalid_filter = client.get("/get-stories?min_rating=bad")
    assert invalid_filter.status_code == 400

    invalid_id = client.post("/rate-story", json={"id": "invalid", "rating": 4})
    assert invalid_id.status_code == 400

    invalid_story = client.post(
        "/save-story",
        json={
            "title": "Test Story",
            "prompt": "A traveler crossed an empty sea.",
            "genre": "Fantasy",
            "generated_story": "The traveler found an island.",
            "model_used": "GPT-2",
            "word_count": "not-a-number",
            "reading_time": 1,
            "generation_time": 1,
        },
    )
    assert invalid_story.status_code == 400


def test_cors_allows_only_configured_frontend(tmp_path, monkeypatch):
    monkeypatch.setattr(Settings, "DB_PATH", tmp_path / "stories.db")
    app = create_app()
    client = app.test_client()

    response = client.get("/health", headers={"Origin": Settings.FRONTEND_ORIGIN})
    assert response.headers["Access-Control-Allow-Origin"] == Settings.FRONTEND_ORIGIN

    blocked = client.get("/health", headers={"Origin": "https://untrusted.example"})
    assert "Access-Control-Allow-Origin" not in blocked.headers
