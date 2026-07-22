import { randomUUID } from "node:crypto";
import type { DatabaseSync } from "node:sqlite";

import {
  enumValues,
  statusTaxonomy,
  taxonomyChecksum,
  type DatabaseEnumBinding,
} from "../status-taxonomy.ts";

const hasColumn = (database: DatabaseSync, table: string, column: string): boolean => {
  const rows = database.prepare(`PRAGMA table_info("${table}")`).all() as Array<{ name: string }>;
  return rows.some((row) => row.name === column);
};

const addColumn = (database: DatabaseSync, table: string, definition: string): void => {
  const column = definition.split(/\s+/)[0];
  if (!hasColumn(database, table, column)) {
    database.exec(`ALTER TABLE "${table}" ADD COLUMN ${definition}`);
  }
};

const desiredEnumRows = () => Object.entries(statusTaxonomy.enums)
  .flatMap(([enumName, group]) => [
    ...group.active.map((value) => ({ enumName, value, active: 1 })),
    ...group.inactive.map((value) => ({ enumName, value, active: 0 })),
  ])
  .sort((left, right) => `${left.enumName}:${left.value}`.localeCompare(`${right.enumName}:${right.value}`));

const syncEnumValues = (database: DatabaseSync, timestamp: string): void => {
  const desired = desiredEnumRows();
  const current = (database.prepare(`
    SELECT enum_name AS enumName, value, active
    FROM enum_values
    ORDER BY enum_name, value
  `).all() as Array<{ enumName: string; value: string; active: number }>);
  const latest = database.prepare(`
    SELECT checksum
    FROM enum_taxonomy_syncs
    ORDER BY created_at DESC, id DESC
    LIMIT 1
  `).get() as { checksum?: string } | undefined;

  if (JSON.stringify(current) === JSON.stringify(desired) && latest?.checksum === taxonomyChecksum) return;

  database.prepare("UPDATE enum_values SET active = 0, updated_at = ?").run(timestamp);
  const upsert = database.prepare(`
    INSERT INTO enum_values(enum_name, value, active, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(enum_name, value) DO UPDATE SET
      active = excluded.active,
      updated_at = excluded.updated_at
  `);
  for (const row of desired) {
    upsert.run(row.enumName, row.value, row.active, timestamp, timestamp);
  }

  database.prepare(`
    INSERT INTO enum_taxonomy_syncs(id, taxonomy_version, checksum, created_at)
    VALUES (?, ?, ?, ?)
  `).run(randomUUID(), statusTaxonomy.schemaVersion, taxonomyChecksum, timestamp);
};

const assertPersistedValuesKnown = (database: DatabaseSync, binding: DatabaseEnumBinding): void => {
  const rows = database.prepare(`
    SELECT DISTINCT "${binding.column}" AS value
    FROM "${binding.table}"
    WHERE "${binding.column}" IS NOT NULL
  `).all() as Array<{ value: string }>;
  const known = new Set(enumValues(binding.enum, true));
  const unknown = rows.map((row) => row.value).filter((value) => !known.has(value));
  if (unknown.length > 0) {
    throw new Error(`Unknown persisted ${binding.enum} value(s): ${unknown.join(", ")}`);
  }
};

const installEnumTriggers = (database: DatabaseSync): void => {
  for (const binding of statusTaxonomy.databaseBindings) {
    const triggerBase = `validate_${binding.table}_${binding.column}`;
    const nullCondition = binding.nullable ? `NEW."${binding.column}" IS NOT NULL AND` : "";
    const validation = `${nullCondition} NOT EXISTS (
      SELECT 1 FROM enum_values
      WHERE enum_name = '${binding.enum}'
        AND value = NEW."${binding.column}"
        AND active = 1
    )`;

    database.exec(`
      DROP TRIGGER IF EXISTS "${triggerBase}_insert";
      DROP TRIGGER IF EXISTS "${triggerBase}_update";

      CREATE TRIGGER "${triggerBase}_insert"
      BEFORE INSERT ON "${binding.table}"
      WHEN ${validation}
      BEGIN
        SELECT RAISE(ABORT, 'invalid ${binding.enum} value');
      END;

      CREATE TRIGGER "${triggerBase}_update"
      BEFORE UPDATE OF "${binding.column}" ON "${binding.table}"
      WHEN ${validation}
      BEGIN
        SELECT RAISE(ABORT, 'invalid ${binding.enum} value');
      END;
    `);
  }
};

const installTimestampTriggers = (database: DatabaseSync): void => {
  database.exec(`
    DROP TRIGGER IF EXISTS require_test_run_timestamps;
    DROP TRIGGER IF EXISTS require_attempt_timestamps;
    DROP TRIGGER IF EXISTS require_dataset_timestamps;

    CREATE TRIGGER require_test_run_timestamps
    BEFORE INSERT ON test_runs
    WHEN NEW.finished_at IS NULL OR NEW.duration_ms IS NULL
    BEGIN
      SELECT RAISE(ABORT, 'test run timestamps are required');
    END;

    CREATE TRIGGER require_attempt_timestamps
    BEFORE INSERT ON attempts
    WHEN NEW.started_at IS NULL OR NEW.finished_at IS NULL OR NEW.duration_ms IS NULL
    BEGIN
      SELECT RAISE(ABORT, 'attempt timestamps are required');
    END;

    CREATE TRIGGER require_dataset_timestamps
    BEFORE INSERT ON execution_datasets
    WHEN NEW.started_at IS NULL OR NEW.finished_at IS NULL OR NEW.duration_ms IS NULL
    BEGIN
      SELECT RAISE(ABORT, 'dataset timestamps are required');
    END;
  `);
};

export const migrateStatusTaxonomyAndTimestamps = (database: DatabaseSync): void => {
  const timestamp = new Date().toISOString();
  database.exec("BEGIN IMMEDIATE");
  try {
    database.exec(`
      CREATE TABLE IF NOT EXISTS enum_values (
        enum_name TEXT NOT NULL,
        value TEXT NOT NULL,
        active INTEGER NOT NULL CHECK(active IN (0, 1)),
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        PRIMARY KEY(enum_name, value)
      );
      CREATE TABLE IF NOT EXISTS enum_taxonomy_syncs (
        id TEXT PRIMARY KEY,
        taxonomy_version INTEGER NOT NULL,
        checksum TEXT NOT NULL,
        created_at TEXT NOT NULL
      );
    `);

    addColumn(database, "test_runs", "finished_at TEXT");
    addColumn(database, "test_runs", "duration_ms INTEGER");
    addColumn(database, "attempts", "started_at TEXT");
    addColumn(database, "attempts", "finished_at TEXT");
    addColumn(database, "attempts", "duration_ms INTEGER");
    addColumn(database, "execution_datasets", "started_at TEXT");
    addColumn(database, "execution_datasets", "finished_at TEXT");
    addColumn(database, "execution_datasets", "duration_ms INTEGER");

    syncEnumValues(database, timestamp);
    for (const binding of statusTaxonomy.databaseBindings) {
      assertPersistedValuesKnown(database, binding);
    }
    installEnumTriggers(database);
    installTimestampTriggers(database);

    database.prepare(`
      INSERT OR IGNORE INTO schema_migrations(version, applied_at, checksum)
      VALUES (2, ?, ?)
    `).run(timestamp, "status-taxonomy-and-timestamps-v2");
    database.exec("COMMIT");
  } catch (error) {
    database.exec("ROLLBACK");
    throw error;
  }
};
