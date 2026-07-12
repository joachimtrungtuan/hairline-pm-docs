import { createRequire } from "node:module";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { readCredential } from "./credential-registry.ts";

type Environment = Record<string, string | undefined>;

const globalMcpPackageJson = process.env.HAIRLINE_PLAYWRIGHT_HOST_PACKAGE
  || "/opt/homebrew/lib/node_modules/@playwright/mcp/package.json";
const globalRequire = createRequire(globalMcpPackageJson);
const localDocs = resolve(dirname(fileURLToPath(import.meta.url)), "../../..");
const credentialFile = (name: string) => resolve(localDocs, "testing-plans/testing-credentials", name);

const required = (environment: Environment, name: string): string => {
  const value = environment[name]?.trim();
  if (!value) throw new Error(`Missing required environment variable: ${name}`);
  return value;
};

const credential = (
  environment: Environment,
  emailKey: string,
  passwordKey: string,
  file: string,
  accountId: string,
) => environment[emailKey]?.trim() && environment[passwordKey]?.trim()
  ? { email: required(environment, emailKey), password: required(environment, passwordKey) }
  : readCredential(credentialFile(file), accountId);

export const loadRuntimeConfig = (environment: Environment = process.env) => ({
  baseUrl: environment.HAIRLINE_BASE_URL?.trim() || "https://admin.hairline.app",
  apiUrl: environment.HAIRLINE_API_URL?.trim() || "https://backend.hairline.app/api",
  headless: environment.HAIRLINE_HEADLESS === "true",
  browserExecutable: environment.HAIRLINE_BROWSER_EXECUTABLE?.trim()
    || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  provider: credential(environment, "HAIRLINE_PROVIDER_EMAIL", "HAIRLINE_PROVIDER_PASSWORD", "provider-accounts.md", environment.HAIRLINE_PROVIDER_ACCOUNT || "V1"),
  patient: credential(environment, "HAIRLINE_PATIENT_EMAIL", "HAIRLINE_PATIENT_PASSWORD", "patient-accounts.md", environment.HAIRLINE_PATIENT_ACCOUNT || "P1"),
  restrictedProvider: credential(environment, "HAIRLINE_RESTRICTED_PROVIDER_EMAIL", "HAIRLINE_RESTRICTED_PROVIDER_PASSWORD", "admin-accounts.md", environment.HAIRLINE_RESTRICTED_PROVIDER_ACCOUNT || "S1"),
  playwrightPackageJson: globalRequire.resolve("playwright/package.json"),
});

export const loadExistingPlaywright = () => globalRequire("playwright");
