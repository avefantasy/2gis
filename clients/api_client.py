from typing import Any

from httpx import Client, URL, Response
from httpx._types import RequestData, HeaderTypes


class APIClient:
    def __init__(self, client: Client):
        self.client = client

    def post(
            self,
            url: URL | str,
            json: Any | None = None,
            data: RequestData | None = None,
            headers: HeaderTypes | None = None
    ) -> Response:
        """
        Выполняет POST-запрос.

        :param url: URL-адрес эндпоинта.
        :param json: Данные в формате JSON.
        :param data: Форматированные данные формы (application/x-www-form-urlencoded).
        :param headers: Произвольные заголовки запроса.
        :return: Объект Response с данными ответа.
        """
        return self.client.post(url, json=json, data=data, headers=headers)