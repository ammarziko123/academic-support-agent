
from pathlib import Path
import re

KNOWLEDGE_BASE_DIR = Path(__file__).parent / "knowledge_base"
SUPPORTED_EXTENSIONS = {".txt", ".md"}

def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def load_documents():
    documents = []

    for file_path in sorted(KNOWLEDGE_BASE_DIR.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            text = clean_text(
                file_path.read_text(encoding="utf-8")
            )

            if text:
                documents.append({
                    "document_name": file_path.name,
                    "content": text
                })

    return documents

def main():
    documents = load_documents()
    total_words = 0

    print("\nACADEMIC SUPPORT AGENT")
    print("=" * 35)

    for document in documents:
        word_count = len(re.findall(r"\b[\w'-]+\b", document["content"]))
        total_words += word_count

        print(f"{document['document_name']}: {word_count} words")

    print("=" * 35)
    print(f"Total documents: {len(documents)}")
    print(f"Total words: {total_words}")

    if len(documents) < 5:
        print("WARNING: At least 5 documents are required.")

    if total_words < 2000:
        print("WARNING: The corpus needs at least 2000 words.")
    else:
        print("SUCCESS: Minimum word-count requirement satisfied.")

if __name__ == "__main__":
    main()
