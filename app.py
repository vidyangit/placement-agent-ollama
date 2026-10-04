import os

from agent import run_agent, MODEL


def main():
    print("=" * 72)
    print("LOCAL PLACEMENT SUPPORT AGENT")
    print("=" * 72)
    print(f"Model : {MODEL}")
    print("Backend: Ollama (local)")
    #print("No cloud API key is required.")
    print("Type 'exit' to stop.")
    print("=" * 72)

    while True:
        question = input("\nStudent: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Agent: Goodbye.")
            break

        if not question:
            continue

        try:
            answer = run_agent(question)
            print("\nAgent:")
            print(answer)
        except Exception as exc:
            print(f"\nApplication error: {exc}")
            print("Check that Ollama is running and the selected model is installed.")


if __name__ == "__main__":
    main()
