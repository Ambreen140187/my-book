@echo off
echo Starting AI Native Book RAG Chatbot with Floating UI...
echo.

echo Setting up backend...
cd backend
echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Populating vector database...
python populate_db.py
echo.

echo Starting API server on port 8000...
start cmd /k "cd /d %~dp0\backend && echo Starting backend server... && python -c \"import os; print('COHERE_API_KEY is configured') if os.getenv('COHERE_API_KEY') else print('Warning: COHERE_API_KEY not found')\" && uvicorn main:app --host 0.0.0.0 --port 8000"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo To start the Docusaurus website:
echo 1. Open a new terminal
echo 2. Navigate to ai-native-book-website directory
echo 3. Run: npm install && npm start
echo.
echo The API will be available at http://localhost:8000
echo The chatbot will be integrated into the Docusaurus website at http://localhost:3000
echo.
echo The floating chatbot icon should appear on all pages in the bottom-right corner.