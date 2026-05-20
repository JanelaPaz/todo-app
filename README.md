# Full-Stack Todo Application

A full-stack Todo application with user authentication, full CRUD operations, filtering/sorting, and a responsive dashboard UI.

- **Backend**: Python FastAPI with JSON file-based storage and JWT authentication
- **Frontend**: Nuxt 3 with TailwindCSS and Pinia state management

## Prerequisites

- **Python** 3.11 or higher
- **Node.js** 18 or higher
- **npm** (comes with Node.js)

## Backend Setup

```cmd
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload
```

The backend API runs at **http://localhost:8000**.

## Frontend Setup

```cmd
cd frontend

# Install dependencies
npm install

# Start the frontend dev server
npm run dev
```

The frontend runs at **http://localhost:3000**.

## Running Both Servers

You can start both servers at once using the provided script:

**Windows:**
```cmd
run.bat
```

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

This opens separate terminal windows for the backend and frontend servers.

## Project Structure

```
todo-app/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Pydantic data models
│   ├── store.py             # JSON file persistence layer
│   ├── dependencies.py      # Auth dependency (JWT extraction)
│   ├── exceptions.py        # Custom exception classes and handlers
│   ├── requirements.txt     # Python dependencies
│   ├── data/                # JSON data files (users.json, todos.json)
│   ├── routers/             # API route handlers
│   │   ├── auth.py          # Auth endpoints (/api/auth/*)
│   │   └── todos.py         # Todo endpoints (/api/todos/*)
│   └── services/            # Business logic
│       ├── auth_service.py  # Authentication service
│       └── todo_service.py  # Todo CRUD service
├── frontend/
│   ├── pages/               # Nuxt pages (login, register, dashboard)
│   ├── components/          # Vue components
│   ├── composables/         # Composable functions
│   ├── stores/              # Pinia stores (auth, todos)
│   ├── middleware/          # Route guards
│   ├── nuxt.config.ts       # Nuxt configuration
│   └── package.json         # Node.js dependencies
├── README.md
├── run.bat                  # Windows script to start both servers
└── run.sh                   # Linux/macOS script to start both servers
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Log in with email/username and password |
| POST | `/api/auth/logout` | Log out (clears cookie) |
| GET | `/api/auth/me` | Get current user info |

### Todos

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos` | List todos (supports `status`, `priority`, `sort_by` query params) |
| POST | `/api/todos` | Create a new todo |
| GET | `/api/todos/{id}` | Get a specific todo |
| PUT | `/api/todos/{id}` | Update a todo |
| DELETE | `/api/todos/{id}` | Delete a todo |
