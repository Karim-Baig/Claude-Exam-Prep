# Blind adjudication — 50 disagreement(s)

Coverage 2,472/2,472 shipped items. Agreement 98.0%.

Each entry below is an item where an independent verifier, working without
sight of the recorded answer, chose differently from the author. One of the
two is wrong, or the item is ambiguous. Verdicts needed.

## CKM-A-026 — Configuration and Knowledge Management / hard / single

- **recorded answer:** D
- **verifier answer:** C  (confidence: medium)
- **verifier reasoning:** C and D are near-duplicates (both say build it), but D's arithmetic fails: 15 deliverables x 10 min = 150 min saved in month 1 against 240 min setup, so it cannot 'recover its setup cost within the first month'; C's two-month break-even (240 / (150-30)) is correct.

## CKM-A-036 — Configuration and Knowledge Management / medium / multi

- **recorded answer:** B+D
- **verifier answer:** A+B  (confidence: low)
- **verifier reasoning:** Near-duplicate options: A and B describe the identical fix (replace the generic instruction with per-content-type register/length/structure rules triggered by a content-type declaration), and D is also true though narrower, so any two of A/B/D are defensible.

## CKM-A-047 — Configuration and Knowledge Management / hard / multi

- **recorded answer:** A+D
- **verifier answer:** B+D  (confidence: medium)
- **verifier reasoning:** A (three role-specific Projects) is equally sound architecture and is the answer this bank gives to structurally identical items, so three options are responsive while only two are requested.

> A claims operations manager at an insurance company is designing a Claude Project for a team of 20 claims handlers, 4 senior claims managers, and 2 fraud analysts. The three groups have very different output requirements: handlers need triage summaries (brief, structured, next-action focused), managers need reserve adequacy analysis (detailed, financial, risk-quantified), and fraud analysts need red-flag pattern analysis (evidence-based, comparative, hypothesis-generating). The manager asks which TWO instruction architecture approaches would BEST serve all three groups.
> 
> Which TWO approaches should she adopt? (Choose TWO)

- `A` Create three separate Projects — one per team role — each with instructions precisely configured for its output type and knowledge base. **(recorded)**
- `B` Use a single Project with a role-declaration trigger: 'Declare role at start of chat (Handler/Manager/Analyst)' and separate instruction blocks defining output requirements for each role. **(verifier)**
- `C` Use a single generic instruction set and rely on each team member's individual prompting to differentiate their output type. 
- `D` Configure the single Project's knowledge base to contain claims data, policy guidelines, and fraud indicators — so all three roles draw from the same underlying reference material while their output instructions differ. **(recorded)****(verifier)**
- `E` Separate the fraud analyst role into a completely standalone process, as fraud analysis should not be performed using the same tool as claims processing. 

*Author's rationale:* Three separate Projects (A) gives each role a precisely configured instruction environment without the complexity of a three-way conditional system — each role has the right instructions and knowledge base for their specific output without risk of applying the wrong profile. However, if a single Project is used, a shared knowledge base (D) allows all three roles to draw from the same claims data, policy guidelines, and fraud indicators — avoiding three separate copies of the same reference material that must be kept in sync. The combination A + D describes the most complete and scalable architecture: three Projects (one per role) sharing a knowledge base approach where possible, or a single Project with separate instruction blocks and a unified knowledge base.

## RCL-CKM-009 — Configuration and Knowledge Management / hard / single

- **recorded answer:** B
- **verifier answer:** A  (confidence: low)
- **verifier reasoning:** B is also true - custom instructions can govern any behaviour while styles address tone and voice - so 'scope' is doing all the disambiguating work; separately, D asserts a style-over-instruction precedence rule that is not safely stateable.

## RCL-CKM-054 — Configuration and Knowledge Management / medium / multi

- **recorded answer:** C+E
- **verifier answer:** A+E  (confidence: low)
- **verifier reasoning:** Over-keyed: A, C and E are all true and responsive; C states the correct division of labour but is a definition rather than a 'practice', and it duplicates the keyed content of RCL-CKM-037.

## GRR-A-040 — Governance, Risk, and Responsible Use / medium / single

- **recorded answer:** B
- **verifier answer:** C  (confidence: medium)
- **verifier reasoning:** B is genuinely defensible — many professional retention schedules run from formal completion of the work, not final settlement; the stem's invoicing detail is the only thing tipping it to C.

> A project manager at a legal technology firm has been using a Claude Project to manage documentation for a software development contract with a large law firm client. The contract signed two years ago specifies a 5-year retention period for all project records. The development work was completed and formally signed off eight months ago, though invoicing continued until three months ago.
> 
> From which event does the 5-year retention period MOST likely begin under standard contract and professional records principles?

- `A` From the date the contract was signed two years ago 
- `B` From the date the project was formally signed off as complete eight months ago **(recorded)**
- `C` From the date the final invoice was settled three months ago, as this represents the conclusion of all financial obligations under the contract **(verifier)**
- `D` From today's date, since the retention clock starts when the organisation first reviews its retention obligations 

