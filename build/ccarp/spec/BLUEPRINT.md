# CCAR-P — Claude Certified Architect, Professional — Exam Blueprint

Source: Claude Certified Architect – Professional Exam Guide **v1.0, effective July 2026**,
cross-checked across four independent published summaries.

## Exam facts

| | |
|---|---|
| Code | CCAR-P |
| Items | 63 |
| Time | 120 minutes |
| Score | 100–1000 scale, **720 to pass** |
| Delivery | Online proctored / Pearson VUE test centre |
| Book | Closed. No AI assistance. |
| Objectives | 38 graded objectives across 7 domains |
| Audience | Solution architects, AI/ML engineers, tech leads, senior SWEs |
| Assumed background | 3+ yrs systems architecture; 6+ months production LLM work |

The Professional tier differs from Foundations in *what it asks of you*. Foundations asks
whether you can **design** a working Claude system. Professional asks whether you can
**own one in production** — build it, ship it, defend the decisions to stakeholders, and
keep it safe and compliant across its lifecycle.

That difference must show up in every question. See AUTHORING.md.

## Domain weights (official, sum to 100%)

| # | Code | Domain | Weight | Items on real exam |
|---|---|---|---:|---:|
| D3 | `INT` | Integration | **19%** | ~12 |
| D1 | `SDA` | Solution Design & Architecture | **17%** | ~11 |
| D4 | `ETO` | Evaluation, Testing & Optimisation | **16%** | ~10 |
| D5 | `GSR` | Governance, Safety & Risk Management | **14%** | ~9 |
| D6 | `SCL` | Stakeholder Communication & Lifecycle Management | **14%** | ~9 |
| D2 | `CPE` | Claude Models, Prompting & Context Engineering | **13%** | ~8 |
| D7 | `DPO` | Developer Productivity & Operational Enablement | **7%** | ~4 |

This is the flattest weight spread of any Claude certification — 7% to 19%. There is no
domain you can safely skip.

## Exact domain strings

Use these **verbatim** in the `domain` field. Any deviation fails the build.

```
Integration
Solution Design & Architecture
Evaluation, Testing & Optimisation
Governance, Safety & Risk Management
Stakeholder Communication & Lifecycle Management
Claude Models, Prompting & Context Engineering
Developer Productivity & Operational Enablement
```

Note the British `-isation` in *Optimisation* and the `&` (not "and") in every domain
that has one.

---

## Batch scope map

Each batch owns a **disjoint** slice of its domain. Do not write outside your slice —
overlapping batches produce near-duplicate questions, which is the single most common
way a bank of this size goes bad.

### INT — Integration (4 batches)

- **INT-A — RAG pipelines.** Chunking strategy and chunk size trade-offs, chunk overlap,
  metadata attachment, embedding model selection, vector store choice, hybrid
  (dense+sparse/BM25) search, reranking, query rewriting/expansion, retrieval
  evaluation, index refresh and incremental update, multi-tenant retrieval isolation,
  contextual retrieval.
- **INT-B — Tool use & MCP.** Tool schema design, description quality, parameter
  typing, tool result shaping, parallel vs sequential tool calls, tool error handling
  and returning errors to the model, MCP server architecture, MCP transports
  (stdio vs HTTP/SSE), tools vs resources vs prompts, MCP authentication and scoping,
  tool count/context budget, dynamic tool selection.
- **INT-C — API mechanics.** Streaming (SSE) and partial responses, Batch API and when
  it applies, prompt caching (cache breakpoints, TTL, economics), rate limits and 429
  handling, retry with exponential backoff and jitter, idempotency, timeouts, token
  counting and budgeting, message/turn structure, stop reasons, max_tokens behaviour,
  system vs user role placement, multi-turn conversation state.
