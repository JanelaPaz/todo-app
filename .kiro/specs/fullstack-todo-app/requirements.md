# Requirements Document

## Introduction

A full-stack Todo application designed as a polished workshop demo. The application features user authentication with JWT tokens, full CRUD operations on todos with filtering and sorting, and a modern responsive UI. The backend uses Python with FastAPI and JSON file-based storage, while the frontend uses Nuxt 3 with TailwindCSS.

## Glossary

- **Backend**: The Python FastAPI server responsible for API endpoints, authentication, and data persistence
- **Frontend**: The Nuxt 3 (Vue 3 + Composition API) client application with TailwindCSS styling
- **JSON_Store**: The file-based storage system using users.json and todos.json files for data persistence
- **Auth_Service**: The authentication service responsible for user registration, login, logout, and token management
- **Todo_Service**: The service responsible for CRUD operations on todo items
- **JWT**: JSON Web Token used for stateless authentication, stored in httpOnly cookies
- **User**: An entity with id, email, username, password_hash, and created_at fields
- **Todo**: An entity with id, user_id, title, description, priority, due_date, status, reminder_at, created_at, and updated_at fields
- **Dashboard**: The main authenticated view showing todo statistics, recent activity, and the todo list
- **Priority**: A classification for todos with values: low, medium, or high
- **Status**: A classification for todo progress with values: pending, in-progress, or done

## Requirements

### Requirement 1: User Registration

**User Story:** As a new user, I want to register with my email, username, and password, so that I can create an account and manage my todos.

#### Acceptance Criteria

1. WHEN a registration request is received with email, username, password, and password confirmation, THE Auth_Service SHALL validate that the password and password confirmation match
2. IF the password and password confirmation do not match, THEN THE Auth_Service SHALL return a 422 validation error with a message indicating the passwords do not match
3. WHEN a registration request contains an email already present in the JSON_Store, THE Auth_Service SHALL return a 409 conflict error with a message indicating the email is already registered
4. WHEN a registration request contains a username already present in the JSON_Store, THE Auth_Service SHALL return a 409 conflict error with a message indicating the username is already taken
5. WHEN a valid registration request is received, THE Auth_Service SHALL validate that the email is in a valid email format, the username is between 3 and 30 characters containing only alphanumeric characters and underscores, and the password is at least 8 characters long
6. WHEN a valid registration request is received, THE Auth_Service SHALL hash the password using bcrypt before storing the User in the JSON_Store
7. WHEN a valid registration request is received, THE Auth_Service SHALL create a User record with a unique id, the provided email, username, the hashed password, and a created_at timestamp
8. WHEN registration is successful, THE Auth_Service SHALL issue a JWT token with an expiration time of 24 hours and set it as an httpOnly cookie in the response
9. WHEN a registration request is missing required fields, THE Auth_Service SHALL return a 422 validation error with field-level error messages identifying each missing or invalid field

### Requirement 2: User Login

**User Story:** As a registered user, I want to log in with my email or username and password, so that I can access my todos.

#### Acceptance Criteria

1. WHEN a login request is received with a valid email or username and correct password, THE Auth_Service SHALL issue a JWT token with a 24-hour expiration containing the user's id and set it as an httpOnly cookie in the response
2. IF a login request contains an email or username that does not exist in the JSON_Store, THEN THE Auth_Service SHALL return a 401 unauthorized error with a generic message indicating invalid credentials
3. IF a login request contains a valid email or username but incorrect password, THEN THE Auth_Service SHALL return a 401 unauthorized error with a generic message indicating invalid credentials
4. WHEN login is successful, THE Frontend SHALL redirect the user to the Dashboard
5. IF a login request is missing the identifier (email or username) or password field, THEN THE Auth_Service SHALL return a 422 validation error with descriptive field-level error messages

### Requirement 3: User Logout

**User Story:** As a logged-in user, I want to log out, so that my session is terminated and my account is secured.

#### Acceptance Criteria

1. WHEN a logout request is received with a valid JWT cookie, THE Auth_Service SHALL clear the JWT httpOnly cookie from the response and return a 200 status code
2. WHEN logout is successful, THE Frontend SHALL clear the client-side authentication state and redirect the user to the login page
3. IF a logout request is received without a valid JWT cookie, THEN THE Auth_Service SHALL still clear the JWT httpOnly cookie from the response and return a 200 status code

