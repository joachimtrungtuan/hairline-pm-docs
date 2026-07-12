export const resultEnvelopeFixture = {
  schemaVersion: 1,
  run: {
    id: "RUN-20260712T010203Z-a1b2c3d4",
    command: "pnpm test:function P-99 P-99-FN-001",
    environment: "development",
    baseUrl: "https://admin.hairline.app",
    startedAt: "2026-07-12T01:02:03.000Z",
  },
  execution: {
    id: "execution-1",
    caseId: "P-99-TC-0001",
    caseRevision: "v1",
    functionOrFlowId: "P-99-FN-001",
    primaryModuleId: "P-99",
    title: "Authorized provider edits a sent quote",
    registryStatus: "DRAFT",
    outcome: "POTENTIAL_ISSUE",
    reviewStatus: "NEEDS_HUMAN_REVIEW",
    startedAt: "2026-07-12T01:02:04.000Z",
    finishedAt: "2026-07-12T01:02:24.000Z",
    durationMs: 20000,
    finalAttemptNumber: 4,
  },
  attempts: [
    {
      id: "attempt-1",
      number: 1,
      status: "failed",
      errorMessage: "assertion failed",
    },
  ],
};