- **INT-D — Enterprise integration & deployment.** Claude on Amazon Bedrock and Google
  Vertex AI, first-party API vs cloud-hosted trade-offs, VPC/PrivateLink and private
  networking, data residency and regional routing, SSO/identity and service accounts,
  secrets management, gateway/proxy patterns, event-driven and queue-based integration,
  webhook delivery and reliability, legacy/mainframe and ETL integration, sync vs async
  contract design.

### SDA — Solution Design & Architecture (4 batches)

- **SDA-A — Pattern selection.** The augmented LLM baseline, prompt chaining, routing,
  parallelisation (sectioning and voting), orchestrator–workers, evaluator–optimiser,
  and the central question of **workflow vs agent**. When added autonomy pays for
  itself and when it is pure risk. Task decomposition.
- **SDA-B — Multi-agent systems.** Subagent design and boundaries, context isolation
  between agents, handoff protocols, shared vs private state, coordination and token
  overhead, when multi-agent genuinely beats a single agent with tools, termination
  conditions, loop/recursion limits, result aggregation, agent-to-agent error
  propagation.
- **SDA-C — Non-functional trade-offs.** Latency budgets and where time actually goes,
  cost modelling per request and at volume, throughput and concurrency design, accuracy
  targets and how they drive architecture, maintainability and change cost, caching
  layers, horizontal scaling, capacity planning, build-vs-buy, model-tier mixing within
  one system.
- **SDA-D — Reliability & failure design.** Human-in-the-loop placement and escalation
  design, guardrail placement in the request path, circuit breakers, graceful
  degradation and fallback chains, idempotency across retries, partial failure
  handling, state recovery and checkpointing, timeout budgets across a chain,
  observability hooks designed in from the start, blast-radius containment.

### ETO — Evaluation, Testing & Optimisation (4 batches; D is a short top-up)

- **ETO-A — Eval design.** Building eval sets, golden/reference datasets, sampling
  representative cases, task-specific metrics, exact-match vs fuzzy vs model-graded,
  LLM-as-judge design, rubric writing, position/verbosity bias in judges, validating
  the grader itself, inter-rater agreement, sample size and statistical significance,
  eval-driven development.
- **ETO-B — Testing in practice.** Regression suites and CI integration, gating
  deployments on evals, A/B testing prompts and models, canary and shadow deployment,
  red-teaming and adversarial testing, jailbreak test suites, edge-case discovery from
  production traffic, RAG-specific evaluation (faithfulness, answer relevance, context
  precision/recall), agent trajectory evaluation vs final-answer-only.
- **ETO-C — Production optimisation & monitoring.** Latency optimisation levers, cost
  reduction levers and their quality cost, prompt caching economics, model downgrade
  behind a quality gate, batch vs realtime routing, token reduction, monitoring
  (latency percentiles, error rate, cost per task, quality proxies), drift detection,
  alert thresholds, feedback loops from production into evals, continuous improvement
  cadence.
- **ETO-D — Top-up.** Harder cross-cutting items spanning eval + optimisation +
  production incident response. Fewer items; make them genuinely difficult.

### GSR — Governance, Safety & Risk Management (3 batches)

- **GSR-A — Safety architecture.** Input and output guardrails, prompt injection defence
  (especially indirect injection via retrieved/tool content), jailbreak resistance,
  content filtering and classification, PII detection and redaction, data minimisation,
  least privilege for tool and data access, sandboxing tool execution, confused-deputy
  problems, output sanitisation before downstream execution.
- **GSR-B — Compliance & regulation.** GDPR (lawful basis, DSR, DPIA, cross-border
  transfer), HIPAA and PHI handling, SOC 2, PCI DSS scope, EU AI Act risk tiers and
  obligations, model risk management (SR 11-7 style validation), audit logging and
  immutability, retention and deletion, explainability and adverse-action requirements,
  sector-specific rules, zero data retention and training-data commitments.
