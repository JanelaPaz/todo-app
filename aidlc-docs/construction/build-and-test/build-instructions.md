# Build Instructions

## Prerequisites
- **Python**: 3.11+
- **Package Manager**: pip
- **Dependencies**: See `backend/requirements.txt`
- **Test Framework**: pytest

## Build Steps

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
pip install pytest
```

### 2. Verify Python Syntax
```bash
cd backend
python -c "import ast; ast.parse(open('models.py').read()); print('models.py OK')"
python -c "import ast; ast.parse(open('services/todo_service.py').read()); print('todo_service.py OK')"
python -c "import ast; ast.parse(open('services/reminder_checker.py').read()); print('reminder_checker.py OK')"
python -c "import ast; ast.parse(open('services/notification_service.py').read()); print('notification_service.py OK')"
```

### 3. Verify Imports
```bash
cd backend
python -c "from models import Todo, TodoCreate, TodoUpdate; print('Models import OK')"
python -c "from models import Notification, NotificationType; print('Notification models import OK')"
python -c "from services.reminder_checker import check_user; print('ReminderChecker import OK')"
python -c "from services.todo_service import TodoService; print('TodoService import OK')"
python -c "from services.notification_service import NotificationService; print('NotificationService import OK')"
```

### 4. Start the Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 5. Verify Build Success
- **Expected Output**: Server starts on `http://localhost:8000`
- **Health Check**: `curl http://localhost:8000/` should return `{"status":"ok","message":"Todo App API"}`
- **No import errors** in server startup logs

### 6. Verify Endpoints Registered
With the server running, visit `http://localhost:8000/docs` and confirm:
- `/api/notifications` (GET) is listed
- `/api/notifications/{notification_id}/read` (PATCH) is listed
- `/api/notifications/read-all` (POST) is listed
- `/api/notifications` (DELETE) is listed
- `/api/todos` (POST/GET/PUT/DELETE) includes `reminder_at` field

### 7. Verify Data Files Exist
```bash
cat backend/data/notifications.json
cat backend/data/todos.json
```

## Build Artifacts
- No compiled artifacts (Python interpreted)
- `backend/data/notifications.json` — empty JSON array (storage file)
- `backend/data/todos.json` — todo storage file

## Troubleshooting

### Import Error: email-validator
- **Cause**: `pydantic[email]` extras not installed
- **Solution**: `pip install pydantic[email]`

### ModuleNotFoundError: passlib or python-jose
- **Cause**: Auth dependencies not installed
- **Solution**: `pip install -r requirements.txt`

### Import Error: `models` module
- **Cause**: Running from wrong directory
- **Solution**: Ensure you're in the `backend/` directory when running

### Pydantic Validation Error on Startup
- **Cause**: Model field type mismatch
- **Solution**: Verify `reminder_at` field types match (datetime | None in Todo, str | None in TodoCreate/TodoUpdate)
