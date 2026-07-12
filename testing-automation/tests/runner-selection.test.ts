import assert from "node:assert/strict";
import test from "node:test";

import { listRegisteredCases, selectCases } from "../framework/src/case-registry.ts";

test("a clean registry begins with no product test cases", () => {
  assert.deepEqual(listRegisteredCases(), []);
});

test("selection rejects functions until registration", () => {
  assert.throws(() => selectCases("P-99", "P-99-FN-001"), /Unknown function/);
});
