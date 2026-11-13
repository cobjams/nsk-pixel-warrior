---
name: spd-localization-auditor
description: >-
  Use this skill before and after editing any .properties localization file in
  core/src/main/assets/messages/. Validates key parity and Java printf format
  specifiers against vanilla v3.3.8, checks underscore highlight balance, flags
  long UI labels, and reports lingering RPG terminology.
---

# SPD Localization Auditor

Use this skill to catch crash-inducing format-string errors, missing/extra keys, and lingering fantasy RPG terminology across the 9 English `.properties` bundles.

## Quick Usage

Run the strict validation + lore terminology report:

```bash
python3 .agents/skills/spd-localization-auditor/scripts/audit_properties.py --lore-report
```

Audit a single bundle with custom UI name length threshold:

```bash
python3 .agents/skills/spd-localization-auditor/scripts/audit_properties.py \
  --file actors/actors.properties --lore-report --max-name-len 28
```

## Interpreting Output

- **Hard Errors (Exit Code `1`):** Must be fixed immediately.
  - Missing or unexpected extra keys relative to `v3.3.8`
  - Duplicate keys within the same `.properties` file
  - Mismatched Java `String.format` specifiers (`%s`, `%d`, `%1$d`, etc.) or stray unescaped `%`
  - Unbalanced `_highlight_` markers when the baseline key had balanced markers
- **Lore & UI Warnings (Exit Code `0` unless `--strict-lore` is passed):**
  - **Edited-key RPG hits:** Lingering RPG words (`dungeon`, `magic`, `potion`, `scroll`, `wand`, `warrior`, etc.) inside keys you already modified—clean these up first.
  - **Untouched-key RPG hits:** Remaining vanilla strings still awaiting conversion.
  - **Long `.name` / `.title` / `.short_name` values:** Labels exceeding `--max-name-len` (default `28`) that may wrap awkwardly or clip in UI buttons.
