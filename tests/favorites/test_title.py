from http import HTTPStatus
import pytest
import allure
from clients.favorites.favorites_schema import FavoritesSchema
from tools.assertions.base import assert_status_code
from tools.assertions.favorites import assert_favorite_match

@pytest.mark.regression
@pytest.mark.title
@allure.epic("Favorites API")
@allure.feature("Проверка параметра Название (title)")
class TestTitle:

    @pytest.mark.positive
    @pytest.mark.parametrize("title", ["Test", "Тест", "12345", "Test,Test!", "Тест123Test!"])
    @allure.story("Разрешенные символы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание избранного места с допустимыми символами в названии")
    def test_title_valid_symbols(self, favorites_client, title, make_request):
        request = make_request(title=title)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        favorite = FavoritesSchema.model_validate_json(response.text)
        assert_favorite_match(favorite, request)

    @pytest.mark.negative
    @pytest.mark.parametrize("title", ["👌", "@#$%^&*", " ", ""])
    @allure.story("Запрещенные символы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Попытка создать избранное место с недопустимыми символами в названии")
    def test_title_invalid_symbols(self, favorites_client, title, make_request):
        request = make_request(title=title)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

    @pytest.mark.positive
    @pytest.mark.parametrize("title", ["A", "AА", "A" * 500, "A" * 998, "A" * 999])
    @allure.story("Валидная длина")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание избранного места с допустимой длиной названия")
    def test_title_valid_length(self, favorites_client, title, make_request):
        request = make_request(title=title)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        favorite = FavoritesSchema.model_validate_json(response.text)
        assert_favorite_match(favorite, request)

    @pytest.mark.negative
    @pytest.mark.parametrize("title", ["A" * 1000, "A" * 1500])
    @allure.story("Невалидная длина")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Попытка создать избранное место с слишком длинным названием")
    def test_title_invalid_length(self, favorites_client, title, make_request):
        request = make_request(title=title)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)


    @pytest.mark.positive
    @allure.story("Обязательный параметр присутствует")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание избранного места с обязательным параметром title")
    def test_title_required_present(self, favorites_client, make_request):
        request = make_request(title="Test")
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        favorite = FavoritesSchema.model_validate_json(response.text)
        assert_favorite_match(favorite, request)

    @pytest.mark.negative
    @allure.story("Обязательный параметр отсутствует")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Попытка создать избранное место без параметра title")
    def test_title_required_missing(self, favorites_client):
        payload = {"lat": "55.755825", "lon": "37.617298", "color": "BLUE"}
        response = favorites_client.post("/v1/favorites", data=payload)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)


