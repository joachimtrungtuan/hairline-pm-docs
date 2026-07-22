import assert from "node:assert/strict";

import { createApiClient } from "../../../../../framework/src/api-client.ts";
import { buildTeamInvitationDataset, type TeamInvitationDataset } from "./datasets.ts";

type BrowserPage = any;
type RegisteredTeamCase = { id: string; datasetId: string };
type Invitation = { email?: string; status?: string; expires_at?: string };

export const caseTitles = {
  "PR-01-TC-0007": "Authorized Provider can access Team and Invitations",
  "PR-01-TC-0008": "Team directory search covers required member attributes",
  "PR-01-TC-0009": "Team directory filters expose role status and region controls",
  "PR-01-TC-0010": "Team directory uses the required default page size",
  "PR-01-TC-0011": "Invite form exposes the complete PRD field contract",
  "PR-01-TC-0012": "Provider invites a Manager with fresh Maildrop delivery",
  "PR-01-TC-0013": "Invite form rejects an invalid email without submission",
  "PR-01-TC-0014": "Duplicate invitation within the Provider is blocked",
  "PR-01-TC-0015": "Invitation role choices exclude Owner",
  "PR-01-TC-0016": "Pending invitation exposes governed management actions",
  "PR-01-TC-0017": "Resending a pending invitation refreshes expiry and email",
  "PR-01-TC-0018": "Cancelling a pending invitation requires confirmation",
  "PR-01-TC-0019": "Team search shows an empty state for an unavailable value",
  "PR-01-TC-0020": "Role filter returns an available team member",
  "PR-01-TC-0021": "Status filter returns an available team member",
  "PR-01-TC-0022": "Region filter returns an available team member",
  "PR-01-TC-0023": "Role status and region filters return their shared match",
  "PR-01-TC-0024": "Valid combined filters show an empty state when no member matches",
} as const;

export const setupDataset = async (
  testCase: RegisteredTeamCase,
  environment: Record<string, string | undefined>,
  runId: string,
): Promise<TeamInvitationDataset> => buildTeamInvitationDataset(testCase.datasetId, environment, runId);

const required = (environment: Record<string, string | undefined>, key: string): string => {
  const value = environment[key]?.trim();
  if (!value) throw new Error(`Missing runtime value: ${key}`);
  return value;
};

const loginProvider = async (page: BrowserPage, environment: Record<string, string | undefined>) => {
  const baseUrl = environment.HAIRLINE_BASE_URL || "https://admin.hairline.app";
  await page.goto(`${baseUrl}/auth`, { waitUntil: "domcontentloaded" });
  await Promise.all([
    page.waitForURL((url: URL) => url.pathname === "/auth/provider/login"),
    page.getByRole("link", { name: "Log in for Provider" }).click(),
  ]);
  await page.getByRole("textbox", { name: "Username" }).fill(required(environment, "HAIRLINE_PROVIDER_EMAIL"));
  await page.getByRole("textbox", { name: "Password" }).fill(required(environment, "HAIRLINE_PROVIDER_PASSWORD"));
  const responsePromise = page.waitForResponse((response: any) => (
    response.request().method() === "POST" && new URL(response.url()).pathname === "/api/auth/login"
  ));
  await page.getByRole("button", { name: "Log in", exact: true }).click();
  const response = await responsePromise;
  assert.equal(response.status(), 200, "Provider prerequisite login must succeed");
  await page.waitForURL((url: URL) => url.pathname === "/");
};

const openTeam = async (page: BrowserPage, environment: Record<string, string | undefined>) => {
  await loginProvider(page, environment);
  const teamLink = page.getByRole("link", { name: /Team/ }).first();
  await teamLink.waitFor({ state: "visible" });
  await Promise.all([
    page.waitForURL((url: URL) => url.pathname === "/team"),
    teamLink.click(),
  ]);
  await page.getByRole("button").filter({ hasText: "Invite Staff" }).first().waitFor({ state: "visible" });
};

const invitationRow = (page: BrowserPage, email: string) => page.getByRole("row").filter({ hasText: email });

