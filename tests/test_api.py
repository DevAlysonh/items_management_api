from http import HTTPStatus

import pytest
from uuid import UUID
from app.api import app, get_items_from_order
from app.schema import Item
from fastapi.testclient import TestClient
from app.exception import OrderNotFoundException

@pytest.fixture
def httpClient():
    return TestClient(app)

@pytest.fixture
def override_get_items_from_order():
    def _override_get_items_from_order(items_or_error):
        def duble(order_code: UUID) -> list[Item]:
            if isinstance(items_or_error, Exception):
                raise items_or_error
            return items_or_error
        app.dependency_overrides[get_items_from_order] = duble
    yield _override_get_items_from_order
    app.dependency_overrides.clear()

class TestHealthCheck:
    def test_should_return_status_200_when_an_user_verify_system_health(self, httpClient):
        response = httpClient.get("/healthcheck")
        assert response.status_code == HTTPStatus.OK

    def test_app_should_return_the_healthcheck_response_in_json_format(self, httpClient):
        response = httpClient.get("/healthcheck")
        assert response.headers["Content-Type"] == "application/json"

    def test_when_checking_integrity_should_contain_information(self, httpClient):
        response = httpClient.get("healthcheck")
        assert response.json() == {"status": "ok"}

class TestGetOrders:
    def test_get_items_when_receiving_invalid_order_id_should_return_an_error(self, httpClient, override_get_items_from_order):
        response = httpClient.get("/orders/invalid-value/items")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_get_items_when_order_id_not_found_should_return_an_error(self, httpClient, override_get_items_from_order):
        override_get_items_from_order(OrderNotFoundException())
        response = httpClient.get("/orders/7e290683-d67b-4f96-a940-44bef1f69d21/items")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_get_items_when_order_found_should_return_ok_status(self, httpClient, override_get_items_from_order):
        override_get_items_from_order([])
        response = httpClient.get("/orders/7e290683-d67b-4f96-a940-44bef1f69d21/items")
        assert response.status_code == HTTPStatus.OK

    def test_get_items_when_order_found_should_return_items(self, httpClient, override_get_items_from_order):
        items = [
            Item(sku='1', description='Item 1', image_url='http://url.com/img1', reference='ref1', quantity=1).model_dump(),
            Item(sku='2', description='Item 2', image_url='http://url.com/img2', reference='ref2', quantity=2).model_dump(),
        ]
        override_get_items_from_order(items)
        resposta = httpClient.get("/orders/7e290683-d67b-4f96-a940-44bef1f69d21/items")
        assert resposta.json() == items