/* ============================================================
   CCAR-F Master Question Bank -- metadata
   Domains, weights, task statements and exam scenarios,
   mirroring the published Claude Certified Architect
   (Foundations) exam blueprint.
   ============================================================ */

const DOMAINS = {
  1:{n:"Agent Architecture & Orchestration", w:27, c:"var(--d1)"},
  2:{n:"Tool Design & MCP Integration",      w:18, c:"var(--d2)"},
  3:{n:"Claude Code Configuration & Workflows", w:20, c:"var(--d3)"},
  4:{n:"Prompt Engineering & Structured Output", w:20, c:"var(--d4)"},
  5:{n:"Context Management & Reliability",   w:15, c:"var(--d5)"}
};

const TASKS = {
  "1.1":"Designing agentic loops for autonomous task execution",
  "1.2":"Orchestrating multi-agent systems (coordinator / subagent)",
  "1.3":"Subagent calls, context passing and spawning",
  "1.4":"Multi-step workflows: enforcement and handoff patterns",
  "1.5":"Agent SDK hooks for intercepting tool calls and normalising data",
  "1.6":"Task decomposition strategies for complex workflows",
  "1.7":"Session state, resuming and forking",
  "2.1":"Designing tool interfaces with clear descriptions",
  "2.2":"Structured error responses for MCP tools",
  "2.3":"Allocating tools across agents and configuring tool_choice",
  "2.4":"Integrating MCP servers into Claude Code and agent workflows",
  "2.5":"Selecting and applying built-in tools (Read/Write/Edit/Bash/Grep/Glob)",
  "3.1":"CLAUDE.md hierarchy, scope and modular organisation",
  "3.2":"Custom slash commands and skills",
  "3.3":"Path-specific rules for conditional convention loading",
  "3.4":"Planning mode vs direct execution",
  "3.5":"Iterative refinement for progressive improvement",
  "3.6":"Integrating Claude Code into CI/CD pipelines",
  "4.1":"Prompts with explicit criteria to improve accuracy",
  "4.2":"Few-shot prompting for output consistency",
  "4.3":"Structured output with tool_use and JSON Schemas",
  "4.4":"Validation, retries and feedback loops for extraction quality",
  "4.5":"Efficient batch processing strategies",
  "4.6":"Multi-instance and multi-pass review architectures",
  "5.1":"Managing conversation context to preserve critical information",
  "5.2":"Escalation patterns and resolving ambiguity",
  "5.3":"Error propagation strategies in multi-agent systems",
  "5.4":"Managing context when investigating large codebases",
  "5.5":"Human oversight and confidence calibration",
  "5.6":"Preserving provenance and handling uncertainty in synthesis"
};

const SCEN = {
  CSA:{n:"Customer Support Resolution Agent",
    b:"You are building a customer support agent on the Claude Agent SDK to handle returns, billing disputes and account issues. It uses MCP tools <code>get_customer</code>, <code>lookup_order</code>, <code>process_refund</code> and <code>escalate_to_human</code>. The business target is 80%+ first-contact resolution with appropriate escalation to human agents."},
  CGC:{n:"Code Generation with Claude Code",
    b:"Your team uses Claude Code to accelerate development: code generation, refactoring, debugging and documentation. You are responsible for the shared configuration &mdash; CLAUDE.md, custom slash commands, skills and rules &mdash; and for guiding when to use planning mode versus direct execution."},
  MAR:{n:"Multi-Agent Research System",
    b:"A coordinator agent delegates to specialised subagents: web research, document analysis, synthesis and report generation. The system must produce complete, well-cited reports and degrade gracefully when individual subagents fail."},
  DPT:{n:"Developer Productivity Tools",
    b:"An agent helps engineers explore unfamiliar codebases, generate boilerplate and automate routine tasks. It relies on Claude Code built-in tools (Read, Write, Edit, Bash, Grep, Glob) plus MCP servers for Jira, GitHub and internal systems."},
  CCI:{n:"Claude Code for Continuous Integration",
    b:"Claude Code runs inside a CI/CD pipeline for automated code review, test generation and pull-request feedback. Runs must be non-interactive, emit machine-readable output, and keep false positives low enough that developers keep trusting the bot."},
  SDE:{n:"Structured Data Extraction",
    b:"A pipeline extracts structured information from messy, unstructured documents (invoices, contracts, scanned forms), validates output against JSON Schemas and must sustain high field-level accuracy while handling edge cases correctly."},
  CAP:{n:"Conversational AI Architecture Patterns",
    b:"You design multi-turn conversational systems: context-window management, instruction persistence across turns, memory strategies, tool design for safe execution, and handling ambiguous or conflicting user input."},
  AAT:{n:"Agentic AI Tools",
    b:"You are designing and hardening the tool layer that agentic systems depend on: tool contracts, permissioning, observability, idempotency, and the boundary between what the model decides and what your code guarantees."},
  GEN:{n:"General knowledge check",
    b:"A direct knowledge question with no scenario attached &mdash; the underlying fact, path, parameter or decision rule the exam expects you to know cold."}
};
