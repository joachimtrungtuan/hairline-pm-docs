import { existsSync } from "node:fs";
import { resolve } from "node:path";

import { createResultStore } from "./result-store.ts";
import { assertEnumValue } from "./status-taxonomy.ts";

const args = process.argv.slice(2);
const value = (flag: string): string | undefined => {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : undefined;
};
const executionId = args[0];
const classification = value("--classification");
const reviewer = value("--reviewer");
const notes = value("--notes");

if (args.includes("--help")) {
  console.log("Usage: pnpm test:review <execution-id> --classification <human-decision> --reviewer <name-or-role> --notes <text> [--retest-required]");
} else if (!executionId || !classification || !reviewer || !notes) {
  console.log("Usage: pnpm test:review <execution-id> --classification <human-decision> --reviewer <name-or-role> --notes <text> [--retest-required]");
  process.exitCode = 2;
} else {
  assertEnumValue("humanClassification", classification);
  const databasePath = resolve(import.meta.dirname, "../../results/test-results.sqlite");
  if (!existsSync(databasePath)) throw new Error("No runtime result database exists yet");
  const store = createResultStore(databasePath);
  store.reviewExecution(executionId, {
    classification,
    reviewer,
    notes,
    retestRequired: args.includes("--retest-required"),
  });
  store.close();
  console.log(`Recorded human review for ${executionId}`);
  console.log(`Classification: ${classification}`);
}
