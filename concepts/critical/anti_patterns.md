---
type: anti-pattern-catalog
title: Anti-pattern catalog
description: Central index of documented misconceptions — what agents must NOT generate, each entry linked to its detailed concept.
status: verified
evidence:
  - "Each linked entry carries its own evidence trail; this catalog only aggregates"
verified_by: kk
last_verified: 2026-07-16
priority: critical
consult: always
tags: [anti-pattern, index, safety]
timestamp: 2026-07-16
---

# Anti-pattern catalog

Negative knowledge is first-class knowledge. Every entry below documents a *plausible but false* assumption about DemoLang, the observed failure, and the verified alternative. Agents: treat these as hard constraints during generation.

| Misconception | Failure class | Detail concept |
|---|---|---|
| Timers accept integer milliseconds | silent 1000× timing error | [timer_units](/concepts/critical/timer_units.md) |
| `len(arr)` exists for array sizing | compile error, or hallucinated loop bounds | [language_profile §unsupported](/concepts/language/language_profile.md) |
| Array indices start at 0 | off-by-one on inclusive-bounds arrays | [safe_array_access](/concepts/snippets/safe_array_access.md) |

## Intake rule

New entries follow [GUIDELINES §3](/GUIDELINES.md): misconception → observed failure (with evidence) → correct alternative. A rejected assumption without a documented alternative is not mergeable.
