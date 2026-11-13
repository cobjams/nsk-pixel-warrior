---
name: spd-tileset-compositor
description: >-
  Use this skill whenever modifying, generating, or reviewing environment
  tilesets (tiles_*.png), liquids (water0..4.png), custom_tiles/*.png, or
  terrain_features.png. Renders in-context 12x10 room composites with walls,
  overhangs, water stitching cutouts, chasms, doors, traps, and sprites.
---

# SPD Tileset Compositor

Use this skill to verify 16x16 environment tilesets in actual room context rather than inspecting flat grids in isolation.

## Quick Usage

Render a sector preview (with sprites & traps overlaid, plus side-by-side vanilla comparison from `v3.3.8`):

```bash
python3 .agents/skills/spd-tileset-compositor/scripts/render_sector_preview.py \
  --sector 1 --with-sprites --compare-vanilla \
  --output docs/previews/sector1_compositor_test.png
```

Render all 5 sectors at once:

```bash
python3 .agents/skills/spd-tileset-compositor/scripts/render_sector_preview.py \
  --sector all --with-sprites --compare-vanilla
```

Preview a custom tilesheet and liquid file directly:

```bash
python3 .agents/skills/spd-tileset-compositor/scripts/render_sector_preview.py \
  --tiles core/src/main/assets/environment/tiles_prison.png \
  --water core/src/main/assets/environment/water1.png \
  --with-sprites --output docs/previews/sector2_preview.png
```

## Visual Verification Checklist

When inspecting the rendered output image:
1. **Wall Top -> Overhang -> Raised Wall Continuity:** Check rows `y=0..2` in the preview. `WALL_INTERNAL` (`row 9` 0-based), `WALL_OVERHANG` (`row 12`), and `RAISED_WALL` (`row 5`) must align seamlessly without stray gaps or mismatched bevels.
2. **Water Stitching Alpha Cutouts:** Check the 3x3 liquid pool in the room center. Row 2 stitching tiles (`WATER+1..15`) must preserve transparent pixels (`alpha=0`) over the liquid interior so `waterN.png` shows cleanly underneath, with crisp edges meeting floor tiles.
3. **Door & Locked Door Alignment:** Check the raised door (`row 7`) and overhang (`row 14`) on the top wall, plus flat doors (`row 3`).
4. **Chasm Drop-Offs:** Check `CHASM_FLOOR` (`(10, 1)` 0-based) and `CHASM` (`(8, 1)` 0-based) at the bottom-right corner.
5. **Figure-Ground Contrast:** With `--with-sprites`, verify the `Janitor` (`warrior.png`), sector mob sprite, and `terrain_features.png` traps/spills stand out clearly against floor tiles without blending into noisy floor textures.
