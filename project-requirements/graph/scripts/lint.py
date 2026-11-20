"""Check the whole requirements graph against its guardrails.

Usage: lint.py [--db DB_PATH] [--fr FR-NNN] [--json]

Prints one row per finding and exits 1 if there is any finding, 0 if the graph is clean,
2 on a usage or database error. Every finding has a stable ID, rule code plus subject
(for example L03:SCR-004-01), so finding counts can be compared between runs.

Only current requirements are checked: retired nodes, and edges with a retired end, are
history and are skipped. --fr keeps findings whose subject node is owned by that FR, so
findings about unowned nodes (Stages, Actors, Sources, and L01 missing-owner findings)
never appear with it.

L12 compares Rule statements after normalise_statement (lowercase, punctuation replaced by a space,
whitespace collapsed, the noise words in NOISE_WORDS removed). Two Rules are duplicates when their
normalised statements are equal, and near-duplicates when difflib's SequenceMatcher character ratio of
the two normalised statements is at least SIMILARITY_THRESHOLD (pairs whose word-level ratio is below
WORD_PREFILTER are skipped without the character ratio, for speed). Near-duplicates are a review list:
they can be different rules worded alike, and only a person decides. query.py duplicates uses the same
matching. A pair is skipped when either Rule lists the other in its distinct_from attribute (reviewed and
kept as different rules); query.py duplicates still shows such pairs. L02 and L13 do not overlap: L13 fires
on a Rule with no 'applies at' or 'applies to' edge, L02 on a Rule whose edges all end at retired nodes.

L14 to L19 check the flow model (schema v6): Steps owned by FRs, linked by 'next', with Flows as named start
points. A Step with handoff_from set is reported by L18, not L14, until its incoming cross-FR link is stitched.
L15 compares Stage sequence only when both Stages are on one timeline.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sqlite3
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from common import DEFAULT_DB_PATH, Edge, Graph, Node, Schema, SchemaError, load_graph, load_schema, open_db, validate_fr

RULES: dict[str, str] = {
    "L01": "node lacks an owning FR or an attribute that its type requires in schema.yaml",
    "L02": "Rule that is not global has 'applies at' or 'applies to' edges, but none ends at an active node",
    "L03": "Screen shows a non-Field, or shows nothing (unless display_only with a display_only_reason); a display_only Screen has no Step on it, or shows a Field",
    "L04": "Event has no producer Stage (several are allowed)",
    "L05": "Field calculated_by column and 'calculated by' edge disagree",
    "L06": "edge verb not allowed for its node-type pair",
    "L07": "'shows' edge has a missing or invalid provenance",
    "L08": "Stage timeline structure is broken: follows nothing, follows across timelines, "
           "shares a sequence, or a parallel timeline with a standalone entry has no Stage that enters from "
           "or joins another Stage",
    "L09": "Entity has no Fields",
    "L10": "Rule or Entity has no 'decided by' Source",
    "L11": "Field node has no row in the fields table",
    "L12": "Rule statement equals, or is near, another active Rule's statement after normalisation",
    "L13": "Rule that is not global has no 'applies at' or 'applies to' edge at all",
    "L14": "Step cannot be reached from any Flow through 'starts at' and 'next' links",
    "L15": "'next' link goes to a Step at an earlier Stage of the same timeline without back: true",
    "L16": "Step's Actor has no 'acts in' edge to the Step's Stage",
    "L17": "Step lacks a 'done by' Actor, or does not have exactly one 'at' Stage",
    "L18": "Step has an open cross-FR hand-off (handoff_to or handoff_from) not yet stitched as a 'next' link",
    "L19": "'next' link condition is not an active Rule id",
}

# Words dropped by normalise_statement: requirement boilerplate that carries no meaning of its own.
NOISE_WORDS = frozenset({"system", "must", "shall", "the", "a", "an"})
# Lowest SequenceMatcher ratio of two normalised statements reported as a near-duplicate. Measured on the
# 1079 REQ lines of the frozen PRDs (2026-11-08 baseline): 0.8 gives 34 pairs (4 exact), including the true
# cross-FR repeat REQ-004-008 / REQ-005-008 (0.81); 0.7 roughly doubles that with sibling rules that differ
# by one word or number (the same check for patients and for providers).
SIMILARITY_THRESHOLD = 0.8
# Word-level ratio a pair must reach before the slower character ratio is computed (see similarity).
WORD_PREFILTER = 0.5
_PUNCTUATION = re.compile(r"[^\w\s]")

MAIN_TIMELINE = "main"


@dataclass(frozen=True)
class Finding:
    rule: str
    key: str  # node ID, or a from>verb>to key for edge findings
    node_id: str  # subject node, used for the --fr filter
    message: str

    @property
    def id(self) -> str:
        return f"{self.rule}:{self.key}"

    def as_dict(self) -> dict[str, str]:
        return {"id": self.id, "rule": self.rule, "node_id": self.node_id, "message": self.message}


def edge_key(e: Edge) -> str:
    return f"{e.from_id}>{e.verb.replace(' ', '-')}>{e.to_id}"


def check_l01(g: Graph, schema: Schema) -> list[Finding]:
    out = []
    for n in g.active.values():
        spec = schema.node_types.get(n.type)
        if spec is None:
            continue
        if spec.owner_fr == "required" and not n.owner_fr:
            out.append(Finding("L01", n.id, n.id, f"{n.type} {n.id} has no owning FR"))
        for attr in sorted(spec.attrs.required):
            if attr not in n.attrs:
                out.append(Finding("L01", f"{n.id}#{attr}", n.id, f"{n.type} {n.id} lacks required attribute {attr!r}"))
    return out


def _is_global(n) -> bool:
    return n.attrs.get("scope") == "global"


def check_l02(g: Graph) -> list[Finding]:
    placing = ("applies at", "applies to")
    edged = {e.from_id for e in g.edges if e.verb in placing}
    live = {e.from_id for e in g.live_edges if e.verb in placing}
    return [
        Finding("L02", n.id, n.id, f"Rule {n.id} has 'applies at' or 'applies to' edges, but all end at retired nodes")
        for n in g.of_type("Rule")
        if n.id in edged and n.id not in live and not _is_global(n)
    ]


def check_l03(g: Graph) -> list[Finding]:
    shows = g.out("shows")
    on = g.into("on")
    out = []
    for n in g.of_type("Screen"):
        edges = shows.get(n.id, [])
        if n.attrs.get("display_only") is True:
            # A display-only Screen must still appear in a flow, and must not show a Field.
            if not on.get(n.id):
                out.append(Finding("L03", f"{n.id}>no-step", n.id, f"Screen {n.id} is marked display_only but no Step is 'on' it"))
            if edges:
                out.append(Finding("L03", f"{n.id}>display-only-shows", n.id,
                                   f"Screen {n.id} is marked display_only but has 'shows' edges"))
        if not edges:
            if n.attrs.get("display_only") is True:
                reason = n.attrs.get("display_only_reason")
                if isinstance(reason, str) and reason.strip():
                    continue
                out.append(Finding("L03", n.id, n.id,
                                   f"Screen {n.id} is marked display_only but has no display_only_reason, and has no 'shows' edges"))
                continue
            out.append(Finding("L03", n.id, n.id, f"Screen {n.id} has no 'shows' edges"))
        for e in edges:
            target = g.active[e.to_id]
            if target.type != "Field":
                out.append(Finding("L03", f"{n.id}>{e.to_id}", n.id, f"Screen {n.id} shows {target.type} {e.to_id}, not a Field"))
    return out


def check_l04(g: Graph) -> list[Finding]:
    emits = g.into("emits")
    out = []
    for n in g.of_type("Event"):
        producers = [e.from_id for e in emits.get(n.id, []) if g.active[e.from_id].type == "Stage"]
        if not producers:
            out.append(Finding("L04", n.id, n.id, f"Event {n.id} has no producer Stage"))
    return out


def check_l05(g: Graph) -> list[Finding]:
    # Compared on all edges, retired ends included: this checks two copies of one fact stay in sync.
    edge_targets: dict[str, set[str]] = defaultdict(set)
    for e in g.edges:
        if e.verb == "calculated by":
            edge_targets[e.from_id].add(e.to_id)
    out = []
    for n in g.of_type("Field"):
        column = g.calculated_by.get(n.id)
        expected = {column} if column else set()
        actual = edge_targets.get(n.id, set())
        if expected != actual:
            out.append(Finding(
                "L05", n.id, n.id,
                f"Field {n.id}: calculated_by column is {column or 'empty'}, "
                f"'calculated by' edges point at {', '.join(sorted(actual)) or 'nothing'}",
            ))
    return out


def check_l06(g: Graph, schema: Schema) -> list[Finding]:
    out = []
    for e in g.live_edges:
        pair = (g.active[e.from_id].type, g.active[e.to_id].type)
        verb = schema.edge_verbs.get(e.verb)
        if verb is None or pair not in verb.pairs:
            allowed = ", ".join(f"{a}->{b}" for a, b in sorted(verb.pairs)) if verb else "verb not in schema.yaml"
            out.append(Finding("L06", edge_key(e), e.from_id, f"'{e.verb}' cannot join {pair[0]} -> {pair[1]} (allowed: {allowed})"))
    return out


def check_l07(g: Graph, schema: Schema) -> list[Finding]:
    allowed = set(schema.enum("provenance"))
    out = []
    for e in g.live_edges:
        if e.verb != "shows":
            continue
        value = e.attrs.get("provenance")
        if value is None:
            out.append(Finding("L07", edge_key(e), e.from_id, f"{e.from_id} shows {e.to_id} without a provenance"))
        elif value not in allowed:
            out.append(Finding("L07", edge_key(e), e.from_id, f"{e.from_id} shows {e.to_id} with invalid provenance {value!r}"))
    return out


def _sequence_order(n: Node) -> tuple[int, str]:
    """Sort key for Stages: by sequence, a missing or non-integer sequence last, then by ID."""
    sequence = n.attrs.get("sequence")
    return (sequence if type(sequence) is int else sys.maxsize, n.id)


def check_l08(g: Graph) -> list[Finding]:
    follows = g.out("follows")
    stages = g.of_type("Stage")
    out = []
    for n in stages:
        sequence = n.attrs.get("sequence")
        is_first = type(sequence) is int and sequence == 1
        if is_first or n.attrs.get("standalone_entry") is True:
            continue
        if not any(g.active[e.to_id].type == "Stage" for e in follows.get(n.id, [])):
            out.append(Finding("L08", n.id, n.id, f"Stage {n.id} (sequence {sequence}) follows no Stage and is not a standalone entry"))

    for n in stages:
        for e in follows.get(n.id, []):
            target = g.active[e.to_id]
            if target.type != "Stage":
                continue
            own, other = n.attrs.get("timeline"), target.attrs.get("timeline")
            if own != other:
                out.append(Finding(
                    "L08", edge_key(e), n.id,
                    f"Stage {n.id} (timeline {own}) follows {target.id} on a different timeline ({other})",
                ))

    by_slot: dict[tuple[str, int], list[str]] = defaultdict(list)
    for n in stages:
        timeline, sequence = n.attrs.get("timeline"), n.attrs.get("sequence")
        if isinstance(timeline, str) and type(sequence) is int:
            by_slot[(timeline, sequence)].append(n.id)
    for (timeline, sequence), ids in by_slot.items():
        if len(ids) > 1:
            ids.sort()
            out.append(Finding(
                "L08", "+".join(ids), ids[0],
                f"Stages {', '.join(ids)} share sequence {sequence} on timeline {timeline}",
            ))

    # A parallel timeline that can start on its own (it has a standalone entry) must still link to
    # another timeline somewhere; any of its Stages may carry the link. Account timelines have no
    # standalone entry and are not checked.
    by_timeline: dict[str, list[Node]] = defaultdict(list)
    for n in stages:
        timeline = n.attrs.get("timeline")
        if isinstance(timeline, str) and timeline != MAIN_TIMELINE:
            by_timeline[timeline].append(n)
    for timeline, members in by_timeline.items():
        if not any(n.attrs.get("standalone_entry") is True for n in members):
            continue
        if any(
            g.active[e.to_id].type == "Stage"
            for n in members
            for e in g.edges_from(n.id, "enters from") + g.edges_from(n.id, "joins")
        ):
            continue
        first = min(members, key=_sequence_order)
        out.append(Finding(
            "L08", first.id, first.id,
            f"Timeline {timeline} has no Stage with an 'enters from' or 'joins' edge to a Stage",
        ))
    return out


def check_l09(g: Graph) -> list[Finding]:
    with_fields = {entity for fid, entity in g.entity_of.items() if fid in g.active}
    return [
        Finding("L09", n.id, n.id, f"Entity {n.id} has no active Fields")
        for n in g.of_type("Entity")
        if n.id not in with_fields
    ]


def check_l10(g: Graph) -> list[Finding]:
    decided = g.out("decided by")
    out = []
    for n in g.of_type("Rule") + g.of_type("Entity"):
        if not any(g.active[e.to_id].type == "Source" for e in decided.get(n.id, [])):
            out.append(Finding("L10", n.id, n.id, f"{n.type} {n.id} has no 'decided by' Source"))
    return out


def check_l11(g: Graph) -> list[Finding]:
    return [
        Finding("L11", n.id, n.id, f"Field {n.id} has no row in the fields table")
        for n in g.of_type("Field")
        if n.id not in g.entity_of
    ]


def normalise_statement(text: str) -> str:
    """Lowercase, replace punctuation with a space, collapse whitespace and drop NOISE_WORDS."""
    words = _PUNCTUATION.sub(" ", text.lower()).split()
    return " ".join(w for w in words if w not in NOISE_WORDS)


@dataclass(frozen=True)
class Match:
    """One Rule matched against a statement: score 1.0 and exact True when the normalised texts are equal."""

    rule_id: str
    other: str  # the other Rule's id, or "" when matching free text
    score: float
    exact: bool


class _Comparer:
    """Scores normalised statements against one fixed statement, reusing difflib's cached work on it."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.words = difflib.SequenceMatcher(None, autojunk=False)
        self.words.set_seq2(text.split())

    def similarity(self, other: str) -> float | None:
        """Character ratio against other, or None when the word-level ratio is below WORD_PREFILTER.

        The word-level pass is cheap and keeps a scan of a thousand Rules to a few seconds; on the
        frozen PRD lines it keeps every pair the full character scan finds at SIMILARITY_THRESHOLD.
        """
        w = self.words
        w.set_seq1(other.split())
        if w.real_quick_ratio() < WORD_PREFILTER or w.quick_ratio() < WORD_PREFILTER or w.ratio() < WORD_PREFILTER:
            return None
        return difflib.SequenceMatcher(None, other, self.text, autojunk=False).ratio()

    def match(self, other: str, rule_id: str, other_id: str, threshold: float) -> Match | None:
        if other == self.text:
            return Match(rule_id, other_id, 1.0, True)
        score = self.similarity(other)
        return Match(rule_id, other_id, score, False) if score is not None and score >= threshold else None


