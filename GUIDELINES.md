---
type: governance
title: KB Guidelines — verification & quality
description: The rules that make this bundle trustworthy — metadata contract, verification flow, anti-pattern intake.
status: stable
generated: { by: human:kaeferboeck, at: 2026-07-16 }
verified: { by: human:kaeferboeck, at: 2026-07-16 }
evidence:
  - "Method proven on a private production KB for a proprietary industrial language (2025–2026); reduced agent-generated defect classes documented there"
tags: [governance, verification, quality]
---

# KB Guidelines — verification & quality

A knowledge base for AI agents is only as good as its worst confident claim. These rules exist to keep the worst claim honest.

This bundle targets **OKF v0.2** and layers a domain profile on top of it. The two layers are checked separately (see §1) and never mixed: a profile warning is not OKF nonconformance, and a profile pass never rescues a core failure.

## 1. Metadata contract — two layers, two verdicts

**Core layer (OKF v0.2, SPEC §4–§5).** Used exactly as specified, never redefined:

| Field | Rule (from the spec) |
|---|---|
| `type` | required — the only always-required key. This bundle's vocabulary: `anti-pattern`, `anti-pattern-catalog`, `language-profile`, `playbook`, `snippet`, `governance` |
| `status` | lifecycle: `draft` \| `stable` \| `deprecated` (absent ⇒ `stable`) |
| `generated` | `{ by, at }` — who produced the current content, and when it last meaningfully changed |
| `verified` | `{ by, at }` (or a list of such events) — who confirmed the content. Trust tiers (SPEC §5.3) derive from this: no `verified` ⇒ unverified; non-`human:` actors ⇒ machine-confirmed; a `human:` actor ⇒ human-reviewed |
| `title`, `description`, `tags` | recommended, for discovery |

**Profile layer (this framework, via SPEC §4.1 producer keys).** What the domain adds on top:

| Field | Rule |
|---|---|
| `evidence` | **required whenever `verified` is claimed** — list of concrete observations: test runs, compiler output, source citations, reproduced failures. "It's well known" is not evidence. No evidence, no merge. |
| `support_status` | for capability claims: `supported` \| `unsupported` \| `partial`. Requires `evidence` + `verified` — a capability claim without proof is not mergeable. |
| `priority` / `consult` | `critical` / `always` for concepts whose omission causes damage. `priority: critical` requires an explicit `consult` directive. |

The verification *state* needs no field of its own anymore — it is derivable: a concept without `verified` is unverified (SPEC §5.3) and consumers should treat its claims accordingly. A disputed claim loses its `verified` entry (and gains an anti-pattern or log entry explaining why) rather than carrying a special status value.

CI (`tools/validate.py`) enforces both layers **as separate verdicts** — core conformance and profile compliance are reported independently, and either failing fails the build.

## 2. Verification flow

1. **Research:** search the authoritative sources (docs, source code, real system) — establish that the claim is testable.
2. **Minimal test:** build the smallest reproducible case (or cite an existing production occurrence).
3. **Record evidence:** file paths, error messages, log excerpts, dates — enough for a stranger to re-verify.
4. **Classify:** `supported` (proven working), `unsupported` (proven absent/failing — this is valuable, keep it!), `partial` (works with unresolved edge cases, list them).
5. **Sign:** add a `verified: { by: human:<id>, at: <date> }` event (actor convention, SPEC §7). Content changes without re-confirmation update `generated.at` only — `verified` stays what it was, which is exactly the spec's point in keeping them distinct.
6. **Index:** add the concept to `index.md`.
7. **Review & merge:** at least one reviewer; no evidence → no merge.

## 3. Negative knowledge (anti-patterns)

When a plausible assumption turns out to be false, it becomes a **concept of `type: anti-pattern`** with three mandatory sections:

| Section | Content |
|---|---|
| Misconception | what a reasonable person (or LLM) assumes |
| Observed failure | what actually happens, with evidence |
| Correct alternative | the verified way, linked to its concept |

Rationale: LLMs interpolate from mainstream knowledge into niche domains. Documenting *what is not there* is the only reliable counterweight — a model told explicitly "DemoLang has no `sleep()`" stops inventing it. Note this is deliberately a concept **type**, not a metadata key: a consumer should treat anti-patterns as generation constraints, not as trust hints on some other claim.

## 4. Staleness

- Safety-critical concepts: re-verify on every related system change.
- Everything else: quarterly review; a newest `verified.at` older than 12 months triggers a CI warning (profile layer). Concepts with a hard expiry may additionally declare the core `stale_after` date (SPEC §5.5).

## 5. Confidentiality rule

Evidence must never contain customer names, project identifiers, or proprietary source excerpts when the bundle is shared beyond its origin team. Anonymize at intake ("tier-1 automotive project", not the name), not at publication time — retrofitting confidentiality into evidence chains does not work.
