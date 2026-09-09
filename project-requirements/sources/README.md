# Subsequent Stakeholder Sources

## Purpose

This directory records requirement evidence received after the original client transcriptions. It preserves provenance without turning meeting discussion, audits, or recommendations into approved product requirements.

Approved PRDs and approved Change Requests remain the actionable product contracts. A source record may explain or challenge a contract, but it does not modify that contract until the change is reviewed and incorporated through the normal requirement-change process.

## Source Types

- `raw/` preserves stakeholder-provided files unchanged.
- `meetings/` contains concise extractions from stakeholder meetings. Rough transcripts and unrelated conversation stay outside the agent-searchable project corpus.
- `briefs/` contains normalized Markdown records for stakeholder-provided documents that mix requirements with analysis, recommendations, or unresolved questions.
- `source-register.md` is the routing index and status register.

## Classification

Every extracted item must use one classification:

- **Confirmed decision**: clearly agreed in the source and suitable for later contract reconciliation.
- **Confirmed direction**: agreed outcome or constraint whose detailed contract is not yet settled.
- **Working model**: a proposed operating model accepted for further design, not a final detailed requirement.
- **Open question**: requires stakeholder or product-owner resolution.
- **Future direction**: intentionally deferred capability or commercial direction.
- **Current-state observation**: statement about implementation or operations at a point in time; not a requirement.
- **Recommendation**: advice from the document author or project team; not stakeholder approval.

## Authority and Lifecycle

Authority is determined by validation status, not by which file is newest:

1. Approved PRD or approved Change Request.
2. Stakeholder-validated source extraction.
3. Raw stakeholder-provided artifact.
4. Unvalidated meeting extraction, proposal, or open question.
5. Code-audit observation or author recommendation.

Source records move through `captured`, `extracted`, `stakeholder-validated`, `incorporated`, and `superseded`. Validation confirms that an extraction represents the source correctly. Incorporation is a separate step that updates an owning product contract.

## Recording Rules

- Preserve raw stakeholder files byte-for-byte; create a companion Markdown record instead of editing the raw artifact.
- Do not place rough meeting transcripts in this directory. Record the meeting date, participants, external evidence location, and concise requirement extraction.
- Mark missing dates, participants, recordings, and companion documents explicitly. Never infer them from file creation time.
- Separate decisions, open questions, implementation observations, and recommendations.
- Give every material item a stable source-local ID.
- Link incorporated items to the owning PRD or Change Request instead of expanding the source record into a second PRD.
- Keep discussion unrelated to product scope out of the extraction.

## Review Boundary

The records currently in this directory are source extractions only. They do not authorize PRD, schema, implementation, design, legal, commercial, or roadmap changes.
