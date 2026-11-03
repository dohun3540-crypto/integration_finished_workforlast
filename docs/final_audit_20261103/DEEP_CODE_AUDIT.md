# 정밀 코드 감사

감사일: 2026-11-03T13:53:16.870235+09:00

감사 대상 코드 HEAD: `b78c8c0e8dff5480c850bce8868de40ed71f49c8` / Git Tree: `5e378f4bb3c3f40c67e81a7bbe5d8686cf3ab450`.
안전 기준선: `9684b8d9f2098191ca2b1bc3f1c5645321fc6ed5`. [추가 변경 Draft PR #2](https://github.com/dohun3540-crypto/integration_finished_workforlast/pull/2).
이 보고서와 증거 파일을 추가한 후의 최종 HEAD/CI는 PR #2 본문에 별도로 기록합니다.
보고서가 자기 자신의 커밋 SHA를 포함할 수 없으므로 코드 검증 SHA와 문서 패키징 SHA를 구분합니다.


## 결과와 실제 수정

| ID | 심각도 | 재현된 이전 동작 | 수정 후 동작 | 근거 |
|---|---|---|---|---|
| NUM-1 | P0, 비용 QA false PASS | 단가 `0.12345678901234567890123456789` × 60 + 운송비 500이 28자리에서 반올림되어 `507.4074073407407407340740741`; 운영 결과와 QA가 함께 정상 판정 | 정확히 표현할 수 없는 비용은 엔진 BLOCKED, QA FAIL | `numeric-before.txt`, `test_final_numeric_safety.py` |
| NUM-2 | P1, 안전 응답 누락 | 단가 `1e999999`의 계산에서 Decimal Overflow로 엔진/QA 예외 종료 | 엔진은 빈 추천·null 비용·검토 사유를 반환; QA는 UNVERIFIABLE_COST_ARITHMETIC | 같은 회귀 파일 |
| NUM-3 | P1, 실행 환경 의존 | 호출자의 Decimal precision=4일 때 정상 소수 단가 비용도 `6.050E+4`로 변형 | 격리된 28 유효숫자 Context에서 `60500.60`, 호출자 Context 보존 | 동일 파일의 Context 회귀 |
| PROV-1 | P1, 저장소/SHA 오표기 | 인계 빌더가 호출자 SHA에 과거 `.copy` 저장소 이름을 강제로 붙임; 실제 통합 저장소를 지정할 인터페이스가 없음 | repository+SHA 명시 전달 및 기대 저장소와 독립 비교, 불일치 FAIL | `repository-binding-before.txt`, `test_final_repository_binding.py` |

금액은 원래 사용하던 28 유효숫자 범위를 명시적으로 고정했습니다. 무손실 연산만 정상 결과로 반환합니다. 높은 정밀도의 비용이 필요하면 별도 금융 정책과 QA 정답을 정의해야 하며, 이번에는 임의 반올림 정책을 추가하지 않았습니다. 원본 PDF·Config·Gold와 기존 테스트는 수정하지 않았습니다.

## 실제 연결 관계와 계약

| 단계 | 구현/입력 → 출력 | 누락·타입·실패 처리와 검증 한계 |
|---|---|---|
| PDF → Parse | Native v4 Config의 standard/force OCR/coordinates → 파싱 자료 | 원본 3+57 PDF는 보존. 이번 클라우드 Parse 실행 없음 |
| Classify → Extract | Config의 purchase_order/delivery_notice/quotation/other → 역할별 추출 | 실제 신규 분류 정확도 미측정. `pipeline_config_audit`, `extract_null_contract`는 정적·합성 검증 |
| Merge → Normalize | `metadata.source_files`, `merge.items`, Native `content` 문자열 → documents 배열 | `documents_from_export`가 외부/내부 Strict JSON, 단일 envelope, Job 상태/ID 확인. `studio_contract`는 메타데이터 내부 정합성 검사이며 공급자 인증 아님 |
| Adapter | `validate_documents` → `apply_studio_extractions` | schema+FormatChecker, PO/product/receipt·수량·EA/KRW·중복 통보·견적 배열 검증. null/빈 배열/0/Boolean을 별도 처리 |
| Python V6 | `analyze_studio_documents` → `analyze_portfolio` | 원본 deepcopy, baseline/revised 두 차례 allocate, 공유 견적 capacity·견적당 운송비 1회. 계산 불가 시 BLOCKED |
| Independent QA | `audit_portfolio` + 독립 `reference_allocations` | 수량 보존·기한별 배분·비용·추천 상한·출처 ID 검사. 운영 엔진을 정답 oracle로 호출하지 않음. 불확실 PDF 근거를 인증하지 않음 |
| Cross-Agent | `build_studio_raw_handoff` → `audit_cross_agent_handoff` | SHA·Agent/Config/Version·QA Job·보고서·repository/SHA 기대값 연결. QA Job과 운영 Job은 달라도 허용하되 각자의 바인딩 필요 |
| 통합 | `audit_combined_bytes` → `qa.integration.audit_integration` | 실제 V6와 QA를 호출. 선택적 QA Native/Report/PDF receipt/sidecar 누락 시 BLOCKED 유지 |
| B0/E1 | `audit_b0_e1_readiness`, `compare_normalized_field_values` | 별도 CLI/증거 bundle 경로. 동일 Case/PDF 바이트와 별도 Job 요구. 필드 변화는 개선률이나 Gold 정확도로 승격되지 않음 |
| Release | `audit_parallel_e2e_bundle`, `audit_release_folder`, `build_integration_gate` | 로컬 파일·Stage·receipt를 연결. 외부 인증·Human Gold 없으면 Release 불가. CI 성공이 Release 성공을 의미하지 않음 |

`qa.integration`은 모든 클라우드 단계를 실행하는 오케스트레이터가 아니라 읽기 전용 로컬 통합 CLI입니다. B0/E1 및 Stage intake는 별도 CLI 또는 preflight bundle로 명시 연결해야 합니다. 원래 `analysis.analyze_case`는 간단한 MVP 데모이며 Safety V6의 공식 통합 경로가 아닙니다.

## 남은 제한과 유지한 정책

- P2 운영 혼동 가능성: `configs/studio_workflow.import.json`의 exportedFrom은 Config v3, `configs/studio_native/config_v4.export.json`은 v4입니다. 파일 이름만 보고 최신으로 판단하지 말고 실제 Config ID/Version을 확인해야 합니다. 원본 Config는 보존했습니다.
- `gate.REQUIRED_EXTERNAL_GATES`는 보수적인 정적 차단 사유를 유지합니다. 일부 과거 명칭을 현재 코드 부재의 증거로 해석하면 안 됩니다. 최신 코드 상태는 이 보고서와 SHA로 판정합니다.
- 기존 public helper/독립 CLI는 호환성을 위해 `.copy` 기본값을 보존합니다. 현재 저장소 인계에는 `--github-repository` 또는 `--expected-github-repository`를 명시합니다. `python -m qa.integration` 기본값은 현재 통합 저장소입니다.
- 저장소/SHA 바인딩은 로컬 계약입니다. 해당 SHA가 외부 저장소에 실제 존재하거나 provider 실행과 연결됐다는 인증을 새로 주장하지 않습니다.
- 신규 Live와 사람 Gold는 입력 자체가 없어 검증하지 않았습니다. 미해결 P0/P1을 안전한 Release PASS로 처리한 경로는 없습니다.
