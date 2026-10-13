# Architecture Thesis

```
|=-----------------------------------------------------------------------------------=|
|  DOC: ARCHITECTURE-V1.2  |  STATUS: WORKING SPEC  |  PROVENANCE: fsecurity CORE    |
|=-----------------------------------------------------------------------------------=|
```

---

## 1. System Vision and Operational Model

`fsecurity` is structured as a decoupled, multi-tier autonomous cybersecurity engineering workspace and harness. It transforms high-level security objectives into verified assessment findings and reproducible telemetry by establishing an explicit operational contract:

* **The Human Operator** specifies the legitimate target objectives, rules of engagement, and strict authorization boundaries.
* **The Specialist Agent** determines its own workflow, capability sequencing, diagnostic hypotheses, and testing methodology within those boundaries.
* **The Workspace Harness** enforces scope boundaries before any packet is transmitted, provides isolated ephemeral execution environments, and requires deterministic, runnable proof before any vulnerability is reported.

```
+-----------------------------------------------------------------------------------+
|                                 OPERATOR INTENT                                   |
|                ("Audit GraphQL API endpoints for IDOR within *.target.internal")   |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                     TIER 1: SCOPE SYNTHESIZER & INTENT COMPILER                   |
|                                                                                   |
|   +-----------------------+   +----------------------+   +--------------------+   |
|   | Scope & Target Probe  |   | Boundary Enforcer    |   | Assessment Spec    |   |
|   | (CIDR, domain, routes)|-->| (Prevent out-of-scope|-->| Compiler           |   |
|   |                       |   |  drift / violations) |   | (Formal test tree) |   |
|   +-----------------------+   +----------------------+   +--------------------+   |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                     TIER 2: CAPABILITY & ORCHESTRATION ENGINE                     |
|                                                                                   |
|   +-----------------------+   +----------------------+   +--------------------+   |
|   | Model Router          |   | On-Demand Skill Hub  |   | MCP Security Bridge|   |
|   | (Strategic vs Worker) |   | (Recon, Web, Binary) |   | (Sandboxed tools)  |   |
|   +-----------------------+   +----------------------+   +--------------------+   |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                     TIER 3: ISOLATED WORKSPACE SECURITY HARNESS                   |
|                              (Sandboxes & Swarm Execution)                        |
|                                                                                   |
|   +-----------------------+   +----------------------+   +--------------------+   |
|   | Ephemeral Process     |   | Live Telemetry &     |   | Terminal Stream    |   |
|   | Sandboxes (Isolated)  |   | Rate-Limit Monitor   |   | & Workspace State  |   |
|   +-----------------------+   +----------------------+   +--------------------+   |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                     TIER 4: VERIFICATION & REPRODUCIBILITY ENGINE                 |
|                                                                                   |
|   +-----------------------+   +----------------------+   +--------------------+   |
|   | PoC Reproducer        |   | Evidence Collector   |   | Structured Finding |   |
|   | (Deterministic runner)|-->| (Raw requests/traces)|-->| Package Generator  |   |
|   +-----------------------+   +----------------------+   +--------------------+   |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                           VERIFIED SECURITY ASSESSMENT                            |
|                     (Actionable finding with reproducible proof)                  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Current Reality (Phase 0 Foundation)

To maintain absolute engineering discipline, `fsecurity` strictly distinguishes what exists in the repository today from future roadmap hypotheses:

* **Repository Foundation & Governance:**
  - Portable root [`AGENTS.md`](../AGENTS.md) defining 16 universal operating invariants.
  - Path-scoped agent instructions in [`.claude/rules/`](../.claude/rules/) for documentation, branding, and licensing.
  - Vulnerability disclosure and reporting policy in [`SECURITY.md`](../SECURITY.md).
  - Strong copyleft licensing under [`LICENSE`](../LICENSE) (GNU AGPL-3.0-or-later).
* **Brand Identity & Mathematical Design System:**
  - Complete design specification in [`DESIGN.md`](../DESIGN.md).
  - Master vector mark: **The Bastion Reticle** enclosing the shared `ftools` canonical `f` glyph with Electric Phosphor telemetry nodes and cardinal calipers.
  - Canonical mascot: **`cerb`** (The Bastion Sentinel Hound) constructed entirely from terminal character geometry.
  - Tactical color palette: Obsidian Night (`#080B10`), Vault Charcoal (`#101520`), Boreas Slate (`#2E384D`), Glacier White (`#E6EDF5`), Electric Phosphor (`#00F59B`), Cyber Azure (`#38BDF8`).
* **Automated Asset Generation & Invariant Verification:**
  - [`scripts/generate_brand.py`](../scripts/generate_brand.py): Deterministically derives all 29 production brand assets from master vectors with zero runtime font dependencies.
  - [`scripts/verify_brand.py`](../scripts/verify_brand.py): Verifies all 7 core brand invariants (coordinates, uniform scaling, zero `<text>` tags, avatar parity, dimensions, transparency contract).
  - [`scripts/verify_foundation.py`](../scripts/verify_foundation.py): Validates markdown hyperlinks, repository cleanliness, and SPDX license headers.
