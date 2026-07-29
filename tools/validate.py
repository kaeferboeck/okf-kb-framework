#!/usr/bin/env python3
"""Two-verdict validator: OKF v0.2 core conformance + safety-profile compliance.

The two layers are checked and reported SEPARATELY (GUIDELINES §1):
a profile warning is not core nonconformance, and a profile pass never
rescues a core failure. Either layer failing fails the build.

CORE (OKF v0.2, SPEC §4–§5, §8, §12) — errors:
    - missing frontmatter block on a concept document
    - missing/empty `type` (the only always-required key, §4.1)
    - `status` outside draft|stable|deprecated (§5.4)
    - `generated` without `by` (§5.2)
    - `verified` event without `by` or `at` (§5.2)
    - root `index.md` frontmatter carrying keys beside `okf_version` (§8, §12)
  core warnings:
    - legacy `timestamp` key (superseded by `generated.at`, §13.1)
    - legacy `# Citations` body heading (superseded by `sources`, §13.1)

PROFILE (safety profile, GUIDELINES §1) — errors:
    - `verified` claimed without `evidence`  ("no evidence, no merge")
    - `type: anti-pattern` without `evidence` + `verified`
    - `support_status` present but not supported|unsupported|partial,
      or without `evidence` + `verified`
    - `priority: critical` without a `consult` directive
    - pre-v0.2 profile keys (`verified_by`, `last_verified`,
      `status: verified`) — migrate to core `verified: { by, at }`
  profile warnings:
    - newest `verified.at` older than 12 months
    - missing recommended discovery fields (title, description, tags)

Stdlib only — no PyYAML. Line-based frontmatter parsing plus a minimal
inline-mapping reader for `{ by: ..., at: ... }` events (the bare-mapping
form §5.2 explicitly allows; block lists of such mappings also work).

Usage: python3 tools/validate.py <bundle-root>
"""
import re
import sys
from datetime import date, timedelta
from pathlib import Path

EXEMPT = {"README.md", "log.md"}  # index.md is checked, but by §8 rules
CORE_STATUS = {"draft", "stable", "deprecated"}
SUPPORT_STATUS = {"supported", "unsupported", "partial"}
RECOMMENDED = ("title", "description", "tags")
STALE_AFTER = timedelta(days=365)

_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")
_EVENT_RE = re.compile(r"\{\s*(.*?)\s*\}")


