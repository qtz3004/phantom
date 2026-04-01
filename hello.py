"""환경 설치 확인용 Hello World"""

from deepagents import create_deep_agent

print("deepagents 설치 확인 OK!")
print(f"deepagents version: {__import__('deepagents').__version__}")
print()
print("다음 단계: .env 파일에 API 키를 설정한 후 'uv run main.py'를 실행하세요.")
