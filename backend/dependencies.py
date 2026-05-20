"""FastAPI dependencies for request processing."""

import os

from fastapi import Request

from exceptions import UnauthorizedError
from models import User
from services.auth_service import AuthService
from store import JSONStore

# Initialize user store and auth service
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
user_store = JSONStore(os.path.join(DATA_DIR, "users.json"))
auth_service = AuthService(user_store)


async def get_current_user(request: Request) -> User:
    """Extract and validate JWT from httpOnly cookie, return User.

    Extracts the JWT token from the 'token' httpOnly cookie,
    verifies the token signature and expiry, loads the user from
    the store, and returns the User object.

    Args:
        request: The incoming FastAPI request.

    Returns:
        The authenticated User object.

    Raises:
        UnauthorizedError: If no token cookie is present, token is invalid,
            or the user referenced by the token does not exist.
    """
    token = request.cookies.get("token")
    if not token:
        raise UnauthorizedError("Authentication required")

    # verify_token raises UnauthorizedError if token is invalid/expired
    user_id = auth_service.verify_token(token)

    # Load user from store
    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise UnauthorizedError("Authentication failed")

    return user
