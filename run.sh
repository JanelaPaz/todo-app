#!/bin/bash

# Full-Stack Todo App - Start Script
# Starts both backend (FastAPI/uvicorn) and frontend (Nuxt 3) servers

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Full-Stack Todo Application...${NC}"
echo ""

# Store the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

# Start backend server
echo -e "${YELLOW}[Backend]${NC} Starting uvicorn on http://localhost:8000..."
cd "$PROJECT_ROOT/backend"
uvicorn main:app --reload &
BACKEND_PID=$!

# Start frontend server
echo -e "${YELLOW}[Frontend]${NC} Starting Nuxt dev server on http://localhost:3000..."
cd "$PROJECT_ROOT/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}Both servers are running:${NC}"
echo -e "  Backend:  http://localhost:8000"
echo -e "  Frontend: http://localhost:3000"
echo ""
echo -e "Press Ctrl+C to stop both servers."

# Trap Ctrl+C to kill both processes
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID 2>/dev/null
    wait $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}Servers stopped.${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
