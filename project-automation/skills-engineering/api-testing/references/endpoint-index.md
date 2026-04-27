# Endpoint Index

Use this index before opening endpoint profiles. Open only the matching profile for the endpoint under test. Add short live notes here when they affect endpoint selection or prevent repeated mistakes.

| Method | Path | Profile | Purpose | Auth | Tags | Live Notes |
|---|---|---|---|---|---|---|
| POST | `/auth/login` | `endpoint-profiles/post-auth-login.md` | Authenticate patient, provider, or admin and capture token/profile IDs | None | auth, token | `profile_type` is required. Use `provider` for provider users and clinicians. |
| POST | `/inquiry/create-inquiry` | `endpoint-profiles/post-inquiry-create-inquiry.md` | Create a patient inquiry with scan image upload and date ranges | Patient | inquiry, patient, image-upload | Use `assets/sample-hair-photo.jpg` for `scan_url[0][image]` unless the user provides another image. |
| GET | `/treatment/get-all-treatments-with-packages` | `endpoint-profiles/get-treatment-get-all-treatments-with-packages.md` | Resolve provider treatment and package IDs for quote creation | Provider | treatment, package, quote | Live test treatments may use `status=in_progress`; quote creation accepts this as active. |
| GET | `/provider-user/get-all-clinicians` | `endpoint-profiles/get-provider-user-get-all-clinicians.md` | Resolve provider-scoped clinician IDs for quote creation | Provider | clinician, provider, quote | Correct clinician resolver for quote flows. Do not use `/provider/get-provider-staff` for this purpose; it returned `Unauthenticated` in live testing even with provider token. |
| POST | `/quote/create-quote` | `endpoint-profiles/post-quote-create-quote.md` | Create one provider quote with treatment date options | Provider | quote, treatment-dates, clinicians | If using clinicians, resolve them with the same provider token via `/provider-user/get-all-clinicians` and prefer `status=active`. |

## Maintenance

- Keep this file concise; put detailed request/response behavior in endpoint profiles.
- When a run discovers a reusable endpoint lesson, add one short note here and the full detail in the endpoint profile.
- If a profile is missing, research the endpoint, propose a new profile, and add an index row only after user confirmation.
