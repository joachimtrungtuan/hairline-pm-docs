import assert from "node:assert/strict";
import test from "node:test";

import { buildRunInvocation, getMenuCatalog } from "../framework/src/test-menu-support.ts";

test("menu catalog groups active registered cases by module and function or flow", () => {
  const catalog = getMenuCatalog();

  assert.deepEqual(catalog.map((module) => ({
    id: module.id,
    title: module.title,
    tenant: module.tenant,
    scopes: module.scopes.map((scope) => ({
      id: scope.id,
      title: scope.title,
      kind: scope.kind,
      activeCaseCount: scope.activeCases.length,
      coverageGapCount: scope.coverageGapCount,
    })),
  })), [{
    id: "PR-01",
    title: "Auth & Team Management",
    tenant: "Provider",
    scopes: [{
      id: "PR-01-FN-001",
      title: "Provider login",
      kind: "FUNCTION",
      activeCaseCount: 6,
      coverageGapCount: 4,
    }],
  }]);
});

test("menu builds function-wide and diagnostic case invocations without draft overrides", () => {
  const scope = getMenuCatalog()[0].scopes[0];

  assert.deepEqual(buildRunInvocation(scope, { headless: false }), {
    command: "pnpm",
    args: ["test:function", "PR-01", "PR-01-FN-001"],
    environment: {},
  });
  assert.deepEqual(buildRunInvocation(scope, {
    headless: true,
    caseId: "PR-01-TC-0005",
  }), {
    command: "pnpm",
    args: ["test:function", "PR-01", "PR-01-FN-001", "--case", "PR-01-TC-0005"],
    environment: { HAIRLINE_HEADLESS: "true" },
  });
});

test("menu rejects a diagnostic case outside the selected scope", () => {
  const scope = getMenuCatalog()[0].scopes[0];

  assert.throws(
    () => buildRunInvocation(scope, { headless: false, caseId: "PR-99-TC-9999" }),
    /not an active case/,
  );
});
