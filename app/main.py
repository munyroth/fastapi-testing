from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables
from app.errors import register_all_errors
from app.routers import routes_auth, routes_users


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await create_db_and_tables()
    yield

version = "v1"
version_prefix =f"/api/{version}"
app = FastAPI(
    title="konektAgri API",
    description="RESTful API for KonektAgri platform - managing agricultural connections and data",
    version=version,

    lifespan=lifespan
)

# Adjust origins for production!
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://your-production-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_all_errors(app)

# Include routers
app.include_router(routes_auth.router, prefix=f"{version_prefix}/auth", tags=["Authentication"])
app.include_router(routes_users.router, prefix=f"{version_prefix}/users", tags=["Users"])
