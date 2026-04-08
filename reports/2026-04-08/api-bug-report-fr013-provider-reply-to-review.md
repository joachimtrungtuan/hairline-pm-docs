# API Bug Report — FR-013: Provider Reply to Review

**Date:** 2026-04-08  
**Tested by:** QA (automated via Claude Code API testing)  
**Feature:** FR-013 Review Management — Provider response to patient review  
**Environment:** Production API — `https://backend.hairline.app/api`

---

## Summary

Two bugs were found while testing the provider-reply-to-review flow (Flow 11, FR-013). The core `POST` endpoint for submitting a provider response works correctly. However, providers cannot list their own reviews, and patients cannot see provider responses in their review feed.

| # | Bug | Severity | Endpoint |
|---|-----|----------|----------|
| B1 | `GET /provider/reviews` returns 404 | High | `GET /provider/reviews` |
| B2 | Patient review feed does not include provider response | High | `GET /patient/reviews` |

---

## Test Setup

### Accounts Used

| Role | Email | Account ID |
|------|-------|------------|
| Provider (V3) | test_provider3@clinic.com | — |
| Patient (P1) | joachimtrungtuan.work@gmail.com | — |
| Patient (P2) | trung.dang@vantaymedia.com | — |

### Reviews Used

| Review ID | Written by | Directed at |
|-----------|-----------|-------------|
| `518ad03d-f43b-4372-bd91-b20883807f14` | P1 (joachimtrungtuan.work@gmail.com) | V3 |
| `9e2a78a7-2309-42b0-8adf-382cf42e9cea` | P2 (trung.dang@vantaymedia.com) | V3 |

### Provider Responses Posted (confirmed saved to DB)

| Response ID | Review | Posted at |
|-------------|--------|-----------|
| `edd595f3-f877-4b9e-8ca9-904af113ce45` | `518ad03d-...` (P1) | 2026-04-08T09:48:36Z |
| `cb4d0b6e-1745-46cf-ba0d-ff0b77349038` | `9e2a78a7-...` (P2) | 2026-04-08T09:49:14Z |

---

## What Works

`POST /provider/reviews/{id}/respond` — **working correctly.**

```
POST https://backend.hairline.app/api/provider/reviews/518ad03d-f43b-4372-bd91-b20883807f14/respond
Authorization: Bearer {V3_TOKEN}
Body (JSON): { "response_text": "Thank you for your kind review!..." }

→ 200 OK
→ Response ID created: edd595f3-f877-4b9e-8ca9-904af113ce45
```

> **Note:** The request body field is `response_text` (not `response`). Update collection/docs accordingly.

---

## Bug B1 — `GET /provider/reviews` Returns 404

### Description

The provider has no way to list the reviews they have received. The endpoint is documented in the collection map but is not reachable on the server.

### Steps to Reproduce (Postman)

**Step 1 — Login as Provider V3**

```
POST https://backend.hairline.app/api/auth/login
Body (JSON):
{
  "email": "test_provider3@clinic.com",
  "password": "password",
  "profile_type": "provider"
}
```
Copy the `token` from the response.

**Step 2 — Fetch provider reviews**

```
GET https://backend.hairline.app/api/provider/reviews
Authorization: Bearer {token from step 1}
```

### Expected vs Actual

| | Result |
|-|--------|
| **Expected** | 200 OK with a paginated list of reviews for this provider |
| **Actual** | 404 Not Found |

### Impact

Providers cannot see their reviews from within the app. The "Post Response" flow is also blocked in practice — a provider cannot know which review IDs exist without this list endpoint.

---

## Bug B2 — Patient Cannot See Provider Response in Review Feed

### Description

After a provider successfully posts a response to a review, the patient's review feed (`GET /patient/reviews`) does not include the provider response in the review object. The response is confirmed saved to the database (via `POST /provider/reviews/{id}/respond` returning 200 with a response ID), but the patient-facing endpoint does not return it.

### Steps to Reproduce (Postman)

**Pre-condition:** Provider V3 has already responded to review `518ad03d-f43b-4372-bd91-b20883807f14` (response posted at 2026-04-08T09:48:36Z, response ID `edd595f3-f877-4b9e-8ca9-904af113ce45`).

**Step 1 — Login as Patient P1**

```
POST https://backend.hairline.app/api/auth/login
Body (JSON):
{
  "email": "joachimtrungtuan.work@gmail.com",
  "password": "1234567890@Abc",
  "profile_type": "patient"
}
```
Copy the `token` from the response.

**Step 2 — Fetch patient reviews**

```
GET https://backend.hairline.app/api/patient/reviews
Authorization: Bearer {token from step 1}
```

Find the review object with `"id": "518ad03d-f43b-4372-bd91-b20883807f14"`.

### Expected vs Actual

| | Result |
|-|--------|
| **Expected** | Review object contains a `provider_response` field with the response text and metadata |
| **Actual** | Review object has no `provider_response` field — the response data is entirely absent |

**Actual response fields returned:**
`id`, `provider`, `treatment`, `rating`, `facility_rating`, `staff_rating`, `results_rating`, `value_rating`, `review`, `photos`, `status`, `date`, `country`, `created_at`, `updated_at`

**Missing:** `provider_response` / `providerResponse`

### Second Data Point (P2)

Same result with Patient P2:

```
POST https://backend.hairline.app/api/auth/login
Body: { "email": "trung.dang@vantaymedia.com", "password": "1234567890@Abc", "profile_type": "patient" }

GET https://backend.hairline.app/api/patient/reviews
→ Review 9e2a78a7-2309-42b0-8adf-382cf42e9cea has no provider_response field
  (Provider response ID cb4d0b6e-1745-46cf-ba0d-ff0b77349038 confirmed saved)
```

### Impact

Patients cannot see provider responses at all. The feature is non-functional from the patient's perspective.

### Root Cause Hint (for dev)

The `ReviewProviderResponse` model and its `hasOne` relationship on `Review` exist in the backend. The patient reviews query is likely missing the eager load. Check the `with([...])` clause in the query powering `GET /patient/reviews` and add the `providerResponse` relationship. The transform/resource also needs to expose the field.

---

## Summary Table

| # | Endpoint | Account | Status | Expected | Actual |
|---|----------|---------|--------|----------|--------|
| — | POST /provider/reviews/{id}/respond | V3 | **200 OK** | Response saved | Works correctly |
| B1 | GET /provider/reviews | V3 | **404** | Review list | Not found |
| B2 | GET /patient/reviews | P1, P2 | **200 OK** | Includes `provider_response` | Field missing |
