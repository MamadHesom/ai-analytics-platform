"""Security dependencies for the HTTP layer."""

from fastapi import Header, HTTPException, status

from app.core.config import Settings


def require_api_key(settings: Settings, x_api_key: str | None = Header(default=None)) -> None:
    """Validate an API key when one is configured.

    Local development deliberately permits unauthenticated requests when ``API_KEY``
    is empty. Deployments should always configure a key or replace this dependency
    with an identity-aware authentication provider.
    """

    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A valid X-API-Key header is required",
            headers={"WWW-Authenticate": "ApiKey"},
        )
