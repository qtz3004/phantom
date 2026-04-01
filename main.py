import os

from dotenv import load_dotenv

load_dotenv()

# 회사 프록시 SSL 인증서 설정
if os.getenv("SSL_CERT_FILE"):
    os.environ.setdefault("REQUESTS_CA_BUNDLE", os.environ["SSL_CERT_FILE"])

from langchain_google_genai import ChatGoogleGenerativeAI


def main():
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke("안녕")
    print(response.content)


if __name__ == "__main__":
    main()
