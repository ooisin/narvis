import uuid
from typing import Optional

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
    id: uuid.UUID = Field(default_factory=uuid.uuid4(), primary_key=True)
    hashed_password: str
    narratives: list["Narrative"] = Relationship(back_populates="user", cascade_delete=True)


"""
TODO: In future could have a public user class returning non-sensitive data for admin queries
TODO: User update functions, forgot password, new email, name etc...
"""


class NarrativeComponentLink(SQLModel, table=True):
    narrative_id: int | None = Field(foreign_key="narrative.id", default=None, primary_key=True)
    component_id: int | None = Field(foreign_key="narrativecomponent.id", default=None, primary_key=True)

# Revise for a NarrativeBase class to avoid any duplicate code when the model is more complicated
class Narrative(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None, index=True)
    name: str
    description: str
    owner_id: uuid.UUID = Field(foreign_key="user.id",)
    owner: Optional[User] = Relationship(back_populates="narratives")

    components: list["NarrativeComponent"] = Relationship(back_populates="narratives", link_model=NarrativeComponentLink)


class NarrativeComponent(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None, index=True)
    name: str
    description: str
    location: str
    interaction_type: str

    narratives: list[Narrative] = Relationship(back_populates="components", link_model=NarrativeComponentLink)


class UserBase(SQLModel):
    pass
