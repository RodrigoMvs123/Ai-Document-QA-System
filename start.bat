@echo off
echo ========================================
echo AI Document QA System - Quick Start
echo ========================================
echo.
echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: Open frontend/index.html in your browser
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

python -m uvicorn generativeai:app --reload --host 0.0.0.0 --port 8000
