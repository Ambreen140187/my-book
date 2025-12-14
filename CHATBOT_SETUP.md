# AI Native Book - Floating Chatbot Setup

## Overview
The floating chatbot is already implemented and integrated into the Docusaurus website. It appears as a floating button in the bottom-right corner that expands into a full chat interface when clicked.

## Features
- Floating chat icon visible on all pages
- Chat window with message history
- Integration with backend RAG system
- Source citations for responses
- Selected text context support
- Dark/light mode support

## Backend Setup (API)

### Environment Variables
Create a `.env` file in the `backend/` directory:
```bash
COHERE_API_KEY=your_cohere_api_key_here
FRONTEND_URL=http://localhost:3000  # For development
# FRONTEND_URL=https://yourdomain.com  # For production
```

### Running the Backend
```bash
cd backend
pip install -r requirements.txt
python populate_db.py  # To populate the vector database
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## Frontend Setup (Docusaurus)

### Environment Variables
Create a `.env` file in the `ai-native-book-website/` directory:
```bash
REACT_APP_API_BASE_URL=http://localhost:8000  # For development
# REACT_APP_API_BASE_URL=https://your-backend-domain.com  # For production
```

### Running the Frontend
```bash
cd ai-native-book-website
npm install
npm start
```

The website will be available at `http://localhost:3000`

## Configuration Files

### API Configuration
The frontend uses `src/components/ChatBot/config.js` to manage API endpoints:
```javascript
const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
  ENDPOINTS: {
    ASK: '/ask',
    HEALTH: '/health'
  },
  TIMEOUT: 30000
};
```

### Docusaurus Integration
The chatbot is integrated into the entire Docusaurus site via:
- `src/components/RootWrapper/RootWrapper.jsx` - Injects the chatbot component
- `docusaurus.config.ts` - Uses a plugin to load the RootWrapper

## Security Notes
- API keys are loaded from environment variables, not hardcoded
- CORS is configured to allow only specified origins
- No sensitive information is exposed in frontend code

## Production Deployment
1. Set appropriate environment variables for your production environment
2. Update `FRONTEND_URL` to your production domain
3. Update `REACT_APP_API_BASE_URL` to your backend API domain
4. Ensure SSL/TLS is configured for both frontend and backend