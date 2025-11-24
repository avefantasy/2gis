from clients.favorites.favorites_schema import FavoritesSchema, CreateFavoritesRequestSchema
from tools.assertions.base import assert_equal, assert_is_true
from datetime import datetime


def assert_favorite_basic(favorite: FavoritesSchema):
    """
    Базовая проверка структуры ответа.
    """
    assert_is_true(isinstance(favorite.id, int), "id")
    assert_is_true(isinstance(favorite.title, str), "title")
    assert_is_true(isinstance(favorite.lat, float), "lat")
    assert_is_true(isinstance(favorite.lon, float), "lon")
    assert_is_true(favorite.color is None or isinstance(favorite.color, str), "color")

    try:
        datetime.fromisoformat(favorite.created_at)
    except ValueError:
        raise AssertionError(f"Invalid created_at format: {favorite.created_at}")


def assert_favorite_match(favorite: FavoritesSchema, request: CreateFavoritesRequestSchema):
    """
    Проверка соответствия полей запроса и ответа.
    """
    assert_favorite_basic(favorite)
    assert_equal(favorite.title, request.title, "title")
    assert_equal(float(favorite.lat), float(request.lat), "lat")
    assert_equal(float(favorite.lon), float(request.lon), "lon")
    assert_equal(favorite.color, request.color, "color")

