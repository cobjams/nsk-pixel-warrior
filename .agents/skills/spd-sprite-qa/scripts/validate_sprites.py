#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw

ASSETS_ROOT = "core/src/main/assets"
TEX_REF_PATH = "docs/texture_reference.json"


def check_asset_header(relpath: str, expected_size: List[int], expected_mode: str) -> Tuple[Optional[Image.Image], List[str]]:
    full_path = os.path.join(ASSETS_ROOT, relpath)
    errs: List[str] = []
    if not os.path.exists(full_path):
        return None, [f"MISSING FILE: {full_path}"]
    im = Image.open(full_path)
    if list(im.size) != list(expected_size):
        errs.append(f"SIZE MISMATCH in {relpath}: got {list(im.size)}, expected {list(expected_size)}")
    if im.mode != expected_mode:
        errs.append(f"MODE MISMATCH in {relpath}: got '{im.mode}', expected '{expected_mode}'")
    return im, errs


def validate_hero_sheet(relpath: str, im: Image.Image) -> List[str]:
    errs: List[str] = []
    if im.mode != "P" or im.size != (256, 128):
        return errs

    # Ghost/die frames: frames 8..12 => x = 96..155, row 0 y=0..14 vs rows 1..6 y=r*15..r*15+14
    px = im.load()
    row0_ghost = [[px[x, y] for x in range(96, 156)] for y in range(0, 15)]
    for tier in range(1, 7):
        y0 = tier * 15
        diff_count = 0
        for dy in range(15):
            for dx in range(60):
                if px[96 + dx, y0 + dy] != row0_ghost[dy][dx]:
                    diff_count += 1
        if diff_count > 0:
            errs.append(
                f"HERO DIE-FRAME DRIFT in {relpath}: tier {tier} differs from tier 0 in {diff_count} pixel(s) within x=96..155"
            )

    # Check stray non-zero pixels outside active 21*12=252 x 7*15=105 region
    stray = 0
    for y in range(128):
        for x in range(256):
            if (x >= 252 or y >= 105) and px[x, y] != 0:
                stray += 1
    if stray > 0:
        errs.append(f"HERO STRAY PIXELS in {relpath}: {stray} non-zero pixel(s) outside 252x105 active sheet")
    return errs


def is_pixel_opaque(im: Image.Image, px: Any, x: int, y: int) -> bool:
    val = px[x, y]
    if im.mode == "P":
        return val != 0
    if isinstance(val, tuple):
        return len(val) >= 4 and val[3] > 0
    return val != 0


def audit_cell_bleed(
    im: Image.Image,
    entries: List[Dict[str, Any]],
    cell_size: int,
    label: str,
) -> List[str]:
    errs: List[str] = []
    px = im.load()
    for ent in entries:
        x0 = int(ent["pixel_x"])
        y0 = int(ent["pixel_y"])
        bw = int(ent["width"])
        bh = int(ent["height"])
        bleed_pixels = 0
        for dy in range(cell_size):
            for dx in range(cell_size):
                if dx >= bw or dy >= bh:
                    if x0 + dx < im.width and y0 + dy < im.height:
                        if is_pixel_opaque(im, px, x0 + dx, y0 + dy):
                            bleed_pixels += 1
        if bleed_pixels > 0:
            errs.append(
                f"FRAME BLEED in {label} [{ent['name']} @ ({x0},{y0}) box {bw}x{bh}]: "
                f"{bleed_pixels} opaque pixel(s) outside declared bounding box"
            )
    return errs


