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

# 4. .env 파일에 API 키 입력
# ANTHROPIC_API_KEY=sk-ant-...
# TAVILY_API_KEY=tvly-...

# 5. 실행
uv run main.py
```

> `uv`가 `.python-version` 파일을 보고 Python 3.12를 자동 설치합니다. 별도로 Python을 설치할 필요가 없습니다.
