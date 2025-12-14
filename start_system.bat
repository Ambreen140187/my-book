@echo off
echo Starting AI Native Book RAG Chatbot...
echo.

echo Setting up backend...
cd backend
echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Populating vector database...
python populate_db.py
echo.

echo Starting API server...
echo Please ensure you have set the COHERE_API_KEY environment variable
echo Or create a .env file in the backend directory with your API key
start cmd /k "cd /d %~dp0\backend && python -c \"import os; from main import COHERE_API_KEY; print('Starting server...')\" && uvicorn main:app --host 0.0.0.0 --port 8000"

echo.
echo To start the Docusaurus website:
echo 1. Open a new terminal
echo 2. Navigate to ai-native-book-website directory
echo 3. Run: npm install && npm start
echo.
echo The API will be available at http://localhost:8000
echo The chatbot will be integrated into the Docusaurus website at http://localhost:3000