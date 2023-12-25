from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    slug: str
    email: str
    password: str
    is_superuser: bool
    is_staff: bool
    is_active: bool
    is_verified: bool
    date_joined: datetime
    last_login: datetime | None


class EmailVerification(BaseModel):
    id: int
    code: str
    user_id: int
    created_at: datetime
    expiration: datetime
