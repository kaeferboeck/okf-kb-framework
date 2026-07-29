---
type: snippet
title: "Snippet: safe array access"
description: Verified template for bounds-checked array iteration in DemoLang — the pattern agents should copy instead of inventing len().
status: stable
generated: { by: human:kaeferboeck, at: 2026-07-16 }
verified: { by: human:kaeferboeck, at: 2026-07-16 }
evidence:
  - "Template compiled & ran on DemoLang 2.4 simulator (2026-07-16), including empty-array edge case"
tags: [snippet, array, bounds, template]
---

# Snippet: safe array access

Structured header travels *inside* the code block so the snippet stays self-describing when copied out of the bundle:

```demolang
// @snippet-id: safe_array_access
// @title: Bounds-checked array iteration
// @purpose: prevents out-of-bounds and hallucinated len()
// @last-verified: 2026-07-16
// @related: language_profile, anti_patterns

range := bounds(items)              // inclusive [low, high]
if range.low > range.high then      // empty array: low > high by contract
    return
end
for i := range.low to range.high do
    process(items[i])
end
```

## Why this shape

- `bounds()` is the **only** verified sizing primitive ([language profile](/concepts/language/language_profile.md)); `len()` does not exist.
- Indices are **inclusive on both ends** and do not necessarily start at 0 — deriving `high` as `count - 1` is the documented off-by-one source ([anti-pattern catalog](/concepts/critical/anti_patterns.md)).
- The empty-array contract (`low > high`) must be checked before the loop; the runtime does not.
