import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import uuid

class DocumentRAG:
    def __init__(self):
        # Initialize ChromaDB and embedding model
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("engineering_docs")  # What should we call our collection?
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    def add_document(self, text: str, filename: str):
        chunk_size = 500
        overlap = 50
        chunks = []

        for i in range(0, len(text), chunk_size-overlap):
            chunk = text[i:i + chunk_size]
            chunks.append(chunk)

        for chunk in chunks:
            # Create unique ID for this chunk
            chunk_id = str(uuid.uuid4())

            # Convert chunk text to vector
            embedding = self.embedder.encode([chunk])

            # Store in ChromaDB
            self.collection.add(
                embeddings=embedding.tolist(),  # Convert numpy array to list
                documents=[chunk],  # The actual text chunk
                ids=[chunk_id],  # The unique ID we created
                metadatas=[{"filename": filename, "chunk_index": len(chunks)}]  # Extra info
            )

    def search_documents(self, query: str, n_results: int = 3) -> List[str]:
        query_embedding = self.embedder.encode([query])

        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
        n_results = n_results
        )

        return results['documents'][0]

if __name__ == "__main__":
        # Import our document processor
        import sys
        sys.path.append('.')
        from document_processor import extract_pdf_text

        # Create RAG system
        rag = DocumentRAG()

        # Extract text from your bridge PDF
        print("Extracting text from bridge document...")
        bridge_text = extract_pdf_text("../uploads/bridge_design.pdf")

        # Add to RAG system
        print("Adding document to vector database...")
        rag.add_document(bridge_text, "bridge_design.pdf")

        # Test search
        print("\nTesting search...")
        results = rag.search_documents("bridge abutment", 3)

        print("Search results:")
        for i, chunk in enumerate(results):
            print(f"\n--- Result {i + 1} ---")
            print(chunk[:200] + "...")
