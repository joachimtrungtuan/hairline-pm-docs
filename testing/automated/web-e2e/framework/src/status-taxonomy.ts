import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

type EnumGroup = {
  active: string[];
  inactive: string[];
};

export type DatabaseEnumBinding = {
  table: string;
  column: string;
  enum: string;
  nullable: boolean;
};

type StatusTaxonomy = {
  schemaVersion: number;
  enums: Record<string, EnumGroup>;
  databaseBindings: DatabaseEnumBinding[];
};

const taxonomyPath = resolve(import.meta.dirname, "../../status-taxonomy.json");
const source = readFileSync(taxonomyPath, "utf8");
const taxonomy = JSON.parse(source) as StatusTaxonomy;
const identifier = /^[a-z][a-z0-9_]*$/i;

const assertIdentifier = (value: string): void => {
  if (!identifier.test(value)) throw new Error(`Unsafe taxonomy identifier: ${value}`);
};

const validateTaxonomy = (): void => {
  if (taxonomy.schemaVersion !== 1) throw new Error("Unsupported status taxonomy version");

  for (const [name, group] of Object.entries(taxonomy.enums)) {
    assertIdentifier(name);
    if (!Array.isArray(group.active) || !Array.isArray(group.inactive)) {
      throw new Error(`Enum ${name} must define active and inactive arrays`);
    }
    const values = [...group.active, ...group.inactive];
    if (values.some((value) => typeof value !== "string" || value.length === 0)) {
      throw new Error(`Enum ${name} contains an invalid value`);
    }
    if (values.length !== new Set(values).size) throw new Error(`Duplicate value in enum ${name}`);
  }

  for (const binding of taxonomy.databaseBindings) {
    assertIdentifier(binding.table);
    assertIdentifier(binding.column);
    assertIdentifier(binding.enum);
    if (!taxonomy.enums[binding.enum]) throw new Error(`Unknown bound enum: ${binding.enum}`);
  }
};

validateTaxonomy();

export const statusTaxonomy = Object.freeze(taxonomy);
export const taxonomyChecksum = createHash("sha256").update(source).digest("hex");

export const enumValues = (enumName: string, includeInactive = false): readonly string[] => {
  const group = taxonomy.enums[enumName];
  if (!group) throw new Error(`Unknown enum: ${enumName}`);
  return includeInactive ? [...group.active, ...group.inactive] : [...group.active];
};

export const assertEnumValue = (
  enumName: string,
  value: unknown,
  options: { allowInactive?: boolean } = {},
): string => {
  if (typeof value !== "string") throw new Error(`${enumName} must be a string`);
  const group = taxonomy.enums[enumName];
  if (!group) throw new Error(`Unknown enum: ${enumName}`);
  if (group.active.includes(value)) return value;
  if (options.allowInactive && group.inactive.includes(value)) return value;
  throw new Error(`Invalid active ${enumName}: ${value}`);
};
