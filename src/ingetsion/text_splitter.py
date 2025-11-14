
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ingetsion.document_loaders import load_web_documents, urls

def split_texts(docs=None, use_minimal_url_set=False):
    if docs is None:
        # Load documents from the comprehensive URL list
        docs = load_web_documents(urls)
    
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=200,
    )
    docs_splits =  text_splitter.split_documents(docs)
    return docs_splits

