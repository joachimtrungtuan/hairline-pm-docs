# Web E2E Manual Operations Runbook

**Status:** MVP setup complete; six-case Provider login suite active; Team directory and invitation-management suite draft
**Runtime:** Existing global `@playwright/mcp` package plus installed system Chrome
**Package manager:** pnpm only

This is the manual runbook for executing registered Hairline web E2E cases and reviewing their results without AI assistance. Run every command below from `local-docs/testing-automation/`.

## 1. Prerequisites and Boundaries

- Use Node.js 22 or later and pnpm. The project declares pnpm `11.11.0`.
- Use the existing global `@playwright/mcp` runtime and installed system Chrome.
- Do not install Playwright, its browsers, or another browser from this project.
- Confirm the development dashboard and backend are reachable.
- The runner resolves registered V1, P1, and S1 accounts from `local-docs/testing-plans/testing-credentials/` by default. Environment variables may select another registered account or override runtime credentials.
- Never place credentials in commands, source files, results, review notes, or a committed environment file. See `.env.example` for optional variable names and export values only in the shell when needed.
- Do not read from, import from, write to, or otherwise depend on `main/`.
- Use live PRDs as requirement authority and the development UI/API as implementation evidence.
- Retain generated development records.
- Maildrop inboxes are public. Draft invitation-mutation cases stop before sending unless a human has accepted that the generated invitation link can be publicly readable and explicitly exports `HAIRLINE_ALLOW_PUBLIC_INVITE_MAILBOX=true`. Prefer a private controlled test mailbox when available.

## 2. Registry Statuses

- `status-taxonomy.json` is the centralized source for every registry status, outcome, review status, human classification, attempt/dataset status, artifact type, and CLI-visible scope enum.
- `ACTIVE` means the case has activation approval and can run normally.
- `DRAFT` means the case is registered but not activated. Normal execution rejects it.
- Other governed registry statuses remain non-active unless the taxonomy and Constitution explicitly say otherwise.
- Use `--allow-draft` only for an explicitly approved controlled validation. The flag does not activate, approve, or change the registry entry.

## 3. Start the Interactive Test Console

From `local-docs/testing-automation/`, start the centralized deterministic console:

```bash
./test.sh
```

The console reads the machine-readable registry and lets you:

- browse registered modules, then functions or flows;
- run every active case in one selected function or flow;
- run one active case for diagnosis;
- run all active registered tests;
- choose visible or headless Chrome;
- inspect the pending human-review queue;
- view the latest SQLite run summary;
- run preflight independently.

The normal menu never offers `DRAFT` cases or `--allow-draft`. Before browser execution it shows the selected scope, active-case count, governed coverage-gap count, browser mode, and confirmation prompt. It runs preflight automatically and then delegates to the existing pnpm runner. No AI agent participates.

Direct pnpm commands remain supported for troubleshooting, controlled draft validation, and external automation.

## 4. Run a Registered Function Suite Directly

1. Open Terminal.

2. Change to the testing automation directory:

   ```bash
   cd "/Users/joachimtrungtuan/My Documents/Vân Tay Media/Products/Hairline/local-docs/testing-automation"
   ```

3. Run preflight before browser execution:

   ```bash
   pnpm test:preflight
   ```

   Continue only after Terminal reports `Preflight passed` and identifies the dashboard, Playwright package, and browser. Fix any reported runtime or connectivity problem without installing Playwright or browsers.

4. Locate registered module, function, and case IDs and confirm each status:

   ```bash
   rg -n -m 50 'Registry status|Function ID|TC-[0-9]+' registry/*/*/module.md registry/*/*/functions/*/test-cases.md
   ```

   Start with `registry/README.md`, then read the matching module's `module.md` and function's `test-cases.md`. Do not assume a case is `ACTIVE` from its presence in the registry.

