# Team 3 최종 회귀검증 기록 — 2026-11-03

## 정확한 실행 출처
- 수정된 코드 HEAD: `bbd2c1ea359fa2a3655a9cf099129a1cb0284316`.
- [GitHub Actions Integrated Python QA #41604457812](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41604457812): **SUCCESS**, 전체 pytest **861 passed**, Team1 E2E 단독 **37 passed**, `python -m ruff check .` PASS.
- [GitHub Actions Team 3 Gold Data Quality Checks #41604457818](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41604457818): **SUCCESS**, `python -m pytest tests/qa -q` **95 passed**, `python -m ruff check qa tests/qa` PASS.
- 양쪽 CI 모두 `python -m qa.inventory --root . --out ...` : **PASS 60/60**, FAIL 0/BLOCKED 0, SHA 중복 0. XZ 원본 아카이브 SHA-256 `a3f4ed1cefee4ebea3a4b94f9408f8a039bf042bd651a3a9222a5162c22149dc`.
- 통합 CI의 archive/local C001 replay 예상 상태 `PASS_LOCAL`/release `BLOCKED`, full protected-file / archived synthetic semantic PDF audit 단계도 성공. 테스트 828개였던 원래 base 대비 기존 테스트 파일을 삭제하거나 의미를 바꾼 변경 경로는 0개.

## 의무 검증별 증거 상태
| 항목 | 상태 | 실제 실행 및 한계 |
|---|---|---|
| 전체 pytest, B/C 기존 회귀 | PASS | 통합 CI 861. 각 시나리오를 *Live* Native 환경에서 별도 재실행한 것은 아님. |
| 팀3 pytest | PASS | 전용 CI 95. |
| 팀1 E2E / Adapter 계약 | PASS | CI에서 기존 타깃 테스트 37. 팀1 소스 Blob 불변. |
| 전체/QA Ruff | PASS | 각각 통합 및 팀3 전용 CI 로그 확인. |
| PDF SHA·페이지·XZ·경로·manifest | PASS | 실제 GitHub runner의 원본 바이트에 대해 60/60 기계 검사, 0 SHA 중복. 사람 원문 시각 검토는 NOT_VERIFIED. |
| 검수 CSV/XLSX 타입·null·수식·중복 | PASS | synthetic 회귀로 검사. 진짜 최신 검수 XLSX 파일이 없어 사용자 검수 결과 대조는 EXTERNAL_EVIDENCE_BLOCKED. |
| C001 후보, 미승인 Gold 지표 차단 | PASS | `AI_CANDIDATE` -> `BLOCKED / NOT_MEASURED / metrics={}`의 CLI 부정 검증 CI PASS. |
| C008 Receipt 분할 | PASS | 후보 R1 40, R2 60, notice R2만 60; 실제 Studio 정확도 NOT_MEASURED. |
| C013 PO 원문 충돌·계산 분리 | PASS_LOCAL | 후보 PO1/PO999/PO1과 synthetic 평가기의 충돌 탐지 vs business-block 분리. Native 업무 차단은 NOT_VERIFIED. |
| C017 한국어 날짜 | PASS | 한국어 원문 11/3·11/8·11/4 보존, ISO 후보 2026-11-03·08·04 일치, 시각 검수/Studio는 미실행. |
| Evidence ID·SHA·페이지·원문·null·중복·타 케이스 | PASS | 반례 회귀: 잘못된 데이터면 PASS 불가; 근거 없는 Synthetic Studio 실측을 주장하지 않음. |
| 잘못된 승인 시각·해시·상태 | PASS | 잘못된 승인 메타데이터는 NOT_MEASURED, 엑셀 승인-결정 불일치는 BLOCKED. 사람 신원 인증은 별도. |
| 원본 PDF·Gold DRAFT·Team1·Team2 불변 | PASS | 기준 HEAD Git Blob 비교. 작업 범위 외 수정 없음. |
| 최신 Native Job/Config/File ID·사람 Gold 승인 | EXTERNAL_EVIDENCE_BLOCKED | 실제 제출자료 확보 전; 측정 수치 작성 불가. |

## 케이스별 결과의 근거 수준
| 케이스 | A. PDF 기계 검사 | B. 후보 일관성 | C. Human Gold | D. Studio 실측 | E. 업무 차단 |
|---|---|---|---|---|---|
| C001 | PASS | PASS (100 EA 발주/R1, 60 EA 견적/PO1, 날짜별 구분) | BLOCKED | NOT_MEASURED | PASS_LOCAL archived only; Live NOT_VERIFIED |
| C008 | PASS | PASS (R1=40, R2=60, notice R2만 지연) | BLOCKED | NOT_MEASURED | NOT_VERIFIED |
| C013 | PASS | PASS (PO1/PO999/PO1, 원문 자동수정 안 함) | BLOCKED | NOT_MEASURED | NOT_VERIFIED (synthetic 충돌 Gate만 PASS) |
| C017 | PASS | PASS (한국어 날짜 원문과 ISO 날짜 후보) | BLOCKED | NOT_MEASURED | NOT_VERIFIED |

**메트릭 규칙:** 승인 출처와 Native 실행 연결이 없으면 공식 지표 분자·분모를 계산하지 않고 `NOT_MEASURED`. 실험용 Mock fixture의 `MEASURED`는 테스트용 내부 계약 평가이지 대회 제출용 정확도가 아니다.

## 재현 명령
실행 환경: GitHub ubuntu-latest / Python 3.11 / `requirements-validation.txt`. 실제 사용된 명령은 `.github/workflows/ci.yml` 및 `member3-data-check.yml`에 보존.
```bash
python -m pip install -r requirements-validation.txt
python -m ruff check .
python -m pytest -q tests/test_qa_parallel_e2e_bundle.py
python -m pytest -q --junitxml=validation-logs/pytest.xml
python -m pytest tests/qa -q
python -m ruff check qa tests/qa
python -m qa.inventory --root . --out validation-logs/inventory
python scripts/qa_final_file_integrity_check.py
python scripts/qa_semantic_pdf_audit.py
```
이미 CI에서 이 명령들이 각각 실행됐다. 보고서-only 커밋 뒤 HEAD CI를 별도 확인해야 한다.
