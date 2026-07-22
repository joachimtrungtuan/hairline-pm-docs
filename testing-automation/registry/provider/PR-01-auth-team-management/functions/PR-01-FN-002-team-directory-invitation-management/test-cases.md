# Registered Function: `PR-01-FN-002` Team Directory and Invitation Management

**Primary module:** `PR-01`
**Participating modules:** None
**Registry status:** `DRAFT`
**Coverage status:** Eighteen executable cases registered; nine governed fixture, permission, rate-limit, and lifecycle gaps remain open
**Last UI-confirmed date:** 2026-07-15

> This registry entry points to live PRDs. It records test interpretation and implementation evidence without replacing requirement authority.

## 1. Registry Control

| Field | Value |
| --- | --- |
| Function ID | `PR-01-FN-002` |
| Test level | `function` |
| Primary module | `PR-01` |
| Human owner | Product Owner |
| Happy-path approval | Approved function boundary and invitation lifecycle direction, 2026-07-15 |
| Derived-case authority | Testing Constitution v1.2 |
| Registry status | `DRAFT` |
| Created | 2026-07-15 |
| Last approved revision | `v1` case design approved; activation pending |
| Supersedes | None |

## 2. Live Source References

Hashes are SHA-256 values for the referenced source ranges at registration time.

| Reference ID | Source path | Requirement / heading | Approved hash |
| --- | --- | --- | --- |
| `PR-01-TC-0007-SRC-01` | `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md` | Team Management Dashboard and Invite Team Member Form | `a581aff5f7db3d1e6e68fb01e8c3b5da8967b0cb3573e1a1f73b313b68de4787` |
| `PR-01-TC-0007-SRC-02` | `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md` | Team invitation business rules | `b88b6fedb659aa2ebc550efcf79120cf58f94c8dc97358dfe2189aead459d263` |
| `PR-01-TC-0008-SRC-01` | `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` | Shared search and filter controls | `9e7c9561bee970ce11ec124d27d5bf20167172c302bf21a57a7ee011def4b59b` |
| `PR-01-TC-0008-SRC-02` | `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` | Provider Team Directory | `21c2ba46178f74649fc73e62b4524ea391323bf3fd5429a2ecd577e50b05c40d` |
| `PR-01-TC-0008-SRC-03` | `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` | Team search requirement and pagination defaults | `d8ea3508fc16a10a9514c8fa183ec547cc6763ab361a772360e01e118da8647c` |
| `PR-01-TC-0019-SRC-01` | `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` | Alternate Flow B1 — no results found | `91aca46b813cf50c18abfc684d8bba0e3190746c1f64f8aa17a37ced1d4e330f` |
| `PR-01-TC-0020-SRC-01` | `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` | Team Role filter | `21c2ba46178f74649fc73e62b4524ea391323bf3fd5429a2ecd577e50b05c40d` |
| `PR-01-TC-0021-SRC-01` | `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` | Team Status filter | `21c2ba46178f74649fc73e62b4524ea391323bf3fd5429a2ecd577e50b05c40d` |
| `PR-01-TC-0022-SRC-01` | `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` | Team Region filter | `21c2ba46178f74649fc73e62b4524ea391323bf3fd5429a2ecd577e50b05c40d` |
| `PR-01-TC-0023-SRC-01` | `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` | Filter AND logic across criteria | `9e7c9561bee970ce11ec124d27d5bf20167172c302bf21a57a7ee011def4b59b` |
| `PR-01-TC-0024-SRC-01` | `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` | Alternate Flow B1 — no results found | `91aca46b813cf50c18abfc684d8bba0e3190746c1f64f8aa17a37ced1d4e330f` |
| `PR-01-TC-0012-SRC-01` | `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md` | Invite Team Member user story | `3dbe402431dc9d98210fc029d8b1481724b953f55af2ffebbb64bb19997fac85` |
| `PR-01-TC-0012-SRC-02` | `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md` | Requirements summary | `eae11b1ecdf09ab0cffcf217925ad1310f1b4c58ddf1aab06f6d9a6a1e4a27ff` |
| `PR-01-TC-0007-SRC-03` | `local-docs/project-requirements/functional-requirements/fr031-admin-access-control/prd.md` | PR-01 Provider permissions | `23b03b1eb7b0b04bcf731f7a1d48a771752c45ce0c6431163927461bafdca425` |
| `PR-01-TC-0015-SRC-01` | `local-docs/project-requirements/functional-requirements/fr031-admin-access-control/prd.md` | Provider role matrix | `c2a6ab0e0478638c2a96b3f821dc9e4f9c302fce630ebe1adb8bb6d19c0b5c11` |

