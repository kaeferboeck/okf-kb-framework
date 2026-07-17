#!/usr/bin/env python3
"""Frontmatter contract validator (GUIDELINES §1).

Stdlib only — no PyYAML dependency. Parses top-level frontmatter keys
line-based, which is sufficient for the contract checks:

  errors (exit 1):
    - missing frontmatter block
    - missing `type:`  (OKF requirement)
    - missing `status:`
    - `status: verified` without evidence / verified_by / last_verified
  warnings:
    - missing recommended OKF fields (title, description, tags, timestamp)
    - last_verified older than 12 months

Usage: python3 tools/validate.py <bundle-root>
"""
import re
import sys
from datetime import date, timedelta
from pathlib import Path

# index.md and log.md are OKF-reserved files (SPEC §3), not concept documents
EXEMPT = {"README.md", "index.md", "log.md"}
RECOMMENDED = ("title", "description", "tags", "timestamp")
STALE_AFTER = timedelta(days=365)


def frontmatter_keys(text):
    """Return dict of top-level frontmatter keys -> raw value ('' for blocks)."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    keys = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            keys[m.group(1)] = m.group(2).strip()
    return keys


def main(root):
    errors, warnings = [], []
    files = [p for p in Path(root).rglob("*.md")
             if ".git" not in p.parts and p.name not in EXEMPT]
    for path in sorted(files):
        rel = path.relative_to(root)
        keys = frontmatter_keys(path.read_text(encoding="utf-8"))
        if keys is None:
            errors.append(f"{rel}: no YAML frontmatter block")
            continue
        if "type" not in keys:
            errors.append(f"{rel}: missing required field 'type' (OKF)")
        if "status" not in keys:
            errors.append(f"{rel}: missing required field 'status'")
        elif keys["status"] == "verified":
            for field in ("evidence", "verified_by", "last_verified"):
                if field not in keys:
                    errors.append(f"{rel}: status is 'verified' but '{field}' is missing")
        for field in RECOMMENDED:
            if field not in keys:
                warnings.append(f"{rel}: recommended field '{field}' missing")
        if keys.get("last_verified"):
            try:
                verified = date.fromisoformat(keys["last_verified"])
                if date.today() - verified > STALE_AFTER:
                    warnings.append(f"{rel}: last_verified {verified} is older than 12 months")
            except ValueError:
                errors.append(f"{rel}: last_verified is not an ISO date: {keys['last_verified']!r}")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(files)} files checked — {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