def parse_frontmatter(text):
    """Top-level keys -> (raw value, list of indented continuation lines)."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    keys, current = {}, None
    for line in text[4:end].splitlines():
        m = _KEY_RE.match(line)
        if m:
            current = m.group(1)
            keys[current] = (m.group(2).strip(), [])
        elif current and line.startswith((" ", "\t")):
            keys[current][1].append(line.strip())
    return keys, text[end + 4:]


def parse_events(entry):
    """`verified:`/`generated:` value -> list of {by, at} dicts (best effort)."""
    raw, block = entry
    chunks = []
    if raw.startswith("{"):
        chunks.append(raw)
    chunks += [l.lstrip("- ").strip() for l in block if l.lstrip().startswith("-")]
    events = []
    for chunk in chunks:
        m = _EVENT_RE.search(chunk)
        # actor values themselves contain ':' (human:x) — split on by/at only
        events.append(dict(_refield(m.group(1))) if m else {})
    return events


def _refield(inner):
    """Split 'by: human:x, at: 2026-01-01' into [(by, human:x), (at, ...)]."""
    out = []
    for part in inner.split(","):
        part = part.strip()
        m = re.match(r"^(by|at)\s*:\s*(.+)$", part)
        if m:
            out.append((m.group(1), m.group(2).strip()))
    return out


def check_index(path, root, core_err):
    keys, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
    rel = path.relative_to(root)
    if keys is None:
        return  # §8: index without frontmatter is fine
    extra = sorted(set(keys) - {"okf_version"})
    if path.parent == Path(root):
        if extra:
            core_err.append(
                f"{rel}: root index frontmatter may only carry okf_version (§8/§12); found {extra}")
    elif keys:
        core_err.append(f"{rel}: non-root index files contain no frontmatter (§8)")


def main(root):
    core_err, core_warn, prof_err, prof_warn = [], [], [], []
    root_path = Path(root)
    files = [p for p in root_path.rglob("*.md") if ".git" not in p.parts]

    for path in sorted(files):
        rel = path.relative_to(root_path)
        if path.name == "index.md":
            check_index(path, root_path, core_err)
            continue
        if path.name in EXEMPT:
            continue
        keys, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if keys is None:
            core_err.append(f"{rel}: no YAML frontmatter block")
            continue

        raw = {k: v[0] for k, v in keys.items()}

        # ---------------- CORE: OKF v0.2 ----------------
        if not raw.get("type"):
            core_err.append(f"{rel}: missing or empty required field 'type' (§4.1)")
        if "status" in raw and raw["status"] not in CORE_STATUS:
            core_err.append(
                f"{rel}: status '{raw['status']}' is not draft|stable|deprecated (§5.4)")
        if "generated" in keys:
            for ev in parse_events(keys["generated"]):
                if "by" not in ev:
                    core_err.append(f"{rel}: generated without 'by' (§5.2)")
        verified_events = parse_events(keys["verified"]) if "verified" in keys else []
        for ev in verified_events:
            if "by" not in ev or "at" not in ev:
                core_err.append(f"{rel}: verified event without 'by'/'at' (§5.2)")
        if "timestamp" in keys:
            core_warn.append(f"{rel}: legacy 'timestamp' — superseded by generated.at (§13.1)")
        if re.search(r"^#+\s*Citations\s*$", body, re.M):
            core_warn.append(f"{rel}: legacy '# Citations' heading — superseded by sources (§13.1)")

        # ---------------- PROFILE: safety ----------------
        for legacy in ("verified_by", "last_verified"):
            if legacy in keys:
                prof_err.append(
                    f"{rel}: pre-v0.2 key '{legacy}' — migrate to verified: {{ by, at }}")
        if raw.get("status") == "verified":
            prof_err.append(
                f"{rel}: 'status: verified' is the pre-v0.2 contract — "
                f"use core status (§5.4) plus a verified event")
        if verified_events and "evidence" not in keys:
            prof_err.append(f"{rel}: verified is claimed but 'evidence' is missing")
        if raw.get("type") == "anti-pattern":
            for need in ("evidence", "verified"):
                if need not in keys:
                    prof_err.append(f"{rel}: type anti-pattern requires '{need}'")
        if "support_status" in raw:
            if raw["support_status"] not in SUPPORT_STATUS:
                prof_err.append(
                    f"{rel}: support_status '{raw['support_status']}' "
                    f"is not supported|unsupported|partial")
            for need in ("evidence", "verified"):
                if need not in keys:
                    prof_err.append(f"{rel}: support_status requires '{need}'")
        if raw.get("priority") == "critical" and "consult" not in keys:
            prof_err.append(f"{rel}: priority critical without a 'consult' directive")
        for field in RECOMMENDED:
            if field not in keys:
                prof_warn.append(f"{rel}: recommended field '{field}' missing")
        newest = None
        for ev in verified_events:
            try:
                d = date.fromisoformat(ev.get("at", "")[:10])
                newest = d if newest is None or d > newest else newest
            except ValueError:
                core_err.append(f"{rel}: verified.at is not ISO 8601: {ev.get('at')!r}")
        if newest and date.today() - newest > STALE_AFTER:
            prof_warn.append(f"{rel}: newest verified.at {newest} is older than 12 months")

    def report(label, errors, warnings):
        for w in warnings:
            print(f"[{label}] WARN  {w}")
        for e in errors:
            print(f"[{label}] ERROR {e}")
        verdict = "FAIL" if errors else "PASS"
        print(f"[{label}] {verdict} — {len(errors)} error(s), {len(warnings)} warning(s)")
        return verdict

    n = len([p for p in files if p.name not in EXEMPT])
    print(f"{n} files checked\n")
    c = report("core   ", core_err, core_warn)
    p = report("profile", prof_err, prof_warn)
    return 1 if "FAIL" in (c, p) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
