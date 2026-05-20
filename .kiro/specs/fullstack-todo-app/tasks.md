# Implementation Plan: Full-Stack Todo Application

## Overview

This plan implements a full-stack Todo application with a Python FastAPI backend (JSON file storage, JWT auth via httpOnly cookies, bcrypt password hashing) and a Nuxt 3 frontend (TailwindCSS, Pinia state management, route guards). Tasks are ordered to build foundational layers first (data store, models, services), then API endpoints, then the frontend, and finally integration wiring.

## Tasks

- [x] 1. Set up backend project structure and core data layer
  - [x] 1.1 Initialize backend project with FastAPI, dependencies, and directory structure
    - Create `backend/` directory with `main.py`, `requirements.txt`, `data/` directory
    - Install dependencies: fastapi, uvicorn, pydantic[email], python-jose[cryptography], passlib[bcrypt], python-multipart
    - Configure CORS middleware allowing origin http://localhost:3000, methods GET/POST/PUT/DELETE, credentials, and Content-Type header
    - Create `backend/exceptions.py` with custom exception classes (ValidationError, ConflictError, UnauthorizedError, NotFoundError) and FastAPI exception handlers
    - _Requirements: 13.1, 13.2, 13.5_

  - [x] 1.2 Implement JSON Store persistence layer (`backend/store.py`)
    - Implement `JSONStore` class with `read_all`, `write_all`, `find_by_id`, `find_by_field`, `add`, `update`, `delete` methods
    - Implement atomic writes using temp file + `os.replace` to prevent corruption
    - Handle file-not-exists by creating file with empty array `[]`
    - Return 500 internal server error on file I/O failures
    - _Requirements: 14.1, 14.2, 14.3, 14.8_

  - [ ]* 1.3 Write property tests for JSON Store
    - **Property 15: Todo serialization round-trip**
    - **Property 16: User serialization round-trip**
    - **Property 17: ID uniqueness invariant**
    - **Property 18: Atomic write prevents corruption**
    - **Validates: Requirements 14.4, 14.5, 14.6, 14.7, 14.8**

  - [x] 1.4 Define Pydantic data models (`backend/models.py`)
    - Implement `User`, `UserCreate`, `UserResponse` models with email validation, username pattern, password min length
    - Implement `Priority` and `Status` enums
    - Implement `Todo`, `TodoCreate`, `TodoUpdate`, `TodoStats` models with field constraints (title 1-200 chars, description max 2000 chars)
    - _Requirements: 1.5, 5.2, 5.5, 5.8, 7.5, 7.6, 7.7, 7.8_

- [x] 2. Implement authentication service and endpoints
  - [x] 2.1 Implement Auth Service (`backend/services/auth_service.py`)
    - Implement `register` method: validate password match, check email/username uniqueness, hash password with bcrypt, create user record with UUID and timestamp
    - Implement `login` method: find user by email or username, verify password with bcrypt, return user on success or raise UnauthorizedError with generic message
    - Implement `create_token` method: create JWT with user_id claim and 24h expiry using python-jose
    - Implement `verify_token` method: verify signature, check expiry, return user_id or raise UnauthorizedError
    - Implement `get_user_by_id` method for session validation
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.1, 2.2, 2.3_

  - [ ]* 2.2 Write property tests for registration validation
    - **Property 1: Registration input validation**
    - **Validates: Requirements 1.1, 1.2, 1.5, 1.9**

  - [ ]* 2.3 Write property tests for registration uniqueness
    - **Property 2: Registration uniqueness enforcement**
    - **Validates: Requirements 1.3, 1.4**

  - [ ]* 2.4 Write property tests for user record creation
    - **Property 3: Registration creates correct user record with bcrypt hash**
    - **Validates: Requirements 1.6, 1.7**

  - [ ]* 2.5 Write property tests for JWT issuance and verification
    - **Property 4: Successful authentication issues valid JWT**
    - **Property 5: Invalid credentials return 401**
    - **Property 6: JWT verification correctness**
    - **Validates: Requirements 1.8, 2.1, 2.2, 2.3, 4.1, 4.2, 4.5**

  - [x] 2.6 Implement auth dependency and auth router (`backend/dependencies.py`, `backend/routers/auth.py`)
    - Implement `get_current_user` dependency: extract JWT from httpOnly cookie, verify token, load user from store, raise 401 if any step fails
    - Implement POST /api/auth/register endpoint: validate input, call auth service, set httpOnly cookie with JWT, return user response
    - Implement POST /api/auth/login endpoint: validate input, call auth service, set httpOnly cookie with JWT, return user response
    - Implement POST /api/auth/logout endpoint: clear JWT cookie, return 200
    - Implement GET /api/auth/me endpoint: return current user's id, email, username, created_at
    - _Requirements: 1.8, 1.9, 2.1, 2.4, 2.5, 3.1, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 3. Implement todo service and endpoints
  - [x] 3.1 Implement Todo Service (`backend/services/todo_service.py`)
    - Implement `create` method: validate title, set defaults (priority=medium, status=pending), generate UUID, set created_at, persist to store
    - Implement `list_todos` method: filter by user_id, apply optional status/priority filters, apply sort (due_date asc with nulls last, created_at desc)
    - Implement `get_by_id` method: find todo, verify ownership (return 404 if not owned or not found)
    - Implement `update` method: find todo, verify ownership, update only provided fields, set updated_at
    - Implement `delete` method: find todo, verify ownership, remove from store
    - Implement `get_stats` method: compute total, completed, pending, overdue counts
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 8.1, 8.2, 8.3, 8.4, 9.1, 9.2, 9.3, 9.4_

  - [ ]* 3.2 Write property tests for todo creation
    - **Property 7: Todo creation with correct fields and defaults**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4**

  - [ ]* 3.3 Write property tests for todo input validation
    - **Property 8: Todo input validation rejects invalid data**
    - **Validates: Requirements 5.5, 5.7, 5.8, 6.9, 7.5, 7.6, 7.7, 7.8**

  - [ ]* 3.4 Write property tests for user data isolation
    - **Property 9: User data isolation**
    - **Validates: Requirements 6.1, 6.7, 7.3, 8.3**

  - [ ]* 3.5 Write property tests for filtering and sorting
    - **Property 10: Filter correctness**
    - **Property 11: Sort correctness**
    - **Validates: Requirements 6.2, 6.3, 6.4, 6.5**

  - [ ]* 3.6 Write property tests for update and delete operations
    - **Property 12: Update modifies only specified fields**
    - **Property 13: Delete removes todo from store**
    - **Validates: Requirements 7.1, 8.1**

  - [ ]* 3.7 Write property tests for statistics computation
    - **Property 14: Statistics computation correctness**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4**

  - [x] 3.8 Implement todo router (`backend/routers/todos.py`)
    - Implement GET /api/todos endpoint: accept status, priority, sort_by query params, validate param values, call todo service list_todos
    - Implement POST /api/todos endpoint: validate request body, call todo service create, return 201
    - Implement GET /api/todos/{id} endpoint: call todo service get_by_id
    - Implement PUT /api/todos/{id} endpoint: validate request body, call todo service update
    - Implement DELETE /api/todos/{id} endpoint: call todo service delete, return 204
    - _Requirements: 5.6, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.2, 8.2_

