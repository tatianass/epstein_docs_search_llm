import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama  # Or use HuggingFaceHub / OpenAI
from langchain_ollama import ChatOllama


# 1. INGESTION: Transforming docs in chuncks
def ingest_docs(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()

    # Chunking: Crucial for Transformer context windows (BERT/RoBERTa style)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    chunks = text_splitter.split_documents(data)
    return chunks


# 2. EMBEDDING: Applying Deep Learning Theory (Vector Spaces)
def create_vector_db(chunks):
    # Using a sentence-transformer model (All-MiniLM-L6-v2)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Persisting data into Chroma as vectors
    vector_db = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory="./chroma_db"
    )
    return vector_db


# 3. RETRIEVAL: query db for relevant chuncks and invoke the LLM to answer the question
def query_system(vector_db, query):
    # Search for top n relevant chunks
    docs = vector_db.similarity_search(query, k=3)

    context = "\n".join([d.page_content for d in docs])
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"

    # Here you can use different llms
    llm = ChatOllama(model="llama3.2:1b", temperature=0)
    response = llm.invoke(prompt)
    return response.content


# Execution Flow
if __name__ == "__main__":
    path = "pdfs/EFTA02731023.pdf"  # Epstein document
    doc_chunks = ingest_docs(path)
    db = create_vector_db(doc_chunks)
    final_prompt = query_system(db, "Who is mentioned?")
    print(final_prompt)
