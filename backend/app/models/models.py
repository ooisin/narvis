import uuid

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


class NarrativeComponentLink(SQLModel, table=True):
    narrative_id: int | None = Field(foreign_key="narrative.id", default=None, primary_key=True)
    component_id: int | None = Field(foreign_key="narrativecomponent.id", default=None, primary_key=True)


class Narrative(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None, index=True)
    name: str
    description: str

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
