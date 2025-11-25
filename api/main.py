"""
Vercel serverless function entrypoint for FastAPI
This file imports the FastAPI app from Backend/main.py
"""
import sys
import os

# Get the project root directory (one level up from api/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_path = os.path.join(project_root, 'Backend')

# Add Backend directory to Python path
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Also add project root for any other imports
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the FastAPI app from Backend/main.py
from main import app

# Vercel expects the app to be exported as 'app'
# This is already done by importing from main.py

