import pytest
import httpx
from clients.favorites.favorites_client import FavoritesClient
from clients.favorites.favorites_schema import CreateFavoritesRequestSchema
from clients.http_builder import get_public_http_client


@pytest.fixture
def http_client_with_token():
    """
    Получает новый токен перед каждым тестом
    и создаёт httpx.Client с токеном в cookie.
    """
    token_resp = httpx.post("https://regions-test.2gis.com/v1/auth/tokens")
    assert token_resp.status_code == 200, "Не удалось получить токен"
    token = token_resp.cookies.get("token")
    assert token, "Сервер не вернул cookie 'token'"
    client = get_public_http_client(token)
    return client

@pytest.fixture
def favorites_client(http_client_with_token):
    """Фикстура клиента для /v1/favorites"""
    return FavoritesClient(client=http_client_with_token)

@pytest.fixture
def make_request():
    """
    Фикстура для создания корректного запроса с возможностью
    переопределять любые поля.
    """
    def _make_request(**overrides):
        base = {
            "title": "Test",
            "lat": "55.755825",
            "lon": "37.617298",
            "color": "BLUE"
        }
        base.update(overrides)
        return CreateFavoritesRequestSchema(**base)

    return _make_request

