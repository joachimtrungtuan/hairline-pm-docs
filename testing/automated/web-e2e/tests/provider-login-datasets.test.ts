import assert from "node:assert/strict";
import test from "node:test";

import { buildProviderLoginDataset } from "../registry/provider/PR-01-auth-team-management/functions/PR-01-FN-001-provider-login/datasets.ts";

const environment = {
  HAIRLINE_PROVIDER_EMAIL: "active-provider@example.test",
  HAIRLINE_PROVIDER_PASSWORD: "ActiveProviderPass123!",
  HAIRLINE_RESTRICTED_PROVIDER_EMAIL: "secondary-provider@example.test",
  HAIRLINE_RESTRICTED_PROVIDER_PASSWORD: "SecondaryProviderPass123!",
};

test("builds deterministic datasets for every executable Provider login case", () => {
  const runId = "RUN-20260715T000000Z-a1b2c3d4";
  const datasets = [1, 2, 3, 4, 5, 6].map((number) => buildProviderLoginDataset(
    `PR-01-DS-${String(number).padStart(4, "0")}`,
    environment,
    runId,
  ));

  assert.equal(datasets[0].username, environment.HAIRLINE_PROVIDER_EMAIL);
  assert.equal(datasets[0].password, environment.HAIRLINE_PROVIDER_PASSWORD);
  assert.equal(datasets[1].username, "");
  assert.notEqual(datasets[1].password, "");
  assert.notEqual(datasets[2].username, "");
  assert.equal(datasets[2].password, "");
  assert.equal(datasets[3].username, "");
  assert.equal(datasets[3].password, "");
  assert.match(datasets[4].username, /^e2e-login-/);
  assert.equal(datasets[5].username, environment.HAIRLINE_RESTRICTED_PROVIDER_EMAIL);
  assert.equal(new Set(datasets.map((dataset) => dataset.marker)).size, 6);
});

test("rejects an unknown Provider login dataset", () => {
  assert.throws(
    () => buildProviderLoginDataset("PR-01-DS-9999", environment, "RUN-TEST"),
    /Unknown Provider login dataset/,
  );
});
