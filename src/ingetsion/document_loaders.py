from langchain_community.document_loaders import WebBaseLoader
import urllib3
import ssl
import time

# Disable SSL warnings for corporate networks
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Complete URL list with comprehensive LangChain and LangGraph documentation
urls_full = [
    # Core LangChain Documentation
    "https://python.langchain.com/v0.2/docs/introduction/",
    "https://python.langchain.com/v0.2/docs/concepts/",
    "https://python.langchain.com/v0.2/docs/tutorials/",
    "https://python.langchain.com/v0.2/docs/how_to/",
    "https://python.langchain.com/v0.2/docs/tutorials/llm_chain/",
    "https://python.langchain.com/v0.2/docs/tutorials/chatbot/",
    "https://python.langchain.com/v0.2/docs/tutorials/rag/",
    "https://python.langchain.com/v0.2/docs/tutorials/agents/",
    
    # LangChain Components - Comprehensive
    "https://python.langchain.com/v0.2/docs/concepts/chat_models/",
    "https://python.langchain.com/v0.2/docs/concepts/llms/",
    "https://python.langchain.com/v0.2/docs/concepts/prompts/",
    "https://python.langchain.com/v0.2/docs/concepts/output_parsers/",
    "https://python.langchain.com/v0.2/docs/concepts/document_loaders/",
    "https://python.langchain.com/v0.2/docs/concepts/text_splitters/",
    "https://python.langchain.com/v0.2/docs/concepts/vectorstores/",
    "https://python.langchain.com/v0.2/docs/concepts/retrievers/",
    "https://python.langchain.com/v0.2/docs/concepts/indexing/",
    "https://python.langchain.com/v0.2/docs/concepts/embedding_models/",
    
    # LangChain Integrations - Key ones
    "https://python.langchain.com/v0.2/docs/integrations/document_loaders/",
    "https://python.langchain.com/v0.2/docs/integrations/vectorstores/",
    "https://python.langchain.com/v0.2/docs/integrations/retrievers/",
    "https://python.langchain.com/v0.2/docs/integrations/text_embedding/",
    "https://python.langchain.com/v0.2/docs/integrations/chat/",
    "https://python.langchain.com/v0.2/docs/integrations/llms/",
    
    # LangGraph Documentation - Updated URLs
    "https://python.langchain.com/docs/langgraph/",
    "https://python.langchain.com/docs/concepts/langgraph/",
    "https://python.langchain.com/docs/tutorials/langgraph/",
    "https://python.langchain.com/docs/how_to/langgraph/",
    
    # LangChain Advanced Topics
    "https://python.langchain.com/v0.2/docs/how_to/custom_chat_model/",
    "https://python.langchain.com/v0.2/docs/how_to/custom_llm/",
    "https://python.langchain.com/v0.2/docs/how_to/custom_tools/",
    "https://python.langchain.com/v0.2/docs/how_to/callbacks/",
    "https://python.langchain.com/v0.2/docs/how_to/streaming/",
    "https://python.langchain.com/v0.2/docs/how_to/debugging/",
    
    # LangChain Community Resources
    "https://blog.langchain.dev/",
    "https://python.langchain.com/v0.2/docs/security/",
    "https://python.langchain.com/v0.2/docs/guides/",
]

# Default URLs
urls = urls_full

def load_web_documents(urls_to_use=None, use_minimal_set=False):
    """
    Load web documents from URLs with SSL handling.
    
    Args:
        urls_to_use: Custom list of URLs to load. If None, uses default comprehensive set.
        use_minimal_set: If True, uses minimal URL set for testing/quota limits.
    """
    if urls_to_use is None:
        urls_to_use = urls
    
    docs = []
    successful_loads = 0
    print(f"Loading {len(urls_to_use)} documentation pages...")
    
    for i, url in enumerate(urls_to_use, 1):
        try:
            print(f"[{i}/{len(urls_to_use)}] Loading: {url}")
            
            # Configure WebBaseLoader with SSL settings
            loader = WebBaseLoader(
                url,
                requests_kwargs={
                    "verify": False,  # Disable SSL verification for corporate networks
                    "timeout": 30,
                    "headers": {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                }
            )
            
            loaded_docs = loader.load()
            if loaded_docs:
                docs.extend(loaded_docs)
                successful_loads += 1
                print(f"   Success: {len(loaded_docs)} documents ({len(docs)} total)")
            else:
                print(f"   Warning: No content found")
            
            # Small delay to be respectful
            time.sleep(0.5)
            
        except Exception as e:
            print(f"   Failed: {str(e)[:100]}...")
    
    print(f"\nSuccessfully loaded {successful_loads}/{len(urls_to_use)} URLs")
    print(f"Total documents loaded: {len(docs)}")
    return docs