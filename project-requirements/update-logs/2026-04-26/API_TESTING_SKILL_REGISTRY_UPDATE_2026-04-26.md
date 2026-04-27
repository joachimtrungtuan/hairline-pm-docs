# API Testing Skill Registry Update - 2026-04-26

## Summary

Added endpoint and flow registry references for the Hairline API testing skills to reduce repeated endpoint discovery and preserve live API findings across sessions.

## Changes

- Added endpoint index and endpoint profiles under `api-testing/references/`.
- Added flow index and migrated Create Quote flow profile under `api-flow-testing/references/`.
- Documented the correct provider-scoped clinician resolver: `GET /provider-user/get-all-clinicians`.
- Documented that `/provider/get-provider-staff` should not be used for Create Quote clinician lookup because it returned `Unauthenticated` during live testing with provider tokens.
- Added Create Quote prerequisites requiring clinician lookup when clinician assignment is part of the run.
- Added explicit file-upload guidance so image endpoints use bundled files from `api-testing/assets/`, including `sample-hair-photo.jpg` for inquiry scan upload.

## Files

- `local-docs/project-automation/skills-engineering/api-testing/references/endpoint-index.md`
- `local-docs/project-automation/skills-engineering/api-testing/references/endpoint-profiles/post-auth-login.md`
- `local-docs/project-automation/skills-engineering/api-testing/references/endpoint-profiles/post-inquiry-create-inquiry.md`
- `local-docs/project-automation/skills-engineering/api-testing/references/endpoint-profiles/get-treatment-get-all-treatments-with-packages.md`
- `local-docs/project-automation/skills-engineering/api-testing/references/endpoint-profiles/get-provider-user-get-all-clinicians.md`
- `local-docs/project-automation/skills-engineering/api-testing/references/endpoint-profiles/post-quote-create-quote.md`
- `local-docs/project-automation/skills-engineering/api-flow-testing/references/flow-index.md`
- `local-docs/project-automation/skills-engineering/api-flow-testing/references/flow-profiles/create-quote.md`
