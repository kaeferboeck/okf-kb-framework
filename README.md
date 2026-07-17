# okf-kb-framework

**A governance layer for [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) knowledge bases — built for domains where a wrong answer breaks machines, not just conversations.**

OKF (Google Cloud, v0.1) standardizes *how* agents read curated knowledge: markdown files with YAML frontmatter, linked into a knowledge graph. It deliberately says nothing about *whether the knowledge is true*. In safety-critical domains — industrial automation, robotics, medical tooling — that gap is the whole problem: an agent that confidently repeats an unverified claim generates production-breaking code.

This framework adds three conventions on top of OKF, all fully additive (SPEC §4.1 allows arbitrary frontmatter keys; OKF consumers that don't know them are unaffected):

1. **Evidence-based verification.** Every concept that claims `status: verified` must carry an `evidence` trail (what was tested / observed / cited), `verified_by`, and `last_verified`. No evidence, no merge.
2. **Negative knowledge (anti-patterns).** What does *not* work is a first-class concept type. Documented misconceptions — with the observed failure and the correct alternative — are the single most effective guard against LLM hallucination in niche domains, because models interpolate from mainstream languages into yours.
3. **Consumption priority.** Safety-critical concepts declare `priority: critical` and `consult: always`, so agents load them before generating anything — reading order is not left to chance.

## Origin

This method was developed and battle-tested on a private, production knowledge base for a proprietary industrial robot-programming language (which cannot be published for IP reasons — this repository demonstrates the method on a fictional language, *DemoLang*). It predates the OKF spec and converged on the same core pattern independently; this repo aligns it with OKF conventions.

## Structure

```
okf-kb-framework/
├─ index.md                 ← OKF bundle entry point
├─ log.md                   ← append-only change history
├─ GUIDELINES.md            ← the governance rules (verification flow, metadata contract)
├─ concepts/
│  ├─ critical/             ← priority: critical — agents read these FIRST
│  ├─ language/             ← language profile: supported / unsupported / partial
│  ├─ playbooks/            ← diagnostic and workflow knowledge
│  └─ snippets/             ← verified code templates with structured headers
└─ tools/
   └─ validate.py           ← CI: frontmatter contract enforcement
```

## Frontmatter contract (summary)

| Field | Required | Purpose |
|---|---|---|
| `type` | ✅ (OKF) | concept kind: `rule`, `pattern`, `anti-pattern`, `language-profile`, `playbook`, `snippet` |
| `title`, `description`, `tags`, `timestamp` | recommended (OKF) | discovery & staleness detection |
| `status` | ✅ (this framework) | `draft` \| `verified` \| `disputed` \| `deprecated` |
| `evidence` | if `verified` | list of observations/tests/sources that back the claim |
| `verified_by`, `last_verified` | if `verified` | who confirmed it, and when |
| `support_status` | for capability claims | `supported` \| `unsupported` \| `partial` |
| `priority`, `consult` | for safety-critical | `critical` + `always` → load before generation |

Full rules: [GUIDELINES.md](/GUIDELINES.md). Machine enforcement: `python tools/validate.py .`

## Status

v0.1 — extracted method, fictional example domain. License: Apache-2.0 (planned).