### Requirement 4: Session Validation

**User Story:** As a logged-in user, I want my session to be validated on each request, so that only authenticated users can access protected resources.

#### Acceptance Criteria

1. WHEN a request to a protected endpoint includes a JWT cookie that has a valid signature, is not expired, and references a user_id that exists in the JSON_Store, THE Backend SHALL extract the user identity, attach it to the request context, and forward the request to the endpoint handler
2. IF a request to a protected endpoint includes a JWT cookie that is expired (issued more than 24 hours ago), has a tampered or unverifiable signature, or is malformed, THEN THE Backend SHALL return a 401 unauthorized error with a message indicating authentication failure
3. IF a request to a protected endpoint does not include a JWT cookie, THEN THE Backend SHALL return a 401 unauthorized error with a message indicating authentication is required
4. WHEN a GET request is made to /api/auth/me with a valid JWT cookie, THE Auth_Service SHALL return the current User's id, email, username, and created_at fields
5. IF a request to a protected endpoint includes a JWT cookie with a valid signature that references a user_id that does not exist in the JSON_Store, THEN THE Backend SHALL return a 401 unauthorized error with a message indicating authentication failure

### Requirement 5: Create Todo

**User Story:** As an authenticated user, I want to create a new todo item, so that I can track tasks I need to complete.

#### Acceptance Criteria

1. WHEN a create todo request is received with a title, THE Todo_Service SHALL create a Todo record with a unique id, the authenticated user's id, the provided title, and a created_at timestamp
2. WHEN a create todo request includes optional fields (description, priority, due_date, status), THE Todo_Service SHALL validate that priority is one of "low", "medium", or "high", that status is one of "pending", "in-progress", or "done", and store the valid values in the Todo record
3. WHEN a create todo request does not specify a priority, THE Todo_Service SHALL default the priority to "medium"
4. WHEN a create todo request does not specify a status, THE Todo_Service SHALL default the status to "pending"
5. IF a create todo request has a missing, empty, or whitespace-only title, or a title exceeding 200 characters, THEN THE Todo_Service SHALL return a 422 validation error indicating the title is invalid
6. WHEN a todo is successfully created, THE Todo_Service SHALL return the complete Todo record with a 201 status code
7. IF a create todo request includes a priority value that is not one of "low", "medium", or "high", or a status value that is not one of "pending", "in-progress", or "done", THEN THE Todo_Service SHALL return a 422 validation error indicating the invalid field
8. IF a create todo request includes a description exceeding 2000 characters, THEN THE Todo_Service SHALL return a 422 validation error indicating the description is too long

### Requirement 6: Read Todos

**User Story:** As an authenticated user, I want to view my todo items with filtering and sorting options, so that I can find and organize my tasks efficiently.

#### Acceptance Criteria

1. WHEN a GET request is made to /api/todos, THE Todo_Service SHALL return only the todos belonging to the authenticated user
2. WHEN a GET request includes a status query parameter with a valid value (pending, in-progress, or done), THE Todo_Service SHALL return only todos matching that status value
3. WHEN a GET request includes a priority query parameter with a valid value (low, medium, or high), THE Todo_Service SHALL return only todos matching that priority value
4. WHEN a GET request includes a sort_by query parameter with value "due_date", THE Todo_Service SHALL return todos sorted by due_date in ascending order, with todos having no due_date placed last
5. WHEN a GET request includes a sort_by query parameter with value "created_at", THE Todo_Service SHALL return todos sorted by created_at in descending order
6. WHEN a GET request is made to /api/todos/{id}, THE Todo_Service SHALL return the specific todo if it belongs to the authenticated user
7. IF a GET request is made to /api/todos/{id} for a todo that does not belong to the authenticated user, THEN THE Todo_Service SHALL return a 404 not found error
8. IF a GET request is made to /api/todos/{id} for a todo id that does not exist in the JSON_Store, THEN THE Todo_Service SHALL return a 404 not found error
9. IF a GET request includes a status, priority, or sort_by query parameter with a value not in the allowed set, THEN THE Todo_Service SHALL return a 422 validation error indicating the invalid parameter value

### Requirement 7: Update Todo

**User Story:** As an authenticated user, I want to update my todo items, so that I can modify task details as they change.

#### Acceptance Criteria

