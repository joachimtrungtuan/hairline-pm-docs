"""Tests for the cross-FR consistency checks."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import consistency
import init_db
import query
from common import connect


class ConsistencyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self._tmp.name) / "graph.db"
        init_db.init_db(self.db_path)
        self.conn = connect(self.db_path)
        for fr in ("FR-001", "FR-002"):
            self.node(fr, "FR")
        self.stage("STG-main-01-inquiry", "main", 1)
        self.stage("STG-main-02-quote", "main", 2)
        self.stage("STG-aftercare-01-plan", "aftercare", 1)

    def tearDown(self) -> None:
        self.conn.close()
        self._tmp.cleanup()

    def node(self, node_id: str, node_type: str, owner: str | None = None, title: str | None = None,
             status: str = "active", **attrs: Any) -> str:
        self.conn.execute("INSERT INTO nodes (id, type, owner_fr, title, status, attrs) VALUES (?, ?, ?, ?, ?, ?)",
                          (node_id, node_type, owner, title or node_id, status, json.dumps(attrs)))
        return node_id

    def stage(self, stage_id: str, timeline: str, sequence: int) -> str:
        return self.node(stage_id, "Stage", timeline=timeline, sequence=sequence)

    def field(self, entity_id: str, name: str, owner: str) -> str:
        field_id = self.node(f"{entity_id}.{name}", "Field", owner)
        self.conn.execute("INSERT INTO fields (id, entity_id, name, data_type) VALUES (?, ?, ?, 'text')",
                          (field_id, entity_id, name))
        return field_id

    def edge(self, from_id: str, verb: str, to_id: str) -> None:
        self.conn.execute("INSERT INTO edges (from_id, verb, to_id) VALUES (?, ?, ?)", (from_id, verb, to_id))

    def rule(self, rule_id: str, owner: str, **attrs: Any) -> str:
        return self.node(rule_id, "Rule", owner, statement="A statement", **attrs)

    def kinds(self, check: str) -> list[str]:
        return [row["kind"] for row in consistency.CHECKS[check](self.conn)[1]]


class TestBoundary(ConsistencyTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.node("ENT-quote", "Entity", "FR-002")
        self.price = self.field("ENT-quote", "price", "FR-002")
        self.node("SCR-001-01", "Screen", "FR-001")
        self.edge("SCR-001-01", "shows", self.price)
        self.rule("REQ-001-001", "FR-001")
        self.edge("REQ-001-001", "applies to", "ENT-quote")
        self.rule("REQ-002-001", "FR-002")

    def test_cross_fr_links_without_reference_are_reported_per_fr_pair(self) -> None:
        rows = consistency.boundary(self.conn)[1]
        self.assertEqual([(r["kind"], r["from_fr"], r["data_owner_fr"], r["links"]) for r in rows],
                         [("rule applies to data", "FR-001", "FR-002", 1), ("screen shows field", "FR-001", "FR-002", 1)])
        self.assertEqual(rows[1]["sample"], ["SCR-001-01 shows ENT-quote.price"])

    def test_references_edge_clears_the_pair(self) -> None:
        self.edge("FR-001", "references", "REQ-002-001")
        self.assertEqual(consistency.boundary(self.conn)[1], [])

    def test_same_fr_and_retired_nodes_are_ignored(self) -> None:
        self.node("SCR-002-01", "Screen", "FR-002")
        self.edge("SCR-002-01", "shows", self.price)
        self.node("SCR-001-02", "Screen", "FR-001", status="retired")
        self.edge("SCR-001-02", "shows", self.price)
        self.assertEqual([r["links"] for r in consistency.boundary(self.conn)[1]], [1, 1])


class TestOwnership(ConsistencyTestCase):
    def test_same_name_or_table_with_two_owners(self) -> None:
        self.node("ENT-quote", "Entity", "FR-001", "Quote", table="quotes")
        self.node("ENT-quotes", "Entity", "FR-002", "quote", table="quotes")
        self.node("SET-max-files", "Setting", "FR-001", "Max files")
        self.node("SET-max-files-b", "Setting", "FR-001", "Max-Files")
        rows = consistency.ownership(self.conn)[1]
        self.assertEqual([(r["kind"], r["type"], r["owners"]) for r in rows], [
            ("same name, different owners", "Entity", ["FR-001", "FR-002"]),
            ("same table, different owners", "Entity", ["FR-001", "FR-002"])])

    def test_field_owned_apart_from_its_entity(self) -> None:
        self.node("ENT-quote", "Entity", "FR-001")
        self.field("ENT-quote", "price", "FR-002")
        self.field("ENT-quote", "total", "FR-001")
        rows = consistency.ownership(self.conn)[1]
        self.assertEqual([(r["kind"], r["name"]) for r in rows],
                         [("field owner differs from entity owner", "ENT-quote.price")])


class TestFlow(ConsistencyTestCase):
    def test_event_with_no_consuming_rule(self) -> None:
        self.node("EVT-quote-sent", "Event", "FR-001")
        self.edge("STG-main-02-quote", "emits", "EVT-quote-sent")
        self.assertIn("event emitted, no rule applies to it", self.kinds("flow"))
        self.rule("REQ-001-001", "FR-001")
        self.edge("REQ-001-001", "applies to", "EVT-quote-sent")
        self.assertNotIn("event emitted, no rule applies to it", self.kinds("flow"))

    def test_event_consumed_only_at_an_earlier_stage(self) -> None:
        self.node("EVT-quote-sent", "Event", "FR-001")
        self.edge("STG-main-02-quote", "emits", "EVT-quote-sent")
        self.rule("REQ-001-001", "FR-001")
        self.edge("REQ-001-001", "applies to", "EVT-quote-sent")
        self.edge("REQ-001-001", "applies at", "STG-main-01-inquiry")
        self.assertIn("event consumed only at earlier stages", self.kinds("flow"))
        self.edge("REQ-001-001", "applies at", "STG-aftercare-01-plan")
        self.assertNotIn("event consumed only at earlier stages", self.kinds("flow"))

    def test_entity_read_write_gaps(self) -> None:
        for name in ("written", "read", "idle", "early", "fine"):
            self.node(f"ENT-{name}", "Entity", "FR-001")
        self.edge("STG-main-01-inquiry", "writes", "ENT-written")
        self.edge("STG-main-01-inquiry", "reads", "ENT-read")
        self.edge("STG-main-01-inquiry", "reads", "ENT-early")
        self.edge("STG-main-02-quote", "writes", "ENT-early")
        self.edge("STG-main-01-inquiry", "writes", "ENT-fine")
        self.edge("STG-main-02-quote", "reads", "ENT-fine")
        rows = {r["node"]: r["kind"] for r in consistency.flow(self.conn)[1] if r["node"].startswith("ENT-")}
        self.assertEqual(rows, {
            "ENT-written": "entity written, never read",
            "ENT-read": "entity read, never written",
            "ENT-idle": "entity neither read nor written at any stage",
            "ENT-early": "entity read only before it is written"})

    def test_stage_that_reads_nothing(self) -> None:
        self.node("ENT-quote", "Entity", "FR-001")
        self.edge("STG-main-01-inquiry", "reads", "ENT-quote")
        self.edge("STG-main-02-quote", "writes", "ENT-quote")
        rows = [r for r in consistency.flow(self.conn)[1] if r["kind"] == "stage reads no data"]
        self.assertEqual([r["node"] for r in rows], ["STG-aftercare-01-plan", "STG-main-02-quote"])
        self.assertEqual(rows[1]["detail"], ["writes 1", "emits 0", "rules 0"])


class TestJoins(ConsistencyTestCase):
    def setUp(self) -> None:
        super().setUp()
        for name in ("booking", "plan", "orphan"):
            self.node(f"ENT-{name}", "Entity", "FR-001")
        self.edge("STG-aftercare-01-plan", "enters from", "STG-main-02-quote")

    def test_entry_reads_must_be_written_upstream(self) -> None:
        self.edge("STG-main-01-inquiry", "writes", "ENT-booking")
        self.edge("STG-aftercare-01-plan", "writes", "ENT-plan")
        for name in ("booking", "plan", "orphan"):
            self.edge("STG-aftercare-01-plan", "reads", f"ENT-{name}")
        rows = consistency.joins(self.conn)[1]
        self.assertEqual([(r["kind"], r["entity"]) for r in rows],
                         [("read at entry, not written upstream", "ENT-orphan")])

    def test_entry_that_reads_nothing(self) -> None:
        self.assertEqual(self.kinds("joins"), ["entry stage reads no data"])

    def test_join_must_carry_data_the_joined_stage_reads(self) -> None:
        self.edge("STG-aftercare-01-plan", "reads", "ENT-plan")
        self.edge("STG-aftercare-01-plan", "writes", "ENT-plan")
        self.edge("STG-aftercare-01-plan", "joins", "STG-main-01-inquiry")
        self.assertEqual(self.kinds("joins"), ["join carries no data the joined stage reads"])
        self.edge("STG-main-01-inquiry", "reads", "ENT-plan")
        self.assertEqual(self.kinds("joins"), [])


class TestCoverage(ConsistencyTestCase):
    def test_missing_actor_and_stage_links(self) -> None:
        self.node("ACT-patient", "Actor", group="patient")
        self.node("SCR-001-01", "Screen", "FR-001")
        self.node("SCR-001-02", "Screen", "FR-001")
        self.edge("ACT-patient", "uses", "SCR-001-01")
        self.edge("ACT-patient", "acts in", "STG-main-01-inquiry")
        self.edge("ACT-patient", "acts in", "STG-main-02-quote")
        self.rule("REQ-001-001", "FR-001")
        self.rule("REQ-001-002", "FR-001", scope="global")
        self.rule("REQ-001-003", "FR-001")
        self.edge("REQ-001-003", "applies at", "STG-main-01-inquiry")
        rows = consistency.coverage(self.conn)[1]
        self.assertEqual([(r["kind"], r["node"]) for r in rows], [
            ("screen without actor", "SCR-001-02"),
            ("stage without actor", "STG-aftercare-01-plan"),
            ("rule without stage", "REQ-001-001")])


class TestQueryCommands(ConsistencyTestCase):
    def test_every_check_is_a_query_command(self) -> None:
        self.conn.commit()
        for name in consistency.CHECKS:
            args = query.build_parser().parse_args([name, "--db", str(self.db_path)])
            result = query.run(self.conn, None, args)
            self.assertEqual(result.columns, consistency.CHECKS[name](self.conn)[0])


if __name__ == "__main__":
    unittest.main()
