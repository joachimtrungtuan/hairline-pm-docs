import assert from "node:assert/strict";
import test from "node:test";

import { listRegisteredCases, selectCases } from "../framework/src/case-registry.ts";

test("the Provider login registry contains the active happy path and derived suite", () => {
  assert.deepEqual(listRegisteredCases().map(({ id, datasetId, status }) => ({ id, datasetId, status })), [
    { id: "PR-01-TC-0001", datasetId: "PR-01-DS-0001", status: "ACTIVE" },
    { id: "PR-01-TC-0002", datasetId: "PR-01-DS-0002", status: "ACTIVE" },
    { id: "PR-01-TC-0003", datasetId: "PR-01-DS-0003", status: "ACTIVE" },
    { id: "PR-01-TC-0004", datasetId: "PR-01-DS-0004", status: "ACTIVE" },
    { id: "PR-01-TC-0005", datasetId: "PR-01-DS-0005", status: "ACTIVE" },
    { id: "PR-01-TC-0006", datasetId: "PR-01-DS-0006", status: "ACTIVE" },
  ]);
});

test("selection resolves the registered Provider login function", () => {
  assert.deepEqual(selectCases("PR-01", "PR-01-FN-001").map((item) => item.id), [
    "PR-01-TC-0001",
    "PR-01-TC-0002",
    "PR-01-TC-0003",
    "PR-01-TC-0004",
    "PR-01-TC-0005",
    "PR-01-TC-0006",
  ]);
});

test("selection still rejects unknown functions", () => {
  assert.throws(() => selectCases("P-99", "P-99-FN-001"), /Unknown function/);
});
