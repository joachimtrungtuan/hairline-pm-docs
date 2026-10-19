import { mkdir, rename, rm } from "node:fs/promises";
import { join } from "node:path";

type Capture = (path: string) => Promise<void>;

export const createArtifactManager = (root: string, runId: string, moduleId: string, caseId: string) => {
  const directory = join(root, runId, moduleId, caseId);
  const rollingFailure = join(directory, ".rolling-failure.png");
  const rollingPass = join(directory, ".rolling-pass.png");
  const rollingTrace = join(directory, ".rolling-trace.zip");
  const ensureDirectory = () => mkdir(directory, { recursive: true });
  const moveIfPresent = async (from: string, to: string): Promise<string[]> => {
    try {
      await rename(from, to);
      return [to];
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === "ENOENT") return [];
      throw error;
    }
  };

  return {
    captureFailure: async (capture: Capture) => {
      await ensureDirectory();
      await capture(rollingFailure);
    },
    capturePass: async (capture: Capture) => {
      await ensureDirectory();
      await capture(rollingPass);
    },
    captureTrace: async (capture: Capture) => {
      await ensureDirectory();
      await capture(rollingTrace);
    },
    finalize: async (outcome: string): Promise<string[]> => {
      await ensureDirectory();
      if (outcome === "PASSED") {
        await rm(directory, { recursive: true, force: true });
        return [];
      }
      if (outcome === "FLAKY_OR_TRANSIENT") {
        const failed = join(directory, "flaky-failure.png");
        const passed = join(directory, "flaky-pass.png");
        await rename(rollingFailure, failed);
        await rename(rollingPass, passed);
        const trace = join(directory, "trace.zip");
        return [failed, passed, ...await moveIfPresent(rollingTrace, trace)];
      }
      const final = join(directory, "final-failure.png");
      await rename(rollingFailure, final);
      await rm(rollingPass, { force: true });
      const trace = join(directory, "trace.zip");
      return [final, ...await moveIfPresent(rollingTrace, trace)];
    },
  };
};
