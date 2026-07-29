---
okf_version: "0.2"
---

# Bundle index

**Reading order matters in this bundle.** Concepts under `/concepts/critical/` declare `consult: always` — load them before generating any code or advice.

# Critical (always consult)

* [Anti-pattern catalog](/concepts/critical/anti_patterns.md) - central index of documented misconceptions — what agents must NOT generate, each entry linked to its detailed concept.
* [Timer units anti-pattern](/concepts/critical/timer_units.md) - DemoLang timer primitives take SECONDS as float — passing integer milliseconds compiles fine and waits 1000× too long.

# Language knowledge

* [DemoLang language profile](/concepts/language/language_profile.md) - verified capability map of DemoLang — supported, unsupported, and partial features, each claim with evidence.

# Playbooks

* [Incident triage playbook](/concepts/playbooks/incident_triage.md) - systematic reading order for machine incident reports — where to look first, what is normal noise, when alarm text lies.

# Snippets

* [Safe array access](/concepts/snippets/safe_array_access.md) - verified template for bounds-checked array iteration in DemoLang — the pattern agents should copy instead of inventing len().

# Governance

* [GUIDELINES](/GUIDELINES.md) - verification flow and metadata contract (read before contributing).
* [log](/log.md) - append-only change history.
