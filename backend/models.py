"""Pydantic data models for the Todo application."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


# --- User Models ---


class User(BaseModel):
    """Internal user model with all fields including password hash."""

    id: str  # UUID4 string
    email: EmailStr  # Valid email format
    username: str  # 3-30 chars, alphanumeric + underscore
    password_hash: str  # bcrypt hash
    created_at: datetime  # ISO 8601 timestamp


class UserCreate(BaseModel):
    """Request model for user registration."""

    email: EmailStr
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8)
    password_confirm: str


class UserResponse(BaseModel):
    """Response model for user data (excludes password_hash)."""

    id: str
    email: str
    username: str
    created_at: datetime


# --- Enums ---


class Priority(str, Enum):
    """Priority levels for todo items."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(str, Enum):
    """Status values for todo items."""

    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    DONE = "done"


# --- Todo Models ---


class Todo(BaseModel):
    """Internal todo model with all fields."""

    id: str  # UUID4 string
    user_id: str  # Reference to User.id
    title: str  # 1-200 chars, non-whitespace-only
    description: str | None = None  # Optional, max 2000 chars
    priority: Priority = Priority.MEDIUM
    due_date: str | None = None  # ISO 8601 date (YYYY-MM-DD) or None
    status: Status = Status.PENDING
    reminder_at: datetime | None = None  # ISO 8601 datetime or None
    created_at: datetime
    updated_at: datetime | None = None


class TodoCreate(BaseModel):
    """Request model for creating a todo."""

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    priority: Priority = Priority.MEDIUM
    due_date: str | None = None  # Validated as YYYY-MM-DD
    status: Status = Status.PENDING
    reminder_at: str | None = None  # Validated as ISO 8601 datetime


class TodoUpdate(BaseModel):
    """Request model for updating a todo (all fields optional)."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    priority: Priority | None = None
    due_date: str | None = None
    status: Status | None = None
    reminder_at: str | None = None  # ISO 8601 datetime or null to clear


class TodoStats(BaseModel):
    """Statistics model for dashboard display."""

    total: int
    completed: int
    pending: int
    overdue: int


# --- Notification Models ---


class NotificationType(str, Enum):
    """Types of notifications."""

    REMINDER = "reminder"
    OVERDUE = "overdue"


class Notification(BaseModel):
    """Internal notification model with all fields."""

    id: str  # UUID4 string
    user_id: str  # Reference to User.id
    todo_id: str  # Reference to Todo.id
    type: NotificationType
    message: str  # Human-readable message
    is_read: bool = False
    created_at: datetime  # ISO 8601 timestamp


class NotificationResponse(BaseModel):
    """Response model for a single notification."""

    id: str
    user_id: str
    todo_id: str
    type: NotificationType
    message: str
    is_read: bool
    created_at: datetime


class NotificationsListResponse(BaseModel):
    """Response model for notification list endpoint."""

    notifications: list[NotificationResponse]
    unread_count: int
