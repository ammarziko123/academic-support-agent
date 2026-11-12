
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from agent_tools import lookup_deadline


def run_test(name, test_function):
    try:
        test_function()
        print(f"PASS: {name}")
        return True
    except Exception as error:
        print(f"FAIL: {name}")
        print(f"Details: {type(error).__name__}: {error}")
        return False


def test_assignment_1_deadline():
    result = lookup_deadline("Python Assignment 1")
    assert "Release Date: 2026-11-04" in result
    assert "Deadline: 2026-11-11 at 23:59" in result


def test_assignment_2_deadline():
    result = lookup_deadline("Python Assignment 2")
    assert "Release Date: 2026-11-16" in result
    assert "Deadline: 2026-11-25 at 23:59" in result


def test_submission_format():
    result = lookup_deadline("Python Assignment 1")
    assert "Submission Format: IPYNB" in result


def test_unknown_assignment():
    result = lookup_deadline("Unknown Assignment 99")
    assert "No matching assignment was found" in result


def test_empty_assignment_name():
    try:
        lookup_deadline("   ")
    except ValueError:
        return
    raise AssertionError("Empty assignment name was accepted.")


def evaluate_deadlines():
    tests = [
        ("Assignment 1 release date and deadline", test_assignment_1_deadline),
        ("Assignment 2 release date and deadline", test_assignment_2_deadline),
        ("Submission format", test_submission_format),
        ("Unknown assignment", test_unknown_assignment),
        ("Reject empty assignment name", test_empty_assignment_name),
    ]

    passed = 0
    failed = 0

    print("\nDEADLINE TOOL EVALUATION")
    print("=" * 60)

    for name, test_function in tests:
        if run_test(name, test_function):
            passed += 1
        else:
            failed += 1

    total = passed + failed
    accuracy = passed / total * 100 if total else 0

    print("\n" + "=" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Deadline evaluation score: {accuracy:.2f}%")
    print(f"Total tests: {total}")


if __name__ == "__main__":
    evaluate_deadlines()
