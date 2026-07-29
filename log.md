# Change log (append-only)

## 2026-07-29
- Migrated the bundle from OKF v0.1 to v0.2: `status: verified` (pre-v0.2 contract) replaced by core `status` (§5.4) plus `verified: { by, at }` events (§5.2); `verified_by`/`last_verified` folded into `verified`; `timestamp` superseded by `generated: { by, at }` (§13.1); root `index.md` frontmatter reduced to `okf_version: "0.2"` (§8). The verification *state* is now derived via trust tiers (§5.3) instead of a profile status value.
- `tools/validate.py` rewritten as a two-verdict validator: core conformance (OKF v0.2) and profile compliance (evidence bar) are checked and reported separately; either failing fails CI.
- Positioning sharpened: this is a governance *profile* over OKF core — core fields are used as specified, never redefined; profile keys are §4.1 producer keys.

## 2026-07-16
- Initial bundle: governance guidelines, anti-pattern catalog + timer-units example, DemoLang language profile, incident triage playbook, safe array access snippet, frontmatter validator.
