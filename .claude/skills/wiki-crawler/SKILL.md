---
name: wiki-crawler
description: 회사 Wiki(Confluence) 페이지를 크롤링하여 LLM 최적화된 Markdown 문서로 변환
license: MIT
compatibility: 회사 내부 네트워크 접근 필요
metadata:
  author: hsookim
  version: "0.1"
allowed-tools: http_request, read_file, write_file
---

# wiki-crawler

회사 Confluence Wiki 페이지를 파싱하여 LLM이 효율적으로 검색·이해할 수 있는 구조화된 Markdown으로 변환한다.

## 입력

사용자는 Wiki URL 또는 `pageId`(숫자)를 전달한다. 페이지에 본문/첨부파일/표 중 무엇이 있든 **모두 동일한 방식**으로 추출·정규화하여 하나의 Markdown 문서로 통합한다.

**입력이 없으면 즉시 작업을 중단하고 사용자에게 Wiki URL 또는 pageId를 입력해달라고 요청한다.** 추측해서 임의의 pageId로 진행하지 않는다.

## Instructions

1. `credentials.yaml`에서 Wiki 인증 정보를 읽는다
2. 전달받은 입력에서 `pageId`를 추출한다 (URL이면 쿼리스트링 또는 경로에서 파싱)
3. Confluence REST API로 페이지 데이터를 가져온다
   - 본문: `GET {base_url}/rest/api/content/{pageId}?expand=body.storage,metadata.labels`
   - 첨부 목록: `GET {base_url}/rest/api/content/{pageId}/child/attachment`
   - Basic Auth 사용
4. **모든 콘텐츠 소스를 동일한 섹션 구조로 변환**한다. 소스별 취급 방식은 다르지만 출력 형식은 같다:
   - **페이지 본문(HTML)**: h1/h2/h3 헤더를 그대로 섹션 경계로 사용. 테이블은 Markdown 표로, Confluence 매크로는 텍스트로 변환
   - **첨부파일**: 다운로드 후 텍스트 추출
     - PDF → 텍스트/표 추출 (pdfplumber, pdfminer 등)
     - 이미지/다이어그램 → OCR 또는 캡션/설명을 섹션으로 포함
     - Office 문서(xlsx, docx, pptx) → 텍스트/표 추출
   - **표(본문 내 표, 첨부 내 표)**: 모두 Markdown 표로 변환하여 해당 섹션에 포함
5. 각 섹션에 뉴스 기사형 완전한 제목을 생성한다
   - 사용자 질문과 시맨틱 비교가 가능하도록 서술형 제목
   - 예: "코나 결제 시스템의 전체 아키텍처와 구성 요소"
   - 본문·첨부·표 어디서 왔는지와 무관하게 동일 규칙 적용
6. 출력 파일을 생성한다
   - 소규모 페이지: 단일 `{pageId}.md` 파일
   - 대규모 페이지 (200줄 초과): h2 단위로 분할
     - 인덱스: `{pageId}_index.md`
     - 섹션: `{pageId}_{번호}_{슬러그}.md`
7. 모든 헤더에 파일명, 라인 범위, 참조 라인 정보를 포함한다
   - h1: `# 제목 | 파일명: xxx.md | 라인: 1-N | 참조: ref_start-ref_end`
   - h2+: `## 제목 | 라인: start-end | 참조: ref_start-ref_end`
8. 출처와 첨부 정보는 h1 바로 아래에 1회만 기재한다
   - `> 출처: [Wiki 페이지 (pageId: xxx)](URL)`
   - `> 첨부: [파일명](다운로드URL)` (첨부마다 한 줄씩, 여러 개면 반복)
   - h2 헤더의 `참조:`는 출처/첨부가 있는 라인 범위를 가리킨다
   - Python 스크립트가 h2 섹션을 grab할 때 본문(`라인:`)과 메타정보(`참조:`)를 함께 추출할 수 있다
   - 파일 분할 시에는 각 분할 파일의 h1 아래에 출처/첨부를 포함하여 독립적으로 추적 가능하게 한다

## 통합 규칙

- 본문 섹션과 첨부 섹션은 섞어서 배치하지 않는다. 본문에서 파생된 섹션을 먼저, 첨부에서 파생된 섹션을 뒤에 둔다
- 첨부에서 파생된 섹션의 제목에는 출처 파일명을 **붙이지 않는다** (제목은 내용 기반 서술형 유지). 대신 h1 아래 `> 첨부:` 라인으로 추적
- 본문과 첨부의 내용이 중복되면 **본문을 우선**하고 첨부에서 새로 추가된 정보만 별도 섹션으로 기록한다

## 참조 포맷 (필수)

출력 Markdown은 항상 `.claude/skills/wiki-crawler/output/sample.md`의 구조를 템플릿으로 삼아 생성한다. sample.md는 **h2 헤더 라인만 훑어봐도 사용자 질문과 시맨틱 매칭**해 필요한 섹션을 특정할 수 있도록 설계된 기준 샘플이다. (후속으로 header-extractor가 이 헤더들을 뽑아 tocs.md를 만든다.)

구체적으로 sample.md를 따라 맞출 요소:

- h1/h2 헤더의 `| 파일명: ... | 라인: ... | 참조: ... |` 메타 표기
- h1 바로 아래 `> 출처:`, `> 첨부:` 한 줄 기재 규칙
- 각 h2 제목은 **완결된 뉴스 기사형 서술문**이어야 한다. 단순 명사·축약 코드만 넣지 말고 질문에 그대로 매칭될 수 있는 키워드·요지를 포함한다.
  - 컴포넌트/객체 목록 페이지라면 `## {CODE} ({Full Name}) — {한 줄 요약} | ...` 처럼 코드·정식명·요약을 함께 넣어 개별 항목 단위로 질의할 수 있게 한다.
  - 일반 서술 페이지라면 사용자 질문형(주어+핵심내용)으로 제목을 쓴다.
- 섹션 본문은 짧은 불릿 위주로 작성하되, 표가 필요하면 sample.md처럼 Markdown 표를 섹션 내부에 포함시킨다.

원문 작성 시 다음을 점검한다: **출력 파일의 h2 헤더 라인만 훑어서 각 섹션이 어떤 질문에 답하는지 판별 가능한가?** 아니라면 제목을 다시 쓴다.

## 출력 경로

`.claude/skills/wiki-crawler/output/` 디렉토리에 저장한다. 파일명은 `{pageId}.md`.

## 인증

`.claude/skills/wiki-crawler/credentials.yaml` 파일을 읽는다. 이 파일은 `.gitignore` 대상이다.

```yaml
wiki:
  base_url: https://konawiki.konai.com
  username: your-id
  password: your-password
```
