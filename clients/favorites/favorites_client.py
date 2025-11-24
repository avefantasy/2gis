from httpx import Response

from clients.api_client import APIClient
from clients.favorites.favorites_schema import CreateFavoritesRequestSchema, FavoritesSchema



class FavoritesClient(APIClient):
    """
    Клиент для работы с /v1/favorites.
    """

    def create_favorite_api(self, request: CreateFavoritesRequestSchema) -> Response:
        """
        Метод делает запрос на создание избранного места.

        :param request: Объект CreateFavoritesRequestSchema.
        :return: httpx.Response
        """
        return self.post(
            "/v1/favorites",
            data=request.model_dump(exclude_none=True),
        )

    def create_favorite(self, request: CreateFavoritesRequestSchema) -> FavoritesSchema:
        """
        Метод создаёт избранное место и валидирует ответ через Pydantic.

        :param request: Объект CreateFavoritesRequestSchema.
        :return: FavoritesSchema
        """
        response = self.create_favorite_api(request)
        return FavoritesSchema.model_validate_json(response.text)