*Author's rationale:* Under standard contract and professional records principles, the retention period for project records typically runs from the date the contractual engagement concludes — the formal sign-off of deliverables. The sign-off date (eight months ago) is the point at which the primary contractual obligations were discharged. While invoicing continued, ongoing billing is an administrative extension of the relationship, not a continuation of the substantive project. Legal limitation periods typically run from the date obligations were performed, not the date administrative follow-up concluded.

## GRR-A-044 — Governance, Risk, and Responsible Use / medium / single

- **recorded answer:** D
- **verifier answer:** C  (confidence: medium)
- **verifier reasoning:** C and D prescribe substantively the same action and differ only in rationale; D is wrong solely because withdrawal of consent is NOT retrospective (GDPR Art. 7(3)), which is a very fine distinction for a foundations-level item.

## GRR-B-038 — Governance, Risk, and Responsible Use / medium / multi

- **recorded answer:** A+D
- **verifier answer:** A+C  (confidence: medium)
- **verifier reasoning:** D is also a true statement (the lawyer retains professional responsibility regardless of AI use), so three of five options are correct as written — it is only excluded because it describes accountability rather than the capability boundary.

## GRR-B-060 — Governance, Risk, and Responsible Use / hard / nextstep

- **recorded answer:** D
- **verifier answer:** C  (confidence: medium)
- **verifier reasoning:** D (an independent unanchored re-read before consulting either assessment) is standard radiological discrepancy practice and is defensible as the immediate next step; C wins only if the author values joint clinical reconciliation over avoiding anchoring.

> A hospital's radiology AI tool flags findings on a chest CT scan consistent with early-stage lung cancer. The treating pulmonologist reviewed the same scan the previous day and documented it as clear, with no significant findings. Both the AI flag and the pulmonologist's documentation now exist in the patient record as conflicting assessments. A senior radiologist has just been notified of the discrepancy.
> 
> What should the senior radiologist do NEXT?

- `A` Update the patient record immediately to formally note the discrepancy, so the conflict is documented before the treating team's next interaction with the patient. 
- `B` Contact the AI tool's vendor to report the discrepancy for model quality review and recalibration. 
- `C` Contact the treating pulmonologist to discuss the AI flag and initiate a joint clinical review of the findings. **(verifier)**
- `D` Independently review the scan without first consulting either the AI output or the pulmonologist's prior assessment, to form an unanchored professional judgment before any further action. **(recorded)**

*Author's rationale:* The senior radiologist's first obligation is to form their own independent clinical assessment of the scan — without anchoring on either the AI flag or the pulmonologist's existing documentation. Both prior assessments are conflicting reference points; consulting either before forming an independent view risks anchoring the senior radiologist's judgment on an output that may itself be wrong. Once an independent clinical view is formed, the radiologist has a sound basis for updating the record (A), discussing with the pulmonologist (C), or determining whether model reporting is warranted (B). The diagnostic step must precede the communication and documentation steps.

## GRR-B-080 — Governance, Risk, and Responsible Use / hard / nextstep

- **recorded answer:** D
- **verifier answer:** B  (confidence: medium)
- **verifier reasoning:** D (securing decision logs and records before anything else) is a defensible first step and is what many incident-response frameworks require; B wins only on the principle that stopping ongoing customer harm outranks evidence preservation.

> A newly appointed Chief Ethics Officer discovers during a routine audit that the company's AI-assisted contract renewal system has been automatically reducing service tiers for customers who have filed complaints — a practice running for 18 months with no human review, no customer notice, and no accountability trail. No current leadership team member was aware. The CEtO must decide what to do FIRST.
> 
> What should the CEtO do FIRST?

- `A` Commission an independent external audit to establish the full scope, duration, and customer impact of the practice immediately. 
- `B` Immediately disable the AI system responsible for automated service tier changes to stop any ongoing harm to customers. **(verifier)**
- `C` Brief the board of directors and retain external legal counsel on the discovery before any further internal steps are taken. 
- `D` Identify and secure all records related to the practice — decision logs, affected customer accounts, and any internal communications — before any investigation, remediation, or external disclosure activity begins. **(recorded)**

*Author's rationale:* Evidence preservation is uniquely time-sensitive: it must happen before any investigation, remediation, or disclosure action, because those actions themselves can alter or destroy the records needed to understand the full scope of the problem. Disabling the system (B) may trigger automated log rotation or data purges. Commissioning an external audit (A) has nothing to audit if records have been altered. Briefing the board (C) without having secured the factual record means briefing on incomplete information that the investigation will need to revise. Securing the records is the prerequisite for everything else — it does not foreclose any other step; all other steps require it to be done first.

## GRR-C-052 — Governance, Risk, and Responsible Use / medium / single

- **recorded answer:** B
- **verifier answer:** C  (confidence: high)

> An information security analyst at a pharmaceutical company is reviewing AI conversation audit logs. She notices that a single user account submitted 847 prompts between 2 AM and 4 AM on a Sunday, all requesting synthesis details and compound structures for a specific class of restricted precursor chemicals. The account belongs to a research chemist who is on holiday.
> 
> What does this pattern MOST strongly indicate?

