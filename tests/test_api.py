from http import HTTPStatus

import pytest
from app.api import app
from fastapi.testclient import TestClient

@pytest.fixture
def httpClient():
    return TestClient(app)

def test_should_return_status_200_when_an_user_verify_system_health(httpClient):
    response = httpClient.get("/healthcheck")
    assert response.status_code == HTTPStatus.OK

def test_app_should_return_the_healthcheck_response_in_json_format(httpClient):
    response = httpClient.get("/healthcheck")
    assert response.headers["Content-Type"] == "application/json"

def test_when_checking_integrity_should_contain_information(httpClient):
    response = httpClient.get("healthcheck")
    assert response.json() == {"status": "ok"}