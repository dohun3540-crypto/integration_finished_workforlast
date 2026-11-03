# 데이터 품질 전수 감사

감사일: 2026-11-03T13:53:16.870235+09:00

감사 대상 코드 HEAD: `b78c8c0e8dff5480c850bce8868de40ed71f49c8` / Git Tree: `5e378f4bb3c3f40c67e81a7bbe5d8686cf3ab450`.
안전 기준선: `9684b8d9f2098191ca2b1bc3f1c5645321fc6ed5`. [추가 변경 Draft PR #2](https://github.com/dohun3540-crypto/integration_finished_workforlast/pull/2).
이 보고서와 증거 파일을 추가한 후의 최종 HEAD/CI는 PR #2 본문에 별도로 기록합니다.
보고서가 자기 자신의 커밋 SHA를 포함할 수 없으므로 코드 검증 SHA와 문서 패키징 SHA를 구분합니다.


60/60 PDF가 원본 SHA·페이지·파싱 검사를 통과했습니다. 두 합성 문서 템플릿의 실제 페이지에서 라벨 바로 다음 값과 표 셀을 추출해 DRAFT와 대조했고 60/60에서 일치했습니다. 숫자가 페이지의 다른 위치에 존재하는지만 확인하는 substring 검사는 사용하지 않았습니다. 정확도/개선률은 NOT_MEASURED, Human Gold와 최신 사람 검수 XLSX는 MISSING_REQUIRED_EVIDENCE입니다.

기계 검사 상세: [semantic-pdf.json](evidence/semantic-pdf.json), [원본 인벤토리](evidence/inventory/INVENTORY_REPORT.json). 모든 문서 결과에 filename, 원본 SHA, page, 검사 필드 및 날짜 원문/정규화 값을 연결했습니다. 이 결과는 기존 합성 템플릿의 텍스트 대조이며 이미지의 시각적 정확성·실제 공급자 내용·사람 정답 인증이 아닙니다.

## 20개 Case × 8개 차원

아래 PASS의 범위: Accuracy는 미승인 DRAFT와 라벨/표 텍스트의 일치, Timeliness는 날짜 구문 및 원문 정규화, Traceability는 로컬 페이지/SHA 연결입니다. 클라우드 File ID·업로드 원본 인증과 사람 검수는 모든 Case에서 NOT_VERIFIED/NEEDS_HUMAN_REVIEW입니다. 필수 값이 없는 Case의 Validity는 NOT_VERIFIED로 구분했습니다.

| Case | Completeness | Validity | Consistency | Accuracy | Uniqueness | Timeliness | Traceability | Integrity |
|---|---|---|---|---|---|---|---|---|
| SYN-C001 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C002 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C003 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C004 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C005 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C006 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C007 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C008 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C009 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C010 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C011 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C012 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C013 | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS |
| SYN-C014 | FAIL | NOT_VERIFIED | FAIL | PASS | PASS | PASS | PASS | PASS |
| SYN-C015 | FAIL | NOT_VERIFIED | FAIL | PASS | PASS | PASS | PASS | PASS |
| SYN-C016 | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS |
| SYN-C017 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C018 | FAIL | NOT_VERIFIED | FAIL | PASS | PASS | PASS | PASS | PASS |
| SYN-C019 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SYN-C020 | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS |


## 의도된 불량 자료와 업무 계산

| Case | 원본에서 확인된 내용 | 실제 Safety V6 결과 |
|---|---|---|
| C001 | 발주/통보 수량 100, 대체 견적 capacity 60, 단가 1,000, 운송비 500 | 기존 부족 0 → 변경 부족 60, 대체 60, 총 60,500 KRW |
| C008 | 발주 R1=40/R2=60, 통보는 R2만 변경 | 변경 부족 40, 비용 40,500 KRW, R1 ETA 보존 |
| C013 | 발주 PO1, 통보 PO999 | 잘못된 receipt 매칭을 BLOCKED |
| C014 | 변경일 NOT PROVIDED | 필수 변경일 누락 BLOCKED |
| C015 | 통보 수량 NOT PROVIDED | null을 0으로 바꾸지 않고 BLOCKED |
| C016 | 통보 품목 UNKNOWN-X | trusted inbound와 미일치 BLOCKED |
| C017 | 2026년 11월 3일/8일/4일 | ISO 정규화 일치; 원문과 페이지 SHA 보존 |
| C018 | 동일 PO에 두 receipt, 통보 receipt 누락 | 임의 배분 없이 BLOCKED |
| C020 | 표 11/8, 문구 11/9 | 경고가 있는 문서 BLOCKED |

이 6개 차단 Case는 의도된 적대적 입력이며 원본 오류를 임의 보정하지 않았습니다. 나머지 14개는 합성/보관 로컬 계산 경로에서 COMPLETED였습니다. C001의 과거 Native는 10/30 v4 보관 자료이며 신규 Live로 표기하지 않았습니다.

## CSV/XLSX/Gold와 정보 누출

- 현재 tracked CSV의 헤더 중복·행 열 수와 Strict JSON 검사를 실행했습니다. 수량/금액/날짜, null·0·Boolean, 중복 키 및 비유한/underflow 숫자는 기존 회귀와 추가 금액 회귀로 검증했습니다.
- 검수 XLSX는 저장소에 없습니다. 필수 Sheet/Column의 실제 파일 감사는 NOT_RUN입니다. Shared String/빈 셀·index 49 계약은 기존 합성 XLSX 회귀로만 확인했습니다. 이전 문서의 XLSX SHA가 파일 존재 증거가 되지는 않습니다.
- `qa.review_records`는 검수자·시간·기준 후보 일치 형식만 확인하며 사람 신원이나 Gold 승인 권한을 인증하지 않습니다.
- C001 Gold 후보는 AI_CANDIDATE, human_reviewed=false, team_approved=false, eligible_for_official_metrics=false, gold_frozen=false를 유지합니다. C002–C020 DRAFT도 미검수 상태입니다.
- DRAFT는 PDF generator와 같은 원천에서 만들어졌습니다. 텍스트와 일치한다는 사실로 독립 평가 정답을 확보했다고 볼 수 없습니다. 운영 ingest는 Gold/fixture wrapper를 거절하고, candidate 비교는 공식 정확도에 사용하지 않습니다.
- 운송비는 견적별 1회, 견적 60은 발주 100과 별개, 원본 통화/단위는 KRW/EA입니다. 통화·단위 충돌 및 중복 receipt는 기존 경계 회귀로 차단됩니다.
