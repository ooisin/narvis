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

#Creates generic Artefacts Class with listed attributes
class ArtefactsBase(SQLModel):
    artefact_id: str = Field(min_length = 1, max_length = 255)
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    distribution: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    status: str | None = Field(default=None, max_length=255)
    theme: str | None = Field(default=None, max_length=255)
    card_id: str | None = Field(default=None, max_length=255)


#Creates generic Clusters Class with listed attributes
class ClustersBase(SQLModel):
    cluster_id: str = Field(min_length = 1, max_length = 255)
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    size: int | None = Field(deafult=0, max_length=255)
    boundary_north: str | None = Field(default=None, max_length=255)
    boundary_east: str | None = Field(default=None, max_length=255)
    boundary_south: str | None = Field(default=None, max_length=255)
    boundary_west: str | None = Field(default=None, max_length=255)
    documentation: str | None = Field(default=None, max_length=255)
    status: str | None = Field(default=None, max_length=255)

#Creates generic Experience Components Class with listed attributes
class ExperienceComponentsBase(SQLModel):
    xp_components_id: str = Field(min_length = 1, max_length = 255)
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    component_type: str | None = Field(default=None, max_length=255)
    status: str | None = Field(default=None, max_length=255)
    provider: str | None = Field(default=None, max_length=255)
    card_id: str | None = Field(default=None, max_length=255)
    documentation: str | None = Field(default=None, max_length=255)

#Creates generic Experience Feasibility Class with listed attributes
class ExperienceFeasibilityBase(SQLModel):
    feasibility_id: str = Field(min_length = 1, max_length = 255)
    study: str | None = Field(default=None, max_length=255)
    study_name: str | None = Field(default=None, max_length=255)
    study_description: str | None = Field(default=None, max_length=255)
    study_state: str | None = Field(default=None, max_length=255)
    irr: str | None = Field(default=None, max_length=255)
    roi: str | None = Field(default=None, max_length=255)
    documentation: str | None = Field(default=None, max_length=255)
    feasible: bool | None = Field(default=False)

#Creates generic Experiences Class with listed attributes
class ExperiencesBase(SQLModel):
    xp_id: str = Field(min_length = 1, max_length = 255)
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    xp_type: str | None = Field(default=None, max_length=255)
    investment: str | None = Field(default=None, max_length=255)
    stage: str | None = Field(default=None, max_length=255)
    status: str | None = Field(default=None, max_length=255)
    stakeholders: str | None = Field(default=None, max_length=255)
    responsible: str | None = Field(default=None, max_length=255)
    accountable: str | None = Field(default=None, max_length=255)
    consulted: str | None = Field(default=None, max_length=255)
    informed: str | None = Field(default=None, max_length=255)
    blueprint_id: str | None = Field(default=None, max_length=255)

#Creates generic Hubs Class with listed attributes
class HubsBase(SQLModel):
    hub_id: str = Field(min_length = 1, max_length = 255)
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    size: int | None = Field(deafult=0, max_length=255)
    boundary_north: str | None = Field(default=None, max_length=255)
    boundary_east: str | None = Field(default=None, max_length=255)
    boundary_south: str | None = Field(default=None, max_length=255)
    boundary_west: str | None = Field(default=None, max_length=255)
    tags: str | None = Field(default=None, max_length=255)

#Creates generic Narratives Class with listed attributes
class NarrativesBase(SQLModel):
    narrative_id: str = Field(min_length = 1, max_length = 255)
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    theme: str | None = Field(default=None, max_length=255)
    subtheme: str | None = Field(default=None, max_length=255)
    distribution: str | None = Field(default=None, max_length=255)
    main_characters: str | None = Field(default=None, max_length=255)
    status: str | None = Field(default=None, max_length=255)
    card_id: str | None = Field(default=None, max_length=255)

#Creates generic Sites Class with listed attributes
class SitesBase(SQLModel):
    site_id: str = Field(min_length = 1, max_length = 255)
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    category: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    size: int | None = Field(deafult=0, max_length=255)
    boundary_north: str | None = Field(default=None, max_length=255)
    boundary_east: str | None = Field(default=None, max_length=255)
    boundary_south: str | None = Field(default=None, max_length=255)
    boundary_west: str | None = Field(default=None, max_length=255)
    documentation: str | None = Field(default=None, max_length=255)
    status: str | None = Field(default=None, max_length=255)

#Creates generic Substories Class with listed attributes
class SubstoriesBase(SQLModel):
    substory_id: str = Field(min_length = 1, max_length = 255)
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    locations: str | None = Field(default=None, max_length=255)
    distribution:str | None = Field(default=None, max_length=255)
    theme: str | None = Field(default=None, max_length=255)
    status: str | None = Field(default=None, max_length=255)
    card_id: str | None = Field(default=None, max_length=255)

#Creates generic Tours Class with listed attributes
class ToursBase(SQLModel):
    tour_id: str = Field(min_length = 1, max_length = 255)
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    theme: str | None = Field(default=None, max_length=255)
    start_location: str | None = Field(default=None, max_length=255)
    end_location: str | None = Field(default=None, max_length=255)
    length: int | None = Field(deafult=0, max_length=255)
    time: int | None = Field(deafult=0, max_length=255)
    status: str | None = Field(default=None, max_length=255)



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