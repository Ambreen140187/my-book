# AI Native Book - Floating Chatbot

## Overview
A floating chatbot is integrated into the Docusaurus website that allows users to chat about the book content. The chatbot appears as a floating icon in the bottom-right corner of all pages.

## Features
- Floating chat icon visible on all pages
- Expandable chat window with message history
- Integration with RAG (Retrieval Augmented Generation) backend
- Source citations for AI responses
- Selected text context support
- Dark/light mode support

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm/yarn

## Setup Instructions

### 1. Backend Setup (API Server)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables by creating a `.env` file in the `backend/` directory:
   ```
   COHERE_API_KEY=GlCohKRVje9RSSIrxlMK9DwRNZBiiiY6ojvlmICn
   FRONTEND_URL=http://localhost:3000
   ```

4. Populate the vector database with book content:
   ```bash
   python populate_db.py
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### 2. Frontend Setup (Docusaurus Website)

1. Navigate to the website directory:
   ```bash
   cd ai-native-book-website
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables by creating a `.env` file in the `ai-native-book-website/` directory:
   ```
   REACT_APP_API_BASE_URL=http://localhost:8000
   ```

4. Start the Docusaurus development server:
   ```bash
   npm start
   ```

## Quick Start

Alternatively, you can use the provided batch script to start the backend:

1. Run the batch script:
   ```bash
   start_chatbot.bat
   ```

2. In a separate terminal, start the frontend:
   ```bash
   cd ai-native-book-website
   npm install && npm start
   ```

## Architecture

### Frontend Components
- `src/components/ChatBot/ChatBot.jsx` - Main React component with state management and UI
- `src/components/ChatBot/ChatBot.css` - Complete styling for the floating interface
- `src/components/RootWrapper/RootWrapper.jsx` - Docusaurus Root component that renders the chatbot globally

### Backend API
- `backend/main.py` - FastAPI server handling `/ask` endpoint
- Uses Cohere for AI responses and Qdrant for vector database
- Implements RAG (Retrieval Augmented Generation) for book content

### Docusaurus Integration
- Configured in `docusaurus.config.ts` with a plugin that loads the RootWrapper
- The chatbot is automatically injected into all pages via the RootWrapper

## How It Works

1. The floating chat icon appears on all pages in the bottom-right corner
2. When clicked, it expands into a full chat interface
3. User messages are sent to the backend API at `/ask`
4. The backend retrieves relevant book content from the vector database
5. Cohere generates responses based on the retrieved content
6. Responses are returned with source citations and displayed in the chat

## Security Notes

- API keys are loaded from environment variables, not hardcoded
- CORS is configured to allow only specified origins
- No sensitive information is exposed in frontend code
- The system is ready for production deployment with proper environment configuration

## Production Deployment

For production deployment:
1. Update `FRONTEND_URL` to your production domain in backend `.env`
2. Update `REACT_APP_API_BASE_URL` to your backend API domain in frontend `.env`
3. Ensure SSL/TLS is configured for both frontend and backend
4. Use secure methods to manage secrets in your deployment environment