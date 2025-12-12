import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vector_db_setup import initialize_vector_database

async def populate_database():
    """
    Script to populate the Qdrant database with book content.
    """
    print("Starting database population...")

    # Path to the book content directory
    book_dir = "../ai-native-book-website/book"

    # Initialize the vector database with book content
    await initialize_vector_database(book_dir)

    print("Database populated successfully!")

if __name__ == "__main__":
    asyncio.run(populate_database())