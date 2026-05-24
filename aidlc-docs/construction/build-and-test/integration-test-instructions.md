# Integration Test Instructions

## Purpose
Test the notification and reminder endpoints via HTTP to verify routers, services, and stores work together correctly with authentication.

## Prerequisites
- Backend server running: `uvicorn main:app --reload --port 8000`
- A registered user with valid JWT cookie (use `/api/auth/login` first)

## Setup Integration Test Environment

### 1. Start Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 2. Register and Login
```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123","password_confirm":"password123"}'

# Login (captures cookie)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email":"test@example.com","password":"password123"}'
```

---

## Unit 1: Notification Backend Scenarios

### Scenario 1: List Notifications (Empty State)
- **Endpoint**: `GET /api/notifications`
- **Auth**: Valid JWT cookie
- **Expected Response** (200):
```json
{
  "notifications": [],
  "unread_count": 0
}
```

### Scenario 2: Mark Read (Not Found)
- **Endpoint**: `PATCH /api/notifications/nonexistent-id/read`
- **Auth**: Valid JWT cookie
- **Expected Response** (404):
```json
{
  "detail": "Notification not found"
}
```

### Scenario 3: Mark All Read (Empty State)
- **Endpoint**: `POST /api/notifications/read-all`
- **Auth**: Valid JWT cookie
- **Expected Response** (200):
```json
{
  "message": "All notifications marked as read",
  "count": 0
}
```

### Scenario 4: Delete All (Empty State)
- **Endpoint**: `DELETE /api/notifications`
- **Auth**: Valid JWT cookie
- **Expected Response** (200):
```json
{
  "message": "All notifications cleared",
  "count": 0
}
```

### Scenario 5: Unauthenticated Access
- **Endpoint**: `GET /api/notifications`
- **Auth**: No cookie
- **Expected Response** (401):
```json
{
  "detail": "Authentication required"
}
```

---

## Unit 2: Reminder Trigger Logic Scenarios

### Scenario 6: Create Todo with reminder_at via API

**Description**: Verify the POST /api/todos endpoint accepts and returns `reminder_at`.

**Test Steps**:
```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"Buy groceries","reminder_at":"2026-05-25T09:00:00Z"}'
```

**Expected Results**:
- Response status: 201
- Response body includes `"reminder_at": "2026-05-25T09:00:00Z"` (or equivalent ISO format)

### Scenario 7: Update Todo to set reminder_at

**Description**: Verify PUT /api/todos/{id} accepts `reminder_at`.

**Test Steps**:
```bash
curl -X PUT http://localhost:8000/api/todos/{todo_id} \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"reminder_at":"2026-06-01T10:00:00Z"}'
```

**Expected Results**:
- Response status: 200
- Response body includes updated `reminder_at` value

### Scenario 8: Update Todo to clear reminder_at

**Description**: Verify PUT /api/todos/{id} accepts `null` to clear reminder.

**Test Steps**:
```bash
curl -X PUT http://localhost:8000/api/todos/{todo_id} \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"reminder_at":null}'
```

**Expected Results**:
- Response status: 200
- Response body includes `"reminder_at": null`

### Scenario 9: Create Todo with invalid reminder_at

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

### Scenario 10: GET /api/todos returns reminder_at

**Description**: Verify list endpoint includes `reminder_at` in response.

**Test Steps**:
```bash
curl -X GET http://localhost:8000/api/todos -b cookies.txt
```

**Expected Results**:
- Response status: 200
- Each todo object includes `reminder_at` field (null or ISO datetime string)

### Scenario 11: Existing todos without reminder_at still work

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

## Manual Integration Test Script

```bash
# 1. Register a user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123","password_confirm":"password123"}'

# 2. Login to get cookie
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  -c cookies.txt

# 3. List notifications (should be empty)
curl -X GET http://localhost:8000/api/notifications -b cookies.txt

# 4. Mark all read
curl -X POST http://localhost:8000/api/notifications/read-all -b cookies.txt

# 5. Delete all
curl -X DELETE http://localhost:8000/api/notifications -b cookies.txt

# 6. Unauthenticated (should 401)
curl -X GET http://localhost:8000/api/notifications

# 7. Create todo with reminder
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"Buy groceries","reminder_at":"2026-05-25T09:00:00Z"}'

# 8. List todos (verify reminder_at present)
curl -X GET http://localhost:8000/api/todos -b cookies.txt
```

## Cleanup
```bash
# Stop server (Ctrl+C)
# Remove test cookies
rm -f cookies.txt
```

## Notes
- Full integration with notification creation requires the reminder checker to run (Unit 2 triggers notifications via Unit 1's service)
- Unit 3 (Notification Bell UI) consumes Unit 1's HTTP endpoints
- Unit 4 (Reminder Form Integration) provides the frontend for setting reminder_at