def rule_statements(g: Graph) -> dict[str, str]:
    """Normalised statement of every active Rule that has a non-empty one, by Rule id."""
    out = {}
    for n in g.of_type("Rule"):
        statement = n.attrs.get("statement")
        if isinstance(statement, str) and (norm := normalise_statement(statement)):
            out[n.id] = norm
    return out


def match_statement(text: str, statements: dict[str, str], threshold: float = SIMILARITY_THRESHOLD) -> list[Match]:
    """Rules whose normalised statement equals or is near text, best score first."""
    norm = normalise_statement(text)
    if not norm:
        return []
    comparer = _Comparer(norm)
    found = (comparer.match(other, rule_id, "", threshold) for rule_id, other in statements.items())
    return sorted((m for m in found if m), key=lambda m: (-m.score, m.rule_id))


def duplicate_pairs(statements: dict[str, str], threshold: float = SIMILARITY_THRESHOLD) -> list[Match]:
    """Every pair of Rules whose statements are equal or near after normalisation, best score first.

    rule_id is the lower id of the pair and other the higher, so each pair appears once.
    """
    ids = sorted(statements)
    found = []
    for i, a in enumerate(ids):
        comparer = _Comparer(statements[a])
        found += [comparer.match(statements[b], a, b, threshold) for b in ids[i + 1:]]
    return sorted((m for m in found if m), key=lambda m: (-m.score, m.rule_id, m.other))


