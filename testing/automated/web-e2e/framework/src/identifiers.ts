const MODULE = "(?:P|PR|A|S)-\\d{2}[a-z]?";

const FUNCTION_ID = new RegExp(`^${MODULE}-FN-\\d{3}$`);
const TEST_CASE_ID = new RegExp(`^${MODULE}-TC-\\d{4}$`);
const DATASET_ID = new RegExp(`^${MODULE}-DS-\\d{4}$`);

export const isFunctionId = (value: string): boolean =>
  FUNCTION_ID.test(value);

export const isTestCaseId = (value: string): boolean =>
  TEST_CASE_ID.test(value);

export const isDatasetId = (value: string): boolean =>
  DATASET_ID.test(value);
