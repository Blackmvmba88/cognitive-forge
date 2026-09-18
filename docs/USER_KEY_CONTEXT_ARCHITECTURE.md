# FORK-001 / FORK-002 — User Key + Context Router

## Purpose

The runtime needs continuity without dumping all remembered information into every task.

The split is deliberate:

- **User Key** identifies the stable context boundary.
- **Context Router** selects only the context relevant to the active objective.

## User Key

A User Key is not a prose biography. It is a stable namespace used to associate durable context, project lineage, preferences, prior decisions, and evidence.

The key should avoid embedding secrets directly.

## Context Router

The router receives:

```text
objective + current evidence + available context references
```

and returns a bounded context set with provenance.

It should optimize for:

1. relevance,
2. recency when recency matters,
3. explicit user constraints,
4. project continuity,
5. minimal unrelated disclosure.

## Routing rule

```text
available memory ≠ active context
```

The existence of information does not make it relevant to the current task.

## Future contract

A routed context item should eventually carry:

```json
{
  "context_id": "ctx/...",
  "source": "memory|repo|file|conversation|sensor",
  "reason_selected": "...",
  "confidence": 0.0,
  "scope": "task|project|long_term"
}
```

This becomes useful after Real Watcher, Diagram / BRAIN, DEFINE, and the Fork Manager provide a stable evidence spine.