def _distinct_pairs(g: Graph) -> set[frozenset[str]]:
    """Pairs of Rule ids reviewed and kept as different rules, from either side's distinct_from attribute."""
    pairs = set()
    for n in g.of_type("Rule"):
        value = n.attrs.get("distinct_from")
        if isinstance(value, str):
            pairs.update(frozenset((n.id, other.strip())) for other in value.split(",") if other.strip())
    return pairs


def check_l12(g: Graph) -> list[Finding]:
    """One finding per Rule that has duplicates, listing each with its score, so --fr shows both sides."""
    partners: dict[str, list[tuple[str, Match]]] = defaultdict(list)
    distinct = _distinct_pairs(g)
    for m in duplicate_pairs(rule_statements(g)):
        if frozenset((m.rule_id, m.other)) in distinct:
            continue
        partners[m.rule_id].append((m.other, m))
        partners[m.other].append((m.rule_id, m))
    out = []
    for rule_id, items in partners.items():
        detail = ", ".join(
            f"{other} ({'same text' if m.exact else f'similar {m.score:.2f}'})"
            for other, m in sorted(items, key=lambda item: (-item[1].score, item[0]))
        )
        out.append(Finding("L12", rule_id, rule_id, f"Rule {rule_id} duplicates {detail}"))
    return out


