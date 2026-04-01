# Phantom

DeepAgent 기반 에이전트 프로젝트

## 사전 준비

### Git 설치

**Windows (Git이 없는 경우):**
```powershell
winget install Git.Git
```
또는 https://git-scm.com/downloads/win 에서 다운로드

**Mac:** Xcode Command Line Tools에 포함 (터미널에서 `git --version` 입력하면 자동 설치 안내)

### uv 설치

**Mac / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> 설치 후 터미널을 재시작하세요.

## 시작하기

```bash
# 1. 프로젝트 클론
git clone https://github.com/qtz3004/phantom.git
cd phantom

# 2. 의존성 설치 (Python 3.12 자동 설치됨)
uv sync

# 3. 환경변수 설정
cp .env.example .env
# Windows: copy .env.example .env

# 4. .env 파일에 API 키와 PEM 인증서 경로 입력
# GOOGLE_API_KEY=AIza...
# TAVILY_API_KEY=tvly-...
# SSL_CERT_FILE=/path/to/your-proxy.pem

# 5. 설치 확인
uv run hello.py

# 6. 실행
uv run main.py
```

> `uv`가 `.python-version` 파일을 보고 Python 3.12를 자동 설치합니다. 별도로 Python을 설치할 필요가 없습니다.

## 기대 결과

아래 결과가 나오면 환경 셋업이 완료된 것입니다.

### hello.py (설치 확인 - API 키 없이도 동작)

```
$ uv run hello.py
deepagents 설치 확인 OK!
deepagents version: 0.4.12

다음 단계: .env 파일에 API 키를 설정한 후 'uv run main.py'를 실행하세요.
```

### main.py (DeepAgent 실행 - API 키 필요)

```
$ uv run main.py
[{'type': 'text', 'text': 'Hello! I am a large language model, trained by Google.
I can help you with a wide range of tasks, from answering your questions and
providing information to assisting with creative writing and coding.
How can I help you today?'}]
```

> 위와 유사한 텍스트 응답이 출력되면 성공입니다. 응답 내용은 매번 달라질 수 있습니다.

## Claude Code 설치

위 환경 셋업이 완료된 후, Claude Code도 설치해야 합니다.

```bash
npm install -g @anthropic-ai/claude-code
```

> Node.js가 없는 경우: https://nodejs.org 에서 LTS 버전을 설치하세요.

설치 확인:

```bash
claude --version
```

프로젝트 디렉토리에서 실행:

```bash
cd phantom
claude
```
