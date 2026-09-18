# Architecture

## Purpose

Cognitive Forge is a modular cognitive runtime. It converts raw signals into structured evidence and routes that evidence through explicit stages rather than hiding reasoning inside one monolithic agent.

## Canonical loop

```text
OBSERVE → RELATE → UNDERSTAND → DEFINE → REMEMBER → DECIDE → INTERVENE
   ↑                                                                  │
   └──────────────────────────────────────────────────────────────────┘
```

### OBSERVE
Collect raw facts without interpreting them. Examples: repository files, timestamps, changed paths, process state, sensor readings.

### RELATE
Connect observations to existing entities, previous snapshots, projects, goals, and known interfaces.

### UNDERSTAND
Build hypotheses or models from the related evidence. This layer must mark confidence and provenance.

### DEFINE
Turn ambiguous interpretation into an explicit contract: objective, constraints, inputs, outputs, acceptance criteria, and prohibited actions.

### REMEMBER
Persist stable knowledge, decisions, evidence, and branch lineage so the system does not repeatedly rediscover the same facts.

### DECIDE
Select a next action from defined options. Decision should remain distinguishable from observation.

### INTERVENE
Perform an external mutation only when authorized and then read back the result for verification.

## Evidence model

Every cognitive artifact should be able to answer:

- What was directly observed?
- What was inferred?
- How confident is the inference?
- What evidence supports it?
- What changed relative to the previous state?
- Which branch/fork owns the idea?
- What action, if any, was authorized?

## Form-C: circular-dependency evidence

When modules refer to each other in a cycle, the runtime must not silently flatten the cycle into a fake hierarchy.

A circular dependency record should contain:

```json
{
  "type": "circular_dependency",
  "members": ["A", "B", "C"],
  "evidence": ["A→B", "B→C", "C→A"],
  "confidence": 1.0
}
```

The rule is simple: **represent the loop as evidence before trying to resolve it.**

## Initial execution spine

1. Real Watcher collects deterministic repository evidence.
2. Diagram / BRAIN converts evidence into a graph.
3. DEFINE creates explicit contracts around ambiguous or actionable nodes.
4. Cognitive Fork Manager preserves divergent branches.
5. User Key + Context Router attach relevant persistent context.

## Mutation discipline

For any external write:

```text
READ → PLAN → WRITE → READ BACK → COMPARE → CERTIFY
```

A successful API response is not equivalent to a certified result.
