import { assertEnumValue } from "./status-taxonomy.ts";

export type RegisteredCase = {
  id: string;
  revision: string;
  functionId: string;
  moduleId: string;
  title: string;
  datasetId: string;
  status: string;
  requiredRole: string;
  automationModule: string;
};

export type RegisteredModule = {
  id: string;
  title: string;
  tenant: string;
};

export type RegisteredScope = {
  id: string;
  moduleId: string;
  title: string;
  kind: string;
  runnerScript: string;
  coverageGapCount: number;
};

const modules: RegisteredModule[] = [{
  id: "PR-01",
  title: "Auth & Team Management",
  tenant: "Provider",
}];

const scopes: RegisteredScope[] = [{
  id: "PR-01-FN-001",
  moduleId: "PR-01",
  title: "Provider login",
  kind: "FUNCTION",
  runnerScript: "test:function",
  coverageGapCount: 4,
}, {
  id: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Team directory and invitation management",
  kind: "FUNCTION",
  runnerScript: "test:function",
  coverageGapCount: 9,
}];

const cases: RegisteredCase[] = [{
  id: "PR-01-TC-0001",
  revision: "v1",
  functionId: "PR-01-FN-001",
  moduleId: "PR-01",
  title: "Active Provider successfully logs in",
  datasetId: "PR-01-DS-0001",
  status: "ACTIVE",
  requiredRole: "provider",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-001-provider-login/tests.spec.ts",
}, {
  id: "PR-01-TC-0002",
  revision: "v1",
  functionId: "PR-01-FN-001",
  moduleId: "PR-01",
  title: "Provider login requires a username",
  datasetId: "PR-01-DS-0002",
  status: "ACTIVE",
  requiredRole: "provider",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-001-provider-login/tests.spec.ts",
}, {
  id: "PR-01-TC-0003",
  revision: "v1",
  functionId: "PR-01-FN-001",
  moduleId: "PR-01",
  title: "Provider login requires a password",
  datasetId: "PR-01-DS-0003",
  status: "ACTIVE",
  requiredRole: "provider",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-001-provider-login/tests.spec.ts",
}, {
  id: "PR-01-TC-0004",
  revision: "v1",
  functionId: "PR-01-FN-001",
  moduleId: "PR-01",
  title: "Provider login reports both required fields when empty",
  datasetId: "PR-01-DS-0004",
  status: "ACTIVE",
  requiredRole: "provider",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-001-provider-login/tests.spec.ts",
}, {
  id: "PR-01-TC-0005",
  revision: "v1",
  functionId: "PR-01-FN-001",
  moduleId: "PR-01",
  title: "Unknown Provider credentials are rejected safely",
  datasetId: "PR-01-DS-0005",
  status: "ACTIVE",
  requiredRole: "provider",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-001-provider-login/tests.spec.ts",
}, {
  id: "PR-01-TC-0006",
  revision: "v1",
  functionId: "PR-01-FN-001",
  moduleId: "PR-01",
  title: "Provider credentials cannot authenticate as Hairline Team",
  datasetId: "PR-01-DS-0006",
  status: "ACTIVE",
  requiredRole: "provider",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-001-provider-login/tests.spec.ts",
}, {
  id: "PR-01-TC-0007",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Authorized Provider can access Team and Invitations",
  datasetId: "PR-01-DS-0007",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0008",
  revision: "v2",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Team search returns matches for name email and status",
  datasetId: "PR-01-DS-0008",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0009",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Team directory filters expose role status and region controls",
  datasetId: "PR-01-DS-0009",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0010",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Team directory uses the required default page size",
  datasetId: "PR-01-DS-0010",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0011",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Invite form exposes the complete PRD field contract",
  datasetId: "PR-01-DS-0011",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0012",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Provider invites a Manager with fresh Maildrop delivery",
  datasetId: "PR-01-DS-0012",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0013",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Invite form rejects an invalid email without submission",
  datasetId: "PR-01-DS-0013",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0014",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Duplicate invitation within the Provider is blocked",
  datasetId: "PR-01-DS-0014",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0015",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Invitation role choices exclude Owner",
  datasetId: "PR-01-DS-0015",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0016",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Pending invitation exposes governed management actions",
  datasetId: "PR-01-DS-0016",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0017",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Resending a pending invitation refreshes expiry and email",
  datasetId: "PR-01-DS-0017",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0018",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Cancelling a pending invitation requires confirmation",
  datasetId: "PR-01-DS-0018",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0019",
  revision: "v2",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Team search shows an empty state for an unavailable value",
  datasetId: "PR-01-DS-0019",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0020",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Role filter returns an available team member",
  datasetId: "PR-01-DS-0020",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0021",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Status filter returns an available team member",
  datasetId: "PR-01-DS-0021",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0022",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Region filter returns an available team member",
  datasetId: "PR-01-DS-0022",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0023",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Role status and region filters return their shared match",
  datasetId: "PR-01-DS-0023",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}, {
  id: "PR-01-TC-0024",
  revision: "v1",
  functionId: "PR-01-FN-002",
  moduleId: "PR-01",
  title: "Valid combined filters show an empty state when no member matches",
  datasetId: "PR-01-DS-0024",
  status: "DRAFT",
  requiredRole: "provider-owner-or-manager",
  automationModule: "registry/provider/PR-01-auth-team-management/functions/PR-01-FN-002-team-directory-invitation-management/tests.spec.ts",
}];

for (const module of modules) assertEnumValue("tenant", module.tenant);
for (const scope of scopes) {
  assertEnumValue("scopeKind", scope.kind);
  assertEnumValue("runnerScript", scope.runnerScript);
}
for (const testCase of cases) assertEnumValue("registryStatus", testCase.status);

export const listRegisteredCases = (): readonly RegisteredCase[] => cases;
export const listRegisteredModules = (): readonly RegisteredModule[] => modules;
export const listRegisteredScopes = (): readonly RegisteredScope[] => scopes;

export const selectCases = (moduleId: string, functionId: string, caseId?: string): RegisteredCase[] => {
  const selected = cases.filter((item) => item.moduleId === moduleId && item.functionId === functionId);
  if (selected.length === 0) throw new Error(`Unknown function: ${moduleId}/${functionId}`);
  if (!caseId) return selected;
  const narrowed = selected.filter((item) => item.id === caseId);
  if (narrowed.length === 0) throw new Error(`Unknown case: ${caseId}`);
  return narrowed;
};
