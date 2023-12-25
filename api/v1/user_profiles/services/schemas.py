from pydantic import BaseModel


class UserProfile(BaseModel):
    id: int
    image: str | None
    about: str | None
    body_weight: int | float
