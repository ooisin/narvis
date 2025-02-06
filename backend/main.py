from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from pydantic_core.core_schema import nullable_schema
from sqlmodel import SQLModel, Session, create_engine, Field, Integer, String, select, Relationship
import shutil

app = FastAPI()


#TODO: Use if __name__ = __main__ to handle on startup
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/narvistest"
engine = create_engine(DATABASE_URL, echo=True)
SQLModel.metadata.create_all(engine)


#TODO: Make separate models.py
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


def get_session():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


#TODO: Make separate services.py
@app.get("/components", response_model=list[NarrativeComponent])
def read_components(session: Session = Depends(get_session)):
    statement = select(NarrativeComponent)
    return session.exec(statement).all()


@app.get("/components/{component_id}", response_model=NarrativeComponent)
def read_component(component_id: int, session: Session = Depends(get_session)):
    statement = select(NarrativeComponent).where(NarrativeComponent.id == component_id)
    return session.exec(statement).first()


@app.post("/components", response_model=NarrativeComponent)
def create_component(component: NarrativeComponent, session: Session = Depends(get_session)):
    try:
        session.add(component)
        session.commit()
        session.refresh(component)
        return component
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to insert component: {str(e)}")


@app.put("/components/{component_id}", response_model=NarrativeComponent)
def update_component(component_id: int, updated_component: NarrativeComponent, session: Session = Depends(get_session)):
    try:
        statement = select(NarrativeComponent).where(NarrativeComponent.id == component_id)
        component = session.exec(statement).first()
        if component is None:
            raise HTTPException(status_code=404, detail=f"Component with id {component_id} not found")
        for k, v in updated_component.model_dump(exclude_unset=True).items():
            setattr(component, k, v)
        session.add(component)
        session.commit()
        session.refresh(component)
        return component
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update component: {str(e)}")


@app.delete("/components/{component_id}")
def delete_component(component_id: int, session: Session = Depends(get_session)):
    try:
        session.delete(component_id)
        session.commit()
        session.refresh(component_id)
        return {"ok - component deleted successfully": True}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete component: {str(e)}")


@app.get("/narratives", response_model=list[Narrative])
def read_narratives(session: Session = Depends(get_session)):
    statement = select(Narrative)
    return session.exec(statement).all()


@app.get("/narratives/{narrative_id}", response_model=Narrative)
def read_narrative(narrative_id: int, session: Session = Depends(get_session)):
    statement = select(Narrative).where(Narrative.id == narrative_id)
    return session.exec(statement).first()


@app.post("/narratives", response_model=Narrative)
def create_narrative(narrative: Narrative, session: Session = Depends(get_session)):
    try:
        session.add(narrative)
        session.commit()
        session.refresh(narrative)
        return narrative
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to insert narrative: {str(e)}")


@app.put("/narratives/{narrative_id}", response_model=Narrative)
def update_narrative(narrative_id: int, updated_narrative: Narrative, session: Session = Depends(get_session)):
    try:
        statement = select(Narrative).where(Narrative.id == narrative_id)
        narrative = session.exec(statement).first()
        if narrative is None:
            raise HTTPException(status_code=404, detail=f"Narrative with id {narrative_id} not found")
        for k, v in updated_narrative.model_dump(exclude_unset=True).items():
            setattr(narrative, k, v)
        session.add(narrative)
        session.commit()
        session.refresh(narrative)
        return narrative
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update narrative: {str(e)}")


@app.delete("/narratives/{narrative_id}")
def delete_narrative(narrative_id: int, session: Session = Depends(get_session)):
    try:
        session.delete(narrative_id)
        session.commit()
        session.refresh(narrative_id)
        return {"ok - component deleted successfully": True}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete narrative: {str(e)}")


# Rudimentary file upload method for initial development using Swagger UI docs
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"backend/test_uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}