const openInviteDialog = async (page: BrowserPage) => {
  await page.getByRole("button").filter({ hasText: "Invite Staff" }).first().click();
  const dialog = page.getByRole("dialog");
  await dialog.getByRole("heading", { name: /Invite staff/i }).waitFor({ state: "visible" });
  return dialog;
};

const chooseManager = async (page: BrowserPage, dialog: any) => {
  await dialog.locator(".ant-select-selector").click({ force: true });
  const option = page.locator(".ant-select-dropdown:visible .ant-select-item-option-content")
    .filter({ hasText: /^Manager$/ });
  await option.waitFor({ state: "visible" });
  await option.click();
};

const submitInvite = async (page: BrowserPage, dataset: TeamInvitationDataset) => {
  const dialog = await openInviteDialog(page);
  await dialog.getByRole("textbox", { name: /Email address/i }).fill(dataset.email);
  await chooseManager(page, dialog);
  const responsePromise = page.waitForResponse((response: any) => {
    const request = response.request();
    return request.method() === "POST" && new URL(response.url()).pathname === "/api/team/invitations";
  });
  await dialog.getByRole("button", { name: "Send", exact: true }).click();
  const response = await responsePromise;
  assert.ok(response.status() >= 200 && response.status() < 300, "Invitation request must succeed");
  await page.getByText("Invitation sent successfully", { exact: true }).waitFor({ state: "visible" });
  await invitationRow(page, dataset.email).waitFor({ state: "visible" });
};

const ensurePendingInvitation = async (page: BrowserPage, dataset: TeamInvitationDataset) => {
  if (await invitationRow(page, dataset.email).count() === 0) await submitInvite(page, dataset);
  const row = invitationRow(page, dataset.email);
  await row.getByText("Pending", { exact: true }).waitFor({ state: "visible" });
  return row;
};

const maildropMessages = async (mailbox: string): Promise<Array<{ id: string; subject?: string }>> => {
  const response = await fetch("https://api.maildrop.cc/graphql", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: "query Inbox($mailbox: String!) { inbox(mailbox: $mailbox) { id subject } }",
      variables: { mailbox },
    }),
  });
  if (!response.ok) throw new Error(`Maildrop API returned HTTP ${response.status}`);
  const payload = await response.json() as { data?: { inbox?: Array<{ id: string; subject?: string }> }; errors?: unknown };
  if (payload.errors) throw new Error("Maildrop API returned a GraphQL error");
  return payload.data?.inbox || [];
};

const poll = async <T>(read: () => Promise<T>, accept: (value: T) => boolean, timeoutMs = 30_000): Promise<T> => {
  const deadline = Date.now() + timeoutMs;
  let value = await read();
  while (!accept(value) && Date.now() < deadline) {
    await new Promise((done) => setTimeout(done, 1_000));
    value = await read();
  }
  if (!accept(value)) throw new Error("Expected state was not observed before the polling deadline");
  return value;
};

const readInvitations = async (environment: Record<string, string | undefined>): Promise<Invitation[]> => {
  const api = createApiClient(required(environment, "HAIRLINE_API_URL"));
  const token = await api.login({
    email: required(environment, "HAIRLINE_PROVIDER_EMAIL"),
    password: required(environment, "HAIRLINE_PROVIDER_PASSWORD"),
    profileType: "provider",
  });
  const response = await api.get<{ data?: Invitation[] }>("/team/invitations", token);
  return response.data || [];
};

const findInvitation = (invitations: Invitation[], email: string) => invitations.find((item) => item.email === email);

const assertSevenDayExpiry = (expiresAt?: string) => {
  assert.ok(expiresAt, "Pending invitation must expose an expiry timestamp");
  const difference = new Date(expiresAt).getTime() - Date.now();
  const sevenDays = 7 * 24 * 60 * 60 * 1_000;
  assert.ok(Math.abs(difference - sevenDays) < 10 * 60 * 1_000, "Invitation expiry must be seven days from creation");
};

