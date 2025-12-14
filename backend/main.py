from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import cohere
import logging
import asyncio
import os
from vector_db_setup import search_relevant_chunks

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Native Book RAG Chatbot",
              description="Retrieval-Augmented Generation Chatbot for AI Native Book",
              version="1.0.0")

# Add CORS middleware to allow requests from frontend
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")  # Default for development

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # Only allow specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Cohere client with environment variable
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "GlCohKRVje9RSSIrxlMK9DwRNZBiiiY6ojvlmICn")  # Using provided key as default

co = cohere.Client(api_key=COHERE_API_KEY)

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
    return {"message": "AI Native Book RAG Chatbot API", "status": "running"}

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Main endpoint to answer questions based on book content.

    If selected_text is provided, only use that text for answering.
    Otherwise, retrieve relevant chunks from the vector database.
    """
    try:
        logger.info(f"Received question: {request.question[:50]}...")

        selected_text_used = False

        if request.selected_text:
            # If user has selected specific text, use only that for context
            context_chunks = [{"content": request.selected_text, "source": "user_selection", "score": 1.0, "page": "selected"}]
            selected_text_used = True
            logger.info("Using user-selected text for context")
        else:
            # Retrieve relevant chunks from the vector database
            logger.info("Searching vector database for relevant content...")
            context_chunks = search_relevant_chunks(request.question, top_k=request.top_k)

            if not context_chunks:
                logger.warning("No relevant content found in vector database")
                return AnswerResponse(
                    answer="I couldn't find relevant information in the book to answer your question.",
                    sources=[],
                    selected_text_used=False
                )

        # Combine the context chunks into a single context string
        context_parts = []
        sources = []

        for chunk in context_chunks:
            context_parts.append(chunk['content'])
            sources.append({
                "content": chunk['content'][:200] + "..." if len(chunk['content']) > 200 else chunk['content'],  # Truncate for display
                "source": chunk['source'],
                "page": chunk['page'],
                "relevance_score": chunk['score'] if 'score' in chunk else 1.0
            })

        context = "\n\n".join(context_parts)

        # Construct the prompt for the Cohere model
        if selected_text_used:
            prompt = f"""Based on the selected text below, please answer the user's question. Only use information from the provided text.

Selected Text:
{context}

Question: {request.question}

Answer concisely and accurately based on the provided text."""
        else:
            prompt = f"""Based on the following book content, please answer the user's question. Only use information from the provided content.

Book Content:
{context}

Question: {request.question}

Provide a comprehensive answer based on the book content. If the information is not available in the provided content, say so clearly."""

        logger.info("Sending request to Cohere model...")

        # Generate response using Cohere
        response = co.chat(
            message=prompt,
            model="command-r-08-2024",  # Updated to current model version
            temperature=0.3,
            max_tokens=500
        )

        answer = response.text

        logger.info("Successfully generated answer")

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
    return {"status": "healthy", "service": "RAG Chatbot API"}

@app.on_event("startup")
async def startup_event():
    """Initialize the vector database on startup if needed"""
    logger.info("Starting up RAG Chatbot API...")
    # Optionally initialize vector DB here if needed
    # await initialize_vector_database("../../ai-native-book-website/book")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)