1. WHEN a PUT request is made to /api/todos/{id} with one or more updatable fields (title, description, priority, due_date, status), THE Todo_Service SHALL update only the provided fields and set the updated_at timestamp to the current time
2. WHEN a todo is successfully updated, THE Todo_Service SHALL return the complete updated Todo record
3. IF a PUT request is made to /api/todos/{id} for a todo that does not belong to the authenticated user, THEN THE Todo_Service SHALL return a 404 not found error
4. IF a PUT request is made to /api/todos/{id} for a todo that does not exist, THEN THE Todo_Service SHALL return a 404 not found error
5. IF a PUT request includes a priority value that is not one of: low, medium, or high, THEN THE Todo_Service SHALL return a 422 validation error indicating the invalid priority value
6. IF a PUT request includes a status value that is not one of: pending, in-progress, or done, THEN THE Todo_Service SHALL return a 422 validation error indicating the invalid status value
7. IF a PUT request includes a title field that is empty or contains only whitespace, THEN THE Todo_Service SHALL return a 422 validation error indicating that title must not be blank
8. IF a PUT request includes a due_date value that is not a valid ISO 8601 date string (YYYY-MM-DD), THEN THE Todo_Service SHALL return a 422 validation error indicating the invalid date format

### Requirement 8: Delete Todo

**User Story:** As an authenticated user, I want to delete a todo item, so that I can remove tasks I no longer need.

#### Acceptance Criteria

1. WHEN a DELETE request is made to /api/todos/{id} for a todo belonging to the authenticated user, THE Todo_Service SHALL remove the todo from the JSON_Store
2. WHEN a todo is successfully deleted, THE Todo_Service SHALL return a 204 no content response
3. IF a DELETE request is made to /api/todos/{id} for a todo that does not belong to the authenticated user, THEN THE Todo_Service SHALL return a 404 not found error
4. IF a DELETE request is made to /api/todos/{id} for a todo that does not exist, THEN THE Todo_Service SHALL return a 404 not found error

### Requirement 9: Dashboard Statistics

**User Story:** As an authenticated user, I want to see a summary of my todo statistics on the dashboard, so that I can quickly understand my task progress.

#### Acceptance Criteria

1. THE Dashboard SHALL display the total count of todos belonging to the authenticated user
2. THE Dashboard SHALL display the count of todos with status "done" as completed count
3. THE Dashboard SHALL display the count of todos with status "pending" or "in-progress" as pending count
4. THE Dashboard SHALL display the count of todos with a due_date earlier than the current server date and status not equal to "done" as overdue count
5. THE Dashboard SHALL display filtering controls that allow the user to filter the todo list by status (pending, in-progress, done) and by priority (low, medium, high)
6. THE Dashboard SHALL display sorting controls that allow the user to sort the todo list by due_date in ascending order or by created_at in descending order
7. WHEN a todo is created, updated, or deleted, THE Dashboard SHALL refresh the displayed statistics counts and the todo list to reflect the current data

### Requirement 10: Frontend Authentication Flow

**User Story:** As a user, I want a seamless authentication experience with proper routing guards, so that I am directed to the appropriate pages based on my authentication state.

#### Acceptance Criteria

1. WHILE a user is not authenticated (no valid JWT cookie present), THE Frontend SHALL redirect requests to protected pages (dashboard, todos) to the login page within 1 second of navigation
2. WHILE a user is authenticated (valid JWT cookie present), THE Frontend SHALL redirect requests to the login and register pages to the dashboard within 1 second of navigation
3. WHEN the user attempts to submit a registration or login form with invalid input, THE Frontend SHALL display validation error messages adjacent to the corresponding form fields indicating the specific validation failure (e.g., required field empty, email format invalid, password below 8 characters, password confirmation mismatch) and SHALL prevent form submission to the Backend
4. WHEN a registration or login form is submitted, THE Frontend SHALL disable the submit button and display a loading indicator until the Backend responds or 15 seconds elapse, whichever comes first
5. IF the Backend does not respond within 15 seconds after form submission, THEN THE Frontend SHALL re-enable the submit button and display an error message indicating the request timed out
6. IF the Backend returns an error response (401, 409, or 422) after form submission, THEN THE Frontend SHALL display the error message from the response adjacent to the relevant form field or at the top of the form and SHALL re-enable the submit button

