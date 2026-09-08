# CCDV-F Question Authoring Spec — READ FULLY BEFORE WRITING

You are authoring exam questions for the **Claude Certified Developer – Foundations (CCDV-F)** practice bank. A student is paying for this exam. **A wrong answer key actively teaches them the wrong thing.** Accuracy outranks volume.

---

## 1. Output format — EXACT

Write ONE file containing ONE `QB.push(...)` call. No HTML, no `<script>` tags, no markdown fences around it. Plain JavaScript:

```
QB.push(
{id:1001,d:"D1",s:"Claude API Mechanics",t:"S",f:"M",
q:"Question stem text?",
o:["A. First option","B. Second option","C. Third option","D. Fourth option"],a:2,
e:"Explanation that teaches the concept.",
w:"A — why A is wrong. B — why B is wrong. D — why D is wrong."},

{id:1002,d:"D1",s:"Streaming",t:"R",f:"E",
q:"...",
o:["A. ...","B. ...","C. ...","D. ..."],a:0,
e:"...",
w:"B — ... C — ... D — ..."}
);
```

### Field rules
| Field | Rule |
|---|---|
| `id` | Integer. **Use ONLY your assigned range.** Never reuse or overlap. |
| `d` | Domain code exactly: `"D1"`…`"D8"` |
| `s` | Sub-skill string — **copy verbatim from `subskills.md`**. Do not invent new ones. |
| `t` | `"S"` = scenario, `"R"` = recall |
| `f` | `"E"` easy, `"M"` medium, `"H"` hard |
| `q` | The stem. `\n` for newlines. Use ` ``` ` fences for code blocks, backticks for inline code. |
| `o` | **Exactly 4** options, each prefixed `"A. "`, `"B. "`, `"C. "`, `"D. "` in that order |
| `a` | 0-based index of the correct option |
| `e` | Explanation (see §4) |
| `w` | Why the other three fail (see §5) |

### Escaping — this breaks builds if you get it wrong
- The file is evaluated as JS. Inside double-quoted strings, escape inner double quotes: `\"`
- Prefer backticks for inline code in prose: `` `stop_reason` `` — do NOT use double quotes around code
- No trailing comma after the last object before `)`
- No template literals, no comments inside the array

---

## 2. Your quota and mix

- Hit your assigned question count.
- **70% scenario (`t:"S"`) / 30% recall (`t:"R"`)** across your batch.
- Difficulty spread roughly **15% E / 50% M / 35% H**. Exam-realistic, tuned slightly hard.
- **Spread `a` values evenly across 0, 1, 2, 3.** Roughly a quarter each. Do not park the answer at one index — count them before finishing.

---

## 3. Scenario questions — what "exam-realistic" means

A scenario stem gives a **concrete situation with enough detail to reason from**, then asks for the correct engineering judgement. Model these:

> "A nightly job fires thousands of concurrent requests and takes a wave of 429s. Every worker retries after exactly 2 seconds. Throughput stays terrible. What is the flaw?"

> "A team enables prompt caching and total spend rises. `usage` shows high `cache_creation_input_tokens` and low `cache_read_input_tokens`. What is the economic explanation?"

Good scenarios include realistic numbers, a symptom, and a plausible-but-wrong instinct as a distractor. **Bad** scenario stems are recall questions with "A developer wants to…" bolted on the front.

Distractors must be **plausible to someone who half-knows the material** — common misconceptions, adjacent-but-wrong mechanisms, right-idea-wrong-parameter. Never filler or joke options.

---

## 4. The `e` explanation — this is the product

The student is using this to **learn**, not just to be graded. Each explanation must:
- State *why* the correct answer is correct, mechanically
- Name the specific parameter / field / event / status code involved, in backticks
- Give the **transferable principle** where one exists ("the model proposes, deterministic code authorises")
- Where a fact is **version-sensitive**, say so explicitly (see §6)

Length: roughly 60–130 words. Dense and specific. Use `**bold**` for the key term. Do not pad, do not restate the question, do not moralise.

---

## 5. The `w` field — REQUIRED FORMAT

Explain why each incorrect option fails, referencing options **by letter followed by an em dash**:

