# 파일 무결성 및 원본 보존

감사일: 2026-11-03T13:53:16.870235+09:00

감사 대상 코드 HEAD: `b78c8c0e8dff5480c850bce8868de40ed71f49c8` / Git Tree: `5e378f4bb3c3f40c67e81a7bbe5d8686cf3ab450`.
안전 기준선: `9684b8d9f2098191ca2b1bc3f1c5645321fc6ed5`. [추가 변경 Draft PR #2](https://github.com/dohun3540-crypto/integration_finished_workforlast/pull/2).
이 보고서와 증거 파일을 추가한 후의 최종 HEAD/CI는 PR #2 본문에 별도로 기록합니다.
보고서가 자기 자신의 커밋 SHA를 포함할 수 없으므로 코드 검증 SHA와 문서 패키징 SHA를 구분합니다.


비공개 저장소의 일반 HTTPS Clone은 로컬 인증 부재로 실패했습니다. 연결된 GitHub API에서 정확한 기준선의 346개 파일을 받고 모든 Git Blob을 검증했습니다. 원래 commit `9684b8d9f2098191ca2b1bc3f1c5645321fc6ed5`와 tree `e3abd39a58667f2ed6df8accefe575d9a509b0ae`를 해시가 일치하도록 로컬 Git에 복원했습니다. 최종 클라우드 checkout은 CI 증거로 별도 확인합니다.

- 기준선 346개 중 335개는 byte-identical입니다. 의도적으로 수정한 기존 파일 11개는 아래와 같습니다.
- PDF 60/60, Case Manifest 20/20, Native/Config/Gold, 기존 모든 테스트 파일은 보존했습니다.
- 57 PDF의 XZ-TAR SHA-256: `a3f4ed1cefee4ebea3a4b94f9408f8a039bf042bd651a3a9222a5162c22149dc`.
- C001 Native SHA-256: `88387f8d6aee1421c9f628304c6b91811396b32da297d41b40e3d53c3d98dfea`.
- 중복 PDF SHA 0, 파싱 FAIL/BLOCKED 0. 아카이브는 허용 상대 경로·링크·중복·크기 제한을 적용해 메모리에서 읽었습니다.
- 기존 보호 Blob 7/7이 일치합니다. 전체 목록과 모든 346개 전후 SHA는 [baseline-blob-comparison.json](evidence/baseline-blob-comparison.json), 실제 감사 출력은 [final-file-audit.json](evidence/final-file-audit.json)입니다.
- Main `67b93291c1f32acaf43e45815d2d1119480b652a`과 PR #1 브랜치는 쓰기 대상이 아닙니다. 새 브랜치/PR #2에만 체크포인트를 저장했습니다.

| 수정한 기존 파일 | 변경 전 Git Blob | 변경 후 Git Blob |
|---|---|---|
| `.github/workflows/ci.yml` | `ffbfb20de3753debcea7c6725c04368b9f0f9819` | `4563348b3d65b9b73a556fc1924d4eef511eb0e6` |
| `qa/integration.py` | `dc3aba5f4e81f6ea87c15428de20434104fc1bb4` | `b3ff72c6bee3a79e928f3bd91683b2ef794d857d` |
| `scripts/qa_combined_e2e_check.py` | `32326b0c436573f3c6d12d2c7917bfe3d17a024b` | `c36f670453182e26d09a63f4ab07debde2477404` |
| `scripts/qa_cross_agent_check.py` | `1199898f94e6ac9791ebfaf65991c13a2c3c76aa` | `7f215b77485db6b31aed9c362cbc7e337c1880bd` |
| `scripts/qa_gate_check.py` | `b7e0915b6f97e348b9556486cbc3ffdb7b4ceada` | `68f2147ab82ec6b65e45bb8926994283c3d06aae` |
| `scripts/qa_prepare_studio_raw_handoff.py` | `6a7cf278ccaac3b1a00634e63dc445baf9d289bd` | `610f008db4b6045a6922e741f7b78074806afe5a` |
| `src/leadtime_guardian/engine.py` | `bc0ecdc3df55c0ad95dc8195f1631579aa95d866` | `352ab6b166196cd24449f8271c77adc2acb6fd8a` |
| `src/leadtime_guardian/qa/cross_agent.py` | `731ae46c96a16604ed3953213c7b90ebdc9a53cd` | `c16efdda4a5a1c62dae7c6c29cd6c92e87422416` |
| `src/leadtime_guardian/qa/gate.py` | `0e63c8bd995bd4315f43eb78d4f98bff0931434f` | `6544c8a66623510931682f9dab5c572b3c8ee810` |
| `src/leadtime_guardian/qa/handoff_builder.py` | `0be4aa4ccf44db43079d3860c7f79c76601cec40` | `d5274644abc49517c9bc2e0c3479d214f7795a6d` |
| `src/leadtime_guardian/qa/portfolio.py` | `358ddf58696afb415c08269c967ccde9b16ace27` | `28fc07af57a0e590c3d96ef2b4154c516008c75a` |

변경 이유: engine/portfolio는 비용 예외·반올림 보호, Cross-Agent/hand-off/CLI는 repository/SHA 스코프 연결, CI는 semantic PDF 검사 한 단계 추가입니다. 기존 CI 단계와 테스트는 유지했습니다. 추가한 파일은 semantic 검사 스크립트 1개, 회귀 파일 3개, 이 보고서 및 실제 로그입니다.

기계 SHA 일치와 사람의 의미·시각 검수는 구분합니다. 파일이 존재하지 않는 최신 검수 XLSX, 새 QA Native, B0/E1를 생성해 실측 증거로 저장하지 않았습니다.
