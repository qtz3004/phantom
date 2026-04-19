# Phantom

🔗 https://github.com/qtz3004/phantom

Claude Code, DeepAgent, CopilotKit을 활용한 에이전트 구축 데모.

---

## 1. Git 설치

**Mac:**
```bash
xcode-select --install
```

**Windows (PowerShell):**
```powershell
winget install --id Git.Git -e
```

확인: `git --version`

## 2. uv 설치

**Mac / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

확인: `uv --version`

## 3. 프로젝트 내려받기

```bash
git clone https://github.com/qtz3004/phantom.git
cd phantom
uv sync
```

## 4. 설치 확인

```bash
uv run hello.py
```

## 5. API 키 설정

```bash
cp .env.example .env
```

`.env`를 열어 키를 입력하세요:
```
GOOGLE_API_KEY=...
```

> 📌 API 키 / 사내망 PEM 인증서: https://konawiki.konai.com/pages/viewpage.action?pageId=424296262
>
> 사내망에서 SSL 에러 시 `.env`에 `SSL_CERT_FILE=/path/to/your-proxy.pem` 추가

## 6. Gemini 호출

```bash
uv run main.py
```

> LLM은 실시간 정보에 접근할 수 없어 "시간을 모른다"는 답이 자연스럽습니다. 다음 단계에서 Claude Code로 이 한계를 보완합니다.

## 7. Claude Code 실행

```bash
claude
```

> 사내망에서 SSL 에러 시 쉘 프로파일에 `export NODE_EXTRA_CA_CERTS="/path/to/your-proxy.pem"` 추가 후 터미널 재시작 (Node.js용, Python용 `SSL_CERT_FILE`과 별개).
