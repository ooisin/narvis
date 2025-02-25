import datetime
import uuid

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


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
Links for many to many rels
"""

"""
TODO: In future could have a public user class returning non-sensitive data for admin queries
TODO: User update functions, forgot password, new email, name etc...
"""

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


''' Link Models for Many:Many '''
class ExperienceSiteLink(SQLModel, table=True):
    experience_id: Optional[uuid.UUID] = Field(default=None, foreign_key='experience.id', primary_key=True)
    site_id: Optional[uuid.UUID] = Field(default=None, foreign_key='site.id', primary_key=True)


class SiteNarrativeLink(SQLModel, table=True):
    site_id: Optional[uuid.UUID] = Field(default=None, foreign_key='site.id', primary_key=True)
    narrative_id: Optional[uuid.UUID] = Field(default=None, foreign_key='narrative.id', primary_key=True)


class ArtefactNarrativeLink(SQLModel, table=True):
    artefact_id: Optional[uuid.UUID] = Field(default=None, foreign_key='artefact.id', primary_key=True)
    narrative_id: Optional[uuid.UUID] = Field(default=None, foreign_key='narrative.id', primary_key=True)


class NarrativeTourLink(SQLModel, table=True):
    narrative_id: Optional[uuid.UUID] = Field(default=None, foreign_key='narrative.id', primary_key=True)
    tour_id: Optional[uuid.UUID] = Field(default=None, foreign_key='tour.id', primary_key=True)


class SiteTourLink(SQLModel, table=True):
    site_id: Optional[uuid.UUID] = Field(default=None, foreign_key='site.id', primary_key=True)
    tour_id: Optional[uuid.UUID] = Field(default=None, foreign_key='tour.id', primary_key=True)


class SiteHubLink(SQLModel, table=True):
    site_id: Optional[uuid.UUID] = Field(default=None, foreign_key='site.id', primary_key=True)
    hub_id: Optional[uuid.UUID] = Field(default=None, foreign_key='hub.id', primary_key=True)


class ClusterHubLink(SQLModel, table=True):
    cluster_id: Optional[uuid.UUID] = Field(default=None, foreign_key='cluster.id', primary_key=True)
    hub_id: Optional[uuid.UUID] = Field(default=None, foreign_key='hub.id', primary_key=True)


class ExperienceHubLink(SQLModel, table=True):
    experience_id: Optional[uuid.UUID] = Field(default=None, foreign_key='experience.id', primary_key=True)
    hub_id: Optional[uuid.UUID] = Field(default=None, foreign_key='hub.id', primary_key=True)


class ExperienceClusterLink(SQLModel, table=True):
    experience_id: Optional[uuid.UUID] = Field(default=None, foreign_key='experience.id', primary_key=True)
    cluster_id: Optional[uuid.UUID] = Field(default=None, foreign_key='cluster.id', primary_key=True)


class ExperienceTourLink(SQLModel, table=True):
    experience_id: Optional[uuid.UUID] = Field(default=None, foreign_key='experience.id', primary_key=True)
    tour_id: Optional[uuid.UUID] = Field(default=None, foreign_key='tour.id', primary_key=True)


class ExperienceNarrativeLink(SQLModel, table=True):
    experience_id: Optional[uuid.UUID] = Field(default=None, foreign_key='experience.id', primary_key=True)
    narrative_id: Optional[uuid.UUID] = Field(default=None, foreign_key='narrative.id', primary_key=True)


''' Experiences - will need to consider update class later '''
class ExperienceBase(SQLModel):
    experience_name: str = Field(max_length=255)
    experience_description: Optional[str] = Field(default=None, max_length=1000)
    location_type: Optional[str] = Field(default=None, max_length=255)
    investment: Optional[float] = Field(default=None)
    stage: Optional[str] = Field(default="concept", max_length=50)
    status: Optional[str] = Field(default="draft", max_length=50)
    stakeholders: Optional[str] = Field(default=None, max_length=1000)
    responsible: Optional[str] = Field(default=None, max_length=255)
    accountable: Optional[str] = Field(default=None, max_length=255)
    consulted: Optional[str] = Field(default=None, max_length=255)
    informed: Optional[str] = Field(default=None, max_length=255)
    experience_blueprint_id: Optional[str] = Field(default=None, max_length=50)


class Experience(ExperienceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: Optional[uuid.UUID] = Field(foreign_key="user.id") # TODO: composite PK with user id?

    ''' Relationships '''
    # 1:Many - Experience:ExperienceComponent
    experience_components: List["ExperienceComponent"] = Relationship(back_populates="experience")

    # 1:1 - Experience:ExperienceFeasibility
    experience_feasibility: Optional["Feasibility"] = Relationship(back_populates="experience", uselist=False)

    # Many:Many
    sites: List["Site"] = Relationship(back_populates="experiences", link_model=ExperienceSiteLink)
    hubs: List["Hub"] = Relationship(back_populates="experiences", link_model=ExperienceHubLink)
    clusters: List["Cluster"] = Relationship(back_populates="experiences", link_model=ExperienceClusterLink)
    narratives: List["Narrative"] = Relationship(back_populates="experiences", link_model=ExperienceNarrativeLink)
    tours: List["Tour"] = Relationship(back_populates="experiences", link_model=ExperienceTourLink)


class ExperiencePublic(ExperienceBase):
    id: uuid.UUID


class ExperiencesPublic(SQLModel):
    experiences: list[ExperiencePublic]
    count: int


class ExperienceCreate(ExperienceBase):
    experience_component_id: uuid.UUID
    hub_id: uuid.UUID
    cluster_id: uuid.UUID
    site_id: uuid.UUID
    narrative_ids: uuid.UUID
    feasibility_id: uuid.UUID


''' Experience Components - will need to consider update class later '''
class ExperienceComponentBase(SQLModel):
    experience_component_name: str = Field(max_length=255)
    experience_component_description: Optional[str] = Field(default=None, max_length=1000)
    experience_component_type: Optional[str] = Field(default=None, max_length=255)
    experience_component_status: Optional[str] = Field(default="draft", max_length=50)
    experience_component_provider: Optional[str] = Field(default=None, max_length=255)
    experience_component_card_id: Optional[str] = Field(default=None, max_length=50)
    experience_component_documentation: Optional[str] = Field(default=None, max_length=2000)


class ExperienceComponent(ExperienceComponentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: Optional[uuid.UUID] = Field(foreign_key="user.id")

    ''' Relationships '''
    # 1:Many - Experience:ExperienceComponent
    experience_id: Optional[uuid.UUID] = Field(default=None, foreign_key="experience.id")
    experience: Optional["Experience"] = Relationship(back_populates="experience_components")

class ExperienceComponentPublic(ExperienceComponentBase):
    id: uuid.UUID


class ExperienceComponentsPublic(SQLModel):
    experience_components: list[ExperienceComponentPublic]
    count: int


class ExperienceComponentCreate(ExperienceComponentBase):
    experience_id: uuid.UUID


'''
- Scaffold and logic follows from the user model
- TODO: relationships and fks
- TODO: Update a narrative
- Add owners appropriately - should only be for narratives? 
'''
class NarrativeBase(SQLModel):
    narrative_name: str = Field(max_length=255)
    narrative_description: str = Field(default=None, max_length=1000)
    theme: Optional[str] = Field(default=None, max_length=255)
    sub_theme: Optional[str] = Field(default=None, max_length=255)
    narrative_formats: Optional[str] = Field(default=None, max_length=500)
    narrative_main_characters: Optional[str] = Field(default=None, max_length=500)
    narrative_status: Optional[str] = Field(default="draft", max_length=50)
    narrative_card_id: Optional[str] = Field(default=None, max_length=50)


class Narrative(NarrativeBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    #owner_id: Optional[uuid.UUID] = Field(foreign_key="user.id")

    ''' Relationships '''
    # 1:Many - Narrative:Substory
    substories: List["Substory"] = Relationship(back_populates="narrative")

    # Many:Many
    experiences: List["Experience"] = Relationship(back_populates="narratives", link_model=ExperienceNarrativeLink)
    artefacts: List["Artefact"] = Relationship(back_populates="narratives", link_model=ArtefactNarrativeLink)
    tours: List["Tour"] = Relationship(back_populates="narratives", link_model=NarrativeTourLink)
    sites: List["Site"] = Relationship(back_populates="narratives", link_model=SiteNarrativeLink)

class NarrativePublic(NarrativeBase):
    id: uuid.UUID
    #owner_id: uuid.UUID


class NarrativesPublic(SQLModel):
    narratives: list[NarrativePublic]
    count: int


class NarrativeCreate(NarrativeBase):
    hub_id: uuid.UUID
    site_ids: uuid.UUID
    substory_ids: uuid.UUID
    artefact_ids: uuid.UUID


''' Substories - will need to consider update class later '''
class SubstoryBase(SQLModel):
    substory_name: str = Field(max_length=255)
    substory_description: Optional[str] = Field(default=None, max_length=1000)
    substory_locations: Optional[str] = Field(default=None, max_length=500)
    substory_format: Optional[str] = Field(default=None, max_length=255)
    substory_theme: Optional[str] = Field(default=None, max_length=255)
    substory_status: Optional[str] = Field(default="draft", max_length=50)
    substory_card_id: Optional[str] = Field(default=None, max_length=50)


class Substory(SubstoryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    #owner_id: Optional[uuid.UUID] = Field(foreign_key="user.id")

    ''' Relationships '''
    # 1:Many - Narrative:Substory
    narrative_id: Optional[uuid.UUID] = Field(default=None, foreign_key="narrative.id")
    narrative: Optional["Narrative"] = Relationship(back_populates="substories")


class SubstoryPublic(SubstoryBase):
    id: uuid.UUID


class SubstoriesPublic(SQLModel):
    substories: list[SubstoryPublic]
    count: int


class SubstoryCreate(SubstoryBase):
    experience_id: uuid.UUID
    narrative_id: uuid.UUID
    artefact_id: uuid.UUID
    site_id: uuid.UUID


''' Sites - will need to consider update class later '''
class SiteBase(SQLModel):
    site_name: str = Field(max_length=255)
    site_description: Optional[str] = Field(default=None, max_length=1000)
    site_category: Optional[str] = Field(default=None, max_length=255)
    site_location: Optional[str] = Field(default=None, max_length=255)
    site_size: Optional[float] = Field(default=None)
    site_boundary_north: Optional[float] = Field(default=None)
    site_boundary_east: Optional[float] = Field(default=None)
    site_boundary_south: Optional[float] = Field(default=None)
    site_boundary_west: Optional[float] = Field(default=None)
    site_documentation: Optional[str] = Field(default=None, max_length=2000)
    site_status: Optional[str] = Field(default="draft", max_length=50)


class Site(SiteBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    #owner_id: Optional[uuid.UUID] = Field(foreign_key="user.id")

    ''' Relationships '''
    # 1:Many - Site:Artefact
    artefacts: List["Artefact"] = Relationship(back_populates="sites")

    # Many:Many
    experiences: List["Experience"] = Relationship(back_populates="sites", link_model=ExperienceSiteLink)
    hubs: List["Hub"] = Relationship(back_populates="sites", link_model=SiteHubLink)
    tours: List["Tour"] = Relationship(back_populates="sites", link_model=SiteTourLink)
    narratives: List["Narrative"] = Relationship(back_populates="sites", link_model=SiteNarrativeLink)

class SitePublic(SiteBase):
    id: uuid.UUID


class SitesPublic(SQLModel):
    sites: list[SitePublic]
    count: int


class SiteCreate(SiteBase):
    hub_id: uuid.UUID
    cluster_id: uuid.UUID
    experience_component_id: uuid.UUID


''' Clusters - will need to consider update class later '''
class ClusterBase(SQLModel):
    cluster_name: str = Field(max_length=255)
    cluster_description: Optional[str] = Field(default=None, max_length=1000)
    cluster_location: Optional[str] = Field(default=None, max_length=255)
    cluster_size: Optional[float] = Field(default=None)
    cluster_boundary_north: Optional[float] = Field(default=None)
    cluster_boundary_east: Optional[float] = Field(default=None)
    cluster_boundary_south: Optional[float] = Field(default=None)
    cluster_boundary_west: Optional[float] = Field(default=None)
    cluster_documentation: Optional[str] = Field(default=None, max_length=2000)
    cluster_status: Optional[str] = Field(default="draft", max_length=50)


class Cluster(ClusterBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    #owner_id: Optional[uuid.UUID] = Field(foreign_key="user.id")

    ''' Relationships '''
    # Many:Many
    hubs: List["Hub"] = Relationship(back_populates="clusters", link_model=ClusterHubLink)
    experiences: List["Experience"] = Relationship(back_populates="clusters", link_model=ExperienceClusterLink)


class ClusterPublic(ClusterBase):
    id: uuid.UUID


class ClustersPublic(SQLModel):
    clusters: list[ClusterPublic]
    count: int


class ClusterCreate(ClusterBase):
    experience_id: uuid.UUID
    hub_id: uuid.UUID
    experience_component_id: uuid.UUID


''' Artefacts - will need to consider update class later '''
class ArtefactBase(SQLModel):
    artefact_name: str = Field(max_length=255)
    artefact_description: Optional[str] = Field(default=None, max_length=1000)
    artefact_format: Optional[str] = Field(default=None, max_length=255)
    artefact_location: Optional[str] = Field(default=None, max_length=255)
    artefact_status: Optional[str] = Field(default="draft", max_length=50)
    artefact_theme: Optional[str] = Field(default=None, max_length=255)
    artefact_card_id: Optional[str] = Field(default=None, max_length=50)


class Artefact(ArtefactBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    #owner_id: Optional[uuid.UUID] = Field(foreign_key="user.id")

    ''' Relationships '''
    # 1:Many - Site:Artefact
    site_id: Optional[uuid.UUID] = Field(default=None, foreign_key="site.id")
    sites: Optional["Site"] = Relationship(back_populates="artefacts")

    # Many:Many
    narratives: List["Narrative"] = Relationship(back_populates="artefacts", link_model=ArtefactNarrativeLink)

class ArtefactPublic(ArtefactBase):
    id: uuid.UUID


class ArtefactsPublic(SQLModel):
    artefacts: list[ArtefactPublic]
    count: int


class ArtefactCreate(ArtefactBase):
    experience_id: uuid.UUID
    narrative_id: uuid.UUID
    substory_id: uuid.UUID
    site_id: uuid.UUID


''' Hubs - will need to consider update class later '''
class HubBase(SQLModel):
    hub_name: str = Field(max_length=255)
    hub_description: Optional[str] = Field(default=None, max_length=1000)
    hub_location: Optional[str] = Field(default=None, max_length=255)
    hub_size: Optional[float] = Field(default=None)
    hub_boundary_north: Optional[float] = Field(default=None)
    hub_boundary_east: Optional[float] = Field(default=None)
    hub_boundary_south: Optional[float] = Field(default=None)
    hub_boundary_west: Optional[float] = Field(default=None)
    hub_tags: Optional[str] = Field(default=None, max_length=500)


class Hub(HubBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    #owner_id: Optional[uuid.UUID] = Field(foreign_key="user.id")

    ''' Relationships '''
    sites: List["Site"] = Relationship(back_populates="hubs", link_model=SiteHubLink)
    experiences: List["Site"] = Relationship(back_populates="hubs", link_model=ExperienceHubLink)
    clusters: List["Site"] = Relationship(back_populates="hubs", link_model=ClusterHubLink)


class HubPublic(HubBase):
    id: uuid.UUID


class HubsPublic(SQLModel):
    hubs: list[HubPublic]
    count: int


class HubCreate(HubBase):
    experience_id: uuid.UUID
    cluster_id: uuid.UUID


''' Tours - will need to consider update class later '''
class TourBase(SQLModel):
    tour_name: str = Field(max_length=255)
    tour_description: Optional[str] = Field(default=None, max_length=1000)
    tour_theme: Optional[str] = Field(default=None, max_length=255)
    tour_start_location: Optional[str] = Field(default=None, max_length=255)
    tour_end_location: Optional[str] = Field(default=None, max_length=255)
    tour_length: Optional[float] = Field(default=None)
    tour_time: Optional[float] = Field(default=None)
    tour_status: Optional[str] = Field(default="draft", max_length=50)


class Tour(TourBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    #owner_id: Optional[uuid.UUID] = Field(foreign_key="user.id")

    ''' Relationships '''
    # Many:Many
    experiences: List["Experience"] = Relationship(back_populates="tours", link_model=ExperienceTourLink)
    sites: List["Site"] = Relationship(back_populates="tours", link_model=SiteTourLink)
    narratives: List["Narrative"] = Relationship(back_populates="tours", link_model=NarrativeTourLink)


class TourPublic(TourBase):
    id: uuid.UUID


class ToursPublic(SQLModel):
    tours: list[TourPublic]
    count: int


class TourCreate(TourBase):
    experience_id: uuid.UUID
    narrative_id: uuid.UUID
    site_id: uuid.UUID


''' Experience Feasibility - will need to consider update class later '''
class FeasibilityBase(SQLModel):
    feasibility_study_name: str = Field(max_length=255)
    feasibility_study_description: Optional[str] = Field(default=None, max_length=1000)
    feasibility_study_state: Optional[str] = Field(default="draft", max_length=50)
    feasibility_irr: Optional[float] = Field(default=None)
    feasibility_roi: Optional[float] = Field(default=None)
    feasibility_documentation: Optional[str] = Field(default=None, max_length=2000)
    feasible: Optional[bool] = Field(default=None)


class Feasibility(FeasibilityBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    ''' Relationships '''
    # 1:1 - Experience:ExperienceFeasibility
    experience_id: Optional[uuid.UUID] = Field(default=None, foreign_key="experience_id")
    experience: Optional["Experience"] = Relationship(back_populates="experience_feasibility")


class FeasibilityPublic(FeasibilityBase):
    id: uuid.UUID


class FeasibilitiesPublic(SQLModel):
    feasibilities: list[FeasibilityPublic]
    count: int


class FeasibilityCreate(FeasibilityBase):
    experience_id: uuid.UUID