def check_l13(g: Graph) -> list[Finding]:
    """A Rule with no 'applies at' or 'applies to' edge at all; edges that all end at retired nodes are L02."""
    applying = {e.from_id for e in g.edges if e.verb in ("applies at", "applies to")}
    return [
        Finding("L13", n.id, n.id, f"Rule {n.id} has no 'applies at' or 'applies to' edge and is not global")
        for n in g.of_type("Rule")
        if n.id not in applying and not _is_global(n)
    ]


def _step_stage(g: Graph) -> dict[str, str]:
    """Each Step's Stage, when it has exactly one live 'at' edge."""
    return {step: edges[0].to_id for step, edges in g.out("at").items() if len(edges) == 1}


def check_l14(g: Graph) -> list[Finding]:
    nxt = g.out("next")
    reached: set[str] = set()
    todo = [e.to_id for edges in g.out("starts at").values() for e in edges]
    while todo:
        step = todo.pop()
        if step not in reached:
            reached.add(step)
            todo += [e.to_id for e in nxt.get(step, [])]
    return [
        Finding("L14", n.id, n.id, f"Step {n.id} cannot be reached from any Flow")
        for n in g.of_type("Step")
        if n.id not in reached and not n.attrs.get("handoff_from")
    ]


def check_l15(g: Graph) -> list[Finding]:
    stage_of = _step_stage(g)
    out = []
    for e in g.live_edges:
        if e.verb != "next" or e.attrs.get("back") is True:
            continue
        a, b = stage_of.get(e.from_id), stage_of.get(e.to_id)
        if a is None or b is None:
            continue
        sa, sb = g.active[a], g.active[b]
        if sa.attrs.get("timeline") != sb.attrs.get("timeline"):
            continue
        qa, qb = sa.attrs.get("sequence"), sb.attrs.get("sequence")
        if type(qa) is int and type(qb) is int and qb < qa:
            out.append(Finding("L15", edge_key(e), e.from_id,
                               f"Step {e.from_id} at {a} goes next to {e.to_id} at earlier Stage {b}; set back: true if intended"))
    return out


