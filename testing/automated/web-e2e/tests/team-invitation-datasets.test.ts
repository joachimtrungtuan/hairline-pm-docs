import assert from "node:assert/strict";
import test from "node:test";

import {
  buildTeamInvitationDataset,
  deriveTeamFilterFixtures,
} from "../registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/datasets.ts";

const environment = {
  HAIRLINE_API_URL: "https://backend.example.test/api",
  HAIRLINE_PROVIDER_EMAIL: "provider@example.test",
  HAIRLINE_PROVIDER_PASSWORD: "ProviderPass123!",
  HAIRLINE_ALLOW_PUBLIC_INVITE_MAILBOX: "true",
};

test("builds deterministic synthetic Maildrop datasets without API setup cases", async () => {
  const runId = "RUN-20260715T000000Z-a1b2c3d4";
  const datasetIds = [7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    .map((number) => `PR-01-DS-${String(number).padStart(4, "0")}`);
  const datasets = await Promise.all(datasetIds.map((datasetId) => buildTeamInvitationDataset(datasetId, environment, runId)));

  assert.equal(new Set(datasets.map(({ email }) => email)).size, datasets.length);
  assert.ok(datasets.every(({ email }) => /^hl-pr01-[a-f0-9]{20}@maildrop\.cc$/.test(email)));
  assert.ok(datasets.every(({ marker }, index) => marker === `${runId}:${datasetIds[index]}`));
  assert.ok(datasets.every(({ role }) => role === "manager"));
  assert.match(datasets.at(-1)?.noMatchSearchTerm || "", /^no-team-member-[a-f0-9]{16}$/);
});

test("derives individual matching filters and an incompatible combined filter from member data", () => {
  const fixtures = deriveTeamFilterFixtures([{
    first_name: "Alpha",
    email: "alpha@example.test",
    role_name: "Manager",
    status: "active",
    region_name: "North",
  }, {
    first_name: "Beta",
    email: "beta@example.test",
    role_name: "Clinical Staff",
    status: "inactive",
    region_name: "South",
  }]);

  assert.equal(fixtures.role?.role, "Manager");
  assert.equal(fixtures.status?.status, "Active");
  assert.equal(fixtures.region?.region, "North");
  assert.equal(fixtures.combined?.rowText, "alpha@example.test");
  assert.deepEqual(
    { role: fixtures.unavailable?.role, status: fixtures.unavailable?.status, region: fixtures.unavailable?.region },
    { role: "Manager", status: "Active", region: "South" },
  );
});

test("does not fabricate a Region filter fixture when member data has no Region relationship", () => {
  const fixtures = deriveTeamFilterFixtures([{
    email: "member@example.test",
    role_name: "Manager",
    status: "pending",
  }]);

  assert.equal(fixtures.region, undefined);
  assert.equal(fixtures.combined, undefined);
  assert.equal(fixtures.unavailable, undefined);
});

test("rejects an unknown Team and Invitation dataset", async () => {
  await assert.rejects(
    () => buildTeamInvitationDataset("PR-01-DS-9999", environment, "RUN-TEST"),
    /Unknown Team and Invitation dataset/,
  );
});

test("blocks public Maildrop invitation mutations without explicit human acknowledgement", async () => {
  await assert.rejects(
    () => buildTeamInvitationDataset(
      "PR-01-DS-0012",
      { ...environment, HAIRLINE_ALLOW_PUBLIC_INVITE_MAILBOX: "false" },
      "RUN-TEST",
    ),
    /Public Maildrop invitation is disabled/,
  );
});
