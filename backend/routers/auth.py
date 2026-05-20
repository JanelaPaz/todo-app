"""Authentication router handling register, login, logout, and session endpoints."""

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, Field

from dependencies import auth_service, get_current_user
from models import User, UserCreate, UserResponse


class LoginRequest(BaseModel):
    """Request model for user login."""

    identifier: str = Field(min_length=1, description="Email or username")
    password: str = Field(min_length=1, description="User password")

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Cookie configuration
COOKIE_NAME = "token"
COOKIE_MAX_AGE = 24 * 60 * 60  # 24 hours in seconds


def _set_auth_cookie(response: Response, token: str) -> None:
    """Set the JWT token as an httpOnly cookie on the response.

    Args:
        response: The FastAPI response object.
        token: The JWT token string to set.
    """
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=COOKIE_MAX_AGE,
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
        path="/",
    )


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate, response: Response) -> UserResponse:
    """Register a new user.

    Validates input via Pydantic model, calls auth service to create user,
    sets httpOnly cookie with JWT, and returns user response.

    Args:
        user_data: The registration request body.
        response: The FastAPI response object for setting cookies.

    Returns:
        The created user's public information.
    """
    user = auth_service.register(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        password_confirm=user_data.password_confirm,
    )

    # Create JWT and set as httpOnly cookie
    token = auth_service.create_token(user.id)
    _set_auth_cookie(response, token)

    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        created_at=user.created_at,
    )


@router.post("/login", response_model=UserResponse)
async def login(login_data: LoginRequest, response: Response) -> UserResponse:
    """Log in an existing user.

    Validates input via Pydantic model, calls auth service to authenticate,
    sets httpOnly cookie with JWT, and returns user response.

    Args:
        login_data: The login request body with identifier and password.
        response: The FastAPI response object for setting cookies.

    Returns:
        The authenticated user's public information.
    """
    user = auth_service.login(identifier=login_data.identifier, password=login_data.password)

    # Create JWT and set as httpOnly cookie
    token = auth_service.create_token(user.id)
    _set_auth_cookie(response, token)

    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        created_at=user.created_at,
    )


@router.post("/logout")
async def logout(response: Response) -> dict:
    """Log out the current user.

    Clears the JWT httpOnly cookie regardless of whether a valid
    token is present. Always returns 200.

    Args:
        response: The FastAPI response object for clearing cookies.

    Returns:
        A success message.
    """
    response.delete_cookie(
        key=COOKIE_NAME,
        httponly=True,
        samesite="lax",
        secure=False,
        path="/",
    )
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Get the current authenticated user's information.

    Returns the user's id, email, username, and created_at.

    Args:
        current_user: The authenticated user (injected by dependency).

    Returns:
        The current user's public information.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        created_at=current_user.created_at,
    )
