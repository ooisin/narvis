import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, func

from backend.app.api.deps import SessionDep, get_current_active_superuser, CurrentUser

from backend.app.models.models import Tour, TourCreate, TourPublic, ToursPublic

router = APIRouter(prefix="/tours", tags=["tours"])


@router.get("/{id}", response_model=TourPublic)
def get_tour(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> Any:
    tour = session.get(Tour, id)
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    if not current_user.is_superuser and (tour.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to access this tour")
    return tour


@router.get("/", response_model=ToursPublic)
def get_tours(session: SessionDep, current_user: CurrentUser, limit: int = 100) -> Any:
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Tour)
        count = session.exec(count_statement).one()
        statement = select(Tour).limit(limit)
        tours = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Tour)
            .where(Tour.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Tour)
            .where(Tour.owner_id == current_user.id)
            .limit(limit)
        )
        tours = session.exec(statement).all()

    return ToursPublic(data=tours, count=count)


@router.post("/", response_model=TourPublic)
def create_tour(session: SessionDep, tour_in: TourCreate, current_user: CurrentUser) -> Any:
    tour = Tour.model_validate(tour_in, update={"owner_id": current_user.id})
    session.add(tour)
    session.commit()
    session.refresh(tour)
    return tour


@router.delete("/{id}")
def delete_tour(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> str:
    tour = session.get(Tour, id)
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    if not current_user.is_superuser and (tour.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to delete this tour")
    session.delete(tour)