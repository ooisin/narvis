from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from pydantic_core.core_schema import nullable_schema
from sqlmodel import SQLModel, Session, create_engine, Field, Integer, String, select, Relationship
import shutil

app = FastAPI()


DATABASE_URL = "postgresql://postgres:1234@localhost:5432/narvistest"
engine = create_engine(DATABASE_URL, echo=True)


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


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.post("/addcomponent", response_model=NarrativeComponent)
def create_component(component: NarrativeComponent, session: Session = Depends(get_session)):
    try:
        session.add(component)
        session.commit()
        session.refresh(component)
        return component
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to insert component: {str(e)}")


@app.post("/addnarrative", response_model=Narrative)
def create_narrative(narrative: Narrative, session: Session = Depends(get_session)):
    try:
        session.add(narrative)
        session.commit()
        session.refresh(narrative)
        return narrative
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to insert narrative: {str(e)}")


@app.get("/getcomponent", response_model=list[NarrativeComponent])
def read_components(session: Session = Depends(get_session)):
    statement = select(NarrativeComponent)
    return session.exec(statement).all()

@app.get("/getnarrative", response_model=list[Narrative])
def read_narratives(session: Session = Depends(get_session)):
    statement = select(Narrative)
    return session.exec(statement).all()


@app.delete("/deletecomponent/{component_id}")
def delete_component(component_id: int, session: Session = Depends(get_session)):
    try:
        session.delete(component_id)
        session.commit()
        session.refresh(component_id)
        return {"ok - deleted successfully": True}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete component: {str(e)}")


# Rudimentary file upload method for initial development using Swagger UI docs
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"backend/test_uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}


def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()
