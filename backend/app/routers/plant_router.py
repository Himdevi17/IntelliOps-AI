from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.plant import PlantCreate, PlantResponse
from app.services.plant_service import create_plant, get_all_plants


router = APIRouter(
    prefix="/plants",
    tags=["Plants"]
)


@router.post("/", response_model=PlantResponse)
def create_new_plant(
    plant: PlantCreate,
    db: Session = Depends(get_db)
):
    return create_plant(db, plant)


@router.get("/", response_model=list[PlantResponse])
def get_plants(
    db: Session = Depends(get_db)
):
    return get_all_plants(db)