5. Run every `ACTIVE` case registered for a function in the default visible browser:

   ```bash
   pnpm test:function <module-id> <function-id>
   ```

   The active Provider login suite command is:

   ```bash
   pnpm test:function PR-01 PR-01-FN-001
   ```

   This runs all six active login cases. Use `--case <case-id>` only for diagnosis, targeted re-verification, or an explicitly selected review item. Use `--allow-draft` only for a separately approved controlled validation of draft coverage; the flag never activates a case.

   The first Team function is registered as `PR-01-FN-002` but remains absent from the interactive console while its cases are `DRAFT`. An explicitly approved controlled validation can run all eighteen cases with:

   ```bash
   pnpm test:function PR-01 PR-01-FN-002 --allow-draft
   ```

   The Maildrop mutation cases additionally require the explicit safety acknowledgement described in Section 1. Without it, they produce a reviewable `BLOCKED` result before browser execution.

6. Optionally run headless by setting the runtime variable for the same command:

   ```bash
   HAIRLINE_HEADLESS=true pnpm test:function <module-id> <function-id>
   ```

## 5. Read and Inspect Results

1. Read the Terminal output. For each case, the runner prints the case ID, automated outcome, and review status. It then prints the run ID, outcome counts, pending-review count, and SQLite result path.

2. Treat a non-success shell result as a signal to inspect the outcome, not as confirmation of a product bug. The runner returns non-success when human review is required; preflight, configuration, selection, and usage failures can also stop execution. Do not infer a confirmed bug from the shell result alone.

3. Inspect the human-review queue:

   ```bash
   pnpm test:review-queue
   ```

   The queue shows the `executionId`, case ID, automated outcome, review status, and start time. Keep the `executionId` for the review command.

4. Locate persistent evidence relative to this directory:

   - Canonical SQLite data: `results/test-results.sqlite`
   - Retained screenshots and traces: `results/artifacts/<run-id>/<module>/<case-id>/`

   Artifact folders exist only when the constitutional retention rules keep evidence; a clean initial pass intentionally retains no screenshot or trace. New runs, attempts, dataset setup actions, review events, artifacts, taxonomy synchronizations, and migrations retain UTC timestamps. Legacy fields that predate timestamp capture remain `NULL` rather than receiving invented times.

5. After a human has inspected the terminal result, queue entry, and retained evidence, record the decision:

   ```bash
   pnpm test:review <execution-id> --classification <human-decision> --reviewer <name-or-role> --notes "<text>"
   ```

   The classification must be active under `humanClassification` in `status-taxonomy.json`; both the CLI and SQLite reject unknown values. `POSSIBLE_UI_DISCREPANCY` is the governed classification for functioning UI whose visible contract may differ from an approved requirement. Append `--retest-required` when the human decision requires another run. The command records the decision and changes the queue status to `REVIEWED`; it never changes the original automated outcome. Do not put credentials or personal data in review notes.

6. After an approved product fix or approved test revision, run preflight and repeat the function command. Use a case selector first only when the human review scope is deliberately limited; finish with the complete affected function suite when the fix could affect sibling cases.

## 6. Screenshot, Retry, and Human-Review Rules

- `PASSED`: the initial attempt passed; no screenshot or trace is retained.
- `FLAKY_OR_TRANSIENT`: a retry passed; the latest failed and passing screenshots are retained; human review is required.
- `POTENTIAL_ISSUE`: four equivalent failures occurred at least five seconds apart; only the rolling final screenshot is retained; human review is required.
- `INCONSISTENT_FAILURE`: four failures produced different signatures; the final screenshot is retained; human review is required.
- `BLOCKED`: preflight or API dataset preparation prevented browser execution; no UI screenshot is fabricated; human review is required.

Every non-pass enters `NEEDS_HUMAN_REVIEW`. Neither the runner nor AI confirms a bug. One initial attempt plus up to three retries is allowed, with at least five seconds between failures.

## 7. Registration and Frontend Changes

Registration begins with a narrow scout of the live PRD's module scope and overall workflows, followed by Product Owner correction and approval of the function boundary and canonical happy path. Testing Constitution v1.3 then delegates derivation of the remaining unambiguous PRD cases without case-by-case approval. The registration must map every applicable requirement to an executable case or a governed gap and record why each standard category is covered, not applicable, or blocked.

A UI discrepancy never causes automatic test rewriting. Route the execution to human review. After a human confirms an intentional frontend change, update the approved selectors/actions and case revision through the registration workflow, then re-run the affected tests.
