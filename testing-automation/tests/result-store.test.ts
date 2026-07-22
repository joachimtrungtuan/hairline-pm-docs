import assert from "node:assert/strict";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import test from "node:test";

import { resultEnvelopeFixture as envelope } from "./fixtures.ts";
import {
  createResultStore,
  formatRunSummary,
} from "../framework/src/result-store.ts";

test("writes an execution atomically and creates a human-review queue item", async () => {
  const directory = await mkdtemp(join(tmpdir(), "hairline-results-"));
  try {
    const store = createResultStore(join(directory, "results.sqlite"));
    const first = store.writeEnvelope(envelope);
    const second = store.writeEnvelope(envelope);

    assert.equal(first.status, "written");
    assert.equal(second.status, "duplicate");
    assert.equal(store.countExecutions(), 1);

    const queue = store.listReviewQueue();
    assert.equal(queue.length, 1);
    assert.equal(queue[0].caseId, "P-99-TC-0001");
    assert.equal(queue[0].reviewStatus, "NEEDS_HUMAN_REVIEW");
    store.close();
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test("formats a terminal summary with pending human reviews", async () => {
  const directory = await mkdtemp(join(tmpdir(), "hairline-summary-"));
  try {
    const store = createResultStore(join(directory, "results.sqlite"));
    store.writeEnvelope(envelope);
    const summary = formatRunSummary(store.getRunSummary(envelope.run.id));

    assert.match(summary, /RUN-20260712T010203Z-a1b2c3d4/);
    assert.match(summary, /Potential issues: 1/);
    assert.match(summary, /Pending human review: 1/);
    store.close();
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test("returns the latest persisted run summary", async () => {
  const directory = await mkdtemp(join(tmpdir(), "hairline-latest-summary-"));
  try {
    const store = createResultStore(join(directory, "results.sqlite"));
    store.writeEnvelope(envelope);
    const laterEnvelope = {
      ...envelope,
      run: {
        ...envelope.run,
        id: "RUN-20260712T020304Z-b2c3d4e5",
        startedAt: "2026-07-12T02:03:04.000Z",
        finishedAt: "2026-07-12T02:03:05.000Z",
        durationMs: 1000,
      },
      execution: {
        ...envelope.execution,
        id: "019f1234-1111-7111-8111-111111111111",
        outcome: "PASSED",
        reviewStatus: "REVIEW_NOT_REQUIRED",
        startedAt: "2026-07-12T02:03:04.000Z",
        finishedAt: "2026-07-12T02:03:05.000Z",
      },
      attempts: [{
        id: "019f1234-2222-7222-8222-222222222222",
        number: 1,
        status: "passed",
        startedAt: "2026-07-12T02:03:04.000Z",
        finishedAt: "2026-07-12T02:03:05.000Z",
        durationMs: 1000,
      }],
    };
    store.writeEnvelope(laterEnvelope);

    assert.deepEqual(store.getLatestRunSummary(), {
      runId: "RUN-20260712T020304Z-b2c3d4e5",
      passed: 1,
      flaky: 0,
      potentialIssues: 0,
      inconsistent: 0,
      blocked: 0,
      sourceReview: 0,
      unknown: 0,
      pendingReview: 0,
    });
    store.close();
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test("stores dataset and artifact metadata and accepts explicit human review", async () => {
  const directory = await mkdtemp(join(tmpdir(), "hairline-review-"));
  try {
    const store = createResultStore(join(directory, "results.sqlite"));
    const extended = {
      ...envelope,
      dataset: {
        id: "P-99-DS-0001",
        revision: "v1",
        setupStatus: "passed",
        correlationKey: "E2E-test",
        startedAt: "2026-07-12T01:02:03.000Z",
        finishedAt: "2026-07-12T01:02:04.000Z",
        durationMs: 1000,
      },
      artifacts: [{ attemptNumber: 1, type: "final-failure-screenshot", relativePath: "RUN/x/final-failure.png" }],
    };
    store.writeEnvelope(extended);
    assert.equal(store.countArtifacts(envelope.execution.id), 1);
    store.reviewExecution(envelope.execution.id, {
      classification: "INSUFFICIENT_EVIDENCE",
      reviewer: "Product Owner",
      notes: "Reference ID requires confirmation",
      retestRequired: true,
    });
    assert.equal(store.listReviewQueue().length, 0);
    store.close();
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test("stores action timestamps and enforces enum values in both runtime and SQLite", async () => {
  const directory = await mkdtemp(join(tmpdir(), "hairline-contracts-"));
  const databasePath = join(directory, "results.sqlite");
  try {
    const store = createResultStore(databasePath);
    store.writeEnvelope(envelope);
    assert.throws(() => store.reviewExecution(envelope.execution.id, {
      classification: "AD_HOC_STATUS",
      reviewer: "Product Owner",
      notes: "Must be rejected",
      retestRequired: false,
    }), /Invalid active humanClassification/);
    store.close();

    const database = new DatabaseSync(databasePath);
    const attempt = database.prepare(`
      SELECT started_at AS startedAt, finished_at AS finishedAt, duration_ms AS durationMs
      FROM attempts
      WHERE case_execution_id = ?
    `).get(envelope.execution.id) as { startedAt: string; finishedAt: string; durationMs: number };
    assert.equal(attempt.startedAt, envelope.attempts[0].startedAt);
    assert.equal(attempt.finishedAt, envelope.attempts[0].finishedAt);
    assert.equal(attempt.durationMs, envelope.attempts[0].durationMs);
    assert.throws(
      () => database.prepare("UPDATE case_executions SET review_status = 'AD_HOC_STATUS' WHERE id = ?").run(envelope.execution.id),
      /invalid reviewStatus value/,
    );
    database.close();
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});
