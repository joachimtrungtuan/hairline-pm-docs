import assert from "node:assert/strict";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { createArtifactManager } from "../framework/src/artifact-manager.ts";

test("rolling failures replace older screenshots and final failure is retained", async () => {
  const root = await mkdtemp(join(tmpdir(), "hairline-artifacts-"));
  const manager = createArtifactManager(root, "RUN-20260712T000000Z-abcdef12", "P-99", "P-99-TC-0001");
  await manager.captureFailure(async (path) => { await import("node:fs/promises").then(({ writeFile }) => writeFile(path, "first")); });
  await manager.captureFailure(async (path) => { await import("node:fs/promises").then(({ writeFile }) => writeFile(path, "second")); });
  const retained = await manager.finalize("POTENTIAL_ISSUE");
  assert.equal(retained.length, 1);
  assert.equal(await readFile(retained[0], "utf8"), "second");
});

test("flaky cases retain the latest failed and passing screenshots", async () => {
  const root = await mkdtemp(join(tmpdir(), "hairline-artifacts-"));
  const manager = createArtifactManager(root, "RUN-20260712T000000Z-abcdef12", "P-99", "P-99-TC-0001");
  await manager.captureFailure(async (path) => { await import("node:fs/promises").then(({ writeFile }) => writeFile(path, "failure")); });
  await manager.capturePass(async (path) => { await import("node:fs/promises").then(({ writeFile }) => writeFile(path, "pass")); });
  const retained = await manager.finalize("FLAKY_OR_TRANSIENT");
  assert.deepEqual(retained.map((path) => path.split("/").at(-1)), ["flaky-failure.png", "flaky-pass.png"]);
});

test("potential issues retain the latest failure trace", async () => {
  const root = await mkdtemp(join(tmpdir(), "hairline-artifacts-"));
  const manager = createArtifactManager(root, "RUN-20260712T000000Z-abcdef12", "P-99", "P-99-TC-0001");
  await manager.captureFailure(async (path) => { await import("node:fs/promises").then(({ writeFile }) => writeFile(path, "failure")); });
  await manager.captureTrace(async (path) => { await import("node:fs/promises").then(({ writeFile }) => writeFile(path, "trace")); });
  const retained = await manager.finalize("POTENTIAL_ISSUE");
  assert.deepEqual(retained.map((path) => path.split("/").at(-1)), ["final-failure.png", "trace.zip"]);
});
