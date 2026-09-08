# CCAO-F Domain Blueprint & Batch Assignments

Official exam: 60 items, 120 minutes, scaled 100–1000, pass at 720.

This bank: **1,650 items** across 22 authoring batches of 75.
Weighting approximates the published blueprint, plus a light technical-awareness
slice the user requested for client-conversation fluency.

| # | Domain (`domain` string — copy verbatim) | Batches | Items | Share |
|---|---|---|---|---|
| 1 | `Output Evaluation and Validation` | OEV-A…D | 300 | 18.2% |
| 2 | `Workflow Integration and Solution Design` | WIS-A…C | 225 | 13.6% |
| 3 | `Governance, Risk, and Responsible Use` | GRR-A…C | 225 | 13.6% |
| 4 | `Prompting and Task Execution` | PTE-A…C | 225 | 13.6% |
| 5 | `Product and Model Selection` | PMS-A…B | 150 | 9.1% |
| 6 | `Configuration and Knowledge Management` | CKM-A…B | 150 | 9.1% |
| 7 | `Troubleshooting and Optimisation` | TOP-A…B | 150 | 9.1% |
| 8 | `Technical Awareness` | TAW-A…C | 225 | 13.6% |

Batches within a domain have **disjoint topic assignments**. Stay inside your
assigned topics — that is what prevents 22 agents from writing the same item.

---

## Domain 1 — Output Evaluation and Validation (21% of real exam; heaviest)

### OEV-A — Hallucination & grounding
Hallucination taxonomy; fabricated citations, quotes, statistics, dates, names;
grounded vs. parametric claims; knowledge-cutoff staleness vs. fabrication;
plausible-but-false detail; risk ranking of claim types; which outputs need
source-checking at all.

### OEV-B — Verification workflows
Spot-checking strategy; sampling rates for bulk output; cross-referencing
against source documents; summary fidelity to source; omission vs. commission
errors; verifying extractions and transformations; verifying against a system of
record; who verifies and when; documenting that verification happened.

### OEV-C — Reasoning, consistency & calibration
Arithmetic and unit errors; internal logical inconsistency; contradictions
across a long output; confidence calibration and hedging language; sycophancy
and agreement bias under pushback; overconfident tone masking uncertainty;
self-consistency checks; asking Claude to critique its own output.

### OEV-D — Quality criteria & acceptance
Defining acceptance criteria and rubrics up front; golden-set / benchmark
comparison; bias and fairness review of output; tone, register and brand
compliance; completeness against a brief; "good enough for purpose" thresholds
by stakes; when to reject and restart vs. edit; escalation triggers.

---

## Domain 2 — Workflow Integration and Solution Design (16%)

### WIS-A — Task suitability & process mapping
Identifying high-fit vs. poor-fit tasks; decomposing an end-to-end business
process into Claude-assisted and human steps; where AI adds real leverage;
volume and repeatability as fit signals; batch vs. interactive work; sequencing
a multi-step workflow; recognising tasks that should not be automated at all.

### WIS-B — Human-in-the-loop, handoffs & resilience
Placement of review checkpoints and approval gates; designing escalation paths;
fallback behaviour when Claude fails or refuses; handoff to and from systems of
record; connectors and MCP at a workflow-design level; data flowing in and out;
avoiding unreviewed straight-through processing; designing for auditability.

### WIS-C — Team rollout, standardisation & measurement
Prompt and Project templates for consistency across a team; pilot design and
change management; success metrics, baselines and ROI; scaling from one power
user to a department; documenting a workflow so others can run it; training and
enablement; managing uneven adoption; sunsetting a workflow that is not working.

---

## Domain 3 — Governance, Risk, and Responsible Use (15%)

### GRR-A — Sensitive data handling
Recognising PII, PHI, PCI and commercially confidential material; data
minimisation and redaction before input; client confidentiality and engagement
boundaries; retention and deletion; consumer vs. enterprise data-handling
posture; cross-border and residency concerns at a conceptual level; regulated
data scenarios (GDPR/HIPAA-style, conceptual only).

### GRR-B — Human oversight & high-stakes use
Decisions that require a human decision-maker (hiring, lending, clinical,
disciplinary, legal, safety); acceptable-use boundaries; limits on legal,
medical and financial advice; disclosure and transparency of AI involvement;
bias and fairness obligations in consequential decisions; accountability and who
owns the outcome; consent and notice.

### GRR-C — Organisational controls
Role-based access to Projects and shared knowledge; audit trails and record
keeping; shadow AI and unsanctioned tool use; policy authoring, exceptions and
training; IP, copyright, licensing and attribution; prompt injection from
untrusted documents and web content; incident response when AI output causes
harm; third-party and vendor risk; procurement and approval of AI tooling.

---

## Domain 4 — Prompting and Task Execution (14%)

