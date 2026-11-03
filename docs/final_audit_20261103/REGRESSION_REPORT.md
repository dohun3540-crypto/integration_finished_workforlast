# 회귀 검증 결과

감사일: 2026-11-03T13:53:16.870235+09:00

감사 대상 코드 HEAD: `b78c8c0e8dff5480c850bce8868de40ed71f49c8` / Git Tree: `5e378f4bb3c3f40c67e81a7bbe5d8686cf3ab450`.
안전 기준선: `9684b8d9f2098191ca2b1bc3f1c5645321fc6ed5`. [추가 변경 Draft PR #2](https://github.com/dohun3540-crypto/integration_finished_workforlast/pull/2).
이 보고서와 증거 파일을 추가한 후의 최종 HEAD/CI는 PR #2 본문에 별도로 기록합니다.
보고서가 자기 자신의 커밋 SHA를 포함할 수 없으므로 코드 검증 SHA와 문서 패키징 SHA를 구분합니다.


| 검사 | 실제 결과 | 증거 |
|---|---|---|
| 수정 전 기준선 | 815 PASS, 실패/skip 0 | baseline-pytest.txt/xml |
| 숫자 결함 최소 재현, 수정 전 | 5 FAIL | numeric-before.txt |
| 숫자 수정 관련 회귀 | 182 PASS | numeric-after.txt |
| 저장소 바인딩 재현, 수정 전 | 2 FAIL | repository-binding-before.txt |
| 저장소 바인딩 수정 관련 회귀 | 91 PASS | repository-binding-after.txt |
| Team1 E2E preflight | 37 PASS, 전체에 포함 | team1-regression.txt |
| 최종 로컬 전체 pytest | 828 PASS, 실패/skip 0 | final-pytest.txt/xml |
| Ruff | PASS | ruff.txt |
| requirements-validation 설치 / pip check | PASS | dependencies-install.txt / pip-check.txt |
| 주요 모듈 import | PASS | module-imports.json |
| PDF 60 / 텍스트 대조 60 / tracked 파일 감사 | PASS, 기계 범위 | inventory / semantic-pdf / final-file-audit |
| Archived C001 + Local Gate | PASS_LOCAL; Release BLOCKED | archive.json / gate.json |
| 통합 Offline CLI | exit 2 예상대로; V6 PASS_LOCAL, 최종 BLOCKED | offline-c001.json |

Junit testcase 식별자 집합을 비교해 기존 815개가 최종 828개에 모두 포함됨을 확인했습니다. 기존 테스트 파일은 전부 같은 Git Blob이며 assertion 수정·삭제·skip 추가가 없습니다. 추가 13개는 숫자 결함, PDF 라벨 비교와 한국어 날짜/null 구분, repository/SHA API·CLI 연결을 보호합니다. 기존 테스트를 의미 없이 복제하지 않았습니다.

로컬 Python은 3.12.14입니다. GitHub CI의 3.11 검증은 별도 SHA/Run 증거로 기록합니다. `command-results.json`의 초기 명령은 코드 checkpoint를 명시하며, 최신 replay는 `offline-c001.json`과 최종 CI를 기준으로 확인합니다.

재현 명령:

```bash
python -m pip install -r requirements-validation.txt
python -m ruff check .
python -m pytest -q tests/test_qa_parallel_e2e_bundle.py
python -m pytest -q
python scripts/qa_semantic_pdf_audit.py
python scripts/qa_final_file_integrity_check.py
```

코드 HEAD `b78c8c0e8dff5480c850bce8868de40ed71f49c8`의 GitHub CI #41580379496은 SUCCESS이며 Python3.11 전체828 PASS/Ruff PASS를 확인했습니다. Merge checkout `a23d0ab1910c95a51cb7734faa50660b2cb61ab2`의 tree가 코드 tree와 정확히 같습니다. GitHub CI 실행/테스트 checkout tree는 `CI_RESULT.json`과 PR #2의 최종 SHA 증거를 참고하세요. 과거 다른 HEAD의 성공을 새 HEAD의 검증으로 재사용하지 않습니다.
