from fastapi import Security, HTTPException,status
from fastapi.security import APIKeyHeader

from app.core.settings import settings

_api_key_header = APIKeyHeader(name='X-API-Key', auto_error=False)

def require_api_key(api_key: str | None = Security(_api_key_header))-> None:
    if not settings.API_KEY or api_key != settings.API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid API Key')