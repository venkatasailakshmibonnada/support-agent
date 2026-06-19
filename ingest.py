from dotenv import load_dotenv
load_dotenv()

from src.rag_pipeline import ingest_documents

if __name__ == "__main__":
    print("Starting knowledge base ingestion...")
    ingest_documents()
    print("Done! Vector store saved to chroma_db/")