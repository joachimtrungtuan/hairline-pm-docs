import { createHash } from "node:crypto";

import { createApiClient } from "../../../../../framework/src/api-client.ts";

export type TeamInvitationDataset = {
  marker: string;
  email: string;
  mailbox: string;
  role: "manager";
  searchScenarios?: Array<{ criterion: "name" | "email" | "status"; term: string; expectedRowText: string }>;
  noMatchSearchTerm?: string;
  filterRole?: string;
  filterStatus?: string;
  filterRegion?: string;
  expectedFilteredRowText?: string;
  expectedMemberTotal?: number;
};

export type TeamMemberRecord = {
  first_name?: string;
  last_name?: string;
  email?: string;
  role_name?: string;
  status?: string;
  region?: unknown;
  region_name?: string;
  user?: {
    roles?: Array<{ name?: string; display_name?: string }>;
    region?: unknown;
    region_name?: string;
  };
};

type MemberResponse = {
  data?: {
    data?: TeamMemberRecord[];
    total?: number;
  };
};

type FilterFixture = {
  role?: string;
  status?: string;
  region?: string;
  rowText: string;
};

const required = (environment: Record<string, string | undefined>, key: string): string => {
  const value = environment[key]?.trim();
  if (!value) throw new Error(`Missing registered credential value: ${key}`);
  return value;
};

const mailboxFor = (runId: string, datasetId: string): string => {
  const digest = createHash("sha256").update(`${runId}:${datasetId}`).digest("hex").slice(0, 20);
  return `hl-pr01-${digest}`;
};

const asLabel = (value: unknown): string | undefined => {
  if (typeof value === "string" && value.trim()) return value.trim();
  if (value && typeof value === "object") {
    for (const key of ["label", "name", "display_name"]) {
      const candidate = (value as Record<string, unknown>)[key];
      if (typeof candidate === "string" && candidate.trim()) return candidate.trim();
    }
  }
  return undefined;
};