- `A` The researcher is highly motivated and conducts research asynchronously outside normal business hours to maximise productivity 
- `B` The audit log system has a timestamp error that is displaying Sunday night activity with incorrect metadata **(recorded)**
- `C` The account may have been compromised and is being used to extract restricted chemical information through the AI system **(verifier)**
- `D` The AI system is generating automated test queries to validate that the chemical knowledge base is functioning correctly 

*Author's rationale:* The combination of anomalous timing (2-4 AM Sunday), volume (847 prompts in two hours), the researcher being confirmed absent, and the targeted subject matter (restricted precursor chemicals) strongly suggests account compromise and exfiltration attempt. This is precisely the pattern that AI audit log anomaly detection is designed to surface — a human researcher on holiday is not conducting 847 queries at 2 AM; a compromised credential used by a malicious actor is.

## OEV-A-055 — Output Evaluation and Validation / hard / multi

- **recorded answer:** A+C
- **verifier answer:** C+E  (confidence: medium)
- **verifier reasoning:** C is certain, but the date error is only loosely a 'fabrication' (real event, wrong detail), so A (misattribution) is arguable — none of A/B/E is evidenced by the stem.

> An investigative journalist at a national newspaper is using Claude to help structure a 6,000-word investigative piece. Claude provides background on a regulatory investigation, including a statement that a named regulator 'issued a consent order in March 2023' and a claim that an industry body 'published revised guidance in November 2022' that was later withdrawn. The journalist finds the consent order in the regulator's public records with a different date (June 2023), and cannot find the industry body guidance at all.
> 
> Which TWO hallucination types are MOST precisely represented by these two specific errors? (Choose TWO)

- `A` The wrong consent order date is a misattribution error — Claude applied a date from a different regulatory action to this consent order. **(recorded)**
- `B` The wrong consent order date is a staleness error — Claude's training data reflects a pre-publication draft or announcement date rather than the finalised order date. 
- `C` The non-existent industry guidance is a fabrication — Claude generated a plausible-sounding publication that has no corresponding real document. **(recorded)****(verifier)**
- `D` The non-existent industry guidance is an omission error — Claude should have cited the guidance but incorrectly identified it as withdrawn. 
- `E` The wrong consent order date is a fabrication — Claude generated a date for a real event that has no correspondence to the actual record. **(verifier)**

*Author's rationale:* Option A: The consent order is real (it exists in public records) but the date is wrong (March 2023 vs the real June 2023). Claude applied an incorrect date to a real regulatory event — this is misattribution of a date, where a real action is given the wrong chronological metadata. Option C: The industry body guidance cannot be located anywhere — no such publication, current or withdrawn, exists in the body's record. This is fabrication: a publication was generated with no corresponding real document.

## OEV-A-061 — Output Evaluation and Validation / hard / single

- **recorded answer:** A
- **verifier answer:** B  (confidence: high)

> A quantitative analyst at a hedge fund asks Claude about the composition of a major equity index as of the most recent quarterly rebalance. Claude names 12 specific constituent stocks and their approximate weightings. The analyst checks the current index prospectus and finds that 10 of the 12 stocks are current constituents at approximately correct weights, but 2 of the named stocks were removed from the index 14 months ago and replaced with different names.
> 
> The analyst is deciding whether this represents a knowledge-cutoff error or fabrication. What is the MOST precise assessment?

- `A` This is entirely a knowledge-cutoff error — the index composition as of 14 months ago is accurately reflected, and the two 'errors' are real constituents at the time of training. **(recorded)**
- `B` This is a mixed error: the 10 current constituents reflect accurate training data, but the 2 removed stocks may represent either stale training data (they were real constituents) or partial fabrication (their current weights are generated). **(verifier)**
- `C` This is entirely a fabrication — Claude cannot accurately report index compositions because constituent data changes continuously. 
- `D` This is a misattribution error — Claude applied the weightings from a different index to these two stocks. 

*Author's rationale:* The two stocks removed 14 months ago were real index constituents at the time of Claude's training. Reporting them as current constituents is a staleness error: the training data accurately reflected the index as it existed before the rebalance that removed them. This is a knowledge-cutoff error — real information from a real source, just superseded. The presence of 10 currently correct constituents at approximately right weights supports this diagnosis: the training data was accurate for the pre-rebalance composition.

## OEV-B-009 — Output Evaluation and Validation / easy / single

- **recorded answer:** D
- **verifier answer:** C  (confidence: high)

## OEV-B-010 — Output Evaluation and Validation / medium / multi

- **recorded answer:** B+D
- **verifier answer:** B+C  (confidence: high)

> A senior audit manager at a financial services firm is designing governance for a workflow in which Claude reviews 200 client workpapers each quarter and flags potential gaps or inconsistencies. She needs to decide who should verify Claude's flagged findings before the audit team acts on them.
> 
> Which TWO roles should be involved in verifying Claude's flagged findings before action is taken? (Choose TWO)

