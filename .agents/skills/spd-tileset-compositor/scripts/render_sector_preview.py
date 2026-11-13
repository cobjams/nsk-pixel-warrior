#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import os
import subprocess
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageDraw

SECTORS: Dict[int, Dict[str, str]] = {
    1: {
        "name": "Offices",
        "tiles": "core/src/main/assets/environment/tiles_sewers.png",
        "water": "core/src/main/assets/environment/water0.png",
        "mob": "core/src/main/assets/sprites/rat.png",
    },
    2: {
        "name": "Screw Machine Dept",
        "tiles": "core/src/main/assets/environment/tiles_prison.png",
        "water": "core/src/main/assets/environment/water1.png",
        "mob": "core/src/main/assets/sprites/skeleton.png",
    },
    3: {
        "name": "Grind Dept & Ducts",
        "tiles": "core/src/main/assets/environment/tiles_caves.png",
        "water": "core/src/main/assets/environment/water2.png",
        "mob": "core/src/main/assets/sprites/bat.png",
    },
    4: {
        "name": "Heat-Treat Dept",
        "tiles": "core/src/main/assets/environment/tiles_city.png",
        "water": "core/src/main/assets/environment/water3.png",
        "mob": "core/src/main/assets/sprites/monk.png",
    },
    5: {
        "name": "Assembly & R&D Labs",
        "tiles": "core/src/main/assets/environment/tiles_halls.png",
        "water": "core/src/main/assets/environment/water4.png",
        "mob": "core/src/main/assets/sprites/eye.png",
    },
}


def load_image_from_git(ref: str, relpath: str) -> Optional[Image.Image]:
    try:
        raw = subprocess.check_output(
            ["git", "show", f"{ref}:{relpath}"],
            stderr=subprocess.DEVNULL,
        )
        return Image.open(io.BytesIO(raw)).convert("RGBA")
    except Exception:
        return None


def crop_tile(sheet: Image.Image, tx: int, ty: int) -> Image.Image:
    return sheet.crop((tx * 16, ty * 16, tx * 16 + 16, ty * 16 + 16))


