# 🚀 Quick Start Guide

## For Windows Users

### Step 1: Open Terminal
Open PowerShell or Command Prompt in the `agent_demo` folder

### Step 2: Activate Environment
```bash
..\.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
cd backend
pip3 install -r requirements.txt
cd ..
```

### Step 4: Run Demo
```bash
.\start_demo.bat
```

### Step 5: Access Demo
Browser will open automatically to: **http://localhost:8000**

---

## For Linux/Mac Users

### Step 1: Open Terminal
Navigate to the `agent_demo` folder

### Step 2: Activate Environment
```bash
source ../.venv/bin/activate
```

### Step 3: Install Dependencies
```bash
cd backend
pip3 install -r requirements.txt
cd ..
```

### Step 4: Make Script Executable
```bash
chmod +x start_demo.sh
```

### Step 5: Run Demo
```bash
./start_demo.sh
```

### Step 6: Access Demo
Open browser to: **http://localhost:8000**

---

## Manual Start (If Scripts Don't Work)

### Terminal 1 - Backend:
```bash
..\.venv\Scripts\activate  # Windows
source ../.venv/bin/activate  # Linux/Mac

cd backend
python app.py
```

### Terminal 2 - Frontend:
```bash
cd frontend
python -m http.server 8000
```

### Browser:
Open **http://localhost:8000**

---

## Demo Controls

1. **Setup & Registration** - Initialize the agent
2. **Delegate Authority** - Grant shopping permissions
3. **Execute Purchase** - Complete a purchase flow
4. **Run Complete Demo** - All steps automatically

---

## Troubleshooting

### "Module not found" error
```bash
pip3 install -r backend/requirements.txt
```

### Port already in use
Change ports in:
- `backend/app.py` (line with `port=5000`)
- `frontend/app.js` (line with `API_URL`)

### WebSocket connection failed
1. Ensure backend is running
2. Check browser console for errors
3. Try different browser

---

## Stop Demo

**Windows:** Press any key in the startup window

**Linux/Mac:** Press `Ctrl+C` in the terminal

---

## Need Help?

Check the full **README.md** for detailed documentation.
