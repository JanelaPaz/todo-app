"""Todo router handling CRUD operations and statistics endpoints."""

import os

from fastapi import APIRouter, Depends, Query, Response

from dependencies import get_current_user
from models import Todo, TodoCreate, TodoStats, TodoUpdate, User
from services.todo_service import TodoService
from store import JSONStore

# Initialize todo store and service
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
todo_store = JSONStore(os.path.join(DATA_DIR, "todos.json"))
todo_service = TodoService(todo_store)

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("/stats", response_model=TodoStats)
async def get_stats(current_user: User = Depends(get_current_user)) -> TodoStats:
    """Get dashboard statistics for the authenticated user.

    Returns total, completed, pending, and overdue counts.

    Args:
        current_user: The authenticated user (injected by dependency).

    Returns:
        TodoStats with computed counts.
    """
    return todo_service.get_stats(current_user.id)


@router.get("", response_model=list[Todo])
async def list_todos(
    status: str | None = Query(default=None, description="Filter by status (pending, in-progress, done)"),
    priority: str | None = Query(default=None, description="Filter by priority (low, medium, high)"),
    sort_by: str | None = Query(default=None, description="Sort by field (due_date, created_at)"),
    current_user: User = Depends(get_current_user),
) -> list[Todo]:
    """List todos for the authenticated user with optional filtering and sorting.

    Accepts status, priority, and sort_by query parameters.
    Validates parameter values and calls todo service list_todos.

    Args:
        status: Optional status filter value.
        priority: Optional priority filter value.
        sort_by: Optional sort field.
        current_user: The authenticated user (injected by dependency).

    Returns:
        A list of Todo objects matching the criteria.
    """
    return todo_service.list_todos(
        user_id=current_user.id,
        status=status,
        priority=priority,
        sort_by=sort_by,
    )


@router.post("", response_model=Todo, status_code=201)
async def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
) -> Todo:
    """Create a new todo for the authenticated user.

    Validates request body via Pydantic model and calls todo service create.

    Args:
        todo_data: The todo creation request body.
        current_user: The authenticated user (injected by dependency).

    Returns:
        The created Todo object with 201 status code.
    """
    return todo_service.create(user_id=current_user.id, data=todo_data)


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user),
) -> Todo:
    """Get a specific todo by ID.

    Calls todo service get_by_id which verifies ownership.

    Args:
        todo_id: The todo's ID to retrieve.
        current_user: The authenticated user (injected by dependency).

    Returns:
        The Todo object if found and owned by the user.
    """
    return todo_service.get_by_id(user_id=current_user.id, todo_id=todo_id)


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: str,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
) -> Todo:
    """Update a specific todo by ID.

    Validates request body via Pydantic model and calls todo service update.

    Args:
        todo_id: The todo's ID to update.
        todo_data: The todo update request body.
        current_user: The authenticated user (injected by dependency).

    Returns:
        The updated Todo object.
    """
    return todo_service.update(user_id=current_user.id, todo_id=todo_id, data=todo_data)


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user),
) -> Response:
    """Delete a specific todo by ID.

    Calls todo service delete which verifies ownership.

    Args:
        todo_id: The todo's ID to delete.
        current_user: The authenticated user (injected by dependency).

    Returns:
        204 No Content response on success.
    """
    todo_service.delete(user_id=current_user.id, todo_id=todo_id)
    return Response(status_code=204)
