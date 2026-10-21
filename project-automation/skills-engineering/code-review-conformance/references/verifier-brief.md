# Verifier Brief (fixed prompt template)

The main agent copies everything between the two `BRIEF` markers into each verifier prompt,
fills the `{{...}}` placeholders (same values as the checker run), appends the full text of
`references/rubric.md`, and then adds: the single gap to test, the unit block, the unit's PRD
excerpt, and the code-map pointers. One verifier per gap; never batch gaps.

---BEGIN BRIEF---

A reviewer claims the Hairline source code fails ONE requirement of a functional requirement
(FR) PRD. Your job is to try to **refute** that claim. Assume it may be a false positive: static
review often misses behavior that lives somewhere unexpected. Only if you search honestly and
cannot refute it should you confirm it.

## Where to search for the "missing" behavior

Check each that could plausibly apply before you confirm:

1. The other repo: backend logic the frontend relies on, or a frontend guard for a backend rule
   (and vice versa: a frontend-only guard does not satisfy a backend rule).
2. Middleware, route groups, policies, gates, form requests, global scopes, model observers.
3. Jobs, queued listeners, events, notifications, scheduled commands (`routes/console.php`,
   `app/Console/`).
4. Services, traits, base controllers, shared hooks/components, API client wrappers.
5. Alternate or newer routes and controllers (legacy and current APIs often coexist; check
   which one the dashboard actually calls).
6. Config, seeders, and migrations (defaults, constraints, enum values).
7. The PRD itself: re-read the excerpt. Is the claimed requirement actually stated, for this
   tenant, in this phase? Does the cited section say what the claim says?

Repo scope: `main/hairline-backend/` and `main/hairline-frontend/` only. **Never open or search
`main/hairline-app/`. Never modify any file.** Code maps are a locator only; confirm in source.
Search narrowly (`rg -n -m 20 <pattern> <path>`); narrow any search that floods.

## Probes

Same rules as the checker: target `{{BASE_URL}}`, collection `{{COLLECTION_ID}}`, environment
`{{ENVIRONMENT_ID}}`, accounts from `{{CREDENTIALS_DIR}}` referenced by row ID only, staging
writes **{{WRITES_ALLOWED}}** (off = GET plus login only; on = test data only, log every write).
Never output credential values.

## Honesty rule

If you cannot decide, return `Downgraded` to `Needs runtime` with the reason; never confirm by
default and never refute without a file:line or a PRD quote that shows why.

## Return format (exactly this, nothing before or after)

```yaml
gap: <unit ID>#<gap n>
outcome: Confirmed | Downgraded | Refuted
new_severity: <P0-P3, only if Downgraded>
new_status: <Confirmed | Needs runtime | Needs decision, only if Downgraded>
reason: <one or two sentences>
evidence: [<path:line or probe id that supports the outcome>]
searched: [<short list of locations checked>]
probes:
  - id: VPRB-1
    call: <METHOD path> as <account row ID>
    result: <status code + one-line observation>
    write: false
```

---END BRIEF---
