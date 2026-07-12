import { access, constants } from "node:fs/promises";

import { loadExistingPlaywright, loadRuntimeConfig } from "./runtime-config.ts";

try {
  const config = loadRuntimeConfig();
  await access(config.playwrightPackageJson, constants.R_OK);
  loadExistingPlaywright();
  await access(config.browserExecutable, constants.X_OK);
  const response = await fetch(config.baseUrl, { method: "HEAD", signal: AbortSignal.timeout(15_000) });
  if (!response.ok) throw new Error(`Dashboard returned HTTP ${response.status}`);
  console.log("Preflight passed");
  console.log(`Dashboard: ${config.baseUrl}`);
  console.log(`Playwright: ${config.playwrightPackageJson}`);
  console.log(`Browser: ${config.browserExecutable}`);
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 2;
}
