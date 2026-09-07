from fastapi import FastAPI
from app.core.database import create_tables
from app.routers.user_router import router as user_router
from app.routers.plant_router import router as plant_router

create_tables()

app = FastAPI(
    title="IntelliOps AI",
    description="Explainable AI Agent Platform for Enterprise Operations",
    version="1.0.0"
)
app.include_router(user_router)
app.include_router(plant_router)

@app.get("/")
def root():
    return {
        "message": "IntelliOps AI API is running"
    }