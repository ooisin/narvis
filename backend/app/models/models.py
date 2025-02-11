import uuid

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


# The generic parent User class - prevents dupes, other models will inherit from this
class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    name: str | None = Field(default=None, max_length=255)


# For public facing endpoints - Don't want people to be able to set is_superuser=True etc...
class UserRegister(SQLModel):
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    name: str | None = Field(default=None, max_length=255)
    password: str = Field(min_length=8, max_length=30)


# For admin brute force create user - NOT for public endpoints!
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=30)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    users: list[UserPublic]
    count: int

"""
TODO: In future could have a public user class returning non-sensitive data for admin queries
TODO: User update functions, forgot password, new email, name etc...
"""


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None



class NarrativeBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Revise for a NarrativeBase class to avoid any duplicate code when the model is more complicated
class Narrative(NarrativeBase, table=True):
    id: uuid.UUID | None = Field(primary_key=True, default_factory=uuid.uuid4, index=True)
    name: str
    description: str
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")

    owner: User | None = Relationship(back_populates="items")


class NarrativePublic(NarrativeBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class NarrativesPublic(SQLModel):
    data: list[NarrativePublic]
    count: int


class NarrativeCreate(NarrativeBase):
    pass

class NarrativeComponent(SQLModel):
    pass