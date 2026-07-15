import { randomUUID } from "node:crypto";
import { DatabaseSync } from "node:sqlite";

import {
  checksumEnvelope,
  redactSecrets,
  validateEnvelope,
  type ResultEnvelope,
} from "./envelope.ts";

type ReviewQueueItem = {
  executionId: string;
  caseId: string;
  outcome: string;
  reviewStatus: string;
  startedAt: string;
};

type RunSummary = {
  runId: string;
  passed: number;
  flaky: number;
  potentialIssues: number;
  inconsistent: number;
  blocked: number;
  sourceReview: number;
  unknown: number;
  pendingReview: number;
};

const migrate = (database: DatabaseSync): void => {
  database.exec(`
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS schema_migrations (
      version INTEGER PRIMARY KEY,
      applied_at TEXT NOT NULL,
      checksum TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS test_runs (
      id TEXT PRIMARY KEY,
      command TEXT NOT NULL,
      environment TEXT NOT NULL,
      base_url TEXT NOT NULL,
      started_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS case_executions (
      id TEXT PRIMARY KEY,
      run_id TEXT NOT NULL REFERENCES test_runs(id),
      case_id TEXT NOT NULL,
      case_revision TEXT NOT NULL,
      function_or_flow_id TEXT NOT NULL,
      primary_module_id TEXT NOT NULL,
      title_snapshot TEXT NOT NULL,
      registry_status_snapshot TEXT NOT NULL,
      preliminary_outcome TEXT NOT NULL,
      review_status TEXT NOT NULL,
      started_at TEXT NOT NULL,
      finished_at TEXT NOT NULL,
      duration_ms INTEGER NOT NULL,
      final_attempt_number INTEGER NOT NULL,
      writer_payload_checksum TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS attempts (
      id TEXT PRIMARY KEY,
      case_execution_id TEXT NOT NULL REFERENCES case_executions(id),
      attempt_number INTEGER NOT NULL CHECK(attempt_number BETWEEN 1 AND 4),
      status TEXT NOT NULL,
      error_message TEXT,
      UNIQUE(case_execution_id, attempt_number)
    );
    CREATE TABLE IF NOT EXISTS review_events (
      id TEXT PRIMARY KEY,
      case_execution_id TEXT NOT NULL REFERENCES case_executions(id),
      previous_status TEXT,
      new_status TEXT NOT NULL,
      classification TEXT,
      reviewer TEXT,
      notes TEXT,
      created_at TEXT NOT NULL,
      retest_required INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS execution_datasets (
      id TEXT PRIMARY KEY,
      case_execution_id TEXT NOT NULL REFERENCES case_executions(id),
      dataset_id TEXT NOT NULL,
      dataset_revision TEXT NOT NULL,
      setup_status TEXT NOT NULL,
      correlation_key TEXT
    );
    CREATE TABLE IF NOT EXISTS artifacts (
      id TEXT PRIMARY KEY,
      case_execution_id TEXT NOT NULL REFERENCES case_executions(id),
      attempt_id TEXT REFERENCES attempts(id),
      artifact_type TEXT NOT NULL,
      relative_path TEXT NOT NULL,
      created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_case_review_status
      ON case_executions(review_status, started_at);
    CREATE INDEX IF NOT EXISTS idx_case_module_review
      ON case_executions(primary_module_id, review_status);
  `);

  database.prepare(`
    INSERT OR IGNORE INTO schema_migrations(version, applied_at, checksum)
    VALUES (1, ?, ?)
  `).run(new Date().toISOString(), "initial-result-store-v1");
};

