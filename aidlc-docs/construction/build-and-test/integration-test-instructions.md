# Integration Test Instructions — Unit 2: Reminder Trigger Logic

## Purpose
Test that Unit 2's changes integrate correctly with the existing Todo API endpoints.

## Test Scenarios

### Scenario 1: Create Todo with reminder_at via API

**Description**: Verify the POST /api/todos endpoint accepts and returns `reminder_at`.

**Setup**: Start backend server, register a user, login to get auth cookie.

**Test Steps**:
```bash
# 1. Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123","password_confirm":"password123"}'

# 2. Login (captures cookie)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email":"test@example.com","password":"password123"}'

# 3. Create todo with reminder_at
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"Buy groceries","reminder_at":"2026-05-25T09:00:00Z"}'
```

**Expected Results**:
- Response status: 201
- Response body includes `"reminder_at": "2026-05-25T09:00:00Z"` (or equivalent ISO format)

---

### Scenario 2: Update Todo to set reminder_at

**Description**: Verify PUT /api/todos/{id} accepts `reminder_at`.

**Test Steps**:
```bash
# Update existing todo with reminder_at
curl -X PUT http://localhost:8000/api/todos/{todo_id} \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"reminder_at":"2026-06-01T10:00:00Z"}'
```

**Expected Results**:
- Response status: 200
- Response body includes updated `reminder_at` value

---

### Scenario 3: Update Todo to clear reminder_at

**Description**: Verify PUT /api/todos/{id} accepts `null` to clear reminder.

**Test Steps**:
```bash
# Clear reminder_at
curl -X PUT http://localhost:8000/api/todos/{todo_id} \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"reminder_at":null}'
```

**Expected Results**:
- Response status: 200
- Response body includes `"reminder_at": null`

---

### Scenario 4: Create Todo with invalid reminder_at

**Description**: Verify validation rejects invalid datetime format.

**Test Steps**:
```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"Bad reminder","reminder_at":"not-a-date"}'
```

**Expected Results**:
- Response status: 422
- Error message mentions invalid datetime format

---

### Scenario 5: GET /api/todos returns reminder_at

**Description**: Verify list endpoint includes `reminder_at` in response.

**Test Steps**:
```bash
curl -X GET http://localhost:8000/api/todos \
  -b cookies.txt
```

**Expected Results**:
- Response status: 200
- Each todo object includes `reminder_at` field (null or ISO datetime string)

---

### Scenario 6: Existing todos without reminder_at still work

**Description**: Verify backward compatibility — existing todos in `data/todos.json` without `reminder_at` field still load correctly.

**Test Steps**:
1. Ensure `data/todos.json` has existing todos without `reminder_at` key
2. Start server
3. Call `GET /api/todos`

**Expected Results**:
- Response status: 200
- Existing todos return with `reminder_at: null`
- No errors or crashes

---

## Setup Integration Test Environment

### 1. Start Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 2. Clean Test Data (Optional)
```bash
# Reset todos.json to empty array for clean test
echo "[]" > backend/data/todos.json
```

## Cleanup
```bash
# Stop server (Ctrl+C)
# Remove test cookies
rm -f cookies.txt
```
