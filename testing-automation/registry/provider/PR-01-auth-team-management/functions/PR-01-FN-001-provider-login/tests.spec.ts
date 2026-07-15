import assert from "node:assert/strict";

import { buildProviderLoginDataset, type ProviderLoginDataset } from "./datasets.ts";

type BrowserPage = any;
type RegisteredLoginCase = { id: string; datasetId: string };

export const caseTitles = {
  "PR-01-TC-0001": "Active Provider successfully logs in",
  "PR-01-TC-0002": "Provider login requires a username",
  "PR-01-TC-0003": "Provider login requires a password",
  "PR-01-TC-0004": "Provider login reports both required fields when empty",
  "PR-01-TC-0005": "Unknown Provider credentials are rejected safely",
  "PR-01-TC-0006": "Provider credentials cannot authenticate as Hairline Team",
} as const;

export const setupDataset = async (
  testCase: RegisteredLoginCase,
  environment: Record<string, string | undefined>,
  runId: string,
): Promise<ProviderLoginDataset> => buildProviderLoginDataset(testCase.datasetId, environment, runId);

const routeForRole = (role: ProviderLoginDataset["role"]) => role === "provider"
  ? "/auth/provider/login"
  : "/auth/hairline-team/login";

const roleName = (role: ProviderLoginDataset["role"]) => role === "provider"
  ? "Log in for Provider"
  : "Log in for Hairline Team";

const openSelectedLogin = async (page: BrowserPage, baseUrl: string, role: ProviderLoginDataset["role"]) => {
  await page.goto(`${baseUrl}/auth`, { waitUntil: "domcontentloaded" });

  const providerRole = page.getByRole("link", { name: "Log in for Provider" });
  const hairlineTeamRole = page.getByRole("link", { name: "Log in for Hairline Team" });
  await Promise.all([
    providerRole.waitFor({ state: "visible" }),
    hairlineTeamRole.waitFor({ state: "visible" }),
  ]);

  await Promise.all([
    page.waitForURL((url: URL) => url.pathname === routeForRole(role)),
    page.getByRole("link", { name: roleName(role) }).click(),
  ]);
};

const isLoginRequest = (requestOrResponse: any) => {
  const url = new URL(requestOrResponse.url());
  const request = typeof requestOrResponse.request === "function" ? requestOrResponse.request() : requestOrResponse;
  return request.method() === "POST" && url.pathname === "/api/auth/login";
};

const fillCredentials = async (page: BrowserPage, dataset: ProviderLoginDataset) => {
  if (dataset.username) await page.getByRole("textbox", { name: "Username" }).fill(dataset.username);
  if (dataset.password) await page.getByRole("textbox", { name: "Password" }).fill(dataset.password);
};

const submitAndGetResponse = async (page: BrowserPage) => {
  const responsePromise = page.waitForResponse(isLoginRequest);
  await page.getByRole("button", { name: "Log in", exact: true }).click();
  return responsePromise;
};

const assertValidationWithoutRequest = async (page: BrowserPage, expectedMessages: string[]) => {
  let loginRequestCount = 0;
  page.on("request", (request: any) => {
    if (isLoginRequest(request)) loginRequestCount += 1;
  });
  await page.getByRole("button", { name: "Log in", exact: true }).click();
  await Promise.all(expectedMessages.map((message) => page.getByText(message, { exact: true }).waitFor({ state: "visible" })));
  assert.equal(loginRequestCount, 0, "Client validation must block the authentication request");
};

export const executeBrowserCase = async (
  testCase: RegisteredLoginCase,
  page: BrowserPage,
  dataset: ProviderLoginDataset,
  environment: Record<string, string | undefined>,
): Promise<void> => {
  const baseUrl = environment.HAIRLINE_BASE_URL || "https://admin.hairline.app";
  await openSelectedLogin(page, baseUrl, dataset.role);
  await fillCredentials(page, dataset);

  switch (testCase.id) {
    case "PR-01-TC-0001": {
      const response = await submitAndGetResponse(page);
      assert.equal(response.status(), 200, `Expected Provider authentication HTTP 200, received ${response.status()}`);
      await page.waitForURL((url: URL) => url.pathname === "/");
      await page.getByRole("heading", { name: "Dashboard", exact: true }).first().waitFor({ state: "visible" });
      await page.getByRole("link", { name: /Provider Profile/ }).waitFor({ state: "visible" });
      return;
    }
    case "PR-01-TC-0002":
      await assertValidationWithoutRequest(page, ["Please input your Username!"]);
      return;
    case "PR-01-TC-0003":
      await assertValidationWithoutRequest(page, ["Please input your Password!"]);
      return;
    case "PR-01-TC-0004":
      await assertValidationWithoutRequest(page, ["Please input your Username!", "Please input your Password!"]);
      return;
    case "PR-01-TC-0005":
    case "PR-01-TC-0006": {
      const response = await submitAndGetResponse(page);
      assert.equal(response.status(), 403, `Expected authentication rejection HTTP 403, received ${response.status()}`);
      await page.getByText("The email or password you entered is incorrect. Please try again.", { exact: true })
        .waitFor({ state: "visible" });
      assert.equal(new URL(page.url()).pathname, routeForRole(dataset.role));
      return;
    }
    default:
      throw new Error(`No Provider login automation mapped for ${testCase.id}`);
  }
};
