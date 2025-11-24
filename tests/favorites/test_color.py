from http import HTTPStatus
import pytest
import allure
from clients.favorites.favorites_schema import FavoritesSchema, CreateFavoritesRequestSchema
from tools.assertions.base import assert_status_code
from tools.assertions.favorites import assert_favorite_match

@pytest.mark.regression
@pytest.mark.color
@allure.epic("Favorites API")
@allure.feature("Проверка поля Цвет (color)")
class TestColor:

    @pytest.mark.positive
    @pytest.mark.parametrize("color", ["BLUE", "GREEN", "RED", "YELLOW"])
    @allure.story("Валидные значения")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание избранного с допустимым цветом")
    def test_color_valid(self, favorites_client, color, make_request):
        request = make_request(color=color)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        favorite = FavoritesSchema.model_validate_json(response.text)
        assert_favorite_match(favorite, request)

    @pytest.mark.negative
    @pytest.mark.parametrize("color", ["black", "blue", "123", " ", "👌"])
    @allure.story("Невалидные значения")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Попытка создать избранное с недопустимым цветом")
    def test_color_invalid(self, favorites_client, color, make_request):
        request = make_request(color=color)
        response = favorites_client.create_favorite_api(request)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

    @pytest.mark.positive
    @allure.story("Параметр не передан")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание избранного места без указания цвета")
    def test_color_not_passed(self, favorites_client):
        payload = {"title": "Test", "lat": "55.755825", "lon": "37.617298"}
        response = favorites_client.post("/v1/favorites", data=payload)
        assert_status_code(response.status_code, HTTPStatus.OK)
        request = CreateFavoritesRequestSchema(**payload)
        favorite = FavoritesSchema.model_validate_json(response.text)
        assert favorite.color is None
        assert_favorite_match(favorite, request)
