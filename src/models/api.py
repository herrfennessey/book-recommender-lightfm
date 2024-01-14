from typing import List

from pydantic import BaseModel


class ProfileRecommendationsRequest(BaseModel):
    user_id: int
    genres: List[str] = []
    limit: int = 10
