# Testing Results

Dated outputs of the Android testing skills (`android-emulator-qa`, `android-flow-test`, `android-flow-register`) are written to `results/YYYY-MM-DD/`, one folder per run date (reports, plus any session screenshots the skill keeps).

The API testing skills (`api-testing`, `api-flow-testing`) write no result files: they report in the conversation, and confirmed learnings go to the endpoint and flow profiles under `automated/api/`.

Results that live elsewhere:

| Output | Location |
|---|---|
| Web E2E results (SQLite and artifacts) | `automated/web-e2e/results/` |
| Manual test results | In the manual batch files under `manual/phases/` |
| Manual evidence files | Team cloud storage; links in the batch Evidence column (see `../TEST-STRATEGY.md` §5) |
| Pre-2026-10-19 reports | `archive/reports/` |

See [../TEST-STRATEGY.md](../TEST-STRATEGY.md) §9.
