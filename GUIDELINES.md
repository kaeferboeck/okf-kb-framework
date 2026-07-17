---
type: governance
title: KB Guidelines — verification & quality
description: The rules that make this bundle trustworthy — metadata contract, verification flow, anti-pattern intake.
status: verified
evidence:
  - "Method proven on a private production KB for a proprietary industrial language (2025–2026); reduced agent-generated defect classes documented there"
verified_by: kk
last_verified: 2026-07-16
tags: [governance, verification, quality]
timestamp: 2026-07-16
---

# KB Guidelines — verification & quality

A knowledge base for AI agents is only as good as its worst confident claim. These rules exist to keep the worst claim honest.

## 1. Metadata contract

Every concept file carries YAML frontmatter with at least `type` (OKF requirement). This framework adds:

| Field | Rule |
|---|---|
| `status` | required: `draft` \| `verified` \| `disputed` \| `deprecated` |
| `evidence` | **required when `status: verified`** — list of concrete observations: test runs, compiler output, source citations, reproduced failures. "It's well known" is not evidence. |
| `verified_by` | required when verified — initials or handle; peer review noted as `author+peer` |
| `last_verified` | required when verified — ISO date of the most recent confirmation |
| `support_status` | for capability claims: `supported` \| `unsupported` \| `partial` |
| `priority` / `consult` | `critical` / `always` for concepts whose omission causes damage |

CI (`tools/validate.py`) enforces this contract — a `verified` concept without evidence fails the build.

## 2. Verification flow

1. **Research:** search the authoritative sources (docs, source code, real system) — establish that the claim is testable.
2. **Minimal test:** build the smallest reproducible case (or cite an existing production occurrence).
3. **Record evidence:** file paths, error messages, log excerpts, dates — enough for a stranger to re-verify.
4. **Classify:** `supported` (proven working), `unsupported` (proven absent/failing — this is valuable, keep it!), `partial` (works with unresolved edge cases, list them).
5. **Index:** add the concept to `index.md`.
6. **Review & merge:** at least one reviewer; no evidence → no merge.

## 3. Negative knowledge (anti-patterns)

When a plausible assumption turns out to be false, it becomes a **concept of `type: anti-pattern`** with three mandatory sections:

| Section | Content |
|---|---|
| Misconception | what a reasonable person (or LLM) assumes |
| Observed failure | what actually happens, with evidence |
| Correct alternative | the verified way, linked to its concept |

Rationale: LLMs interpolate from mainstream knowledge into niche domains. Documenting *what is not there* is the only reliable counterweight — a model told explicitly "DemoLang has no `sleep()`" stops inventing it.

## 4. Staleness

- Safety-critical concepts: re-verify on every related system change.
- Everything else: quarterly review; `last_verified` older than 12 months triggers a CI warning.

## 5. Confidentiality rule

Evidence must never contain customer names, project identifiers, or proprietary source excerpts when the bundle is shared beyond its origin team. Anonymize at intake ("tier-1 automotive project", not the name), not at publication time — retrofitting confidentiality into evidence chains does not work.
