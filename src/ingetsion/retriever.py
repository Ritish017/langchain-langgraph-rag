from langchain_chroma import Chroma
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

_vectorstore_cache = None

def create_vectorstore(texts=None, persist_directory="./chroma_db", force_reload=False):
    """
    Create or load a vector store.
    
    Args:
        texts: Optional list of documents to add. If None and store doesn't exist, will load from URLs.
        persist_directory: Directory to persist the vector store
        force_reload: If True, forces reloading the vector store even if cached
    
    Returns:
        A retriever instance
    """
    global _vectorstore_cache
    
    # Return cached vectorstore if available and not forcing reload
    if _vectorstore_cache is not None and not force_reload:
        return _vectorstore_cache
    
    # Import embedding here to avoid Python 3.13 compatibility issues
    from src.llms.offline_embeddings import OfflineTfIdfEmbeddings
    
    # Use offline TF-IDF embeddings (no internet required)
    embedding = OfflineTfIdfEmbeddings(max_features=5000)
    
    # Check if persistent vector store already exists
    if os.path.exists(persist_directory):
        print("Loading existing vector store...")
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding
        )
        existing_count = vectorstore._collection.count()
        print(f"Loaded vector store with {existing_count} documents")
        
        # Only add new documents if explicitly provided
        if texts is not None and len(texts) > 0:
            print(f"Adding {len(texts)} new documents to vector store...")
            vectorstore.add_documents(texts)
            new_count = vectorstore._collection.count()
            print(f"Vector store now has {new_count} documents (added {new_count - existing_count} new documents)")
        
        _vectorstore_cache = vectorstore.as_retriever()
        return _vectorstore_cache
    
    # If vector store doesn't exist and no texts provided, load from URLs
    if texts is None:
        print("Vector store not found. Loading documents from URLs...")
        from src.ingetsion.text_splitter import split_texts
        texts = split_texts()
    
    print(f"Creating new vector store with {len(texts)} documents...")
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embedding,
        persist_directory=persist_directory
    )
    print(f"Created vector store with {len(texts)} documents")
    _vectorstore_cache = vectorstore.as_retriever()
    return _vectorstore_cache

    