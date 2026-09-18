# FORK-008 — Real Watcher

## Mission

Real Watcher answers one question:

> **What is actually here right now?**

It must collect evidence before any cognitive layer tries to explain that evidence.

## v0.0.1 contract

### Command

```bash
watcher scan ./repo
```

### Input

A local directory.

### Output

A deterministic JSON snapshot containing:

- schema version,
- normalized root label,
- file count,
- total bytes,
- sorted file records,
- per-file SHA-256,
- extension histogram,
- snapshot SHA-256.

Absolute machine paths and scan timestamps are intentionally excluded from the canonical payload because they would make identical repository states hash differently.

### Initial exclusions

The scanner ignores implementation noise by default:

- `.git/`
- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.DS_Store`

## Determinism invariant

If the observable repository state does not change, two scans must produce the same canonical JSON and the same `snapshot_sha256`.

If one observed file changes, the snapshot hash must change.

## Boundary

Real Watcher **does not** decide whether a file is important.

It reports:

```text
path + size + type + digest
```

Importance belongs to later stages:

```text
RELATE → UNDERSTAND → DEFINE
```

## Future increments

- compare snapshot A/B,
- classify created/modified/deleted paths,
- emit evidence events,
- optionally inspect Git metadata as a separate evidence source,
- hand graph-ready edges to Diagram / BRAIN.

Those are deliberately outside v0.0.1.
