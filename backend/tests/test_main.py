
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

@pytest.mark.parametrize("query, source, mock_answer", [
    ("what are the sales", "CSV", "CSV answer"),
    ("what is the policy", "RAG", "RAG answer"),
    ("what are the top products", "SQL", [{"label": "Product A", "value": 100}]),
    ("some random query", "Unknown", None),
])
def test_ask(monkeypatch, query, source, mock_answer):
    # Mock the router and handlers
    def mock_route_query(query):
        return source

    def mock_answer_from_csv(query):
        return mock_answer

    def mock_answer_from_rag(query):
        return mock_answer

    def mock_answer_from_sql(query):
        return mock_answer

    monkeypatch.setattr("main.route_query", mock_route_query)
    monkeypatch.setattr("main.answer_from_csv", mock_answer_from_csv)
    monkeypatch.setattr("main.answer_from_rag", mock_answer_from_rag)
    monkeypatch.setattr("main.answer_from_sql", mock_answer_from_sql)

    response = client.post("/api/ask", json={"query": query})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["source"] == source
    if source != "Unknown":
        assert json_response["answer"] == mock_answer
    else:
        assert json_response["query"] == query