const teamRows = (page: BrowserPage) => page.getByRole("table").first().locator("tbody tr");
const teamSearch = (page: BrowserPage) => page.locator('input[placeholder^="Search"]').first();
const waitForTeamDirectoryReady = async (page: BrowserPage) => {
  await teamRows(page).filter({ hasText: /@/ }).first().waitFor({ state: "visible" });
};
const enterTeamSearch = async (page: BrowserPage, value: string) => {
  const search = teamSearch(page);
  await search.click();
  await search.fill(value);
};

const isTeamMembersResponse = (response: any) => {
  const request = response.request();
  return request.method() === "GET" && new URL(response.url()).pathname === "/api/team/members";
};

const performAndWaitForTeamMembers = async (page: BrowserPage, action: () => Promise<void>) => {
  const responsePromise = page.waitForResponse(isTeamMembersResponse);
  await action();
  const response = await responsePromise;
  assert.ok(response.status() >= 200 && response.status() < 300, "Team member query must succeed");
  return response;
};

const expectTeamEmptyState = async (page: BrowserPage) => {
  await page.getByText(/No team members|No results|No data/i).first().waitFor({ state: "visible" });
};

const openTeamFilter = async (page: BrowserPage) => {
  await page.getByRole("button", { name: "Filter", exact: true }).first().click();
  const panel = page.locator(".ant-modal:visible, .ant-drawer:visible, .ant-popover:visible").last();
  await panel.waitFor({ state: "visible" });
  return panel;
};

const exactText = (value: string) => new RegExp(`^${value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}$`);

const selectTeamFilter = async (page: BrowserPage, panel: any, label: "Role" | "Status" | "Region", value: string) => {
  const accessible = panel.getByRole("combobox", { name: new RegExp(label, "i") });
  if (await accessible.count()) {
    await accessible.first().click({ force: true });
  } else {
    const labelNode = panel.getByText(label, { exact: true });
    await labelNode.waitFor({ state: "visible" });
    const field = labelNode.locator("xpath=ancestor::*[contains(@class,'ant-form-item') or contains(@class,'filter')][1]");
    await field.locator(".ant-select-selector").first().click({ force: true });
  }
  const option = page.locator(".ant-select-dropdown:visible .ant-select-item-option-content")
    .filter({ hasText: exactText(value) });
  await option.waitFor({ state: "visible" });
  await option.click();
  await page.keyboard.press("Escape");
};

const applyTeamFilters = async (
  page: BrowserPage,
  filters: Array<{ label: "Role" | "Status" | "Region"; value?: string }>,
) => {
  const panel = await openTeamFilter(page);
  for (const filter of filters) {
    assert.ok(filter.value, `${filter.label} filter dataset value is required`);
    await selectTeamFilter(page, panel, filter.label, filter.value);
  }
  await performAndWaitForTeamMembers(page, () => (
    panel.getByRole("button", { name: /Apply Filters?|Apply|Filter/i }).last().click()
  ));
};

