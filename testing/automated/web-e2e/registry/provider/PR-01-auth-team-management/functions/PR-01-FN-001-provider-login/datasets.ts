export type ProviderLoginDataset = {
  marker: string;
  username: string;
  password: string;
  role: "provider" | "hairline-team";
};

const required = (environment: Record<string, string | undefined>, key: string): string => {
  const value = environment[key]?.trim();
  if (!value) throw new Error(`Missing registered credential value: ${key}`);
  return value;
};

export const buildProviderLoginDataset = (
  datasetId: string,
  environment: Record<string, string | undefined>,
  runId: string,
): ProviderLoginDataset => {
  const safeRunId = runId.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const marker = `${runId}:${datasetId}`;

  switch (datasetId) {
    case "PR-01-DS-0001":
      return {
        marker,
        username: required(environment, "HAIRLINE_PROVIDER_EMAIL"),
        password: required(environment, "HAIRLINE_PROVIDER_PASSWORD"),
        role: "provider",
      };
    case "PR-01-DS-0002":
      return { marker, username: "", password: "ValidationOnly123!", role: "provider" };
    case "PR-01-DS-0003":
      return { marker, username: `e2e-validation-${safeRunId}@hairline.invalid`, password: "", role: "provider" };
    case "PR-01-DS-0004":
      return { marker, username: "", password: "", role: "provider" };
    case "PR-01-DS-0005":
      return {
        marker,
        username: `e2e-login-${safeRunId}@hairline.invalid`,
        password: "InvalidPass123!",
        role: "provider",
      };
    case "PR-01-DS-0006":
      return {
        marker,
        username: required(environment, "HAIRLINE_RESTRICTED_PROVIDER_EMAIL"),
        password: required(environment, "HAIRLINE_RESTRICTED_PROVIDER_PASSWORD"),
        role: "hairline-team",
      };
    default:
      throw new Error(`Unknown Provider login dataset: ${datasetId}`);
  }
};
