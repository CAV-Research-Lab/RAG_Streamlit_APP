from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import os

# __Document Chunking__
chunk_size = 2000
chunk_overlap = 300

current_dir = os.path.dirname(__file__)
database_directory = os.path.join(current_dir, "saved_data", "database") # Directory containing txt files with content and metadata
chromadb_directory = os.path.join(current_dir, "chroma_db") # Directory to store ChromaDB data 

def extract_keywords(text, top_n=5):
    """Extract top N keywords using TF-IDF."""
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
    tfidf_matrix = vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()
    return keywords.tolist()

# Initialize ChromaDB client and collection
client = chromadb.PersistentClient(chromadb_directory)
collection = client.get_or_create_collection(name="RAG_Assistant", metadata={"hnsw:space": "cosine"})

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ". ", "? ", "! "],  # List of characters to split on
    chunk_size=chunk_size,  # The maximum size of your chunks
    chunk_overlap=chunk_overlap,  # The maximum overlap between chunks
)

# Process each txt file in the directory
for file_name in os.listdir(database_directory):
    if file_name.endswith('.txt'):
        file_path = os.path.join(database_directory, file_name)

        # Read content and metadata from the txt file
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            metadata_index = lines.index("=== Metadata ===\n") + 1  # Locate metadata start
            content_index = lines.index("=== Content ===\n") + 1  # Locate content start

            metadata = json.loads("".join(lines[metadata_index:content_index-1]))
            content = "".join(lines[content_index:])

        # Create chunks using langchain
        langchain_chunks = text_splitter.create_documents([content])

        # Insert chunks and metadata into ChromaDB collection
        for i, chunk in enumerate(langchain_chunks):
            chunk_id = f"{file_name}_chunk_{i}"
            metadata_with_chunk = metadata.copy()
            metadata_with_chunk["chunk_number"] = i
            collection.add(
                ids=[chunk_id],
                documents=[chunk.page_content],
                metadatas=[metadata_with_chunk]
            )

        print(f"Processed and inserted file: {file_name}")

print("All files have been processed and inserted into ChromaDB successfully!")
