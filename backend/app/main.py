from fastapi import FastAPI

app = FastAPI(
    title="IntelliOps AI",
    description="Explainable AI Agent Platform for Enterprise Operations",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "IntelliOps AI API is running"
    }