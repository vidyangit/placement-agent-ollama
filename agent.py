import os
from typing import Any

from ollama import chat

from prompts import INSTRUCTION_PROMPT, REASONING_PROMPT, REFLECTION_PROMPT
from tools import AVAILABLE_TOOLS


MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")


def run_agent(user_question: str, verbose: bool = True) -> str:
    """Run the local tool-calling agent."""
    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": INSTRUCTION_PROMPT + "\n" + REASONING_PROMPT,
        },
        {
            "role": "user",
            "content": user_question,
        },
    ]

    # Ollama's Python SDK can derive tool schemas directly from Python
    # functions with Google-style docstrings.
    tool_functions = list(AVAILABLE_TOOLS.values())

    max_rounds = 6

    for _ in range(max_rounds):
        response = chat(
            model=MODEL,
            messages=messages,
            tools=tool_functions,
        )

        messages.append(response.message)

        tool_calls = response.message.tool_calls or []

        if not tool_calls:
            draft = response.message.content
            break

        for tool_call in tool_calls:
            name = tool_call.function.name
            arguments = dict(tool_call.function.arguments)

            if verbose:
                print(f"\n[AGENT DECIDED TO CALL TOOL] {name}")
                print(f"[ARGUMENTS] {arguments}")

            function_to_call = AVAILABLE_TOOLS.get(name)

            if function_to_call is None:
                result = {"error": f"Unknown tool: {name}"}
            else:
                try:
                    result = function_to_call(**arguments)
                except Exception as exc:
                    result = {"error": str(exc)}

            if verbose:
                print(f"[TOOL RESULT] {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "content": str(result),
                }
            )
    else:
        raise RuntimeError("Agent exceeded the maximum tool-calling rounds.")

    # Reflection is a second local LLM pass.
    reflection_messages = [
        {
            "role": "system",
            "content": REFLECTION_PROMPT,
        },
        {
            "role": "user",
            "content": (
                f"USER QUESTION:\n{user_question}\n\n"
                f"DRAFT ANSWER:\n{draft}\n\n"
                "Return the corrected final answer."
            ),
        },
    ]

    reflection = chat(
        model=MODEL,
        messages=reflection_messages,
    )

    return reflection.message.content


if __name__ == "__main__":
    question = input("Student: ").strip()
    if question:
        print("\nAgent:")
        print(run_agent(question))
