from http import HTTPStatus
import pytest
import allure
from tools.assertions.base import assert_status_code
from clients.favorites.favorites_schema import FavoritesSchema

@pytest.mark.regression
@pytest.mark.lon
@allure.epic("Favorites API")
@allure.feature("Проверка параметра Долгота (lon)")
class TestLon:

    @pytest.mark.positive
    @pytest.mark.parametrize("lon", ["155.028254", "-155.028254"])
    @allure.story("Разрешенные символы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание избранного места с допустимой долготой")
    def test_lon_valid_values(self, favorites_client, lon, make_request):
        request = make_request(lon=lon)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        favorite = FavoritesSchema.model_validate_json(response.text)
        assert float(favorite.lon) == float(lon)

    @pytest.mark.negative
    @pytest.mark.parametrize("lon", ["abc", "155,028254", "155..220000", "55. 028000", "55 028000"])
    @allure.story("Недопустимые символы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Попытка создать избранное место с недопустимыми символами долготы")
    def test_lon_invalid_values(self, favorites_client, lon, make_request):
        request = make_request(lon=lon)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

    @pytest.mark.positive
    @pytest.mark.parametrize("lon", ["-180.000000", "-179.900000", "179.900000", "180.000000", "0.000000"])
    @allure.story("Валидный диапазон")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Проверка валидного диапазона долготы")
    def test_lon_valid_range(self, favorites_client, lon, make_request):
        request = make_request(lon=lon)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        favorite = FavoritesSchema.model_validate_json(response.text)
        assert float(favorite.lon) == float(lon)

    @pytest.mark.negative
    @pytest.mark.parametrize("lon", ["-180.100000", "-240.000000", "180.100000", "240.100000"])
    @allure.story("Невалидный диапазон")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Проверка недопустимого диапазона долготы")
    def test_lon_invalid_range(self, favorites_client, lon, make_request):
        request = make_request(lon=lon)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

    @pytest.mark.negative
    @allure.story("Создание избранного места без долготы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_lon_required_missing(self, favorites_client):
        payload = {
            "title": "Test",
            "lat": "55.755825",
            "color": "BLUE",
        }
        response = favorites_client.post("/v1/favorites", data=payload)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)