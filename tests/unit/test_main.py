import pytest
from backend.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


client = TestClient(app)



@patch("backend.main.requests.get")
@patch("backend.main.engine")


def test_convert_success(mock_engine, mock_requests):
# 🔌 Mock API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "base": "USD",
        "rates": {"EUR": 91.0},
        "date": "2024-01-01"
    }
    mock_response.raise_for_status.return_value = None
    mock_requests.return_value = mock_response

    # 💾 Mock DB connection and insert
    mock_conn = MagicMock()
    mock_engine.begin.return_value.__enter__.return_value = mock_conn

    # 🔍 Call the endpoint
    response = client.get("/convert?from_currency=USD&to_currency=EUR&amount=1")

    # ✅ Assert
    assert response.status_code == 200
    data = response.json()
    assert data["from"] == "USD"
    assert data["to"] == "EUR"
    assert data["amount"] == 1
    assert data["converted"] == 91.0
    assert data["rate"] == 91.0



@patch("backend.main.engine")
def test_db_check_success(mock_engine):
    mock_conn = MagicMock()
    mock_result = MagicMock()
    mock_result.mappings().fetchone.return_value = {"count": 10}
    mock_conn.execute.return_value = mock_result
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    response = client.get("/db-check")
    assert response.status_code == 200
    assert "status" in response.json()

@patch("backend.main.engine")
def test_history_success(mock_engine):
    mock_conn = MagicMock()
    mock_result = MagicMock()
    mock_result.mappings().all.return_value = [
        {"id": 1, "from_currency": "EUR", "to_currency": "USD", "amount": 100, "rate": 1.1, "converted": 110, "date": "2025-07-23"}
    ]
    mock_conn.execute.return_value = mock_result
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_convert():
    pass