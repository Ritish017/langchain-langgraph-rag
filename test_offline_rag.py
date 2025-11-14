"""
Test the RAG system with offline embeddings and local sample documents
"""

from src.llms.offline_embeddings import OfflineTfIdfEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import tempfile
import os

def create_sample_documents():
    """Create sample documents about LangChain and LangGraph"""
    documents = [
        Document(
            page_content="""
            LangGraph is a library for building stateful, multi-actor applications with LLMs. 
            It is built on top of LangChain and provides a framework for creating complex workflows 
            and agent systems. LangGraph uses graph-based structures to represent the flow of 
            execution between different components.
            """,
            metadata={"source": "langgraph_intro", "topic": "introduction"}
        ),
        Document(
            page_content="""
            LangChain is a framework for developing applications powered by language models. 
            It provides tools for document loading, text splitting, vector stores, retrievers, 
            and chains. LangChain enables developers to build complex applications like 
            question-answering systems, chatbots, and document analysis tools.
            """,
            metadata={"source": "langchain_intro", "topic": "introduction"}
        ),
        Document(
            page_content="""
            Vector stores in LangChain are databases that store and retrieve high-dimensional 
            vectors representing text embeddings. Popular vector stores include Chroma, Pinecone, 
            and Weaviate. These stores enable semantic search and retrieval augmented generation 
            (RAG) applications by finding documents similar to a query.
            """,
            metadata={"source": "vector_stores", "topic": "components"}
        ),
        Document(
            page_content="""
            RAG (Retrieval Augmented Generation) is a technique that combines information 
            retrieval with language generation. It works by first retrieving relevant documents 
            from a knowledge base, then using those documents as context for generating responses. 
            This approach helps reduce hallucinations and provides more accurate, grounded answers.
            """,
            metadata={"source": "rag_explanation", "topic": "concepts"}
        ),
        Document(
            page_content="""
            LangGraph nodes are individual components in a graph that perform specific tasks. 
            Each node can be a function that processes the state and returns updated state. 
            Nodes can be connected with edges to create complex workflows. Common node types 
            include generators, retrievers, graders, and rewriters.
            """,
            metadata={"source": "langgraph_nodes", "topic": "components"}
        ),
        Document(
            page_content="""
            Document graders in RAG systems evaluate the relevance of retrieved documents 
            to the user's question. They typically use binary scoring (relevant/not relevant) 
            or confidence scores. Graders help improve the quality of generated answers by 
            filtering out irrelevant information.
            """,
            metadata={"source": "document_grading", "topic": "rag"}
        )
    ]
    return documents

def test_offline_rag():
    """Test the complete offline RAG system"""
    print("🧪 Testing Offline RAG System")
    print("=" * 50)
    
    # Create sample documents
    documents = create_sample_documents()
    print(f"📚 Created {len(documents)} sample documents")
    
    # Initialize offline embeddings
    embedding = OfflineTfIdfEmbeddings(max_features=1000)
    
    # Extract text content for fitting the embeddings
    texts = [doc.page_content for doc in documents]
    print("🔧 Fitting offline embeddings...")
    embedding.fit(texts)
    
    # Create vector store without persistence to avoid file locking issues
    print(f"🗃️  Creating in-memory vector store")
    
    # Create vector store with offline embeddings (in-memory)
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding
    )
    
    # Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    # Test queries
    test_queries = [
        "What is LangGraph?",
        "How do vector stores work?",
        "Explain RAG systems",
        "What are document graders?"
    ]
    
    print("\n🔍 Testing Retrieval:")
    print("-" * 30)
    
    for query in test_queries:
        print(f"\n❓ Query: {query}")
        docs = retriever.invoke(query)
        
        print(f"📄 Retrieved {len(docs)} documents:")
        for i, doc in enumerate(docs, 1):
            preview = doc.page_content[:100].strip().replace('\n', ' ')
            print(f"  {i}. {preview}...")
            print(f"     Source: {doc.metadata.get('source', 'unknown')}")

if __name__ == "__main__":
    test_offline_rag()