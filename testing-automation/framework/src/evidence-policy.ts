import type { PreliminaryOutcome } from "./retry-outcome.ts";

export type EvidencePlan = {
  screenshots: string[];
  retainTrace: boolean;
  rollingFailureScreenshot: boolean;
};

export const evidencePlan = (
  outcome: PreliminaryOutcome,
): EvidencePlan => {
  if (outcome === "PASSED") {
    return {
      screenshots: [],
      retainTrace: false,
      rollingFailureScreenshot: false,
    };
  }

  if (outcome === "FLAKY_OR_TRANSIENT") {
    return {
      screenshots: ["flaky-failure.png", "flaky-pass.png"],
      retainTrace: true,
      rollingFailureScreenshot: true,
    };
  }

  return {
    screenshots: ["final-failure.png"],
    retainTrace: true,
    rollingFailureScreenshot: true,
  };
};
