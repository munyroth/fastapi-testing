from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.database import create_db_and_tables
from app.errors import register_all_errors
from app.routers import routes_auth, routes_users


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await create_db_and_tables()
    yield


version = "v1"
version_prefix = f"/api/{version}"
app = FastAPI(
    title="konektAgri API",
    description="RESTful API for KonektAgri platform - managing agricultural connections and data",
    version=version,

    lifespan=lifespan
)

API_KEY = "testttt"
API_KEY_NAME = "X-API-KEY"

EXCLUDE_PATHS = ["/docs", "/openapi.json", "/health"]


@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    if request.url.path in EXCLUDE_PATHS:
        return await call_next(request)

    api_key = request.headers.get(API_KEY_NAME)
    if api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={
                "message": "Invalid API Key",
                "error_code": "invalid_api_key"
            }
        )

    return await call_next(request)


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
