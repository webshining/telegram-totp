from pydantic import Field, BaseModel

from .base import Base


class UserTotpKey(BaseModel):
    name: str
    secret: str
    digits: int = Field(default=6)
    period: int = Field(default=30)


class User(Base):
    id: int
    name: str
    username: str | None = Field(default=None)
    lang: str = Field(default="en")
    keys: list[UserTotpKey] = Field(default=[])


User.set_collection("user")
