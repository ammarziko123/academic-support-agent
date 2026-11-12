
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from agent_tools import create_support_ticket, TICKETS_FILE


def run_test(name, test_function):
    try:
        test_function()
        print(f"PASS: {name}")
        return True
    except Exception as error:
        print(f"FAIL: {name}")
        print(f"Details: {type(error).__name__}: {error}")
        return False


def test_valid_ticket():
    ticket = create_support_ticket(
        "Evaluation Test Student",
        "Testing support ticket creation."
    )

    assert ticket["ticket_id"].startswith("TICKET-")
    assert ticket["student_name"] == "Evaluation Test Student"
    assert ticket["issue"] == "Testing support ticket creation."
    assert ticket["status"] == "Open"

    with TICKETS_FILE.open("r", encoding="utf-8") as file:
        tickets = json.load(file)

    assert any(
        saved_ticket["ticket_id"] == ticket["ticket_id"]
        for saved_ticket in tickets
    )


def test_empty_name():
    try:
        create_support_ticket("", "Testing issue.")
    except ValueError:
        return

    raise AssertionError("Empty student name was accepted.")


def test_empty_issue():
    try:
        create_support_ticket("Evaluation Test Student", "   ")
    except ValueError:
        return

    raise AssertionError("Empty issue description was accepted.")


def test_whitespace_is_trimmed():
    ticket = create_support_ticket(
        "  Evaluation Student  ",
        "  Cannot access course materials.  "
    )

    assert ticket["student_name"] == "Evaluation Student"
    assert ticket["issue"] == "Cannot access course materials."


def evaluate_tickets():
    tests = [
        ("Create and save a valid ticket", test_valid_ticket),
        ("Reject an empty student name", test_empty_name),
        ("Reject an empty issue description", test_empty_issue),
        ("Trim unnecessary whitespace", test_whitespace_is_trimmed),
    ]

    passed = 0
    failed = 0

    print("\nSUPPORT TICKET EVALUATION")
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
    print(f"Ticket evaluation score: {accuracy:.2f}%")
    print(f"Total tests: {total}")


if __name__ == "__main__":
    evaluate_tickets()
