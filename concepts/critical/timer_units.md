---
type: anti-pattern
title: "Anti-pattern: integer milliseconds passed to timers"
description: DemoLang timer primitives take SECONDS as float — passing integer milliseconds compiles fine and waits 1000× too long.
status: verified
evidence:
  - "wait_t(500) observed to block a demo cell for ~8.3 minutes instead of 0.5 s (reproduced 2026-07-16, DemoLang 2.4 simulator)"
  - "DemoLang reference §4.2: 'duration: FLOAT, unit seconds'"
verified_by: kk
last_verified: 2026-07-16
support_status: unsupported
priority: critical
consult: always
tags: [anti-pattern, timer, units, safety]
timestamp: 2026-07-16
---

# Anti-pattern: integer milliseconds passed to timers

## Misconception

Developers (and LLMs trained on mainstream APIs where `sleep(500)` means milliseconds) assume DemoLang timer calls take milliseconds:

```demolang
wait_t(500)        // WRONG: waits 500 seconds, not 0.5
```

The call **compiles without warning** — the failure is silent and only appears at runtime as a machine that seems to hang.

## Observed failure

A `wait_t(500)` in a handling sequence blocked the demo cell for over 8 minutes. No error, no log entry — the timer did exactly what it was told.

## Correct alternative

Timer durations are **seconds as float**, always written with a decimal point and a unit comment:

```demolang
wait_t(0.5)        // 0.5 s gripper settle time
```

Never derive durations by multiplying with 1000. If a value comes from an HMI field in milliseconds, convert at the boundary and name the variable with its unit (`settle_time_s`).
