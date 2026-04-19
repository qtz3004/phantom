# 코나카드 결제 플랫폼 CORE 컴포넌트 143종의 개별 카탈로그 | 파일명: knowledge.md | 라인: 1-2107 | 참조: 3-3

> 출처: [Wiki 페이지 (pageId: 64690600)](https://konawiki.konai.com/pages/viewpage.action?pageId=64690600)

코나카드 결제 플랫폼을 구성하는 CORE 컴포넌트 143개의 개별 카탈로그다. 각 컴포넌트마다 독립된 h2 섹션으로 정리되어 있으며, 섹션 제목에 컴포넌트 코드·정식명·한 줄 요약을 모두 포함해 컴포넌트명으로 시맨틱 검색이 가능하도록 구성했다. 섹션 본문은 정식명, 에러코드, 결제데이터 보유 여부, 보존기간, 담당자, 상세 설명을 동일한 구조로 제공한다. Component Name 알파벳 순이 아닌 Wiki 원문 등록 순서를 유지한다.

## AMLS (AML Service) — AML 연계 서비스 | 라인: 7-20 | 참조: 3-3

- 정식명: AML Service
- 에러코드 ID: 150
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 하승원(SeungWon Ha)
- 설명(Korean):
  - AML 연계 서비스
  - 코나카드 결제 플랫폼과 AML 솔루션을 연계
- 설명(English):
  - AML Interface Service
  - Interface Service Between KonaCard And AML Solution

## ACS (Accumulation Calculation System) — 누적 시스템 | 라인: 21-36 | 참조: 3-3

- 정식명: Accumulation Calculation System
- 에러코드 ID: 39
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 하승원(SeungWon Ha)
- 설명(Korean):
  - 누적 시스템
  - 거래에 대한 누적 정보를 관리함
  - 누적 정보 기준으로 각 종 이벤트에 제공될 수 있도록 함
- 설명(English):
  - Cumulative system
  - Manage cumulative information on transactions
  - Provided to various events based on accumulated information

## AGS (Authorization Gateway Service) — 인증 게이트웨이 서비스 컴포넌트 | 라인: 37-50 | 참조: 3-3

- 정식명: Authorization Gateway Service
- 에러코드 ID: 41
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 김현수(HyunSoo Kim)
- 설명(Korean):
  - 인증 게이트웨이 서비스 컴포넌트
  - JWT Token 을 사용하여 인증된 API 만 특정 서버로 Routing 수행
- 설명(English):
  - Authorization Gateway Service
  - Routing only authenticated API using JWT Token to a specific server

## APIGW (API Gateway) — 앱 요청 게이트웨이 서비스 컴포넌트 | 라인: 51-63 | 참조: 3-3

- 정식명: API Gateway
- 에러코드 ID: 30
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 김현수(HyunSoo Kim) · 장성우(Sungwoo Jang)
- 설명(Korean):
  - 앱 요청 게이트웨이 서비스 컴포넌트
  - 사용자 월렛과 서비스 서버간의 세션을 관리하며, 사용자 월렛의 다양한 API 호출을 각 Component 에 라우팅 한다. 또한 보안키보드 관련 작업과 API 버전을 관리한다. 최종 응답단계에서 동일한 포맷으로 에러메시지를 변경후 각국의 언어에 맞게 지역화 시킨다. 현재는 국문/일문/중문/영문 에러메시지를 제공한다.
- 설명(English):
  - Route api call from wallet to service layer and core component. Handle secure keyboard related operation. Uniform error response and provide localized error message

## APS (Authentication processing server) — 코나카드의 충전단말기의 거래를 인증하기 위한 보안수단으로 Card Activation 및 충전/충전취소 거래 시 단말기에 설치된 SAM으로... | 라인: 64-75 | 참조: 3-3

- 정식명: Authentication processing server
- 에러코드 ID: 없음
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 박병건(Byounggun Park)
- 설명(Korean):
  - 코나카드의 충전단말기의 거래를 인증하기 위한 보안수단으로 Card Activation 및 충전/충전취소 거래 시 단말기에 설치된 SAM으로 연산된 MAC값을 검증한다.
- 설명(English):
  - Verify Mac value computed by SAM, which is connected to charging terminal, when Card Activation, Charging and Charging cancellation. This is a security method to authenticate transaction b/w KonaCard and Charging terminal.

## BAS (Bconline Authentication Service) — BC온라인거래 발생 시 코나카드 별도로 내부검증이 필요하다. 이 때 사용되는 Cryptogram을 생성한다. | 라인: 76-87 | 참조: 3-3

- 정식명: Bconline Authentication Service
- 에러코드 ID: 57
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 권수연(SooYeon Kwon)
- 설명(Korean):
  - BC온라인거래 발생 시 코나카드 별도로 내부검증이 필요하다. 이 때 사용되는 Cryptogram을 생성한다.
- 설명(English):
  - Internal verification is required when Bc Online Transaction is occured. BAS generate cryptogram value which is used for this transaction case.

## VVAN (Virtual-Value Addition Network) — 가맹점/단말기 검증 | 라인: 88-111 | 참조: 3-3

- 정식명: Virtual-Value Addition Network
- 에러코드 ID: 26
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 권수연(SooYeon Kwon)
- 설명(Korean):
  - 가맹점/단말기 검증
  - van사 역할 대행
  - 단말기 개통/정보 수정
  - 단말기 및 가맹점 검증
  - 온라인/오프라인 결제거래 검증
  - ISO8583 형식 검증
  - 거래 검증 및 결제 로직 수행
  - 코나샵/캐시비
- 설명(English):
  - verify merchant/cat or pos terminal
  - verify status of affiliate and terminal
  - open terminal and correct its information.
  - verify online/offline payment transaction
  - ISO8583 full text format
  - kona direct payment/cashbee

## BGS (Bank Gateway Service) — 은행 게이트웨이 서비스 컴포넌트 | 라인: 112-125 | 참조: 3-3

- 정식명: Bank Gateway Service
- 에러코드 ID: 40
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 김현수(HyunSoo Kim) · 김병수(Byeongsu Kim)
- 설명(Korean):
  - 은행 게이트웨이 서비스 컴포넌트
  - 은행 Gateway 컴포넌트 로서, 은행에서 제공하는 API 기반으로 은행 업무 로직을 수행
- 설명(English):
  - Bank Gateway Service
  - As a bank gateway component, it performs banking logic based on the API provided by the bank.

## BIZB (business Batch server) — 행안부 데이터(dis) ↔ 비즈포탈에서 승인할 수 있는 데이터 | 라인: 126-140 | 참조: 3-3

- 정식명: business Batch server
- 에러코드 ID: 95
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: Retired_박도경(Dokyung Park)
- 설명(Korean):
  - 행안부 데이터(dis) ↔ 비즈포탈에서 승인할 수 있는 데이터
  - 를 변환하여 양쪽에 업데이트 쳐주는 서버
  - 행안부 데이터를 코나카드 정보와 결합하여 비즈포탈에 넘겨주고 반대로 지급 이후에는 지급이력을 행안부 데이터에 업데이트 치는 역할을 하고 있다.
  - 온라인 신청/오프라인 신청 각각 배치를 통해 승인 데이터를 만들고 있음
- 설명(English):
  - A component which transform Goverment data into biz portal data so that kona operator can see and confirm the rechargeable data.

## BIZS (business portal API server) — BPP(business portal platform)의 데이터와 코나카드 코어와의 데이터 통신을 위한 API 서버(월렛서버에 떠있음). 주... | 라인: 141-153 | 참조: 3-3

- 정식명: business portal API server
- 에러코드 ID: 62
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 곽용기(Yongkee Kwak)
- 설명(Korean):
  - BPP(business portal platform)의 데이터와 코나카드 코어와의 데이터 통신을 위한 API 서버(월렛서버에 떠있음). 주로 BPP만 가지고 있는 정보(정책수당 수혜자 정보)의 검증(수당 대상자가 맞는지)이 필요할 때 사용된다.
  - 카드등록, 카드교체 액션이 일어날 때 수당 지급을 위해 비즈서버에도 저장하려고 호출되며, 매일 배치를 통해 지급일에 도달한 수당을 지급하는 일도 하고있다.
- 설명(English):
  - Api server for BPP to communicate with core components. Especially used for checking if he/she is right person to receive money and provide/withdraw point or balance.

## BTS (Barcode Translator Service) — QR코드 정보 생성을 위한 서버 컴포넌트 | 라인: 154-165 | 참조: 3-3

- 정식명: Barcode Translator Service
- 에러코드 ID: 106
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 유정현 (JungHyun Yoo)
- 설명(Korean):
  - QR코드 정보 생성을 위한 서버 컴포넌트
- 설명(English):
  - Server component for generating QR code information

## CA (Certificate Authority) — 인증서발급 및 전자서명을 위한 컴포넌트로, Portal에서 상품 및 가맹점을 등록/승인할 때 사용한다. | 라인: 166-177 | 참조: 3-3

- 정식명: Certificate Authority
- 에러코드 ID: 없음
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: KSL
- 설명(Korean):
  - 인증서발급 및 전자서명을 위한 컴포넌트로, Portal에서 상품 및 가맹점을 등록/승인할 때 사용한다.
- 설명(English):
  - Use as a component for certificate issuance and digital signature when registering and approving products and affiliates at portal.

## CAMS (card application manage system) — 체크 카드 신청 및 발급을 관리한다. | 라인: 178-189 | 참조: 3-3

- 정식명: card application manage system
- 에러코드 ID: 68
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 홍주표(Joopyo Hong)
- 설명(Korean):
  - 체크 카드 신청 및 발급을 관리한다.
- 설명(English):
  - A component to manage check card issue and status.

## PMS (pocket money management service) — 용돈 관리 서비스를 제공한다. | 라인: 190-201 | 참조: 3-3

- 정식명: pocket money management service
- 에러코드 ID: 112
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 유정현 (JungHyun Yoo)
- 설명(Korean):
  - 용돈 관리 서비스를 제공한다.
- 설명(English):
  - Provide pocket money management service.

## CARDSE (CardSE) — 실물카드(CardSE)의 발급과 폐기를 관리하고, 실물카드(CardSE)와 모바일카드(HCE 카드)의 연결 또는 복제 기능을 제공한다. | 라인: 202-214 | 참조: 3-3

- 정식명: CardSE
- 에러코드 ID: 32
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: Norun Nobi
- 설명(Korean):
  - 실물카드(CardSE)의 발급과 폐기를 관리하고, 실물카드(CardSE)와 모바일카드(HCE 카드)의 연결 또는 복제 기능을 제공한다.
- 설명(English):
  - - Batch Raw data generation controls, Batch Tokenization,
  - Download new HCE card with CardSE, Connect anactiveCardsewithan active HCE, Activate/Deactivate CardSE in the system after issuance

## CDM (Card Delivery Management(System)) — 웰컴 카드, 정책수당카드 등 코나카드의 배송을 관리하는 컴포넌트로, App에서 회원가입 완료시 신청한 정보(혹은 EDM, CALL, BIZ... | 라인: 215-229 | 참조: 3-3

- 정식명: Card Delivery Management(System)
- 에러코드 ID: 54
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 서용하(Yongha Seo)
- 설명(Korean):
  - 웰컴 카드, 정책수당카드 등 코나카드의 배송을 관리하는 컴포넌트로, App에서 회원가입 완료시 신청한 정보(혹은 EDM, CALL, BIZ 등에서 넘어온 정보)를 코나C공장으로 전달하여 다음날 배치를 통해 배송이 되도록 한다. 배송 후 공장의 완료파일을 읽어 상태 값/카드번호 등을 업데이트 치고 있다.
  - 또한 배송신청데이터를 앱/포탈 등에 보여주기 위한 조회 API를 제공하고 있다. 비용부과카드 구매, 재발급구매카드 신청 시 비용한 금액 등도 관리한다.
  - (단,코나샵의 카드 배송과 무관)
- 설명(English):
  - A component to manage deliveries of KonaCard such as welcome card, Acuon card, SKT card and Pentaport card.
  - Have Kimpo factory deliver by sending requested batch information which is from other companies after signing up at APP. This is irrelevant to KONA Shop's delivery.

## CLR (Clearing) — 코나카드 정산 컴포넌트 | 라인: 230-245 | 참조: 3-3

- 정식명: Clearing
- 에러코드 ID: 83
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 서버개발 4팀
- 설명(Korean):
  - 코나카드 정산 컴포넌트
  - 코나카드 거래 데이터를 기반으로 계약서에 의거하여 수수료 및 대금을 확정하고 확정된 대금에 대한 지급 데이터 생성, 지급에 대한 근거 자료를 생성한다.
  - 거래 데이터는 승인단에서 정산에 필요한 원장 데이터를 파일 형태로 전달받고 부가적인 데이터는 관련 컴포넌트에 저장된 정보를 이용한다.
  - 정산은 서비스 운영에 영향을 미치지 않도록 비교적 거래가 적은 새벽 시간 대에 배치로 수행된다.
- 설명(English):
  - Confirm commission and payment amount based on Konacard's transaction data.
  - Create payment data for confirmed payment amount and its related evidences.

## CRMS (Corporation Recharge Management Service) — 법인 계좌 출금이체후 카드에 충전 컴포넌트 | 라인: 246-260 | 참조: 3-3

- 정식명: Corporation Recharge Management Service
- 에러코드 ID: 86
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 김현수(HyunSoo Kim)
- 설명(Korean):
  - 법인 계좌 출금이체후 카드에 충전 컴포넌트
  - 쿠콘 출금이체 수행후, 카드 충전 요청 수행
  - 실제 서비스는 HOLD 되었으나, 법인 계좌 출금 요청을 수행하고 있음
  - (출금이체 API, 충전 API, 출금이체 + 충전 API 가 분리되어 있음
- 설명(English):
  - Corporation Recharge Management Service

## CMS (Card Management System) — 카드 원장 관리 | 라인: 261-281 | 참조: 3-3

- 정식명: Card Management System
- 에러코드 ID: 21
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 남유선(Peter Nam) · 심규도(Kyudo Shim) · 예진욱(Jinuk Ye)
- 설명(Korean):
  - 카드 원장 관리
  - 카드 발급을 위한 로우 데이터 생성
  - 모든 카드의 PAN 및 PAR 생성
  - PAN : 카드 고유 번호
  - PAR : 카드 고유 번호에 대한 닉네임 (거래에 사용)
  - 모든 카드에 대한 라이프사이클 관리
  - 카드 기반 정보 관리
  - 소득공제
  - 기명화
- 설명(English):
  - Create and manage card number of mobile card and plastic card(for internal use only), expiry date, life cycle and full text.
  - Support income tax deduction as an additional function.

## CRS (Customer Reward System) — 리워드 관련 정보 등록/업데이트/삭제 등의 관리와 활성화된 리워드에 따른 실시간 리워드 지급을 위한 조건 검사 기능을 제공한다. | 라인: 282-301 | 참조: 3-3

- 정식명: Customer Reward System
- 에러코드 ID: 63
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 남유선(Peter Nam) · 심규도(Kyudo Shim)
- 설명(Korean):
  - 리워드 관련 정보 등록/업데이트/삭제 등의 관리와 활성화된 리워드에 따른 실시간 리워드 지급을 위한 조건 검사 기능을 제공한다.
  - 다음 두 가지 종류에 대한 실시간 리워드 지급이 가능하다.
  - Point
  - Coupon
  - 다음 세 가지 상황에 실시간 리워드 지급을 할 수 있다
  - 회원가입
  - 카드등록
  - 결제 / 충전
- 설명(English):
  - Manage reward-related registration, update, deletion.
  - Support condition check function to grant real time reward on activated reward.

## CS (Charge Service) — 은행계좌 및 신용 카드를 통한 충전 기능 온라인 충전상 충전을 담당한다. | 라인: 302-318 | 참조: 3-3

- 정식명: Charge Service
- 에러코드 ID: 24
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 홍주표(Joopyo Hong) · 서용하(Yongha Seo)
- 설명(Korean):
  - 은행계좌 및 신용 카드를 통한 충전 기능 온라인 충전상 충전을 담당한다.
  - 사용자는 계좌주 실명 조회, ARS 인증을 거쳐, 은행 계좌를 앱에 등록할 수 있다. 등록된 계좌를 통해, 코나카드에 충전을 할 수 있다.
  - 외부 PG사와의 연동을 통하여 고객 계좌에서 출금이체가 이루어지도록 한다.
  - 사용자는 월별 자동 충전 또는 기준 하한 자동 충전 설정을 통해, 추가적인 입력 없이, 조건에 따라 자동으로 충전되는 기능을 지원한다.
- 설명(English):
  - CS manages charging via bank account or credit card to kona card. Users can register their bank accounts in the app via account name lookup, ARS verification. Users can charge Kona cards through the registered account.
  - The withdrawal from the customer's account is made through the interlocking with the external PG company.
  - The user can charge automatically according to conditions, without any additional input, either through monthly automatic charging or standard low automatic charging setting.

## CVS (Certificate Verification Service) — 외부 인증 모듈로 현재 주민등록증 인증과 운전면허증 인증을 제공한다. 소득공제 및 충전한도 상향시 신분증 인증을 사용한다. | 라인: 319-332 | 참조: 3-3

- 정식명: Certificate Verification Service
- 에러코드 ID: 53
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 김현수(HyunSoo Kim) · 김병수(Byeongsu Kim)
- 설명(Korean):
  - 외부 인증 모듈로 현재 주민등록증 인증과 운전면허증 인증을 제공한다. 소득공제 및 충전한도 상향시 신분증 인증을 사용한다.
  - 주민등록증 인증 - 정부24
  - 운전면허증 인증 - 경찰청
- 설명(English):
  - The external authentication module provides current resident registration certificate and driver's license certification.

## DCP (Digital Card Platform) — 모바일 카드 관리 | 라인: 333-351 | 참조: 3-3

- 정식명: Digital Card Platform
- 에러코드 ID: 12
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: KSL
- 설명(Korean):
  - 모바일 카드 관리
  - 모바일 카드 토큰 관리
  - 라이프 사이클 관리
  - DELETE : 삭제
  - ACTIVE : 활성화
  - SUSPENDED : 정지
  - 키 관리
  - 모바일 거래에 사용되는 암호화 키 관리
- 설명(English):
  - Manage digital card life cycle. Manage transaction keys and replenishment

## DDA/DDV (Display data service) — App을 위한 전시데이터 제공용 API 서비스 | 라인: 352-363 | 참조: 3-3

- 정식명: Display data service
- 에러코드 ID: 102
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: Retired_이승욱(Seungwook Lee)1
- 설명(Korean):
  - App을 위한 전시데이터 제공용 API 서비스
- 설명(English):
  - API service for providing exhibition data for App

## DMS (Donation Management Service) — 기부 서비스 | 라인: 364-377 | 참조: 3-3

- 정식명: Donation Management Service
- 에러코드 ID: 81
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 심규도(Kyudo Shim) · 조성구(Sunggu Jo)
- 설명(Korean):
  - 기부 서비스
  - 포인트 or 잔액을 통한 기부 서비스
- 설명(English):
  - Donation Service
  - user donate point or cash to charity

## EAS (External Alliance Service) — 외부 제휴 서비스를 위한 컴포넌트 | 라인: 378-395 | 참조: 3-3

- 정식명: External Alliance Service
- 에러코드 ID: 45
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 조성구(Sunggu Jo) · 예진욱(Jinuk Ye)
- 설명(Korean):
  - 외부 제휴 서비스를 위한 컴포넌트
  - KB PLCC
  - CU Membership
  - 상품 서브스 코드 관리
- 설명(English):
  - server component for external alliance service
  - KB PLCC Card
  - CU Membership
  - Service code menagement

## EDM (External Data Manager) — 외부 서비스 제휴사와의 커뮤니케이션을 담당하는 컴포넌트이며 제휴사로부터 서비스에 필요한 정보를 수집하거나 제휴사에게 부가 서비스를 제공한다... | 라인: 396-410 | 참조: 3-3

- 정식명: External Data Manager
- 에러코드 ID: 55
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 서용하(Yongha Seo)
- 설명(Korean):
  - 외부 서비스 제휴사와의 커뮤니케이션을 담당하는 컴포넌트이며 제휴사로부터 서비스에 필요한 정보를 수집하거나 제휴사에게 부가 서비스를 제공한다. 제휴사별 정책에 따라, 제휴사 카드 등록 시, 혜택을 제공하는 기능, 제휴사 충전 기능, 은행 계좌 등록 시, 제휴사 계좌 정보 제공 기능을 지원한다.
  - 제휴사는, 모두, SKT, 통합콜, 아들에날린, 농협은행이 있다.
- 설명(English):
  - EDM is a component responsible for communication with external service partners and collects information necessary for the service from affiliates or provides additional services to affiliates.
  - According to the affiliate policy, it supports the function of providing benefits when registering an affiliate card, the function of charging an affiliate, the function of providing information of an affiliate account when registering a bank account.
  - Affiliates are MODU, SKT, Unified Call, Nonghyup bank.

## EGS (External Gateway System) — Portal과 고객센터 등 외부 컴포넌트가 코어 API와 소통하는 Gateway 역할을 한다. | 라인: 411-424 | 참조: 3-3

- 정식명: External Gateway System
- 에러코드 ID: -
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 남유선(Peter Nam) · 심규도(Kyudo Shim)
- 설명(Korean):
  - Portal과 고객센터 등 외부 컴포넌트가 코어 API와 소통하는 Gateway 역할을 한다.
  - Gateway 리스트
  - etn, itn, map, ias, apigw, cdm, cardse, cms, kps, kcs, knotify, , userporal, gs, kcps, crs, cs, rs, vvan, edm, tsp, bizs, kmp
- 설명(English):
  - A Gateway for external components such as Portal and Customer Center to communicate cord API.

## EIM · BPP와 통합되어 사용안함 (2018.10.31) (Electronic ID Management System) — 기업에서 패용되는 사원증의 발급 및 출입권한 통제, 코나카드시스템과 연동하여 선불카드와 결합하여 사용할 수 있다. | 라인: 425-436 | 참조: 3-3

- 정식명: Electronic ID Management System
- 에러코드 ID: 25
- 결제데이터 보유: 미지정
- 보존기간: 미지정
- 담당자: 정희영
- 설명(Korean):
  - 기업에서 패용되는 사원증의 발급 및 출입권한 통제, 코나카드시스템과 연동하여 선불카드와 결합하여 사용할 수 있다.
- 설명(English):
  - Issue employee identification

## ELASTIC (ELASTIC Search) — 연계된 지자체의 충전, 결제, 유저정보의 빅데이터 처리 및 지자체 전송을 진행 하는 역할을 한다. | 라인: 437-448 | 참조: 3-3

- 정식명: ELASTIC Search
- 에러코드 ID: -
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 윤병근(Byeonggeun Yoon)
- 설명(Korean):
  - 연계된 지자체의 충전, 결제, 유저정보의 빅데이터 처리 및 지자체 전송을 진행 하는 역할을 한다.
- 설명(English):
  - It plays a role in charging, payment, big data processing of user information, and transmission to local governments.

## EMS (Echo Mileage Service) — 인천 서구 환경 마일리지 서비스를 위한 컴포넌트 | 라인: 449-460 | 참조: 3-3

- 정식명: Echo Mileage Service
- 에러코드 ID: 129
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 하승원(SeungWon Ha)
- 설명(Korean):
  - 인천 서구 환경 마일리지 서비스를 위한 컴포넌트
- 설명(English):
  - It is a server for providing environmental mileage service in Seo-gu, Incheon, and serves to provide mileage by linking walking and cycling partners.

## EPMS (External Portal Data Management Service) — 외부 지자체 포탈의 데이터를 연동하는 컴포넌트로 해당 데이터는 App 전시데이터로 활용된다. | 라인: 461-472 | 참조: 3-3

- 정식명: External Portal Data Management Service
- 에러코드 ID: 181
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: Retired_심재성(Jaeseong Sim) , · 엄지선(Jisun Eom)
- 설명(Korean):
  - 외부 지자체 포탈의 데이터를 연동하는 컴포넌트로 해당 데이터는 App 전시데이터로 활용된다.
- 설명(English):
  - It is a component that links data on external local government portals, and the data is used as app exhibition data.

## EWSM (External Web Service Manager) — 외부 웹 서비스와의 연동을 담당하는 컴포넌트이다. | 라인: 473-487 | 참조: 3-3

- 정식명: External Web Service Manager
- 에러코드 ID: 71
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 조성구(Sunggu Jo)
- 설명(Korean):
  - 외부 웹 서비스와의 연동을 담당하는 컴포넌트이다.
  - 현재, MG신용정보(주) 와 서비스 연동을 통해, ARS 서비스를 제공하고 있다. ARS 서비스를 통해, 수당 카드 등록, 준준회원 가입, 카드 분실 및 분실 해제, 소득 공제 신청, 카드 잔액 및 포인트 조회 기능을 제공한다.
- 설명(English):
  - EWSM is a component responsible for communication with external web service partners.
  - At this moment, EWSM provide ARS service with MG Credit Info affiliate.
  - Through out ARS, it provides allowance request, deduction, card lost & lost release, semi-user register.

## FDMS (FDS Management System) — 마스터카드 해외결제의 이상금융거래탐지(FDS)를 검증하기 위해 매입사인 KB와의 연동을 담당하는 컴포넌트이다. | 라인: 488-499 | 참조: 3-3

- 정식명: FDS Management System
- 에러코드 ID: 181
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: Retired_심재성(Jaeseong Sim) , 엄지선(Jisun Eom)
- 설명(Korean):
  - 마스터카드 해외결제의 이상금융거래탐지(FDS)를 검증하기 위해 매입사인 KB와의 연동을 담당하는 컴포넌트이다.
- 설명(English):
  - It is a component in charge of linking with KB, the buyer, to verify the abnormal financial transaction detection (FDS) of MasterCard's overseas payment.

## FDS (Fraud Detection System) — 이상금융거래탐지(FDS)는 3가지의 주요업무를 수행한다. | 라인: 500-517 | 참조: 3-3

- 정식명: Fraud Detection System
- 에러코드 ID: 72
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 박소현(Sohyun Park)
- 설명(Korean):
  - 이상금융거래탐지(FDS)는 3가지의 주요업무를 수행한다.
  - 이상탐지(Detection) : 기초 데이터를 사전 정의된 정책으로 분석하여 이상거래를 도출한다.
  - 정책정의(Policy) : 이상거래로 도출하기 위한 정책을 정의하고 이상탐지 시 정의된 사항으로 이상금융거래로 도출되도록 한다.
  - 이상조치(Response) : 이상금융거래로 도출된 정보를 바탕으로 해당 플레이어를 대상으로 금융거래의 제제를 가한다.
- 설명(English):
  - The component FDS will do three major jobs:
  - detect the fraud: Based on the policy defined previously, FDS will detect fraud transaction.
  - define the policy: Define the policy for fraud transaction.
  - deal with the frauds: Based on the accumulated information of the user and the policy, FDS will manage his/her fraud history and stop/resume his/her transaction.

## FPS (Fee Policy System) — 과금 시스템 | 라인: 518-530 | 참조: 3-3

- 정식명: Fee Policy System
- 에러코드 ID: 40
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 하승원(SeungWon Ha)
- 설명(Korean):
  - 과금 시스템
  - 서비스 이용 따른 과금 관리 서비스
- 설명(English):
  - Fee Payment SystemBilling management service according to service use

## FTM (File transfer management) — 파일전송관리 시스템 | 라인: 531-540 | 참조: 3-3

- 정식명: File transfer management
- 에러코드 ID: 84
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 정희영(HeeYoung Jeong)
- 설명(Korean):
  - 파일전송관리 시스템

## GS (Gift Service) — 카드 선물, 쿠폰 선물 및 송금을 관장하는 컴포넌트로, 선물 및 송금 전송에 따른 상태를 관리하고 전송자와 수신자를 이어주는 역할을 한다. | 라인: 541-555 | 참조: 3-3

- 정식명: Gift Service
- 에러코드 ID: 52
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 홍주표(Joopyo Hong) · Retired_심재성(Jaeseong Sim)
- 설명(Korean):
  - 카드 선물, 쿠폰 선물 및 송금을 관장하는 컴포넌트로, 선물 및 송금 전송에 따른 상태를 관리하고 전송자와 수신자를 이어주는 역할을 한다.
  - 선물 서비스에는, “사용자간 선물 서비스”, “어드민 선물 서비스”이 있으며, 송금 서비스에는 "사용자간 송금", "카드로 직접 송금"으로 나뉜다.
- 설명(English):
  - GS manages card gift, coupon gift, and remittance.
  - It manages the status of the gift and remittance transfer and connects the sender and receiver.
  - Card/Coupon gift service includes "user gift service" and "administrator gift service", and remittance service is divided into "user transfer" and "card direct transfer".

## IAS (Issuer authorization system) — 카드의 최종 원장을 관리하며 라이프사이클 및 카드 잔액과 서비스에 필요한 상태 등을 관리한다. | 라인: 556-572 | 참조: 3-3

- 정식명: Issuer authorization system
- 에러코드 ID: 22
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 최동식 (Dongsik Choi) · 박병건(Byounggun Park)
- 설명(Korean):
  - 카드의 최종 원장을 관리하며 라이프사이클 및 카드 잔액과 서비스에 필요한 상태 등을 관리한다.
  - 거래발생시 PP를 통해 ISO8583 데이터를 가공하여 승인처리를 진행 및 충전, 지불, 환불 등 거래내역 등을 관리하며 추후 정산에 필요한 데이터를 생성하는 역할을 한다.
  - 카드 원장 및 거래 데이터는 월렛 및 콜센터, 운영UI등에 표현된다.
- 설명(English):
  - Manage final register, life cycle, card balance and state for service.
  - Fulfill approval by processing ISO8583 data via PP when transaction occurs.
  - Manage transaction history such as charge, payment and refund to prepare necessary data to calculate at the later date.
  - Card register and transaction data are reflected in wallet, call center and operation UI.

## ICMS (Integrated Cash Management System) — CMS TCP 통신 컴포넌트 | 라인: 573-585 | 참조: 3-3

- 정식명: Integrated Cash Management System
- 에러코드 ID: 없음
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: Retired_원영훈(Younghoon Won) · 김현수(HyunSoo Kim)
- 설명(Korean):
  - CMS TCP 통신 컴포넌트
  - 각 외부 제휴사들과 CMS 전문방식으로 파일 송수신 연동을 관리한다. 파일을 송신하는 클라이언트와 파일을 수신하는 서버로 구성되어있다.
- 설명(English):
  - It manages file transmission/reception interlocking with each external partner in a CMS-specialized method. It consists of a client sending a file and a server receiving the file.

## ITA(TMS) (Issuer Token Adapter) — 크립토그램 검증 | 라인: 586-613 | 참조: 3-3

- 정식명: Issuer Token Adapter
- 에러코드 ID: 13
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: Kayum Hossan
- 설명(Korean):
  - 크립토그램 검증
  - 거래 요청 수락
  - 카드 브랜드 및 거래 모드 결정
  - 위 결정에 따라 크립토그램 검증
  - 카드 데이터를 통한 비정상 거래 관리
  - ATC 값의 범위 정책을 통해서 거래요청을 검증
  - 검증 결과가 부적격이면 디지털 카드의 정보를 삭제요청
  - 토큰 해제
  - TSP와 통신하여 토큰 해제
- 설명(English):
  - Cryptogram Validation
  - Accepts transaction request
  - Determines Card Brand and Transaction Mode
  - Validates Cryptogram according to Card Brand and Transaction Mode
  - Fraud Management
  - Checks validity of data in transaction request and ATC values in the range of accepted values
  - Requests to suspend or wipe Digitized Card depending on the outcome of the validation
  - De-Tokenization
  - De-tokenizes Token using interfaces with TSP

## KAS (Kona Address System) — 주소 검색 시스템 | 라인: 614-629 | 참조: 3-3

- 정식명: Kona Address System
- 에러코드 ID: 130
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 조성구(Sunggu Jo)
- 설명(Korean):
  - 주소 검색 시스템
  - 가맹점 배치 전문 수신 후 테이블 import 시 가맹점의 위경도를 채번하여 넣는다.
  - 주소 검색을 통해 위경도, 도로명 → 지번 , 지번 → 도로명을 검색할 수 있다.
- 설명(English):
  - Search Address System
  - The merchant's latitude and longitude are found in the merchant's data import.
  - Search Address And Get Infomation (Road To Jibun, Jibun to Road, zipCode)

## KCMW (Kona Consultant Mobile Web) — 코나카드 모집인을 통해서 회원가입을 한 회원 수 및 일정 금액 이상을 결제한 회원 정보를 모바일 환경을 통해 월별 실적 정보로 제공함으로써... | 라인: 630-641 | 참조: 3-3

- 정식명: Kona Consultant Mobile Web
- 에러코드 ID: 없음
- 결제데이터 보유: Y/N
- 보존기간: 12 Months
- 담당자: Retired_조성민(SungMin Cho) · Retired_김상진(SangJin Kim)
- 설명(Korean):
  - 코나카드 모집인을 통해서 회원가입을 한 회원 수 및 일정 금액 이상을 결제한 회원 정보를 모바일 환경을 통해 월별 실적 정보로 제공함으로써 코나카드 모집인들이 자신의 실적을 확인 할 수 있는 정보를 제공하는 컴포넌트이다.
- 설명(English):
  - Provide recruiter's monthly record.

## KCPS (Kona Coupon System) — KonaCard 쿠폰 관리 시스템으로, 제휴 인프라에서 사용하는 외부쿠폰과 내부 인프라에서 사용하는 내부쿠폰을 관리한다. | 라인: 642-657 | 참조: 3-3

- 정식명: Kona Coupon System
- 에러코드 ID: 58
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 권수연(SooYeon Kwon)
- 설명(Korean):
  - KonaCard 쿠폰 관리 시스템으로, 제휴 인프라에서 사용하는 외부쿠폰과 내부 인프라에서 사용하는 내부쿠폰을 관리한다.
  - CRS 또는 Admin(Portal), 혹은 쿠폰샵에서 요청하는 쿠폰을 발행 또는 발행 취소 등을 관리 한다.
  - 쿠폰 설정 정보는 KOD가 관리하며 KCPS는 필요 시 KOD를 통해 쿠폰 설정 및 정책에 대한 정보를 취득한다.
- 설명(English):
  - It is a KonaCard coupon management system that manages external coupons provided by partner companies and internal coupons used in internal infrastructure.
  - Manage coupon issuance or cancellation requested by CRS, Admin(Portal), or coupon shop.
  - Information on setting coupons is managed by KOD, and KCPS obtains information on coupon settings and policies through KOD, if necessary.

## KCS (Kona Consultant Service) — 코나카드 고객 유치를 위한 회원 가입을 유도하는 모집인 관련 컴포넌트로 모집인 관리 및 모집인 실적을 제공한다. | 라인: 658-671 | 참조: 3-3

- 정식명: Kona Consultant Service
- 에러코드 ID: 없음
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 김현수(HyunSoo Kim)
- 설명(Korean):
  - 코나카드 고객 유치를 위한 회원 가입을 유도하는 모집인 관련 컴포넌트로 모집인 관리 및 모집인 실적을 제공한다.
  - 모집인은 다양한 방법으로 코나카드 회원을 모집하며 고객이 가입 시 입력한 추천인 코드를 근거로하여 고객 모집 실적을 판단한다.
  - 모집인의 실적에 따라서 모집 수수료 내역과 근거 자료를 생성하고 수수료 지급을 할 수 있도록 한다.
- 설명(English):
  - A component to provide Core API related to recruiter.

## KFDS (Kona Fraud Detection System) — A-safe를 대신하여 신규로 추가되는 이상금융거래탐지(FDS) 룰을 관리하며 이상거래를 탐지하여 정보를 제공하는 컴포넌트이다. | 라인: 672-683 | 참조: 3-3

- 정식명: Kona Fraud Detection System
- 에러코드 ID: 222
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 조진수(JinSu Jo)
- 설명(Korean):
  - A-safe를 대신하여 신규로 추가되는 이상금융거래탐지(FDS) 룰을 관리하며 이상거래를 탐지하여 정보를 제공하는 컴포넌트이다.
- 설명(English):
  - This is a component that manages the newly added Abnormal Financial Transaction Detection (FDS) rules on behalf of A-safe and detects abnormal transactions and provides information.

## KMC (Konacard Multi-CRM) — 고객으로부터 오는 각종 서비스 관련 문의에 대해 신속히 대응하기 위한 고객센터 웹 서버이다. 고객, 가맹점, 비회원배송 등에 대해 조회가 ... | 라인: 684-696 | 참조: 3-3

- 정식명: Konacard Multi-CRM
- 에러코드 ID: 없음
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: Unknown User (lee.yj)
- 설명(Korean):
  - 고객으로부터 오는 각종 서비스 관련 문의에 대해 신속히 대응하기 위한 고객센터 웹 서버이다. 고객, 가맹점, 비회원배송 등에 대해 조회가 가능하다.
- 설명(English):
  - A Customer Center web server to quickly respond to customer's inquiries for various service.
  - Available to check customer, affiliate and nonmember delivery.

## KMS (Key Management System) — HSM 등의 암호화 처리 장비를 이용하여 Key를 안전하게 관리하고 사용하기 위한 편의 기능들을 제공한다. | 라인: 697-708 | 참조: 3-3

- 정식명: Key Management System
- 에러코드 ID: 17
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: Yasser Arafat
- 설명(Korean):
  - HSM 등의 암호화 처리 장비를 이용하여 Key를 안전하게 관리하고 사용하기 위한 편의 기능들을 제공한다.
- 설명(English):
  - Communicator between KonaCard component and HSM. Perform encryption/decryption using HSM.

## KNOTIFY (Knotify) — 코나카드 서비스의 장애, 통보, 거래 내역 등 알림을 담당한다 | 라인: 709-730 | 참조: 3-3

- 정식명: Knotify
- 에러코드 ID: 29
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: Shawrup K Suter
- 설명(Korean):
  - 코나카드 서비스의 장애, 통보, 거래 내역 등 알림을 담당한다
  - Notification Type
  - SMS
  - Push
  - E-Mail
  - Notification 서비스를 제공하며 API요청으로 전달받은 알림내역을 각 타입에 맞게 전송한다
- 설명(English):
  - It is responsible for notification of Kona card service
  - Notification Type
  - SMS
  - Push
  - E-Mail
  - Notification service is provided and the notification received by the API request is transmitted according to each type

## Knotify-DMZ (Knotify DMZ) — 푸시 서비스 공급자 컴포넌트간의 라우팅하는 처리로, 컴포넌트의 주요 역할은 knotify가 보낸 푸시를 전달하는 것이다. | 라인: 731-748 | 참조: 3-3

- 정식명: Knotify DMZ
- 에러코드 ID: 29
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: Shawrup K Suter
- 설명(Korean):
  - 푸시 서비스 공급자 컴포넌트간의 라우팅하는 처리로, 컴포넌트의 주요 역할은 knotify가 보낸 푸시를 전달하는 것이다.
  - 푸시 서비스 공급자
  - FCM (Firebase Cloud Messaging)
  - APN (Apple Push Notification Service)
- 설명(English):
  - Push Service Providers Routing between components, the main function of the component is to convey pushes sent by knotify.
  - Push service provider
  - Firebase Cloud Messaging (FCM)
  - Apple Push Notification Service (APN)

## KOD_ETN (Kona Operation Desk  -External) — 선불 결제 시스템 운영에 관한 모든 정보(시스템 정책 및 시스템 운영 정보, 파트너 및 상품의 정보)들을 설정하고 관리 할 수 있도록 운영... | 라인: 749-761 | 참조: 3-3

- 정식명: Kona Operation Desk  -External
- 에러코드 ID: 35
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 유정현 (JungHyun Yoo) · 조성구(Sunggu Jo)
- 설명(Korean):
  - 선불 결제 시스템 운영에 관한 모든 정보(시스템 정책 및 시스템 운영 정보, 파트너 및 상품의 정보)들을 설정하고 관리 할 수 있도록 운영 포탈(플랫폼, 파트너, 비즈등)에 제공한다. 운영 포탈들에 내부 컴포넌트들의 정보들을 조회 및 조합하여 제공하는 역할을 담당한다.
- 설명(English):
  - Save system policy along with its operational information, partner and product's information.
  - Work as a gateway for Portal and internal component to communicate.

## KOD_ITN (Kona Operation Desk  -Internal) — 선불 결제 시스템 운영에 관한 모든 정보들을 제공한다. Core 컴포넌트 & Wallet App의 요청에 따라 상품 정보, 가맹점 및 기타... | 라인: 762-773 | 참조: 3-3

- 정식명: Kona Operation Desk  -Internal
- 에러코드 ID: 70
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 조성구(Sunggu Jo)
- 설명(Korean):
  - 선불 결제 시스템 운영에 관한 모든 정보들을 제공한다. Core 컴포넌트 & Wallet App의 요청에 따라 상품 정보, 가맹점 및 기타 Player들에 대한 정보, 시스템 설정 정보, 각종 정책, 할인 정보(즉시할인, 포인트 적립, 단골 할인등), 쿠폰 정보, 결제 우선 순위 및 결제/충전/환불 사용자 수수료 계산 기능, 정산관련 설정 정보등을 제공한다.
- 설명(English):
  - This component provides information about products, merchants and other players, system configuration information, various policies, discounts and user fee calculation function by the request of other core components in the system.

## KPF (Kona Private Funding) — 계 서비스 | 라인: 774-791 | 참조: 3-3

- 정식명: Kona Private Funding
- 에러코드 ID: 80
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 조성구(Sunggu Jo)
- 설명(Korean):
  - 계 서비스
  - 한국의 전통 계를 모바일 앱을 통해 제공하는 서비스
- 설명(English):
  - Kona Private Funding
  - traditional funding of korea
  - create private group for funding
  - private group has round which is count of members
  - each round pick recipient
  - except for recipient, member pay funding amount

## KPS (Kona Point System) — 포인트(캐시백)을 관리한다. 정책에 기반한 포인트 적립, 사용, 지급, 차감, 포인트 내역 조회를 제공한다. | 라인: 792-809 | 참조: 3-3

- 정식명: Kona Point System
- 에러코드 ID: 56
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 조진수(JinSu Jo)
- 설명(Korean):
  - 포인트(캐시백)을 관리한다. 정책에 기반한 포인트 적립, 사용, 지급, 차감, 포인트 내역 조회를 제공한다.
  - 포인트는 유저 계정별 포인트(유저포인트), 카드 및 정책별 포인트가 존재하며 각 포인트들의 원장 및 한도관련 처리를 담당한다.
  - 혜택 적립, 포인트 사용, 포인트 자동사용, 포인트 자동 복합 사용, 인센티브 적립, 고객센터 유저 포인트 지급/차감, 수당 지급/회수, 포인트 이용내역, 복지포인트 지급, 환불시 포인트 차감 등을 제공한다.
  - 포인트 소멸- 소멸일자와 이미 사용된 포인트를 계산하여 소멸 대상 포인트를 소멸시킨다.
- 설명(English):
  - Manage points (cashback). Provide policy-based point accumulation, usage, payment, deduction, and point tracking.
  - Points exist for each user account point (user point), card, and policy, and are responsible for processing related to the ledger and limit of each point.
  - Provide benefits, points, automatic points, automatic points, incentives, customer center user point payment / deduction, payment / collection of benefits, points of use, payment of welfare points, and deduction of points for refunds.
  - Extinguish Point - Destroy the expired point by calculating the expiration date and the points already used.

## KSTS (Kona Stamp System) — 스탬프 시스템 | 라인: 810-827 | 참조: 3-3

- 정식명: Kona Stamp System
- 에러코드 ID: 76
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 권수연(SooYeon Kwon)
- 설명(Korean):
  - 스탬프 시스템
  - 스탬프 정책 관리
  - 결제이력에 따른 스탬프 적립/취소
  - 적립 이력에 따라 보상/보상취소
- 설명(English):
  - stamp system
  - Stamp policy management
  - Stamp accumulation/cancellation according to payment history
  - Compensation/compensation cancellation according to accumulation history

## KDS (Kona Delivery Service) — 외부 배달 대행 서비스 | 라인: 828-843 | 참조: 3-3

- 정식명: Kona Delivery Service
- 에러코드 ID: 44
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 조성구(Sunggu Jo)
- 설명(Korean):
  - 외부 배달 대행 서비스
  - 배달 대행사 관리
  - 외부 배달 대행사 접수 연동
- 설명(English):
  - Delivery Order Routing Service
  - Manage delivery agency
  - order Delivery Service from merchant to customer

## LOP (Local Order Platform) — 배달 서비스 | 라인: 844-861 | 참조: 3-3

- 정식명: Local Order Platform
- 에러코드 ID: 82
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 남유선(Peter Nam) · 심규도(Kyudo Shim) · 예진욱(Jinuk Ye)
- 설명(Korean):
  - 배달 서비스
  - 배달 가맹점 관리
  - 배달 가맹점 매뉴 및 정책 관리
  - 배달 결제 기능 제공
- 설명(English):
  - Delivery service for specific product (ex, food)
  - Manage PLACE (delivery merchant)
  - Manage Menu and Policy
  - Serve payment functionality

## LOP_EXT (Local Order Platform - Externel) — 배달 서비스 | 라인: 862-872 | 참조: 3-3

- 정식명: Local Order Platform - Externel
- 에러코드 ID: 149
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 남유선(Peter Nam)
- 설명(Korean):
  - 배달 서비스
  - 외부 연동 (재사용 용기)

## LOP_DTS (Local Order Platform - Data Transfer Service) — 배달 서비스 | 라인: 873-883 | 참조: 3-3

- 정식명: Local Order Platform - Data Transfer Service
- 에러코드 ID: 150
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 남유선(Peter Nam)
- 설명(Korean):
  - 배달 서비스
  - 데이터 관리

## MAP (Mobile Application Platform) — 회원 | 라인: 884-919 | 참조: 3-3

- 정식명: Mobile Application Platform
- 에러코드 ID: 11
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 하승원(SeungWon Ha)
- 설명(Korean):
  - 회원
  - 회원 가입, 일시중지, 회원 탈퇴 등 회원 서비스 이용 상태를 관리
  - 비정상 서비스 이용상태를 블랙리스트로 관리
  - 회원의 Wallet 인증을 Token, password 관리
  - 회원 가입 시 Device정보를 관리
  - 회원별 등급 관리(준준회원, 준회원, 정회원)
  - 약관
  - ASP별 약관 별 관리
  - 약관에 대한 회원 동의 여부 관리
  - 프로모션
  - 프로모션 서비스를 위한 회원의 프로모션 코드 관리
  - 추천인
  - 회원의 추천코드 및 추천 받은 회원의 정보를 관리
- 설명(English):
  - Member Management
  - member life cycle management(join, suspend, withdrawal )
  - not normal member life cycle(black list)
  - token, password form certification user for wallet
  - device of member management
  - grade of member management
  - Tems
  - tems management by asp management
  - aggreement tems by member management
  - Promotion
  - manage a member's promotional code for promotional services
  - Recommender
  - Management of member's recommendation letter and recommendation member information

## MIS (Mobility Integration Service) — 모빌리티 연동 서비스 | 라인: 920-930 | 참조: 3-3

- 정식명: Mobility Integration Service
- 에러코드 ID: 없음
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 심재진(Jaejin Sim)
- 설명(Korean):
  - 모빌리티 연동 서비스
  - 코나모빌리티 & 제휴사 데이터 연동 지원

## OASG (Open API Service Gateway) — Gateway for OpenApi | 라인: 931-942 | 참조: 3-3

- 정식명: Open API Service Gateway
- 에러코드 ID: 없음
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 정희영(HeeYoung Jeong)
- 설명(Korean):
  - Gateway for OpenApi
- 설명(English):
  - Gateway for OpenApi

## OASR (Open API Service Route & Data ReMapping Service) — Open API 서비스 컴포넌트 | 라인: 943-962 | 참조: 3-3

- 정식명: Open API Service Route & Data ReMapping Service
- 에러코드 ID: 없음
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 심재진(Jaejin Sim)
- 설명(Korean):
  - Open API 서비스 컴포넌트
  - 웰컴 저축은행
  - 애큐온 저축은행
  - 레몬트리
  - 코리엠소프트
- 설명(English):
  - Server component for Open API
  - Wellcome bank
  - Acuon bank
  - Lemontree
  - KORIEMSOFT

## PCS (Prepaid Card Service) — Wallet App향 Service Layer로 IAS, DCP, PCS, CS, CMS, CDM, KOD_ITN 등 여러 코어 컴포넌트들... | 라인: 963-974 | 참조: 3-3

- 정식명: Prepaid Card Service
- 에러코드 ID: 28
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 조성구(Sunggu Jo)
- 설명(Korean):
  - Wallet App향 Service Layer로 IAS, DCP, PCS, CS, CMS, CDM, KOD_ITN 등 여러 코어 컴포넌트들이 제공하는 정보를 조합하여 선불 카드의 유효기간, 혜택, 정책, 웰컴 카드 등의 카드 기준 정보와 관련된 조회 서비스를 제공하며, 배송관리, 재발급 신청, 다운로드, 삭제, 정지 등 카드의 라이프사이클과 관련된 기본 기능을 관리하는 서비스를 제공한다.
- 설명(English):
  - Service layer component. Perform prepaid card related operation (HCE card download, suspend/resume/delete card, card list etc) using core component.

## PCSI (Prepaid Card Service Inquiry) — ** 월렛에서 필요한 정보를 수집하여 제공하는 서비스 컴포넌트 | 라인: 975-998 | 참조: 3-3

- 정식명: Prepaid Card Service Inquiry
- 에러코드 ID: 27
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: Retired_심재성(Jaeseong Sim) · 엄지선(Jisun Eom) · 안성진(Seongjin Ahn)
- 설명(Korean):
  - ** 월렛에서 필요한 정보를 수집하여 제공하는 서비스 컴포넌트
  - IAS, DCP, PCS, CS, CMS, RMS등 여러 코어 컴포넌트들이 제공하는 정보를 조합하여 아래의 정보를 제공한다.
  - 사용자에게 발급 된 카드 목록 제공.
  - IAS, DCP, PCS, CardSE, CMS, CS, KPS, KOD_ITN으로부터 정보를 취합하여, 카드번호, 잔액, 서비스명, 닉네임, 기명화 여부, 사용가능한 서비스, 카드 포인트 잔액 등등 정보를 제공한다.
  - 계정 요약 정보
  - IAS, CS, RS, GS, KPS, CMS, KCPS 등으로부터 정보를 취합하여, 카드 개수, 쿠폰 개수, 연결된 계좌 정보, 등 정보를 제공한다.
  - 사용자가 받은 누적 혜택 정보
  - 카드 실적 정보
  - 사용자 환불 진행 정보
  - 카드 거래내역 정보
  - 카드 포인트 사용내역 정보
  - 상점에서 사용가능한 카드 목록
- 설명(English):
  - Manage information about purchasing card's PAN, expiry date, balance, benefits and policy by combining information provided by various Core components such as IAS, DCP, PCS, CS, CMS, RMS.
  - Provide card's transaction history and refund records.

## PP (Payment Processor) — 코나카드에서 발생하는 충전/환불/잔액 이동/지불 등 카드와 관련 된 모든 거래의 흐름을 제어한다. | 라인: 999-1018 | 참조: 3-3

- 정식명: Payment Processor
- 에러코드 ID: 23
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 박병건(Byounggun Park) · 최동식 (Dongsik Choi)
- 설명(Korean):
  - 코나카드에서 발생하는 충전/환불/잔액 이동/지불 등 카드와 관련 된 모든 거래의 흐름을 제어한다.
  - VAN으로 부터 올라오는 ISO8583 메시지의 Gateway로, 전문의 기본적인 형식을 검증하고 TMS/CMS/IAS 컴포넌트 등에 전달하는 역할을 담당한다.
  - TMS를 통해서 크립토그램 및 DCVV 등의 카드 데이터 검증 및 토큰 해제를 수행한다.
  - 토큰 해제 된 PAN을 IAS에 보내서 거래를 처리한다.
  - 오프라인 충전/환불 및 온/오프라인 지불의 결과에 대한 사용자 푸쉬 알림 기능을 제공한다.
- 설명(English):
  - Controls the flow of all card-related transactions such as recharge/refund/balance transfer/payment that occur on the KONA Card.
  - As a gateway for ISO8583 messages coming from VAN, it is responsible for verifying the basic format of messages and delivering them to TMS/CMS/IAS components.
  - Through TMS, card data verification such as cryptogram and DCVV and token release are performed.
  - Send the token-released PAN to IAS to process the transaction.
  - Offline recharge/refund and on/offline payment results are provided with user push notifications.

## PRM (Personal information access record management system) — 개인정보 접근기록 관리 시스템 | 라인: 1019-1031 | 참조: 3-3

- 정식명: Personal information access record management system
- 에러코드 ID: 85
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 곽용기(Yongkee Kwak)
- 설명(Korean):
  - 개인정보 접근기록 관리 시스템
  - 플랫폼/고객센터/비즈포탈 에서 관리자가 사용자에 대한 정보를 조회 할 경우 누가 언제 어떤 화면에서 누구를 조회했는지 이력을 남기는 컴포넌트
- 설명(English):
  - This is privacy logging component which is called whenever some operator view/search someone's data. it stores who saw who's data at when and where.

## QRS (Query Running Service) — 쿼리 실행 서비스, 복잡한 쿼리식을 요하는 서비스 제공 시 빠르게 서비스를 제공할 수 있도록 고안된 컴포넌트 | 라인: 1032-1050 | 참조: 3-3

- 정식명: Query Running Service
- 에러코드 ID: 103
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 남유선(Peter Nam)
- 설명(Korean):
  - 쿼리 실행 서비스, 복잡한 쿼리식을 요하는 서비스 제공 시 빠르게 서비스를 제공할 수 있도록 고안된 컴포넌트
  - 현재까지 사용처
  - 타겟 푸시 서비스
  - API 리스트
  - /query POST PUT
  - 쿼리 서비스 제공을 위한 정책 저장 / 수정
  - /query/{queryId} GET
  - 쿼리 서비스 정책 조회
  - /query/{queryId}/run POST
  - 쿼리 서비스 실행

## RPG (Remote Payment Gateway) — 코나플랫폼의 온라인PG 역할로, 모바일과 웹사이트의 온라인 결제 기능을 제공한다. 따라서 외부 가맹점에서의 온라인 결제를 관리한다. | 라인: 1051-1064 | 참조: 3-3

- 정식명: Remote Payment Gateway
- 에러코드 ID: 16
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: Kayum Hossan
- 설명(Korean):
  - 코나플랫폼의 온라인PG 역할로, 모바일과 웹사이트의 온라인 결제 기능을 제공한다. 따라서 외부 가맹점에서의 온라인 결제를 관리한다.
  - 외부 가맹점들과 암호화하여 통신한다. RPG는 비대칭키 암호화 방식과 대칭키 암호화 방식을 모두 지원하고 있다. 비밀키를 위해 RPG-KM과 통신한다. RPG는 가맹점의 주문 정보를 저장하고 VVAN과 통신하여 거래를 진행한다.
- 설명(English):
  - Online Transaction data preparation and validation, cancel online transactions. So RPG manage online payment from external merchant.
  - Merchant communicates with RPG. Communication between merchant and RPG is encrypted. RPG supports both asymmetric and symmetric key cryptographic . It communicate with RPG-KM for secret keys. RPG store merchant order information and communicate with VVAN to make the transaction,

## RPG-KM (RPG key management) — 외부 가맹점과 RPG의 요청에 의해 온라인 거래에 필요한 key를 생성하고 그 주기를 관리한다. | 라인: 1065-1076 | 참조: 3-3

- 정식명: RPG key management
- 에러코드 ID: 34
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: Kayum Hossan
- 설명(Korean):
  - 외부 가맹점과 RPG의 요청에 의해 온라인 거래에 필요한 key를 생성하고 그 주기를 관리한다.
- 설명(English):
  - Rpg Key Management (rpgkm) produce, store and manage key life cycle those are required from merchant and rpg component.

## RS (Refund Service) — 환불 처리기능을 제공한다. | 라인: 1077-1091 | 참조: 3-3

- 정식명: Refund Service
- 에러코드 ID: 50
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 하승원(SeungWon Ha)
- 설명(Korean):
  - 환불 처리기능을 제공한다.
  - 카드 잔액 계좌 환불, 콜센터 환불, 잔액모으기(코나머니로 잔액이동),잔액 전환(개인이 소유한 카드간 잔액 이동) 기능 제공,
  - 환불 가능 여부 조회, 환불 가능 금액 조회,
  - 환불계좌 성명 인증/환불 계좌 등록/변경/삭제 기능을 제공한다.
- 설명(English):
  - Provide refund function such as balance account refund, call center refund, collecting balance, checking refund amount, refund account authentication, registration, change, deletion.

## SAS (Statistics Analysis System) — 통계 컴포넌트 | 라인: 1092-1107 | 참조: 3-3

- 정식명: Statistics Analysis System
- 에러코드 ID: -
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 김병수(Byeongsu Kim)  ·  , 김현수(HyunSoo Kim)
- 설명(Korean):
  - 통계 컴포넌트
  - 코나카드의 거래 추이를 한 눈에 쉽게 알아 볼 수 있도록 거래 데이터를 가공하여 도표 및 그래프로 시각화하여 제공한다.
  - 고객의 인입 경로, 성별, 연령, 주 사용 시간 등의 정보를 이용하여 다양한 프로모션을 기획하며
  - 코나카드 마케팅 및 추후 운영 방향을 결정하기 위한 자료로 활용되기도 한다.
- 설명(English):
  - Visualize accumulated and daily transaction amount depending on transaction data into statistical data and graph.
  - These are the source for Konacard marketing and future operational decisions.

## TCS (Transaction Compare System) — VAN과의 대사 파일을 송신 및 수신한다. | 라인: 1108-1124 | 참조: 3-3

- 정식명: Transaction Compare System
- 에러코드 ID: -
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 한지백(JiBaek Han)
- 설명(Korean):
  - VAN과의 대사 파일을 송신 및 수신한다.
  - 각 VAN 사 별로의 별도 전문 양식을 기반으로 파일 파싱후 집계 및 해당 집계에 대한 파일을 검증한다.
  - 또한 VAN사에 대사 파일을 전송하는 기능또한 제공하고 있다.
  - VAN사와의 거래 대사를 통하여 정산 대상 거래에 대한 유효성 검증을 진행하여 데이터의 신뢰도를 높인다.
  - 또한 거래 유효성 검증을 통하여 승인 단의 거래까지 한 번 더 확인하는 작업이 이루어진다.
- 설명(English):
  - Send and receive 대사 파일 from/to VAN.
  - Verify corresponding 대사파일.

## TSP (Token Service Provider) — 카드 번호 토큰화 | 라인: 1125-1155 | 참조: 3-3

- 정식명: Token Service Provider
- 에러코드 ID: 14
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: Retired_Sk Kamruzzaman , Kayum Hossan
- 설명(Korean):
  - 카드 번호 토큰화
  - 새 토큰 발급
  - 토큰 해제
  - 재 토큰화
  - 대량 토큰화
  - 토큰 관리
  - BIN 관리
  - PAN BIN 생성 및 관리
  - 토큰 BIN 관리
  - PAN BIN과 토큰 BIN의 매핑 생성
- 설명(English):
  - Tokenization
  - Issue New Token
  - Detokenization
  - Retokenization
  - Bulk Tokenization
  - Re-Tokenization
  - Token Management
  - BIN Management
  - Pan Bin Generation and Management
  - Token Bin Management
  - Create Pan Bin-Token Bin Mapping

## GDIS (Gyeonggi-do Disaster Service) — 경기도 재난지원금 컴포넌트 | 라인: 1156-1165 | 참조: 3-3

- 정식명: Gyeonggi-do Disaster Service
- 에러코드 ID: 113
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 김현수(HyunSoo Kim) · 남유선(Peter Nam)
- 설명(Korean):
  - 경기도 재난지원금 컴포넌트

## MAS (Mobility Application Service) — 택시 컴포넌트 | 라인: 1166-1175 | 참조: 3-3

- 정식명: Mobility Application Service
- 에러코드 ID: 115
- 결제데이터 보유: Y/N
- 보존기간: 12 Months
- 담당자: 안 희
- 설명(Korean):
  - 택시 컴포넌트

## MAS-S (MAS Service) — 모빌리티 실시간 관제 | 라인: 1176-1186 | 참조: 3-3

- 정식명: MAS Service
- 에러코드 ID: 164
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: Retired_강동수
- 설명(Korean):
  - 모빌리티 실시간 관제
  - 실시간 택시 위치 Tracking, 실시간 택시 Call 호출 현황 관제

## MAS-B (MAS Batch) — 모빌리티 통계 | 라인: 1187-1199 | 참조: 3-3

- 정식명: MAS Batch
- 에러코드 ID: 165
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 김재헌
- 설명(Korean):
  - 모빌리티 통계
  - 모빌리티 포탈로 부터 택시 통계 데이터 조회 API 제공
  - IAS로 부터 택시 서비스 실시간 거래 데이터 수신 후 적재
  - CLR로 부터 정산 데이터 수신 후 적재

## MAS-J (MAS Job) — 모빌리티 배치 | 라인: 1200-1210 | 참조: 3-3

- 정식명: MAS Job
- 에러코드 ID: 166
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 이희수
- 설명(Korean):
  - 모빌리티 배치
  - 모빌리티 통계/정산 데이터에 대한 배치 작업 수행

## ETH (Event To Hadoop) — 택시 이벤트 투 하둡 저장 컴포넌트 | 라인: 1211-1220 | 참조: 3-3

- 정식명: Event To Hadoop
- 에러코드 ID: X
- 결제데이터 보유: Y/N
- 보존기간: 12 Months
- 담당자: 김재헌
- 설명(Korean):
  - 택시 이벤트 투 하둡 저장 컴포넌트

## RDS (Realtime Dispatcher Service) — 택시 실시간 위치 트레킹 및 요청 전송 컴포넌트 | 라인: 1221-1230 | 참조: 3-3

- 정식명: Realtime Dispatcher Service
- 에러코드 ID: X
- 결제데이터 보유: Y/N
- 보존기간: 12 Months
- 담당자: 김대우
- 설명(Korean):
  - 택시 실시간 위치 트레킹 및 요청 전송 컴포넌트

## ESP (Elastic Search Platform) — 엘라스틱서치 - 택시정보 관리 컴포넌트 | 라인: 1231-1240 | 참조: 3-3

- 정식명: Elastic Search Platform
- 에러코드 ID: 117
- 결제데이터 보유: Y/N
- 보존기간: 12 Months
- 담당자: Retired_강동수
- 설명(Korean):
  - 엘라스틱서치 - 택시정보 관리 컴포넌트

## BUSAN (Busan Core Service) — 부산 동백전 정보 이관 연계 컴포넌트 | 라인: 1241-1255 | 참조: 3-3

- 정식명: Busan Core Service
- 에러코드 ID: 118
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 심재진(Jaejin Sim)
- 설명(Korean):
  - 부산 동백전 정보 이관 연계 컴포넌트
  - 동백전 회원 정보 이관
  - 회원 가입 완료시, 회원 정보 이관 및 신규 wallet 회원 ID 매핑 처리
  - 동백전 잔액 정보 이관
  - 카드 발급 완료시, 잔액 정보 이관 처리
  - 동백전 이용 내역 정보 이관

## ETMS (Entry Ticket Management System) — 응모권 발급 | 라인: 1256-1273 | 참조: 3-3

- 정식명: Entry Ticket Management System
- 에러코드 ID: 38
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 권수연(SooYeon Kwon)
- 설명(Korean):
  - 응모권 발급
  - 이벤트 발생에 따른 응모권 발급
  - 응모정책 별 중복없는 응모권번호 채번
  - 1회 요청에 중복없는 사용자에 대해 어드민응모권 발급
- 설명(English):
  - the issuance of an entry ticket
  - Issue entry tiekcts for users who meet the event conditions
  - Generate entry ticket numbers without duplicates for each entry policy
  - Issue Admin entry tickets for users who do not have duplicates in one request

## MYDS (-) — 마이데이터 정보제공자 컴포넌트 | 라인: 1274-1283 | 참조: 3-3

- 정식명: -
- 에러코드 ID: 90
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 홍주표(Joopyo Hong) · Retired_심재성(Jaeseong Sim)
- 설명(Korean):
  - 마이데이터 정보제공자 컴포넌트

## MYDG (-) — 마이데이터 정보제공 서비스를 위한 Gateway 컴포넌트 | 라인: 1284-1293 | 참조: 3-3

- 정식명: -
- 에러코드 ID: 91
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 홍주표(Joopyo Hong) · Retired_심재성(Jaeseong Sim)
- 설명(Korean):
  - 마이데이터 정보제공 서비스를 위한 Gateway 컴포넌트

## PIS (-) — 선불카드조회 서비스 컴포넌트 - 신규 | 라인: 1294-1318 | 참조: 3-3

- 정식명: -
- 에러코드 ID: 145
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 김현수(HyunSoo Kim) , 홍주표(Joopyo Hong) , Retired_심재성(Jaeseong Sim)
- 설명(Korean):
  - 선불카드조회 서비스 컴포넌트 - 신규
  - ** 월렛에서 필요한 정보를 수집하여 제공하는 서비스 컴포넌트
  - IAS, DCP, PCS, CS, CMS, RMS등 여러 코어 컴포넌트들이 제공하는 정보를 조합하여 아래의 정보를 제공한다.
  - 사용자에게 발급 된 카드 목록 제공.
  - IAS, DCP, PCS, CardSE, CMS, CS, KPS, KOD_ITN으로부터 정보를 취합하여, 카드번호, 잔액, 서비스명, 닉네임, 기명화 여부, 사용가능한 서비스, 카드 포인트 잔액 등등 정보를 제공한다.
  - 계정 요약 정보
  - IAS, CS, RS, GS, KPS, CMS, KCPS 등으로부터 정보를 취합하여, 카드 개수, 쿠폰 개수, 연결된 계좌 정보, 등 정보를 제공한다.
  - 사용자가 받은 누적 혜택 정보
  - 카드 실적 정보
  - 사용자 환불 진행 정보
  - 카드 거래내역 정보
  - 카드 포인트 사용내역 정보
  - 상점에서 사용가능한 카드 목록
- 설명(English):
  - Manage information about purchasing card's PAN, expiry date, balance, benefits and policy by combining information provided by various Core components such as IAS, DCP, PCS, CS, CMS, RMS.
  - Provide card's transaction history and refund records.

## TSS (Transfer(Take-over) Support Service) — 이관 지원 서비스 | 라인: 1319-1338 | 참조: 3-3

- 정식명: Transfer(Take-over) Support Service
- 에러코드 ID: 156
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 심재진(Jaejin Sim) · 이경원(KyoungWon Lee)
- 설명(Korean):
  - 이관 지원 서비스
  - 회원 정보 이관
  - 잔액 정보 이관
  - 체크 카드 연동 정보 이관
  - 거래 내역 정보 이관
- 설명(English):
  - Support to take over from other company service
  - Transfer User Information
  - Transfer Balance Information
  - Transfer Debit Card Information
  - Transfer Transactions Information

## UIS (User Identification Service) — 코나카드 사용자의 신분증 진위 확인을 검증한다. | 라인: 1339-1350 | 참조: 3-3

- 정식명: User Identification Service
- 에러코드 ID: 155
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 김병수(Byeongsu Kim) · Retired_서정호(Jeongho Seo)
- 설명(Korean):
  - 코나카드 사용자의 신분증 진위 확인을 검증한다.
- 설명(English):
  - Verifies the authenticity of the KONA CARD user's ID.

## OASL (Open API Service Layer) — No HCE 기반 오픈 API 서비스 레이어 | 라인: 1351-1366 | 참조: 3-3

- 정식명: Open API Service Layer
- 에러코드 ID: 159
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 심재진(Jaejin Sim)
- 설명(Korean):
  - No HCE 기반 오픈 API 서비스 레이어
  - 코나 Health
  - JADU
  - PINO
- 설명(English):
  - Server component for Open API (No HCE)
  - Kona Health

## LSS (Luckyloco Support Service) — 코나카드 플랫폼과 럭키로코 서비스 연계 지원 | 라인: 1367-1378 | 참조: 3-3

- 정식명: Luckyloco Support Service
- 에러코드 ID: 160
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 하승원(SeungWon Ha)
- 설명(Korean):
  - 코나카드 플랫폼과 럭키로코 서비스 연계 지원
- 설명(English):
  - Support Servicee Between Konacard and Luckyloco

## YBAT (KonaYs Batch Service) — KonaYs Batch Service | 라인: 1379-1390 | 참조: 3-3

- 정식명: KonaYs Batch Service
- 에러코드 ID: 151
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 남유선(Peter Nam)
- 설명(Korean):
  - KonaYs Batch Service
- 설명(English):
  - KonaYs Batch Service

## YSTORE (KonaYs Store Service) — KonaYs Store Service | 라인: 1391-1403 | 참조: 3-3

- 정식명: KonaYs Store Service
- 에러코드 ID: 221
- 결제데이터 보유: N
- 보존기간: 2 Months
- 담당자: 남유선(Peter Nam)
- 설명(Korean):
  - KonaYs Store Service
  - KonaYs 프로젝트용 데이터 수집 서비스
- 설명(English):
  - KonaYs Store Service

## RFS (Request For Subsidy) — 보조금 24 (내게 맞는 정책수당 찾기 서비스) | 라인: 1404-1415 | 참조: 3-3

- 정식명: Request For Subsidy
- 에러코드 ID: 167
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 홍주표(Joopyo Hong)
- 설명(Korean):
  - 보조금 24 (내게 맞는 정책수당 찾기 서비스)
- 설명(English):
  - Request For Subsidy

## SPS (Secure Phonenumber Service) — 안심번호 제공 서비스 | 라인: 1416-1427 | 참조: 3-3

- 정식명: Secure Phonenumber Service
- 에러코드 ID: 119
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 남유선(Peter Nam) · 심규도(Kyudo Shim)
- 설명(Korean):
  - 안심번호 제공 서비스
- 설명(English):
  - Secure PhoneNumber Service

## TTS (Taxi Transaction System) — 택시 거래 시스템 | 라인: 1428-1445 | 참조: 3-3

- 정식명: Taxi Transaction System
- 에러코드 ID: 168
- 결제데이터 보유: Y
- 보존기간: 12 Months
- 담당자: 권수연(SooYeon Kwon) · 박병건(Byounggun Park)
- 설명(Korean):
  - 택시 거래 시스템
  - 앱미터기 전문 연동 후 VAN사를 통해 신용카드 거래 중계
  - 중계된 거래 수집시스템
  - 정산파일 제공
- 설명(English):
  - Taxi Transaction System
  - Intermediate credit card transaction through VAN company after professional linkage of Appmeter terminal
  - Relayed transaction collection system
  - Settlement file provided

## KBC_B (KONA business card Batch) — 복지카드 배치서비스 | 라인: 1446-1457 | 참조: 3-3

- 정식명: KONA business card Batch
- 에러코드 ID: 158
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 정희영(HeeYoung Jeong) · 곽용기(Yongkee Kwak) · 외주 개발사 : UX CUBE
- 설명(Korean):
  - 복지카드 배치서비스
- 설명(English):
  - Welfare card batch service

## LOP_RDS (LOP Realtime Dispatcher Service) — LOP 실시간 폴링 서비스 | 라인: 1458-1470 | 참조: 3-3

- 정식명: LOP Realtime Dispatcher Service
- 에러코드 ID: 175
- 결제데이터 보유: N
- 보존기간: 12Months
- 담당자: 남유선(Peter Nam) · 심규도(Kyudo Shim)
- 설명(Korean):
  - LOP 실시간 폴링 서비스
- 설명(English):
  - LOP Realtime Dispatcher Service
  - lop realtime polling service

## CSG (Call Service Gateway) — 지역전화콜 연동 서비스 | 라인: 1471-1484 | 참조: 3-3

- 정식명: Call Service Gateway
- 에러코드 ID: 176
- 결제데이터 보유: N
- 보존기간: 12Months
- 담당자: 김대우
- 설명(Korean):
  - 지역전화콜 연동 서비스
  - 지역전화콜 시스템과 코나택시(MAS) 사이에서 호출 서비스 중계
- 설명(English):
  - Call Service Gateway
  - Transfer call service between local call system and Kona taxi system(MAS)

## CPG (Credit Payment Gateway) — 신용카드 결제 게이트웨이 | 라인: 1485-1500 | 참조: 3-3

- 정식명: Credit Payment Gateway
- 에러코드 ID: 185
- 결제데이터 보유: Y
- 보존기간: 12Months
- 담당자: 윤병근(Byeonggeun Yoon)
- 설명(Korean):
  - 신용카드 결제 게이트웨이
  - EZPS에서 관리하는 카드정보를 통해 카드 간편결제 거래 중계
  - 정산데이터 제공
- 설명(English):
  - credit card payment gateway
  - Payment transactions are delivered to credit card companies using card information managed by EZPS.
  - Settlement data provided

## EZPS (Easy Payment Service) — 신용카드 간편 결제 관리 서비스 | 라인: 1501-1512 | 참조: 3-3

- 정식명: Easy Payment Service
- 에러코드 ID: 187
- 결제데이터 보유: N
- 보존기간: 12Months
- 담당자: 홍주표(Joopyo Hong) · 서용하(Yongha Seo) · 엄지선(Jisun Eom)
- 설명(Korean):
  - 신용카드 간편 결제 관리 서비스
- 설명(English):
  - Credit card easy payment management service

## ETM (Event To Mongo) — 택시 이벤트 투 MongoDB 저장 컴포넌트 | 라인: 1513-1522 | 참조: 3-3

- 정식명: Event To Mongo
- 에러코드 ID: X
- 결제데이터 보유: N
- 보존기간: 12Months
- 담당자: 김재헌
- 설명(Korean):
  - 택시 이벤트 투 MongoDB 저장 컴포넌트

## IMCS (IMCS) — 교통정산 컴포넌트 (Integrated Mobility Clearing and Settlement) | 라인: 1523-1541 | 참조: 3-3

- 정식명: IMCS
- 에러코드 ID: 195
- 결제데이터 보유: Y
- 보존기간: 12Months
- 담당자: 김현수(HyunSoo Kim)
- 설명(Korean):
  - 교통정산 컴포넌트 (Integrated Mobility Clearing and Settlement)
  - 신용카드사의 EDI 가맹점으로 교통 PG 역할을 수행함
  - 거래데이터를 수집하여, VAN or 신용카드사에 대표가맹점으써, 매입요청을 하고 매입 완료 되면 정산 대금을 받아서, 택시 사업자에게 정산함
  - Online 결제 : 신용카드사 직연동
  - Offline 결제 : VAN 사 연동
- 설명(English):
  - Integrated Mobility Clearing and Settlement
  - It serves as a transportation PG as an EDI affiliate of a credit card company Collect transaction data, make a purchase request to VAN or credit card company, receive the settlement price when the purchase is completed, and settle it with the taxi operator
  - Online payment: Direct connection with credit card companies
  - Offline Payment: Interworking with VAN Company

## DAPM (Display Advertisment Platform Messagebroker) — 광고 플랫폼 메세징 컴포넌트 | 라인: 1542-1557 | 참조: 3-3

- 정식명: Display Advertisment Platform Messagebroker
- 에러코드 ID: 189
- 결제데이터 보유: N
- 보존기간: 12Months
- 담당자: 남유선(Peter Nam) · 예진욱(Jinuk Ye)
- 설명(Korean):
  - 광고 플랫폼 메세징 컴포넌트
  - 광고 서비스는 모든 요청을 메세지로 관리하기에 광고 서비스 가장 앞단에서 모든 요청을 받는 서버
  - 받은 요청을 정규화를 통해 메세지 큐로 전달하는 역할
- 설명(English):
  - Advertising platform messaging components
  - The ad service manages all requests by message, so the server that receives all requests at the front end of the ad service
  - Responsible for forwarding received requests to message queues through normalization

## DAPC (Display Advertisment Platform Core) — 광고 플랫폼 코어 컴포넌트 | 라인: 1558-1571 | 참조: 3-3

- 정식명: Display Advertisment Platform Core
- 에러코드 ID: 190
- 결제데이터 보유: N
- 보존기간: 12Months
- 담당자: 남유선(Peter Nam) · 심규도(Kyudo Shim)
- 설명(Korean):
  - 광고 플랫폼 코어 컴포넌트
  - DAPM 로 부터 발생된 메세지를 받아, 광고 서비스에 사용할 수 있도록 가공 및 저장, 집계 등을 담당
- 설명(English):
  - Advertising Platform Core Components
  - Responsible for processing, storing, and aggregating messages from DAPM for use in advertising services

## DAPA (Display Advertisment Platform API) — 광고 플랫폼 API 컴포넌트 | 라인: 1572-1585 | 참조: 3-3

- 정식명: Display Advertisment Platform API
- 에러코드 ID: 191
- 결제데이터 보유: N
- 보존기간: 12Months
- 담당자: 남유선(Peter Nam) · 심규도(Kyudo Shim)
- 설명(Korean):
  - 광고 플랫폼 API 컴포넌트
  - 광고 기능 중 API 로 제공되어야할 기능들을 담당
- 설명(English):
  - Advertising platform API components
  - Responsible for the functions that should be provided as API among advertising functions

## MONIS (Monitoring Interface Service) — 관제 / 택시 시스템 간의 연동 컴포넌트 | 라인: 1586-1598 | 참조: 3-3

- 정식명: Monitoring Interface Service
- 에러코드 ID: 192
- 결제데이터 보유: N
- 보존기간: 12Months
- 담당자: 김대우
- 설명(Korean):
  - 관제 / 택시 시스템 간의 연동 컴포넌트
  - 관제 시스템과 택시 호출 시스템의 데이터 연동하기 위한 인터페이스 컴포넌트
- 설명(English):
  - Interface component between taxi system and FMS system

## CBSS (Customer Benefit segmentation statics) — 고객 혜택 집계 관리 컴포넌트 | 라인: 1599-1612 | 참조: 3-3

- 정식명: Customer Benefit segmentation statics
- 에러코드 ID: 193
- 결제데이터 보유: N
- 보존기간: 12Months
- 담당자: Retired_심재성(Jaeseong Sim) · Retired_서정호(Jeongho Seo) · 조진수(JinSu Jo) · 조성구(Sunggu Jo) · 엄지선(Jisun Eom)
- 설명(Korean):
  - 고객 혜택 집계 관리 컴포넌트
  - IAS, KPS의 거래 데이터를 수집하여 혜택 유형별 집계 데이터를 제공
- 설명(English):
  - Customer Benefit Aggregation Management Component
  - Collects transaction data from IAS and KPS to provide aggregate data by benefit type

## CAS (Card Authentification Service) — 카드 인증 서비스 | 라인: 1613-1626 | 참조: 3-3

- 정식명: Card Authentification Service
- 에러코드 ID: 196
- 결제데이터 보유: N
- 보존기간: 12Month
- 담당자: Retired_심재성(Jaeseong Sim) · 엄지선(Jisun Eom) · 안성진(Seongjin Ahn)
- 설명(Korean):
  - 카드 인증 서비스
  - 간편결제 카드인증, 구인증, 해외결제 인증, 직가맹 카드인증 서비스를 제공
- 설명(English):
  - Card Authentification Service
  - Provides simple payment card authentication, old authentication, and direct affiliate store card authentication services.

## PLD (Personal Identifiable Information Leak Detection) — 개인 정보 유출 탐지 컴포넌트 | 라인: 1627-1640 | 참조: 3-3

- 정식명: Personal Identifiable Information Leak Detection
- 에러코드 ID: 197
- 결제데이터 보유: N
- 보존기간: 24Month (미정)
- 담당자: 서정화(Junghwa Seo) · Retired_엄용운(Youngwoon Eom) · 정현주(Hyeonjoo Jeong) · 김형진(Hyungjin Kim)
- 설명(Korean):
  - 개인 정보 유출 탐지 컴포넌트
  - ISMS-P 인증 용 개인 정보 유출 탐지 기능을 담당
- 설명(English):
  - Personal information leak detection components
  - Provides personal information leak detection service for ISMS-P certification

## MDPS (Mobility Data Purge Service) — 모빌리티 데이터 삭제 서비스 | 라인: 1641-1654 | 참조: 3-3

- 정식명: Mobility Data Purge Service
- 에러코드 ID: 198
- 결제데이터 보유: N
- 보존기간: 12Month
- 담당자: 김재헌
- 설명(Korean):
  - 모빌리티 데이터 삭제 서비스
  - ISMS-P 관련하여 데이터 삭제 및 익명화 기능 담당
- 설명(English):
  - Mobility Data Purge Service
  - Responsible for Data Deletion and Anonymization Functions in ISMS-P policy

## ORS (Overseas Remittance Service) — 해외 송금 서비스 | 라인: 1655-1666 | 참조: 3-3

- 정식명: Overseas Remittance Service
- 에러코드 ID: 188
- 결제데이터 보유: 미지정
- 보존기간: 미지정
- 담당자: 홍주표(Joopyo Hong) · 안성진(Seongjin Ahn) · 서용하(Yongha Seo)
- 설명(Korean):
  - 해외 송금 서비스
- 설명(English):
  - Manage overseas remittance service

## VCC (Visible Chatbot Core) — 보이는 챗봇 코어 서비스 | 라인: 1667-1682 | 참조: 3-3

- 정식명: Visible Chatbot Core
- 에러코드 ID: 199
- 결제데이터 보유: N
- 보존기간: 12Month
- 담당자: 남유선(Peter Nam) · 심규도(Kyudo Shim) · 예진욱(Jinuk Ye)
- 설명(Korean):
  - 보이는 챗봇 코어 서비스
  - 사용자로부터 전달받는 메세지를 특정 인덱스에 따라서 사용자를 가이드하고 메세지를 AI 코어 서비스로 전달하는 서비스
  - 기획자로부터 정의받은 인덱스를 관리하는 서비스
- 설명(English):
  - Visible Chatbot Core
  - Responsible for receive user message from VCF components and lead to follow certain indexes and send message to AI core service
  - Response for management certain indexes defined by project manager

## AICC (AI Contact Center) — AI 고객센터 | 라인: 1683-1698 | 참조: 3-3

- 정식명: AI Contact Center
- 에러코드 ID: 200
- 결제데이터 보유: N
- 보존기간: 60Months
- 담당자: 담당자 변경 · 서정화, 엄용운 -> · 이민구(Min-goo Lee) · 홍주표(Joopyo Hong) · 김현수(HyunSoo Kim) · 박한결(Hankyeol Park) · 예진욱(Jinuk Ye)
- 설명(Korean):
  - AI 고객센터
  - 고객 문의 의도 파악
  - 시스템 정책과 개인화 데이터를 기반으로 AI 알고리즘을 활용하여 고객 서비스 운영 간소화
- 설명(English):
  - AI Contact Center
  - Understanding the intent of customer inquiries
  - The system simplifies customer service operations by utilizing AI algorithms based on system policies and personalized data

## VAS (Voice Assistant Service) — 음성 비서 서비스 | 라인: 1699-1712 | 참조: 3-3

- 정식명: Voice Assistant Service
- 에러코드 ID: 201
- 결제데이터 보유: N
- 보존기간: 60Months
- 담당자: 서정화(Junghwa Seo) · 정현주(Hyeonjoo Jeong)
- 설명(Korean):
  - 음성 비서 서비스
  - 음성을 텍스트로(STT), 텍스트를 음성으로(TTS) 변환
- 설명(English):
  - Voice Assistant Service
  - Speech to Text(STT), Text to Speech(TTS)

## AMM (AppMeter Manager) — 앱미터 매니저 | 라인: 1713-1726 | 참조: 3-3

- 정식명: AppMeter Manager
- 에러코드 ID: 203
- 결제데이터 보유: N
- 보존기간: 60Month
- 담당자: 박동민
- 설명(Korean):
  - 앱미터 매니저
  - 앱미터 단말기 개통, 해지, 설정 업데이트를 하는 서비스
- 설명(English):
  - AppMeter Manager
  - Service for opening, canceling, and updating settings of AppMeter terminals

## MSMA (Mobility Supply-chain Management Api Service) — 모빌리티 자산 관리 시스템 | 라인: 1727-1739 | 참조: 3-3

- 정식명: Mobility Supply-chain Management Api Service
- 에러코드 ID: 204
- 결제데이터 보유: N
- 보존기간: 60Month
- 담당자: Retired_강동수
- 설명(Korean):
  - 모빌리티 자산 관리 시스템
  - 모빌리티 자산에 대한 관리를 하는 서비스
- 설명(English):
  - Mobility Supply-chain Management Api Service

## MSMW (Mobility Supply-chain Management Web) — 모빌리티 자산 관리 시스템 포탈 | 라인: 1740-1752 | 참조: 3-3

- 정식명: Mobility Supply-chain Management Web
- 에러코드 ID: 205
- 결제데이터 보유: N
- 보존기간: 60Month
- 담당자: Retired_강동수
- 설명(Korean):
  - 모빌리티 자산 관리 시스템 포탈
  - 모빌리티 자산에 대한 관리하는 포탈
- 설명(English):
  - Mobility Supply-chain Management Web

## MOSP (Mobility OTA Service Portal) — 모빌리티 OTA 서비스 포탈 | 라인: 1753-1765 | 참조: 3-3

- 정식명: Mobility OTA Service Portal
- 에러코드 ID: 206
- 결제데이터 보유: N
- 보존기간: 60Month
- 담당자: 박동민
- 설명(Korean):
  - 모빌리티 OTA 서비스 포탈
  - 앱미터 OTA 관리 포탈
- 설명(English):
  - Mobility OTA Service Portal

## VCF (Visible Chatbot Front) — 보이는 챗봇 | 라인: 1766-1779 | 참조: 3-3

- 정식명: Visible Chatbot Front
- 에러코드 ID: 207
- 결제데이터 보유: N
- 보존기간: 60Month
- 담당자: 신동욱(Dongwook Shin)
- 설명(Korean):
  - 보이는 챗봇
  - 사용자로부터 전달받는 메세지를 특정 인덱스에 따라서 사용자를 가이드하고 메세지를 AI 코어 서비스로 전달하는 서비스
- 설명(English):
  - a visible chatbot
  - A service that guides users according to specific indexes and delivers messages to AI core services

## FXS (Foreign eXchange Service) — 외환 관리 서비스 | 라인: 1780-1799 | 참조: 3-3

- 정식명: Foreign eXchange Service
- 에러코드 ID: 210
- 결제데이터 보유: N
- 보존기간: 60 Month
- 담당자: 심재진(Jaejin Sim)
- 설명(Korean):
  - 외환 관리 서비스
  - 외화 계좌 및 매입/매도 내역 관리
  - 실시간 환율 조회 서비스 제공
  - 보유 외화 환율 평단가 관리
  - 외화 매입/매도 정산
- 설명(English):
  - Foreign Exchange Service
  - Managing foreign currency accounts and purchase/sale details
  - Providing real-time exchange rate inquiry service
  - Managing the unit price of foreign currency exchange rate held
  - Settlement of foreign currency purchases/sale

## LBMS (Location-Base Merchant Service) — 위치 기반 가맹점 서비스 | 라인: 1800-1813 | 참조: 3-3

- 정식명: Location-Base Merchant Service
- 에러코드 ID: 212
- 결제데이터 보유: N
- 보존기간: 60 Month
- 담당자: 하승원(SeungWon Ha) · 조성구(Sunggu Jo)
- 설명(Korean):
  - 위치 기반 가맹점 서비스
  - 위치 기반 가맹점 정보 조회를 위해 Elasticsech에 가맹점 정보를 관리 및 조회
- 설명(English):
  - Location-Base Merchant Service
  - Management and inquiry of merchant information to Elasticsech for location-based merchant information inquiry

## MASI (Mobility Application Service Interface) — 모빌리티 택시 데이터 조회 서비스 | 라인: 1814-1827 | 참조: 3-3

- 정식명: Mobility Application Service Interface
- 에러코드 ID: 213
- 결제데이터 보유: N
- 보존기간: 12 Months
- 담당자: 김재헌
- 설명(Korean):
  - 모빌리티 택시 데이터 조회 서비스
  - 포탈에서 데이터 Read 전용(masm, masp, ...)
- 설명(English):
  - Mobility taxi data inquiry service
  - Read only data from portal(masm, masp, ...)

## COPS (Co-Payment Service) — 모아서 결제 서비스 | 라인: 1828-1845 | 참조: 3-3

- 정식명: Co-Payment Service
- 에러코드 ID: 214
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 안성진(Seongjin Ahn)
- 설명(Korean):
  - 모아서 결제 서비스
  - 결제참여 요청 및 승인/거절
  - 모으기 / 모으기 취소
  - 모아서 결제
- 설명(English):
  - Collection payment service
  - Payment participation request and approval/rejection
  - Collect / Cancel Collect
  - Collect and pay

## KS-BATCH (KS data batch server) — 고객센터 모니터링을 위한 배치 | 라인: 1846-1861 | 참조: 3-3

- 정식명: KS data batch server
- 에러코드 ID: 208
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 신동욱(Dongwook Shin)
- 설명(Korean):
  - 고객센터 모니터링을 위한 배치
  - KS의 CTI 데이터 중 일부를 조회 해 KONAI DB에 적재한다.
  - KS의 데이터를 실시간으로 보기 위해 API를 제공한다.
- 설명(English):
  - Batch Server for Customer Center Monitoring
  - Some of KS's CTI data are inquired and loaded into the KONAI DB.
  - We provide an API to view KS's data in real time.

## DBMT (Database Monitoring) — 데이터베이스 모니터링 컴포넌트 (API 서버) | 라인: 1862-1875 | 참조: 3-3

- 정식명: Database Monitoring
- 에러코드 ID: 216
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: @서정호 · @김민호
- 설명(Korean):
  - 데이터베이스 모니터링 컴포넌트 (API 서버)
  - x7, x8, x9 의 db cpu 부하 상태에 대한 API를 제공한다.
- 설명(English):
  - Database monitoring component (API server)
  - Provides API for DB CPU load status of x7, x8, x9.

## VAM (Virtual Account Management) — 가상 계좌 매핑 및 관리 서비스 | 라인: 1876-1887 | 참조: 3-3

- 정식명: Virtual Account Management
- 에러코드 ID: 218
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 심재진(Jaejin Sim)
- 설명(Korean):
  - 가상 계좌 매핑 및 관리 서비스
- 설명(English):
  - Virtual Account Management service

## RDMT (Rundeck Monitoring) — 런덱 모니터링 컴포넌트 (API 서버) | 라인: 1888-1900 | 참조: 3-3

- 정식명: Rundeck Monitoring
- 에러코드 ID: 220
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: Retired_서정호(Jeongho Seo) · Retired_김민호(Minho Kim) · 옥승주(Seungju Oak)
- 설명(Korean):
  - 런덱 모니터링 컴포넌트 (API 서버)
  - 런덱의 구동 상태, 스케쥴 진행 상태 등에 대한 API를 제공한다
- 설명(English):
  - Rundeck monitoring component (API server)

## AICV (AI Contract Validation) — 가맹점 계약 검증 컴포넌트 (API 서버) | 라인: 1901-1913 | 참조: 3-3

- 정식명: AI Contract Validation
- 에러코드 ID: 219
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 서정화(Junghwa Seo) · Retired_엄용운(Youngwoon Eom) · 김수환(Suhwan KiM) · 정현주(Hyeonjoo Jeong) · 김형진(Hyungjin Kim)
- 설명(Korean):
  - 가맹점 계약 검증 컴포넌트 (API 서버)
  - 가맹점 계약 검수 API를 제공한다.
- 설명(English):
  - Merchant Contract Validation component (API server)

## SCC (Spring Cloud Config) — OpenAPI 관련 컴퍼넌트 설정 정보 통합 관리 컴퍼넌트 | 라인: 1914-1929 | 참조: 3-3

- 정식명: Spring Cloud Config
- 에러코드 ID: 220
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 하승원(SeungWon Ha)
- 설명(Korean):
  - OpenAPI 관련 컴퍼넌트 설정 정보 통합 관리 컴퍼넌트
  - TGS의 설정 정보 변경 시 서비스 재시작 없이 API를 통해서 실시간 반영하도록 설정 정보를 제공한다.
  - 컴퍼넌트 필요 시 통합 관리 설정 정보 추가 가능
- 설명(English):
  - Component of Management Configuration
  - When TGS configuration information is changed, the configuration information is provided to be reflected in real time through API without restarting the service.
  - Integrated management setting information can be added when required for components

## SDTS (Secure Document Transfer System) — 솔리데오 PINO 전자문서지갑 서비스 제공 | 라인: 1930-1941 | 참조: 3-3

- 정식명: Secure Document Transfer System
- 에러코드 ID: 223
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 심규도(Kyudo Shim)
- 설명(Korean):
  - 솔리데오 PINO 전자문서지갑 서비스 제공
- 설명(English):
  - Secure Document Transfer System

## CLR_KT (Clearing Kotlin) — 코나카드 정산 컴포넌트는 거래 데이터를 기반으로 수수료와 대금을 계산하고, 지급 데이터를 생성합니다. Spring Boot 3.2.3, J... | 라인: 1942-1953 | 참조: 3-3

- 정식명: Clearing Kotlin
- 에러코드 ID: 224
- 결제데이터 보유: Y
- 보존기간: 60 Months
- 담당자: 서버개발4팀
- 설명(Korean):
  - 코나카드 정산 컴포넌트는 거래 데이터를 기반으로 수수료와 대금을 계산하고, 지급 데이터를 생성합니다. Spring Boot 3.2.3, JDK 21, Kotlin으로 업그레이드된 CLR_KT로 새롭게 제공됩니다. 정산은 서비스에 영향을 주지 않도록 새벽 시간에 자동으로 처리됩니다.
- 설명(English):
  - The Kona Card Clearing kotlin component calculates fees and payments based on transaction data and generates payment data. Previously built with Spring Boot 1.x, JDK 8, and Java, it has now been upgraded to CLR_KT, using Spring Boot 3.2.3, JDK 21, and Kotlin. Clearing kotlin processes are automatically handled during early morning hours to avoid service disruption.

## PRS (Personalized Recommendation System) — 개인 맞춤형 추천 시스템 | 라인: 1954-1967 | 참조: 3-3

- 정식명: Personalized Recommendation System
- 에러코드 ID: 226
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 서용하(Yongha Seo) · 엄지선(Jisun Eom)
- 설명(Korean):
  - 개인 맞춤형 추천 시스템
  - 사용자의 활동 이력을 기반으로 자주 사용하는 서비스를 알려주고, 사용자를 성별/연령대/지역 등으로 구분해 그룹화하여 그룹별 선호하는 서비스를 분석하여 사용자 맞춤 서비스를 추천해준다.
- 설명(English):
  - Personalized Recommendation System
  - Based on the user's activity history, it informs frequently used services, groups users by gender/age group/region, and analyzes preferred services for each group to recommend customized services.

## OPBO (Open Partner Back-Office) — 개방형 플랫폼 제휴 파트너 API 사용량 대시보드/통계 | 라인: 1968-1981 | 참조: 3-3

- 정식명: Open Partner Back-Office
- 에러코드 ID: 227
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 미지정
- 설명(Korean):
  - 개방형 플랫폼 제휴 파트너 API 사용량 대시보드/통계
  - Konaplate를 사용하는 제휴사들의 API 사용량, 통계 및 기타 서비스를 제공한다.
- 설명(English):
  - Open Partner Back-Office
  - Provides API usage, statistics, and other services for affiliates using Konaplate.

## KTC (Kona Traffic Controller) — 트레이서 대기열 솔루션을 내재화한 프로젝트 | 라인: 1982-1995 | 참조: 3-3

- 정식명: Kona Traffic Controller
- 에러코드 ID: 228
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 예진욱(Jinuk Ye)
- 설명(Korean):
  - 트레이서 대기열 솔루션을 내재화한 프로젝트
  - 앱/웹 진입 의 특정 Zone 진입 시 N분 당 M명의 사용자만 접속을 허용하며, 대기중인 사용자에게 현재 대기열 순번을 제공한다.
- 설명(English):
  - Project Internalizing Tracer Queue Solutions
  - When entering a specific zone of app/web entry, only M users are allowed to access per N minutes, and the current queue sequence is provided to the waiting users.

## KTCA (Kona Traffic Controller API Server) — 트레이서 대기열 솔루션을 내재화한 프로젝트의 API 서버 | 라인: 1996-2009 | 참조: 3-3

- 정식명: Kona Traffic Controller API Server
- 에러코드 ID: 229
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 심규도(Kyudo Shim) · 예진욱(Jinuk Ye)
- 설명(Korean):
  - 트레이서 대기열 솔루션을 내재화한 프로젝트의 API 서버
  - 특정 Zone 에 대한 N분당 M명의 사용자만 접속 허용하는 정책을 반영하며, 실시간 Zone 및 대기열 현황을 시각화하기 위한 데이터를 제공한다.
- 설명(English):
  - API servers for projects that internalize tracer queue solutions
  - It reflects a policy that allows access to only M users per N minutes for a specific zone, and provides data for visualizing real-time zone and queue status.

## STT (SpeechToText) — 음성파일을 텍스트로 변환기능 제공 | 라인: 2010-2021 | 참조: 3-3

- 정식명: SpeechToText
- 에러코드 ID: 230
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 서정화(Junghwa Seo)
- 설명(Korean):
  - 음성파일을 텍스트로 변환기능 제공
- 설명(English):
  - Provides the ability to convert voice files to text

## AFS (Annual Fee Service) — 연회비 서비스. | 라인: 2022-2037 | 참조: 3-3

- 정식명: Annual Fee Service
- 에러코드 ID: 233
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 심재진(Jaejin Sim) · 예진욱(Jinuk Ye)
- 설명(Korean):
  - 연회비 서비스.
  - 카드 혜택에 따른 정기 결제를 담당한다.
  - 결제는 카드 출금 실패 시 계좌 출금 순으로 진행한다.
- 설명(English):
  - Annual fee service.
  - It's responsible for the recurring payments based on card benefits.
  - Payments are processed first by card debit and then by bank account debit if the card payment fails.

## CIMS (Card Inventory Management Service) — 카드 재고 관리 서비 | 라인: 2038-2051 | 참조: 3-3

- 정식명: Card Inventory Management Service
- 에러코드 ID: 232
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 안성진(Seongjin Ahn)
- 설명(Korean):
  - 카드 재고 관리 서비
  - E2MAX 와 연동하여 카드 재고를 관리한다.
- 설명(English):
  - Card Inventory Management Service
  - Manage card inventory in conjunction with E2MAX.

## IIS (Instant Issue Service) — 즉시 발급 서비스 | 라인: 2052-2063 | 참조: 3-3

- 정식명: Instant Issue Service
- 에러코드 ID: 236
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 남유선(Peter Nam)
- 설명(Korean):
  - 즉시 발급 서비스
- 설명(English):
  - Instant Issue Service

## ACC (Agent Chatbot Core) — 지역화폐 챗봇 에이전트 - 코어 서버. | 라인: 2064-2079 | 참조: 3-3

- 정식명: Agent Chatbot Core
- 에러코드 ID: 237
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 이민구(Min-goo Lee) · 홍주표(Joopyo Hong) · 김현수(HyunSoo Kim) · 박한결(Hankyeol Park) · 예진욱(Jinuk Ye)
- 설명(Korean):
  - 지역화폐 챗봇 에이전트 - 코어 서버.
  - AI(LLM) + 지역화폐 관련 문서 + 여러 Wallet 서버들의 정책 / 개인화 정보들을 조합하여 응답한다.
  - 민감정보는 마스킹 처리된다.
- 설명(English):
  - The Core Server generates responses by synthesizing AI (LLM), local currency-related documentation, and the specific policies and personalized information from various Wallet servers.
  - Data Synthesis: Integrates LLM capabilities with domain-specific knowledge bases and real-time wallet data.
  - Data Security: All sensitive information is processed using masking to ensure privacy.

## ACW (Agent Chatbot Web) — 지역화폐 챗봇 에이전트 - 웹 서버. | 라인: 2080-2094 | 참조: 3-3

- 정식명: Agent Chatbot Web
- 에러코드 ID: 238
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 이민구(Min-goo Lee) · 홍주표(Joopyo Hong) · 김현수(HyunSoo Kim) · 박한결(Hankyeol Park) · 예진욱(Jinuk Ye)
- 설명(Korean):
  - 지역화폐 챗봇 에이전트 - 웹 서버.
  - ACC와 SSE 통신을 하며 사용자에게 화면을 실시간 렌더링한다.
- 설명(English):
  - The Web Server handles the real-time interface, communicating with the ACC via SSE to render screens for the user.
  - Communication: Utilizes SSE (Server-Sent Events) for persistent, real-time data flow.
  - UI Rendering: Executes real-time screen rendering to provide a seamless user experience.

## MLS (Mileage service) — 마일리지 서비스 | 라인: 2095-2107 | 참조: 3-3

- 정식명: Mileage service
- 에러코드 ID: 239
- 결제데이터 보유: N
- 보존기간: 미지정
- 담당자: 안성진(Seongjin Ahn)
- 설명(Korean):
  - 마일리지 서비스
  - 마일리지 적립, 사용, 취소, 만료 기능을 제공 한다.
- 설명(English):
  - Mileage Service
  - Provides functions for accumulating, using, canceling, and expiring mileage.