- **GSR-C — Organisational governance.** AI usage policy, approval and exception
  workflows, model/system cards, AI incident response and postmortems, third-party and
  vendor risk assessment, shadow AI discovery, acceptable-use enforcement, human
  accountability and RACI for AI decisions, responsible scaling, board/regulator
  reporting, AI inventory and registration.

### SCL — Stakeholder Communication & Lifecycle Management (3 batches)

- **SCL-A — Discovery & requirements.** Structured discovery workshops, use-case
  qualification and triage, feasibility assessment, distinguishing an LLM problem from a
  non-LLM problem, success criteria and measurable acceptance, requirement elicitation
  from non-technical stakeholders, scoping and de-scoping, stakeholder mapping, baseline
  measurement before building.
- **SCL-B — Communicating architecture & trade-offs.** Architecture decision records,
  presenting trade-offs without false precision, executive vs technical framing, risk
  communication and calibrated language, cost and ROI narratives, TCO beyond API spend,
  expectation setting on accuracy and non-determinism, SLA/SLO negotiation for a
  probabilistic system, handling "why not just fine-tune / why not GPT" challenges.
- **SCL-C — Lifecycle ownership.** Phased delivery, pilot-to-production criteria,
  production readiness review, handoff and runbook documentation, change management and
  user adoption, training and enablement, post-launch review cadence, iteration
  prioritisation, versioning and deprecation, migration and sunset planning, ownership
  transfer to a run team.

### CPE — Claude Models, Prompting & Context Engineering (3 batches)

- **CPE-A — Model selection & capabilities.** Haiku vs Sonnet vs Opus trade-offs on
  cost/latency/capability, extended thinking and when reasoning budget pays off, vision
  and document input, context window and output token limits, choosing a tier per
  subtask rather than per system, upgrade/downgrade decision criteria, benchmark
  relevance vs task-specific eval, model version pinning and migration.
- **CPE-B — Prompt engineering at scale.** System prompt architecture and ordering,
  XML/structured delimiters, few-shot example selection and count, chain-of-thought and
  when it helps, assistant prefill, output format enforcement (JSON, schema, tool-based
  structured output), role/persona prompting, negative instructions, prompt templates
  and parameterisation, prompt versioning and testing, instruction conflict resolution.
- **CPE-C — Context engineering.** Context window budgeting, what belongs in system vs
  turn vs retrieved context, compaction and summarisation strategy, context rot and
  degradation with length, long-context retrieval vs RAG, structured note-taking and
  external scratchpads, just-in-time context loading, sub-agent context isolation as a
  context strategy, multi-turn state management, conversation pruning.

### DPO — Developer Productivity & Operational Enablement (2 batches)

- **DPO-A — Claude Code for teams.** `CLAUDE.md` and memory hierarchy, settings
  precedence (enterprise → project → user), permissions and allow/deny rules, hooks and
  their events, subagents, skills, slash commands, MCP server configuration and scope,
  headless/print mode, CI and automation usage, team-shared vs personal configuration,
  sandboxing and safe autonomy.
- **DPO-B — Operational enablement.** Debugging AI-integrated systems, tracing and
  correlation across a multi-step chain, reproducing non-deterministic failures, cost
  visibility and per-team budgets, developer onboarding to an AI codebase, prompt
  libraries as versioned code, secret hygiene in AI workflows, triage of AI-feature
  incidents, progressive rollout and feature flags for AI features, measuring developer
  productivity honestly.

---

## Target volumes

| Domain | Batches | Items each | Total |
|---|---:|---:|---:|
| INT | A, B, C, D | 72 | 288 |
| SDA | A, B, C, D | 72 | 288 |
| ETO | A, B, C + D top-up | 72 / 40 | 256 |
| GSR | A, B, C | 72 | 216 |
| SCL | A, B, C | 72 | 216 |
| CPE | A, B, C | 72 | 216 |
| DPO | A, B | 72 | 144 |
| **Total** | **22** | | **~1,624** |

Plus ~140 flashcards across the 7 domains.
