from PIL import Image
import os

def render_sample_room(tiles_path, water_path, output_path, scale=3):
    tiles = Image.open(tiles_path).convert("RGBA")
    water = Image.open(water_path).convert("RGBA")

    # Repeat water 32x32 over 160x160 area
    w_block = Image.new("RGBA", (160, 160))
    for wy in range(0, 160, 32):
        for wx in range(0, 160, 32):
            w_block.paste(water, (wx, wy))

    canvas = Image.new("RGBA", (160, 160), (20, 24, 30, 255))

    # Helper to get tile from tilesheet (16x16)
    def get_tile(tx, ty):
        return tiles.crop((tx*16, ty*16, tx*16+16, ty*16+16))

    # Sample room layout 10x10 tiles (each 16x16)
    # y=0: Internal wall top (row 9: tx=0)
    # y=1: Wall overhang (row 12: tx=0)
    # y=2: Raised wall (row 5: tx=0)
    # y=3..8: Floor, water pool, deco, doors, bookshelf
    # y=9: Bottom wall

    # Paste water under entire canvas first
    canvas.paste(w_block, (0, 0))

    # Map of tile coords (tx, ty) for each grid cell
    # Floor: (0, 0), Floor deco: (1, 0), Floor SP: (4, 0)
    # Wall top: (0, 9), Wall overhang: (0, 12), Raised wall: (0, 5)
    # Flat wall: (0, 3), Bookshelf: (2, 3), Door: (8, 3)
    # Water stitching: Row 2. Center water has alpha=0 cutout to show water underneath.
    # Region deco: (10, 4)
    # Entrance: (0, 1), Exit: (1, 1)

    grid = [
        # y=0: internal wall top
        [(0, 9)] * 10,
        # y=1: wall overhang
        [(0, 12)] * 10,
        # y=2: raised wall, with a door in the middle (tx=0, ty=7 is raised door)
        [(0, 5), (0, 5), (0, 5), (0, 5), (0, 7), (1, 7), (0, 5), (0, 5), (0, 5), (0, 5)],
        # y=3: floor row with entrance at (1,3), bookshelf at (8,3)
        [(0, 5), (0, 1), (0, 0), (6, 0), (0, 0), (6, 0), (0, 0), (6, 0), (2, 3), (0, 5)],
        # y=4: floor row with deco
        [(0, 5), (0, 0), (1, 0), (0, 0), (7, 0), (0, 0), (1, 0), (0, 0), (0, 0), (0, 5)],
        # y=5: water pool row (water stitching at x=3,4,5)
        [(0, 5), (6, 0), (0, 0), (1, 2), (0, 2), (2, 2), (0, 0), (10, 4), (6, 0), (0, 5)],
        # y=6: water pool row
        [(0, 5), (0, 0), (6, 0), (8, 2), (15, 2), (4, 2), (6, 0), (0, 0), (0, 0), (0, 5)],
        # y=7: floor sp row (special floor / carpet / executive parquet)
        [(0, 5), (4, 0), (4, 0), (10, 0), (10, 0), (4, 0), (4, 0), (0, 0), (1, 1), (0, 5)],
        # y=8: raised wall bottom layer
        [(0, 5), (0, 0), (6, 0), (0, 0), (0, 0), (6, 0), (0, 0), (6, 0), (0, 0), (0, 5)],
        # y=9: bottom wall
        [(0, 5)] * 10,
    ]

    for gy in range(10):
        for gx in range(10):
            tx, ty = grid[gy][gx]
            tile = get_tile(tx, ty)
            canvas.alpha_composite(tile, (gx*16, gy*16))

    scaled = canvas.resize((canvas.width * scale, canvas.height * scale), Image.NEAREST)
    scaled.save(output_path)
    print(f"Saved sample room preview to {output_path}")

if __name__ == "__main__":
    render_sample_room(
        "core/src/main/assets/environment/tiles_sewers.png",
        "core/src/main/assets/environment/water0.png",
        "docs/previews/sector1_vanilla_preview.png"
    )
