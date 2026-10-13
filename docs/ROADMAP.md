# Phased Product Roadmap & Actionable TODOs

```
|=-----------------------------------------------------------------------------------=|
|  DOC: ROADMAP-V1.2  |  STATUS: WORKING PLAN  |  PROVENANCE: fsecurity CORE         |
|=-----------------------------------------------------------------------------------=|
```

---

## Phase Overview

```
+-----------------------------------------------------------------------------------+
| [PHASE 0: FOUNDATION]                                          STATUS: IN PROGRESS|
| Identity, Governance, Security Thesis, and Repository Foundation                  |
+-----------------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------------+
| [PHASE 1: NATIVE HARNESS CORE]                                  STATUS: PLANNED  |
| Provider Routing, Primitive Tools, Streaming CLI, and Sandbox Boundaries          |
+-----------------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------------+
| [PHASE 2: SCOPE SYNTHESIZER & CAPABILITIES]                     STATUS: PLANNED  |
| Scope Ingestion, Boundary Compiler, On-Demand Skills & MCP Integration            |
+-----------------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------------+
| [PHASE 3: CONCURRENT SCANNERS & VERIFICATION]                   STATUS: PLANNED  |
| Ephemeral Sandboxes, Telemetry Daemon, Automated PoC Reproduction Loops           |
+-----------------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------------+
| [PHASE 4: RESEARCHER PREVIEW & HARDENING]                       STATUS: PLANNED  |
| Headless CI Execution (`fsecurity exec`), Structured Finding Reports, Portal       |
+-----------------------------------------------------------------------------------+
```

---

## Detailed Phase Breakdown

### Phase 0: Foundation, Identity & Governance *(Current Milestone)*
- [x] **Architecture and Foundation Specifications:** Author canonical docs ([`docs/ARCHITECTURE.md`](ARCHITECTURE.md), [`docs/ROADMAP.md`](ROADMAP.md), [`docs/DECISIONS_AND_NON_GOALS.md`](DECISIONS_AND_NON_GOALS.md), [`DESIGN.md`](../DESIGN.md)).
- [x] **Agent Governance Architecture:** Author canonical portable [`AGENTS.md`](../AGENTS.md), thin [`CLAUDE.md`](../CLAUDE.md), scoped [`.claude/rules/`](../.claude/rules/), and security reporting policy in [`SECURITY.md`](../SECURITY.md).
- [x] **Repository Licensing:** Adopt canonical GNU AGPL-3.0-or-later in root [`LICENSE`](../LICENSE).
- [x] **Brand Kit & Mascot:** Author canonical master vector mark (**The Bastion Reticle** enclosing canonical `f`), original mascot (**`cerb`**: The Bastion Sentinel Hound), frozen vector wordmark outlines, automated generator script, and verification test suite.
- [ ] **Human Review & Approval:** Present complete uncommitted working tree and review artifacts for human approval.

### Phase 1: Native Harness Core & Universal Providers *(Candidate Implementations)*
- [ ] **Native Core Prototyping:** Implement and benchmark candidate engine architecture (evaluating Rust for sub-20ms cold boot, low memory footprint, and memory-safe concurrency).
- [ ] **Universal Provider Layer:** Implement direct streaming API clients for:
  - Anthropic Messages API
  - OpenAI Chat Completions / Responses API
  - Google Gemini API
  - OpenRouter API
  - Local OpenAI-compatible endpoints (Ollama, vLLM, LM Studio)
- [ ] **Primitive Tool Execution Engine:** Implement minimal, high-discipline tools (`read_file`, `write_file`, `edit_file`, `run_sandboxed_command`, `http_probe`) with strict output budgeting and truncation protection.
- [ ] **Basic Terminal Streaming Interface:** Keyboard-driven terminal output with fast feedback, TrueColor rendering, and clean ANSI degradation.
- [ ] **Process Execution Sandbox:** Initial OS-level command execution with approval tiers (passive inspection, interactive confirmation, sandboxed auto-exec).

### Phase 2: Scope Synthesizer & Capability Hub
- [ ] **Scope Ingestion & Boundary Engine:**
  - Build target boundary validator for CIDR ranges, subdomains, and API paths.
  - Implement heuristic ambiguity detector to surface underspecified scope boundaries before probe execution.
  - Interactive boundary confirmation modal for operator scope sign-off.
- [ ] **Assessment Spec Compiler:** Generate structured internal task trees (`scope.md` & `tasks.md` format) from synthesized intent.
- [ ] **On-Demand Security Skill Hub:**
  - Implement on-demand security skill loader (`fsecurity skills add / list / invoke`).
  - Strict context budgeting: inject security skills into active prompt only during relevant assessment tasks.
- [ ] **MCP Protocol Integration:** Support `stdio` and `sse` Model Context Protocol servers for standard security tool adapters.

### Phase 3: Concurrent Scanners & Verification Loops
- [ ] **Ephemeral Sandbox Provisioning:**
  - Implement isolated task environments (`fsecurity sandbox spawn <task-id>`).
  - Isolate speculative network traffic and local state from the primary workspace.
  - Enforce per-target network egress filtering.
- [ ] **Telemetry & Rate-Limit Monitor Daemon:**
  - Background daemon monitoring packet rate, concurrency, and target HTTP status responses.
  - Early throttle detection to prevent unintended server degradation and backoff.
- [ ] **Proof-of-Concept Reproduction Engine:**
  - Automated replay and deterministic verification of candidate vulnerabilities.
  - Raw request/response capture and minimal cURL reproduction command generation.
  - Bounded verification limits to prevent redundant probe cycles.

### Phase 4: Researcher Preview & Ecosystem
- [ ] **Headless Scriptable CLI (`fsecurity exec`):** Support non-interactive execution for DevSecOps pipelines and automated security checks.
- [ ] **Structured Finding Package Generator:** Automated generation of human review packages (executive summary, vulnerability diff, raw evidence, remediation advice).
- [ ] **Skill Crystallization:** Generalize successful multi-step assessment workflows into reusable project-specific security skills.
- [ ] **Public Distribution & Installer:** Multi-platform installation scripts (`curl | sh`, Homebrew tap, binary releases) and comprehensive documentation.
- [ ] **Documentation Portal:** Deploy static documentation frontend (evaluating Starlight) powered by portable Markdown source files.

