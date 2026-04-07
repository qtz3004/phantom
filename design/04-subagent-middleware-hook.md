# 04. 서브에이전트 미들웨어 훅 설계

## 개요

오케스트레이터와 서브에이전트 사이에 미들웨어 훅을 두어,
서브에이전트가 질문을 받으면 TOC(헤더 목차)를 자동 주입하고,
LLM이 선택한 헤더의 본문과 참조를 자동 grab하여 오케스트레이터에 반환하는 구조.
서브에이전트는 답변을 생성하지 않고 원문 데이터만 반환하며,
오케스트레이터가 사용자 질문에 맞게 요약하여 최종 답변을 생성한다.

## 전체 흐름

```
사용자 질문
  → 오케스트레이터 (golden-cabbage)
    → 맥락 포함 자립적 질문으로 재구성
    → 적절한 서브에이전트로 위임

  → 서브에이전트 (oil-subsidy-guide)
    → [Before Hook] TOC 자동 주입
    → LLM이 TOC에서 관련 헤더 선택
    → [After Hook] 선택된 헤더(복수 가능)의 본문 + 참조 grab
    → grab된 원문 데이터를 오케스트레이터에 반환

  → 오케스트레이터
    → 사용자 질문과 반환된 원문을 매칭
    → 간결하게 요약하여 최종 답변 생성
```

## 서브에이전트 문서 폴더 구조

각 서브에이전트는 자체 `docs/` 폴더를 가진다.
wiki-crawler 출력 파일을 이 폴더에 복사하여 사용한다.

```
subagents/
├── oil_subsidy/
│   ├── __init__.py
│   ├── oil_subsidy.py        # 서브에이전트 정의, 도구, 미들웨어
│   └── docs/                 # 문서 폴더 (사용자가 직접 복사)
│       ├── 422767515.md      # wiki-crawler 출력 원본
│       └── ...               # 추가 문서
```

## Before Hook: TOC 자동 주입

### 동작

1. 서브에이전트에 질문이 들어오면 Before Hook이 실행된다
2. `docs/` 폴더 내 모든 `.md` 파일을 재귀 탐색한다
3. 각 파일에서 `#`, `##`, `###` 헤더만 추출한다 (header-extractor 로직 재사용)
4. 추출된 TOC를 질문과 함께 LLM에 전달한다

### LLM에 전달되는 형식

```
[사용자 질문]
고유가 피해지원금 대상자는 누구인가요?

[참고 문서 목차]
L1: # 2026년 중동전쟁 위기 극복을 위한 고유가 피해지원금 참여사 설명자료 | 파일명: 422767515.md | 라인: 1-50 | 참조: 3-4
L6: ## 고유가 피해지원금은 소득하위 70% 국민에게 1인당 10~60만원을 지역화폐로 지급하는 4.8조원 규모의 사업이다 | 파일명: 422767515.md | 라인: 6-17 | 참조: 3-4
L19: ## 참여사는 4월 6일까지 참여 여부를 회신해야 하며 ... | 파일명: 422767515.md | 라인: 19-27 | 참조: 3-4
...
```

### LLM 응답 형식

LLM은 관련 헤더를 선택하여 다음 형식으로 응답한다.
**복수 섹션 선택이 가능**하며, SELECT를 여러 줄 작성한다:

```
SELECT: 422767515.md | 라인: 6-17 | 참조: 3-4
SELECT: 422767515.md | 라인: 34-40 | 참조: 3-4
```

전체적인 질문(예: "고유가 피해지원금이 뭐야?")의 경우 `#` 헤더를 선택하여
문서 전체를 반환할 수 있다:

```
SELECT: 422767515.md | 라인: 1-50 | 참조: 3-4
```

## After Hook: 본문 + 참조 Grab

### 동작

1. LLM 응답에서 `SELECT:` 패턴을 파싱한다
2. 파일명, 라인 범위, 참조 범위를 추출한다
3. `docs/` 폴더를 재귀 탐색하여 해당 파일을 찾는다
4. 파일에서 라인 범위와 참조 범위를 grab한다
5. grab된 내용을 LLM에 반환하여 최종 답변을 생성한다

### 파싱 규칙

```
SELECT: {파일명} | 라인: {start}-{end} | 참조: {ref_start}-{ref_end}
```

- `파일명`: docs/ 폴더에서 재귀 검색할 파일명
- `라인: start-end`: 본문 내용을 grab할 범위
- `참조: ref_start-ref_end`: 출처/첨부를 grab할 범위

### Grab 결과 형식

```
[본문] (422767515.md, 라인 6-17)
- 고유가·고물가로 인한 서민층의 이중 부담 경감이 목적
- 기초·차상위가구는 1차로 우선 지급, 건보료 등을 통해 ...
...

[참조] (422767515.md, 라인 3-4)
> 출처: [Wiki 페이지 (pageId: 422767515)](URL)
> 첨부: [2026년 고유가 피해지원금 참여사 설명자료_26.04.02.pdf](URL)
```

### 파일 미발견 시

```
해당 문서(xxx.md)를 찾을 수 없어 답변할 수 없습니다.
```

## 미들웨어 구현 (DeepAgent 패턴)

DeepAgent의 `@wrap_tool_call` 미들웨어 패턴을 활용한다.

```python
from langchain.agents.middleware import wrap_tool_call

@wrap_tool_call
def toc_inject_middleware(request, handler):
    """Before: TOC 주입 → LLM 처리 → After: 본문 grab"""
    # Before Hook: TOC 주입
    toc = build_toc_from_docs(docs_dir)
    request.messages.append(toc_message)

    # LLM 처리
    result = handler(request)

    # After Hook: SELECT 패턴 파싱 → grab
    if "SELECT:" in result.content:
        grabbed = grab_section(result.content, docs_dir)
        return grabbed

    return result
```

## 핵심 함수

| 함수 | 역할 | 위치 |
|------|------|------|
| `build_toc_from_docs(docs_dir)` | docs/ 폴더 전체 헤더 추출 → TOC 생성 | `subagents/oil_subsidy.py` |
| `find_file(filename, docs_dir)` | docs/ 하위 재귀 탐색으로 파일 찾기 | `subagents/oil_subsidy.py` |
| `grab_lines(file_path, start, end)` | 파일에서 지정 라인 범위 추출 | `subagents/oil_subsidy.py` |
| `parse_select(response)` | LLM 응답에서 SELECT 패턴 파싱 | `subagents/oil_subsidy.py` |

## 오케스트레이터 역할

오케스트레이터는 사용자의 질문을 서브에이전트에 위임할 때,
**맥락을 포함한 자립적 질문**으로 재구성하여 전달한다.

### 예시

```
사용자: "대상자가 누구야?"
  ↓ (대화 맥락: 고유가 피해지원금 논의 중)
오케스트레이터 → 서브에이전트: "고유가 피해지원금의 지원 대상자는 누구인가요?"
```

이를 통해 서브에이전트는 대화 히스토리 없이도 독립적으로 답변할 수 있다.

## 수정 대상 파일

- `agent.py` — 오케스트레이터 시스템 프롬프트에 자립적 질문 재구성 지침 추가
- `subagents/oil_subsidy.py` — Before/After 미들웨어 훅 구현, docs/ 폴더 탐색 로직
- `prompts/orchestrator.md` — 자립적 질문 재구성 규칙 명시
- `prompts/oil_subsidy_guide.md` — TOC 기반 섹션 선택 및 SELECT 응답 형식 지침 추가