def compose_room(
    tiles_img: Image.Image,
    water_img: Image.Image,
    with_sprites: bool = False,
    mob_path: Optional[str] = None,
) -> Image.Image:
    cols, rows = 12, 10
    w, h = cols * 16, rows * 16
    canvas = Image.new("RGBA", (w, h), (16, 18, 22, 255))

    # Base layer: repeating 32x32 liquid texture under the entire room
    for wy in range(0, h, 32):
        for wx in range(0, w, 32):
            canvas.paste(water_img, (wx, wy))

    # 0-based tile coordinates matching DungeonTileSheet.java (16x16 tiles)
    # Row 0: FLOOR=(0,0), FLOOR_DECO=(1,0), FLOOR_SP=(4,0), FLOOR_ALT_1=(6,0), FLOOR_DECO_ALT=(7,0), FLOOR_SP_ALT=(10,0)
    # Row 1: ENTRANCE=(0,1), EXIT=(1,1), WELL=(2,1), PEDESTAL=(4,1), CHASM=(8,1), CHASM_FLOOR=(9,1), CHASM_FLOOR_SP=(10,1), CHASM_WALL=(11,1)
    # Row 2: WATER+1..15 stitching (+1 top, +2 right, +4 bottom, +8 left) -> (tx=mask, ty=2)
    #        top-left pool: +1+8 -> (9,2); top: +1 -> (1,2); top-right: +1+2 -> (3,2)
    #        left: +8 -> (8,2); center: 0 -> (0,2); right: +2 -> (2,2)
    #        bot-left: +4+8 -> (12,2); bot: +4 -> (4,2); bot-right: +2+4 -> (6,2)
    # Row 3: FLAT_WALL=(0,3), FLAT_BOOKSHELF=(2,3), FLAT_DOOR=(8,3), FLAT_DOOR_LOCKED=(10,3), UNLOCKED_EXIT=(12,3)
    # Row 4: FLAT_ALCHEMY_POT=(0,4), FLAT_BARRICADE=(1,4), FLAT_STATUE=(8,4), FLAT_REGION_DECO=(10,4)
    # Row 5: RAISED_WALL=(0,5), RAISED_WALL_DECO=(4,5), RAISED_WALL_DOOR=(8,5), RAISED_WALL_BOOKSHELF=(12,5)
    # Row 7: RAISED_DOOR=(0,7), RAISED_DOOR_OPEN=(1,7), RAISED_DOOR_LOCKED=(2,7), RAISED_OTHER/BARRICADE=(9,7), RAISED_REGION_DECO=(8+10? no: xy(9,8)=>(8,7)+10=(2,8)?)
    # Row 9: WALL_INTERNAL=(0,9) (+1 right, +2 rightBelow, +4 leftBelow, +8 left)
    # Row 12: WALL_OVERHANG=(0,12)
    # Row 14: DOOR_OVERHANG=(0,14), DOOR_OVERHANG_OPEN=(1,14), DOOR_SIDEWAYS=(3,14), DOOR_SIDEWAYS_LOCKED=(4,14)

    base_grid: List[List[Tuple[int, int]]] = [
        # y=0: internal wall tops
        [(0, 9)] * 12,
        # y=1: wall overhang with door overhang at x=5 and locked door overhang at x=8
        [(0, 12), (0, 12), (0, 12), (0, 12), (0, 12), (0, 14), (0, 12), (0, 12), (0, 14), (0, 12), (0, 12), (0, 12)],
        # y=2: raised wall with normal door (x=5), wall deco (x=3), bookshelf (x=7), locked door (x=8)
        [(0, 5), (0, 5), (0, 5), (4, 5), (0, 5), (8, 5), (0, 5), (12, 5), (8, 5), (0, 5), (0, 5), (0, 5)],
        # y=3: upper floor row: entrance (x=1), deco, well (x=9), exit (x=10)
        [(0, 5), (0, 1), (0, 0), (6, 0), (1, 0), (0, 0), (7, 0), (0, 3), (0, 0), (2, 1), (1, 1), (0, 5)],
        # y=4: floor + 3x3 water pool at x=3..5, y=4..6 + flat region deco at x=8
        [(0, 5), (0, 0), (6, 0), (9, 2), (1, 2), (3, 2), (0, 0), (0, 0), (10, 4), (6, 0), (0, 0), (0, 5)],
        # y=5: floor + water pool middle + pedestal at x=8
        [(0, 5), (1, 0), (0, 0), (8, 2), (0, 2), (2, 2), (6, 0), (0, 0), (4, 1), (0, 0), (6, 0), (0, 5)],
        # y=6: floor + water pool bottom + special floor patch at x=7..8
        [(0, 5), (0, 0), (0, 0), (12, 2), (4, 2), (6, 2), (0, 0), (4, 0), (10, 0), (0, 0), (0, 0), (0, 5)],
        # y=7: special floor + barricade + chasm transition at x=9..10
        [(0, 5), (4, 0), (4, 0), (0, 0), (6, 0), (0, 0), (0, 0), (4, 0), (4, 0), (9, 1), (9, 1), (0, 5)],
        # y=8: lower floor + chasm drop-off at x=9..10
        [(0, 5), (0, 0), (1, 0), (0, 0), (0, 0), (8, 4), (0, 0), (0, 0), (0, 0), (8, 1), (8, 1), (0, 5)],
        # y=9: bottom raised wall border
        [(0, 5)] * 12,
    ]

    for gy in range(rows):
        for gx in range(cols):
            tx, ty = base_grid[gy][gx]
            canvas.alpha_composite(crop_tile(tiles_img, tx, ty), (gx * 16, gy * 16))

    # Overlay raised doors on y=2 (x=5 normal closed door, x=8 locked door)
    canvas.alpha_composite(crop_tile(tiles_img, 0, 7), (5 * 16, 2 * 16))
    canvas.alpha_composite(crop_tile(tiles_img, 2, 7), (8 * 16, 2 * 16))
    # Overlay flat bookshelf at (7,3) -> (2,3) and barricade at (2,7) -> (1,4)
    canvas.alpha_composite(crop_tile(tiles_img, 2, 3), (7 * 16, 3 * 16))
    canvas.alpha_composite(crop_tile(tiles_img, 1, 4), (2 * 16, 7 * 16))

    if with_sprites:
        terrain_path = "core/src/main/assets/environment/terrain_features.png"
        if os.path.exists(terrain_path):
            tf = Image.open(terrain_path).convert("RGBA")
            # Sample traps (row 0 col 0, row 2 col 4) and grass/spills (row 7 col 0)
            canvas.alpha_composite(crop_tile(tf, 0, 0), (2 * 16, 4 * 16))
            canvas.alpha_composite(crop_tile(tf, 4, 2), (6 * 16, 6 * 16))
            canvas.alpha_composite(crop_tile(tf, 0, 7), (6 * 16, 4 * 16))

        hero_path = "core/src/main/assets/sprites/warrior.png"
        if os.path.exists(hero_path):
            hero = Image.open(hero_path).convert("RGBA")
            # Janitor tier 1 (Cotton Coveralls) frame 0 -> (0, 15, 12, 30)
            janitor_frame = hero.crop((0, 15, 12, 30))
            canvas.alpha_composite(janitor_frame, (1 * 16 + 2, 5 * 16))

        if mob_path and os.path.exists(mob_path):
            mob = Image.open(mob_path).convert("RGBA")
            # First frame ~16x16 top-left
            mw = min(16, mob.width)
            mh = min(16, mob.height)
            mob_frame = mob.crop((0, 0, mw, mh))
            canvas.alpha_composite(mob_frame, (7 * 16 + (16 - mw) // 2, 5 * 16 + (16 - mh) // 2))

    return canvas


def label_and_scale(img: Image.Image, label: str, scale: int) -> Image.Image:
    scaled = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    header_h = 24
    out = Image.new("RGBA", (scaled.width, scaled.height + header_h), (24, 26, 32, 255))
    out.paste(scaled, (0, header_h))
    draw = ImageDraw.Draw(out)
    draw.text((8, 6), label, fill=(235, 238, 245, 255))
    return out


def render_one(
    sector: Optional[int],
    tiles_path: str,
    water_path: str,
    output_path: str,
    scale: int,
    with_sprites: bool,
    compare_vanilla: bool,
) -> None:
    tiles_img = Image.open(tiles_path).convert("RGBA")
    water_img = Image.open(water_path).convert("RGBA")
    mob_path = SECTORS[sector]["mob"] if sector in SECTORS else None
    sector_label = f"Sector {sector}: {SECTORS[sector]['name']}" if sector in SECTORS else os.path.basename(tiles_path)

    mod_room = compose_room(tiles_img, water_img, with_sprites=with_sprites, mob_path=mob_path)

    if compare_vanilla:
        v_tiles = load_image_from_git("v3.3.8", tiles_path)
        v_water = load_image_from_git("v3.3.8", water_path)
        if v_tiles is not None and v_water is not None:
            van_room = compose_room(v_tiles, v_water, with_sprites=with_sprites, mob_path=mob_path)
            left = label_and_scale(van_room, f"Vanilla v3.3.8 ({os.path.basename(tiles_path)})", scale)
            right = label_and_scale(mod_room, f"Modded ({sector_label})", scale)
            gap = 12
            combined = Image.new("RGBA", (left.width + right.width + gap, max(left.height, right.height)), (15, 17, 21, 255))
            combined.paste(left, (0, 0))
            combined.paste(right, (left.width + gap, 0))
            final_img = combined
        else:
            final_img = label_and_scale(mod_room, f"Modded ({sector_label})", scale)
    else:
        final_img = label_and_scale(mod_room, f"Modded ({sector_label})", scale)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    final_img.save(output_path)
    print(f"Saved preview to {output_path} ({final_img.width}x{final_img.height})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an in-context 12x10 room composite for SPD tilesets.")
    parser.add_argument("--sector", default="1", help="Sector 1..5 or 'all'")
    parser.add_argument("--tiles", help="Custom tilesheet path (overrides --sector)")
    parser.add_argument("--water", help="Custom water texture path (overrides --sector)")
    parser.add_argument("--scale", type=int, default=3, help="Nearest-neighbor upscale factor (default: 3)")
    parser.add_argument("--with-sprites", action="store_true", help="Overlay hero, mob, and terrain_features samples")
    parser.add_argument("--compare-vanilla", action="store_true", help="Render side-by-side vanilla v3.3.8 vs current")
    parser.add_argument("--output", help="Output PNG path")
    args = parser.parse_args()

    if args.tiles and args.water:
        out = args.output or "docs/previews/custom_compositor_preview.png"
        render_one(None, args.tiles, args.water, out, args.scale, args.with_sprites, args.compare_vanilla)
        return 0

    if args.sector == "all":
        for sid, info in SECTORS.items():
            out = f"docs/previews/sector{sid}_compositor_preview.png"
            render_one(sid, info["tiles"], info["water"], out, args.scale, args.with_sprites, args.compare_vanilla)
        return 0

    sid = int(args.sector)
    if sid not in SECTORS:
        raise SystemExit(f"Unknown sector {sid}; expected 1..5 or 'all'")
    info = SECTORS[sid]
    out = args.output or f"docs/previews/sector{sid}_compositor_preview.png"
    render_one(sid, info["tiles"], info["water"], out, args.scale, args.with_sprites, args.compare_vanilla)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
