export type RegisteredCase = {
  id: string;
  revision: string;
  functionId: string;
  moduleId: string;
  title: string;
  datasetId: string;
  status: "DRAFT" | "ACTIVE";
  requiredRole: string;
  automationModule: string;
};

export type RegisteredModule = {
  id: string;
  title: string;
  tenant: "Provider" | "Admin";
};

export type RegisteredScope = {
  id: string;
  moduleId: string;
  title: string;
  kind: "FUNCTION" | "FLOW";
  runnerScript: "test:function" | "test:flow";
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
}];

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
