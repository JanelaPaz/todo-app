"""Authentication service handling registration, login, and token management."""

import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from exceptions import ConflictError, UnauthorizedError, ValidationError
from models import User
from store import JSONStore

# JWT configuration
SECRET_KEY = "todo-app-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


class AuthService:
    """Handles registration, login, and token management."""

    def __init__(self, user_store: JSONStore):
        """Initialize with user store.

        Args:
            user_store: JSONStore instance for user persistence.
        """
        self.user_store = user_store

    def register(self, email: str, username: str, password: str, password_confirm: str) -> User:
        """Register a new user.

        Validates password match, checks email/username uniqueness,
        hashes password with bcrypt, and creates user record with UUID and timestamp.

        Args:
            email: User's email address.
            username: User's chosen username.
            password: User's password.
            password_confirm: Password confirmation for validation.

        Returns:
            The created User object.

        Raises:
            ValidationError: If passwords don't match.
            ConflictError: If email or username already exists.
        """
        # Validate password match
        if password != password_confirm:
            raise ValidationError([{"field": "password_confirm", "message": "Passwords do not match"}])

        # Check email uniqueness
        existing_email = self.user_store.find_by_field("email", email)
        if existing_email:
            raise ConflictError("Email already registered")

        # Check username uniqueness
        existing_username = self.user_store.find_by_field("username", username)
        if existing_username:
            raise ConflictError("Username already taken")

        # Hash password with bcrypt
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Create user record
        user_data = {
            "id": str(uuid.uuid4()),
            "email": email,
            "username": username,
            "password_hash": password_hash,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        self.user_store.add(user_data)

        return User(**user_data)

    def login(self, identifier: str, password: str) -> User:
        """Authenticate by email or username.

        Finds user by email or username, verifies password with bcrypt.
        Returns user on success or raises UnauthorizedError with generic message.

        Args:
            identifier: Email or username to authenticate with.
            password: Password to verify.

        Returns:
            The authenticated User object.

        Raises:
            UnauthorizedError: If credentials are invalid (generic message).
        """
        # Try to find user by email first, then by username
        user_data = self.user_store.find_by_field("email", identifier)
        if not user_data:
            user_data = self.user_store.find_by_field("username", identifier)

        if not user_data:
            raise UnauthorizedError("Invalid credentials")

        # Verify password with bcrypt
        if not bcrypt.checkpw(password.encode("utf-8"), user_data["password_hash"].encode("utf-8")):
            raise UnauthorizedError("Invalid credentials")

        return User(**user_data)

    def create_token(self, user_id: str) -> str:
        """Create a JWT with user_id claim and 24h expiry.

        Args:
            user_id: The user's ID to encode in the token.

        Returns:
            The encoded JWT string.
        """
        expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        payload = {
            "sub": user_id,
            "exp": expire,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    def verify_token(self, token: str) -> str:
        """Verify JWT signature and expiry, return user_id.

        Args:
            token: The JWT string to verify.

        Returns:
            The user_id extracted from the token.

        Raises:
            UnauthorizedError: If token is invalid, expired, or malformed.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str | None = payload.get("sub")
            if user_id is None:
                raise UnauthorizedError("Invalid token")
            return user_id
        except JWTError:
            raise UnauthorizedError("Invalid token")

    def get_user_by_id(self, user_id: str) -> User | None:
        """Retrieve user by id for session validation.

        Args:
            user_id: The user's ID to look up.

        Returns:
            The User object if found, None otherwise.
        """
        user_data = self.user_store.find_by_id(user_id)
        if not user_data:
            return None
        return User(**user_data)
