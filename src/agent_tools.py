
from pathlib import Path
import re
import json
from datetime import datetime
def calculate_grade(earned_points, total_points):
    try:
        earned_points = float(earned_points)
        total_points = float(total_points)
    except (ValueError, TypeError):
        raise ValueError("Scores must be valid numbers.")

    if total_points <= 0:
        raise ValueError("Total points must be greater than zero.")

    if earned_points < 0:
        raise ValueError("Earned points cannot be negative.")

    if earned_points > total_points:
        raise ValueError("Earned points cannot exceed total points.")

    percentage = (earned_points / total_points) * 100

    return {
        "earned_points": earned_points,
        "total_points": total_points,
        "percentage": round(percentage, 2)
    }






BASE_DIR = Path(__file__).resolve().parent.parent
CALENDAR_FILE = BASE_DIR / "knowledge_base" / "academic_calendar.md"


def lookup_deadline(assignment_name):
    if not isinstance(assignment_name, str) or not assignment_name.strip():
        raise ValueError("Assignment name cannot be empty.")

    if not CALENDAR_FILE.exists():
        raise FileNotFoundError("Academic calendar file was not found.")

    content = CALENDAR_FILE.read_text(encoding="utf-8")
    query = " ".join(assignment_name.lower().split())
    lines = content.splitlines()

    for i, line in enumerate(lines):
        normalized_line = " ".join(line.lower().split())

        if normalized_line.rstrip(":") == query.rstrip(":"):
            details = [line.strip()]

            for next_line in lines[i + 1:]:
                stripped_line = next_line.strip()

                if not stripped_line:
                    break

                if not stripped_line.startswith("-"):
                    break

                details.append(stripped_line)

            return "\n".join(details)

    return "No matching assignment was found in the academic calendar."






TICKETS_FILE = BASE_DIR / "data" / "support_tickets.json"
def create_support_ticket(student_name, issue):
    if not isinstance(student_name, str) or not student_name.strip():
        raise ValueError("Student name cannot be empty.")

    if not isinstance(issue, str) or not issue.strip():
        raise ValueError("Issue description cannot be empty.")

    TICKETS_FILE.parent.mkdir(parents=True, exist_ok=True)

    tickets = []

    if TICKETS_FILE.exists():
        with TICKETS_FILE.open("r", encoding="utf-8") as file:
            tickets = json.load(file)

    ticket = {
        "ticket_id": f"TICKET-{len(tickets) + 1:04d}",
        "student_name": student_name.strip(),
        "issue": issue.strip(),
        "created_at": datetime.now().astimezone().isoformat(),
        "status": "Open"
    }

    tickets.append(ticket)

    with TICKETS_FILE.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4, ensure_ascii=False)

    return ticket





if __name__ == "__main__":
    print("Grade test:")
    print(calculate_grade(85, 100))

    print("\nDeadline test:")
    print(lookup_deadline("Python Assignment 1"))

    print("\nSupport ticket test:")
    ticket = create_support_ticket(
    "Test Student",
    "I cannot access my course assignment."
    )
    print(ticket)