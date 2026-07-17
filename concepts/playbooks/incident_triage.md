---
type: playbook
title: Incident triage playbook
description: Systematic reading order for machine incident reports — where to look first, what is normal noise, when alarm text lies.
status: verified
evidence:
  - "Method distilled from production incident analyses on industrial cells (2026); domain specifics anonymized"
verified_by: kk
last_verified: 2026-07-16
priority: high
tags: [playbook, triage, diagnosis, alarm-vs-rootcause]
timestamp: 2026-07-16
---

# Incident triage playbook

An incident report bundle contains hundreds of files. Without a reading order, analysis burns hours on irrelevant logs — or worse, produces a confident diagnosis from startup noise. This playbook encodes the order and the two hard-won rules.

## Reading order

1. **Project-specific code first.** Most incidents are caused by the newest, least-reviewed layer — customer/project code — not by the platform.
2. **Event log with timestamps second.** Establish the timeline: what changed in the minutes before the failure?
3. **Configuration switches third.** They tell you which features were active — context, rarely cause.
4. **Platform/system code last.** Only descend here once the upper layers are excluded.

## Rule 1: know your noise

Every machine of a given type produces the *same* warnings on every startup (config-overwritten notices, transient link messages). A diagnosis that cites one of these is wrong by default. Maintain a **known-noise list** per machine type; triage strikes those lines *before* interpretation.

## Rule 2: alarm text is a symptom, not a cause

Documented case pattern: an alarm names condition X ("axis not at home position") while the axis demonstrably *is* home — the real cause was a latch held TRUE by a mis-mapped reset event. The alarm system reports the *first visible consequence*, not the origin. Procedure:

1. Find the variable that raises the alarm.
2. Trace what *sets* and what *clears* it — asymmetric set/reset mapping is a classic.
3. Only then interpret the alarm text.

## Comparative triage

When one cell of a fleet fails: diff the incident bundle against a bundle from a healthy sibling cell. Divergence points to the cause faster than any single-bundle analysis (differential triage).
