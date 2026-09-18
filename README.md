# BlackMamba Cognitive Forge

**Cognitive Forge** is the executable core of the BlackMamba cognitive architecture.

The repository began as **Autonomous Fastener Intelligence & Dispensing runtime (mobile + industrial)**. That industrial origin is preserved here as an early domain application; the runtime is now generalized into a reusable cognitive system that can observe signals, relate them to context, build understanding, define what matters, preserve memory, decide what to do, and intervene only when action is justified.

> Nothing is irrelevant. Every signal can become structured memory.

## Core loop

```text
OBSERVE
  ↓
RELATE
  ↓
UNDERSTAND
  ↓
DEFINE
  ↓
REMEMBER
  ↓
DECIDE
  ↓
INTERVENE
  ↺
```

Each stage is inspectable and replaceable. Evidence is kept separate from inference, and external actions should remain attributable to an explicit decision.

## First executable target

**Real Watcher v0.0.1**

```bash
watcher scan ./repo
```

The Watcher does not try to be the whole brain. It observes a repository, extracts structural evidence, and emits a deterministic snapshot for later stages.

## Architecture principles

1. **Evidence before inference** — observations and interpretations are represented separately.
2. **Memory before repetition** — reusable knowledge is preserved instead of rediscovered.
3. **Fork instead of overwrite** — divergent ideas survive as explicit branches.
4. **Definition before action** — ambiguous intent becomes an explicit contract before execution.
5. **Modular cognition** — watcher, context, memory, reasoning, and intervention are separable.
6. **Read → Plan → Write → Read back → Compare → Certify** for external mutations.
7. **Human authority remains final** for consequential external actions.

## Cognitive fork registry

- **FORK-001 — User Key**
- **FORK-002 — Context Router**
- **FORK-003 — Life Tree**
- **FORK-004 — Adaptive Interface**
- **FORK-005 — Proactive / Outbound AI**
- **FORK-006 — Linguistic Identity**
- **FORK-007 — Diagram / BRAIN**
- **FORK-008 — Real Watcher**
- **FORK-009 — DEFINE**
- **FORK-010 — Cognitive Fork Manager**

See `docs/FORK_REGISTRY.md`.

## First implementation spine

```text
Real Watcher
    ↓
Diagram / BRAIN
    ↓
DEFINE
    ↓
Cognitive Fork Manager
    ↓
User Key / Context Router
```

This sequence gives the architecture measurable evidence and branch-preserving behavior before proactive agents or adaptive UI are introduced.

## Repository layout

```text
.
├── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── FORK_REGISTRY.md
│   ├── REAL_WATCHER.md
│   ├── USER_KEY_CONTEXT_ARCHITECTURE.md
│   └── COGNITIVE_FORK_MANAGER.md
├── src/
│   └── blackmamba_cognitive/
│       ├── __init__.py
│       └── watcher.py
├── tests/
│   └── test_watcher.py
└── pyproject.toml
```

## Phase

**Phase 0 — architecture recovery + executable seed.**

The immediate milestone is simple and testable: install the package, run `watcher scan <path>`, and obtain a deterministic JSON description of the observed repository.
