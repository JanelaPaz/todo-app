"""Notification router handling notification CRUD and reminder detection."""

import os

from fastapi import APIRouter, Depends, Response

from dependencies import get_current_user
from models import (
    Notification,
    NotificationResponse,
    NotificationsListResponse,
    User,
)
from services.notification_service import NotificationService
from services.reminder_checker import check_user
from store import JSONStore

# Initialize stores and services
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
notification_store = JSONStore(os.path.join(DATA_DIR, "notifications.json"))
todo_store = JSONStore(os.path.join(DATA_DIR, "todos.json"))
notification_service = NotificationService(notification_store)

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("", response_model=NotificationsListResponse)
async def list_notifications(
    current_user: User = Depends(get_current_user),
) -> NotificationsListResponse:
    """Get notifications for the authenticated user.

    On each call, runs reminder detection logic to auto-create
    notifications for due reminders and overdue todos.

    Returns notifications list (max 20, newest first) and unread count.

    Args:
        current_user: The authenticated user (injected by dependency).

    Returns:
        NotificationsListResponse with notifications and unread_count.
    """
    user_id = current_user.id

    # Read user's todos
    all_todos = todo_store.read_all()
    user_todos = [t for t in all_todos if t.get("user_id") == user_id]

    # Read existing notifications for deduplication
    all_notifications = notification_store.read_all()
    user_notifications = [
        n for n in all_notifications if n.get("user_id") == user_id
    ]

    # Detect new notifications via reminder_checker
    new_notifications = check_user(user_id, user_todos, user_notifications)

    # Create any newly detected notifications
    for todo_id, notification_type, message in new_notifications:
        if not notification_service.exists(user_id, todo_id, notification_type):
            notification_service.create(user_id, todo_id, notification_type, message)

    # Return current notification list
    notifications = notification_service.list_for_user(user_id)
    unread_count = notification_service.get_unread_count(user_id)

    return NotificationsListResponse(
        notifications=[
            NotificationResponse(
                id=n.id,
                user_id=n.user_id,
                todo_id=n.todo_id,
                type=n.type,
                message=n.message,
                is_read=n.is_read,
                created_at=n.created_at,
            )
            for n in notifications
        ],
        unread_count=unread_count,
    )


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
) -> NotificationResponse:
    """Mark a single notification as read.

    Args:
        notification_id: The notification's ID to mark as read.
        current_user: The authenticated user (injected by dependency).

    Returns:
        The updated notification.

    Raises:
        NotFoundError: If notification not found or not owned by user.
    """
    notification = notification_service.mark_as_read(
        user_id=current_user.id, notification_id=notification_id
    )

    return NotificationResponse(
        id=notification.id,
        user_id=notification.user_id,
        todo_id=notification.todo_id,
        type=notification.type,
        message=notification.message,
        is_read=notification.is_read,
        created_at=notification.created_at,
    )


@router.post("/read-all")
async def mark_all_as_read(
    current_user: User = Depends(get_current_user),
) -> dict:
    """Mark all notifications as read for the authenticated user.

    Args:
        current_user: The authenticated user (injected by dependency).

    Returns:
        Dict with marked_count indicating how many were marked.
    """
    marked_count = notification_service.mark_all_as_read(user_id=current_user.id)
    return {"marked_count": marked_count}


@router.delete("", status_code=204)
async def clear_all_notifications(
    current_user: User = Depends(get_current_user),
) -> Response:
    """Clear all notifications for the authenticated user.

    Args:
        current_user: The authenticated user (injected by dependency).

    Returns:
        204 No Content response on success.
    """
    notification_service.clear_all(user_id=current_user.id)
    return Response(status_code=204)
