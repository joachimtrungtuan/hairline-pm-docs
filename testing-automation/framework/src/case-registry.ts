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

const cases: RegisteredCase[] = [];

export const listRegisteredCases = (): readonly RegisteredCase[] => cases;

export const selectCases = (moduleId: string, functionId: string, caseId?: string): RegisteredCase[] => {
  const selected = cases.filter((item) => item.moduleId === moduleId && item.functionId === functionId);
  if (selected.length === 0) throw new Error(`Unknown function: ${moduleId}/${functionId}`);
  if (!caseId) return selected;
  const narrowed = selected.filter((item) => item.id === caseId);
  if (narrowed.length === 0) throw new Error(`Unknown case: ${caseId}`);
  return narrowed;
};
