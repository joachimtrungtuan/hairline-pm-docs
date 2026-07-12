import assert from "node:assert/strict";
import test from "node:test";

import { evidencePlan } from "../framework/src/evidence-policy.ts";

test("retains no screenshot or trace for a clean initial pass", () => {
  assert.deepEqual(evidencePlan("PASSED"), {
    screenshots: [],
    retainTrace: false,
    rollingFailureScreenshot: false,
  });
});

test("retains only the final rolling screenshot and trace for a potential issue", () => {
  assert.deepEqual(evidencePlan("POTENTIAL_ISSUE"), {
    screenshots: ["final-failure.png"],
    retainTrace: true,
    rollingFailureScreenshot: true,
  });
});

test("retains failed and passing screenshots plus trace for a flaky execution", () => {
  assert.deepEqual(evidencePlan("FLAKY_OR_TRANSIENT"), {
    screenshots: ["flaky-failure.png", "flaky-pass.png"],
    retainTrace: true,
    rollingFailureScreenshot: true,
  });
});
