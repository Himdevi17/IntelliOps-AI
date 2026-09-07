from pydantic import BaseModel, ConfigDict


class PlantCreate(BaseModel):
    name: str
    code: str
    location: str


class PlantResponse(BaseModel):
    id: int
    name: str
    code: str
    location: str

    model_config = ConfigDict(from_attributes=True)