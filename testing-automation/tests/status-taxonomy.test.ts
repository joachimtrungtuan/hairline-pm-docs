import assert from "node:assert/strict";
import test from "node:test";

import {
  assertEnumValue,
  enumValues,
  statusTaxonomy,
} from "../framework/src/status-taxonomy.ts";

test("central taxonomy exposes every governed test-case registry status", () => {
  assert.deepEqual(enumValues("registryStatus"), [
    "DRAFT",
    "ACTIVE",
    "SOURCE_REVIEW_REQUIRED",
    "UI_REVIEW_REQUIRED",
    "UPDATE_APPROVED",
    "SUPERSEDED",
    "RETIRED",
  ]);
});

test("possible UI discrepancy is an active human classification", () => {
  assert.equal(
    assertEnumValue("humanClassification", "POSSIBLE_UI_DISCREPANCY"),
    "POSSIBLE_UI_DISCREPANCY",
  );
});

test("unknown and inactive enum values cannot be used for new records", () => {
  assert.throws(
    () => assertEnumValue("humanClassification", "AD_HOC_STATUS"),
    /Invalid active humanClassification/,
  );
  assert.ok(statusTaxonomy.databaseBindings.length > 0);
});
