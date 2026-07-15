import {
  listRegisteredCases,
  listRegisteredModules,
  listRegisteredScopes,
  type RegisteredCase,
  type RegisteredModule,
  type RegisteredScope,
} from "./case-registry.ts";

export type MenuScope = RegisteredScope & {
  activeCases: RegisteredCase[];
};

export type MenuModule = RegisteredModule & {
  scopes: MenuScope[];
};

export type RunInvocation = {
  command: "pnpm";
  args: string[];
  environment: Record<string, string>;
};

export const getMenuCatalog = (): MenuModule[] => {
  const cases = listRegisteredCases();
  const scopes = listRegisteredScopes().map((scope): MenuScope => ({
    ...scope,
    activeCases: cases.filter((testCase) => (
      testCase.moduleId === scope.moduleId
      && testCase.functionId === scope.id
      && testCase.status === "ACTIVE"
    )),
  })).filter((scope) => scope.activeCases.length > 0);

  return listRegisteredModules().map((module): MenuModule => ({
    ...module,
    scopes: scopes.filter((scope) => scope.moduleId === module.id),
  })).filter((module) => module.scopes.length > 0);
};

export const buildRunInvocation = (
  scope: MenuScope,
  options: { caseId?: string; headless: boolean },
): RunInvocation => {
  if (options.caseId && !scope.activeCases.some((testCase) => testCase.id === options.caseId)) {
    throw new Error(`${options.caseId} is not an active case in ${scope.id}`);
  }

  const args = [scope.runnerScript, scope.moduleId, scope.id];
  if (options.caseId) args.push("--case", options.caseId);
  return {
    command: "pnpm",
    args,
    environment: options.headless ? { HAIRLINE_HEADLESS: "true" } : {},
  };
};
