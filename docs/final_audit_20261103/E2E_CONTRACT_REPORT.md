# E2E 계약 검증과 실측 증거

감사일: 2026-11-03T13:53:16.870235+09:00

감사 대상 코드 HEAD: `b78c8c0e8dff5480c850bce8868de40ed71f49c8` / Git Tree: `5e378f4bb3c3f40c67e81a7bbe5d8686cf3ab450`.
안전 기준선: `9684b8d9f2098191ca2b1bc3f1c5645321fc6ed5`. [추가 변경 Draft PR #2](https://github.com/dohun3540-crypto/integration_finished_workforlast/pull/2).
이 보고서와 증거 파일을 추가한 후의 최종 HEAD/CI는 PR #2 본문에 별도로 기록합니다.
보고서가 자기 자신의 커밋 SHA를 포함할 수 없으므로 코드 검증 SHA와 문서 패키징 SHA를 구분합니다.


| 경계 | 실제 확인한 범위 | 결과 |
|---|---|---|
| 보관 C001 3문서 → V6 → 독립 QA | 실제 10/30 Native 원본의 Job/Step/source 파일 3개 및 계산 | PASS_LOCAL |
| C001 계산 | 기존 부족 0 / 변경 부족 60 / 대체 60 / 비용 60,500 | PASS_LOCAL |
| C008 부분 입고 | R1 40/R2 60, R2만 변경, 부족40/비용40,500 | PASS_LOCAL, 합성 DRAFT |
| C013 PO 충돌 | PO1/PO999의 receipt 결합 차단 | PASS_LOCAL, 합성 적대적 입력 |
| C017 한국어 날짜 | 원본 년월일 → ISO 필드 대조, 잘못된 날짜 거절 | PASS_LOCAL; 신규 cloud Normalize 실행 없음 |
| Stage | Extract branches·Merge·Normalize·QA Input/Report SHA/Job/Step/Config 및 중복 ID/역할 교환 회귀 | PASS_LOCAL, 계약/합성 자료 |
| QA·Cross-Agent | 별도 QA Job 허용, 다른 Case/Native SHA·receipt·provenance 혼합 거절 | PASS_LOCAL, 계약/합성 자료 |
| repository/SHA | 빌더·combined·단독 validator·gate CLI의 실제 target repository 전달 | PASS_LOCAL, 신규 회귀 |
| B0/E1 | 동일 PDF 바이트·동일 Case·별도 Config/Job, 필드 diff와 Gold 성능 분리 | PASS_LOCAL, 계약/합성 자료 |
| 신규 Studio B0/E1·QA | 인증된 신규 raw Stage/QA/receipt 미제공 | NOT_VERIFIED |
| 공식 정확도/개선률 | 승인 Gold와 비교 실행 없음 | NOT_MEASURED |

Stage/클라우드 관련 통과는 원본 파일을 사용한 보관 replay 또는 합성 변조 계약 테스트입니다. 현재 Studio 계정/최신 편집 워크플로우를 조회하거나 유료 실행하지 않았습니다. 10/30 보관 실행 존재와 이번 신규 Live 성공은 별개입니다.

## 실제 CLI

```bash
python -m qa.integration --help
python scripts/team1_e2e_preflight.py --help
python scripts/qa_cross_agent_check.py --help
python scripts/qa_b0_e1_compare_check.py --help
python -m qa.integration \
  --native data/results/studio_runs/C001_20261030_v4/instruct_original.json \
  --trusted-base data/cases/SYN-C001/trusted_base_case.json \
  --candidate qa/gold_candidates/SYN-C001/candidate.v1.json \
  --case-id C001 --job-id job_gPmEYKzuJdBA6BmKhVnujs \
  --github-sha b78c8c0e8dff5480c850bce8868de40ed71f49c8 \
  --github-repository dohun3540-crypto/integration_finished_workforlast
```

Offline 명령은 exit 2와 전체 BLOCKED가 정상입니다. `combined.python_safety_status=PASS_LOCAL`, `release_or_merge_authorized=false`를 확인해야 합니다. SHA 일치만으로 실측 성공을 선언하지 않습니다.

## 다음 외부 증거

1. 같은 PDF 3개의 원본 바이트·SHA·실제 File ID와 Case당 단일 operational Job.
2. 저장된 Agent/Config ID/Version과 Extract 각 branch·Merge·Normalize 원본 다운로드/Job/Step.
3. 별도 QA Job의 Native와 IndependentQA Input/Report, 실제 운영 Native SHA를 연결하는 sidecar와 PDF receipts.
4. 실제 PDF를 독립 검수한 최신 XLSX/필드 Evidence Matrix, 검수자·시간·승인된 Gold 버전/SHA. 승인 값을 AI가 작성하지 않습니다.
5. 같은 PDF 바이트를 사용한 B0/E1 원본 두 세트와 실행 조건. 승인 Gold가 연결된 후에만 실측 정확도와 개선률을 산출합니다.
