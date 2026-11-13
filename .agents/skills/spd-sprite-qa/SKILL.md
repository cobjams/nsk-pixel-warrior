---
name: spd-sprite-qa
description: >-
  Use this skill whenever inspecting, editing, or validating character sprite
  sheets (warrior..cleric), mob sheets, items.png, item_icons.png, or UI
  textures. Checks PNG mode ('P' vs 'RGBA'), canvas dimensions, hero die-frame
  invariance, item/icon bounding-box bleed, and renders 4x contact sheets.
---

# SPD Sprite QA

Use this skill alongside **Pixel Workbench** (`init_workspace`, `regression_report`, `inspect_animation`) to enforce strict asset integrity across `core/src/main/assets/`.

## Quick Usage

Validate all assets listed in `docs/texture_reference.json`:

```bash
python3 .agents/skills/spd-sprite-qa/scripts/validate_sprites.py
```

Validate a single asset after editing:

```bash
python3 .agents/skills/spd-sprite-qa/scripts/validate_sprites.py --file sprites/warrior.png
```

Render a `4x` contact sheet for `items.png` (optionally filtered by category) paired with `item_icons.png` overlays:

```bash
python3 .agents/skills/spd-sprite-qa/scripts/validate_sprites.py \
  --render-items docs/previews/items_qa_contact.png --category RINGS
```

## Checks Performed

1. **Format & Dimension Parity:** Ensures every asset in `docs/texture_reference.json` exists on disk and matches its declared `canvas_size` and color `mode` (`P` vs `RGBA`).
2. **Hero Sheet Invariants (`sprites/warrior.png` .. `cleric.png`):**
   - Verifies `256x128` mode `P`.
   - Verifies death/ghost frames `8..12` (`x = 96..155`) are pixel-identical across all 7 armor rows (`y = 0..104`).
   - Checks for stray non-zero palette indices outside the active `x < 252, y < 105` region.
3. **Item & Mini-Icon Frame Bleed (`items.png` & `item_icons.png`):**
   - Checks every `16x16` (`items.png`) and `8x8` (`item_icons.png`) cell to confirm no non-transparent pixels leak outside the declared `(width, height)` bounding box from `ItemSpriteSheet.java`.
4. **4x Contact Sheet & Icon Pairing (`--render-items`):**
   - Draws `items.png` cells at `4x` with bounding-box outlines and composites `7x7` `item_icons.png` badges onto the top-right corner of sample Ring, Scroll, and Potion sprites to verify readability in inventory slots.
