from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Native Book Test Chatbot",
              description="Test version without external dependencies",
              version="1.0.0")

# Add CORS middleware
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None
    top_k: Optional[int] = 5

class AnswerResponse(BaseModel):
    answer: str
    sources: List[dict]
    selected_text_used: bool

@app.get("/")
async def root():
    return {"message": "AI Native Book Test Chatbot API", "status": "running"}

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Test endpoint that returns a mock response without external dependencies.
    """
    try:
        logger.info(f"Received question: {request.question[:50]}...")

        selected_text_used = False

        if request.selected_text:
            selected_text_used = True
            answer = f"I received your selected text and question: '{request.question}'. This is a test response from the mock API."
            sources = [{"content": request.selected_text[:200] + "...", "source": "user_selection", "page": "selected", "relevance_score": 1.0}]
        else:
            answer = f"This is a test response for your question: '{request.question}'. The actual API would connect to Cohere and Qdrant for real responses."
            sources = [
                {"content": "This is mock content from the AI Native Book...", "source": "test_source.mdx", "page": "1", "relevance_score": 0.95},
                {"content": "More mock content for testing purposes...", "source": "test_source2.mdx", "page": "2", "relevance_score": 0.87}
            ]

        return AnswerResponse(
            answer=answer,
            sources=sources,
            selected_text_used=selected_text_used
        )

    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Test Chatbot API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)