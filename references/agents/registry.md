# Agent Registry

This skill uses a capability-oriented multi-agent model. Activate only the smallest subset needed for the task.

The principal agent owns clarification. No agent mesh should activate until the user goal, scope, allowed behavior change, and main constraints are clear enough to execute without guessing. If those are already explicit, proceed without redundant questions.
Technical uncertainty is not user ambiguity. Resolve library, API, command, version, and framework questions with local tooling or MCPs before asking the user, unless only the user can supply the missing project rule.

- `Observability Agent`: structural telemetry, dependency graph, complexity, coupling, cohesion
- `Blueprint Architect`: requirements-to-structure blueprint generation
- `Refactoring Engine`: syntax-aware and paradigm-aware structural refactors
- `Regression Sentinel`: A/B breaking change and side-effect drift detection
- `Execution Orchestrator`: framework-agnostic verification runner
- `Governance & Compliance`: principle enforcement, lint-like checks, architecture policy validation
- `Synthesis Reporting`: result aggregation for terminal or chat

Typical activation patterns:

- **Quick**: Observability + Refactoring Engine + Execution Orchestrator
- **Standard**: Observability + Blueprint Architect or Refactoring Engine + Regression Sentinel + Execution Orchestrator + Governance & Compliance
- **Deep**: all seven agents when contracts, boundaries, or architecture are in motion

Do not activate extra agents just because they exist. The mesh is modular, not ceremonial.
