from sqlalchemy.orm import Session

from app.models.plant import Plant
from app.schemas.plant import PlantCreate


def create_plant(db: Session, plant: PlantCreate):
    db_plant = Plant(
        name=plant.name,
        code=plant.code,
        location=plant.location
    )

    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)

    return db_plant


def get_all_plants(db: Session):
    return db.query(Plant).all()