```
w:"A — temperature controls randomness, not length. B — a stop sequence would truncate earlier, worsening it. D — it is deterministic, so retrying reproduces it."
```

**Critical:** the app randomises option order and rewrites these letter references automatically. It recognises exactly these forms:
- `A — reason` (letter, space, em dash `—`)
- `A/C — reason` (slash-joined)
- `A, B, and D — reason` (comma list)
- `Option A`

Use **only** those forms. Do NOT write "the first option", "answer (a)", "choice A:", or a colon instead of an em dash — the remapper will miss it and the student will see a reference to the wrong option.

Cover all three wrong options. Combine with a slash only when the reason genuinely is identical.

---

## 6. VERIFIED CURRENT FACTS — do not contradict these

Five fact-check passes against live `platform.claude.com/docs` found **57 errors** in earlier questions written from model recall. Your training data is behind. These are the corrected facts. **Questions contradicting anything below will be rejected.**

**API basics**
- Request identifier header is **`request-id`** — NOT `x-request-id`. Also a top-level `request_id` in error bodies.
- **Both** `Authorization: Bearer <token>` and legacy `x-api-key` are valid credential headers. `anthropic-version` and `content-type: application/json` are required.
- Endpoint `POST /v1/messages`. Required body: `model`, `max_tokens`, `messages`.
- Roles in `messages`: `user`, `assistant`. Some newer models additionally accept a `system` role **mid-conversation** (never as `messages[0]`). Top-level `system` param is the way to set instructions from turn one.
- Tool results go in a **`user`** message as `tool_result` blocks with matching `tool_use_id`. No `tool` role. Unmatched `tool_use` id → **400**.
- `tool_result.content` may be an **array of content blocks, including images**.