## 3. Current Implementation Mapping

| Surface | Current route / API | Mapping status | Last confirmed | Notes |
| --- | --- | --- | --- | --- |
| Team directory | `/team` | Confirmed | 2026-07-15 | Team Members and Invitations share the page; Invite Staff is accessible to the registered Provider |
| Invite form | `/team` dialog | Confirmed with discrepancy | 2026-07-15 | Current dialog exposes Email address, Role, and Send; PRD-required name, message, and seat surfaces are not currently visible |
| Team search/filter | `/team` controls | Confirmed with discrepancy | 2026-07-15 | Current placeholder and filter content do not match the Team requirements; member responses do not currently expose a deterministic Region value |
| Roles | `GET /api/team/roles` | Confirmed | 2026-07-15 | Manager, Clinical Staff, and Billing Staff are returned; Owner is excluded |
| Members | `GET /api/team/members` | Confirmed | 2026-07-15 | Used only to prepare deterministic search/page-size data |
| Invitations | `GET/POST /api/team/invitations` | Confirmed | 2026-07-15 | Pending creation, resend, copy-link surface, cancellation, and 7-day expiry are implemented |
| Email delivery | `POST https://api.maildrop.cc/graphql` | Confirmed with safety gate | 2026-07-15 | Public inbox; mutation cases require explicit human acceptance before sending, and links/tokens are never persisted |

## 4. Requirement and Category Coverage

### Requirement Coverage Matrix

| Requirement or rule | Category | Case / gap | Coverage |
| --- | --- | --- | --- |
| Owner/Manager can open Team and see required directory/invitation data | Happy / permission | `PR-01-TC-0007` | Partial pending controlled validation |
| Team search returns matching name, email, and status values and restores results after clear | Search / data consistency | `PR-01-TC-0008` | Draft executable |
| Team search shows an explicit empty state for an unavailable value | Search / negative | `PR-01-TC-0019` | Draft executable |
| Team filters expose role, status, and region with reset | Filter / data consistency | `PR-01-TC-0009` | Draft executable |
| Role, Status, and Region filters each return an API-confirmed matching member | Filter / positive | `PR-01-TC-0020`, `PR-01-TC-0021`, `PR-01-TC-0022` | Draft executable; Region setup blocks if the API supplies no member-region relationship |
| Role, Status, and Region combine with AND logic for a shared matching member | Filter / data consistency | `PR-01-TC-0023` | Draft executable; deterministic Region fixture required |
| Valid Role, Status, and Region values with no shared member show an empty state | Filter / negative | `PR-01-TC-0024` | Draft executable; deterministic incompatible combination required |
| Team directory defaults to 25 records per page | Boundary | `PR-01-TC-0010` | Draft executable |
| Invite form exposes names, email, role, message, and seat context | Validation / UX contract | `PR-01-TC-0011` | Draft executable |
| Fresh invitation becomes Pending, expires after 7 days, and reaches mailbox | Happy / state transition | `PR-01-TC-0012` | Draft executable |
| Invalid email is rejected without creating an invitation | Negative / validation | `PR-01-TC-0013` | Draft executable |
| Same-Provider duplicate invitation is rejected | Negative / idempotency | `PR-01-TC-0014` | Draft executable |
| Assignable roles include Manager, Clinical, and Billing but not Owner | Permission / role | `PR-01-TC-0015` | Draft executable |
| Pending row exposes Resend, Copy Link, Cancel, and Refresh | State / action availability | `PR-01-TC-0016` | Draft executable |
| Resend refreshes expiry and produces another email | State transition | `PR-01-TC-0017` | Draft executable |
| Cancel requires confirmation and removes the Pending invitation | State transition | `PR-01-TC-0018` | Draft executable |
| Cross-Provider membership duplication is rejected | Privacy / negative | `GAP-04` | Open — no isolated second-Provider membership fixture |
| Seat boundary blocks invite and exposes request-more-seats action | Boundary | `GAP-05` | Open — no safe near-limit Provider fixture |
| Invitation rate limit enforces 10 per hour | Boundary / security | `GAP-06` | Open — no isolated counter/reset mechanism |
| Failed email delivery remains Pending Send and retries | Failure recovery | `GAP-07` | Open — no controllable email-failure fixture |
| Expired invitation can be resent and old token is invalid | Lifecycle / security | `GAP-08` | Open — no fresh controlled expired invitation fixture |
| Clinical/Billing cannot view or invite; Owner/Manager can | Permission | `GAP-09` | Open — dedicated role-specific login accounts are unavailable |
| Concurrent duplicate submits create only one invitation | Concurrency / idempotency | `GAP-10` | Open — needs isolated concurrency fixture and deterministic API observation |
| Team changes are represented in audit history | Audit / data consistency | `GAP-11` | Deferred to the approved PR-01 activity-audit-log function boundary |
| One Provider cannot observe another Provider's directory/invitations | Privacy | `GAP-12` | Open — requires two isolated Provider organizations |

