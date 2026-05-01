import json

from fastapi import Request
from fastapi.responses import JSONResponse

from app.cache.keys import MAINTENANCE_KEY


ALLOWED_DURING_MAINTENANCE = {
    "/",
    "/status",
    "/docs",
    "/redoc",
    "/openapi.json",
}


async def maintenance_middleware(request: Request, call_next):
    path = request.url.path

    if path in ALLOWED_DURING_MAINTENANCE or path.startswith("/ops"):
        return await call_next(request)

    r = getattr(request.app.state, "redis", None)

    if r is None:
        return await call_next(request)

    raw = await r.get(MAINTENANCE_KEY)

    if raw is None:
        return await call_next(request)

    data = json.loads(raw)

    if data.get("enabled") is True:
        return JSONResponse(
            status_code=503,
            content={
                "detail": "Service is under maintenance.",
                "maintenance": True,
                "message": data.get(
                    "message",
                    "Currently under maintenance. Please check back soon.",
                ),
            },
            headers={
                "Retry-After": "300",
            },
        )

    return await call_next(request)