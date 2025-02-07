import os
from fastapi import Depends, Request, HTTPException
from fastapi.security import APIKeyHeader

# EntraIDトークンスキーマ
api_key_scheme = APIKeyHeader(
    name="X-Api-Key",
)


# EntraIDトークン認証
def authenticate(request: Request, api_key: str = Depends(api_key_scheme)):
    if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        return

    # Verify api key
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Unautorized")