### Category Applicability

| Category | Status | Notes |
| --- | --- | --- |
| Happy path | Covered in draft | Access and fresh invitation cases |
| Negative / validation | Covered in draft | Invalid and duplicate email cases |
| Boundary / edge | Partial | Pagination covered; seat, rate, and expiry fixtures remain gaps |
| Permission / role | Partial | Assignable roles covered; role-specific access accounts remain a gap |
| State transition | Covered in draft | Pending, resend, and cancel; expired transition remains a gap |
| Idempotency | Partial | Sequential duplicate covered; concurrency remains a gap |
| Concurrency-sensitive | Gap | `GAP-10` |
| Data consistency | Partial | UI/API state covered; audit and cross-Provider isolation remain gaps |

## 5. Dataset Recipes

All generated invitation records use a deterministic run-and-dataset mailbox under `maildrop.cc`. Because Maildrop inboxes are public, mutation datasets stop before browser execution unless `HAIRLINE_ALLOW_PUBLIC_INVITE_MAILBOX=true` records explicit human acceptance of public invitation-link exposure. Credentials, bearer tokens, raw invitation tokens, and email-body links are not stored.

| Dataset ID | Revision | Scenario purpose | Builder reference | Retention marker |
| --- | --- | --- | --- | --- |
| `PR-01-DS-0007` | `v1` | Authorized Team access | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0008` | `v1` | API-confirmed member search value | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0009` | `v1` | Team filter contract | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0010` | `v1` | API-confirmed member total | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0011` | `v1` | Invite form contract | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0012` | `v1` | Fresh Manager invitation and Maildrop delivery | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0013` | `v1` | Invalid email | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0014` | `v1` | Same-Provider duplicate invitation | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0015` | `v1` | Assignable-role boundary | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0016` | `v1` | Pending invitation actions | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0017` | `v1` | Resend transition | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0018` | `v1` | Cancel transition | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0019` | `v1` | Deterministic unavailable search term | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0020` | `v1` | API-confirmed member Role | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0021` | `v1` | API-confirmed member Status | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0022` | `v1` | API-confirmed member Region | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0023` | `v1` | API-confirmed matching Role, Status, and Region combination | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |
| `PR-01-DS-0024` | `v1` | Individually valid filter values with no shared member | `datasets.ts#buildTeamInvitationDataset` | Run ID plus dataset ID |

## 6. Draft Test Cases

All cases use status `DRAFT`, automation module `tests.spec.ts`, and the constitutional retry/evidence policy. Cases use revision `v1` unless an individual case or the revision log records a later revision.

### `PR-01-TC-0007` — Authorized Provider can access Team and Invitations

- **Category / priority:** Happy path and permission, `P0`, smoke/affected/module/full.
- **Actions:** Log in through Provider role selection and navigate to Team from the dashboard navigation.
- **Assertions:** Team Members, Invitations, Invite Staff, and the required directory columns are visible.

### `PR-01-TC-0008` — Team search returns matches for name email and status

- **Revision:** `v2`.
- **Category / priority:** Search and data consistency, `P1`, affected/module/full.
- **Setup:** Select API-confirmed member fixtures for name, email, and status.
- **Actions:** Search each criterion separately, wait beyond the 500ms debounce, and clear before the next criterion.
- **Assertions:** Every criterion returns its expected member; clearing each search restores the directory results.

### `PR-01-TC-0009` — Team directory filters expose role status and region controls

- **Category / priority:** Filter and data consistency, `P1`, affected/module/full.
- **Actions:** Open the Team filter surface.
- **Assertions:** Role, Status, Region, and Clear/Reset controls are present.

