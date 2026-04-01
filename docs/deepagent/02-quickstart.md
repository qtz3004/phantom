# 빠른 시작

> 몇 분 안에 첫 번째 딥 에이전트 구축하기

## 선행 조건

모델 제공자(예: Anthropic, OpenAI)의 API 키 확보. 딥 에이전트는 도구 호출을 지원하는 모델 필요.

## 1단계: 의존성 설치

```bash
pip install deepagents tavily-python
# 또는
uv init && uv add deepagents tavily-python && uv sync
```

## 2단계: API 키 설정

```bash
export ANTHROPIC_API_KEY="your-api-key"
export TAVILY_API_KEY="your-tavily-api-key"
```

## 3단계: 검색 도구 생성

```python
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """웹 검색 실행"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )
```

## 4단계: 딥 에이전트 생성

```python
research_instructions = """전문 연구자입니다. 철저한 조사를 수행한 후 정제된 보고서를 작성합니다.

인터넷 검색 도구에 접근 가능합니다.
"""

# Anthropic 사용
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[internet_search],
    system_prompt=research_instructions,
)

# OpenAI 사용
# agent = create_deep_agent(model="openai:gpt-5.4", ...)

# Google 사용
# agent = create_deep_agent(model="google_genai:gemini-3.1-pro-preview", ...)
```

## 5단계: 에이전트 실행

```python
result = agent.invoke({"messages": [{"role": "user", "content": "What is langgraph?"}]})
print(result["messages"][-1].content)
```

## 작동 원리

딥 에이전트는 자동으로 다음을 수행합니다:

1. **계획 수립**: 내장 `write_todos` 도구로 연구 작업 분해
2. **조사 수행**: `internet_search` 도구로 정보 수집
3. **컨텍스트 관리**: 파일 시스템 도구(`write_file`, `read_file`)로 대규모 검색 결과 오프로드
4. **서브에이전트 생성**: 복잡한 소작업을 특화된 서브에이전트에 위임
5. **보고서 합성**: 결과물을 일관성 있는 응답으로 컴파일

## 다음 단계

- **에이전트 커스터마이징**: 커스텀 시스템 프롬프트, 도구, 서브에이전트 포함 커스터마이징 옵션 학습
- **장기 메모리 추가**: 대화 간 지속형 메모리 활성화
- **프로덕션 배포**: LangGraph 애플리케이션 배포 옵션 학습

> 원본: https://docs.langchain.com/oss/python/deepagents/quickstart