**stop_reason — SEVEN values, extensible**
`end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `pause_turn`, `refusal`, `model_context_window_exceeded`. The **versioning policy permits the enum to grow**, so clients need a default branch. Detect refusals via `stop_reason: "refusal"`, not string matching.

**Errors**
400 `invalid_request_error` · 401 `authentication_error` · 402 `billing_error` · 403 `permission_error` · 413 `request_too_large` · 429 `rate_limit_error` · 500 `api_error` · 529 `overloaded_error`. Body: `{"type":"error","error":{"type":..,"message":..},"request_id":..}`. Configured org/workspace spend limit → **400**; usage-tier monthly cap → **429**.

**Rate limits**
Dimensions: requests/min, **input** tokens/min, **output** tokens/min. Headers: `anthropic-ratelimit-*`; `retry-after` on 429. **`max_tokens` does NOT factor into output-token rate limits** — lowering it relieves no throttling.

**DEPRECATED — these now 400**
- `temperature`, `top_p`, `top_k` are **deprecated and rejected with 400** on models after Opus 4.6. Steer with `output_config.effort` (`low`/`medium`/`high`/`xhigh`/`max`) and prompting instead. Where still supported, temperature range is 0.0–1.0, default 1.0, and output is **not fully deterministic even at 0**.
- **Assistant prefill returns 400** on Claude 4.6+ ("does not support assistant message prefill"). The `{`-prefill trick is dead — know it as legacy, never recommend it.
- Extended thinking `thinking:{type:"enabled", budget_tokens:N}` **removed on 4.7+ → 400**. Current mechanism is adaptive thinking + `output_config.effort`. On some models thinking cannot be disabled.

**Structured output — NATIVE feature exists**
`output_config.format` = `{"type":"json_schema","schema":{...}}` guarantees schema-valid output via **constrained decoding**. No beta header. Tool-side equivalent is **`strict: true`** on a tool definition. This **supersedes** the old "force a schema-bearing tool" workaround. Forced `tool_choice` (`any`/`tool`) errors under manual extended thinking and 400s on some models; `auto` and `none` always work.

**Prompt caching**
`cache_control: {"type":"ephemeral"}` on the block ending the cacheable prefix; a **top-level `cache_control`** also exists and auto-places the breakpoint. Cacheable prefix order: **tools → system → messages**. Max **4 breakpoints** (5th → 400). TTL **5 min, refreshed on each read**; **1-hour** option available. Cost: write **1.25×** base input (2× for 1h), read **0.1×**. Minimum cacheable length varies by model. Prefix must be **byte-identical**; changing `tool_choice` invalidates cached **message** blocks (tools/system stay cached). `usage` reports `cache_creation_input_tokens` / `cache_read_input_tokens`.

**Streaming**
`"stream": true`. Events: `message_start`, `content_block_start`, `content_block_delta`, `content_block_stop`, `message_delta`, `message_stop`, plus `ping` and `error`. Deltas: `text_delta`, `input_json_delta` (concatenate `partial_json` before parsing), `thinking_delta`. **Final `stop_reason` and cumulative output usage arrive in `message_delta`**, not `message_stop`. Every block event carries an **`index`** — accumulate per index.

**Batch API**
`/v1/messages/batches`. ~**50% discount**. Completes within **24 hours**. Limits **100,000 requests or 256 MB**, whichever first. Each request needs a **`custom_id`** (results are JSONL, not order-guaranteed). Per-request statuses: `succeeded`, `errored`, `canceled`, `expired`. Batch `processing_status: "ended"` ≠ all succeeded. Use the **1-hour cache TTL** for batches, since the 5-min default can expire mid-batch.

**Vision / documents**
Formats JPEG, PNG, GIF, WebP. **Three** source types: `base64`, `url`, `file` (Files API `file_id` — preferred for multi-turn, since statelessness means resending bytes every turn). Cost is **visual tokens in 28×28 patches**: `⌈w/28⌉ × ⌈h/28⌉`. The old `(w×h)/750` formula is **gone**. Long-edge limit ~1568 px on older models, ~2576 px on newest. Claude does **not generate images**. Native PDF support: **32 MB, 600 pages** (100 when context under 1M). On **Amazon Bedrock and Google Cloud, only `base64`** image sources are available.

**Context & tokens**
Context window bounds request **plus generated output including thinking tokens** — output is not a separate budget. `max_tokens` is an additional output cap; above the model ceiling → **400**, no silent clamping. Overflow during generation → `stop_reason: "model_context_window_exceeded"`. Flagship context ~**1M tokens**, smallest tier 200K. `/v1/messages/count_tokens` is **free**, tokenizer-specific, and returns an **estimate**. Newer tokenizer ≈ **30% more tokens** than older (~2.5 chars/token vs ~4).

**Models**
Tiers: Haiku (fastest/cheapest) → Sonnet (balanced speed+intelligence) → Opus (complex agentic/enterprise) → a higher tier above Opus for the most demanding reasoning. Output priced above input. **No `-latest` aliases**: current IDs are **dateless and each is a pinned snapshot** — never append a date suffix. Weights fixed per ID, but **serving infrastructure can change**, so pinning gives stability not bit-identical output. Available on **Amazon Bedrock, Google Cloud, and Microsoft Foundry (Azure)** plus first-party. **7 SDKs**: Python, TypeScript, C#, Go, Java, PHP, Ruby.

**Tools**
Fields `name`, `description`, `input_schema` (JSON Schema, root `type:"object"`). Name regex **`^[a-zA-Z0-9_-]{1,64}$`**. `tool_choice`: `{"type":"auto"|"any"|"tool"|"none"}`, plus `disable_parallel_tool_use`. Tool definitions are **billed as input tokens every request**, plus a fixed tool-use system prompt overhead. **`defer_loading`** + the **tool search tool** excludes deferred tools from context **entirely (not even names)** — but you still transmit all definitions in `tools` each request; at least one tool must have `defer_loading:false` or 400. Prefer improving descriptions and consolidating over adding tools.

**MCP**
Open standard, **JSON-RPC 2.0**. Server primitives: **Tools, Resources, Prompts** (prompts are **user-controlled**; no protocol versioning field). Transports: **stdio** and **Streamable HTTP** (which **replaced** the older HTTP+SSE). Methods `tools/list`, `tools/call`, `resources/list`, `resources/read`, `prompts/list`, `prompts/get`. Long-running work uses the **Tasks extension**, which defines exactly **three** methods — **`tasks/get`**, **`tasks/update`**, **`tasks/cancel`** (statuses `working`/`input_required`/`completed`/`failed`/`cancelled`); the final payload arrives in the `result` field of a `tasks/get` response. **`tasks/result` and `tasks/list` do NOT exist** — removed in the stateless redesign, they answer `-32601`. Also use **`notifications/progress`** with a `progressToken`. Further currency notes: **sampling and roots are deprecated** (only **elicitation** remains current among client primitives); **servers no longer initiate JSON-RPC requests** — server→client interaction is an `InputRequiredResult` carrying `inputRequests`, which the client fulfils by retrying with `inputResponses`; **capability negotiation is per-request, not an `initialize` handshake** (`_meta` carries `protocolVersion`/`clientCapabilities`, servers MUST implement `server/discover`, mismatch → `-32022`); Streamable HTTP **removed** the standalone GET stream and protocol-level `Mcp-Session-Id` (GET/DELETE → 405); protocol-level `notifications/message` logging is deprecated in favour of stderr/OpenTelemetry. Return **structured error envelopes**: category, retryability, alternatives.

**Agent patterns (Anthropic's "Building effective agents" taxonomy)**
The building block is the **augmented LLM** (retrieval + tools + memory). **Workflows** (predefined code paths): prompt chaining, routing, parallelisation (**sectioning** and **voting**), **orchestrator-workers**, evaluator-optimiser. **Agents** = the LLM **directs its own process and tool usage**. Note: **orchestrator-workers is classified a WORKFLOW**, not an agent, despite runtime decomposition. The API is **stateless** — resend the full accumulated history on every iteration.

**Claude Code**
`CLAUDE.md` auto-loaded. **4 memory scopes, CONCATENATED (not overriding), broad→specific**: managed policy (cannot be excluded) → user (`~/.claude/CLAUDE.md`) → project (`./CLAUDE.md` or `./.claude/CLAUDE.md`) → local (`./CLAUDE.local.md`, gitignored). `.claude/rules/` splits instructions, **path-scopeable** via `paths:` frontmatter. `.claude/settings.json` holds permissions, hooks, env. Hooks are **shell command OR HTTP endpoint** handlers across **~32 events** — key ones **PreToolUse** (can block) and **PostToolUse**, plus `SessionStart`, `UserPromptSubmit`, `PreCompact`/`PostCompact`, `Stop`. Subagents get **own context window, own system prompt, own tool permissions**. **Custom commands merged into skills** — `.claude/commands/x.md` and `.claude/skills/x/SKILL.md` both give `/x`; skill wins; skills recommended. Claude Code **auto-compacts** (clears old tool output, then summarises); `/compact [focus]` is the manual trigger.

**Security principles**
The model is **not a security boundary**. Prompt instructions are advisory; enforce in code. Treat model-supplied tool arguments as **untrusted input**; authorise against the **authenticated session**, never an identity the model asserts. **Indirect prompt injection** arrives via retrieved/fetched content. Untrusted content goes in a `user` message inside tags labelled as data — **never** in the system prompt, which elevates its authority. Separate trust domains so the component reading untrusted content lacks sensitive access and outbound channels. Least privilege on tools bounds blast radius.

### ⚠ Verification method warning (found during B12)
**WebFetch page *summaries* can fabricate content.** An intermediate summary of the structured-outputs page invented an entire "Compatibility" section claiming structured outputs is incompatible with streaming, `tool_choice`, and extended thinking. A verbatim re-fetch showed **no such section** — the page in fact says grammars apply to Claude's direct output but not thinking blocks, i.e. extended thinking *is* compatible. **Always re-fetch for verbatim text before asserting a fact that would change an answer key.** Do not trust a single summarised read.

**Corrections to earlier guidance in this spec**
- **Cache scope is NOT per API key.** Caches are isolated **between organisations**, and **per workspace** within an organisation on the Claude API, Claude Platform on AWS, and Microsoft Foundry; Bedrock and Google Cloud use **organisation-level isolation only**. Any claim of per-key scoping is wrong.
- **Pre-warming is a documented, supported feature**, not an anti-pattern: an official pre-warm uses **`max_tokens: 0`** (returns empty `content`, `stop_reason: "max_tokens"`, populated `usage`). It is rejected *inside* a Message Batches request. What *is* an anti-pattern is perpetual synthetic keep-alive pinging to hold a cache warm — use the 1-hour TTL instead.
- Further caching detail: there is a **20-block lookback window** for breakpoint placement; TTL is measured from **request start**; **cache hits are not deducted against rate limits**; `cache_creation` carries a per-TTL breakdown object; longer TTLs must be ordered before shorter ones; and images, `output_config.effort`, and thinking changes are **message-scoped** invalidators, while a tool-definition change invalidates the **whole** prefix and `max_tokens` invalidates **nothing**.
- **Structured outputs schema subset**: `additionalProperties: false` required on all objects; every non-optional property must appear in `required`. Rejected with a detailed 400: recursive schemas, external `$ref`, `minimum`/`maximum`/`multipleOf`, `minLength`/`maxLength`, array constraints beyond `minItems` 0/1, complex types in `enum`. The Python/TS/Ruby/PHP SDKs transform your schema (stripping unsupported constraints into `description`, injecting `additionalProperties: false`) and then **validate the response against your original schema**. Compiled grammars are cached **24 h from last use**, invalidated by schema-structure or tool-set changes but **not** by editing only `name`/`description`.

**Additional verified details** (confirmed during batches B02, B06, B08, B13)
- **Error codes — §6's list above is incomplete.** Also documented: **404 `not_found_error`**, **409 `conflict_error`**, and **504 `timeout_error`** (whose doc guidance is to use streaming for long-running requests). 504 is retryable.
- **A fourth streaming delta type exists: `signature_delta`**, emitted once immediately before `content_block_stop` on a thinking block. Also: `message_delta` usage counts are **cumulative** (explicit doc warning), and fine-grained tool streaming is enabled per tool via **`eager_input_streaming`**.
- **Thinking tokens are a subset of `max_tokens`**, billed as output and counting toward rate limits.
- **Window-overflow arithmetic has two distinct branches**: input **alone** exceeding the window is a **400 `invalid_request_error`**; but input + `max_tokens` exceeding it is **accepted**, and generation then stops with `stop_reason: "model_context_window_exceeded"`.
- **`usage` input fields are mutually exclusive**: `input_tokens` counts tokens *neither* read from *nor* written to cache, so true total input = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`. A dashboard summing `input_tokens` alone under-reports.
- **Cache break-even is one read** at the 5-minute TTL (1.25× write) and **two** at 1-hour (2× write). The tempting wrong inference — "a read is 0.1× so I need ten reads" — is wrong because the write premium is only 0.25× above baseline. The full ~1M window bills at **standard** rates with no long-context surcharge.
- **Batch specifics**: `processing_status` flows `in_progress` → `canceling` → `ended`; `request_counts` breaks down as `processing`/`succeeded`/`errored`/`canceled`/`expired`; `custom_id` regex `^[a-zA-Z0-9_-]{1,64}$`; results retained **29 days** from `created_at`; `params` validation is **asynchronous**; unsupported in batch: `stream: true`, `speed`, `max_tokens: 0`; batches may **slightly exceed** a configured workspace spend limit; the Batches API has its own RPM and queue limits that do **not** consume Messages API limits.
- **Tools**: a **deferred tool cannot carry `cache_control`** (400 — put the breakpoint on a non-deferred tool). **`strict: true` requires `additionalProperties: false`**, and numeric/string-length constraints fall outside the supported schema subset. Compiled strict schemas are cached separately (~24h) from message content, so **PHI must not appear in schema property names, `enum`/`const` values, or `pattern` regexes**. The `defer_loading` error text is `At least one tool must have defer_loading=false.`
- **No API-level idempotency key exists** for the Messages API — idempotency and deduplication belong in your gateway or tool layer, not asserted as an API feature.
- Anthropic's term for long-context degradation is **"context rot"**.

**Additional verified vision/document details** (confirmed against live docs during batch B04)
- Resolution tiers are defined by **two** limits, and the **token limit usually binds first**: standard = 1568 px long edge / **1568 visual tokens**; high-resolution (newest models) = 2576 px / **4784 visual tokens**. High-res is automatic, no beta header. Example: 1920×1080 resizes to 1456×819, *not* 1568×882.
- Images are padded to the next multiple of 28 px on the **bottom and right only**; normalise any coordinate work by the **resized**, not padded, dimensions. Ask for **absolute pixel** coordinates — normalised 0–1000 requests degrade accuracy.
- `transformations: {"oversized_image": "error"|"downsize"}` is settable **per image block** (default `downsize`). `document` blocks reject it. `count_tokens` honours it for inline base64 but never fetches `url`/`file_id` images.
- Per-image limit 10 MB base64 (5 MB on Bedrock/Google Cloud); hard **8000×8000 px** ceiling. Images per request: **100** on 200K-context models, **600** on others. Beyond ~20 image+document blocks a stricter per-image dimension limit applies, and resent history plus `tool_result` images count toward it.
- Preferred ordering is **image-then-text**. Animations give the **first frame only**. **No EXIF/metadata** reaches the model. Inline images are ephemeral and deleted after processing. Claude cannot **edit** images either, not merely generate them; it declines to identify people, is unreliable below ~200 px, and is not for diagnostic medical imaging.
- Oversized `tool_result` images (computer/browser use) are **rejected, not downscaled**.
- **PDF**: each page is delivered as an image **plus** extracted text — roughly 1,500–3,000 text tokens per page *on top of* image tokens, with no separate PDF surcharge. Dense PDFs therefore exhaust context well before the page limit. No password-protected or encrypted files. `.xlsx`/`.docx` are unsupported in document blocks; `.txt`/`.csv`/`.md` work via the Files API as `text/plain`.
- **Microsoft Foundry: the Files API is unsupported** for Azure-hosted deployments.

**Additional verified details** (confirmed against live docs during batch B01)
- **`stop_details`** is populated **only** when `stop_reason == "refusal"`, carrying an open-set `category`; it is `null` for every other stop reason.
- **`anthropic-beta`**: multiple betas go in **one comma-separated header** (`feature1,feature2`), not repeated headers. An invalid or unentitled beta name returns **400 `invalid_request_error`**, not 403.
- **`/v1/messages/count_tokens`** returns exactly one field, **`input_tokens`**, covering messages + system + tools. It does **not** require `max_tokens`, is free with its **own RPM limit independent of message creation**, and does **not** exercise prompt caching.
- Note a **stale doc artefact**: the `count_tokens` API reference still contains legacy prose describing assistant prefill ("If the final message uses the `assistant` role…"). Ignore it — prefill returns **400** on current models, as the structured-outputs and model-migration pages confirm.

### Version-sensitivity rule
Where a fact has recently changed, **teach current behaviour and flag the change in `e`**. Example phrasing: *"**Currency note:** `temperature` is deprecated and returns a 400 on current models."* This is deliberate — the student may meet dated questions in the wild and must recognise them. Avoid asserting exact prices, exact model ID strings, or exact rate-limit numbers; those churn fastest.

---

## 7. Anti-duplication — MANDATORY

Read your domain's `covered_<Dn>.md` before writing. It lists every stem already in the bank. **Do not re-ask those concepts.** Where a topic is partly covered, attack a genuinely different angle: a different failure mode, a different sub-skill, a different decision point — not a reworded restatement.

Within your own batch, no two questions may test the same fact.

---

## 8. Reject-list — do not write these

- Questions whose correct answer is absent from the options
- "All of the above" / "None of the above"
- Options differing only in trivial wording
- Two defensible correct answers
- Trick questions turning on a typo
- Anything asserting exact per-token prices or current model ID strings
- Explanations that just restate the correct option without mechanism

---

## 9. Before you finish — self-check

1. Count questions — does it match your quota?
2. Count `a` values — roughly even across 0/1/2/3?
3. Count `t` — roughly 70% `"S"`?
4. Every `w` uses the `X — reason` em-dash form for all three wrong options?
5. Every `s` copied verbatim from `subskills.md`?
6. IDs strictly inside your assigned range, no duplicates?
7. Valid JS — quotes escaped, no trailing comma, no comments?
8. Nothing contradicting §6?

State your counts at the end of your final message.
