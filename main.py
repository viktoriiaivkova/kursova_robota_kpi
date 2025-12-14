import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.database import create_tables
from src.routers import users, accounts
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing Cache and DB")

    create_tables()
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

    yield
    print("Shutting down.")
app = FastAPI(
    title="API",
    description="Ivkova Viktoriia KP-33 Lab 2",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Дозволити всі джерела
    allow_credentials=True,
    allow_methods=["*"],  # Дозволити всі методи (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Дозволити всі заголовки
)
app.include_router(users.router)
app.include_router(accounts.router)
@app.get("/")
def read_root():
    return {"message": "API is running. Go to /docs"}