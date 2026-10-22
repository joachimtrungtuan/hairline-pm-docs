# Subagent Engines

How the main agent runs checkers, verifiers, and jurors on the engine and model the user picked
in preflight. Every engine receives the same brief text and must return the same YAML schema;
validation (Step 5.3) is identical whatever ran the unit.

## Why this is a preflight choice

The main session's model is not the right default for a fan-out of hundreds of agents. On the
2026-10-21 Phase 1 run, Opus subagents drained the usage quota, and general-purpose agents
started each unit at roughly 50k tokens, mostly the MCP tool catalog. The user decides engine
and model per run because cost, quota, and independence trade off differently each time.

## Engine options (offer these in the engine question)

| Engine | How it runs | Probes | Notes |
|---|---|---|---|
| Claude `code-reviewer`, Sonnet | Agent tool, `subagent_type: "code-reviewer"`, `model: "sonnet"` | yes | Recommended default for checkers and verifiers. |
| Claude `code-reviewer`, Haiku | same, `model: "haiku"` | yes | Cheapest. Weaker on cross-file authorization and contract checks; expect more false positives, and every false positive costs one verifier. |
| Claude `code-reviewer`, Opus | same, `model: "opus"` | yes | Highest cost; use for small scopes or a P0-only slice. |
| Codex headless (OpenAI) | `codex exec` via Bash, see below | static only | Uses the user's ChatGPT login. Different model family, so it is the natural jury engine when checkers ran on Claude. |
| OpenCode headless | `opencode run` via Bash, see below | static only | Any `provider/model` that OpenCode can route. Must pass the canary first. |

Ask for checkers and verifiers in one question, and allow "checkers on X, verifiers on Y" as a
free-text answer. Never pick for the user silently, including in Resume, Delta, and Jury mode.

## Tool use, for every engine

Put this in the prompt (the briefs already contain it): use no MCP tool, ToolSearch, or skill by
default; call one only when a finding needs evidence that source reading and `curl` cannot give
(for example, a Postman request that needs the collection's auth setup). Follow the brief, not
the agent's own default review workflow, and write no files.

## Claude `code-reviewer`

The `code-reviewer` agent definition defaults to Opus and tells itself to run a `code-review`
skill and write reports. Always pass `model` explicitly, and start the prompt with: "Follow only
the brief below. Do not invoke any skill, do not run builds, linters, or tests, and do not write
any file. Return only the YAML." Never use `general-purpose` for review work.

## External engines (Codex, OpenCode)

External engines run outside Claude Code's permission system, so their safety comes from their
own sandbox. Rules:

- **Read-only.** Codex always runs with `--sandbox read-only`. OpenCode runs with a deny-edit,
  deny-shell-except-read config. Never pass `--auto`, `--dangerously-bypass-approvals-and-sandbox`,
  or any write sandbox. `main/` must stay untouched.
- **Credential-blind.** Never paste or point to `local-docs/testing/test-data/credentials/`,
  tokens, or `.env` files in an external prompt. Staging probes are therefore off for external
  engines: they judge statically, and anything that needs a live call returns `Needs runtime`.
- **Absolute paths.** The engine runs in a scratch working folder, so start the prompt with
  "The workspace root is `<absolute path>`; every relative path below is relative to it." and
  give the PRD and code-map paths in absolute form.
- **Canary before the run.** Once per run, before the first unit, run a canary prompt that asks
  the engine to (1) create a file, (2) `touch` a file, and (3) `rg` one line from
  `main/hairline-backend/composer.json`. Proceed only if (1) and (2) fail, (3) succeeds, and no
  file appears in the scratch folder. If the canary fails, record it under Method deviations and
  fall back to the Claude engine the user named as fallback in the engine question (ask for a
  fallback whenever an external engine is chosen).
- **Concurrency.** Run each call as a background Bash command writing to
  `<scratchpad>/engine-out/<unit ID>.jsonl`; keep at most the approved cap in flight.
- **Return.** Extract the final agent message, then validate it exactly like a Claude return.
  A non-zero exit, quota error, or unparseable output counts as one failure (Step 5.3).

### Codex

```bash
codex exec --sandbox read-only --skip-git-repo-check -C "<scratch>/cxwork" --json \
  -c 'mcp_servers={}' [-m <model>] [-c model_reasoning_effort=<low|medium|high>] \
  "<brief + unit block + PRD excerpt + pointers>" < /dev/null > "<scratch>/engine-out/<id>.jsonl"
```

The final answer is the last `item.completed` event whose `item.type` is `agent_message`. The
`turn.completed` event carries `usage`; keep it for the cost line in the report. Observed on
2026-10-22: login via ChatGPT works, the read-only sandbox blocks writes, and each call carries
about 40k input tokens of fixed overhead even with MCP servers disabled.

### OpenCode

OpenCode reads the global config plus `.opencode/opencode.json` in the working folder
(`OPENCODE_CONFIG` is ignored in v2.x). Create `<scratch>/ocwork/.opencode/opencode.json`:

```json
{"$schema":"https://opencode.ai/config.json",
 "permissions":[
  {"action":"edit","resource":"*","effect":"deny"},
  {"action":"webfetch","resource":"*","effect":"deny"},
  {"action":"shell","resource":"*","effect":"deny"},
  {"action":"shell","resource":"rg *","effect":"allow"},
  {"action":"shell","resource":"git -C *","effect":"allow"}]}
```

Then run from that folder:

```bash
opencode run -m <provider/model> --format json "<prompt>" < /dev/null > "<scratch>/engine-out/<id>.jsonl"
```

The answer is the concatenated `part.type == "text"` events; an `error` event (for example
`provider.no-route` or `provider.quota`) is a failure. On 2026-10-22 no OpenAI route in OpenCode
was funded, and disabling the global MCP servers from the working-folder config was not
confirmed, so prefer Codex for OpenAI models until an OpenCode canary passes.
