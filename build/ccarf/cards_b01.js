CARDS.push(
{i:"c1",d:1,t:"1.1",q:"What are the <code>stop_reason</code> values, and what does each mean for an agent loop?",
a:"<code>tool_use</code> &rarr; execute the requested tools and continue the loop.<br><code>end_turn</code> &rarr; Claude finished naturally; stop.<br><code>max_tokens</code> &rarr; output was truncated; <strong>discard the partial turn</strong> and retry with more headroom &mdash; never execute partial tool arguments.<br><code>stop_sequence</code> &rarr; a configured stop sequence was produced.<br><br>Branching on all of them (not just the first two) is what makes a loop robust."},

{i:"c2",d:1,t:"1.1",q:"State the agent loop's append contract.",
a:"After a <code>tool_use</code> response you must append <strong>both</strong>:<br>1. the <strong>assistant</strong> message containing the <code>tool_use</code> block(s), and<br>2. a <strong>user</strong> message containing the matching <code>tool_result</code> block(s), each with <code>tool_use_id</code> equal to the corresponding <code>tool_use.id</code>.<br><br>Then re-send the full history. The API is stateless &mdash; system prompt, tools and history go on <em>every</em> request."},

{i:"c3",d:1,t:"1.1",q:"How do parallel tool calls have to be answered?",
a:"N <code>tool_use</code> blocks in <strong>one</strong> assistant message &rarr; N <code>tool_result</code> blocks in <strong>one</strong> user message, matched by <code>tool_use_id</code>.<br><br>Splitting them across several user messages breaks user/assistant alternation and leaves tool calls unanswered &mdash; the API rejects it. Because pairing is by id, execution order of independent tools is your choice."},

{i:"c4",d:1,t:"1.1",q:"Name the three agentic-loop anti-patterns.",
a:"1. <strong>Parsing assistant text</strong> for a completion marker instead of reading <code>stop_reason</code>.<br>2. Using an <strong>arbitrary iteration limit as the primary stopping mechanism</strong> (it is a safety net, not a termination condition).<br>3. <strong>Rebuilding a minimal conversation</strong> instead of appending to the running history."},

{i:"c5",d:1,t:"1.1",q:"The single most-tested principle on this exam &mdash; state it.",
a:"<strong>Hooks and code give deterministic guarantees; prompts give probabilistic compliance.</strong><br><br>Anything involving money, deletion, identity verification, compliance thresholds or irreversible actions belongs in code &mdash; a precondition, a permission rule, or a <code>PreToolUse</code> hook.<br><br>They are complementary: the hook guarantees the outcome, the prompt makes the agent competent about it."},

{i:"c6",d:1,t:"1.2",q:"What is hub-and-spoke, and why does it matter?",
a:"The coordinator owns <strong>all</strong> inter-agent communication. Spokes never talk to each other.<br><br>Why: one observable trace for debugging, one place to apply error handling and routing policy, and control over coverage and duplication.<br><br>If a spoke constantly needs another's capability, give it a <em>narrow scoped tool</em> &mdash; don't build a mesh."},

{i:"c7",d:1,t:"1.2",q:"List the coordinator's responsibilities.",
a:"Task <strong>decomposition</strong>, <strong>delegation</strong>, result <strong>aggregation</strong>, <strong>error handling</strong>, <strong>routing</strong> and dynamic selection of subagents.<br><br>It does <em>not</em> do the specialists' work &mdash; it routes to synthesis rather than synthesising, and to analysis rather than analysing. A coordinator concatenating raw outputs is a recurring wrong answer."},

{i:"c8",d:1,t:"1.2",q:"Every subagent reports success but the final result is incomplete. Where do you look?",
a:"At the <strong>coordinator's decomposition</strong>.<br><br>Coverage failures are assignment failures. The classic example: a report on &ldquo;AI in creative industries&rdquo; covers only visual art because the coordinator created three visual-domain subtasks. The workers executed correctly on what they were given.<br><br>Defences: enumerate the space before subdividing; state exclusions; add a coverage check at synthesis."},

{i:"c9",d:1,t:"1.3",q:"What context does a subagent inherit from its parent?",
a:"<strong>None.</strong><br><br>Subagents run with isolated context. &ldquo;As discussed above&rdquo;, &ldquo;the same criteria&rdquo;, &ldquo;those files&rdquo; and &ldquo;last time&rdquo; all resolve to nothing.<br><br>A complete delegation = <strong>goal + full inputs (quoted verbatim) + output contract + quality criteria</strong>. The output contract and quality criteria are the two most often omitted."},

{i:"c10",d:1,t:"1.3",q:"How do you spawn subagents, and how do you make them run in parallel?",
a:"Delegation happens via the <code>Task</code> tool &mdash; so the coordinator's <code>allowedTools</code> must include <code>\"Task\"</code>.<br><br>Multiple <code>Task</code> calls emitted in a <strong>single coordinator turn</strong> run concurrently.<br><br>Subagents should normally <em>not</em> have <code>Task</code>, or they spawn their own children and flatten your hub-and-spoke trace into a mesh."},

{i:"c11",d:1,t:"1.3",q:"What do the fields of an <code>AgentDefinition</code> each control?",
a:"<code>description</code> &rarr; when the coordinator should <strong>select</strong> this agent (a selection signal, like a tool description).<br><code>prompt</code> / system prompt &rarr; <strong>how</strong> it works: role, method, standards, exclusions.<br><code>tools</code> / <code>allowedTools</code> &rarr; what it is <strong>able</strong> to do &mdash; the only field with enforcement power.<br><code>model</code> &rarr; capability/cost trade-off.<br><br>Security constraints always live in the tool list."},

{i:"c12",d:1,t:"1.4",q:"When is prompt guidance enough, and when do you need programmatic enforcement?",
a:"Ask: <strong>what does one violation in a hundred cost?</strong><br><br>Negligible (style, tone, cost preferences, priorities) &rarr; prompt, and keep it soft to preserve adaptability.<br>Audit finding, breach, wrong refund, data loss &rarr; <strong>code</strong>: tool precondition, permission rule, or blocking hook.<br>Mechanical and checkable (formatting, import order) &rarr; a <strong>linter</strong>, better than either."},

{i:"c13",d:1,t:"1.4",q:"What must a structured escalation handoff contain?",
a:"1. <strong>Identifier</strong> (customer or case id)<br>2. <strong>Issue summary</strong><br>3. <strong>Verified facts</strong> (identity confirmed, order, amounts, dates)<br>4. <strong>What was attempted and the result</strong><br>5. <strong>Reason for escalation</strong><br>6. <strong>Recommended action</strong><br><br>Items 3 and 4 are the most often omitted and save the human the most time. Don't forget the <em>write-back</em>: the human's resolution must return to case state."},

{i:"c14",d:1,t:"1.5",q:"<code>PreToolUse</code> vs <code>PostToolUse</code> &mdash; what can each actually do?",
a:"<strong><code>PreToolUse</code></strong> &mdash; runs after the model decides, before execution. Documented powers: <code>permissionDecision</code> of <strong>allow / deny / ask / defer</strong> (so it <em>can block</em>), and <strong><code>updatedInput</code></strong>, which <em>replaces the tool's arguments before it runs</em>. This is where enforcement and value-injection (tenant id, actor, compliance flags) live.<br><br><strong><code>PostToolUse</code></strong> &mdash; runs <em>after</em> the tool already ran. It gets a top-level <code>decision: \"block\"</code> with a <code>reason</code> shown to Claude as feedback, and is used for logging, metrics and side effects like linting after an edit.<br><br><strong>The trap:</strong> study guides say <code>PostToolUse</code> normalises, redacts and trims results. Per the official hooks reference it <strong>cannot rewrite a tool result</strong> &mdash; <code>updatedInput</code> is listed only for <code>PreToolUse</code> and <code>PermissionRequest</code>. Do that normalisation <em>in the tool or MCP server</em> instead.<br><br><em>Exam heuristic: enforcement &rarr; Pre. Data-shape / context-bloat &rarr; the blueprint's answer is Post.</em>"},

{i:"c15",d:1,t:"1.5",q:"What must a hook's <em>block</em> result contain?",
a:"Which <strong>rule</strong> was violated, a clear <strong>explanation</strong>, <code>isRetryable: false</code>, and the <strong>valid alternative action</strong> (e.g. &ldquo;use <code>escalate_to_human</code>&rdquo;).<br><br>A bare block causes a <strong>retry storm</strong> &mdash; the agent can't distinguish it from a transient failure. Same contract as a well-designed MCP tool error."},

{i:"c16",d:1,t:"1.5",q:"How should hooks behave when the hook <em>itself</em> fails?",
a:"<strong>Enforcement hooks fail closed</strong> &mdash; if the check can't be evaluated (policy service down), deny, with a clear non-retryable message and an escalation path.<br><br><strong>Observational hooks fail open</strong> &mdash; audit logs, metrics and traces get tight timeouts or run async, so a telemetry outage never takes down the agent.<br><br>Decide this per hook, in advance."},

{i:"c17",d:1,t:"1.6",q:"Fixed pipeline vs adaptive decomposition &mdash; when does each apply?",
a:"<strong>Fixed pipeline / prompt chaining</strong>: the steps are knowable in advance. Predictable multi-aspect work, e.g. per-file review then integration. Gains determinism, auditability, cheap per-step retry.<br><br><strong>Dynamic adaptive decomposition</strong>: the next step depends on what you find. Open-ended investigation. Shape = <em>map structure &rarr; prioritise &rarr; investigate &rarr; revise</em>.<br><br>Fixed pipelines may carry named conditional exits &mdash; go fully adaptive only when branches can't be enumerated."},

{i:"c18",d:1,t:"1.6",q:"Why does reviewing a large diff in one prompt fail, and what replaces it?",
a:"<strong>Attention dilutes</strong> across a long input &mdash; feedback becomes shallow and concentrates on the first files.<br><br>Replace with <strong>multi-pass review</strong>: per-file passes for local defects, plus a <strong>separate cross-file integration pass</strong> for contract and dataflow breaks (a changed signature with stale callers).<br><br>Build the integration pass from <em>changed symbols + their consumers</em>, not all diffs concatenated."},

{i:"c19",d:1,t:"1.7",q:"<code>--resume</code> vs <code>fork_session</code> vs a fresh session &mdash; when do you use each?",
a:"<strong><code>--resume &lt;name&gt;</code></strong>: continue a named session &mdash; correct when the accumulated context is <em>still valid</em>.<br><br><strong><code>fork_session</code></strong>: branch from shared context into independent lines &mdash; for comparing alternatives without cross-contamination. Sessions never <em>merge</em>; pick a winner and carry the rationale forward.<br><br><strong>Fresh session + structured summary</strong>: when the context has gone <em>stale</em> &mdash; notably after files changed on disk."},

{i:"c20",d:1,t:"1.7",q:"What does crash recovery for a long-running agent require?",
a:"Two things, and neither is sufficient alone:<br><br>1. <strong>Durable checkpointing</strong> &mdash; which phases completed <em>and their outputs</em> (or references to them), so you know where to resume and have the inputs.<br>2. <strong>Idempotent phases</strong> &mdash; so a phase interrupted mid-execution can safely re-run without duplicating side effects."},

{i:"c21",d:2,t:"2.1",q:"What makes a strong tool description?",
a:"Five elements:<br>1. What it does<br>2. <strong>When to choose it</strong> (trigger conditions)<br>3. Input format, <strong>with an example</strong><br>4. What it returns<br>5. <strong>The boundary against the nearest alternative</strong> &mdash; what it is <em>not</em> for, and which tool to use instead<br><br>Element 5 does the most work: selection failures are near-misses between neighbours. No adjectives."},

{i:"c22",d:2,t:"2.1",q:"Two tools overlap and the agent misroutes. What is the fix order?",
a:"1. <strong>Expand the descriptions</strong> &mdash; input formats, example queries, edge cases, applicability boundaries. Lowest effort, highest impact.<br>2. <strong>Rename</strong> to eliminate overlap (<code>analyze_content</code> &rarr; <code>extract_web_results</code>). Names carry selection signal.<br>3. If the boundary is <em>genuinely</em> ambiguous, redesign: merge, or re-split along an unambiguous axis.<br><br>Routing layers and classifiers are the over-engineering distractor."},

{i:"c23",d:2,t:"2.2",q:"What belongs in an MCP tool error response?",
a:"<code>isError: true</code> plus:<br>&bull; <code>errorCategory</code> &mdash; <strong>transient / validation / permission / business</strong><br>&bull; <code>isRetryable</code><br>&bull; a <strong>specific, actionable message</strong><br>&bull; any <strong>partial results</strong> salvaged<br><br>Generic errors (&ldquo;Operation failed&rdquo;) prevent correct recovery decisions &mdash; they collapse four situations needing four different responses into one signal."},

{i:"c24",d:2,t:"2.2",q:"Which errors are retryable, and what is the test?",
a:"Test: <strong>would the identical call succeed shortly?</strong><br><br>&bull; <strong>Transient</strong> (timeout, rate limit, 503) &rarr; retryable. Retry with backoff, ideally <em>locally in the subagent</em>.<br>&bull; <strong>Validation</strong> &rarr; not retryable unchanged, but retryable <em>corrected</em> &mdash; so state the expected format.<br>&bull; <strong>Permission</strong> &rarr; never retry; escalate or reroute.<br>&bull; <strong>Business rule</strong> &rarr; never retry; explain and offer the alternative."},

{i:"c25",d:2,t:"2.2",q:"A search returns no results. Is that an error?",
a:"<strong>No.</strong> Return <strong>success with an empty result set</strong>, ideally echoing the query.<br><br>&ldquo;I searched and found nothing&rdquo; is a <em>finding</em>. &ldquo;I could not search&rdquo; is a <em>failure</em>. They demand opposite responses.<br><br>Conflating them causes retry storms on one side and silently-missed gaps on the other. The blueprint states this explicitly."},

{i:"c26",d:2,t:"2.2",q:"Name the three multi-agent error-handling anti-patterns.",
a:"1. <strong>Generic status</strong> hiding context (&ldquo;search unavailable&rdquo;) &mdash; the coordinator can't choose a recovery.<br>2. <strong>Silent suppression</strong> &mdash; returning empty success on failure; the gap becomes invisible.<br>3. <strong>Whole-workflow abort</strong> &mdash; one failure destroys everything that succeeded.<br><br>The correct middle: local recovery for transient faults, structured propagation of the unresolvable, coverage annotation for gaps."},

{i:"c27",d:2,t:"2.3",q:"How many tools should an agent have, and why?",
a:"Roughly <strong>4&ndash;5 role-relevant tools</strong>, plus a small set of narrow cross-role utilities (read-only).<br><br>The blueprint contrasts <strong>18 tools</strong> with a focused <strong>4&ndash;5</strong>: selection reliability falls as the toolset grows, and agents holding tools outside their specialisation tend to misuse them.<br><br>A role needing a dozen tools is usually under-decomposed &mdash; look for the seam."},

{i:"c28",d:2,t:"2.3",q:"The four <code>tool_choice</code> values and when each applies.",
a:"<code>auto</code> &mdash; model chooses text or tools. <strong>Default for conversational loops</strong>; it's what allows <code>end_turn</code>.<br><code>any</code> &mdash; must call <em>some</em> tool. Guarantees structured output when several schemas are valid. <strong>Never leave this set across a loop</strong> &mdash; the loop can't terminate.<br><code>{\"type\":\"tool\",\"name\":\"...\"}</code> &mdash; must call that one. Single-shot extraction.<br><code>none</code> &mdash; no tools this turn. Side-effect-free explanation."},

{i:"c29",d:2,t:"2.4",q:"Where do MCP servers get configured, and how are secrets handled?",
a:"<strong>Project scope</strong>: <code>.mcp.json</code> in the repo &mdash; version-controlled, shared with everyone who clones. Use <strong>environment variable substitution</strong> (<code>${GITHUB_TOKEN}</code>) so no credential enters the repository.<br><br><strong>User scope</strong>: <code>~/.claude.json</code> &mdash; personal and experimental servers.<br><br>The same <code>.mcp.json</code> serves CI, resolving variables from the CI secret store (use a service credential, not a person's token)."},

{i:"c30",d:2,t:"2.4",q:"MCP tools vs MCP resources.",
a:"<strong>Tools</strong> = actions the model invokes.<br><strong>Resources</strong> = readable <em>content catalogues</em> &mdash; database schemas, task summaries, reference data.<br><br>Resources reduce exploratory tool calls: the agent consults the schema instead of probing for it. Better than putting the same content in a prompt, because the server keeps it current and it's read on demand."},

{i:"c31",d:2,t:"2.4",q:"What happens when you connect several MCP servers?",
a:"<strong>All connected servers' tools are discovered on connection and available simultaneously.</strong> There is no activation step and no exclusivity.<br><br>Design consequence: every connection enlarges the choice space for every agent that can see it, degrading selection. Scope servers per agent role, keep experiments in user scope, and consider wrapping a 30-tool community server to expose only the operations you need."},

{i:"c32",d:2,t:"2.5",q:"Built-in tool selection reference.",
a:"<strong>Glob</strong> &mdash; find files by <em>name/extension pattern</em>. Use <code>**/</code> to match at any depth.<br><strong>Grep</strong> &mdash; search file <em>contents</em>: symbols, error messages, imports.<br><strong>Read</strong> &mdash; open a known file; use offset/limit for a range.<br><strong>Write</strong> &mdash; create or fully replace (Read first if it exists).<br><strong>Edit</strong> &mdash; precise change via a <em>unique</em> text match.<br><strong>Bash</strong> &mdash; broadest, most dangerous grant. Last resort."},

{i:"c33",d:2,t:"2.5",q:"<code>Edit</code> fails because the match isn't unique. What do you do?",
a:"Either <strong>expand the match string</strong> with surrounding context until it is unique, or fall back to <strong>Read + Write</strong> for a full-file replacement (the blueprint names this fallback).<br><br>The uniqueness requirement is a <em>safety feature</em> &mdash; it prevents an ambiguous change silently hitting the wrong occurrence. Don't reach for <code>sed</code>."},

{i:"c34",d:2,t:"2.5",q:"What is the incremental investigation pattern?",
a:"<strong>Grep the entry point &rarr; Read it &rarr; follow its calls.</strong> Each read is justified by something found in the previous step.<br><br>Cheap search narrows; expensive read confirms. Never guess-and-read at scale.<br><br>Completeness caveat: a plain symbol search <em>under-reports</em> (usage via wrappers and re-exports) and <em>over-reports</em> (comments, string literals, name collisions). Trace re-exports explicitly and state your coverage."},

{i:"c35",d:3,t:"3.1",q:"Describe the CLAUDE.md hierarchy.",
a:"<strong>User</strong>: <code>~/.claude/CLAUDE.md</code> &mdash; personal, all your projects, <em>never shared via VCS</em>.<br><strong>Project</strong>: <code>CLAUDE.md</code> in the repo root (or <code>.claude/CLAUDE.md</code>) &mdash; version-controlled, shared with everyone who clones.<br><strong>Directory</strong>: a CLAUDE.md in a subdirectory &mdash; applies to work in that subtree.<br><br>They <strong>compose</strong>, they don't override. A new joiner missing conventions &rarr; suspect user-level configuration."},

{i:"c36",d:3,t:"3.1",q:"What does <code>@path</code> do in CLAUDE.md?",
a:"It <strong>imports an external file</strong>, e.g. <code>@./standards/coding-style.md</code>.<br><br>Use it to modularise: shared standards live once, and each package's CLAUDE.md composes the subset it needs (shared style + its own testing standards). Avoids the five-copies-that-drift problem in a monorepo."},

{i:"c37",d:3,t:"3.1",q:"What makes a CLAUDE.md line worth its context?",
a:"It must <strong>encode a specific decision the model would otherwise get wrong</strong>.<br><br>&#10007; &ldquo;Write clean, maintainable code.&rdquo; &mdash; encodes nothing; could appear in any project.<br>&#10003; &ldquo;Errors a caller can recover from return a <code>Result</code>; reserve exceptions for programmer errors.&rdquo;<br><br>CLAUDE.md is a per-request context budget. Prune stale entries, push mechanical rules to linters, keep human onboarding in the README."},

{i:"c38",d:3,t:"3.2",q:"Where do slash commands and skills live, and what's the difference?",
a:"<strong>Commands</strong>: <code>.claude/commands/</code> (project, shared via VCS) or <code>~/.claude/commands/</code> (personal). Essentially a reusable prompt.<br><br><strong>Skills</strong>: <code>.claude/skills/</code> with a <code>SKILL.md</code> per skill. A skill adds <strong>declarative operational configuration</strong> that a plain command has no way to express.<br><br>Rule: <em>location determines sharing</em> &mdash; project <code>.claude/</code> is shared, <code>~/.claude/</code> is personal."},

{i:"c39",d:3,t:"3.2",q:"The key <code>SKILL.md</code> frontmatter fields &mdash; and the one thing almost every study guide gets wrong.",
a:"<code>context: fork</code> &mdash; run the skill in an <strong>isolated subagent context</strong>; verbose output never reaches the main session. Isolation is opt-in, not automatic.<br><br><code>argument-hint</code> &mdash; <strong>prompt for required parameters</strong> at invocation.<br><br><strong>The trap:</strong> <code>allowed-tools</code> does <em>not</em> restrict. Per the official docs it <strong>pre-approves</strong> tools for that turn so they skip the permission prompt, and &ldquo;all tools remain callable&rdquo;. The field that removes capability is <strong><code>disallowed-tools</code></strong>.<br><br>Opposite naming for <strong>subagents</strong>: there, <code>tools</code> (SDK: <code>allowedTools</code>) <em>is</em> an allowlist and does restrict.<br><br><em>Exam note: the blueprint says <code>allowed-tools</code> restricts. If no <code>disallowed-tools</code> option is offered, pick it &mdash; but know the truth.</em>"},

{i:"c40",d:3,t:"3.3",q:"What are path-scoped rules and why use them?",
a:"Files in <code>.claude/rules/</code> carrying YAML frontmatter <code>paths</code> globs, e.g. <code>paths: [\"**/*.test.tsx\"]</code> or <code>paths: [\"terraform/**/*\"]</code>. The rule loads <strong>only</strong> when matching files are being worked on.<br><br>Two wins: <strong>efficiency</strong> (no context cost when irrelevant) and <strong>correctness</strong> (can't be misapplied to unrelated work).<br><br>Use <code>**/</code> to match at any depth &mdash; that's what handles co-located test files."},

{i:"c41",d:3,t:"3.3",q:"Directory-level CLAUDE.md or a path-scoped rule?",
a:"<strong>Directory CLAUDE.md</strong> &mdash; the convention is confined to one self-contained subtree, and applies to everything in it.<br><br><strong>Path-scoped rule</strong> &mdash; the convention follows a <em>file type or pattern across many directories</em>. The blueprint's example: test files co-located throughout the codebase, which no directory boundary captures.<br><br>Make applicability <em>structural</em>, never a &ldquo;when working in X&hellip;&rdquo; clause."},

{i:"c42",d:3,t:"3.4",q:"Planning mode or direct execution?",
a:"<strong>Planning mode</strong>: large scope + multiple defensible approaches + architectural consequence. Also whenever <em>consequence</em> is high (security-critical paths) regardless of diff size. It allows safe read-only exploration before anything is committed.<br><br><strong>Direct execution</strong>: simple, well-understood change &mdash; clear stack trace, single file, obvious fix. Add a regression test.<br><br>The exam tests <em>both</em> directions. Over-planning is a real wrong answer."},

{i:"c43",d:3,t:"3.4",q:"What's the strongest workflow for a very large, discovery-heavy task?",
a:"<strong>Delegate discovery &rarr; plan &rarr; write the plan to a file &rarr; execute in phases.</strong><br><br>An Explore subagent isolates the verbose discovery so only a summary reaches the main context. Planning mode chooses the approach. Writing the plan to a file means each phase starts from the plan rather than the previous phase's full history &mdash; and makes <em>partial rollback</em> possible when a phase-one decision proves wrong."},

{i:"c44",d:3,t:"3.5",q:"What is the most effective way to communicate a requirement to Claude?",
a:"<strong>Two to three concrete input/output examples.</strong> They resolve ambiguities a prose description doesn't know it has.<br><br>Related techniques:<br>&bull; <strong>Test-driven iteration</strong> &mdash; write the test set first (behaviour, edge cases, <em>performance bounds</em>), then iterate to green.<br>&bull; <strong>Interview pattern</strong> &mdash; have Claude question <em>you</em> to surface non-obvious considerations (cache invalidation, failure modes)."},

{i:"c45",d:3,t:"3.5",q:"You have six issues to feed back. How do you group them?",
a:"<strong>Interdependent issues go together in one message</strong> &mdash; if three symptoms stem from one wrong assumption, they must be seen together to be fixed coherently.<br><br><strong>Independent issues go separately</strong> &mdash; each gets focused attention and they don't interact.<br><br>If iteration <em>oscillates</em> across rounds, stop: that means the target is unclear. Write examples or failing tests first."},

{i:"c46",d:3,t:"3.6",q:"Which flags make Claude Code work in CI?",
a:"<code>-p</code> / <code>--print</code> &mdash; <strong>non-interactive</strong>. Without it the job hangs waiting for input.<br><code>--output-format json</code> &mdash; machine-readable results.<br><code>--json-schema</code> &mdash; constrain that output to <em>your</em> shape, so the pipeline can branch on fields and post inline PR comments.<br><br>Never gate a build on text matching. (Also: <code>--resume &lt;name&gt;</code> for named sessions.)"},

{i:"c47",d:3,t:"3.6",q:"Why must CI review run in a separate session from generation?",
a:"<strong>Session context isolation.</strong> The instance that generated the code <em>retains its reasoning</em> and is unlikely to challenge decisions it just argued for. An independent instance &mdash; seeing only the diff and the standards &mdash; finds subtler issues.<br><br>Independence, not strictness, is the operative variable. A longer or sterner review prompt can't dislodge the anchoring."},

{i:"c48",d:3,t:"3.6",q:"Two CI review problems and their prescribed fixes.",
a:"<strong>Re-runs repeat old findings</strong> &rarr; include prior review results as <em>explicit input</em>; report only new or still-unfixed issues. (Explicit input, not implicit session carryover &mdash; CI stays reproducible.)<br><br><strong>Generated tests duplicate coverage and clash in style</strong> &rarr; include existing test files in context, <em>and</em> document testing standards and available fixtures in CLAUDE.md."},

{i:"c49",d:4,t:"4.1",q:"Explicit criteria vs vague instructions &mdash; give the canonical example.",
a:"&#10007; &ldquo;Check that comments are accurate.&rdquo; &rarr; 40% false positives.<br>&#10003; &ldquo;Flag a comment <strong>only when it directly contradicts what the code does</strong>; do not flag comments that are merely incomplete or stylistically dated.&rdquo;<br><br>The blueprint also notes: generic guidance like &ldquo;be more conservative&rdquo; works <em>worse</em> than concrete categorical criteria &mdash; it shifts the threshold without sharpening the boundary."},

{i:"c50",d:4,t:"4.1",q:"Why do false positives in one review category matter so much?",
a:"Because <strong>trust is global, not per-category</strong>. A 45% false-positive rate in &ldquo;maintainability&rdquo; makes developers ignore the bot's <em>accurate</em> security findings too.<br><br>Prescribed remedy: <strong>temporarily disable the noisy category</strong>, develop explicit categorical criteria with code examples, measure, then reintroduce. Don't suppress volume across the board &mdash; that costs recall equally."},

{i:"c51",d:4,t:"4.2",q:"How many few-shot examples, and what should they contain?",
a:"<strong>Two to four targeted examples, each with its rationale.</strong> Volume is not the lever &mdash; targeting is.<br><br>Aim them at the <strong>failure region</strong>, use <strong>contrastive near-miss pairs</strong> (an acceptable pattern beside a genuine issue), and keep them <strong>consistent in format, varied in content</strong>. Homogeneous examples teach a region, not a rule.<br><br>Boundary examples must be <em>balanced</em> &mdash; one-sided examples shift behaviour toward whichever side you demonstrated."},

{i:"c52",d:4,t:"4.2",q:"Name four documented uses of few-shot prompting.",
a:"1. <strong>Output format consistency</strong> &mdash; the most effective method for it.<br>2. <strong>Ambiguous cases</strong> &mdash; tool selection, coverage gaps, escalate-vs-resolve boundaries.<br>3. <strong>Distinguishing acceptable patterns from real issues</strong> in code review.<br>4. <strong>Reducing hallucination in extraction</strong> &mdash; by demonstrating correct handling of <em>missing</em> data.<br><br>It also helps the model generalise to new patterns rather than repeat defaults &mdash; but only if the examples vary."},

{i:"c53",d:4,t:"4.3",q:"What is the most reliable way to get schema-conformant output?",
a:"<strong><code>tool_use</code> with a JSON Schema.</strong> Define a tool whose <code>input_schema</code> is your target schema, force it with <code>tool_choice</code>, and read the object from <strong><code>tool_use.input</code></strong>.<br><br>The tool never has to execute &mdash; the arguments <em>are</em> the output. This eliminates JSON syntax errors <em>structurally</em>, rather than requesting good formatting."},

{i:"c54",d:4,t:"4.3",q:"What do JSON Schemas NOT fix?",
a:"<strong>Semantic errors.</strong><br><br>Schemas guarantee <em>structure</em>: well-formed JSON, required fields present, correct types, enum membership.<br><br>They cannot express &ldquo;line items must sum to the stated total&rdquo;, &ldquo;this string is the vendor not the customer&rdquo;, or &ldquo;this date must be plausible&rdquo;. Those need <strong>domain validation in code</strong> &mdash; and schema design that makes checking possible (extract both <code>calculated_total</code> and <code>stated_total</code>)."},

{i:"c55",d:4,t:"4.3",q:"How should a schema handle information that may be absent, or categories that may not fit?",
a:"<strong>Make fields optional/nullable</strong> when the source may not contain the value &mdash; a <code>required</code> field with no source data pressures the model into <em>fabrication</em>.<br><br><strong>Give every enum escape values</strong>: <code>other</code> and <code>unclear</code>, plus a free-text detail field. This prevents forced fits, keeps the controlled vocabulary clean for analytics, and <em>reveals which category you're missing</em> when you review what lands in <code>other</code>."},

{i:"c56",d:4,t:"4.4",q:"What must a retry-with-feedback prompt contain, and when is retry pointless?",
a:"Three parts: <strong>the original source document</strong>, <strong>the incorrect extraction</strong>, and <strong>the specific validation errors</strong>. Drop the source and corrections become fabrications.<br><br><strong>Retry is futile when the information is simply absent from the source</strong> (it lives in a separate manifest). Then: mark the field genuinely absent, or fetch the other source.<br><br>Retries regenerate <em>everything</em> &mdash; re-validate the whole output each time."},

{i:"c57",d:4,t:"4.5",q:"State the four defining facts about the Message Batches API.",
a:"1. <strong>~50% cost savings</strong><br>2. Processing window <strong>up to 24 hours</strong><br>3. <strong>No latency SLA</strong> &mdash; the deciding constraint<br>4. <strong>No multi-turn tool calling</strong> within a single request (batch = single-shot)<br><br>Decision rule: is anything <em>blocked</em> on the result? Yes &rarr; synchronous. No, with a generous deadline &rarr; Batch."},

{i:"c58",d:4,t:"4.5",q:"What does <code>custom_id</code> do, and how do you plan batch cadence?",
a:"<code>custom_id</code> correlates requests with responses (order is <em>not</em> guaranteed) and identifies exactly which items to <strong>re-submit after partial failure</strong>. Use a meaningful system id, e.g. the document id.<br><br>Cadence: <strong>total time = queue wait + processing window</strong>. For a 30-hour SLA against a 24-hour window, submit roughly every 4 hours. Plan against the <em>maximum</em> window, never the typical case. And always sample-test the prompt before a large run."},

{i:"c59",d:5,t:"5.1",q:"What does progressive summarisation destroy first, and what's the remedy?",
a:"<strong>Numeric values, percentages and dates</strong> &mdash; condensed into vague qualitative statements (&ldquo;the charge from earlier this year&rdquo;).<br><br>Remedy: a <strong>persistent case-facts block</strong> maintained by your code <em>outside</em> the summarised history and re-injected every request &mdash; verified identity, order id, amounts, dates, decisions made, computed values.<br><br>Small, exact, never passes through the summariser."},

{i:"c60",d:5,t:"5.1",q:"What is the lost-in-the-middle effect, and what are the three defences?",
a:"Models process the <strong>start and end</strong> of long inputs reliably and may miss material in the <strong>middle</strong>. It's an attention characteristic, not deletion.<br><br>Defences:<br>1. <strong>Position deliberately</strong> &mdash; key findings first, with explicit section headings.<br>2. <strong>Split into passes</strong> so no single input is that long.<br>3. <strong>Durable instructions in the system prompt</strong>, not buried at turn 2 &mdash; presence in history &ne; salience."},

{i:"c61",d:5,t:"5.1",q:"How do you stop verbose tool output eating the context window?",
a:"<strong>Trim to the relevant fields in a <code>PostToolUse</code> hook</strong>, before the result ever enters context. The blueprint's example: 40 fields returned where 5 are needed.<br><br>Ordering of remedies: <strong>prevent at source</strong> (trim results, scope subagent return payloads, delegate verbose work, collapse redundant polls) <em>then</em> mitigate (compact, summarise). Never accommodate with a bigger window."},

{i:"c62",d:5,t:"5.2",q:"What are the valid escalation triggers &mdash; and the invalid ones?",
a:"<strong>Valid:</strong><br>1. Customer <strong>explicitly asks for a human</strong> &rarr; escalate <em>immediately</em>, no diagnostic questions first.<br>2. <strong>Policy gap or exception</strong> &mdash; the agent has no authority to invent policy.<br>3. <strong>Demonstrated inability to progress</strong>.<br><br><strong>Invalid (recurring distractors):</strong> customer sentiment, model self-rated confidence, turn count, message length."},

{i:"c63",d:5,t:"5.2",q:"Classify the three kinds of uncertainty and what each demands.",
a:"<strong>Retrievable</strong> &mdash; the answer exists and the agent can fetch it &rarr; <em>retrieve it</em>.<br><strong>Resolvable by asking</strong> &mdash; multiple customer records match a name &rarr; <em>ask for another identifier and re-query</em>. Never guess identity heuristically.<br><strong>About authority</strong> &mdash; policy is silent or genuinely ambiguous &rarr; <em>escalate</em>.<br><br>Only the third is an escalation trigger."},

{i:"c64",d:5,t:"5.3",q:"What must a subagent return when it fails?",
a:"<strong>Structured error context:</strong> the failure type, <em>what was attempted</em> (the query/input), any <em>partial results</em> gathered, and <em>viable alternatives</em>.<br><br>That lets the coordinator choose between retrying with a modified query, routing elsewhere, and proceeding with annotated partial coverage.<br><br>Handle errors at the <strong>lowest level capable of resolving them</strong>: retry transient faults locally, propagate only the unresolvable."},

{i:"c65",d:5,t:"5.4",q:"Name the symptom of context degradation, and the correct response order.",
a:"<strong>Symptom:</strong> answers become vague and refer to &ldquo;typical patterns in this kind of codebase&rdquo; instead of the specific classes it read.<br><br><strong>Order: externalise, then reduce.</strong> Write findings, decisions, exact paths and measured values to a <strong>scratchpad file</strong> <em>as you go</em> &mdash; then <code>/compact</code> or start fresh seeded with that file. Compacting first is where the specifics are lost.<br><br>Structure the scratchpad with headings so later reads can be selective."},

{i:"c66",d:5,t:"5.5",q:"Why is 97% aggregate accuracy not enough to automate?",
a:"<strong>Aggregate metrics mask poor performance on specific document types or fields.</strong> 97% overall can hide 61% on handwritten forms, or 70% on tax amounts.<br><br>Before automating: validate accuracy <strong>by document type and by field</strong> against a labelled set, automate only the qualifying segments, and route the rest to human review. Over-sample rare/difficult segments in the validation set."},

{i:"c67",d:5,t:"5.5",q:"How should confidence-based routing be built and monitored?",
a:"<strong>Calibrate first</strong> &mdash; field-level, against labelled ground truth. Raw self-rated confidence is uncalibrated and is a recurring wrong answer; <em>calibrated</em> confidence with a known error rate is legitimate.<br><br>Then monitor <strong>both directions</strong>:<br>&bull; <strong>Stratified random sampling of the auto-approved stream</strong> &mdash; the only way to see new error patterns you approved.<br>&bull; <strong>Review-queue approval rate</strong> &mdash; if it's 98%, the threshold is too conservative.<br><br>Calibration drifts with input mix and model changes &mdash; re-measure."},

{i:"c68",d:5,t:"5.6",q:"How is provenance preserved through a multi-agent pipeline?",
a:"<strong>Structurally, end to end:</strong> every finding is a record carrying <em>claim &rarr; source &rarr; supporting quote &rarr; date</em>.<br><br>Preserve those records through aggregation and render them <strong>inline per claim</strong>. Flattening into prose with a trailing bibliography loses it &mdash; a bibliography proves consultation, not <em>support</em>.<br><br>Trace apparent corroboration to origins: three articles reporting one study is one piece of evidence."},

{i:"c69",d:5,t:"5.6",q:"Two sources give conflicting figures. What do you do?",
a:"<strong>Don't pick, don't hide, don't block.</strong><br><br>The analysis agent <em>completes its scope</em>, carries <strong>both values annotated as conflicting with full attribution</strong>, and lets the coordinator reconcile.<br><br>First check whether they actually conflict: <strong>dates, definitions and population scope</strong> explain most apparent contradictions (a 2021 figure vs a 2025 figure is a trend, not a disagreement). That's why findings must carry all three."},

{i:"c70",d:5,t:"5.3",q:"What is coverage annotation and why does it matter?",
a:"Marking, <strong>per section</strong>, what is fully supported versus partial or missing, <em>and why</em>: &ldquo;Music: partial &mdash; search agent timed out after two attempts.&rdquo;<br><br>Readers calibrate trust on confident prose, so an unannotated gap actively misleads. A blanket disclaimer carries no information; silently dropping the subtopic is equally invisible.<br><br>It depends on structured error propagation &mdash; the coordinator can only annotate what subagents told it."}
);
