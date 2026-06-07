from html import unescape

from fastapi.testclient import TestClient

from app import app
from career_data import DOMAINS, QUESTIONS


client = TestClient(app)


def test_pages_render():
    for path in ["/", "/choose", "/domains", "/assessment"]:
        response = client.get(path)
        assert response.status_code == 200


def test_catalog_has_25_domains_and_questions():
    assert len(DOMAINS) == 25
    assert len(QUESTIONS) == 25
    assert len({domain["slug"] for domain in DOMAINS}) == 25


def test_assessment_returns_ranked_recommendations():
    response = client.post("/api/assessment", json={"answers": [4] * 25})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["recommendations"]) == 5
    assert len(payload["top_traits"]) == 5
    scores = [item["score"] for item in payload["recommendations"]]
    assert scores == sorted(scores, reverse=True)


def test_assessment_rejects_invalid_answers():
    response = client.post("/api/assessment", json={"answers": [6] * 25})
    assert response.status_code == 422


def test_every_roadmap_renders():
    for domain in DOMAINS:
        response = client.get(f"/roadmap/{domain['slug']}")
        assert response.status_code == 200
        assert domain["name"] in unescape(response.text)
