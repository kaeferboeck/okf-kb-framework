---
type: language-profile
title: DemoLang language profile
description: Verified capability map of DemoLang — supported, unsupported, and partial features, each claim with evidence.
status: stable
generated: { by: human:kaeferboeck, at: 2026-07-16 }
verified: { by: human:kaeferboeck, at: 2026-07-16 }
evidence:
  - "Each row's evidence inline; profile re-verified as a whole against DemoLang 2.4 simulator (2026-07-16)"
priority: high
tags: [language-profile, capabilities, verification]
---

# DemoLang language profile

The capability map answers the question agents get wrong most often: *does this feature exist here?* Every claim is classified and backed. Unknown features default to **unverified — do not generate**.

## Supported (proven working)

| Feature | Evidence | Verified |
|---|---|---|
| `bounds(arr)` → inclusive index range | compiled & ran, simulator 2.4 | 2026-07-16 |
| `wait_t(seconds: float)` blocking wait | reference §4.2 + runtime test | 2026-07-16 |
| String interpolation `"{var}"` | compiled & ran | 2026-07-16 |

## Unsupported (proven absent — do not generate)

| Assumed feature | Observation | Alternative |
|---|---|---|
| `len(arr)` | compile error `Name not defined: len` (2026-07-16) | `bounds(arr)` — see [safe_array_access](/concepts/snippets/safe_array_access.md) |
| `sleep(ms)` | not in reference; compile error | `wait_t(s)` — see [timer_units](/concepts/critical/timer_units.md) |
| exceptions / `try` | parser rejects keyword | status-return pattern |

## Partial (works, edge cases open)

| Feature | Works | Open edge case |
|---|---|---|
| nested arrays | 2 levels compile & run | ≥3 levels: untested — treat as unverified |

## Update rule

A compile error `Name not defined: X` for a plausible name is *itself evidence* — file it under **unsupported** the same day ([GUIDELINES §2.4](/GUIDELINES.md)). The unsupported table is this profile's most valuable section: it is what keeps agents from inventing.