### `PR-01-TC-0010` — Team directory uses the required default page size

- **Category / priority:** Boundary, `P1`, affected/module/full.
- **Setup:** Confirm through API that the Provider has at least 25 members.
- **Actions:** Open the initial Team directory page without a page-size override.
- **Assertions:** Exactly 25 member rows are shown on the initial page.

### `PR-01-TC-0011` — Invite form exposes the complete PRD field contract

- **Category / priority:** Validation and UX contract, `P0`, affected/module/full.
- **Actions:** Open Invite Staff.
- **Assertions:** First Name, Last Name, Email, Role, Personal Message, and seat/team-size context are visible.

### `PR-01-TC-0012` — Provider invites a Manager with fresh Maildrop delivery

- **Category / priority:** Happy path and state transition, `P0`, smoke/affected/module/full.
- **Setup:** Generate a unique synthetic Maildrop mailbox.
- **Actions:** Open Invite Staff, enter the fresh email, select Manager, and send through the UI.
- **Assertions:** The request succeeds, the Pending row exists, API status is pending, expiry is seven days, and a Team Invitation email reaches Maildrop.

### `PR-01-TC-0013` — Invite form rejects an invalid email without submission

- **Category / priority:** Negative and validation, `P1`, affected/module/full.
- **Actions:** Enter a syntactically invalid email, select Manager, and submit.
- **Assertions:** Client validation explains the invalid email, no invitation request occurs, and the dialog remains open.

### `PR-01-TC-0014` — Duplicate invitation within the Provider is blocked

- **Category / priority:** Negative and idempotency, `P1`, affected/module/full.
- **Setup:** Create or locate the case-owned Pending invitation.
- **Actions:** Submit the same address again through Invite Staff.
- **Assertions:** No successful second invitation occurs, explanatory feedback is visible, and only one matching row remains.

### `PR-01-TC-0015` — Invitation role choices exclude Owner

- **Category / priority:** Permission and role, `P0`, affected/module/full.
- **Actions:** Open the Role selector in Invite Staff.
- **Assertions:** Manager, Clinical Staff, and Billing Staff are available; Owner is absent.

### `PR-01-TC-0016` — Pending invitation exposes governed management actions

- **Category / priority:** Action availability and data consistency, `P1`, affected/module/full.
- **Setup:** Create or locate the case-owned Pending invitation.
- **Actions:** Inspect the matching row and page controls.
- **Assertions:** Resend, Copy Link, Cancel, and Refresh are visible; the raw link is not captured.

### `PR-01-TC-0017` — Resending a pending invitation refreshes expiry and email

- **Category / priority:** State transition, `P0`, affected/module/full.
- **Setup:** Create or locate the case-owned Pending invitation and record its API expiry/mail count.
- **Actions:** Click Resend through the matching row.
- **Assertions:** The API expiry changes to a fresh seven-day timestamp, status remains pending, and Maildrop receives another message.

### `PR-01-TC-0018` — Cancelling a pending invitation requires confirmation

- **Category / priority:** State transition, `P0`, affected/module/full.
- **Setup:** Create or locate the case-owned Pending invitation.
- **Actions:** Click Cancel, observe the confirmation prompt, then confirm through the UI.
- **Assertions:** The row disappears and the invitation is no longer returned by the active invitation API.

### `PR-01-TC-0019` — Team search shows an empty state for an unavailable value

- **Revision:** `v2`.
- **Category / priority:** Search and negative, `P1`, affected/module/full.
- **Setup:** Generate a run-specific term that cannot match a registered member.
- **Actions:** Enter the unavailable value and wait beyond the 500ms debounce.
- **Assertions:** The Team directory displays its explicit no-results/empty state.

### `PR-01-TC-0020` — Role filter returns an available team member

- **Category / priority:** Filter and positive result, `P1`, affected/module/full.
- **Setup:** Select an API-confirmed member Role and expected member row.
- **Actions:** Apply only the Role filter.
- **Assertions:** The expected matching member remains in the directory.

### `PR-01-TC-0021` — Status filter returns an available team member

- **Category / priority:** Filter and positive result, `P1`, affected/module/full.
- **Setup:** Select an API-confirmed Active, Inactive, or Pending Invitation member state.
- **Actions:** Apply only the Status filter.
- **Assertions:** The expected matching member remains in the directory.

### `PR-01-TC-0022` — Region filter returns an available team member

