import assert from "node:assert/strict";
import test from "node:test";

import {
  checksumEnvelope,
  redactSecrets,
  validateEnvelope,
} from "../framework/src/envelope.ts";
import { resultEnvelopeFixture as envelope } from "./fixtures.ts";

test("validates a versioned result envelope", () => {
  assert.equal(validateEnvelope(envelope).execution.caseId, "P-99-TC-0001");
});

test("rejects an envelope with an invalid case identifier", () => {
  assert.throws(
    () => validateEnvelope({
      ...envelope,
      execution: { ...envelope.execution, caseId: "PR02-TC-1" },
    }),
    /caseId/,
  );
});

test("redacts nested credentials before persistence", () => {
  const redacted = redactSecrets({
    authorization: "Bearer secret-token",
    request: {
      password: "password",
      token: "abc",
      normal: "retained",
    },
  });

  assert.deepEqual(redacted, {
    authorization: "[REDACTED]",
    request: {
      password: "[REDACTED]",
      token: "[REDACTED]",
      normal: "retained",
    },
  });
});

test("produces a stable checksum independent of object key order", () => {
  assert.equal(
    checksumEnvelope({ a: 1, nested: { b: 2, c: 3 } }),
    checksumEnvelope({ nested: { c: 3, b: 2 }, a: 1 }),
  );
});
