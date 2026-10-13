# Architecture Decisions and Non-Goals

```
|=-----------------------------------------------------------------------------------=|
|  DOC: DECISIONS-V1.2  |  STATUS: CANONICAL  |  PROVENANCE: fsecurity CORE          |
|=-----------------------------------------------------------------------------------=|
```

---

## 1. Committed Architectural Decisions

The following architectural principles and operational decisions are fully resolved and canonical:

### Decision 1: Scope-Bounded Autonomous Operation
* **Principle:** Human defines objectives, authorization, and scope boundaries; the specialist agent determines its own workflow, capability sequence, and methodology within those bounds.
* **Rationale:** In cybersecurity operations, unconstrained agents risk spraying traffic across unauthorized networks or shared infrastructure, while micro-managed chat agents impose an unbearable coordination tax on the researcher. Clear boundaries with autonomous execution resolve both problems.

### Decision 2: Mandatory Runnable Verification
* **Principle:** Every reported vulnerability requires deterministic, runnable proof-of-concept verification before it enters the final assessment package.
* **Rationale:** AI models excel at hypothesizing attack vectors but frequently hallucinate non-existent vulnerabilities. Requiring executable verification eliminates false positives and ensures findings are actionable.

### Decision 3: Terminal-First Ergonomics
* **Principle:** Command-line first architecture, Unix composability, and headless scriptability (`fsecurity exec`).
* **Rationale:** Security engineers and researchers live in the terminal. Direct terminal interfaces provide instant keyboard navigation, low resource footprint, and seamless integration into automated security testing pipelines.

### Decision 4: Dynamic On-Demand Capability Loading
* **Principle:** Security scanners, protocol parsers, and Model Context Protocol (MCP) servers index on disk and load strictly on demand based on task classification.
* **Rationale:** Dumping inactive tool schemas and dictionaries into the system prompt causes severe context rot and wastes tokens. Dynamic loading keeps reasoning focused and minimizes token costs.

### Decision 5: Local-First Authority
* **Principle:** Local workspace files, local execution logs, and git history remain the sole authoritative source of truth.
* **Rationale:** Security assessment results often contain sensitive internal telemetry and vulnerability data that must not leak to unmanaged cloud backends.

### Decision 6: Repository Licensing
* **Principle:** GNU AGPL-3.0-or-later for fsecurity source code.
* **Rationale:** Strong copyleft protects researcher agency, guarantees network transparency for agentic security services, and prevents closed-source hoarding of security assessment infrastructure.

---

## 2. Evaluated Candidate Hypotheses (Future Candidates)

The following technical implementation choices represent evaluated hypotheses rather than locked Phase 0 certainties:

### Candidate 1: Rust for Native Engine Implementation
* **Hypothesis:** Compiling the core harness in Rust will achieve sub-20ms cold boot times, low memory consumption under concurrent agent probing, and safe multi-worker memory concurrency without runtime garbage collection pauses.
* **Status:** Candidate architecture for Phase 1. Will be prototyped and benchmarked against runtime criteria before final commitment.

### Candidate 2: Universal Streaming Provider Abstraction
* **Hypothesis:** A unified provider abstraction supporting Anthropic, OpenAI, Gemini, and local OpenAI-compatible endpoints (Ollama, vLLM) enables flexible model routing without vendor lock-in.
* **Status:** Candidate architecture for Phase 1.

### Candidate 3: Lightweight Ephemeral Sandboxes
* **Hypothesis:** OS-level isolation (e.g. Linux namespaces, containers, or lightweight microVMs) will prevent concurrent tool probes from contaminating the host workspace.
* **Status:** Candidate architecture for Phase 2–3.

### Candidate 4: Starlight Documentation Portal
* **Hypothesis:** Deploying Starlight for technical documentation while maintaining source content as portable GitHub-Flavored Markdown in `docs/` provides fast navigation and zero-config search.
* **Status:** Candidate documentation frontend for Phase 4.

---

## 3. Explicit Non-Goals

To maintain sharp engineering focus, `fsecurity` defines what it will not do:

1. **Not an Unconstrained Weaponization Harness:**
   `fsecurity` will not build unauthorized offensive weaponry or unconstrained exploit delivery tools. It is engineered strictly for authorized security assessments, legitimate bug bounty research, and verified defensive testing within explicit scope boundaries.

2. **Not a Heavy Desktop Electron GUI:**
   `fsecurity` will not distribute a 300MB Chromium shell. It is built terminal-native first, fast, and resource-conscious.

3. **Not "Vibe Testing" Without Reproducible Proof:**
   `fsecurity` rejects speculative vulnerability claims where an assistant hallucinates flaws without runnable proof-of-concept validation. Every reported finding requires reproducible verification and structured reproduction steps.

4. **Not a Context Stuffer:**
   `fsecurity` will not inject dozens of static tool schemas, wordlists, and unneeded payload dictionaries into the active context window. Inactive capabilities remain indexed on disk and load dynamically on demand.

5. **Not Synthetic Marketing Theater or Fictitious Benchmarks:**
   `fsecurity` will never publish synthetic benchmark claims, unverified performance graphs, or misleading marketing assertions. Product claims must be reproducible by running standard test commands.

