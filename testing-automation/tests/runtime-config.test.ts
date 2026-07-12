import assert from "node:assert/strict";
import test from "node:test";

import { loadRuntimeConfig } from "../framework/src/runtime-config.ts";

test("runtime config reuses the existing global Playwright MCP installation", () => {
  const config = loadRuntimeConfig({
    HAIRLINE_PROVIDER_EMAIL: "provider@example.test",
    HAIRLINE_PROVIDER_PASSWORD: "secret",
  });

  assert.match(config.playwrightPackageJson, /@playwright\/mcp\/node_modules\/playwright\/package\.json$/);
  assert.equal(config.baseUrl, "https://admin.hairline.app");
});

test("runtime config rejects a partial environment credential instead of mixing sources", () => {
  assert.throws(() => loadRuntimeConfig({
    HAIRLINE_PROVIDER_EMAIL: "provider@example.test",
    HAIRLINE_PROVIDER_ACCOUNT: "UNKNOWN",
  }), /UNKNOWN/);
});
