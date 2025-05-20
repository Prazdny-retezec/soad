import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from settings import AppSettings

security = HTTPBasic()
settings = AppSettings()


def require_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    user = settings.auth_user
    pw = settings.auth_password

    if not (secrets.compare_digest(credentials.username, user) and secrets.compare_digest(credentials.password, pw)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
