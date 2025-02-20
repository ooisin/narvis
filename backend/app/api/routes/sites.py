import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, func

from backend.app.api.deps import SessionDep, get_current_active_superuser, CurrentUser

from backend.app.models.models import Site, SiteBase, SitePublic, SitesPublic, SiteCreate

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get("/{id}", response_model=SitePublic)
def get_site(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> Any:
    site = session.get(Site, id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not current_user.is_superuser and (site.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to access this site")
    return site

@router.get("/", response_model=SitesPublic)
def get_sites(session: SessionDep, current_user: CurrentUser, limit: int = 100) -> Any:
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Site)
        count = session.exec(count_statement).one()
        statement = select(Site).limit(limit)
        sites = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Site)
            .where(Site.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Site)
            .where(Site.owner_id == current_user.id)
            .limit(limit)
        )
        sites = session.exec(statement).all()

    return SitesPublic(data=sites, count=count)


@router.post("/", response_model=SitePublic)
def create_site(session: SessionDep, site_in: SiteCreate, current_user: CurrentUser) -> Any:
    site = Site.model_validate(site_in, update={"owner_id": current_user.id})
    session.add(site)
    session.commit()
    session.refresh(site)
    return site


@router.delete("/{id}")
def delete_site(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> str:
    site = session.get(Site, id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not current_user.is_superuser and (site.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to delete this site")
    session.delete(site)
    session.commit()
    return f"Site: {id} deleted successfully"