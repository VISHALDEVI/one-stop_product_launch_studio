import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.database import create_tables
from backend.routes.api import router

load_dotenv()

app = FastAPI(
    title="AI Product Launch Studio",
    description="Multi-agent AI system for marketplace-ready product package generation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def root():
    return {"message": "AI Product Launch Studio API is running", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("FASTAPI_HOST", "0.0.0.0")
    port = int(os.getenv("FASTAPI_PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=True)
