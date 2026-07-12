import { randomBytes, randomUUID } from "node:crypto";
import { mkdir } from "node:fs/promises";
import { basename, relative, resolve } from "node:path";
import { pathToFileURL } from "node:url";

import { createArtifactManager } from "./artifact-manager.ts";
import { selectCases } from "./case-registry.ts";
import { loadExistingPlaywright, loadRuntimeConfig } from "./runtime-config.ts";
import { createResultStore } from "./result-store.ts";
import { deriveOutcome, type Attempt } from "./retry-outcome.ts";

const root = resolve(import.meta.dirname, "../..");
const databasePath = resolve(root, "results/test-results.sqlite");
const artifactRoot = resolve(root, "results/artifacts");
const wait = (milliseconds: number) => new Promise((done) => setTimeout(done, milliseconds));
const runId = () => `RUN-${new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "")}-${randomBytes(4).toString("hex")}`;

const [moduleId, functionId, ...rest] = process.argv.slice(2);
const caseIndex = rest.indexOf("--case");
const caseId = caseIndex >= 0 ? rest[caseIndex + 1] : undefined;
if (!moduleId || !functionId || rest.includes("--help")) {
  console.log("Usage: pnpm test:function <module-id> <function-id> [--case <case-id>]");
  process.exit(moduleId && functionId ? 0 : 2);
}

const config = loadRuntimeConfig();
const runtimeEnvironment = {
  ...process.env,
  HAIRLINE_PROVIDER_EMAIL: config.provider.email,
  HAIRLINE_PROVIDER_PASSWORD: config.provider.password,
  HAIRLINE_PATIENT_EMAIL: config.patient.email,
  HAIRLINE_PATIENT_PASSWORD: config.patient.password,
  HAIRLINE_RESTRICTED_PROVIDER_EMAIL: config.restrictedProvider.email,
  HAIRLINE_RESTRICTED_PROVIDER_PASSWORD: config.restrictedProvider.password,
};
const selected = selectCases(moduleId, functionId, caseId);
if (selected.some((item) => item.status !== "ACTIVE") && !rest.includes("--allow-draft")) {
  throw new Error("Selection contains DRAFT cases; human activation is required (use --allow-draft only for controlled validation)");
}
const id = runId();
await mkdir(resolve(root, "results"), { recursive: true });
const store = createResultStore(databasePath);
let requiresReview = false;

for (const testCase of selected) {
  const automation = await import(pathToFileURL(resolve(root, testCase.automationModule)).href) as {
    setupDataset: (testCase: typeof testCase, environment: Record<string, string | undefined>, runId: string) => Promise<any>;
    executeBrowserCase: (testCase: typeof testCase, page: any, dataset: any, environment: Record<string, string | undefined>) => Promise<void>;
  };
  const executionId = randomUUID();
  const started = new Date();
  const attempts: Attempt[] = [];
  const attemptRows: Array<{ id: string; number: number; status: string; errorMessage?: string }> = [];
  const artifacts = createArtifactManager(artifactRoot, id, testCase.moduleId, testCase.id);
  let datasetMetadata: { id: string; revision: string; setupStatus: string; correlationKey?: string } = {
    id: testCase.datasetId, revision: "v1", setupStatus: "pending",
  };
  let retainedArtifactPaths: string[] = [];
  let outcome = "BLOCKED";
  let reviewStatus = "NEEDS_HUMAN_REVIEW";
  try {
    const dataset = await automation.setupDataset(testCase, runtimeEnvironment, id);
    datasetMetadata = { id: testCase.datasetId, revision: "v1", setupStatus: "passed", correlationKey: dataset.marker };
    for (let number = 1; number <= 4; number += 1) {
      const { chromium } = loadExistingPlaywright();
      const browser = await chromium.launch({ headless: config.headless, executablePath: config.browserExecutable });
      const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
      await context.tracing.start({ screenshots: true, snapshots: true, sources: false });
      const page = await context.newPage();
      try {
        await automation.executeBrowserCase(testCase, page, dataset, runtimeEnvironment);
        attempts.push({ status: "passed" });
        attemptRows.push({ id: randomUUID(), number, status: "passed" });
        if (number > 1) {
          await artifacts.capturePass((path) => page.screenshot({ path, fullPage: true }));
          await artifacts.captureTrace((path) => context.tracing.stop({ path }));
        } else {
          await context.tracing.stop();
        }
        await browser.close();
        break;
      } catch (error) {
        const message = error instanceof Error ? `${error.name}:${error.message}` : String(error);
        attempts.push({ status: "failed", signature: message });
        attemptRows.push({ id: randomUUID(), number, status: "failed", errorMessage: message });
        await artifacts.captureFailure((path) => page.screenshot({ path, fullPage: true }));
        await artifacts.captureTrace((path) => context.tracing.stop({ path }));
        await browser.close();
        if (number < 4) await wait(5000);
      }
    }
    ({ outcome, reviewStatus } = deriveOutcome(attempts));
    retainedArtifactPaths = await artifacts.finalize(outcome as any);
  } catch (error) {
    if (datasetMetadata.setupStatus === "pending") datasetMetadata.setupStatus = "failed";
    const message = error instanceof Error ? `${error.name}:${error.message}` : String(error);
    attemptRows.push({ id: randomUUID(), number: 1, status: "blocked", errorMessage: message });
  }

  const finished = new Date();
  store.writeEnvelope({
    schemaVersion: 1,
    run: { id, command: `pnpm test:function ${moduleId} ${functionId}`, environment: "development", baseUrl: config.baseUrl, startedAt: started.toISOString() },
    execution: {
      id: executionId, caseId: testCase.id, caseRevision: testCase.revision,
      functionOrFlowId: testCase.functionId, primaryModuleId: testCase.moduleId,
      title: testCase.title, registryStatus: testCase.status, outcome, reviewStatus,
      startedAt: started.toISOString(), finishedAt: finished.toISOString(),
      durationMs: finished.getTime() - started.getTime(), finalAttemptNumber: attemptRows.at(-1)?.number || 1,
    },
    attempts: attemptRows,
    dataset: datasetMetadata,
    artifacts: retainedArtifactPaths.map((path) => ({
      attemptNumber: attemptRows.at(-1)?.number,
      type: basename(path) === "trace.zip" ? "trace" : basename(path).replace(".png", "-screenshot"),
      relativePath: relative(artifactRoot, path),
    })),
  });
  if (reviewStatus === "NEEDS_HUMAN_REVIEW") requiresReview = true;
  console.log(`${testCase.id}: ${outcome} / ${reviewStatus}`);
}

console.log(store.getRunSummary(id));
console.log(`Results: ${databasePath}`);
store.close();
process.exitCode = requiresReview ? 1 : 0;
