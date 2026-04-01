import os

from dotenv import load_dotenv
from deepagents import create_deep_agent

load_dotenv()


def main():
    agent = create_deep_agent(
        model="anthropic:claude-sonnet-4-6",
        system_prompt="You are a helpful assistant.",
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Hello! Tell me about yourself."}]}
    )

    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