def check_l16(g: Graph) -> list[Finding]:
    stage_of = _step_stage(g)
    acts = {(e.from_id, e.to_id) for e in g.live_edges if e.verb == "acts in"}
    out = []
    for step, edges in g.out("done by").items():
        stage = stage_of.get(step)
        if stage is None:
            continue
        for e in edges:
            if (e.to_id, stage) not in acts:
                out.append(Finding("L16", f"{step}>{e.to_id}", step, f"Step {step}: {e.to_id} has no 'acts in' edge to {stage}"))
    return out


def check_l17(g: Graph) -> list[Finding]:
    done_by, at = g.out("done by"), g.out("at")
    out = []
    for n in g.of_type("Step"):
        if not done_by.get(n.id):
            out.append(Finding("L17", f"{n.id}#done-by", n.id, f"Step {n.id} has no 'done by' Actor"))
        stages = len(at.get(n.id, []))
        if stages != 1:
            out.append(Finding("L17", f"{n.id}#at", n.id, f"Step {n.id} has {stages} 'at' Stages, not one"))
    return out


def check_l18(g: Graph) -> list[Finding]:
    out = []
    for n in g.of_type("Step"):
        for key in ("handoff_to", "handoff_from"):
            if n.attrs.get(key):
                out.append(Finding("L18", f"{n.id}#{key}", n.id, f"Step {n.id} {key} {n.attrs[key]!r} is not stitched yet"))
    return out


