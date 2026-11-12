
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from agent_tools import (
    calculate_grade,
    lookup_deadline,
    create_support_ticket,
)
from answer_generator import answer_question


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

MODEL_NAME = "openai/gpt-oss-20b"

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=api_key)
conversation_history = []
MAX_HISTORY_TURNS = 3

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_grade",
            "description": "Calculate a student's percentage from earned and total points.",
            "parameters": {
                "type": "object",
                "properties": {
                    "earned_points": {
                        "type": "number",
                        "description": "Points earned by the student."
                    },
                    "total_points": {
                        "type": "number",
                        "description": "Maximum possible points."
                    }
                },
                "required": ["earned_points", "total_points"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_deadline",
            "description": "Search the academy calendar for an assignment's dates. Never treat a release date as a due date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "assignment_name": {
                        "type": "string",
                        "description": "The assignment or task name to search for."
                    }
                },
                "required": ["assignment_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_support_ticket",
            "description": "Create and save a support ticket only after the student provides their name and issue description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "student_name": {
                        "type": "string",
                        "description": "Name provided by the student."
                    },
                    "issue": {
                        "type": "string",
                        "description": "Description of the student's issue."
                    }
                },
                "required": ["student_name", "issue"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_academic_knowledge",
            "description": "Answer questions about academy policies, courses, attendance, assignments, and FAQs using the knowledge base. Use this instead of guessing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The student's academic question."
                    }
                },
                "required": ["question"]
            }
        }
    }
]


def execute_tool(name, arguments):
    if name == "calculate_grade":
        return calculate_grade(
            arguments["earned_points"],
            arguments["total_points"]
        )

    if name == "lookup_deadline":
        return lookup_deadline(arguments["assignment_name"])

    if name == "create_support_ticket":
        return create_support_ticket(
            arguments["student_name"],
            arguments["issue"]
        )

    if name == "search_academic_knowledge":
        return answer_question(arguments["question"])

    return {"error": f"Unknown tool: {name}"}


def run_agent(user_input):
    if not isinstance(user_input, str) or not user_input.strip():
        return "Please enter a question."

    messages = [
    {
        "role": "system",
        "content": """

You are an Academic Support Agent for a fictional sample academy.

Use the available tools for academic questions.

Rules:
1. Use calculate_grade for numerical grade calculations.
2. Use lookup_deadline to search for assignment dates.
3. Use create_support_ticket only when the student provides their name and issue description.
4. Use search_academic_knowledge for academy policies, course rules, attendance, passing criteria, and FAQs.
5. Never invent academy policies, passing grades, retake rules, deadlines, or consequences of failing.
6. Do not answer policy questions using general knowledge when the academy knowledge base does not support the answer.
7. If the knowledge base does not contain enough information, clearly say that the information is not available in the academy records.
8. A release date is not a due date.
9. Use recent conversation history to understand follow-up questions, but do not treat previous assistant guesses as facts.
10. All academy policies and dates are fictional sample data.
11. Be friendly and concise.

"""
    },
    *conversation_history,
    {
        "role": "user",
        "content": user_input.strip()
    }
]

    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2,
            max_completion_tokens=700
        )

        message = response.choices[0].message




        if not message.tool_calls:
            answer = message.content or "I could not generate a response."

            conversation_history.extend([
              {"role": "user", "content": user_input.strip()},
              {"role": "assistant", "content": answer}
            ])

            del conversation_history[:-6]

            return answer




        messages.append(message)

        for tool_call in message.tool_calls:
            name = tool_call.function.name

            try:
                arguments = json.loads(tool_call.function.arguments)
                result = execute_tool(name, arguments)
            except (ValueError, TypeError, KeyError, FileNotFoundError) as error:
                result = {"error": str(error)}
            except Exception as error:
                result = {
                    "error": f"Tool failed: {type(error).__name__}: {error}"
                }

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": name,
                "content": json.dumps(result, ensure_ascii=False)
                if isinstance(result, (dict, list))
                else str(result)
            })

    return "I could not complete the request within the tool-call limit. Please try again."


if __name__ == "__main__":
    print("Academic Support Agent")
    print("Type 'exit' to stop.")

    while True:
        user_input = input("\nYou: ")

        if user_input.strip().lower() in ["exit", "quit"]:
            break

        try:
            print("\nAgent:", run_agent(user_input))
        except Exception as error:
            print(f"\nError: {type(error).__name__}: {error}")
