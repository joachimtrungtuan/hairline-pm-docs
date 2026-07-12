import { createHash } from "node:crypto";

import { isFunctionId, isTestCaseId } from "./identifiers.ts";

const RUN_ID = /^RUN-\d{8}T\d{6}Z-[a-f0-9]{8}$/;
const REVISION = /^v[1-9]\d*$/;
const MODULE_ID = /^(?:P|PR|A|S)-\d{2}[a-z]?$/;
const SECRET_KEY = /(authorization|cookie|token|password|secret|api[_-]?key)/i;

type JsonObject = Record<string, unknown>;

export type ResultEnvelope = {
  schemaVersion: 1;
  run: {
    id: string;
    command: string;
    environment: string;
    baseUrl: string;
    startedAt: string;
  };
  execution: {
    id: string;
    caseId: string;
    caseRevision: string;
    functionOrFlowId: string;
    primaryModuleId: string;
    title: string;
    registryStatus: string;
    outcome: string;
    reviewStatus: string;
    startedAt: string;
    finishedAt: string;
    durationMs: number;
    finalAttemptNumber: number;
  };
  attempts: Array<{
    id: string;
    number: number;
    status: string;
    errorMessage?: string;
  }>;
  dataset?: {
    id: string;
    revision: string;
    setupStatus: string;
    correlationKey?: string;
  };
  artifacts?: Array<{
    attemptNumber?: number;
    type: string;
    relativePath: string;
  }>;
};

const isObject = (value: unknown): value is JsonObject =>
  typeof value === "object" && value !== null && !Array.isArray(value);

const requireObject = (value: unknown, name: string): JsonObject => {
  if (!isObject(value)) throw new Error(`${name} must be an object`);
  return value;
};

const requireString = (value: unknown, name: string): string => {
  if (typeof value !== "string" || value.length === 0) {
    throw new Error(`${name} must be a non-empty string`);
  }
  return value;
};

export const validateEnvelope = (value: unknown): ResultEnvelope => {
  const root = requireObject(value, "envelope");
  if (root.schemaVersion !== 1) throw new Error("schemaVersion must be 1");

  const run = requireObject(root.run, "run");
  const runId = requireString(run.id, "run.id");
  if (!RUN_ID.test(runId)) throw new Error("run.id is invalid");

  const execution = requireObject(root.execution, "execution");
  const caseId = requireString(execution.caseId, "execution.caseId");
  if (!isTestCaseId(caseId)) throw new Error("execution.caseId is invalid");
  const functionId = requireString(
    execution.functionOrFlowId,
    "execution.functionOrFlowId",
  );
  if (!isFunctionId(functionId)) {
    throw new Error("execution.functionOrFlowId is invalid");
  }
  const moduleId = requireString(
    execution.primaryModuleId,
    "execution.primaryModuleId",
  );
  if (!MODULE_ID.test(moduleId)) {
    throw new Error("execution.primaryModuleId is invalid");
  }
  const revision = requireString(
    execution.caseRevision,
    "execution.caseRevision",
  );
  if (!REVISION.test(revision)) {
    throw new Error("execution.caseRevision is invalid");
  }
  if (!Array.isArray(root.attempts) || root.attempts.length === 0) {
    throw new Error("attempts must be a non-empty array");
  }

  for (const [index, item] of root.attempts.entries()) {
    const attempt = requireObject(item, `attempts[${index}]`);
    const number = attempt.number;
    if (!Number.isInteger(number) || Number(number) < 1 || Number(number) > 4) {
      throw new Error(`attempts[${index}].number is invalid`);
    }
  }

  return value as ResultEnvelope;
};

export const redactSecrets = (value: unknown): unknown => {
  if (Array.isArray(value)) return value.map(redactSecrets);
  if (!isObject(value)) return value;

  return Object.fromEntries(
    Object.entries(value).map(([key, nested]) => [
      key,
      SECRET_KEY.test(key) ? "[REDACTED]" : redactSecrets(nested),
    ]),
  );
};

const stableValue = (value: unknown): unknown => {
  if (Array.isArray(value)) return value.map(stableValue);
  if (!isObject(value)) return value;

  return Object.fromEntries(
    Object.keys(value)
      .sort()
      .map((key) => [key, stableValue(value[key])]),
  );
};

export const checksumEnvelope = (value: unknown): string =>
  createHash("sha256")
    .update(JSON.stringify(stableValue(value)))
    .digest("hex");
