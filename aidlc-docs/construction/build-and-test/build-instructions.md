# Build Instructions — Unit 2: Reminder Trigger Logic

## Prerequisites
- **Python**: 3.11+
- **pip**: Latest version
- **Working Directory**: `backend/`

## Build Steps

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

No new dependencies were added for Unit 2. The existing `requirements.txt` covers all needs (Pydantic for models, FastAPI for routing).

### 2. Verify Python Syntax
```bash
cd backend
python -c "import ast; ast.parse(open('models.py').read()); print('models.py OK')"
python -c "import ast; ast.parse(open('services/todo_service.py').read()); print('todo_service.py OK')"
python -c "import ast; ast.parse(open('services/reminder_checker.py').read()); print('reminder_checker.py OK')"
```

### 3. Verify Imports
```bash
cd backend
python -c "from models import Todo, TodoCreate, TodoUpdate; print('Models import OK')"
python -c "from services.reminder_checker import check_user; print('ReminderChecker import OK')"
python -c "from services.todo_service import TodoService; print('TodoService import OK')"
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

## Troubleshooting

### Import Error: `models` module
- **Cause**: Running from wrong directory
- **Solution**: Ensure you're in the `backend/` directory when running

### Pydantic Validation Error on Startup
- **Cause**: Model field type mismatch
- **Solution**: Verify `reminder_at` field types match (datetime | None in Todo, str | None in TodoCreate/TodoUpdate)
