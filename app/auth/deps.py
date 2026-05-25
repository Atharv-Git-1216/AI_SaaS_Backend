from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.session import get_db
from app.models.base import User
from app.auth.jwt import decode_token

# Instructs FastAPI & Swagger to expect a standard Authorization: Bearer <token> header
# and renders a simple text input box in the UI.
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Validates the JWT token, extracts the user ID, and fetches the user from Supabase.
    This protects all endpoints that inject Depends(get_current_user).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token expired.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Extract the raw string token from the injected credentials object
    token = credentials.credentials
    
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise credentials_exception
        
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Execute async database query
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
        
    return user

async def require_super_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Strict security dependency that verifies the current user holds the Super Admin role.
    Any endpoint injecting this dependency is completely invisible/inaccessible to normal users.
    """
    if current_user.role_id != 5:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Absolute Super Admin privileges required to access this subsystem."
        )
    return current_user