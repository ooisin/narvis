from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from enum import Enum
import pandas as pd
import os
import shutil

app = FastAPI()


class NarrativeCategory(Enum):
    STORIES = 0
    SITES = 1
    EXPERIENCES = 2


class NarrativeComponent(BaseModel):
    id: int
    name: str
    description: str
    location: str
    interaction_type: str
    category: NarrativeCategory


# Dummy data for initial development prior to excel pipeline
components = {
    1: NarrativeComponent(
        id=1,
        name="Prophet's Mosque",
        description="Historic mosque where Prophet Muhammad is buried",
        location="Madinah City Center",
        interaction_type="Historical Exploration",
        category=NarrativeCategory.SITES
    ),
    2: NarrativeComponent(
        id=2,
        name="Battle of Uhud Narrative",
        description="Immersive storytelling about the historic battle",
        location="Uhud Mountain",
        interaction_type="Guided Storytelling",
        category=NarrativeCategory.STORIES
    ),
    3: NarrativeComponent(
        id=3,
        name="Dates Market Experience",
        description="Interactive tour of Madinah's famous date markets",
        location="Al-Madina Souq",
        interaction_type="Culinary Journey",
        category=NarrativeCategory.EXPERIENCES
    ),
    4: NarrativeComponent(
        id=4,
        name="Quba Mosque Journey",
        description="First mosque built by Prophet Muhammad",
        location="Quba District",
        interaction_type="Architectural Discovery",
        category=NarrativeCategory.SITES
    ),
    5: NarrativeComponent(
        id=5,
        name="Hijra Migration Story",
        description="Narrative of Prophet Muhammad's migration to Madinah",
        location="Historical Route",
        interaction_type="Narrative Walk",
        category=NarrativeCategory.STORIES
    ),
    6: NarrativeComponent(
        id=6,
        name="Traditional Craft Workshop",
        description="Hands-on experience with local artisan crafts",
        location="Old City Crafts Center",
        interaction_type="Interactive Workshop",
        category=NarrativeCategory.EXPERIENCES
    ),
    7: NarrativeComponent(
        id=7,
        name="Al-Masjid an-Nabawi Complex",
        description="Comprehensive exploration of the Prophet's Mosque complex",
        location="City Center",
        interaction_type="Architectural Tour",
        category=NarrativeCategory.SITES
    ),
    8: NarrativeComponent(
        id=8,
        name="Bedouin Lifestyle Narrative",
        description="Stories of traditional desert life in Madinah region",
        location="Desert Outskirts",
        interaction_type="Cultural Storytelling",
        category=NarrativeCategory.STORIES
    ),
    9: NarrativeComponent(
        id=9,
        name="Culinary Heritage Tour",
        description="Taste and learn about Madinah's traditional cuisine",
        location="Local Food District",
        interaction_type="Gastronomic Experience",
        category=NarrativeCategory.EXPERIENCES
    ),
    10: NarrativeComponent(
        id=10,
        name="Medina's Green Dome Story",
        description="Historical significance of the Green Dome",
        location="Prophet's Mosque",
        interaction_type="Historical Narrative",
        category=NarrativeCategory.STORIES
    )
}


@app.get("/welcome")
async def welcome():
    return {"message": "Welcome to NARVIS"}

@app.get("/login")
async def login():
    return {"message": "Login Page"}

# Rudimentary file upload method for initial development using Swagger UI docs
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"backend/test_uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}


@app.get("/components")
async def get_component():
    return components


@app.get("/components/{component_id}")
async def get_component_by_id(component_id: int):
    return components[component_id]