- `A` The IT security team, to confirm Claude's output does not contain data exfiltration patterns before it is shared with the audit team. 
- `B` An experienced auditor with subject-matter knowledge of the workpaper type, who can assess whether each flagged gap is genuine. **(recorded)****(verifier)**
- `C` The original preparer of each workpaper, who can confirm whether a flagged gap reflects a real omission or was addressed elsewhere in the file. **(verifier)**
- `D` A senior partner with billing authority, who must approve any additional audit procedures before work hours are committed to a client file. **(recorded)**
- `E` The firm's legal counsel, because Claude-generated audit findings may carry legal liability for the firm if acted upon incorrectly. 

*Author's rationale:* B is correct because an experienced auditor with subject-matter knowledge is best positioned to assess whether a flagged gap is genuine or a false positive — this role supplies the domain expertise Claude cannot provide. D is correct because additional audit procedures triggered by Claude's findings involve committing client work hours, which requires approval from someone with billing authority. Both roles are required: one for quality assessment, one for authorised action.

## OEV-B-025 — Output Evaluation and Validation / medium / multi

- **recorded answer:** C+D
- **verifier answer:** D+E  (confidence: low)
- **verifier reasoning:** C, D and E are all genuinely correct spot-check design choices for only two slots; D+E are the mechanisms that reveal recurring patterns, but random selection (C) is equally defensible and is the obvious foil to A.

## OEV-B-044 — Output Evaluation and Validation / medium / single

- **recorded answer:** A
- **verifier answer:** B  (confidence: high)

## OEV-B-075 — Output Evaluation and Validation / medium / multi

