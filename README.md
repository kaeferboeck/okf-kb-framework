# okf-kb-framework

**A governance profile on top of [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — built for domains where a wrong answer breaks machines, not just conversations.**

OKF standardizes *how* agents read curated knowledge: markdown files with YAML frontmatter, linked into a knowledge graph. Since v0.2 it also makes provenance, trust, and lifecycle first-class (`sources`, `generated`, `verified`, `status`, `stale_after`). What it deliberately leaves to producers is the domain's **evidence bar**: what has to be true before a claim may call itself verified. In safety-critical domains — industrial automation, robotics, medical tooling — that bar is the whole problem: an agent that confidently repeats an unverified claim generates production-breaking code.

This bundle targets **OKF v0.2** and layers a profile on top, using only §4.1 producer keys. Core fields are used exactly as specified, never redefined. OKF consumers that don't know the profile keys are unaffected.

## What core covers, what the profile adds

| Question | Answered by |
|---|---|
| Who wrote this, and when did it last change? | core `generated` (§5.2) |
| Who confirmed it, and how recently? | core `verified` (§5.2), trust tiers (§5.3) |
| Is it current or deprecated? | core `status` (§5.4), `stale_after` (§5.5) |
| **On what evidence was it confirmed?** | profile `evidence` — required whenever `verified` is claimed. No evidence, no merge. |
| **Was it tested and found false?** | profile `type: anti-pattern` — negative knowledge as a first-class concept, and `support_status: unsupported` for proven-absent capabilities |
| **Must an agent read this before generating?** | profile `priority: critical` + `consult: always` |

The two conventions the profile exists for:

1. **Evidence-based verification.** Core `verified` records *who and when*; the profile requires the *what* — an `evidence` list (tests run, failures reproduced, sources cited) on every concept that claims verification. CI enforces it.
2. **Negative knowledge (anti-patterns).** What does *not* work is a first-class concept type: misconception → observed failure (with evidence) → correct alternative. Documented misconceptions are the single most effective guard against LLM hallucination in niche domains, because models interpolate from mainstream languages into yours. This is deliberately a concept *type*, not a metadata key — consumers should treat anti-patterns as generation constraints, not as trust hints.

## Two layers, two verdicts

`tools/validate.py` reports **core conformance** (is this a valid OKF v0.2 bundle?) and **profile compliance** (does it meet the domain's evidence bar?) as separate verdicts. A profile warning is never core nonconformance; a profile pass never rescues a core failure. Either failing fails the CI build.

```
$ python3 tools/validate.py .
7 files checked

[core   ] PASS — 0 error(s), 0 warning(s)
[profile] PASS — 0 error(s), 0 warning(s)
```

## Origin

This method was developed and battle-tested on a private, production knowledge base for a proprietary industrial robot-programming language (which cannot be published for IP reasons — this repository demonstrates the method on a fictional language, *DemoLang*). It predates the OKF spec and converged on the same core pattern independently; this repo keeps it aligned with the spec as it evolves (v0.1 → v0.2 migration: see [log](/log.md)).

## Structure

```
okf-kb-framework/
├─ index.md                 ← OKF bundle entry point (okf_version: "0.2")
├─ log.md                   ← append-only change history
├─ GUIDELINES.md            ← the governance rules (verification flow, metadata contract)
├─ concepts/
│  ├─ critical/             ← priority: critical — agents read these FIRST
│  ├─ language/             ← language profile: supported / unsupported / partial
│  ├─ playbooks/            ← diagnostic and workflow knowledge
│  └─ snippets/             ← verified code templates with structured headers
└─ tools/
   └─ validate.py           ← CI: two-verdict frontmatter validation (core + profile)
```

## Frontmatter contract (summary)

Core layer (OKF v0.2, used as specified):

| Field | Purpose |
|---|---|
| `type` | required — concept kind; this bundle's vocabulary: `anti-pattern`, `anti-pattern-catalog`, `language-profile`, `playbook`, `snippet`, `governance` |
| `status` | lifecycle: `draft` \| `stable` \| `deprecated` |
| `generated` | `{ by, at }` — authorship and last meaningful change |
| `verified` | `{ by, at }` event(s) — confirmation; trust tiers derive from this |
| `title`, `description`, `tags` | discovery |

Profile layer (producer keys, §4.1):

| Field | Rule |
|---|---|
| `evidence` | required whenever `verified` is claimed — the observations backing the claim |
| `support_status` | for capability claims: `supported` \| `unsupported` \| `partial`; requires evidence + verified |
| `priority`, `consult` | `critical` + `always` → load before generation |

Full rules: [GUIDELINES.md](/GUIDELINES.md). Machine enforcement: `python3 tools/validate.py .`

## Status

v0.2-aligned (2026-07-29) — extracted method, fictional example domain. Licensed under [Apache-2.0](/LICENSE).