def render_items_contact_sheet(
    items_im: Image.Image,
    icons_im: Image.Image,
    tex_ref: Dict[str, Any],
    output_path: str,
    category: Optional[str],
    scale: int = 4,
) -> None:
    sprites = tex_ref["items"]["sprites"]
    icons = tex_ref["items"]["item_icons"]["icons"]

    if category:
        cat_upper = category.upper()
        sprites = [s for s in sprites if s["category"].upper() == cat_upper]
        icons_filtered = [ic for ic in icons if ic["category"].upper() == cat_upper]
    else:
        icons_filtered = icons

    cols = 16
    cell_px = 16 * scale
    pad = 4
    step = cell_px + pad

    sprite_rows = max(1, (len(sprites) + cols - 1) // cols)
    # Also include an icon pairing strip at the bottom
    icon_rows = max(1, (len(icons_filtered) + cols - 1) // cols) if icons_filtered else 0

    header_h = 24
    pair_header_h = 26 if icons_filtered else 0
    total_w = cols * step + pad
    total_h = header_h + sprite_rows * step + pair_header_h + icon_rows * step + pad

    canvas = Image.new("RGBA", (total_w, total_h), (24, 27, 34, 255))
    draw = ImageDraw.Draw(canvas)
    title = f"items.png QA ({category.upper() if category else 'ALL'}, {len(sprites)} items)"
    draw.text((8, 6), title, fill=(230, 235, 245, 255))

    items_rgba = items_im.convert("RGBA")
    icons_rgba = icons_im.convert("RGBA")

    for idx, ent in enumerate(sprites):
        gx = idx % cols
        gy = idx // cols
        dx = pad + gx * step
        dy = header_h + gy * step
        draw.rectangle([dx, dy, dx + cell_px - 1, dy + cell_px - 1], fill=(38, 42, 52, 255))
        tile = items_rgba.crop((ent["pixel_x"], ent["pixel_y"], ent["pixel_x"] + 16, ent["pixel_y"] + 16))
        tile_scaled = tile.resize((cell_px, cell_px), Image.NEAREST)
        canvas.alpha_composite(tile_scaled, (dx, dy))
        bw = ent["width"] * scale
        bh = ent["height"] * scale
        draw.rectangle([dx, dy, dx + bw - 1, dy + bh - 1], outline=(90, 200, 140, 140))

    if icons_filtered:
        y_pair = header_h + sprite_rows * step
        draw.text((8, y_pair + 6), f"item_icons.png pairing ({len(icons_filtered)} icons on base item)", fill=(230, 235, 245, 255))
        y_icons = y_pair + pair_header_h

        # Find representative 16x16 base sprites for RING, SCROLL, POTION
        all_sprites = tex_ref["items"]["sprites"]
        bases = {
            "RINGS": next((s for s in all_sprites if s["category"] == "RINGS"), None),
            "SCROLLS": next((s for s in all_sprites if s["category"] == "SCROLLS"), None),
            "POTIONS": next((s for s in all_sprites if s["category"] == "POTIONS"), None),
        }

        for idx, ic in enumerate(icons_filtered):
            gx = idx % cols
            gy = idx // cols
            dx = pad + gx * step
            dy = y_icons + gy * step
            draw.rectangle([dx, dy, dx + cell_px - 1, dy + cell_px - 1], fill=(38, 42, 52, 255))

            base = bases.get(ic["category"])
            comp = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
            if base:
                base_tile = items_rgba.crop((base["pixel_x"], base["pixel_y"], base["pixel_x"] + 16, base["pixel_y"] + 16))
                comp.alpha_composite(base_tile, (0, 0))
            ic_tile = icons_rgba.crop((ic["pixel_x"], ic["pixel_y"], ic["pixel_x"] + ic["width"], ic["pixel_y"] + ic["height"]))
            # SPD renders item_icons at top-right corner of the 16x16 slot
            comp.alpha_composite(ic_tile, (16 - ic["width"], 0))
            canvas.alpha_composite(comp.resize((cell_px, cell_px), Image.NEAREST), (dx, dy))

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    canvas.save(output_path)
    print(f"Saved items QA contact sheet to {output_path} ({canvas.width}x{canvas.height})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SPD sprite sheets against docs/texture_reference.json.")
    parser.add_argument("--file", help="Validate only a single asset path relative to core/src/main/assets/")
    parser.add_argument("--render-items", help="Output path for 4x items + item_icons contact sheet PNG")
    parser.add_argument("--category", help="Optional category filter for --render-items (e.g. RINGS, POTIONS, SCROLLS)")
    parser.add_argument("--fail-on-bleed", action="store_true", help="Exit non-zero if any item/icon bounding-box bleed occurs")
    args = parser.parse_args()

    with open(TEX_REF_PATH, "r", encoding="utf-8") as f:
        tex_ref = json.load(f)

    if args.render_items:
        items_im = Image.open(os.path.join(ASSETS_ROOT, tex_ref["items"]["file"]))
        icons_im = Image.open(os.path.join(ASSETS_ROOT, tex_ref["items"]["item_icons"]["file"]))
        render_items_contact_sheet(items_im, icons_im, tex_ref, args.render_items, args.category)
        return 0

    hard_errors: List[str] = []
    bleed_warnings: List[str] = []
    checked = 0

    def should_check(rel: str) -> bool:
        return args.file is None or args.file == rel

    # 1. Hero sheets + avatars
    hero_cfg = tex_ref["heroes"]
    for cls in hero_cfg["classes"]:
        rel = cls["file"]
        if not should_check(rel):
            continue
        checked += 1
        im, errs = check_asset_header(rel, hero_cfg["canvas_size"], hero_cfg["mode"])
        hard_errors.extend(errs)
        if im is not None:
            hard_errors.extend(validate_hero_sheet(rel, im))

    av = hero_cfg.get("avatars")
    if av and should_check(av["file"]):
        checked += 1
        _, errs = check_asset_header(av["file"], av["canvas_size"], av["mode"])
        hard_errors.extend(errs)

    # 2. Mob/NPC sprites
    for _name, spec in sorted(tex_ref["sprites"].items()):
        rel = spec["file"]
        if not should_check(rel):
            continue
        checked += 1
        _, errs = check_asset_header(rel, spec["canvas_size"], spec["mode"])
        hard_errors.extend(errs)

    # 3. Items & item_icons
    items_cfg = tex_ref["items"]
    if should_check(items_cfg["file"]):
        checked += 1
        im, errs = check_asset_header(items_cfg["file"], items_cfg["canvas_size"], items_cfg["mode"])
        hard_errors.extend(errs)
        if im is not None:
            bleed_warnings.extend(audit_cell_bleed(im, items_cfg["sprites"], 16, items_cfg["file"]))

    icons_cfg = items_cfg["item_icons"]
    if should_check(icons_cfg["file"]):
        checked += 1
        im, errs = check_asset_header(icons_cfg["file"], icons_cfg["canvas_size"], icons_cfg["mode"])
        hard_errors.extend(errs)
        if im is not None:
            bleed_warnings.extend(audit_cell_bleed(im, icons_cfg["icons"], 8, icons_cfg["file"]))

    # 4. Environments
    tf_cfg = tex_ref["environments"]["terrain_features"]
    if should_check(tf_cfg["file"]):
        checked += 1
        _, errs = check_asset_header(tf_cfg["file"], tf_cfg["canvas_size"], tf_cfg["mode"])
        hard_errors.extend(errs)

    # 5. Interfaces & Effects
    for group_name in ("interfaces", "effects"):
        for entry in tex_ref.get(group_name, []):
            rel = entry["file"]
            if not should_check(rel):
                continue
            checked += 1
            _, errs = check_asset_header(rel, entry["canvas_size"], entry["mode"])
            hard_errors.extend(errs)

    print(f"Checked {checked} asset(s): {len(hard_errors)} hard error(s), {len(bleed_warnings)} bleed warning(s).")
    for e in hard_errors:
        print(f"  ERROR: {e}")
    for w in bleed_warnings[:20]:
        print(f"  WARN:  {w}")
    if len(bleed_warnings) > 20:
        print(f"  ... ({len(bleed_warnings) - 20} more bleed warning(s))")

    if hard_errors:
        return 1
    if args.fail_on_bleed and bleed_warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
