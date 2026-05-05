# Phantom

🔗 https://github.com/qtz3004/phantom

Claude Code, DeepAgent, CopilotKit을 활용한 에이전트 구축 데모.

---

## 이 프로젝트의 목적

**"왜 LLM이 아니라 에이전트인가"** 를 손에 잡히는 한 문장으로 보여주기 위한 실습 프로젝트입니다.

가장 단순한 비교는 **"지금 몇 시야?"** 입니다.

- **LLM 단독 호출** — 학습 데이터의 시점에 갇혀 있어 *현재 시각을 알 수 없습니다.* "지금 시간을 알 수 없다" 고 답하거나, 더 위험하게는 그럴듯한 가짜 시각을 만들어 답합니다.
- **DeepAgent (이 프로젝트)** — `get_current_time` 같은 **도구(tool)** 를 LLM에 연결해 두면, 모델이 "이건 내가 모르는 정보네 → 도구를 부르자" 라고 판단해 실시간 시각을 가져와 답합니다.

이 한 가지 차이가 "단발 채팅 모델" 과 "에이전트 시스템" 의 본질적인 분리선입니다. 이 실습은 그 출발점 — **현재 시각을 정확히 답하는 한 가지 일** 만 하는 작은 에이전트를 직접 만들어 보는 데서 시작합니다.

> 핵심 한 줄: **"LLM은 모르는 것을 모르는 채로 답하고, 에이전트는 모르는 것을 도구로 알아내서 답한다."**

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

## 8. 첫 실습 — Claude Code 에 줄 한 줄 명령어

Claude Code 가 떴다면, 아래 한 단락을 그대로 붙여넣어 보세요. Claude 가 두 스펙(프론트/서버)을 읽고 `get_current_time` 도구가 달린 에이전트 + 채팅 UI 까지 한 번에 구성해 줍니다.

> `@docs/copilotkit/` 를 **프론트엔드 스펙**으로,
> `@docs/deepagent/` 를 **서버(에이전트) 스펙**으로 참고해서,
> 사용자가 "지금 몇 시야?" 라고 물으면 **실제 현재 시각** 을 답하는
> DeepAgent 기반 백엔드 에이전트를 만들고 CopilotKit 프론트엔드와 연결해 주세요.

(LLM 만으로는 답할 수 없는 "현재 시각" 을 도구 호출로 해결한다 — 이 한 가지 시연이 에이전트 시스템의 출발점입니다.)
