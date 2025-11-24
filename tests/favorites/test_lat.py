from http import HTTPStatus
import pytest
import allure
from clients.favorites.favorites_schema import FavoritesSchema
from tools.assertions.base import assert_status_code

@pytest.mark.regression
@pytest.mark.lat
@allure.epic("Favorites API")
@allure.feature("Проверка параметра Широта (lat)")
class TestLat:

    @pytest.mark.positive
    @pytest.mark.parametrize("lat", ["55.028254", "-55.028254"])
    @allure.story("Разрешенные символы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание избранного с допустимой широтой")
    def test_lat_valid_values(self, favorites_client, lat, make_request):
        request = make_request(lat=lat)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        favorite = FavoritesSchema.model_validate_json(response.text)
        assert float(favorite.lat) == float(lat)

    @pytest.mark.negative
    @pytest.mark.parametrize("lat", ["abc", "55,028254", "55..220000", "55. 028000", "55 028028000"])
    @allure.story("Недопустимые символы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Попытка создать избранное с недопустимыми символами широты")
    def test_lat_invalid_values(self, favorites_client, lat, make_request):
        request = make_request(lat=lat)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

    @pytest.mark.positive
    @pytest.mark.parametrize("lat", ["-90.000000", "-89.900000", "89.900000", "90.000000", "0.000000"])
    @allure.story("Валидный диапазон")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Проверка валидного диапазона широты")
    def test_lat_valid_range(self, favorites_client, lat, make_request):
        request = make_request(lat=lat)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        favorite = FavoritesSchema.model_validate_json(response.text)
        assert float(favorite.lat) == float(lat)

    @pytest.mark.negative
    @pytest.mark.parametrize("lat", ["-90.100000", "-180.000000", "90.100000", "180.100000"])
    @allure.story("Невалидный диапазон")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Проверка недопустимого диапазона широты")
    def test_lat_invalid_range(self, favorites_client, lat, make_request):
        request = make_request(lat=lat)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

    @pytest.mark.negative
    @allure.story("Обязательный параметр отсутствует")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание избранного места без широты")
    def test_lat_required_missing(self, favorites_client):
        payload = {
            "title": "Test",
            "lon": "37.62",
            "color": "BLUE",
        }
        response = favorites_client.post("/v1/favorites", data=payload)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)