### Requirement 11: UI Design and Responsiveness

**User Story:** As a user, I want a modern, visually appealing interface that works on all devices, so that I have a pleasant experience using the application.

#### Acceptance Criteria

1. THE Frontend SHALL use an indigo/violet primary color palette with neutral gray secondary colors
2. THE Frontend SHALL implement a responsive layout that adapts to mobile (below 768px), tablet (768px to 1023px), and desktop (1024px and above) viewports such that all interactive elements remain visible and usable without horizontal scrolling
3. WHILE the viewport width is 1024px or above, THE Frontend SHALL display a split-screen layout on the login and register pages with a decorative side panel alongside the form
4. THE Frontend SHALL apply CSS transitions with a duration between 150ms and 300ms on hover states, page transitions, and component mount/unmount
5. WHILE data is being fetched from the Backend, THE Frontend SHALL display loading skeleton placeholders in place of the content areas that are loading
6. WHEN a success or error event occurs (todo created, updated, deleted, or a request error), THE Frontend SHALL display a toast notification that automatically dismisses after 5 seconds or can be manually dismissed by the user
7. IF no todos exist for the authenticated user, THEN THE Frontend SHALL display an empty state illustration with text indicating that no todos have been created and guiding the user to create one
8. THE Frontend SHALL include a dark mode toggle that persists the user's preference in local storage and defaults to the light theme when no preference is stored

### Requirement 12: Todo Interaction Patterns

**User Story:** As a user, I want intuitive interaction patterns for managing todos, so that I can efficiently create, edit, and delete tasks.

#### Acceptance Criteria

1. WHEN the user clicks a todo item's editable field (title or status), THE Frontend SHALL enable inline editing for that field with a save action on Enter key or blur and a cancel action on Escape key
2. WHEN the user clicks an edit button on a todo item, THE Frontend SHALL display a full edit modal with all todo fields (title, description, priority, due_date, status) pre-populated with the current values
3. WHEN the user clicks a delete button on a todo item, THE Frontend SHALL display a confirmation dialog before sending the delete request
4. WHEN the user confirms deletion in the confirmation dialog, THE Frontend SHALL send the delete request and remove the todo from the list with an exit animation of no more than 300ms
5. WHEN the user clicks cancel in the confirmation dialog, THE Frontend SHALL close the dialog without sending a delete request

### Requirement 13: CORS and Development Configuration

**User Story:** As a developer, I want proper CORS configuration and development tooling, so that the frontend and backend can communicate during local development.

#### Acceptance Criteria

1. THE Backend SHALL configure CORS to allow requests from the Frontend development server origin (http://localhost:3000) and allow the HTTP methods GET, POST, PUT, and DELETE
2. THE Backend SHALL allow credentials (cookies) in CORS configuration and allow the Content-Type header in CORS requests
3. THE project SHALL include a README.md file containing at minimum: prerequisites (Python, Node.js versions), Backend setup steps (install dependencies, start server), Frontend setup steps (install dependencies, start server), and the URL where each server runs
4. THE project SHALL include a run.sh script that starts both the Backend and Frontend servers
5. IF the Frontend makes a preflight (OPTIONS) request to the Backend, THEN THE Backend SHALL respond with the appropriate CORS headers and a 200 status code

### Requirement 14: Data Persistence and Integrity

**User Story:** As a user, I want my data to be reliably stored and retrieved, so that I do not lose my todos or account information.

#### Acceptance Criteria

1. THE JSON_Store SHALL persist User records to a users.json file in the /backend/data directory
2. THE JSON_Store SHALL persist Todo records to a todos.json file in the /backend/data directory
3. WHEN the JSON_Store reads a file that does not exist, THE JSON_Store SHALL create the file with an empty array
4. THE JSON_Store SHALL ensure each User has a unique id and unique email and unique username
5. THE JSON_Store SHALL ensure each Todo has a unique id
6. FOR ALL valid Todo objects, serializing to JSON and deserializing back SHALL produce an equivalent Todo object (round-trip property)
7. FOR ALL valid User objects (excluding password_hash verification), serializing to JSON and deserializing back SHALL produce an equivalent User object (round-trip property)
8. WHEN a write operation to the JSON_Store fails (e.g., file system error), THE Backend SHALL return a 500 internal server error and SHALL NOT leave the JSON file in a corrupted state
