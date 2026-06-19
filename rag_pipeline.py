import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

CHROMA_PATH = "chroma_db"
DATA_PATH = "data"

embedding_fn = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def ingest_documents():
    docs = []
    for fname in os.listdir(DATA_PATH):
        fpath = os.path.join(DATA_PATH, fname)
        try:
            if fname.endswith(".pdf"):
                loader = PyPDFLoader(fpath)
            elif fname.endswith((".md", ".txt")):
                loader = TextLoader(fpath, encoding="utf-8")
            else:
                continue
            loaded = loader.load()
            for doc in loaded:
                doc.metadata["source"] = fname
            docs.extend(loaded)
            print(f"  Loaded: {fname}")
        except Exception as e:
            print(f"  Skipped {fname}: {e}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    db = Chroma.from_documents(chunks, embedding_fn, persist_directory=CHROMA_PATH)
    print(f"\nIngested {len(chunks)} chunks from {len(docs)} documents.")

def retrieve(query: str, k: int = 4) -> list:
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_fn)
    results = db.similarity_search_with_score(query, k=k)
    chunks = []
    for doc, score in results:
        chunks.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "page": doc.metadata.get("page", "N/A"),
            "score": round(float(score), 3)
        })
    return chunks