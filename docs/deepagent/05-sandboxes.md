# Sandboxes

샌드박스는 에이전트 코드를 격리된 환경에서 실행합니다. 표준 파일시스템 도구 + `execute` 도구를 제공합니다.

## 지원 프로바이더

| 프로바이더 | 설치 | 특징 |
|-----------|------|------|
| AgentCore | `pip install langchain-agentcore-codeinterpreter` | AWS MicroVM 격리, Python |
| Modal | `pip install langchain-modal` | ML/AI 워크로드, GPU 접근 |
| Daytona | `pip install langchain-daytona` | TypeScript/Python, 빠른 콜드 스타트 |
| Runloop | `pip install langchain-runloop` | 일회용 devbox |

## 기본 사용법 (Modal 예제)

```python
import modal
from deepagents import create_deep_agent
from langchain_anthropic import ChatAnthropic
from langchain_modal import ModalSandbox

app = modal.App.lookup("your-app")
modal_sandbox = modal.Sandbox.create(app=app)
backend = ModalSandbox(sandbox=modal_sandbox)

agent = create_deep_agent(
    model=ChatAnthropic(model="claude-sonnet-4-20250514"),
    system_prompt="You are a Python coding assistant with sandbox access.",
    backend=backend,
)
try:
    result = agent.invoke({"messages": [{"role": "user", "content": "Create a small Python package and run pytest"}]})
finally:
    modal_sandbox.terminate()
```

## 수명 주기 관리

### Thread-Scoped (기본)
각 대화에 자체 샌드박스. 대화 정리 또는 TTL 만료 시 파괴.

### Assistant-Scoped
모든 스레드가 하나의 샌드박스 공유. 파일, 패키지, 저장소 등 상태 유지.

> **경고**: Assistant-scoped 샌드박스는 시간이 지남에 따라 상태가 축적됩니다. TTL 구성, 스냅샷 사용, 또는 정리 로직을 구현하세요.

## 통합 패턴

### Sandbox as Tool 패턴 (추천)

에이전트는 로컬에서 실행, 샌드박스 도구 호출은 프로바이더 API를 통해.

장점:
- 이미지 재빌드 없이 에이전트 코드 즉시 업데이트
- API 키가 샌드박스 외부에 유지
- 샌드박스 실패가 에이전트 상태에 영향 없음
- 여러 샌드박스 병렬 실행 가능

```python
from daytona import Daytona
from deepagents import create_deep_agent
from langchain_daytona import DaytonaSandbox

sandbox = Daytona().create()
backend = DaytonaSandbox(sandbox=sandbox)

agent = create_deep_agent(
    backend=backend,
    system_prompt="You are a coding assistant with sandbox access.",
)
```

## 보안 고려사항

**절대 시크릿을 샌드박스 안에 넣지 마세요.** API 키, 토큰, DB 자격증명 등은 context-injection 공격에 의해 읽히고 유출될 수 있습니다.

### 안전한 시크릿 처리

**옵션 1: 호스트 도구에 시크릿 유지 (추천)**
인증을 처리하는 도구를 호스트 환경에서 정의. 에이전트는 자격증명을 보지 않음.

**옵션 2: 네트워크 프록시 + 자격증명 주입**
일부 프로바이더가 아웃바운드 HTTP 요청에 자격증명을 자동 첨부하는 프록시 지원.

### 파일 전송

```python
# 샌드박스에 파일 업로드
backend.upload_files([
    ("/src/index.py", b"print('Hello')\n"),
    ("/pyproject.toml", b"[project]\nname = 'my-app'\n"),
])

# 샌드박스에서 파일 다운로드
results = backend.download_files(["/src/index.py", "/output.txt"])
```

> 원본: https://docs.langchain.com/oss/python/deepagents/sandboxes