* **Architecture Specifications:**
  - System architecture thesis in this document ([`docs/ARCHITECTURE.md`](ARCHITECTURE.md)).
  - Explicit architectural decisions and non-goals in [`docs/DECISIONS_AND_NON_GOALS.md`](DECISIONS_AND_NON_GOALS.md).
  - Phased development roadmap in [`docs/ROADMAP.md`](ROADMAP.md).

*Current Reality Status: No production runtime binaries or install packages have been compiled or published yet. Engine implementation begins in Phase 1 following human review.*

---

## 3. Committed Product Principles

These principles represent invariant commitments across all future implementation phases:

1. **Scope Before Packets:** No network traffic, DNS lookup, or scanner invocation may occur before target parameters are formally compiled and validated against the authorized scope specification.
2. **Agent Autonomy Inside Scope:** The human defines objectives, authorization, and boundaries; the specialist agent freely selects its workflow, capability sequencing, diagnostic hypotheses, and testing methodology within those bounds.
3. **Runnable Verification (Zero Speculative Claims):** A vulnerability claim is strictly provisional until confirmed by an automated, deterministic reproduction step. Speculative findings that cannot be proven with runnable evidence are discarded.
4. **Context Budgeting & Dynamic Loading:** Inactive security scanners, large wordlists, and bulky tool schemas remain on disk and load dynamically on demand. Active prompt context must never be saturated with inactive capability definitions.
5. **Local-First Authority:** Local workspace files, execution logs, and git history remain the sole authoritative record of findings. Remote caches and cloud telemetry are strictly secondary.
6. **Transparent Routing & Fail Closed on Uncertainty:** Silent model swapping or hidden fallback behavior is prohibited. If scope boundaries or tool permissions are ambiguous, the harness fails closed and requests human confirmation.

---

## 4. Future Candidates and Hypotheses

These items represent actively evaluated design candidates and hypotheses for Phase 1 and beyond, rather than locked immutable choices:

### Candidate 1: High-Performance Native Core (Rust)
* **Hypothesis:** Compiling the core engine in Rust produces a single self-contained static binary with sub-20ms cold boot times, low memory consumption under concurrent agent probing, and safe multi-worker memory concurrency.
* **Evaluation Status:** Candidate architecture for Phase 1. Will be prototyped against CLI performance benchmarks.

### Candidate 2: Universal Streaming Provider Abstraction
* **Hypothesis:** A unified provider layer that streams completions across Anthropic, OpenAI, Google Gemini, and local OpenAI-compatible endpoints (Ollama, vLLM) prevents vendor lock-in and allows task-specific model routing.
* **Evaluation Status:** Candidate architecture for Phase 1.

### Candidate 3: Lightweight Ephemeral Sandboxes
* **Hypothesis:** Executing tool probes within ephemeral isolated sandboxes (such as Linux namespaces, containers, or lightweight microVMs) isolates speculative network traffic and prevents accidental contamination of the host workspace.
* **Evaluation Status:** Candidate architecture for Phase 2–3.

### Candidate 4: Telemetry Monitor Daemon
* **Hypothesis:** A background telemetry daemon tracking request rates, concurrency levels, and server response distributions (e.g. HTTP 429/503) will automatically prevent unintentional denial-of-service against target infrastructure.
* **Evaluation Status:** Candidate architecture for Phase 3.

### Candidate 5: Static Documentation Portal (Starlight)
* **Hypothesis:** Deploying a Starlight-powered documentation portal while retaining portable GitHub-Flavored Markdown source files provides fast, accessible web navigation and search.
* **Evaluation Status:** Candidate frontend for Phase 4.

---

## 5. Execution Lifecycle State Machine

```
     [IDLE]
        |  (Operator Objective & Target Input)
        v
[SCOPE SYNTHESIS] <----> [AMBIGUITY & BOUNDARY RESOLUTION] (If target clarification needed)
        |
        v (Authorized Spec Compiled)
[ORCHESTRATION & ROUTING] (Specialist Agent Selects Models, Skills, MCP Servers)
        |
        v
[SANDBOX ISOLATION] (Provision Ephemeral Process Sandbox with Egress Guards)
        |
        v
[PROBE EXECUTION] <----> [RATE & TELEMETRY MONITOR]
        |
        v (Anomaly / Vulnerability Candidate Identified)
[SCOPE AUDIT] ---------> (Boundary Violation Detected: Halt & Quarantine)
        | (Clean)
        v
[PROOF VERIFICATION] (Execute Deterministic Reproduction Check)
        |
        +--- [UNVERIFIED] ---> (Discard Speculative Anomaly / Refine Probe)
        |
        v [CONFIRMED]
[STRUCTURED REVIEW PACKAGE] (Present Reproduction Command, Raw Traces, Remediation)
```

