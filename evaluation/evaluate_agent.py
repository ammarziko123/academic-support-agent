
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from agent import run_agent, conversation_history


def reset_history():
    conversation_history.clear()


def run_test(test_id, question, check_response):
    reset_history()

    print("=" * 65)
    print(f"Test {test_id}")
    print(f"Question: {question}")

    try:
        response = run_agent(question)
        print(f"Response: {response}")

        normalized_response = response.lower().replace("’", "'")
        passed = check_response(normalized_response)    

        if passed:
            print("Result: PASS")
        else:
            print("Result: FAIL")

        return passed

    except Exception as error:
        print("Result: FAIL")
        print(f"Error: {type(error).__name__}: {error}")
        return False


def contains_any(*phrases):
    return lambda response: any(
        phrase.lower() in response for phrase in phrases
    )


def contains_all(*phrases):
    return lambda response: all(
        phrase.lower() in response for phrase in phrases
    )


def evaluate_agent():
    tests = [
        (
            1,
            "Calculate my grade: 85 out of 100",
            contains_any("85")
        ),
        (
            2,
            "Calculate my grade using 45 earned points out of 60",
            contains_any("75")
        ),
        (
            3,
            "What is the attendance requirement?",
            contains_all("80")
        ),
        (
            4,
            "What happens if I fail an assignment?",
            contains_any(
                "couldn't find",
                "could not find",
                "not available",
                "does not specify",
                "not specified",
                "don't contain any information",
                "don't contain",
                "do not contain",
                "records don't contain",
                "records do not contain",
                "don't describe",
                "do not describe",
                "no information about"
            )
        ),
        
        (
            5,
            "Create a support ticket",
            contains_all("name", "issue")
        )
    ]

    passed = 0
    failed = 0

    print("\nACADEMIC SUPPORT AGENT EVALUATION")

    for test_id, question, checker in tests:
        if run_test(test_id, question, checker):
            passed += 1
        else:
            failed += 1

    total = passed + failed
    accuracy = passed / total * 100 if total else 0

    print("\n" + "=" * 65)
    print("FINAL RESULTS")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Agent evaluation score: {accuracy:.2f}%")
    print(f"Total tests: {total}")


if __name__ == "__main__":
    evaluate_agent()
