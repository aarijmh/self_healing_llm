#!/usr/bin/env python3
"""Runner script for Agent Directory Demo"""
import subprocess
import sys
import os

def activate_venv_and_run():
    """Activate virtual environment and run the demo"""
    venv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.venv')
    
    if os.name == 'nt':  # Windows
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
    else:  # Unix/Linux/macOS
        python_path = os.path.join(venv_path, 'bin', 'python')
    
    if not os.path.exists(python_path):
        print(f"Virtual environment not found at {venv_path}")
        print("Please create virtual environment first:")
        print("python -m venv .venv")
        print("source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows")
        print("pip install -r requirements.txt")
        return
    
    # Run the demo with the virtual environment Python
    demo_script = os.path.join(os.path.dirname(__file__), 'agent_directory_demo.py')
    subprocess.run([python_path, demo_script])

if __name__ == "__main__":
    activate_venv_and_run()