- [x] 4. Checkpoint - Backend complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Set up frontend project structure
  - [x] 5.1 Initialize Nuxt 3 project with TailwindCSS and Pinia
    - Create `frontend/` directory with Nuxt 3 project (nuxt.config.ts, package.json)
    - Install and configure TailwindCSS with indigo/violet primary palette and neutral gray secondary colors
    - Install and configure Pinia for state management
    - Set up directory structure: pages/, components/, composables/, middleware/, stores/, types/
    - _Requirements: 11.1_

  - [x] 5.2 Define TypeScript types and API client (`frontend/types/index.ts`, `frontend/utils/api.ts`)
    - Define User, Todo, TodoStats, TodoCreate, TodoUpdate interfaces
    - Create API client using `$fetch` with `credentials: 'include'` for cookie-based auth
    - Configure base URL to http://localhost:8000/api
    - Implement 15-second timeout handling
    - _Requirements: 10.5_

- [x] 6. Implement frontend authentication
  - [x] 6.1 Implement auth Pinia store (`frontend/stores/auth.ts`)
    - Implement state: user, isAuthenticated, loading, error
    - Implement actions: login, register, logout, fetchUser (GET /api/auth/me)
    - Handle error responses (401, 409, 422) and set appropriate error messages
    - _Requirements: 2.4, 3.2, 10.6_

  - [x] 6.2 Implement auth composable with form validation (`frontend/composables/useAuth.ts`)
    - Implement client-side validation: required fields, email format, password min 8 chars, password confirmation match, username 3-30 chars alphanumeric/underscore
    - Implement form submission with loading state and 15-second timeout
    - _Requirements: 10.3, 10.4, 10.5_

  - [x] 6.3 Implement global auth middleware (`frontend/middleware/auth.global.ts`)
    - Redirect unauthenticated users from protected pages (dashboard) to login
    - Redirect authenticated users from login/register to dashboard
    - Check auth state via /api/auth/me on initial load
    - _Requirements: 10.1, 10.2_

  - [x] 6.4 Implement Login page (`frontend/pages/login.vue`)
    - Create login form with email/username and password fields
    - Display field-level validation errors and server error messages
    - Show loading indicator on submit, disable button during request
    - Implement split-screen layout with decorative panel on desktop (≥1024px)
    - _Requirements: 2.4, 10.3, 10.4, 10.6, 11.3_

  - [x] 6.5 Implement Register page (`frontend/pages/register.vue`)
    - Create registration form with email, username, password, password confirmation fields
    - Display field-level validation errors and server error messages
    - Show loading indicator on submit, disable button during request
    - Implement split-screen layout with decorative panel on desktop (≥1024px)
    - _Requirements: 10.3, 10.4, 10.6, 11.3_

