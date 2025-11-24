from httpx import Client


def get_public_http_client(token: str) -> Client:
    """
    Функция создаёт экземпляр httpx.Client с базовыми настройками.

    :return: Готовый к использованию объект httpx.Client.
    """
    client = Client(
        timeout=10,
        base_url="https://regions-test.2gis.com/",
        cookies={"token": token}
    )
    return client