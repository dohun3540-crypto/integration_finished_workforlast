# 팀원 3 김민주 → 팀원 1 구도훈: 코드 동결 후 최종 인계

## 인계 판정
- `TEAM3_CODE_FREEZE`: **APPROVED** — 코드 SHA `bbd2c1ea359fa2a3655a9cf099129a1cb0284316`에서 재검증 PASS. 추가 코드 개발 중단.
- `TEAM3_HANDOFF_READY`: **READY_WITH_EXTERNAL_DEPENDENCIES**.
- `TEAM3_SUBMISSION_DATA_READY`: **BLOCKED**. 실제 Gold·Studio 증거가 들어오지 않았다.

## 지금 사용할 수 있는 고정 경로
- 원본 PDF 메타데이터/압축 읽기: `qa/inventory.py`, 실제 `data/cases/SYN-C001/` 및 `data/cases/SYN-C002-C020_DRAFT_PDFs.tar.xz`.
- C001: `qa/gold_candidates/SYN-C001/candidate.v1.json`, `PDF_EVIDENCE_MATRIX.csv`, `REVIEW_GUIDE.md`.
- C008·C013·C017 후보: `qa/gold_candidates/SYN-C008/candidate.machine.v1.json`, `...SYN-C013/...`, `...SYN-C017/...`.
- 사람이 수집한 XLSX vs CSV 자료형·정확성 비교: `qa/review_bridge.py` (`inspect_xlsx_review`) 및 `qa/xlsx_snapshot.py`.
- 실제 추출·분류·Evidence 평가: `qa/gold_metrics.py` (`evaluate(prediction, approved_gold, native_bindings)`) ; 명시적 원문 근거와 Native 파일 SHA 연결 필요.
- 인터페이스 설명: `docs/team3_quality_20261103/EVALUATION_METRICS_REPORT.md`, `TEAM3_TO_TEAM1_HANDOFF.md`, `TEAM3_FINAL_REGRESSION.md`, `TEAM3_FINAL_FREEZE_DECISION.json`.
- 자동화: `.github/workflows/member3-data-check.yml` 및 기존 `.github/workflows/ci.yml`.

## 인계 후 실제 사용 명령
다음 입력 경로는 **미래 제공이 필요한 예시이며 존재한다고 주장하지 않는다**. `qa.inventory` 출력 디렉터리는 반드시 새 경로여야 한다.
```bash
python -m qa.inventory --root . --out /tmp/team3-final-inventory-unique
python -m qa.review_bridge \
  --xlsx review/latest/PDF_EVIDENCE_MATRIX.xlsx \
  --csv qa/gold_candidates/SYN-C001/PDF_EVIDENCE_MATRIX.csv \
  --out /tmp/team3-xlsx-review-report.json
python -m qa.gold_metrics \
  --gold review/approved/SYN-C001.gold.frozen.json \
  --prediction review/native/latest-studio-result.json \
  --binding review/native/studio-source-bindings.json \
  --out /tmp/team3-official-evaluation.json
```
각 CLI는 PASS 0, BLOCKED/FAIL 2로 종료할 수 있다. `review_bridge`의 PASS는 형식·기준 일치만 의미하고 **Human Gold 자동 승격은 절대 수행하지 않는다**.

## 입력 데이터 계약 — 필요한 실제 필드
**팀원3 김민주 + 지정된 실제 검수자:**
- 최신 편집된 `PDF_EVIDENCE_MATRIX.xlsx` **원본 바이트**, 단일 원본 SHA256, 시트명/셀 좌표/타입, C001 검수 항목별 원문 시각 확인, 결측/부재 명시, reviewer + timezone-aware reviewed_at, decision + approval_state, 수정/반려 및 별도 승인 기록.
- 승인 Gold의 `label_status=HUMAN_GOLD_FROZEN`, `human_reviewed=true`, `team_approved=true`, `gold_frozen=true`, `eligible_for_official_metrics=true`, `gold_sha256`과 `approval_provenance` (`reviewer`, `reviewed_at`, `approval_record_sha256`). **메타데이터 자체로 사람 신원 인증되지 않으므로 외부 승인 절차 필요**.
- `approved_field_evidence[]` 각각 `document_id`, `field_path`, 원본 `source_file_sha256`, 실제 `page`, `decision=ACCEPT`, `review_record_sha256`, `source_original_text`(non-null) 또는 `absence_confirmed=true`(null). 독립 검수된 모든 필드 leaf를 유일하게 포함.

**팀원1 구도훈 / Upstage Studio 담당:**
- 해당 케이스의 최신 *실제* Studio Native 결과 JSON (DRAFT/Archive Replay 아님), 응답의 document_id, 문서별 추출 값과 원문 Evidence, `po_conflict_detected`, `business_status`.
- `studio-source-bindings.json`: `case_id`, `execution_kind=STUDIO_NATIVE`, `job_id`, `config_id`, `workflow_version`, 각 문서의 `file_bindings[]`: `document_id`, `file_id`, `filename`, `sha256`. 발주/통보/견적이 한 케이스라는 것을 Studio 실제 Job 메타데이터로 따로 검증해야 한다.
- 케이스 표기 `C001`과 `SYN-C001`은 한정된 alias로 인식하지만 서로 다른 케이스 번호·SHA·Job은 절대 혼합 금지.

**팀원2 윤현준:** Python Safety V6 로컬 통과 기록과 Live 통합 상태를 **기존 코드 범위**에서 별도 확인. 팀원3 코드 동결을 위해 수정 요청할 항목은 없음.

## 종료 이후 절차
1. 김민주 코드 개발은 여기서 종료하고 PR #3은 Draft 유지. 팀원 1은 코드 SHA와 전체 CI를 확인해 인수한다.
2. 실제 검수 XLSX 확보→검수자의 원문 확인과 승인→별도 Frozen Gold/근거 해시 생성(기존 DRAFT 불변).
3. Studio 최신 단일 케이스 결과와 인증 가능한 Job/Config/File SHA 인계→`qa.gold_metrics`로 공식 분자/분모·누락·Evidence·PO 충돌 차단 검증.
4. 독립 QA + Safety V6와 Live Release Gate를 다시 확인하기 전 제출 데이터 READY/PR Merge 승격 금지.

## 외부 자료 및 보존 상태
저장소 Git Tree(461항목, truncated=false)와 접근 가능한 대화/라이브러리 파일 검색 결과 최신 C001 `PDF_EVIDENCE_MATRIX.xlsx` 원본, 실제 승인 Gold/Native 단일 Job 예측 바인딩은 확인되지 않음. Legacy Native 설정 및 이미지가 존재하는 것은 **최신 실제 실측/승인 Gold를 제공한다는 뜻이 아님**.
코드 검증 CI: 통합 [#41604457812](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41604457812), 팀3 [#41604457818](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41604457818).
