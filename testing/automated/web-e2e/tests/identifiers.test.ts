import assert from "node:assert/strict";
import test from "node:test";

import {
  isDatasetId,
  isFunctionId,
  isTestCaseId,
} from "../framework/src/identifiers.ts";

test("accepts module-first synthetic identifiers", () => {
  assert.equal(isFunctionId("P-99-FN-001"), true);
  assert.equal(isTestCaseId("P-99-TC-0001"), true);
  assert.equal(isDatasetId("P-99-DS-0001"), true);
});

test("rejects malformed or wrong-width identifiers", () => {
  assert.equal(isFunctionId("PR02-FN-001"), false);
  assert.equal(isFunctionId("P-99-FN-01"), false);
  assert.equal(isTestCaseId("P-99-TC-001"), false);
  assert.equal(isDatasetId("P-99-DS-00001"), false);
});
