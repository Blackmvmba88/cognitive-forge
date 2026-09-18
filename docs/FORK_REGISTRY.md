# Cognitive Fork Registry

The fork registry prevents new ideas from silently overwriting earlier ones. A fork may depend on another fork, but it keeps its own responsibility and history.

| ID | Name | Responsibility | Initial dependency |
|---|---|---|---|
| FORK-001 | User Key | Stable user/context identity boundary and retrieval keying | Memory |
| FORK-002 | Context Router | Select context relevant to the current objective | User Key |
| FORK-003 | Life Tree | Long-horizon graph of projects, decisions, relationships, and lineage | Context Router |
| FORK-004 | Adaptive Interface | Adapt the control surface to current task/state | Context Router |
| FORK-005 | Proactive / Outbound AI | Detect when an outbound action may be useful; requires authorization gates | DEFINE |
| FORK-006 | Linguistic Identity | Preserve communication style, terminology, and semantic continuity | User Key |
| FORK-007 | Diagram / BRAIN | Build inspectable graphs from evidence and relationships | Real Watcher |
| FORK-008 | Real Watcher | Observe real state and emit deterministic evidence | — |
| FORK-009 | DEFINE | Convert ambiguity into explicit executable contracts | Diagram / BRAIN |
| FORK-010 | Cognitive Fork Manager | Preserve divergent hypotheses/ideas without destructive overwrite | DEFINE |

## Activation order

```text
FORK-008 Real Watcher
        ↓
FORK-007 Diagram / BRAIN
        ↓
FORK-009 DEFINE
        ↓
FORK-010 Cognitive Fork Manager
        ↓
FORK-001 User Key
        ↓
FORK-002 Context Router
```

The remaining forks can then attach without forcing the runtime to pretend it already understands everything.

## Fork rule

A new branch should be created when at least one of these changes:

- objective,
- assumptions,
- constraints,
- implementation strategy,
- evidence interpretation,
- target domain.

Do not delete the parent idea merely because a child appears stronger.
