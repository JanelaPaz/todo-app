# Unit 2 — Build Instructions

Unit 2 introduces no new dependencies. The existing `backend/requirements.txt`
already covers everything needed for `reminder_at` validation and the pure
detection function in `reminder_checker.py`.

## 1. Activate the backend environment

```bash
cd backend
python3 -m venv .venv          # only if not already created
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Verify syntax and imports

```bash
python -m py_compile models.py services/todo_service.py services/reminder_checker.py
python -c "from services.reminder_checker import check_user, Notification; print('ok')"
```

Both commands should exit `0` with no output (the second prints `ok`).

## 3. Start the server

```bash
uvicorn main:app --reload --port 8000
```

The API serves at `http://localhost:8000`. Visit
`http://localhost:8000/docs` to see `reminder_at` listed on the
`POST /api/todos` and `PUT /api/todos/{id}` request bodies.

## 4. Smoke check

```bash
curl -s http://localhost:8000/openapi.json | python -c "import json,sys; s=json.load(sys.stdin); print('reminder_at' in json.dumps(s['components']['schemas']))"
```

Expected: `True`.