export const executeBrowserCase = async (
  testCase: RegisteredTeamCase,
  page: BrowserPage,
  dataset: TeamInvitationDataset,
  environment: Record<string, string | undefined>,
): Promise<void> => {
  await openTeam(page, environment);

  switch (testCase.id) {
    case "PR-01-TC-0007":
      assert.match(
        await teamSearch(page).getAttribute("placeholder") || "",
        /^Search team members(?:…|\.\.\.)?$/i,
        "Team search must use the registered Team-specific placeholder",
      );
      await page.getByText("Team Members", { exact: true }).waitFor({ state: "visible" });
      await page.getByText("Invitations", { exact: true }).waitFor({ state: "visible" });
      for (const column of ["Name", "Email", "Role", "Status", "Last Active", "Workload", "Actions"]) {
        await page.getByRole("columnheader", { name: column, exact: true }).first().waitFor({ state: "visible" });
      }
      return;

    case "PR-01-TC-0008": {
      assert.equal(dataset.searchScenarios?.length, 3, "Search dataset requires name, email, and status fixtures");
      const search = teamSearch(page);
      await waitForTeamDirectoryReady(page);
      for (const scenario of dataset.searchScenarios!) {
        await enterTeamSearch(page, scenario.term);
        await teamRows(page).filter({ hasText: scenario.expectedRowText }).first().waitFor({ state: "visible" });
        await search.clear();
        await teamRows(page).first().waitFor({ state: "visible" });
        assert.ok(await teamRows(page).count() > 0, `Clearing ${scenario.criterion} search must restore results`);
      }
      return;
    }

    case "PR-01-TC-0009":
      await openTeamFilter(page);
      for (const control of ["Role", "Status", "Region"]) {
        await page.getByText(control, { exact: true }).last().waitFor({ state: "visible" });
      }
      await page.getByRole("button", { name: /Clear|Reset/ }).last().waitFor({ state: "visible" });
      return;

    case "PR-01-TC-0010": {
      assert.ok((dataset.expectedMemberTotal || 0) >= 25, "Page-size boundary requires at least 25 members");
      const rows = page.getByRole("table").first().locator("tbody tr");
      assert.equal(await rows.count(), 25, "Team directory default page size must be 25");
      return;
    }

    case "PR-01-TC-0011": {
      const dialog = await openInviteDialog(page);
      for (const field of ["First Name", "Last Name", "Email", "Role", "Personal Message"]) {
        await dialog.getByText(field, { exact: false }).first().waitFor({ state: "visible" });
      }
      await dialog.getByText(/seat|team size/i).waitFor({ state: "visible" });
      return;
    }

    case "PR-01-TC-0012": {
      await ensurePendingInvitation(page, dataset);
      const invitation = findInvitation(await readInvitations(environment), dataset.email);
      assert.equal(invitation?.status, "pending");
      assertSevenDayExpiry(invitation?.expires_at);
      const messages = await poll(
        () => maildropMessages(dataset.mailbox),
        (items) => items.some((item) => /team invitation/i.test(item.subject || "")),
      );
      assert.ok(messages.length >= 1);
      return;
    }

    case "PR-01-TC-0013": {
      const dialog = await openInviteDialog(page);
      await dialog.getByRole("textbox", { name: /Email address/i }).fill("not-an-email");
      await chooseManager(page, dialog);
      const invitationRequest = page.waitForRequest((request: any) => (
        request.method() === "POST" && new URL(request.url()).pathname === "/api/team/invitations"
      ), { timeout: 1_500 }).then(() => true).catch(() => false);
      await dialog.getByRole("button", { name: "Send", exact: true }).click();
      await dialog.getByText(/valid email/i).waitFor({ state: "visible" });
      assert.equal(await invitationRequest, false, "Invalid email must be rejected before invitation submission");
      return;
    }

    case "PR-01-TC-0014": {
      await ensurePendingInvitation(page, dataset);
      const dialog = await openInviteDialog(page);
      await dialog.getByRole("textbox", { name: /Email address/i }).fill(dataset.email);
      await chooseManager(page, dialog);
      const duplicateResponse = page.waitForResponse((response: any) => (
        response.request().method() === "POST"
        && new URL(response.url()).pathname === "/api/team/invitations"
      ), { timeout: 5_000 }).catch(() => undefined);
      await dialog.getByRole("button", { name: "Send", exact: true }).click();
      await page.getByText(/already|invited|member/i).last().waitFor({ state: "visible" });
      const response = await duplicateResponse;
      assert.ok(!response || response.status() >= 400, "Duplicate invite must not succeed");
      assert.equal(await invitationRow(page, dataset.email).count(), 1);
      return;
    }

    case "PR-01-TC-0015": {
      const dialog = await openInviteDialog(page);
      await dialog.locator(".ant-select-selector").click({ force: true });
      const options = page.locator(".ant-select-dropdown:visible .ant-select-item-option-content");
      await options.filter({ hasText: /^Manager$/ }).waitFor({ state: "visible" });
      assert.deepEqual(
        (await options.allTextContents()).map((value: string) => value.trim()).sort(),
        ["Billing Staff", "Clinical Staff", "Manager"],
      );
      return;
    }

    case "PR-01-TC-0016": {
      const row = await ensurePendingInvitation(page, dataset);
      for (const action of ["Resend", "Copy Link", "Cancel"]) {
        await row.getByRole("button", { name: action, exact: true }).waitFor({ state: "visible" });
      }
      await page.getByRole("button", { name: /Refresh/ }).waitFor({ state: "visible" });
      return;
    }

    case "PR-01-TC-0017": {
      const row = await ensurePendingInvitation(page, dataset);
      const before = findInvitation(await readInvitations(environment), dataset.email);
      const beforeMessages = await maildropMessages(dataset.mailbox);
      await row.getByRole("button", { name: "Resend", exact: true }).click();
      const refreshed = await poll(
        () => readInvitations(environment),
        (items) => findInvitation(items, dataset.email)?.expires_at !== before?.expires_at,
      );
      const after = findInvitation(refreshed, dataset.email);
      assert.equal(after?.status, "pending");
      assertSevenDayExpiry(after?.expires_at);
      await poll(() => maildropMessages(dataset.mailbox), (items) => items.length > beforeMessages.length);
      return;
    }

    case "PR-01-TC-0018": {
      const row = await ensurePendingInvitation(page, dataset);
      await row.getByRole("button", { name: "Cancel", exact: true }).click();
      await page.getByText("Cancel invitation?", { exact: true }).waitFor({ state: "visible" });
      await page.getByRole("button", { name: "Cancel", exact: true }).last().click();
      await invitationRow(page, dataset.email).waitFor({ state: "hidden" });
      await poll(
        () => readInvitations(environment),
        (items) => !findInvitation(items, dataset.email),
      );
      return;
    }

    case "PR-01-TC-0019": {
      assert.ok(dataset.noMatchSearchTerm, "Unavailable search dataset value is required");
      await waitForTeamDirectoryReady(page);
      await enterTeamSearch(page, dataset.noMatchSearchTerm);
      await expectTeamEmptyState(page);
      return;
    }

    case "PR-01-TC-0020":
      await applyTeamFilters(page, [{ label: "Role", value: dataset.filterRole }]);
      assert.ok(dataset.expectedFilteredRowText, "Role filter requires an expected member");
      await teamRows(page).filter({ hasText: dataset.expectedFilteredRowText }).first().waitFor({ state: "visible" });
      return;

    case "PR-01-TC-0021":
      await applyTeamFilters(page, [{ label: "Status", value: dataset.filterStatus }]);
      assert.ok(dataset.expectedFilteredRowText, "Status filter requires an expected member");
      await teamRows(page).filter({ hasText: dataset.expectedFilteredRowText }).first().waitFor({ state: "visible" });
      return;

    case "PR-01-TC-0022":
      await applyTeamFilters(page, [{ label: "Region", value: dataset.filterRegion }]);
      assert.ok(dataset.expectedFilteredRowText, "Region filter requires an expected member");
      await teamRows(page).filter({ hasText: dataset.expectedFilteredRowText }).first().waitFor({ state: "visible" });
      return;

    case "PR-01-TC-0023":
      await applyTeamFilters(page, [
        { label: "Role", value: dataset.filterRole },
        { label: "Status", value: dataset.filterStatus },
        { label: "Region", value: dataset.filterRegion },
      ]);
      assert.ok(dataset.expectedFilteredRowText, "Combined filters require an expected member");
      await teamRows(page).filter({ hasText: dataset.expectedFilteredRowText }).first().waitFor({ state: "visible" });
      return;

    case "PR-01-TC-0024":
      await applyTeamFilters(page, [
        { label: "Role", value: dataset.filterRole },
        { label: "Status", value: dataset.filterStatus },
        { label: "Region", value: dataset.filterRegion },
      ]);
      await expectTeamEmptyState(page);
      return;

    default:
      throw new Error(`No Team and Invitation automation mapped for ${testCase.id}`);
  }
};