### PTE-A — Prompt anatomy & context
The five building blocks — role, context, task, constraints, format; specificity
over vagueness; supplying background the model cannot infer; audience and tone
calibration; role/persona prompting and its limits; stating success criteria in
the prompt; providing reference material; asking Claude to seek clarification
instead of guessing.

### PTE-B — Structuring complex work
Few-shot / multishot examples and how many to give; example quality and
representativeness; chain-of-thought and step-by-step reasoning; task
decomposition; prompt chaining across turns; delimiters and XML-style tags to
separate instructions from content; placing long documents relative to the
question; scoping one prompt to one job.

### PTE-C — Control, iteration & anti-patterns
Output format specification (tables, JSON, headings, word and item counts);
positive framing vs. negative constraints; length and depth control;
prefilling and steering a continuation; iterative refinement loops; multi-turn
conversation management; reusable prompt templates and variables; common
anti-patterns — kitchen-sink prompts, conflicting instructions, buried asks,
politeness padding.

---

## Domain 5 — Product and Model Selection (12%)

### PMS-A — Model tier selection
Haiku vs. Sonnet vs. Opus by cost, latency and reasoning depth; matching tier to
task complexity; when escalating a tier actually helps and when it masks a
prompt problem; downgrading to control cost and latency at volume; extended
thinking — what it buys and when it is wasted; context-window pressure as a
selection factor; mixed-tier pipelines.

### PMS-B — Surface & feature selection
Claude.ai web vs. desktop vs. mobile vs. API vs. Claude Code — who uses which
and why; plan tiers and usage limits at a conceptual level; Artifacts vs. inline
chat output; Research mode vs. plain chat vs. simple web lookup; file upload and
document/image analysis; connectors as a feature choice; Projects vs. one-off
chat as a product decision; picking the cheapest surface that meets the need.

---

## Domain 6 — Configuration and Knowledge Management (12%)

### CKM-A — Projects & instruction design
When a Project earns its keep vs. a single chat; writing effective project-level
custom instructions; instruction specificity, precedence and conflict with
per-chat prompts; organising and naming Projects; sharing with a team and the
consistency benefit; persistence and context across sessions; writing styles and
tone configuration; keeping instructions maintainable as needs change.

### CKM-B — Knowledge source curation
What belongs in Project knowledge and what does not; curation and freshness;
superseded, duplicate and conflicting documents; structuring documents for
retrievability (headings, naming, splitting); scope creep in a knowledge base;
size and volume trade-offs; connectors as living knowledge sources; document
versioning and lifecycle; access control over shared knowledge; when per-chat
upload beats a permanent knowledge base.

---

## Domain 7 — Troubleshooting and Optimisation (10%)

### TOP-A — Diagnosing output failures
Generic, hedged or shallow output; wrong output format; wrong tone or register
for the audience; wrong length; instructions apparently ignored; inconsistent
results across runs of the same prompt; refusals and over-cautious responses on
legitimate work; output that answers a different question than the one asked;
mapping each symptom to the prompt element that fixes it.

### TOP-B — Context, conversation & optimisation
Truncated or cut-off output and continuation strategy; conversation drift and
when to start a fresh chat; degradation in very long threads; important content
buried mid-document; project instructions conflicting with a chat prompt; cost
and latency optimisation; changing one variable at a time when debugging;
capturing and reusing what worked; recognising when to escalate to technical
support or IT; recognising when the task is a poor fit for Claude entirely.

---

## Domain 8 — Technical Awareness (light technical slice)

Keep these **conceptual and decision-oriented**. The candidate is a business
professional who must make good calls and speak credibly to engineers — not
write code. No code-writing items, no syntax recall, no SDK method names.

### TAW-A — API vs. chat, tokens & operating limits
What the API is and who it is for; signals that a workflow has outgrown the chat
interface (volume, embedding in a product, automation, determinism); tokens as a
unit of cost and the intuition that input and output both count; context window
vs. maximum output length; rate limits as a design constraint; why teams pin a
model version instead of tracking "latest"; system prompt and temperature as
API-level controls a business owner should understand.

### TAW-B — Platform capabilities, conceptually
Tool use / function calling — what it enables and its failure modes; MCP and
connectors as standardised access to systems; agents vs. single-shot prompting
and where agents are appropriate; retrieval (RAG) vs. putting everything in a
long context, and the cost/accuracy trade-off; prompt caching and when repeated
context makes it worthwhile; batch processing for non-urgent volume; evals as
the discipline of measuring output quality; prompting and context engineering
vs. fine-tuning as the first lever.

### TAW-C — Deployment, security & working with engineers
What Claude Code is and who benefits from it; cloud deployment options
(Anthropic API vs. hosting through a cloud provider) at a decision level; SSO,
admin controls and centralised governance; API key handling and why keys never
belong in a shared doc or a prompt; writing a prompt or requirements spec a
developer can implement; scoping an AI project with an engineering team;
estimating and governing cost at scale; separating a prompt-quality problem from
an engineering problem when triaging with a technical team.
