# Team 3 최종 소스 감사 및 코드 동결 검토 — 2026-11-03

## 기준과 검증 출처
- Repo: `dohun3540-crypto/integration_finished_workforlast` / Draft PR #3, base `feat/final-quality-regression-audit-20261103` @ `e948a4a6d3aba6aacd68495bec422b1e845075a0`.
- 최초 감사 대상 PR HEAD: `a1e6e59d78fc2efc174f55d6b49b10c5d86dbe10` (원격 SHA 일치). 최종 코드 수정 HEAD: `bbd2c1ea359fa2a3655a9cf099129a1cb0284316`. 원본 팀원3 READ ONLY: `leadtime-guardian-agent` @ `a925103077173b37d1cefcd6a9576ae644dc2040` (원격 SHA 일치).
- 최초 HEAD 두 CI의 실제 head_sha 일치와 SUCCESS를 재확인했다. 최소 버그 수정 이후 [통합 CI #41604457812](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41604457812), [팀3 CI #41604457818](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41604457818) 모두 새 코드 SHA에서 SUCCESS.
- Repo Git tree를 재귀 조회했다(트리 461항목, truncated=false). 기준 브랜치 대비 수정/추가한 비문서 경로는 총 9개이며 모두 팀3 신규 모듈·회귀 테스트·케이스 후보·전용 CI이고, 기존 Team1/Team2/기존 PDF/DRAFT/GitHub Main 소스의 Git Blob은 일치했다.

## 소스별 판정
| 대상 | 감사 결과 | 주의할 계약 / 보완 |
|---|---|---|
| `qa/inventory.py` | PASS | 합성 PDF 60건에 대한 manifest ID·종류·SHA·페이지 검사, 압축 XZ 읽기·크기 상한·경로/심볼릭 링크 검사. 원본 김민주 버전보다 엄격한 통합 버전 보존. |
| `qa/review_records.py` | PASS | CSV 스키마, 중복 키, 누락 검수자/타임존 시각·원본 후보 변경 검사. 사람 신원 인증이나 승인 승격 기능 아님. 원본 Blob 일치. |
| `qa/xlsx_snapshot.py` | PASS | 원본 XLSX 바이트 읽기 전용, 날짜/숫자/문자 타입, 수식·병합·숨긴 행·시트 검사, zip 크기/항목 수 제한. 실행·인증하지 않음. 원본 Blob 일치. |
| `qa/review_bridge.py` | PASS after fix | CSV 대비 XLSX 셀 타입 및 기준값 대조, 명시적 null과 blank 분리, 부재 검수 필요, 거짓/무인증 승인 차단. `TEAM_APPROVED`에 ACCEPT가 없으면 BLOCKED. |
| `qa/gold_metrics.py` | PASS after fix | 사람 승인 메타데이터의 **형식** + Native Job/Config/각 파일 SHA 바인딩 필요; 필드별 승인 원문 근거 필수; 자료 부족 시 공식 NOT_MEASURED. 중복·불명확·타 케이스 Evidence, True==1 페이지 비교, 잘못된 승인 시각/해시 검증 보강. |
| `qa/gold_candidates/` | PASS / Human Gold BLOCKED | C001 기존 후보는 원본 SHA와 동일한 AI_CANDIDATE. C008/13/17은 기계 템플릿·DRAFT 근거 후보이며 독립 Human Gold 아님. |
| `qa/templates/` | PASS | 검수·케이스 매트릭스 CSV는 원본과 Blob 일치; 실제 승인 기록을 작성한 것으로 간주하지 않음. |
| `tests/qa/` | PASS | 기존 QA 테스트를 삭제·완화하지 않고 직접적인 반례 테스트만 추가. Synthetic test-fixture의 승인값은 진짜 승인 근거가 아님. |
| `.github/workflows/member3-data-check.yml` | PASS | PR에서 95 전용 pytest, QA Ruff, 60 PDF, C001 미승인 정확도 차단. 전체 CI는 별도 `ci.yml`로 861 및 Team1 E2E 37개. |

## 감사에서 실제 발견·수정한 안전 결함
1. **Evidence 중복/혼입:** 기존 `any` 검사는 올바른 근거 1개와 중복·타 케이스 잘못된 근거가 함께 있을 때도 PASS 가능. 증거별 유일한 `(document_id, field_path)` 검사와 외부 경로·케이스 혼입 차단, 정확도 분자도 중복 시 인정하지 않도록 최소 수정.
2. **PDF 페이지 타입:** Python `True == 1` 특성으로 Bool 페이지가 1페이지로 합격할 위험 제거.
3. **승인 메타데이터:** 공백/숫자 검수자, 잘못된 타임존 검수시각·승인 기록 해시 형식을 사실상 허용하던 경우 구조적 평가 Gate 차단. 다만 **실제 신원/서명 검증은 외부 검수 절차의 책임**이다.
4. **충돌 없는 지표:** PO 충돌이 없는 케이스에서 business-block 지표 분모 0이면 분자도 0으로 정정(`NOT_MEASURED`).
5. **XLSX 상태 불일치:** `TEAM_APPROVED` / `REVIEWED_BY_MEMBER3` 라벨에 `ACCEPT`가 없으면 구조검사 BLOCKED.

코드 변경 범위는 `qa/gold_metrics.py`, `qa/review_bridge.py`, 관련 테스트뿐이다. 새 기능 개발이나 품질을 위한 무의미한 테스트 증가는 없었으며 위 결함 각각의 반례에 한정해 테스트를 추가했다.

## 남은 결함 및 아키텍처 경계
- **Critical P0/P1 코드 결함**: 이번 범위의 검증된 추가 결함 0건 (위 5종 수정 및 회귀 통과). 소스 감사가 임의·악성 데이터의 완전한 형식적 보증을 뜻하지는 않는다.
- **EXTERNAL_EVIDENCE_BLOCKED**: 최신 사용자 `PDF_EVIDENCE_MATRIX.xlsx` 원본, 검수자/시각/팀 승인, 원문 시각 확인, Gold Frozen SHA와 독립 승인 서명, 같은 케이스의 최신 Studio Native 예측 및 Job/Config/File ID가 없음. 외부 입력이 없는 이유로 코드 작업을 계속하지 않는다.
- **신뢰 경계**: 승인 JSON 메타데이터/sha 문자열은 실제 승인 인원의 신원을 증명하지 않고, Studio 바인딩 문자열만으로 실제 원격 Job을 인증하지 않는다. 외부 검수·Team1 Live 실행 출처 확인이 필수.
- **원본 리포트 파일**: 원본 팀3 저장소의 과거 이관/핸드오프 보고서는 대상 저장소에 그대로 복사되지 않았지만, 현재 `docs/team3_quality_20261103/` 결과와 원본 PR #13을 명시해 인계할 수 있다. 실행 기능 결함으로 취급하지 않는다.

## 판정
- `TEAM3_CODE_FREEZE = APPROVED`: 위 최소 패치가 포함된 코드 SHA를 동결한다. 더 이상의 기능 개발 금지.
- `TEAM3_HANDOFF_READY = READY_WITH_EXTERNAL_DEPENDENCIES`: 명령·경로·입력 계약을 인계한다.
- `TEAM3_SUBMISSION_DATA_READY = BLOCKED`: CI 성공은 사람 승인이나 실제 Studio 정확도 산출을 대체하지 않는다.

문서 패키징은 코드 SHA 이후 별도 문서-only 커밋이므로 최종 PR HEAD CI 결과를 한 번 더 확인해야 한다.
