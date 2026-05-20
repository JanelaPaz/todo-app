@echo off
REM Full-Stack Todo App - Start Script (Windows)
REM Starts both backend (FastAPI/uvicorn) and frontend (Nuxt 3) servers

echo Starting Full-Stack Todo Application...
echo.

REM Store the project root directory
set PROJECT_ROOT=%~dp0

REM Start backend server
echo [Backend] Starting uvicorn on http://localhost:8000...
start "Todo Backend" cmd /c "cd /d %PROJECT_ROOT%backend && uvicorn main:app --reload"

REM Start frontend server
echo [Frontend] Starting Nuxt dev server on http://localhost:3000...
start "Todo Frontend" cmd /c "cd /d %PROJECT_ROOT%frontend && npm run dev"

echo.
echo Both servers are running:
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo.
echo Close the server windows to stop them, or press any key to exit this window.
pause >nul
