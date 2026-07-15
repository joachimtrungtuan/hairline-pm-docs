import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { createInterface } from "node:readline/promises";

import { createResultStore, formatRunSummary } from "./result-store.ts";
import {
  buildRunInvocation,
  getMenuCatalog,
  type MenuScope,
  type RunInvocation,
} from "./test-menu-support.ts";

const root = resolve(import.meta.dirname, "../..");
const databasePath = resolve(root, "results/test-results.sqlite");
const terminal = createInterface({ input: process.stdin, output: process.stdout });

const runCommand = (invocation: RunInvocation): number => {
  console.log(`\nRunning: ${invocation.command} ${invocation.args.join(" ")}\n`);
  const result = spawnSync(invocation.command, invocation.args, {
    cwd: root,
    env: { ...process.env, ...invocation.environment },
    stdio: "inherit",
  });
  if (result.error) {
    console.error(`Unable to start command: ${result.error.message}`);
    return 1;
  }
  return result.status ?? 1;
};

const runPnpm = (args: string[]): number => runCommand({
  command: "pnpm",
  args,
  environment: {},
});

const choose = async (
  heading: string,
  items: string[],
  backLabel?: string,
): Promise<number> => {
  while (true) {
    console.log(`\n${heading}`);
    items.forEach((item, index) => console.log(`  ${index + 1}. ${item}`));
    if (backLabel) console.log(`  0. ${backLabel}`);
    const raw = (await terminal.question("Choose an option: ")).trim();
    const selection = Number(raw);
    if (backLabel && selection === 0) return -1;
    if (Number.isInteger(selection) && selection >= 1 && selection <= items.length) {
      return selection - 1;
    }
    console.log("Please enter one of the listed numbers.");
  }
};

const confirm = async (question: string): Promise<boolean> => {
  const answer = (await terminal.question(`${question} [Y/n]: `)).trim().toLowerCase();
  return answer === "" || answer === "y" || answer === "yes";
};

const chooseHeadless = async (): Promise<boolean | null> => {
  const selection = await choose("Browser mode", [
    "Visible browser (recommended)",
    "Headless browser",
  ], "Back");
  if (selection < 0) return null;
  return selection === 1;
};

const showScope = (scope: MenuScope): void => {
  console.log(`\n${scope.id} — ${scope.title}`);
  console.log(`Type: ${scope.kind === "FUNCTION" ? "Function" : "Flow"}`);
  console.log(`Active cases: ${scope.activeCases.length}`);
  console.log(`Governed coverage gaps: ${scope.coverageGapCount}`);
  scope.activeCases.forEach((testCase) => {
    console.log(`  - ${testCase.id}: ${testCase.title}`);
  });
};

const executeSelection = async (scope: MenuScope, caseId?: string): Promise<void> => {
  const headless = await chooseHeadless();
  if (headless === null) return;
  showScope(scope);
  console.log(`Browser: ${headless ? "Headless" : "Visible"}`);
  console.log(`Selection: ${caseId ? `${caseId} (diagnostic)` : `all ${scope.activeCases.length} active cases`}`);
  if (!await confirm("Run this selection?")) return;

  if (runPnpm(["test:preflight"]) !== 0) {
    console.log("\nPreflight failed. No test cases were started.");
    return;
  }

  const status = runCommand(buildRunInvocation(scope, { caseId, headless }));
  if (status !== 0) {
    console.log("\nThe run needs attention. No bug decision was made automatically.");
    console.log("Choose 'Inspect pending human reviews' from the main menu.");
  }
};

const browseAndRun = async (): Promise<void> => {
  const catalog = getMenuCatalog();
  const moduleIndex = await choose("Registered modules", catalog.map((module) => (
    `${module.id} — ${module.title} (${module.tenant})`
  )), "Main menu");
  if (moduleIndex < 0) return;

  const module = catalog[moduleIndex];
  const scopeIndex = await choose("Registered functions and flows", module.scopes.map((scope) => (
    `${scope.id} — ${scope.title} [${scope.kind.toLowerCase()}] — ${scope.activeCases.length} active cases`
  )), "Modules");
  if (scopeIndex < 0) return;

  const scope = module.scopes[scopeIndex];
  showScope(scope);
  const runIndex = await choose("Execution scope", [
    `Run all ${scope.activeCases.length} active cases`,
    "Run one case for diagnosis",
  ], "Functions and flows");
  if (runIndex < 0) return;
  if (runIndex === 0) {
    await executeSelection(scope);
    return;
  }

  const caseIndex = await choose("Diagnostic case", scope.activeCases.map((testCase) => (
    `${testCase.id} — ${testCase.title}`
  )), "Execution scope");
  if (caseIndex < 0) return;
  await executeSelection(scope, scope.activeCases[caseIndex].id);
};

const runAllActive = async (): Promise<void> => {
  const scopes = getMenuCatalog().flatMap((module) => module.scopes);
  const caseCount = scopes.reduce((sum, scope) => sum + scope.activeCases.length, 0);
  const gapCount = scopes.reduce((sum, scope) => sum + scope.coverageGapCount, 0);
  console.log(`\nActive functions/flows: ${scopes.length}`);
  console.log(`Active cases: ${caseCount}`);
  console.log(`Governed coverage gaps: ${gapCount}`);
  const headless = await chooseHeadless();
  if (headless === null || !await confirm(`Run all ${caseCount} active cases?`)) return;
  if (runPnpm(["test:preflight"]) !== 0) {
    console.log("\nPreflight failed. No test cases were started.");
    return;
  }

  let needsAttention = false;
  for (const scope of scopes) {
    const status = runCommand(buildRunInvocation(scope, { headless }));
    if (status !== 0) needsAttention = true;
  }
  if (needsAttention) {
    console.log("\nAt least one run needs attention. No bug decision was made automatically.");
    console.log("Choose 'Inspect pending human reviews' from the main menu.");
  }
};

const showLatestSummary = (): void => {
  if (!existsSync(databasePath)) {
    console.log("\nNo runtime result database exists yet.");
    return;
  }
  const store = createResultStore(databasePath);
  const summary = store.getLatestRunSummary();
  store.close();
  console.log(summary ? `\n${formatRunSummary(summary)}` : "\nNo test runs exist yet.");
};

const main = async (): Promise<void> => {
  console.log("\nHairline Web E2E Test Console");
  console.log("Development environment — deterministic execution, no AI agent");
  while (true) {
    const selection = await choose("Main menu", [
      "Browse registered modules, functions, and flows",
      "Run all active tests",
      "Inspect pending human reviews",
      "View latest run summary",
      "Run preflight",
      "Exit",
    ]);
    if (selection === 0) await browseAndRun();
    if (selection === 1) await runAllActive();
    if (selection === 2) runPnpm(["test:review-queue"]);
    if (selection === 3) showLatestSummary();
    if (selection === 4) runPnpm(["test:preflight"]);
    if (selection === 5) return;
  }
};

try {
  await main();
} finally {
  terminal.close();
}
