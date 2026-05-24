"""Todo service handling CRUD operations scoped to authenticated users."""

import re
import uuid
from datetime import date, datetime, timezone

from exceptions import NotFoundError, ValidationError
from models import Priority, Status, Todo, TodoCreate, TodoStats, TodoUpdate
from store import JSONStore


class TodoService:
    """Handles CRUD operations on todos scoped to the authenticated user."""

    def __init__(self, todo_store: JSONStore):
        """Initialize with todo store.

        Args:
            todo_store: JSONStore instance for todo persistence.
        """
        self.todo_store = todo_store

    def create(self, user_id: str, data: TodoCreate) -> Todo:
        """Create a todo for the user.

        Validates title, sets defaults (priority=medium, status=pending),
        generates UUID, sets created_at, and persists to store.

        Args:
            user_id: The authenticated user's ID.
            data: TodoCreate model with todo fields.

        Returns:
            The created Todo object.

        Raises:
            ValidationError: If title is invalid or due_date/reminder_at format is wrong.
        """
        # Validate title is not whitespace-only
        if not data.title or not data.title.strip():
            raise ValidationError([{"field": "title", "message": "Title must not be blank"}])

        # Validate due_date format if provided
        if data.due_date is not None:
            self._validate_due_date(data.due_date)

        # Validate reminder_at format if provided
        if data.reminder_at is not None:
            self._validate_reminder_at(data.reminder_at)

        # Create todo record with defaults
        todo_data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "title": data.title,
            "description": data.description,
            "priority": data.priority.value if data.priority else Priority.MEDIUM.value,
            "due_date": data.due_date,
            "status": data.status.value if data.status else Status.PENDING.value,
            "reminder_at": data.reminder_at,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": None,
        }

        self.todo_store.add(todo_data)

        return Todo(**todo_data)

    def list_todos(
        self,
        user_id: str,
        status: str | None = None,
        priority: str | None = None,
        sort_by: str | None = None,
    ) -> list[Todo]:
        """List user's todos with optional filtering and sorting.

        Filters by user_id, applies optional status/priority filters,
        and applies sort (due_date asc with nulls last, created_at desc).

        Args:
            user_id: The authenticated user's ID.
            status: Optional status filter value.
            priority: Optional priority filter value.
            sort_by: Optional sort field ("due_date" or "created_at").

        Returns:
            A list of Todo objects matching the criteria.

        Raises:
            ValidationError: If filter/sort values are invalid.
        """
        # Validate filter values
        if status is not None:
            valid_statuses = [s.value for s in Status]
            if status not in valid_statuses:
                raise ValidationError(
                    [{"field": "status", "message": f"Invalid status value. Must be one of: {', '.join(valid_statuses)}"}]
                )

        if priority is not None:
            valid_priorities = [p.value for p in Priority]
            if priority not in valid_priorities:
                raise ValidationError(
                    [{"field": "priority", "message": f"Invalid priority value. Must be one of: {', '.join(valid_priorities)}"}]
                )

        if sort_by is not None:
            valid_sorts = ["due_date", "created_at"]
            if sort_by not in valid_sorts:
                raise ValidationError(
                    [{"field": "sort_by", "message": f"Invalid sort_by value. Must be one of: {', '.join(valid_sorts)}"}]
                )

        # Get all records and filter by user_id
        all_records = self.todo_store.read_all()
        user_todos = [r for r in all_records if r.get("user_id") == user_id]

        # Apply status filter
        if status is not None:
            user_todos = [r for r in user_todos if r.get("status") == status]

        # Apply priority filter
        if priority is not None:
            user_todos = [r for r in user_todos if r.get("priority") == priority]

        # Apply sorting
        if sort_by == "due_date":
            # Ascending order with nulls last
            user_todos.sort(key=lambda r: (r.get("due_date") is None, r.get("due_date") or ""))
        elif sort_by == "created_at":
            # Descending order
            user_todos.sort(key=lambda r: r.get("created_at", ""), reverse=True)

        return [Todo(**r) for r in user_todos]

    def get_by_id(self, user_id: str, todo_id: str) -> Todo:
        """Get a specific todo by ID.

        Finds the todo and verifies ownership. Returns 404 if not found or not owned.

        Args:
            user_id: The authenticated user's ID.
            todo_id: The todo's ID to retrieve.

        Returns:
            The Todo object.

        Raises:
            NotFoundError: If todo is not found or not owned by user.
        """
        record = self.todo_store.find_by_id(todo_id)

        if not record or record.get("user_id") != user_id:
            raise NotFoundError("Todo not found")

        return Todo(**record)

    def update(self, user_id: str, todo_id: str, data: TodoUpdate) -> Todo:
        """Update a todo.

        Finds the todo, verifies ownership, updates only provided fields,
        and sets updated_at.

        Args:
            user_id: The authenticated user's ID.
            todo_id: The todo's ID to update.
            data: TodoUpdate model with fields to update.

        Returns:
            The updated Todo object.

        Raises:
            NotFoundError: If todo is not found or not owned by user.
            ValidationError: If updated fields are invalid.
        """
        # Find and verify ownership
        record = self.todo_store.find_by_id(todo_id)

        if not record or record.get("user_id") != user_id:
            raise NotFoundError("Todo not found")

        # Build updates dict with only provided fields
        updates = {}

        if data.title is not None:
            if not data.title.strip():
                raise ValidationError([{"field": "title", "message": "Title must not be blank"}])
            updates["title"] = data.title

        if data.description is not None:
            updates["description"] = data.description

        if data.priority is not None:
            updates["priority"] = data.priority.value

        if data.due_date is not None:
            self._validate_due_date(data.due_date)
            updates["due_date"] = data.due_date

        if data.status is not None:
            updates["status"] = data.status.value

        if data.reminder_at is not None:
            self._validate_reminder_at(data.reminder_at)
            updates["reminder_at"] = data.reminder_at
        elif "reminder_at" in data.model_fields_set:
            # Explicitly set to null — clear the reminder
            updates["reminder_at"] = None

        # Set updated_at timestamp
        updates["updated_at"] = datetime.now(timezone.utc).isoformat()

        # Persist updates
        updated_record = self.todo_store.update(todo_id, updates)

        if not updated_record:
            raise NotFoundError("Todo not found")

        return Todo(**updated_record)

    def delete(self, user_id: str, todo_id: str) -> None:
        """Delete a todo.

        Finds the todo, verifies ownership, and removes from store.

        Args:
            user_id: The authenticated user's ID.
            todo_id: The todo's ID to delete.

        Raises:
            NotFoundError: If todo is not found or not owned by user.
        """
        # Find and verify ownership
        record = self.todo_store.find_by_id(todo_id)

        if not record or record.get("user_id") != user_id:
            raise NotFoundError("Todo not found")

        # Remove from store
        deleted = self.todo_store.delete(todo_id)

        if not deleted:
            raise NotFoundError("Todo not found")

    def get_stats(self, user_id: str) -> TodoStats:
        """Compute dashboard statistics for the user.

        Computes total, completed, pending, and overdue counts.
        Overdue = due_date before today AND status != done.

        Args:
            user_id: The authenticated user's ID.

        Returns:
            TodoStats with computed counts.
        """
        all_records = self.todo_store.read_all()
        user_todos = [r for r in all_records if r.get("user_id") == user_id]

        total = len(user_todos)
        completed = sum(1 for r in user_todos if r.get("status") == Status.DONE.value)
        pending = sum(1 for r in user_todos if r.get("status") in (Status.PENDING.value, Status.IN_PROGRESS.value))

        today = date.today()
        overdue = 0
        for r in user_todos:
            due = r.get("due_date")
            if due and r.get("status") != Status.DONE.value:
                try:
                    due_date = date.fromisoformat(due)
                    if due_date < today:
                        overdue += 1
                except (ValueError, TypeError):
                    pass

        return TodoStats(total=total, completed=completed, pending=pending, overdue=overdue)

    def _validate_due_date(self, due_date: str) -> None:
        """Validate that due_date is a valid ISO 8601 date (YYYY-MM-DD).

        Args:
            due_date: The date string to validate.

        Raises:
            ValidationError: If the date format is invalid.
        """
        # Check format with regex first
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", due_date):
            raise ValidationError(
                [{"field": "due_date", "message": "Invalid date format. Must be YYYY-MM-DD"}]
            )

        # Verify it's a valid date
        try:
            date.fromisoformat(due_date)
        except ValueError:
            raise ValidationError(
                [{"field": "due_date", "message": "Invalid date format. Must be YYYY-MM-DD"}]
            )

    def _validate_reminder_at(self, reminder_at: str) -> None:
        """Validate that reminder_at is a valid ISO 8601 datetime.

        Accepts formats like:
        - 2026-05-24T09:00:00Z
        - 2026-05-24T09:00:00+00:00
        - 2026-05-24T09:00:00

        Args:
            reminder_at: The datetime string to validate.

        Raises:
            ValidationError: If the datetime format is invalid.
        """
        try:
            datetime.fromisoformat(reminder_at.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            raise ValidationError(
                [{"field": "reminder_at", "message": "Invalid datetime format. Must be ISO 8601 (e.g., 2026-05-24T09:00:00Z)"}]
            )
