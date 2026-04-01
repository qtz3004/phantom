# Phantom

DeepAgent + Claude Code를 활용한 에이전트 구축 방법을 함께 살펴봅니다.

## 사전 준비

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

# 6. Google API 확인
uv run main.py

# 7. 프로젝트 디렉토리에서 Claude Code 실행
cd phantom
claude
```

> `uv`가 `.python-version` 파일을 보고 Python 3.12를 자동 설치합니다. 별도로 Python을 설치할 필요가 없습니다.

## 사전 준비 확인

**아래 3가지가 모두 정상 출력되어야 합니다. 시작 전에 반드시 확인해주세요.**

### 1. hello.py (설치 확인 - API 키 없이도 동작)

```
$ uv run hello.py
deepagents 설치 확인 OK!
deepagents version: 0.4.12

다음 단계: .env 파일에 API 키를 설정한 후 'uv run main.py'를 실행하세요.
```

### 2. main.py (Google API 키 확인)

```
$ uv run main.py
안녕하세요! 무엇을 도와드릴까요? 😊   ← 예시이며, 응답 내용은 매번 달라집니다
```

> Google Gemini의 텍스트 응답이 출력되면 성공입니다.

### 3. Claude Code 실행

```
$ cd phantom
$ claude

 ▐▛███▜▌   Claude Code v2.1.89
▝▜█████▛▘  Opus 4.6 · Claude Team
  ▘▘ ▝▝    ~/Workspace/07.lab/phantom

❯
```

> 위와 같이 Claude Code 배너가 출력되고 프롬프트(`❯`)가 나타나면 성공입니다.
