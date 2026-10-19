import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { createResultStore } from "./result-store.ts";

const databasePath = resolve(import.meta.dirname, "../../results/test-results.sqlite");
if (!existsSync(databasePath)) {
  console.log("No runtime result database exists yet.");
  console.log("Pending human review: 0");
  process.exit(0);
}
const store = createResultStore(databasePath);
const rows = store.listReviewQueue();
console.table(rows);
console.log(`Pending human review: ${rows.length}`);
store.close();
