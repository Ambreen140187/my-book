# RAG (Retrieval-Augmented Generation) Configuration

This document explains the RAG system for Question Answering with Qdrant vector database.

## System Overview

The RAG system combines vector search with AI generation to provide accurate answers based on book content:

1. **Retrieval**: User questions are converted to embeddings and searched against Qdrant vector database
2. **Augmentation**: Relevant content chunks are retrieved from the vector database
3. **Generation**: AI model generates answers based on the retrieved content

## Qdrant Vector Database Configuration

- **Collection Name**: `book_content`
- **Vector Size**: 1024 dimensions
- **Distance Function**: Cosine similarity
- **Embedding Model**: Cohere `embed-english-v3.0`
- **Input Type**: `search_document` for content, `search_query` for questions

## Data Processing Pipeline

### 1. Document Ingestion
- Book content is loaded from `.mdx` and `.md` files
- Content is cleaned and split into chunks (500-800 tokens each)
- Chunks are embedded using Cohere embeddings
- Embedded chunks are stored in Qdrant with metadata (source, page, content)

### 2. Query Processing
- User questions are embedded using Cohere
- Vector search finds top-k most similar chunks (default k=5)
- Retrieved chunks are used as context for AI generation

## RAG Prompt Configuration

### Core Principles
1. **Information Fidelity**: AI only uses provided context
2. **Uncertainty Handling**: AI explicitly says "I don't know" when information is missing
3. **Transparency**: AI indicates what information is available vs. missing

### Prompt Structure

#### For Selected Text Queries:
```
Based on the selected text below, please answer the user's question. Only use information from the provided text.

Selected Text:
{context}

Question: {request.question}

Instructions:
1. Answer only based on the provided text
2. If the answer is not in the provided text, clearly state "I don't know" or "The provided text does not contain information to answer this question"
3. Be concise and accurate
4. If you can partially answer, clearly indicate what information is available and what is missing
```

#### For General Book Content Queries:
```
Based on the following book content, please answer the user's question. Only use information from the provided content.

Book Content:
{context}

Question: {request.question}

Instructions:
1. Answer only based on the provided book content
2. If the information needed to answer the question is not in the provided content, clearly state "I don't know" or "The provided content does not contain information to answer this question"
3. Be comprehensive but only use the provided information
4. If you can partially answer, clearly indicate what information is available and what is missing
```

## Response Handling

### Success Responses
- AI generates answer based on provided context
- Sources are returned with relevance scores
- Page/chapter references are provided

### Uncertainty Responses
When the answer is not in the provided data, the AI will respond with:
- "I don't know"
- "The provided content does not contain information to answer this question"
- Clear indication of what information is missing

## Quality Assurance

### Content Quality
- Book content is chunked to maintain semantic coherence
- Frontmatter is removed from documents
- Text cleaning removes special characters that might interfere with processing

### Search Quality
- Cosine similarity ensures semantically relevant results
- Top-k search (default k=5) provides sufficient context
- Relevance scores are returned for transparency

### Response Quality
- Temperature setting (0.3) balances creativity and accuracy
- Max tokens (500) ensures comprehensive but concise responses
- Explicit instructions prevent hallucination of information

## Configuration Parameters

- **top_k**: Number of relevant chunks to retrieve (default: 5)
- **max_tokens**: Maximum chunk size for vectorization (default: 600)
- **temperature**: AI response creativity (default: 0.3)
- **max_tokens**: Maximum response length (default: 500)

## Error Handling

- Empty search results return appropriate "I don't know" response
- API errors are caught and return user-friendly error messages
- Network issues are handled gracefully in the frontend