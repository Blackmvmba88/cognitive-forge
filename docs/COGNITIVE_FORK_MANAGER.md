# FORK-010 — Cognitive Fork Manager

## Mission

Preserve divergence without destroying ancestry.

A cognitive system should not replace an earlier idea merely because a newer interpretation appears more useful. It should retain lineage and make the relationship explicit.

## Core record

```json
{
  "fork_id": "FORK-010/example",
  "parent": "idea/original",
  "reason": "implementation strategy changed",
  "assumptions_changed": ["runtime target"],
  "status": "active"
}
```

## Fork triggers

Create a fork when one or more of these materially changes:

- objective,
- constraints,
- assumptions,
- evidence interpretation,
- target domain,
- implementation strategy.

## Non-trigger

A typo correction or formatting-only change does not create a cognitive fork.

## Merge rule

A merge may consolidate implementation, but it must not erase useful lineage. The system should still be able to answer:

- where did this idea come from?
- what alternative existed?
- why was this branch selected for implementation?
- what evidence would reopen the alternative?

## Relationship to Git

Git branches are an implementation mechanism, not the cognitive model itself.

One cognitive fork may map to:
- a Git branch,
- a document branch,
- a hypothesis node,
- a runtime state branch,
- or no code change at all.

The Fork Manager records semantic divergence; Git records source history.
