# CCAR-P blind adjudication — 2 disagreement(s)

Coverage 1,618/1,618. Agreement 99.9%.

Each entry is an item where an independent verifier, working without sight of
the recorded answer, chose differently. Either the key is wrong, or the item is
ambiguous, or the verifier erred. A human read decides which.

## DPO-A-039 — Developer Productivity & Operational Enablement / hard / single  (DISAGREEMENT)

- **recorded:** D
- **verifier:** A (confidence high)

> An external auditor will spend two weeks examining a rail operator's signalling codebase. They need to read widely, search, and run read-only analysis commands such as static analysis and dependency listing. They must not modify source, and the engagement letter states that modification must be structurally impossible rather than merely discouraged. The operator wants the auditor productive on day one without a bespoke build of the tooling.

- `A` Give the auditor a checkout on a read-only filesystem mount, so that write attempts fail at the operating system level regardless of what the session tries to do. **(verifier)**
- `B` Have the auditor work in the default permission mode and rely on the approval prompt for every write, since a prompt gives them an explicit chance to decline each modification.
- `C` Have the auditor work in the mode that automatically accepts edits, and take a git snapshot at the start so any modification can be reverted at the end of the engagement.
- `D` Provision the auditor's sessions in the exploratory permission mode, which permits reading and read-only commands, and add deny rules covering the file-writing tools. **(recorded)**

*Author's rationale:* Two mechanisms are being combined for two different reasons. The exploratory mode gives the correct default posture out of the box — reading and read-only work proceed, source modification does not — which is what makes the auditor productive immediately. The deny rules are what make the property structural rather than a mode setting: a mode can be changed mid-session, whereas a deny rule is evaluated ahead of every allow and does not depend on which mode is active.

## ETO-D-026 — Evaluation, Testing & Optimisation / hard / single  (DISAGREEMENT)

- **recorded:** D
- **verifier:** B (confidence medium)
- **verifier reasoning:** B and D both de-confound the 0.79/0.91 gap, in opposite directions. B gives the capable model's score on the cheap path's categories (the counterfactual the proposed decision actually needs); D gives the cheap model's score on capable-path tickets (tells you about router allocation, not about what moving categories would buy). I chose B because the decision on the table is 'move these categories to capable', and B is the only option that prices that. If the key is D, the stem would need to be about whether the router is allocating well rather than about the category-migration proposal.

> An enterprise IT service desk routes tickets: a classifier decides whether each goes to a cheap fast model or to the higher-capability one. Routing cut cost by 45%. The post-deployment audit shows quality of 0.79 on the cheap path against 0.91 on the capable path, with overall quality four points below the pre-routing baseline. The team proposes moving the lowest-scoring ticket categories permanently to the capable model. Which analysis should precede that decision?

- `A` Re-tune the classifier's confidence threshold so more tickets go to the capable path, then measure the resulting quality and cost and iterate from there.
- `B` Compare the cheap path's score against the pre-routing baseline restricted to the same ticket categories, to establish how large the loss on that path really is before deciding how much of the 45% saving is worth giving back. **(verifier)**
- `C` Increase the audit sample until the twelve-point gap between the two paths reaches statistical significance at the team's chosen confidence level.
- `D` Score the cheap model on the tickets the router sent it and, separately, on a sample the router sent to the capable path, separating the cheap model's capability from the router's allocation decisions. **(recorded)**

*Author's rationale:* A gap between the paths is expected even from a perfect router, because the router deliberately sends harder tickets to the stronger model; the observed 0.79 against 0.91 is therefore uninterpretable as evidence about either component. Cross-scoring breaks the confound. If the cheap model performs well on tickets it was not given, the router is over-escalating and the saving is smaller than it should be; if it performs badly on tickets it was given, the router is under-escalating and the fix is the routing boundary. The proposed category move only makes sense in the second case.

## SCL-C-018 — Stakeholder Communication & Lifecycle Management / medium / next-step  (LOW-CONFIDENCE AGREEMENT)

- **recorded:** D
- **verifier:** D (confidence low)
- **verifier reasoning:** C is equally defensible. The stem gives no cost of delay and no evidence that 7-day activation predicts 30-day churn, so 'wait 30 days and honour the agreed gate' (D) and 'agree a validated proxy and decide now' (C) are both good practice. To separate them the stem would need either a stated cost/deadline pressure on the decision (favouring C) or an explicit statement that the churn criterion is a safety/quality guardrail that cannot be proxied (favouring D).

> A B2B SaaS company finished a four-week pilot of a Claude-based onboarding-email drafter. The criterion agreed before the pilot was: median time to send a first onboarding email drops from 22 minutes to under 10, with no increase in the 30-day churn rate of accounts onboarded during the pilot. Median time came in at 8 minutes. The churn figure cannot exist for another 30 days because the pilot cohort has only just onboarded. The sponsor wants a go/no-go today. What is the next step?

- `A` Declare a no-go, because a criterion that cannot be evaluated at the decision point must be treated as unmet.
- `B` Declare a go on the strength of the time result, since churn is a lagging indicator that would not have been available in time for any four-week pilot's decision.
- `C` Agree a leading proxy for churn, such as seven-day activation rate on the pilot cohort, and read the go/no-go against that proxy instead.
- `D` Hold the decision for 30 days with the pilot cohort still running, and tell the sponsor the churn half of the criterion is why the decision waits. **(recorded)** **(verifier)**

*Author's rationale:* The criterion was written with two halves for a reason: faster emails that lose accounts are not a win, and the sponsor agreed to that framing before any data existed. Rolling out now does not make the churn number arrive sooner, so the only thing waiting costs is thirty days of unrealised benefit on a cohort that is already onboarded. Keeping the pilot running preserves the measurement and lets the conversation with the sponsor be about the criterion they signed, not about the pressure of the meeting.