- **Category / priority:** Filter and positive result, `P1`, affected/module/full.
- **Setup:** Select an API-confirmed member Region and expected member row; block safely if the API exposes no member-region relationship.
- **Actions:** Apply only the Region filter.
- **Assertions:** The expected matching member remains in the directory.

### `PR-01-TC-0023` — Role status and region filters return their shared match

- **Category / priority:** Filter, combined AND logic, and positive result, `P1`, affected/module/full.
- **Setup:** Select one member with API-confirmed Role, Status, and Region values.
- **Actions:** Apply all three criteria together.
- **Assertions:** The shared member remains and the combined filters do not broaden the result set.

### `PR-01-TC-0024` — Valid combined filters show an empty state when no member matches

- **Category / priority:** Filter, combined AND logic, and negative result, `P1`, affected/module/full.
- **Setup:** Select Role, Status, and Region values that each exist independently but have no shared member.
- **Actions:** Apply all three criteria together.
- **Assertions:** The Team directory displays its explicit no-results/empty state.

## 7. Runtime Evidence Requirements

- Apply one initial attempt plus three retries with at least five seconds between failures.
- Retain no screenshot or trace for an initial pass.
- Route every non-clean result to `NEEDS_HUMAN_REVIEW`; no automated result confirms a bug.
- Maildrop automation stores only mailbox/message counts and subject matching in memory. It does not persist raw invitation links or tokens.
- Maildrop mutation datasets require an explicit public-mailbox safety acknowledgement; otherwise the execution is `BLOCKED` for human review before sending.
- Every mutation is performed through the browser. API calls prepare data or confirm resulting state only.
- Generated records are retained; cancellation is the behavior under test, not cleanup.

## 8. Revision Log

| Revision | Date | Status | Reason | Approved by / authority | Originating result |
| --- | --- | --- | --- | --- | --- |
| `v1` | 2026-07-15 | Draft | Initial grouped registration after PRD scout and corrected live UI retry | Product Owner boundary approval plus Constitution v1.2 | None |
| `v1` | 2026-07-15 | Draft validation | Assignable-role case passed; directory-contract case and locator-hardening runs remain queued for human review; public mailbox mutation validation remains safety-gated | Controlled validation only | `RUN-20260715T085339Z-6e36c5fb`, `RUN-20260715T090941Z-8daa99fb` |
| `v1` | 2026-07-15 | Draft expanded | Split search into matching and empty-state behavior; added individual Role, Status, and Region filters plus matching and empty combined-filter cases; read-only setup validation confirmed Region-dependent cases block without a member-region relationship | Product Owner direction | None |
| `v1` | 2026-07-15 | Draft implementation approved | Expanded search/filter case design approved for Playwright implementation; cases remain non-active | Product Owner | None |
| `v1` | 2026-07-15 | Draft controlled validation | Unavailable search reached the visible empty state, but all four attempts observed a Team members request without the entered term; routed without classification | Controlled validation only | `RUN-20260715T101539Z-e2254a55` |
| `v2` | 2026-07-16 | Draft update approved | Removed API URL/search-term coupling from matching and unavailable Team search cases. Search verification now uses only observable matching results, restored results after clear, and the visible empty state. Recorded the generic empty-state presentation separately as a possible UI discrepancy. | Product Owner | `RUN-20260715T101539Z-e2254a55` |
| `v2` | 2026-07-16 | Draft controlled validation | Waited for the Team directory to load before entering the unavailable value. Four attempts consistently observed the search field reset to blank, the member rows remain visible, and no empty state appeared. Routed for human review without an automated bug classification. | Controlled validation only | `RUN-20260716T050857Z-7cfbba33` |

## 9. Registration Checklist

- [x] The PRD flow scout and Product Owner function-boundary discussion were completed.
- [x] Team directory, invite team member, and invitation management remain one correlated function.
- [x] Invitation acceptance through mailbox remains a separate later flow.
- [x] Requirements are mapped to executable cases or governed gaps without copying PRD narratives.
- [x] Current UI and APIs were inspected and dated.
- [x] Stable case/dataset IDs and deterministic synthetic mailboxes are allocated.
- [x] Browser actions are not claimed when API setup performs the prerequisite.
- [x] Tokens, credentials, raw invitation links, and real patient data are absent.
- [ ] Every executable case has completed controlled deterministic validation.
- [ ] Human review has resolved current PRD/UI discrepancies and any validation failures.
- [ ] Cases have received activation approval.
