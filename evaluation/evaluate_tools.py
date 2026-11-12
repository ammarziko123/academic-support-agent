
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from agent_tools import calculate_grade


def test_valid_grade(earned, total, expected):
    try:
        result = calculate_grade(earned, total)

        if isinstance(result, dict):
            percentage = result.get("percentage")
        else:
            percentage = None

        if percentage is not None and abs(float(percentage) - expected) < 0.01:
            return True, str(result)

        return False, f"Unexpected result: {result}"

    except Exception as error:
        return False, f"{type(error).__name__}: {error}"


def test_invalid_grade(earned, total):
    try:
        result = calculate_grade(earned, total)

        if isinstance(result, dict) and result.get("error"):
            return True, str(result)

        return False, f"Invalid input was accepted: {result}"

    except (ValueError, TypeError, ZeroDivisionError) as error:
        return True, f"Correctly rejected: {error}"

    except Exception as error:
        return False, f"Unexpected error: {type(error).__name__}: {error}"


def evaluate_tools():
    tests = [
        ("Valid grade: 85/100", lambda: test_valid_grade(85, 100, 85)),
        ("Valid grade: 45/60", lambda: test_valid_grade(45, 60, 75)),
        ("Zero total points", lambda: test_invalid_grade(10, 0)),
        ("Negative earned points", lambda: test_invalid_grade(-5, 100)),
        ("Earned points exceed total", lambda: test_invalid_grade(120, 100)),
    ]

    passed = 0
    failed = 0

    print("\nTOOL INPUT VALIDATION EVALUATION")

    for name, test in tests:
        success, details = test()

        print("=" * 60)
        print(f"Test: {name}")
        print(f"Details: {details}")
        print(f"Result: {'PASS' if success else 'FAIL'}")

        if success:
            passed += 1
        else:
            failed += 1

    total = passed + failed
    accuracy = passed / total * 100 if total else 0

    print("\n" + "=" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Tool evaluation score: {accuracy:.2f}%")
    print(f"Total tests: {total}")


if __name__ == "__main__":
    evaluate_tools()
