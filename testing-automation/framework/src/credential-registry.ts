import { readFileSync } from "node:fs";

type Credential = { email: string; password: string };

export const readCredential = (path: string, accountId: string): Credential => {
  const lines = readFileSync(path, "utf8").split(/\r?\n/);
  const row = lines.find((line) => new RegExp(`^\\|\\s*${accountId}\\s*\\|`).test(line));
  if (!row) throw new Error(`Credential account ${accountId} was not found`);
  const cells = row.split("|").slice(1, -1).map((cell) => cell.trim());
  const [, email, password] = cells;
  if (!email || !password) throw new Error(`Credential account ${accountId} is incomplete`);
  return { email, password };
};
