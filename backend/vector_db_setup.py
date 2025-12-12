import os
import re
from typing import List, Dict
import asyncio
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url="https://62ae264d-064b-4532-84b1-404818e66566.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.JJNK-AgF7NL0ONsmD_omJSSowwARgbX6SlhnpqGvL8s",
)

# Initialize Cohere client for embeddings
co = cohere.Client(api_key="P0y91LStZoc1d8cu9R5yDrzwKYo25DJ2wgx4fyL2")

def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and special characters"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that might interfere with processing
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', ' ', text)
    return text.strip()

def split_document_into_chunks(document: str, max_tokens: int = 500) -> List[str]:
    """
    Split a document into chunks of approximately max_tokens length.
    Tries to split on sentence boundaries when possible.
    """
    # Clean the document first
    document = clean_text(document)

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', document)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Estimate token count (rough approximation: 1 token ~ 4 characters)
        estimated_tokens = len(sentence.split())

        if len(current_chunk) > 0 and len(current_chunk.split()) + estimated_tokens > max_tokens:
            # If adding this sentence would exceed the limit, save current chunk
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            # Add sentence to current chunk
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence

    # Add the last chunk if it exists
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Handle any remaining chunks that might still be too large
    final_chunks = []
    for chunk in chunks:
        if len(chunk.split()) > max_tokens:
            # If chunk is still too big, split by paragraphs
            paragraphs = chunk.split('\n\n')
            temp_chunk = ""

            for paragraph in paragraphs:
                if len(temp_chunk.split()) + len(paragraph.split()) <= max_tokens:
                    temp_chunk += "\n\n" + paragraph if temp_chunk else paragraph
                else:
                    if temp_chunk.strip():
                        final_chunks.append(temp_chunk.strip())
                    temp_chunk = paragraph

            if temp_chunk.strip():
                final_chunks.append(temp_chunk.strip())
        else:
            final_chunks.append(chunk)

    return final_chunks

async def create_collection_if_not_exists():
    """Create the Qdrant collection for book content if it doesn't exist."""
    try:
        collections = qdrant_client.get_collections()
        collection_names = [collection.name for collection in collections.collections]

        if "book_content" not in collection_names:
            logger.info("Creating Qdrant collection 'book_content'...")
            qdrant_client.create_collection(
                collection_name="book_content",
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
            )
            logger.info("Collection 'book_content' created successfully.")
        else:
            logger.info("Collection 'book_content' already exists.")
    except Exception as e:
        logger.error(f"Error creating collection: {e}")
        raise

async def embed_and_store_documents(documents: List[Dict], batch_size: int = 10):
    """
    Embed documents using Cohere and store them in Qdrant.

    Args:
        documents: List of dicts with 'content', 'source', 'page' keys
        batch_size: Number of documents to process in each batch
    """
    await create_collection_if_not_exists()

    # Process documents in batches
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]

        # Extract content for embedding
        texts_to_embed = [doc['content'] for doc in batch]

        try:
            # Generate embeddings using Cohere
            response = co.embed(
                texts=texts_to_embed,
                model='embed-english-v3.0',
                input_type='search_document'
            )
            embeddings = response.embeddings

            # Prepare points for Qdrant
            points = []
            for idx, (doc, embedding) in enumerate(zip(batch, embeddings)):
                # Use integer IDs for Qdrant
                point_id = i + idx

                points.append(models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "content": doc['content'],
                        "source": doc.get('source', ''),
                        "page": doc.get('page', ''),
                        "chunk_index": doc.get('chunk_index', 0)
                    }
                ))

            # Upload batch to Qdrant
            qdrant_client.upsert(
                collection_name="book_content",
                points=points
            )

            logger.info(f"Uploaded batch {i // batch_size + 1} ({len(points)} documents) to Qdrant")

        except Exception as e:
            logger.error(f"Error embedding and storing batch {i // batch_size + 1}: {e}")
            raise

def load_book_content_from_directory(directory_path: str) -> List[Dict]:
    """
    Load all book content from the specified directory.
    Expects .mdx files from the Docusaurus book.
    """
    content_dir = Path(directory_path)
    documents = []

    # Look for all .mdx files in the directory
    mdx_files = list(content_dir.glob("*.mdx")) + list(content_dir.glob("*.md"))

    for file_path in mdx_files:
        logger.info(f"Processing file: {file_path.name}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove frontmatter if present (between --- markers)
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2].strip()

        # Split the content into chunks
        chunks = split_document_into_chunks(content, max_tokens=600)  # Target 500-800 tokens

        for idx, chunk in enumerate(chunks):
            documents.append({
                'content': chunk,
                'source': file_path.name,
                'page': f"chunk_{idx}",
                'chunk_index': idx
            })

    logger.info(f"Loaded {len(documents)} chunks from {len(mdx_files)} files")
    return documents

async def initialize_vector_database(book_content_dir: str):
    """
    Initialize the vector database with book content.
    """
    logger.info("Starting vector database initialization...")

    # Load documents from directory
    documents = load_book_content_from_directory(book_content_dir)

    if not documents:
        logger.warning("No documents found to index!")
        return

    # Embed and store documents
    await embed_and_store_documents(documents)

    logger.info("Vector database initialized successfully!")

def search_relevant_chunks(query: str, top_k: int = 5) -> List[Dict]:
    """
    Search for relevant chunks in the vector database.
    """
    try:
        # Generate embedding for the query
        response = co.embed(
            texts=[query],
            model='embed-english-v3.0',
            input_type='search_query'
        )
        query_embedding = response.embeddings[0]

        # Search in Qdrant
        search_results = qdrant_client.search(
            collection_name="book_content",
            query_vector=query_embedding,
            limit=top_k
        )

        # Format results
        results = []
        for hit in search_results:
            results.append({
                'content': hit.payload['content'],
                'source': hit.payload['source'],
                'score': hit.score,
                'page': hit.payload['page']
            })

        return results
    except Exception as e:
        logger.error(f"Error searching for relevant chunks: {e}")
        return []

if __name__ == "__main__":
    # For testing purposes
    import sys

    if len(sys.argv) > 1:
        book_dir = sys.argv[1]
    else:
        # Default path - adjust as needed
        book_dir = "../../ai-native-book-website/book"

    # Run the initialization
    asyncio.run(initialize_vector_database(book_dir))