import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from backend.app.api.deps import SessionDep, CurrentUser
from backend.app.models.models import Cluster, ClustersPublic, ClusterCreate, ClusterPublic

router = APIRouter(prefix="/clusters", tags=["clusters"])


@router.get("/", response_model=ClustersPublic)
def get_clusters(session: SessionDep, current_user: CurrentUser, limit: int = 100) -> Any:
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Cluster)
        count = session.exec(count_statement).one()
        statement = select(Cluster).limit(limit)
        clusters = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Cluster)
            .where(Cluster.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Cluster)
            .where(Cluster.owner_id == current_user.id)
            .limit(limit)
        )
        clusters = session.exec(statement).all()

    return ClustersPublic(data=clusters, count=count)


@router.get("/{id}", response_model=ClusterPublic)
def get_cluster(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    cluster = session.get(Cluster, id)
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    if not current_user.is_superuser and (cluster.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to access this cluster")


@router.post("/", response_model=ClusterPublic)
def create_cluster(session: SessionDep, cluster_in: ClusterCreate, current_user: CurrentUser) -> Any:
    cluster = Cluster.model_validate(cluster_in, update={"owner_id": current_user.id})
    session.add(cluster)
    session.commit()
    session.refresh(cluster)
    return cluster


@router.delete("/{id}")
def delete_cluster(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> str:
    cluster = session.get(Cluster, id)
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    if not current_user.is_superuser and (cluster.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="No permission to delete this cluster")
    session.delete(cluster)
    session.commit()
    return f"Cluster: {id} deleted successfully"