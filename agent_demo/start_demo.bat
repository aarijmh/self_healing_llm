@echo off
echo ========================================
echo SecureBank AI Agent - Demo Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "..\\.venv\\Scripts\\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please create a virtual environment first.
    pause
    exit /b 1
)

echo [1/3] Activating virtual environment...
call "..\\.venv\\Scripts\\activate.bat"

echo [2/3] Starting backend server...
start "Backend Server" cmd /k "cd backend && python app.py"

echo [3/3] Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo [4/4] Starting frontend server...
start "Frontend Server" cmd /k "cd frontend && python -m http.server 8000"

echo.
echo ========================================
echo Demo servers are starting!
echo ========================================
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:8000
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak > nul

start http://localhost:8000

echo.
echo Press any key to stop all servers...
pause > nul

echo Stopping servers...
taskkill /FI "WindowTitle eq Backend Server*" /T /F > nul 2>&1
taskkill /FI "WindowTitle eq Frontend Server*" /T /F > nul 2>&1

echo.
echo Demo stopped. Goodbye!
