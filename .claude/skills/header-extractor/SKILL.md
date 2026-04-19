---
name: header-extractor
description: Markdown 파일에서 #, ##, ### 헤더만 추출하여 knowledge_search 서브에이전트의 목차(tocs.md)와 원문(knowledge.md)을 생성한다. LLM 토큰 절감을 위해 전체 파일 대신 헤더만 먼저 읽는 2단계 패턴에 사용한다.
license: MIT
metadata:
  author: hsookim
  version: "0.2"
---

# header-extractor

Markdown 파일에서 `#`, `##`, `###` 헤더 라인을 추출하여 knowledge_search 서브에이전트용 목차/원문 파일을 생성한다. wiki-crawler 출력 파일과 함께 사용하여 LLM 토큰 비용을 절감하는 2단계 읽기 패턴을 구현한다.

## 입력

사용자로부터 **목차화할 소스 Markdown 파일 경로**를 받는다.

**입력이 없으면 즉시 작업을 중단하고 사용자에게 목차화할 Markdown 파일 경로를 입력해달라고 요청한다.** 임의의 파일로 진행하지 않는다.

## 출력 경로 (고정)

- 원문 복사본: `/Users/hsookim/Workspace/09.demo/phantom/subagents/knowledge_search/docs/knowledge.md`
- 목차: `/Users/hsookim/Workspace/09.demo/phantom/subagents/knowledge_search/docs/tocs.md`

두 파일 모두 매 실행마다 **덮어쓴다**.

## 2단계 읽기 패턴

```
1단계: tocs.md만 읽어 헤더의 제목과 라인 범위 확인 (토큰 절감)
  → 사용자 질문과 시맨틱하게 매칭되는 섹션 선택

2단계: knowledge.md에서 해당 섹션의 라인 범위로 본문 읽기
  → `라인: start-end` 범위로 해당 섹션만 read
  → `참조: ref_start-ref_end` 범위로 출처/첨부도 함께 read
```

## Instructions

1. 사용자로부터 소스 Markdown 파일 경로를 입력받는다. 없으면 즉시 요청하고 중단한다.
2. 소스 파일을 읽는다.
3. 본문 내 모든 `| 파일명: <원본>.md |` 표기를 `| 파일명: knowledge.md |`로 치환한다.
   - h1 헤더뿐 아니라 h2/h3에 파일명이 포함된 경우도 모두 치환한다.
4. 치환된 본문을 `subagents/knowledge_search/docs/knowledge.md`에 덮어쓴다.
5. 치환된 본문에서 `#`, `##`, `###`으로 시작하는 헤더 라인과 `> 출처:`, `> 첨부:` 메타 라인을 추출한다.
6. 각 추출 라인에 원본 라인 번호(`L{N}:` 접두사)를 부여해 목차 텍스트를 만든다.
7. 목차를 `subagents/knowledge_search/docs/tocs.md`에 덮어쓴다.
8. 완료 후 처리 요약(원본 경로, 추출된 헤더 수, 출력 파일 경로)을 보고한다.

## 출력 형식 (tocs.md)

```
L1: # 제목 | 파일명: knowledge.md | 라인: 1-N | 참조: ref_start-ref_end
L3: > 출처: [Wiki 페이지 (pageId: xxx)](URL)
L4: > 첨부: [파일명.pdf](다운로드URL)
L6: ## 섹션1 제목 | 라인: 6-17 | 참조: 3-4
L19: ## 섹션2 제목 | 라인: 19-27 | 참조: 3-4
...
```

## 설계 원칙

- **파일명은 항상 `knowledge.md`로 고정**: knowledge_search 서브에이전트가 단일 원문을 대상으로 동작하므로 파일명을 고정해 본문·목차 내 파일명 참조가 항상 일치하도록 한다.
- **소스 파일 자체는 변경하지 않는다**: 원본은 보존하고 치환본만 출력 경로에 저장한다.
- **매 실행 덮어쓰기**: 서브에이전트가 바라보는 knowledge 문서는 "가장 최근에 지정된 1개"임을 전제로 한다.
