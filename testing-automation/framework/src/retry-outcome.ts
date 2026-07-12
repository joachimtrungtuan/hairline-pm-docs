export type Attempt = {
  status: "passed" | "failed";
  signature?: string;
};

export type PreliminaryOutcome =
  | "PASSED"
  | "FLAKY_OR_TRANSIENT"
  | "POTENTIAL_ISSUE"
  | "INCONSISTENT_FAILURE";

export type ReviewStatus =
  | "REVIEW_NOT_REQUIRED"
  | "NEEDS_HUMAN_REVIEW";

export type OutcomeResult = {
  outcome: PreliminaryOutcome;
  reviewStatus: ReviewStatus;
};

const errorSignature = (error: unknown): string => {
  if (error instanceof Error) return `${error.name}:${error.message}`;
  return String(error);
};

export const deriveOutcome = (attempts: Attempt[]): OutcomeResult => {
  const passedIndex = attempts.findIndex((attempt) => attempt.status === "passed");

  if (passedIndex === 0) {
    return { outcome: "PASSED", reviewStatus: "REVIEW_NOT_REQUIRED" };
  }

  if (passedIndex > 0) {
    return {
      outcome: "FLAKY_OR_TRANSIENT",
      reviewStatus: "NEEDS_HUMAN_REVIEW",
    };
  }

  const signatures = new Set(attempts.map((attempt) => attempt.signature));
  if (signatures.size > 1) {
    return {
      outcome: "INCONSISTENT_FAILURE",
      reviewStatus: "NEEDS_HUMAN_REVIEW",
    };
  }

  return {
    outcome: "POTENTIAL_ISSUE",
    reviewStatus: "NEEDS_HUMAN_REVIEW",
  };
};

export const executeWithRetries = async <T>(
  operation: () => Promise<T>,
  wait: (milliseconds: number) => Promise<void>,
): Promise<OutcomeResult & { attempts: Attempt[]; value?: T }> => {
  const attempts: Attempt[] = [];

  for (let attemptNumber = 1; attemptNumber <= 4; attemptNumber += 1) {
    try {
      const value = await operation();
      attempts.push({ status: "passed" });
      return { ...deriveOutcome(attempts), attempts, value };
    } catch (error) {
      attempts.push({ status: "failed", signature: errorSignature(error) });
      if (attemptNumber < 4) await wait(5000);
    }
  }

  return { ...deriveOutcome(attempts), attempts };
};
