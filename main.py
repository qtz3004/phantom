import os

from dotenv import load_dotenv

load_dotenv()

# 회사 프록시 SSL 인증서 설정
if os.getenv("SSL_CERT_FILE"):
    os.environ.setdefault("REQUESTS_CA_BUNDLE", os.environ["SSL_CERT_FILE"])

from deepagents import create_deep_agent


def main():
    agent = create_deep_agent(
        model="google_genai:gemini-2.5-flash",
        system_prompt="You are a helpful assistant.",
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Hello! Tell me about yourself."}]}
    )

    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
