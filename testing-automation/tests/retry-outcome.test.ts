import assert from "node:assert/strict";
import test from "node:test";

import {
  deriveOutcome,
  executeWithRetries,
} from "../framework/src/retry-outcome.ts";

test("runs one initial attempt plus three retries with the minimum delay", async () => {
  let calls = 0;
  const delays: number[] = [];

  const result = await executeWithRetries(
    async () => {
      calls += 1;
      throw new Error("consistent failure");
    },
    async (milliseconds) => {
      delays.push(milliseconds);
    },
  );

  assert.equal(calls, 4);
  assert.deepEqual(delays, [5000, 5000, 5000]);
  assert.equal(result.outcome, "POTENTIAL_ISSUE");
  assert.equal(result.reviewStatus, "NEEDS_HUMAN_REVIEW");
});

test("stops after a later pass and classifies the execution as flaky", async () => {
  let calls = 0;
  const delays: number[] = [];

  const result = await executeWithRetries(
    async () => {
      calls += 1;
      if (calls < 3) throw new Error("temporary failure");
      return "passed";
    },
    async (milliseconds) => {
      delays.push(milliseconds);
    },
  );

  assert.equal(calls, 3);
  assert.deepEqual(delays, [5000, 5000]);
  assert.equal(result.outcome, "FLAKY_OR_TRANSIENT");
  assert.equal(result.reviewStatus, "NEEDS_HUMAN_REVIEW");
});

test("classifies an initial pass as clean", () => {
  assert.deepEqual(deriveOutcome([{ status: "passed" }]), {
    outcome: "PASSED",
    reviewStatus: "REVIEW_NOT_REQUIRED",
  });
});

test("classifies differing failure signatures as inconsistent", () => {
  assert.deepEqual(
    deriveOutcome([
      { status: "failed", signature: "timeout" },
      { status: "failed", signature: "assertion" },
      { status: "failed", signature: "timeout" },
      { status: "failed", signature: "assertion" },
    ]),
    {
      outcome: "INCONSISTENT_FAILURE",
      reviewStatus: "NEEDS_HUMAN_REVIEW",
    },
  );
});
