from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db
from backend.agent.memory import init_chromadb
from backend.routers import chat, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    init_chromadb()
    yield


app = FastAPI(title="SkyAssist AI", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(analytics.router)


@app.get("/")
async def root():
    return {"service": "SkyAssist AI", "status": "running", "version": "2.0.0"}
