from html import unescape

from fastapi.testclient import TestClient

from app import app
from career_data import DOMAINS, QUESTIONS, QUESTION_SETS


client = TestClient(app)


def test_pages_render():
    for path in ["/", "/choose", "/domains", "/assessment"]:
        response = client.get(path)
        assert response.status_code == 200


def test_frontend_assets_render_from_stable_urls():
    for filename in ["app.css", "common.js", "domains.js", "assessment.js", "results.js"]:
        response = client.get(f"/assets/{filename}")
        assert response.status_code == 200


def test_catalog_has_25_domains_and_questions():
    assert len(DOMAINS) == 25
    assert len(QUESTIONS) == 25
    assert len(QUESTION_SETS) == 5
    assert all(len(questions) == 25 for questions in QUESTION_SETS.values())
    assert len({domain["slug"] for domain in DOMAINS}) == 25


def test_questions_endpoint_returns_a_set_id():
    response = client.get("/api/questions")
    assert response.status_code == 200
    payload = response.json()
    assert payload["question_set_id"] in QUESTION_SETS
    assert len(payload["questions"]) == 25


def test_questions_endpoint_can_exclude_previous_set():
    response = client.get("/api/questions?exclude_set_id=set-1")
    assert response.status_code == 200
    payload = response.json()
    assert payload["question_set_id"] in QUESTION_SETS
    assert payload["question_set_id"] != "set-1"


def test_assessment_returns_ranked_recommendations():
    response = client.post(
        "/api/assessment",
        json={"answers": [4] * 25, "question_set_id": "set-1"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["recommendations"]) == 5
    assert len(payload["top_traits"]) == 5
    scores = [item["score"] for item in payload["recommendations"]]
    assert scores == sorted(scores, reverse=True)


def test_assessment_rejects_invalid_answers():
    response = client.post(
        "/api/assessment",
        json={"answers": [6] * 25, "question_set_id": "set-1"},
    )
    assert response.status_code == 422


def test_assessment_rejects_unknown_question_set():
    response = client.post(
        "/api/assessment",
        json={"answers": [4] * 25, "question_set_id": "missing"},
    )
    assert response.status_code == 422


def test_every_roadmap_renders():
    for domain in DOMAINS:
        response = client.get(f"/roadmap/{domain['slug']}")
        assert response.status_code == 200
        html = unescape(response.text)
        assert domain["name"] in html
        assert "Certifications to consider" in html
        assert "Companies to research" in html


def test_roadmap_json_sections_are_populated():
    for domain in DOMAINS:
        assert domain["certifications"], f"{domain['name']} has no certifications"
        assert domain["companies"], f"{domain['name']} has no hiring companies"
        assert domain["exams"], f"{domain['name']} has no exams"
        assert domain["projects"], f"{domain['name']} has no project ideas"


def test_roadmap_json_field_aliases_are_available():
    domain = DOMAINS[0]
    assert domain["domain"] == domain["name"]
    assert domain["overview"] == domain["summary"]
    assert domain["essentialQualities"] == domain["qualities"]
    assert domain["skillsRequired"] == domain["skills"]
    assert domain["careerOpportunities"] == domain["careers"]
    assert domain["expectedCompanies"] == domain["companies"]
    assert domain["bestExams"] == domain["exams"]
    assert domain["projectIdeas"] == domain["projects"]
    assert domain["expectedEntryLevelSalaryIndia"] == domain["salary"]
