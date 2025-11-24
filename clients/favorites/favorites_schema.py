from typing import Optional

from pydantic import BaseModel, ConfigDict

class FavoritesSchema(BaseModel):
    """
    Описание структуры избранного места.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: int
    title: str
    lat: float
    lon: float
    color: str | None
    created_at: str

class CreateFavoritesRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание избранного места.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str
    lat: str
    lon: str
    color: Optional[str] = None

class CreateFavoritesResponseSchema(BaseModel):
    """
    Описание структуры ответа создания пользователя.
    """
    favorites: FavoritesSchema