def check_l19(g: Graph) -> list[Finding]:
    out = []
    for e in g.live_edges:
        if e.verb != "next" or "condition" not in e.attrs:
            continue
        target = g.active.get(e.attrs["condition"])
        if target is None or target.type != "Rule":
            out.append(Finding("L19", edge_key(e), e.from_id,
                               f"'next' {e.from_id} to {e.to_id} has condition {e.attrs['condition']!r}, not an active Rule"))
    return out


def lint(conn: sqlite3.Connection, schema: Schema, fr: str | None = None) -> list[Finding]:
    """Run every rule and return findings sorted by ID. With fr, keep findings whose subject that FR owns."""
    g = load_graph(conn)
    findings = (
        check_l01(g, schema) + check_l02(g) + check_l03(g) + check_l04(g) + check_l05(g)
        + check_l06(g, schema) + check_l07(g, schema) + check_l08(g) + check_l09(g) + check_l10(g)
        + check_l11(g) + check_l12(g) + check_l13(g) + check_l14(g) + check_l15(g) + check_l16(g)
        + check_l17(g) + check_l18(g) + check_l19(g)
    )
    if fr is not None:
        findings = [f for f in findings if f.node_id in g.nodes and g.nodes[f.node_id].owner_fr == fr]
    return sorted(findings, key=lambda f: (f.rule, f.key))


def format_table(findings: list[Finding]) -> str:
    if not findings:
        return "No findings."
    rows = [("ID", "Message")] + [(f.id, f.message) for f in findings]
    width = max(len(r[0]) for r in rows)
    lines = [f"{a.ljust(width)}  {b}" for a, b in rows]
    lines.insert(1, f"{'-' * width}  {'-' * 7}")
    counts: dict[str, int] = defaultdict(int)
    for f in findings:
        counts[f.rule] += 1
    summary = ", ".join(f"{rule}: {n}" for rule, n in sorted(counts.items()))
    lines.append("")
    lines.append(f"{len(findings)} finding(s) ({summary})")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the requirements graph against its guardrails.")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="graph DB (default: graph.db in the graph folder)")
    parser.add_argument("--fr", help="only report findings on nodes owned by this FR (FR-NNN)")
    parser.add_argument("--json", action="store_true", help="print findings as JSON")
    args = parser.parse_args(argv)
    try:
        schema = load_schema()
        conn = open_db(args.db, read_only=True)
        try:
            if args.fr:
                validate_fr(conn, schema, args.fr)
            findings = lint(conn, schema, args.fr)
        finally:
            conn.close()
    except (SchemaError, FileNotFoundError, ValueError, sqlite3.Error) as exc:
        print(f"lint: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"count": len(findings), "findings": [f.as_dict() for f in findings]}, indent=2, ensure_ascii=False))
    else:
        print(format_table(findings))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
