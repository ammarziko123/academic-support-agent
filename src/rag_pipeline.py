
from pathlib import Path
import re
import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
INDEX_DIR = BASE_DIR / "data"
INDEX_PATH = INDEX_DIR / "knowledge.index"
CHUNKS_PATH = INDEX_DIR / "chunks.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 180
CHUNK_OVERLAP = 40


def load_documents():
    documents = []

    for path in sorted(KNOWLEDGE_BASE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()

        if text:
            documents.append({
                "document_name": path.name,
                "content": text
            })

    return documents


def split_into_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])

        if chunk:
            chunks.append(chunk)

        if end == len(words):
            break

        start = end - overlap

    return chunks


def build_knowledge_base():
    documents = load_documents()
    all_chunks = []

    for document in documents:
        chunks = split_into_chunks(document["content"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id": f"{document['document_name']}_chunk_{i}",
                "document_name": document["document_name"],
                "text": chunk
            })

    if not all_chunks:
        raise ValueError("No documents found in knowledge_base.")

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in all_chunks]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))

    with CHUNKS_PATH.open("w", encoding="utf-8") as file:
        json.dump(all_chunks, file, ensure_ascii=False, indent=2)

    print("\nKnowledge base built successfully!")
    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(all_chunks)}")
    print(f"Embedding dimensions: {embeddings.shape[1]}")
    print(f"FAISS index saved to: {INDEX_PATH}")
    print(f"Chunk metadata saved to: {CHUNKS_PATH}")


def search_knowledge_base(query, top_k=3):
    if not INDEX_PATH.exists() or not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            "Knowledge base index not found. Build it first."
        )

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    with CHUNKS_PATH.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    index = faiss.read_index(str(INDEX_PATH))
    model = SentenceTransformer(MODEL_NAME)

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    query_embedding = np.asarray(query_embedding, dtype="float32")
    top_k = max(1, min(top_k, len(chunks)))

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        result = chunks[int(idx)].copy()
        result["score"] = float(score)
        results.append(result)

    return results



if __name__ == "__main__":
    build_knowledge_base()

    test_questions = [
        "What is the attendance requirement?",
        "What is the late submission penalty?",
        "When is Python Assignment 1 due?",
        "What courses are available?",
        "How can a student report a technical issue?"
    ]

    for question in test_questions:
        print("\n" + "=" * 60)
        print(f"Question: {question}")

        results = search_knowledge_base(question, top_k=3)

        for result in results:
            print(f"\nSource: {result['document_name']}")
            print(f"Similarity: {result['score']:.3f}")
            print(result["text"][:300])

