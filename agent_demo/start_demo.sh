#!/bin/bash

echo "========================================"
echo "SecureBank AI Agent - Demo Launcher"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -f "../.venv/bin/activate" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please create a virtual environment first."
    exit 1
fi

echo "[1/3] Activating virtual environment..."
source ../.venv/bin/activate

echo "[2/3] Starting backend server..."
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

echo "[3/3] Waiting for backend to start..."
sleep 5

echo "[4/4] Starting frontend server..."
cd frontend
python3 -m http.server 8000 &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "Demo servers are running!"
echo "========================================"
echo ""
echo "Backend API: http://localhost:5000"
echo "Frontend UI: http://localhost:8000"
echo ""
echo "Opening browser..."
sleep 2

# Try to open browser (works on most Linux/Mac systems)
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8000
elif command -v open > /dev/null; then
    open http://localhost:8000
else
    echo "Please open http://localhost:8000 in your browser"
fi

echo ""
echo "Press Ctrl+C to stop all servers..."

# Trap Ctrl+C and cleanup
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Demo stopped. Goodbye!'; exit 0" INT

# Wait indefinitely
wait
