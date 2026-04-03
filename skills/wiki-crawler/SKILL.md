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

## Instructions

1. `credentials.yaml`에서 Wiki 인증 정보를 읽는다
2. 전달받은 URL에서 `pageId`를 추출한다
3. Confluence REST API로 페이지 본문을 가져온다
   - `GET {base_url}/rest/api/content/{pageId}?expand=body.storage,metadata.labels`
   - Basic Auth 사용
4. HTML 본문을 구조화된 섹션으로 파싱한다
   - 테이블 → Markdown 테이블
   - 첨부파일 링크 → 다운로드 URL로 변환
   - Confluence 매크로 → 텍스트로 변환
5. 각 섹션에 뉴스 기사형 완전한 제목을 생성한다
   - 사용자 질문과 시맨틱 비교가 가능하도록 서술형 제목
   - 예: "코나 결제 시스템의 전체 아키텍처와 구성 요소"
6. 출력 파일을 생성한다
   - 소규모 페이지: 단일 `{pageId}.md` 파일
   - 대규모 페이지 (200줄 초과): h2 단위로 분할
     - 인덱스: `{pageId}_index.md`
     - 섹션: `{pageId}_{번호}_{슬러그}.md`
7. 모든 헤더에 파일명과 라인 정보를 포함한다
   - h1: `# 제목 | 파일명: xxx.md | 라인수: N`
   - h2+: `## 제목 | 라인: start-end`

## 출력 경로

`skills/wiki-crawler/output/` 디렉토리에 저장한다.

## 인증

`skills/wiki-crawler/credentials.yaml` 파일을 읽는다. 이 파일은 `.gitignore` 대상이다.

```yaml
wiki:
  base_url: https://konawiki.konai.com
  username: your-id
  password: your-password
```