export const createResultStore = (path: string) => {
  const database = new DatabaseSync(path);
  migrate(database);

  const writeEnvelope = (input: unknown): { status: "written" | "duplicate" } => {
    const redacted = redactSecrets(input);
    const envelope = validateEnvelope(redacted);
    const checksum = checksumEnvelope(envelope);
    const existing = database.prepare(`
      SELECT writer_payload_checksum AS checksum
      FROM case_executions
      WHERE id = ?
    `).get(envelope.execution.id) as { checksum?: string } | undefined;

    if (existing) {
      if (existing.checksum !== checksum) {
        throw new Error("execution ID already exists with a different checksum");
      }
      return { status: "duplicate" };
    }

    database.exec("BEGIN IMMEDIATE");
    try {
      database.prepare(`
        INSERT OR IGNORE INTO test_runs(id, command, environment, base_url, started_at)
        VALUES (?, ?, ?, ?, ?)
      `).run(
        envelope.run.id,
        envelope.run.command,
        envelope.run.environment,
        envelope.run.baseUrl,
        envelope.run.startedAt,
      );

      database.prepare(`
        INSERT INTO case_executions(
          id, run_id, case_id, case_revision, function_or_flow_id,
          primary_module_id, title_snapshot, registry_status_snapshot,
          preliminary_outcome, review_status, started_at, finished_at,
          duration_ms, final_attempt_number, writer_payload_checksum
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `).run(
        envelope.execution.id,
        envelope.run.id,
        envelope.execution.caseId,
        envelope.execution.caseRevision,
        envelope.execution.functionOrFlowId,
        envelope.execution.primaryModuleId,
        envelope.execution.title,
        envelope.execution.registryStatus,
        envelope.execution.outcome,
        envelope.execution.reviewStatus,
        envelope.execution.startedAt,
        envelope.execution.finishedAt,
        envelope.execution.durationMs,
        envelope.execution.finalAttemptNumber,
        checksum,
      );

      const insertAttempt = database.prepare(`
        INSERT INTO attempts(
          id, case_execution_id, attempt_number, status, error_message
        ) VALUES (?, ?, ?, ?, ?)
      `);
      for (const attempt of envelope.attempts) {
        insertAttempt.run(
          attempt.id,
          envelope.execution.id,
          attempt.number,
          attempt.status,
          attempt.errorMessage ?? null,
        );
      }

      if (envelope.dataset) {
        database.prepare(`
          INSERT INTO execution_datasets(
            id, case_execution_id, dataset_id, dataset_revision, setup_status, correlation_key
          ) VALUES (?, ?, ?, ?, ?, ?)
        `).run(
          randomUUID(), envelope.execution.id, envelope.dataset.id,
          envelope.dataset.revision, envelope.dataset.setupStatus,
          envelope.dataset.correlationKey ?? null,
        );
      }

      const attemptIds = new Map(envelope.attempts.map((attempt) => [attempt.number, attempt.id]));
      for (const artifact of envelope.artifacts ?? []) {
        database.prepare(`
          INSERT INTO artifacts(
            id, case_execution_id, attempt_id, artifact_type, relative_path, created_at
          ) VALUES (?, ?, ?, ?, ?, ?)
        `).run(
          randomUUID(), envelope.execution.id,
          artifact.attemptNumber ? attemptIds.get(artifact.attemptNumber) ?? null : null,
          artifact.type, artifact.relativePath, new Date().toISOString(),
        );
      }

      if (envelope.execution.reviewStatus === "NEEDS_HUMAN_REVIEW") {
        database.prepare(`
          INSERT INTO review_events(
            id, case_execution_id, previous_status, new_status,
            created_at, retest_required
          ) VALUES (?, ?, NULL, ?, ?, 0)
        `).run(
          randomUUID(),
          envelope.execution.id,
          "NEEDS_HUMAN_REVIEW",
          new Date().toISOString(),
        );
      }
      database.exec("COMMIT");
      return { status: "written" };
    } catch (error) {
      database.exec("ROLLBACK");
      throw error;
    }
  };

  const listReviewQueue = (): ReviewQueueItem[] =>
    database.prepare(`
      SELECT
        id AS executionId,
        case_id AS caseId,
        preliminary_outcome AS outcome,
        review_status AS reviewStatus,
        started_at AS startedAt
      FROM case_executions
      WHERE review_status = 'NEEDS_HUMAN_REVIEW'
      ORDER BY started_at ASC
    `).all() as ReviewQueueItem[];

  const countExecutions = (): number => {
    const row = database.prepare(
      "SELECT COUNT(*) AS count FROM case_executions",
    ).get() as { count: number };
    return Number(row.count);
  };

  const countArtifacts = (executionId: string): number => {
    const row = database.prepare(
      "SELECT COUNT(*) AS count FROM artifacts WHERE case_execution_id = ?",
    ).get(executionId) as { count: number };
    return Number(row.count);
  };

  const reviewExecution = (
    executionId: string,
    decision: { classification: string; reviewer: string; notes: string; retestRequired: boolean },
  ): void => {
    const current = database.prepare(
      "SELECT review_status AS status FROM case_executions WHERE id = ?",
    ).get(executionId) as { status?: string } | undefined;
    if (!current?.status) throw new Error(`Unknown execution: ${executionId}`);
    database.exec("BEGIN IMMEDIATE");
    try {
      database.prepare(
        "UPDATE case_executions SET review_status = 'REVIEWED' WHERE id = ?",
      ).run(executionId);
      database.prepare(`
        INSERT INTO review_events(
          id, case_execution_id, previous_status, new_status,
          classification, reviewer, notes, created_at, retest_required
        ) VALUES (?, ?, ?, 'REVIEWED', ?, ?, ?, ?, ?)
      `).run(
        randomUUID(), executionId, current.status, decision.classification,
        decision.reviewer, decision.notes, new Date().toISOString(),
        decision.retestRequired ? 1 : 0,
      );
      database.exec("COMMIT");
    } catch (error) {
      database.exec("ROLLBACK");
      throw error;
    }
  };

  const getRunSummary = (runId: string): RunSummary => {
    const rows = database.prepare(`
      SELECT preliminary_outcome AS outcome, review_status AS reviewStatus
      FROM case_executions
      WHERE run_id = ?
    `).all(runId) as Array<{ outcome: string; reviewStatus: string }>;

    const count = (outcome: string) =>
      rows.filter((row) => row.outcome === outcome).length;
    return {
      runId,
      passed: count("PASSED"),
      flaky: count("FLAKY_OR_TRANSIENT"),
      potentialIssues: count("POTENTIAL_ISSUE"),
      inconsistent: count("INCONSISTENT_FAILURE"),
      blocked: count("BLOCKED"),
      sourceReview: count("SOURCE_REVIEW_REQUIRED"),
      unknown: count("UNKNOWN"),
      pendingReview: rows.filter(
        (row) => row.reviewStatus === "NEEDS_HUMAN_REVIEW",
      ).length,
    };
  };

  const getLatestRunSummary = (): RunSummary | null => {
    const row = database.prepare(`
      SELECT id
      FROM test_runs
      ORDER BY started_at DESC, id DESC
      LIMIT 1
    `).get() as { id?: string } | undefined;
    return row?.id ? getRunSummary(row.id) : null;
  };

  return {
    writeEnvelope,
    listReviewQueue,
    countExecutions,
    countArtifacts,
    reviewExecution,
    getRunSummary,
    getLatestRunSummary,
    close: () => database.close(),
  };
};

export const formatRunSummary = (summary: RunSummary): string => [
  `Run: ${summary.runId}`,
  `Passed: ${summary.passed}`,
  `Flaky: ${summary.flaky}`,
  `Potential issues: ${summary.potentialIssues}`,
  `Inconsistent: ${summary.inconsistent}`,
  `Blocked: ${summary.blocked}`,
  `Source review: ${summary.sourceReview}`,
  `Unknown: ${summary.unknown}`,
  `Pending human review: ${summary.pendingReview}`,
].join("\n");
