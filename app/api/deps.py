"""
API dependencies
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_credentials_exception, verify_token
from app.crud.user import user_crud
from app.db.database import get_async_session
from app.models.user import User

# Security scheme
security = HTTPBearer()


async def get_db() -> AsyncSession:
    """Get database session dependency"""
    async for session in get_async_session():
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise create_credentials_exception()

    username = payload.get("sub")
    if username is None:
        raise create_credentials_exception()

    user = await user_crud.get_by_username(db, username)
    if user is None:
        raise create_credentials_exception()

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current active superuser"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user
