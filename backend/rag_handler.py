import os
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# --- Configuration ---
VECTOR_STORE_PATH = "./vector_store"
CHROMA_COLLECTION_NAME = "chat_docs"

# --- RAG Functions ---

def get_vector_store():
    """Initializes and returns the Chroma vector store."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    return Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embeddings,
        collection_name=CHROMA_COLLECTION_NAME
    )

def process_and_store_document(file_path: str):
    """Loads, splits, and stores a document in the vector store."""
    if not os.path.exists(file_path):
        return {"error": "File not found."}

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    vector_store = get_vector_store()
    vector_store.add_documents(docs)
    vector_store.persist()
    
    os.remove(file_path)

    return {"status": "success", "message": f"Processed and stored {len(docs)} chunks."}


def get_context_from_query(query: str, k: int = 4):
    """Retrieves relevant document chunks based on a user query."""
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    relevant_docs = retriever.invoke(query)
    
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    return context