const statusLabel = (status?: string): string | undefined => {
  if (!status) return undefined;
  const normalized = status.trim().toLowerCase().replace(/[ _-]+/g, "_");
  if (normalized === "pending" || normalized === "invited" || normalized === "pending_invitation") return "Pending Invitation";
  if (normalized === "active") return "Active";
  if (normalized === "inactive") return "Inactive";
  return status.trim().replace(/[ _-]+/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
};

const filterStatusLabel = (status?: string): string | undefined => {
  const label = statusLabel(status);
  return label && ["Active", "Inactive", "Pending Invitation"].includes(label) ? label : undefined;
};

const memberFixture = (member: TeamMemberRecord): FilterFixture => ({
  role: member.role_name?.trim()
    || member.user?.roles?.map((role) => role.display_name || role.name).find(Boolean)?.trim(),
  status: filterStatusLabel(member.status),
  region: member.region_name?.trim()
    || asLabel(member.region)
    || member.user?.region_name?.trim()
    || asLabel(member.user?.region),
  rowText: member.email?.trim() || `${member.first_name || ""} ${member.last_name || ""}`.trim(),
});

export const deriveTeamFilterFixtures = (members: TeamMemberRecord[]) => {
  const fixtures = members.map(memberFixture).filter((fixture) => fixture.rowText);
  const role = fixtures.find((fixture) => fixture.role);
  const status = fixtures.find((fixture) => fixture.status);
  const region = fixtures.find((fixture) => fixture.region);
  const combined = fixtures.find((fixture) => fixture.role && fixture.status && fixture.region);
  const roles = [...new Set(fixtures.map((fixture) => fixture.role).filter(Boolean))] as string[];
  const statuses = [...new Set(fixtures.map((fixture) => fixture.status).filter(Boolean))] as string[];
  const regions = [...new Set(fixtures.map((fixture) => fixture.region).filter(Boolean))] as string[];
  let unavailable: FilterFixture | undefined;

  for (const candidateRole of roles) {
    for (const candidateStatus of statuses) {
      for (const candidateRegion of regions) {
        if (!fixtures.some((fixture) => (
          fixture.role === candidateRole
          && fixture.status === candidateStatus
          && fixture.region === candidateRegion
        ))) {
          unavailable = {
            role: candidateRole,
            status: candidateStatus,
            region: candidateRegion,
            rowText: "",
          };
          break;
        }
      }
      if (unavailable) break;
    }
    if (unavailable) break;
  }

  return { role, status, region, combined, unavailable };
};

export const buildTeamInvitationDataset = async (
  datasetId: string,
  environment: Record<string, string | undefined>,
  runId: string,
): Promise<TeamInvitationDataset> => {
  const sequence = Number(datasetId.slice(-4));
  if (!Number.isInteger(sequence) || sequence < 7 || sequence > 24) {
    throw new Error(`Unknown Team and Invitation dataset: ${datasetId}`);
  }

  const publicMailboxMutationDatasets = new Set([
    "PR-01-DS-0012",
    "PR-01-DS-0014",
    "PR-01-DS-0016",
    "PR-01-DS-0017",
    "PR-01-DS-0018",
  ]);
  if (publicMailboxMutationDatasets.has(datasetId) && environment.HAIRLINE_ALLOW_PUBLIC_INVITE_MAILBOX !== "true") {
    throw new Error(
      "Public Maildrop invitation is disabled: set HAIRLINE_ALLOW_PUBLIC_INVITE_MAILBOX=true only after human acceptance of public invitation-link exposure",
    );
  }

  const mailbox = mailboxFor(runId, datasetId);
  const dataset: TeamInvitationDataset = {
    marker: `${runId}:${datasetId}`,
    email: `${mailbox}@maildrop.cc`,
    mailbox,
    role: "manager",
  };

  if (datasetId === "PR-01-DS-0019") {
    dataset.noMatchSearchTerm = `no-team-member-${createHash("sha256").update(`${runId}:${datasetId}`).digest("hex").slice(0, 16)}`;
  }

  const memberDatasetIds = new Set([
    "PR-01-DS-0008",
    "PR-01-DS-0010",
    "PR-01-DS-0020",
    "PR-01-DS-0021",
    "PR-01-DS-0022",
    "PR-01-DS-0023",
    "PR-01-DS-0024",
  ]);
  if (memberDatasetIds.has(datasetId)) {
    const api = createApiClient(required(environment, "HAIRLINE_API_URL"));
    const token = await api.login({
      email: required(environment, "HAIRLINE_PROVIDER_EMAIL"),
      password: required(environment, "HAIRLINE_PROVIDER_PASSWORD"),
      profileType: "provider",
    });
    const response = await api.get<MemberResponse>("/team/members?per_page=1000", token);
    const members = response.data?.data || [];
    dataset.expectedMemberTotal = response.data?.total;

    if (datasetId === "PR-01-DS-0008") {
      const nameMember = members.find((member) => (member.first_name || member.last_name) && member.email);
      const emailMember = members.find((member) => member.email);
      const statusMember = members.find((member) => member.status && member.email);
      if (!nameMember || !emailMember || !statusMember) {
        throw new Error("Team member setup did not return deterministic name, email, and status search fixtures");
      }
      dataset.searchScenarios = [{
        criterion: "name",
        term: `${nameMember.first_name || ""} ${nameMember.last_name || ""}`.trim(),
        expectedRowText: nameMember.email!,
      }, {
        criterion: "email",
        term: emailMember.email!,
        expectedRowText: emailMember.email!,
      }, {
        criterion: "status",
        term: statusLabel(statusMember.status)!,
        expectedRowText: statusMember.email!,
      }];
    }

    const filters = deriveTeamFilterFixtures(members);
    const selected = datasetId === "PR-01-DS-0020" ? filters.role
      : datasetId === "PR-01-DS-0021" ? filters.status
        : datasetId === "PR-01-DS-0022" ? filters.region
          : datasetId === "PR-01-DS-0023" ? filters.combined
            : datasetId === "PR-01-DS-0024" ? filters.unavailable
              : undefined;
    if (datasetId.startsWith("PR-01-DS-002") && !selected) {
      throw new Error(`Team member setup cannot derive deterministic filter fixture for ${datasetId}`);
    }
    if (selected) {
      dataset.filterRole = selected.role;
      dataset.filterStatus = selected.status;
      dataset.filterRegion = selected.region;
      dataset.expectedFilteredRowText = selected.rowText || undefined;
    }
  }

  return dataset;
};