- [x] 7. Implement frontend todo management
  - [x] 7.1 Implement todos Pinia store (`frontend/stores/todos.ts`)
    - Implement state: todos list, filters (status, priority), sort_by, loading, stats
    - Implement actions: fetchTodos (with filter/sort params), createTodo, updateTodo, deleteTodo, fetchStats
    - Implement getters for filtered/sorted todos and statistics
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 9.7_

  - [x] 7.2 Implement todo composable (`frontend/composables/useTodos.ts`)
    - Wrap todo store with optimistic updates for create/update/delete
    - Implement error handling with rollback on failure
    - _Requirements: 9.7_

  - [x] 7.3 Implement UI utility components
    - Create `components/Toast.vue`: notification system with auto-dismiss (5s) and manual dismiss
    - Create `components/ConfirmDialog.vue`: reusable confirmation modal
    - Create `components/LoadingSkeleton.vue`: skeleton placeholders for loading states
    - Create `components/EmptyState.vue`: empty state illustration with guidance text
    - Create `components/DarkModeToggle.vue`: theme toggle with localStorage persistence, default light
    - _Requirements: 11.5, 11.6, 11.7, 11.8_

  - [x] 7.4 Implement Dashboard page with statistics (`frontend/pages/dashboard.vue`)
    - Create `components/StatsCards.vue`: display total, completed, pending, overdue counts
    - Create `components/FilterBar.vue`: status/priority filter dropdowns and sort controls
    - Integrate stats cards, filter bar, and todo list
    - Refresh stats and list on create/update/delete
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7_

  - [x] 7.5 Implement TodoItem and TodoList components
    - Create `components/TodoItem.vue`: display todo with inline edit (title, status), edit button, delete button
    - Implement inline editing: save on Enter/blur, cancel on Escape
    - Create `components/TodoList.vue`: render filtered/sorted list of TodoItems
    - Apply CSS transitions (150-300ms) for hover states and component mount/unmount
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 11.4_

  - [x] 7.6 Implement TodoForm component and edit modal
    - Create `components/TodoForm.vue`: form with title, description, priority, due_date, status fields
    - Use as create form and as edit modal pre-populated with current values
    - Validate inputs before submission
    - _Requirements: 12.2_

- [x] 8. Implement responsive layout and polish
  - [x] 8.1 Implement responsive layout and dark mode
    - Create app layout with responsive breakpoints: mobile (<768px), tablet (768-1023px), desktop (≥1024px)
    - Ensure all interactive elements visible without horizontal scrolling at all breakpoints
    - Implement dark mode CSS variables and toggle integration
    - Apply exit animation (≤300ms) on todo deletion
    - _Requirements: 11.2, 11.4, 11.8, 12.4_

- [x] 9. Checkpoint - Frontend complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 10. Integration, documentation, and final wiring
  - [x] 10.1 Wire frontend and backend together and verify end-to-end flows
    - Ensure cookie-based auth works across frontend/backend
    - Verify CORS preflight requests succeed
    - Test full auth flow: register → login → dashboard → logout
    - Test full todo CRUD flow: create → read → update → delete
    - _Requirements: 13.1, 13.2, 13.5_

  - [x] 10.2 Create project documentation and run script
    - Create `README.md` with prerequisites (Python 3.11+, Node.js 18+), backend setup steps, frontend setup steps, server URLs
    - Create `run.sh` script that starts both backend (uvicorn) and frontend (nuxt dev) servers
    - _Requirements: 13.3, 13.4_

  - [ ]* 10.3 Write frontend unit tests
    - Test component rendering for key states (loading, empty, error, populated)
    - Test Pinia store actions and state mutations
    - Test composable validation logic
    - Test middleware route guard behavior
    - _Requirements: 10.1, 10.2, 10.3, 11.7_

- [x] 11. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document (Properties 1-18)
- Unit tests validate specific examples and edge cases
- Backend uses Python with pytest + Hypothesis for property-based testing
- Frontend uses TypeScript with Vitest + Vue Test Utils for unit testing
- The backend must be fully functional before frontend integration testing

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "5.1"] },
    { "id": 1, "tasks": ["1.2", "1.4", "5.2"] },
    { "id": 2, "tasks": ["1.3", "2.1"] },
    { "id": 3, "tasks": ["2.2", "2.3", "2.4", "2.5", "2.6"] },
    { "id": 4, "tasks": ["3.1", "6.1", "6.2", "6.3"] },
    { "id": 5, "tasks": ["3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "6.4", "6.5"] },
    { "id": 6, "tasks": ["7.1", "7.2", "7.3"] },
    { "id": 7, "tasks": ["7.4", "7.5", "7.6"] },
    { "id": 8, "tasks": ["8.1"] },
    { "id": 9, "tasks": ["10.1", "10.2"] },
    { "id": 10, "tasks": ["10.3"] }
  ]
}
```
