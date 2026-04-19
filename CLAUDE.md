# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Phantom - 딥에이전트, 클로드코드, 코파일럿킷을 활용한 에이전트 구축 데모 프로젝트.

## ⚠️ 주의: API 키 보안

**API 키가 소스 코드에 노출되지 않도록 특별히 신경쓰세요.**

- 키는 반드시 `.env` 파일에만 저장하고, 코드에 하드코딩하지 마세요.
- `.env`는 `.gitignore`에 포함되어 있으니 **절대 커밋하지 마세요**.
- 예시 문자열(`AIza...`, `sk-...` 등)도 실제 키 앞부분이 노출될 수 있으니 문서/주석에 쓰지 마세요.
- 커밋 전 `git diff`로 키가 포함되지 않았는지 반드시 확인하세요.
