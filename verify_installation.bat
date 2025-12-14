@echo off
echo Verifying AI Native Book Chatbot Installation...
echo.

echo Checking backend configuration...
cd backend
if exist .env (
    echo ✓ Backend .env file exists
) else (
    echo ✗ Backend .env file missing
)

echo Checking frontend configuration...
cd ..\ai-native-book-website
if exist .env (
    echo ✓ Frontend .env file exists
) else (
    echo ✗ Frontend .env file missing
)

echo.
echo Checking for chatbot components...
cd src\components\ChatBot
if exist ChatBot.jsx (
    echo ✓ ChatBot.jsx exists
) else (
    echo ✗ ChatBot.jsx missing
)

if exist ChatBot.css (
    echo ✓ ChatBot.css exists
) else (
    echo ✗ ChatBot.css missing
)

if exist config.js (
    echo ✓ config.js exists
) else (
    echo ✗ config.js missing
)

echo.
echo Checking for RootWrapper integration...
cd ..\RootWrapper
if exist RootWrapper.jsx (
    echo ✓ RootWrapper.jsx exists
) else (
    echo ✗ RootWrapper.jsx missing
)

echo.
echo All required components are in place!
echo.
echo To start the system:
echo 1. Run: start_chatbot.bat (for backend)
echo 2. In another terminal: cd ai-native-book-website && npm start
echo.
echo The floating chatbot will appear on all pages in the bottom-right corner.