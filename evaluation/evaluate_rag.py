
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


from src.rag_pipeline import search_knowledge_base


TEST_FILE = BASE_DIR / "evaluation" / "test_cases.json"
TOP_K = 3


def evaluate_rag():
    with TEST_FILE.open("r", encoding="utf-8") as file:
        test_cases = json.load(file)

    retrieval_cases = [
        case for case in test_cases
        if case["expected_behavior"] == "answer_from_knowledge_base"
    ]

    passed = 0
    failed = 0

    print("=" * 65)
    print("RAG RETRIEVAL EVALUATION")
    print("=" * 65)

    for case in retrieval_cases:
        question = case["question"]
        expected_source = case["expected_source"]

        try:
            results = search_knowledge_base(question, top_k=TOP_K)

            retrieved_sources = [
                result["document_name"] for result in results
            ]

            success = expected_source in retrieved_sources

            if success:
                passed += 1
                status = "PASS"
            else:
                failed += 1
                status = "FAIL"

            top_score = results[0]["score"] if results else 0

            print(f"\nTest {case['id']}: {status}")
            print(f"Question: {question}")
            print(f"Expected source: {expected_source}")
            print(f"Retrieved sources: {retrieved_sources}")
            print(f"Top similarity score: {top_score:.4f}")

        except Exception as error:
            failed += 1
            print(f"\nTest {case['id']}: FAIL")
            print(f"Question: {question}")
            print(f"Error: {type(error).__name__}: {error}")

    total = passed + failed
    accuracy = (passed / total * 100) if total else 0

    print("\n" + "=" * 65)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Retrieval accuracy: {accuracy:.2f}%")
    print(f"Tested cases: {total}")
    print("=" * 65)


if __name__ == "__main__":
    evaluate_rag()
