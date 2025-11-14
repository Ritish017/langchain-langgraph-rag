"""
Script to rebuild the vector store from scratch (clean rebuild)
"""
import shutil
import os
from pathlib import Path

def rebuild_clean():
    """Delete existing vector store and rebuild from scratch"""
    
    # Delete existing vector store
    chroma_path = Path("./chroma_db")
    if chroma_path.exists():
        print("Deleting existing vector store...")
        try:
            shutil.rmtree(chroma_path)
            print("✓ Vector store deleted")
        except Exception as e:
            print(f"✗ Error deleting vector store: {e}")
            print("Please close Streamlit app and try again")
            return
    
    # Load and split documents
    print("\nLoading documents from URLs...")
    from src.ingetsion.document_loaders import load_web_documents, urls_full
    from src.ingetsion.text_splitter import split_texts
    from src.ingetsion.retriever import create_vectorstore
    
    docs = load_web_documents(urls_full)
    print(f"✓ Loaded {len(docs)} documents")
    
    splits = split_texts(docs)
    print(f"✓ Split into {len(splits)} chunks")
    
    # Create new vector store
    print("\nCreating vector store...")
    retriever = create_vectorstore(splits, force_reload=True)
    print("✓ Vector store created successfully!")
    
    print("\n✅ Done! You can now run the Streamlit app.")

if __name__ == "__main__":
    rebuild_clean()
