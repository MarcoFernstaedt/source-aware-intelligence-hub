from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.app.models import Workspace
from backend.app.service import build_workspace

app = FastAPI(
    title="Source-Aware Intelligence Hub",
    description="Credential-free synthetic decision-support demo",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)


@app.middleware("http")
async def security_headers(request: Request, call_next):  # type: ignore[no-untyped-def]
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
        "connect-src 'self'; font-src 'self'; object-src 'none'; base-uri 'none'; "
        "frame-ancestors 'none'; form-action 'none'"
    )
    return response


@app.exception_handler(ValueError)
async def invalid_scenario_handler(_request: Request, _error: ValueError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": "invalid scenario"})


@app.exception_handler(RequestValidationError)
async def validation_handler(_request: Request, _error: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": "invalid scenario or bounded input"})


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "synthetic-demo"}


@app.get("/api/workspace")
def workspace(
    scenario: Literal["baseline", "degraded", "conflict"] = Query(
        default="baseline", max_length=16
    ),
) -> Workspace:
    return build_workspace(scenario)


_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if _DIST.is_dir():
    assets = _DIST / "assets"
    if assets.is_dir():
        app.mount("/assets", StaticFiles(directory=assets), name="assets")

    @app.get("/", include_in_schema=False)
    @app.get("/demo/source/{source_id}", include_in_schema=False)
    def frontend(source_id: str | None = None) -> FileResponse:
        del source_id
        return FileResponse(_DIST / "index.html")
