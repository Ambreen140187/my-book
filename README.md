# 🚀 AI Native Book RAG Chatbot

A Retrieval-Augmented Generation (RAG) Chatbot for the AI Native Book website that allows users to ask questions about the book content and get AI-powered answers based on the book's content.

## 📋 Features

- **Question Answering**: Ask questions about the AI Native Book content
- **Selected Text Focus**: If text is selected on the page, answers are generated based only on that selected text
- **Multi-turn Conversations**: Support for follow-up questions
- **Source Highlighting**: Shows which book chapters/pages were used to generate answers
- **Vector Search**: Uses Qdrant vector database for semantic search
- **Cohere AI**: Leverages Cohere's powerful language models for natural responses

## 🛠️ Architecture

### Backend
- **FastAPI**: Web framework for the API endpoints
- **Qdrant**: Vector database for storing and searching book content embeddings
- **Cohere**: AI model for generating natural language responses
- **Embeddings**: Text embeddings for semantic search

### Frontend
- **React**: Chat widget component
- **Docusaurus Integration**: Seamless integration with the book website
- **Dark/Light Mode**: Automatic theme matching with the website

## 🚀 Quick Start

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Populate Vector Database

```bash
cd backend
python populate_db.py
```

This will:
- Load all book content from `../ai-native-book-website/book/`
- Split content into chunks (500-800 tokens each)
- Generate embeddings using Cohere
- Store in Qdrant Cloud

### 3. Start the Backend Server

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Run the Docusaurus Website

```bash
cd ai-native-book-website
npm install
npm start
```

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI application with /ask endpoint
├── vector_db_setup.py      # Qdrant setup and document processing
├── populate_db.py          # Script to populate the vector database
├── test_api.py             # API testing script
└── requirements.txt        # Python dependencies

ai-native-book-website/
├── src/
│   └── components/
│       └── ChatBot/        # React chat widget
└── docusaurus.config.ts    # Docusaurus config with chatbot integration
```

## 🔧 API Endpoints

### `POST /ask`

Ask a question about the book content.

**Request Body:**
```json
{
  "question": "Your question here",
  "selected_text": "Optional selected text to focus on",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "AI-generated answer",
  "sources": [
    {
      "content": "Relevant text snippet",
      "source": "Source file",
      "page": "Page/chunk info",
      "relevance_score": 0.95
    }
  ],
  "selected_text_used": false
}
```

## 🤖 How It Works

1. **Indexing**: Book content is split into chunks and stored in Qdrant with embeddings
2. **Query Processing**: When a question is asked, it's embedded using Cohere
3. **Semantic Search**: Qdrant finds the most relevant content chunks
4. **Answer Generation**: Cohere generates a response based on the relevant content
5. **Response**: Answer is returned with source information

## 🧪 Testing

Run the test script to verify the API:

```bash
cd backend
python test_api.py
```

## 📚 Customization

### Adding New Book Content
1. Add new `.mdx` files to `ai-native-book-website/book/`
2. Re-run `python populate_db.py` to update the vector database

### Adjusting Chunk Size
Modify the `split_document_into_chunks` function in `vector_db_setup.py` to change the token size (default: 600 tokens per chunk)

### Changing AI Model
Update the model name in `main.py` (currently using `command-r-08-2024`)

## 🚨 Troubleshooting

- **API Keys**: Ensure your Cohere API key and Qdrant credentials are valid
- **Server Not Starting**: Check that port 8000 is available
- **Empty Results**: Verify that the database was populated successfully
- **Cohere Model Issues**: Check the Cohere documentation for current model names

## 🛡️ Security

- API keys are hardcoded for demonstration purposes
- In production, use environment variables for sensitive credentials
- CORS is configured to allow all origins (update for production)

## 📈 Future Enhancements

- Conversation history persistence
- User authentication
- Advanced search filters
- Performance monitoring
- Caching layer