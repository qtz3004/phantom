# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Phantom - DeepAgent 기반 에이전트 프로젝트.

## References

DeepAgent (LangChain) 문서가 `docs/deepagent/`에 로컬 저장되어 있습니다:

| 파일 | 내용 | 원본 URL |
|------|------|----------|
| `01-overview.md` | 개요, 핵심 기능 | https://docs.langchain.com/oss/python/deepagents/overview |
| `02-quickstart.md` | 빠른 시작 가이드 | https://docs.langchain.com/oss/python/deepagents/quickstart |
| `03-customization.md` | 모델, 도구, 미들웨어, 메모리 등 커스터마이징 | https://docs.langchain.com/oss/python/deepagents/customization |
| `04-backends.md` | 파일시스템 백엔드 (State, Filesystem, Store 등) | https://docs.langchain.com/oss/python/deepagents/backends |
| `05-sandboxes.md` | 격리 실행 환경 (Modal, Daytona, Runloop 등) | https://docs.langchain.com/oss/python/deepagents/sandboxes |
| `06-skills.md` | 스킬 시스템 | https://docs.langchain.com/oss/python/deepagents/skills |
| `07-subagents.md` | 서브에이전트 구성 및 패턴 | https://docs.langchain.com/oss/python/deepagents/subagents |
| `08-frontend.md` | 프론트엔드 UI 패턴 | https://docs.langchain.com/oss/python/deepagents/frontend/overview |
| `09-cli.md` | CLI 도구 사용법 | https://docs.langchain.com/oss/python/deepagents/cli/overview |

API 레퍼런스: https://reference.langchain.com/python/deepagents/

## 개발 서버 재시작

`scripts/` 아래의 bash 스크립트로 로컬 개발 서버를 관리한다.

| 스크립트 | 대상 | 포트 | 동작 |
|---------|------|------|------|
| `scripts/restart-backend.sh` | FastAPI 백엔드 (`server.py`) | 8000 | `pkill` 후 `uv run python server.py`로 재기동, `/health` 확인 |
| `scripts/restart-frontend.sh` | Next.js 프론트엔드 | 3000 | 프로세스 종료 + `.next`/`node_modules/.cache` 삭제 후 `npm run dev`, 브라우저 오픈 |
| `scripts/restart-all.sh` | 백엔드 + 프론트엔드 | 8000, 3000 | 위 두 스크립트를 순차 실행 |
| `scripts/stop-all.sh` | 전체 | - | 백엔드·프론트엔드 프로세스 모두 종료 |

- 로그: 백엔드 `logs/backend.log` (stdout `/tmp/backend-stdout.log`), 프론트엔드 `logs/frontend.log`
- "재시작해" / "프론트엔드·클라이언트 재시작" 류 요청은 기본적으로 `scripts/restart-all.sh`로 처리한다.