- **recorded answer:** B+D
- **verifier answer:** A+B  (confidence: medium)
- **verifier reasoning:** A sits in mild tension with the independence principle (GMs verifying summaries of their own property's performance), which other items in this bank treat as a conflict of interest.

> The COO of a 2,000-room hospitality chain is implementing a workflow in which Claude generates weekly operational performance summaries for 14 properties, each summary drawing on occupancy data, F&B revenue, and guest satisfaction scores. The summaries are used by regional directors to allocate operational support resources. The COO asks who should verify the summaries and when.
> 
> Which TWO verification assignments are MOST appropriate for this workflow? (Choose TWO)

- `A` The property general managers, who can verify that the summary accurately reflects their property's data before it is shared with regional directors. **(verifier)**
- `B` A data analyst who has access to the source data systems for all 14 properties, who can confirm that extracted figures match the source data before the summaries are distributed. **(recorded)****(verifier)**
- `C` The regional directors themselves, who will review the summaries critically as part of their resource allocation decision-making process. 
- `D` The COO, who has the strategic perspective to assess whether each summary's resource allocation implications are proportionate. **(recorded)**
- `E` An external auditor, who can provide an independent assessment of whether the AI-generated summaries are an accurate representation of property performance. 

*Author's rationale:* B is correct because a data analyst with access to source data systems can perform a systematic spot-check of the extracted figures against the source occupancy, F&B, and satisfaction data — this is the accuracy verification that ensures the summaries reflect actual property performance. D is correct because the COO, as the decision-maker who designs the workflow and uses the summaries to allocate operational support, is the appropriate authority to assess whether the summaries' resource allocation implications are proportionate and whether the summaries are fit for purpose at the strategic level.

## OEV-C-010 — Output Evaluation and Validation / medium / multi

- **recorded answer:** B+D
- **verifier answer:** A+D  (confidence: low)
- **verifier reasoning:** Three options (A, B and D) are all factually accurate descriptions of the output, so the item is over-keyed however the two slots are filled.

## OEV-C-040 — Output Evaluation and Validation / medium / multi

- **recorded answer:** C+D
- **verifier answer:** B+C  (confidence: low)
- **verifier reasoning:** Statement T is also appropriately calibrated (correlation stated as correlation, scoped to comparable trusts), so option D is equally defensible and three of the five statements are well calibrated.

## OEV-C-061 — Output Evaluation and Validation / easy / single

- **recorded answer:** D
- **verifier answer:** B  (confidence: low)
- **verifier reasoning:** B and D both say 'well calibrated' and give materially equivalent reasons (quantified range plus a flagged contamination scenario vs. base case plus material risk scenario), so the item has two correct options.

## OEV-C-066 — Output Evaluation and Validation / easy / single

- **recorded answer:** D
- **verifier answer:** B  (confidence: high)

## OEV-D-017 — Output Evaluation and Validation / medium / multi

- **recorded answer:** B+D
- **verifier answer:** C+D  (confidence: medium)
- **verifier reasoning:** B overlaps heavily with D (both are about reach/reputational consequence of a published error), so three options compete for two slots.

## OEV-D-020 — Output Evaluation and Validation / hard / nextstep

- **recorded answer:** D
- **verifier answer:** A  (confidence: high)

> A strategy analyst at a management consulting firm is establishing a quality gate for Claude-generated slide commentary in client deliverables. She has completed the following: drafted a five-criterion rubric with explicit pass/fail thresholds, identified a five-deck golden set from prior approved engagements, and recruited three reviewers. No Claude output has been run through the process yet.
> 
> What should she do NEXT?

- `A` Have all three reviewers score the five golden-set decks independently to calibrate inter-rater reliability. **(verifier)**
- `B` Run ten new Claude-generated decks through the rubric to gather error-rate data for a full pilot. 
- `C` Share the rubric with the client engagement lead for approval before applying it to deliverables. 
- `D` Pilot the rubric on a single Claude-generated output with all three reviewers present to test whether the criteria surface real quality differences before scaling. **(recorded)**

*Author's rationale:* The rubric has not been tested against live Claude output. Before investing in a full reviewer-calibration session on the golden set, the minimum-viable next step is to verify the rubric works on real Claude output: do the criteria apply cleanly, are the thresholds calibrated correctly, and do reviewers interpret the criteria consistently? A single-output pilot with all three reviewers present surfaces rubric problems cheaply. Issues found here cost one output's worth of time; issues found mid-calibration cost far more.

## OEV-D-021 — Output Evaluation and Validation / medium / single

- **recorded answer:** B
- **verifier answer:** A  (confidence: medium)
- **verifier reasoning:** B is genuinely defensible (a plausible wrong threshold is acted on directly); A wins only on the detectability principle that a silent omission gives the reviewer no signal at all.

## RCL-OEV-A-020 — Output Evaluation and Validation / hard / single

- **recorded answer:** D
- **verifier answer:** C  (confidence: low)
- **verifier reasoning:** Defective single-answer item: a values-match check leaves B (fabricated citation elsewhere), C (error in the source itself) and D (un-extracted fields) all unaddressed.

## RCL-OEV-B-056 — Output Evaluation and Validation / hard / multi

- **recorded answer:** A+D
- **verifier answer:** A+C  (confidence: low)
- **verifier reasoning:** Over-keyed: A, C and D are all true consequences of a stale golden set, and D is close to a restatement of C, so three responsive options compete for two slots.

## PTE-A-050 — Prompting and Task Execution / medium / multi

- **recorded answer:** A+D
- **verifier answer:** C+D  (confidence: low)
- **verifier reasoning:** Over-keyed: A (role), C (RFP), D (format) and E (audience) are all true and responsive for a generic bid executive summary; only B (word count) is a clear distractor, so the requested pair is arbitrary.

> A bid manager at a 45,000-employee telecoms company is using Claude to help write proposals. Her current prompt is `Write the executive summary for this proposal.` She receives a generic executive summary. A senior colleague reviews the prompt and identifies the TWO improvements that would have the MOST impact on output quality. Choose TWO (Choose TWO)

- `A` Role — `You are a senior bid manager experienced with telecoms infrastructure proposals for government clients.` **(recorded)**
- `B` Word-count constraint of 400 words maximum. 
- `C` Reference to the full RFP document. **(verifier)**
- `D` Format — `Structure the executive summary with these sections: Client Situation, Proposed Solution, Key Differentiators, Pricing Summary, and Implementation Timeline.` **(recorded)****(verifier)**
- `E` Audience description of the procurement committee evaluation panel. 

*Author's rationale:* The two highest-impact improvements are role (activating bid management expertise specific to telecoms infrastructure and government procurement contexts) and format (specifying the five required executive summary sections that structure the document appropriately for a proposal review process). The role addresses why the content is generic (no domain expertise activated); the format addresses why the structure is generic (no required sections specified). Together they produce a domain-appropriate, structurally correct executive summary.

## PTE-A-059 — Prompting and Task Execution / hard / multi

- **recorded answer:** A+C
- **verifier answer:** A+B  (confidence: medium)
- **verifier reasoning:** Over-keyed tendency: C (prior approved label for indication/dosage/safety consistency) is also genuinely correct reference material for a Module 2.7 summary, so three of five options are true.

> A pharma regulatory medical writer is preparing a Module 2.7 clinical summary for a new drug submission. She has: (1) three pivotal clinical study reports, (2) the agency's Module 2.7 guidance document, (3) the product's approved label from a prior submission. She must decide which to include as reference material in her Claude prompts. Which TWO documents should be included as reference material? Choose TWO (Choose TWO)

- `A` The clinical study reports — Claude must reason over the actual trial data, study designs, and efficacy results to produce accurate summary content. **(recorded)****(verifier)**
- `B` The Module 2.7 agency guidance document — it defines the required structure and content standards for the summary. **(verifier)**
- `C` The approved product label from the prior submission — Claude needs the exact prior label language for consistency in describing the indication, dosage, and safety profile. **(recorded)**
- `D` A two-sentence context paragraph describing the submission context is sufficient for all three documents. 
- `E` Only the agency guidance should be included; the study reports should be summarized in the prompt stem. 

*Author's rationale:* The clinical study reports (Option A) must be included because the Module 2.7 summary requires accurate analysis of specific efficacy endpoints, patient populations, safety findings, and statistical results — these cannot be generated from general knowledge. The approved label (Option C) must be included because label consistency is a regulatory requirement: the summary must use the same indication language, dosage description, and contraindication phrasing as the currently approved label. Both are proprietary documents Claude cannot know.

## PTE-A-065 — Prompting and Task Execution / hard / single

- **recorded answer:** A
- **verifier answer:** B  (confidence: medium)
- **verifier reasoning:** Genuine tension: due diligence is about the grantee, so the annual reports (B) come first, but A (regional operating/regulatory environment) is a real competing fix and the stem gives no criterion for ranking them.

> A non-profit international foundation program officer is using Claude to draft due diligence questions for a prospective grantee in a specific region. She provides the grantee's concept note, the foundation's grantmaking strategy, and a two-sentence regional context. Due diligence questions are generic. Two colleagues disagree on the fix: one says add the grantee's last three annual reports; the other says expand the regional context to two paragraphs. Which fix should she prioritize FIRST?

- `A` Expand the regional context to a two-paragraph description covering the operating environment, regulatory landscape, and civil society constraints specific to that region. **(recorded)**
- `B` Include the grantee's last three annual reports as reference material. **(verifier)**
- `C` Add a foundation due diligence expert role prompt. 
- `D` Add explicit success criteria defining what a good due diligence question looks like. 

*Author's rationale:* Due diligence questions are generic because Claude lacks the regional and sector context that determines which risks to probe in that specific operating environment. Regional context — local regulatory constraints, civil society restrictions, government-NGO relationship dynamics, financial system risks — drives the specificity of due diligence questions: which funding controls are relevant, which governance risks are heightened, which programmatic risks are specific to that context. Annual reports provide performance history (useful) but don't explain why the questions lack regional specificity — that gap is the two-sentence regional context.

## PTE-A-080 — Prompting and Task Execution / hard / single

- **recorded answer:** C
- **verifier answer:** B  (confidence: medium)
- **verifier reasoning:** C ('both necessary') has real merit because Colleague 2's fix presupposes the sectioning that Colleague 1 supplies; the item's 'MORE complete' framing is what excludes it.

> A clinical research associate at a contract research organisation is drafting an informed consent form (ICF). The document has two audiences: regulatory reviewers (who will check ICH E6(R3) compliance, technical language acceptable) and trial participants (plain language, no assumed medical background). Both audiences read the same document.
> 
> Her prompt: `"Draft an ICF for a Phase II oncology trial. The audience is regulators and patients."`
> 
> Claude produces a document in technical regulatory language throughout. Two colleagues propose fixes:
> 
> **Colleague 1:** "Add a format instruction splitting the document into a Technical Summary section and a Plain Language section."
> 
> **Colleague 2:** "Add audience context for each section specifying the vocabulary level."
> 
> Which fix is MORE complete?

- `A` Colleague 1 — the format split is the primary fix; vocabulary follows from the section label. 
- `B` Colleague 2 — audience context directly governs vocabulary level; format labels alone do not force register change. **(verifier)**
- `C` Both fixes are necessary; neither alone is sufficient. **(recorded)**
- `D` Colleague 1 — regulatory ICFs always use a two-section structure, so the format instruction encodes the correct vocabulary implicitly. 

*Author's rationale:* Colleague 1's format split is necessary — without a structural division, both audiences receive undifferentiated content. Colleague 2's audience context is also necessary — without vocabulary specifications per section, Claude may write technical language under the plain-language section label. Neither fix alone produces the required output: format without audience context gives structure but not register; audience context without format gives the right register but no structural separation for two audiences. Both are required.

## RCL-PTE-013 — Prompting and Task Execution / hard / single

- **recorded answer:** D
- **verifier answer:** C  (confidence: medium)
- **verifier reasoning:** Role and Context are both defensible: PTE-005 says Role calibrates register and audience, but PTE-019 classifies 'the audience consists of non-technical middle managers' as context — the bank's taxonomy is inconsistent on where audience level lives.

## TAW-A-019 — Technical Awareness / medium / single

- **recorded answer:** D
- **verifier answer:** B  (confidence: low)
- **verifier reasoning:** Stem asks for the MOST reliable enforcement of fixed disclosure language: deterministic post-processing (B) guarantees inclusion, whereas a system-prompt instruction (D) is only probabilistic model compliance, so both are defensible and the item is ambiguous.

## TAW-C-055 — Technical Awareness / medium / single

- **recorded answer:** D
- **verifier answer:** C  (confidence: low)
- **verifier reasoning:** NEAR-DUPLICATE: C and D assert the same distinction (requirements define outcome and acceptance criteria, not parameters); C answers the 'why' asked, D restates it as an action — both are true, so the item is effectively unanswerable as written.

## TOP-A-067 — Troubleshooting and Optimisation / hard / single

- **recorded answer:** B
- **verifier answer:** A  (confidence: low)
- **verifier reasoning:** Genuinely ambiguous: the stem's question is already a yes/no decision request, so B's diagnosis is inaccurate, yet the 'a colleague suggests' framing signals the author intended A to be the distractor.

## TOP-A-075 — Troubleshooting and Optimisation / medium / multi

- **recorded answer:** A+C
- **verifier answer:** A+E  (confidence: low)
- **verifier reasoning:** Over-keyed: A, C and E are all true and responsive (task framing, question placement, supplying the evidence) but only two are requested.

## TOP-B-052 — Troubleshooting and Optimisation / medium / single

- **recorded answer:** D
- **verifier answer:** B  (confidence: low)
- **verifier reasoning:** Genuinely contested: B is the consequence actually caused by 'waiting this long', while D follows from never documenting at all — the stem plants facts supporting both.

## TOP-B-057 — Troubleshooting and Optimisation / medium / multi

- **recorded answer:** B+E
- **verifier answer:** B+D  (confidence: medium)
- **verifier reasoning:** E is genuinely defensible as the second pick (auto-loading current prompts fixes the version-discovery problem) — D wins only because it also creates the refresh process for evolving needs.

## WIS-A-023 — Workflow Integration and Solution Design / medium / single

- **recorded answer:** B
- **verifier answer:** D  (confidence: medium)
- **verifier reasoning:** B is defensible if coverage assessment is treated as judgment; D wins because the stem calls step 3 'preliminary' (a draft) and steps 4-5 are routing/notification, i.e. system steps.

> A claims processing manager at a mid-size insurer is redesigning the first-notice-of-loss (FNOL) intake workflow. She has five steps: (1) extract structured fields from the claimant's written statement, (2) cross-check field values against the policy record, (3) generate a preliminary coverage assessment, (4) assign the claim to an adjuster, and (5) notify the claimant that the claim has been received. Which step represents the CLEAREST boundary between Claude-assisted and human-only, and where does it fall?

- `A` After step 1; extraction is Claude-assisted and everything from step 2 onward requires a human 
- `B` After step 2; extraction and cross-checking are Claude-assisted, but preliminary coverage assessment and adjuster assignment require human judgment **(recorded)**
- `C` After step 5; all five steps are Claude-assisted because they are repeatable processes that follow defined rules 
- `D` After step 3; steps 1–3 are Claude-assisted and steps 4–5 are human or system steps **(verifier)**

*Author's rationale:* Steps 1 and 2 are transformation tasks: extract structured fields from free text, then compare field values against a policy record. Both have defined inputs, rule-based logic, and verifiable outputs. Step 3 — preliminary coverage assessment — requires applying policy interpretation to specific claim facts, which involves judgment about ambiguous coverage language. Step 4 involves routing decisions with workload and complexity factors. The boundary between transformation and judgment falls between steps 2 and 3.

## WIS-A-026 — Workflow Integration and Solution Design / hard / single

- **recorded answer:** D
- **verifier answer:** B  (confidence: low)
- **verifier reasoning:** B and D are both genuinely defensible root flaws (unvalidated scoring vs no rep review); the stakes here are internal sales prioritisation, which weakens the accountability argument in D.

## WIS-A-113 — Workflow Integration and Solution Design / hard / single

- **recorded answer:** D
- **verifier answer:** A  (confidence: medium)
- **verifier reasoning:** A screens candidates out with no human review (classic adverse-impact/AEDT exposure), but D — AI scoring of interview transcripts — is separately regulated in several jurisdictions, so both steps are defensible answers.

> A talent acquisition lead designs an AI-assisted hiring workflow: (1) Claude screens resumes against 8 defined criteria and shortlists candidates, (2) shortlisted candidates are auto-invited to a video interview, (3) Claude analyses interview transcripts and issues a hire/no-hire recommendation, (4) a recruiter reviews the recommendation and makes the final call.
> 
> Legal counsel identifies one step as most likely to attract employment discrimination scrutiny. Which step is it?

- `A` Claude screening resumes against 8 defined criteria to produce a shortlist. **(verifier)**
- `B` The automated video interview invitation sent to shortlisted candidates. 
- `C` The recruiter reviewing Claude's recommendation and making the final hiring decision. 
- `D` Claude analysing interview transcripts to produce a hire/no-hire recommendation on an individual candidate. **(recorded)**

*Author's rationale:* Producing a hire/no-hire recommendation from an interview transcript is an evaluation of an individual's suitability based on their spoken responses — a step that directly implicates anti-discrimination law. Interview-based AI assessments have been found by regulators in multiple jurisdictions to require bias audits and disclosure. The recommendation is on a named individual, uses subjective conversational data, and directly feeds an employment decision. Resume screening against defined, objective criteria is lower-risk because the criteria are explicit and auditable; transcript analysis introduces qualitative, language-based assessment that carries documented demographic bias risk.

## WIS-B-040 — Workflow Integration and Solution Design / medium / single

- **recorded answer:** D
- **verifier answer:** C  (confidence: low)
- **verifier reasoning:** Two 'Neither' distractors are both sound practice — C (risk-stratified ongoing review) answers the review-checkpoint question asked, while D (pilot 20, tune the prompt) is the standard scale-up answer used elsewhere in this bank; the item does not disambiguate.

## WIS-B-076 — Workflow Integration and Solution Design / medium / single

- **recorded answer:** D
- **verifier answer:** B  (confidence: low)
- **verifier reasoning:** NEAR-DUPLICATE: B and D are the same remedy (split the document and prompt the sections separately) differing only in scope, and C offers a rival diagnosis — attention dilution rather than capacity truncation — that is equally consistent with the stem; omission of the FINAL 150 pages favours truncation, so B, but the item is not cleanly separable.

## WIS-C-014 — Workflow Integration and Solution Design / hard / multi

- **recorded answer:** A+C
- **verifier answer:** A+E  (confidence: medium)
- **verifier reasoning:** A and E overlap heavily (both encode tone at the prompt/Project layer) while D (narrated walkthrough as mandatory pre-access) is an equally defensible second pick.

> A customer operations VP at a major telecom carrier is scaling a Claude-assisted complaints-drafting workflow from a three-person pilot team to all 200 agents in the contact centre. The pilot team developed highly refined prompts over four months. Initial scaling shows new agents producing drafts that miss the empathetic tone required by the company's service charter.
> 
> Which TWO actions would MOST effectively close the quality gap for new agents? (Choose TWO)

- `A` Embed representative tone examples — showing acceptable and unacceptable draft language — as few-shot examples inside the shared prompt template. **(recorded)****(verifier)**
- `B` Switch all 200 agents to a more capable model tier so the deeper language understanding produces more empathetic output by default. 
- `C` Implement a quality-review gate where a team leader reviews every draft before it reaches the customer, with corrective coaching tied to specific tone errors. **(recorded)**
- `D` Record a short walkthrough video in which a pilot-team agent narrates her prompting decisions on a real complaints scenario, and make it mandatory pre-access viewing. 
- `E` Update the Project custom instructions to include the service-charter tone principles verbatim, and verify all agents access Claude through the shared Project. **(verifier)**

*Author's rationale:* **A (few-shot tone examples)** directly programs the quality standard into the prompt. Concrete before-and-after examples give Claude a precise calibration target for every draft, reducing the pilot-team-to-new-agent gap without requiring agents to interpret abstract tone descriptions. **C (review gate with coaching)** closes the gap from the human side. A structured quality gate catches tone misses before they reach customers and builds agent skill through feedback tied to specific errors — a feedback loop generic training cannot replicate.

## WIS-C-038 — Workflow Integration and Solution Design / hard / multi

- **recorded answer:** A+C
- **verifier answer:** C+D  (confidence: medium)
- **verifier reasoning:** A (restrict pilot to internal memos) is also true and responsive, so three risk-controlling options compete for two slots; A is the weakest only because it sacrifices learning on the actual target task.

## WIS-C-043 — Workflow Integration and Solution Design / medium / multi

- **recorded answer:** B+C+E
- **verifier answer:** A+B+E  (confidence: low)
- **verifier reasoning:** Over-keyed: A, B, C and E are all true and essential rollout elements (only D is a bad practice), so four options compete for three slots and any subset is arguable.

## WIS-C-047 — Workflow Integration and Solution Design / hard / multi

- **recorded answer:** A+B
- **verifier answer:** B+E  (confidence: medium)
- **verifier reasoning:** B and E are near-duplicates of the same approach (mine prior-year administrative records), which leaves A (caveated retrospective self-estimates) as a legitimate alternative second pick.

## WIS-C-062 — Workflow Integration and Solution Design / medium / multi

- **recorded answer:** C+D
- **verifier answer:** A+C  (confidence: medium)
- **verifier reasoning:** D (first-week feedback check-in before live deliverables) is equally responsive to two-week productive use, giving three true options for two slots.

## WIS-C-063 — Workflow Integration and Solution Design / hard / single

- **recorded answer:** A
- **verifier answer:** D  (confidence: medium)
- **verifier reasoning:** A (verify actual FDA guidance and encode it in the workflow) is also sound practice; D wins only because it structurally answers the specific 'did the specialist do the investigation' concern.

> A compliance VP at a specialty pharmaceutical distributor has rolled out Claude to 22 compliance specialists for drafting deviation investigation reports. After four months, 16 specialists use it regularly. Six do not. When interviewed, five of the six state they are concerned that AI-drafted deviation reports might be perceived as less rigorous by the FDA during an inspection — that inspectors will question whether the compliance specialist actually performed the investigation.
> 
> What is the BEST response to this specific concern?

- `A` Verify the FDA's current guidance on AI-assisted documentation in deviation reports and incorporate the applicable requirements explicitly into the workflow documentation and prompt template. **(recorded)**
- `B` Reassure the specialists verbally that the FDA has no policy against AI-assisted documentation, and encourage them to proceed with adoption. 
- `C` Have the six specialists continue drafting deviation reports manually while the 16 adopters use Claude, creating a two-track quality comparison for the next inspection. 
- `D` Redesign the workflow so Claude drafts only the background and evidence-gathering sections, while the specialist authors the investigation conclusion and corrective actions in their own words — and document the division of labour explicitly in the report. **(verifier)**

*Author's rationale:* The specialists' concern is regulatory compliance — specifically, whether AI-assisted documentation meets FDA inspection expectations. This is a factual, addressable concern that deserves a factual response: verify the applicable FDA guidance and incorporate it into the workflow design. If FDA guidance specifies that AI tools must be disclosed or that the qualified investigator must certify personal review, the workflow should reflect that. If there is no prohibition, that finding closes the concern directly. The correct first step is to answer the regulatory question, not to reassure without evidence.

## WIS-C-068 — Workflow Integration and Solution Design / medium / nextstep

- **recorded answer:** D
- **verifier answer:** B  (confidence: medium)
- **verifier reasoning:** D (revise straight to a tiered enablement track) is a defensible direct fix; B wins only if the assumption gap must be replaced with data before the plan is finalised.
