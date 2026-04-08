# Secrets Scan Report — project-automation

**Scan date:** 2026-02-13  
**Scope:** `local-docs/project-automation` (skills, scripts, commands, workflows, task-prompt, logs)

## Summary

**No API keys or secrets are hardcoded** in the scanned folder. All credential handling uses environment files and placeholders only.

---

## Checks Performed

| Check | Result |
|-------|--------|
| Plane API key pattern (`plane_api_` + long string) | No matches |
| Stripe-style keys (`sk_`, `pk_` + long string) | No matches |
| Bearer tokens | No matches |
| `X-API-Key:` with long value | No matches |
| `password` / `secret` / `api_key` = "…" (long value) | No matches |
| `token` / `private_key` = "…" (long value) | No matches |
| `.env` file in repo (under project-automation) | None found (correct; .env lives under project-automation/task-creation/plane-api and should be gitignored) |

---

## Findings (All Safe)

### 1. Scripts (`skills-engineering/plane-api-commands/scripts/`)

- **create-plane-issues.py**  
  - Loads credentials via `load_env(env_path)` from `.env`.  
  - Uses `config['PLANE_API_KEY']` (variable).  
  - Error message uses placeholder: `"PLANE_API_KEY=plane_api_..."` (no real key).

- **update-plane-issues.py**  
  - Same pattern: load from `.env`, use variable, placeholder only in messages.

### 2. Documentation (SKILL.md, commands, workflows, README)

- All references to `PLANE_API_KEY` are:
  - Variable names or instructions to “load from .env”.
  - Placeholder in examples: `PLANE_API_KEY=plane_api_...` (ellipsis, not a key).
- No actual key values found.

### 3. UUIDs (Project / Assignee / Stage / Issue Type IDs)

- **Present in:** README.md, task-prompt/plane-api-commands.md (and samasu-system-variables.md).
- **Values:** e.g. `PROJECT_ID=ff2d96b2-0ab2-438b-b879-fbdaa078dbd6`, `ASSIGNEE_ID=…`, etc.
- **Assessment:** These are **resource identifiers** (which project/state/assignee/type to use), not authentication secrets. They are required for API calls and are treated as non-secret in Plane’s model; no change needed.

### 4. `.env` Usage

- All mentions of `.env` are:
  - Paths (e.g. `project-automation/task-creation/plane-api/.env`).
  - Instructions to load from file / not hardcode.
- No `.env` file content is embedded in the repo under `project-automation`.

---

## Recommendations

1. **Keep current practice:** Continue loading `PLANE_API_KEY` and other secrets only from `.env`; never commit real keys.
2. **Keep `.env` out of git:** Ensure `project-automation/task-creation/plane-api/.env` (and any other `.env`) is listed in `.gitignore`.
3. **Optional:** Add a one-line note in README or SKILL that the UUIDs (PROJECT_ID, ASSIGNEE_ID, etc.) are resource IDs, not secrets, and are safe to document.

---

## Conclusion

**No API keys or other secrets are hardcoded** in skills, scripts, commands, workflows, or other files under `local-docs/project-automation`. Credential handling is safe and consistent with “never copy .env secrets into scripts or files.”
