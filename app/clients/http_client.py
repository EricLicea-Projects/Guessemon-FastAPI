import httpx
from fastapi import HTTPException
from typing import Any

async def fetch_json(
    client: httpx.AsyncClient,
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    service_name: str = "Upstream",
    not_found_detail: str = "Not Found",
) -> Any:
    try:
        resp = await client.get(url, params=params, headers=headers)

        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail=not_found_detail)

        resp.raise_for_status()

        if resp.status_code == 204 or not resp.content:
            return None

        return resp.json()

    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"{service_name} network error") from e
    except httpx.HTTPStatusError as e:
        code = e.response.status_code
        raise HTTPException(status_code=502, detail=f"{service_name} error {code}") from e
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"{service_name} returned invalid JSON") from e
