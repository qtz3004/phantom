# Deep Agents CLI

Deep Agents SDK 기반 오픈소스 터미널 코딩 에이전트.

## 핵심 기능

- 파일 작업 (읽기, 쓰기, 편집)
- 셸 명령 실행
- 웹 검색 (Tavily API)
- HTTP 요청
- 작업 계획 및 추적
- 메모리 저장 및 검색
- 컨텍스트 압축 및 오프로딩
- Human-in-the-loop
- 스킬, MCP 도구
- LangSmith 추적

## 내장 도구

| 도구 | 설명 | HITL |
|------|------|------|
| `ls` | 파일/디렉토리 목록 | - |
| `read_file` | 파일 읽기 (이미지 멀티모달) | - |
| `write_file` | 파일 생성/덮어쓰기 | 필수 |
| `edit_file` | 기존 파일 편집 | 필수 |
| `glob` | 패턴 매칭 파일 검색 | - |
| `grep` | 텍스트 패턴 검색 | - |
| `execute` | 셸 명령 실행 | 필수 |
| `http_request` | HTTP 요청 | - |
| `web_search` | Tavily 웹 검색 | 필수 |
| `fetch_url` | 웹페이지 마크다운 변환 | 필수 |
| `task` | 서브에이전트 위임 | 필수 |
| `ask_user` | 사용자 질문 | - |
| `compact_conversation` | 메시지 요약/오프로딩 | 혼합 |
| `write_todos` | 작업 목록 관리 | - |

## 빠른 시작

```bash
# 설치
curl -LsSf https://raw.githubusercontent.com/langchain-ai/deepagents/refs/heads/main/libs/cli/scripts/install.sh | bash
# 또는
uv tool install 'deepagents-cli[ollama,groq]'

# 실행
deepagents

# 모델 지정
deepagents --model anthropic:claude-opus-4-5
```

## 비대화형 모드

```bash
deepagents -n "Write a Python script that prints hello world"
cat error.log | deepagents -n "What's causing this error?"
git diff | deepagents -n "Review these changes"
```

## 슬래시 명령어

| 명령어 | 설명 |
|--------|------|
| `/model` | 모델 전환 |
| `/remember` | 메모리/스킬 업데이트 |
| `/offload` | 컨텍스트 창 공간 확보 |
| `/tokens` | 토큰 사용량 표시 |
| `/clear` | 대화 기록 삭제 |
| `/threads` | 이전 스레드 탐색/재개 |
| `/reload` | 런타임 설정 새로고침 |
| `/trace` | LangSmith 추적 열기 |

## 설정 경로

| 경로 | 용도 |
|------|------|
| `~/.deepagents/config.toml` | 모델 기본값, 프로바이더 설정, 프로필 |
| `~/.deepagents/hooks.json` | 생명주기 이벤트 훅 |
| `~/.deepagents/<agent_name>/` | 에이전트별 메모리, 스킬, 스레드 |
| `.deepagents/` (프로젝트 루트) | 프로젝트별 메모리 및 스킬 |

## 에이전트 커스터마이징

### AGENTS.md 파일

- **전역**: `~/.deepagents/<agent_name>/AGENTS.md` — 모든 세션에 로드
- **프로젝트**: `.deepagents/AGENTS.md` — 해당 프로젝트에서만 로드

### 스킬 추가

```bash
# 사용자 스킬
deepagents skills create test-skill

# 프로젝트 스킬
deepagents skills create test-skill --project
```

스킬 발견 위치:
```
~/.deepagents/<agent_name>/skills/
~/.agents/skills/
.deepagents/skills/
.agents/skills/
```

### 커스텀 서브에이전트

```
.deepagents/agents/{subagent-name}/AGENTS.md   # 프로젝트
~/.deepagents/{agent}/agents/{subagent-name}/AGENTS.md  # 사용자
```

```markdown
---
name: researcher
description: Research topics on the web before writing content
model: anthropic:claude-haiku-4-5-20251001
---

You are a research assistant with access to web search.
```

## 원격 샌드박스

```bash
deepagents --sandbox daytona
deepagents --sandbox runloop --sandbox-id dbx_abc123
deepagents --sandbox modal --sandbox-setup ./setup.sh
```

## 주요 명령줄 옵션

| 옵션 | 설명 |
|------|------|
| `-a, --agent NAME` | 명명된 에이전트 사용 |
| `-M, --model MODEL` | 모델 지정 |
| `-r, --resume [ID]` | 세션 재개 |
| `-n, --non-interactive TEXT` | 비대화형 실행 |
| `-q, --quiet` | 정리된 출력 |
| `-y, --auto-approve` | 자동 승인 |
| `-S, --shell-allow-list` | 셸 명령 허용 목록 |
| `--sandbox TYPE` | 원격 샌드박스 사용 |

> 원본: https://docs.langchain.com/oss/python/deepagents/cli/overview
