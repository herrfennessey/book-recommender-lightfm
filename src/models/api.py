from typing import List

from pydantic import BaseModel


class UserToItemRecommendationsRequest(BaseModel):
    user_id: int
    genres: List[str] = []
    limit: int = 10


class ItemToItemRecommendationsRequest(BaseModel):
    work_id: int
    limit: int = 10
