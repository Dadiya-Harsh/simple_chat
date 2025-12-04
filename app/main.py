from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    debug=(settings.debug_level.upper() == "DEBUG"),
    version="1.0.0",
    description="A simple chat application.",  
)

@app.get("/health_check")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "message": "The application is running smoothly."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = settings.deployment_port)