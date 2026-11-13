from PIL import Image
import os

def hex_to_rgb(hx):
    hx = hx.lstrip("#")
    return (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16))

def hex_to_rgba(hx, alpha=255):
    r, g, b = hex_to_rgb(hx)
    return (r, g, b, alpha)

# ==============================================================================
# 1. WATER0.PNG (Chemical Runoff / Toxic Sink Overflow)
# ==============================================================================
def convert_water0():
    path = "core/src/main/assets/environment/water0.png"
    im = Image.open(path)
    assert im.mode == "P"
    assert im.size == (32, 32)
    pal = list(im.getpalette())

    # Vibrant Fluorescent Chemical Runoff
    new_colors = {
        2: hex_to_rgb("#163E20"), # deepest caustic shadow
        5: hex_to_rgb("#1E522B"), # shadow ripple
        1: hex_to_rgb("#286E3A"), # body mid
        0: hex_to_rgb("#38944E"), # base chemical green
        3: hex_to_rgb("#4EB868"), # bright chemical swirl
        4: hex_to_rgb("#6CE088"), # fluorescent surface highlight
    }
    for idx, (r, g, b) in new_colors.items():
        pal[idx*3:idx*3+3] = [r, g, b]

    im.putpalette(pal)
    im.save(path)
    print("Saved water0.png (Offices Chemical Runoff)")

# ==============================================================================
# 2. SEWER_BOSS.PNG (Chemical Basin & Industrial Blast Exit)
# ==============================================================================
def convert_sewer_boss():
    path = "core/src/main/assets/environment/custom_tiles/sewer_boss.png"
    im = Image.open(path)
    assert im.mode == "P"
    assert im.size == (256, 32)
    pal = list(im.getpalette())

    # Row 0: Goo Nest (tiles 0..8) - dark chemical basin
    sludge_map = {
        0: hex_to_rgb("#000000"),
        1: hex_to_rgb("#0A1C10"),
        2: hex_to_rgb("#122A18"),
        3: hex_to_rgb("#051208"),
        4: hex_to_rgb("#1A3A22"),
        5: hex_to_rgb("#224A2C"),
        6: hex_to_rgb("#0E2214"),
    }
    for idx, (r, g, b) in sludge_map.items():
        pal[idx*3:idx*3+3] = [r, g, b]

    # Row 1: Exit to Sector 2 (Screw Machine Dept)
    for idx in range(7, 23):
        r, g, b = pal[idx*3:idx*3+3]
        v = (r + g + b) // 3
        if v > 180:
            pal[idx*3:idx*3+3] = [min(255, int(v * 1.1)), min(255, int(v * 0.9)), int(v * 0.25)]
        else:
            pal[idx*3:idx*3+3] = [int(v * 0.82), int(v * 0.90), int(v * 0.98)]

    for idx in [23, 24, 25, 26, 27, 28, 29, 30, 31, 47, 54]:
        r, g, b = pal[idx*3:idx*3+3]
        v = (r + g + b) // 3
        # beige linoleum
        pal[idx*3:idx*3+3] = [int(v * 1.05), int(v * 1.00), int(v * 0.90)]

    im.putpalette(pal)
    im.save(path)
    print("Saved custom_tiles/sewer_boss.png")

# ==============================================================================
# 3. TILES_SEWERS.PNG
# ==============================================================================
def convert_tiles_sewers():
    path = "core/src/main/assets/environment/tiles_sewers.png"
    im = Image.open(path).convert("RGBA")
    w, h = im.size

    # A. Commercial Beige VCT Linoleum (Warm Beige & Cream Beige, NO sage green)
    BEIGE_A_BASE = hex_to_rgba("#C8BFAB")
    BEIGE_A_HI   = hex_to_rgba("#D5CDBC")
    BEIGE_A_SH   = hex_to_rgba("#BCB29C")

    BEIGE_B_BASE = hex_to_rgba("#D6CFBE")
    BEIGE_B_HI   = hex_to_rgba("#E0D9C9")
    BEIGE_B_SH   = hex_to_rgba("#C9C1AE")

    GROUT        = hex_to_rgba("#8C816E")
    GROUT_DK     = hex_to_rgba("#7A705E")

    # B. Executive Boardroom Parquet (Deep Burgundy / Warm Mahogany)
    EXEC_BASE  = hex_to_rgba("#6E433E")
    EXEC_HI    = hex_to_rgba("#8A554E")
    EXEC_SH    = hex_to_rgba("#54332F")
    EXEC_DK    = hex_to_rgba("#3D2422")

    # C. Bland Beige Drywall Walls (NO vertical tile borders)
    WALL_TOP   = hex_to_rgba("#E8E1D5")
    WALL_UPPER = hex_to_rgba("#DFD7C9")
    WALL_MID   = hex_to_rgba("#D5CCBD")
    WALL_LOWER = hex_to_rgba("#C9BFB0")
    WALL_CAP   = hex_to_rgba("#B8AD9C")

    # D. Brown Cove Base (Commercial Rubber Baseboard)
    COVE_HI    = hex_to_rgba("#6E4D38") # top lip bevel
    COVE_BODY  = hex_to_rgba("#4E3524") # main cove base body
    COVE_SH    = hex_to_rgba("#2E1E14") # bottom contact line

    # E. Chemical Runoff Edge (Translucent green)
    CHEM_EDGE1 = hex_to_rgba("#6CE088", 128)
    CHEM_EDGE2 = hex_to_rgba("#4EB868", 128)
    CHEM_EDGE3 = hex_to_rgba("#38944E", 128)
    CHEM_EDGE4 = hex_to_rgba("#286E3A", 128)

    # F. Chemical Drum Palette (Straight-sided steel 55-gal barrel)
    DRUM_STEEL_DK   = hex_to_rgba("#0F1215")
    DRUM_STEEL_BASE = hex_to_rgba("#1F2429")
    DRUM_STEEL_MID  = hex_to_rgba("#374151")
    DRUM_STEEL_HI   = hex_to_rgba("#4B5563")
    DRUM_CHIME_HI   = hex_to_rgba("#CBD5E1")
    DRUM_CHIME_MID  = hex_to_rgba("#94A3B8")
    DRUM_HAZARD_YEL = hex_to_rgba("#F59E0B")
    DRUM_HAZARD_HI  = hex_to_rgba("#FBBF24")
    DRUM_SHADOW     = hex_to_rgba("#7A7060")

    def get_beige_linoleum_pixel(px, py, phase=False):
        # 8x8 checkerboard sub-grid (alternates between Warm Beige A and Cream Beige B)
        is_a = ((px < 8 and py < 8) or (px >= 8 and py >= 8))
        if phase: is_a = not is_a

        # 1px grout seam
        if px in (7, 15) or py in (7, 15):
            return GROUT if (px == 7 or py == 7) else GROUT_DK

        if is_a:
            speckle = (px * 7 + py * 13) % 5
            return BEIGE_A_HI if speckle == 0 else (BEIGE_A_SH if speckle == 4 else BEIGE_A_BASE)
        else:
            speckle = (px * 11 + py * 17) % 5
            return BEIGE_B_HI if speckle == 0 else (BEIGE_B_SH if speckle == 4 else BEIGE_B_BASE)

    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    for y in range(h):
        ty = y // 16
        py = y % 16
        for x in range(w):
            tx = x // 16
            px = x % 16
            r, g, b, a = im.getpixel((x, y))

            if a == 0:
                out.putpixel((x, y), (0, 0, 0, 0))
                continue

            # ==================================================================
            # ROW 0: FLOOR TILES (y = 0..15)
            # ==================================================================
            if ty == 0:
                # 1. Standard / Alt Beige Linoleum (tx = 0, 6, 12)
                if tx in (0, 6, 12):
                    col = get_beige_linoleum_pixel(px, py, phase=(tx == 6))
                    if tx == 12 and px in (3, 4, 5) and py in (10, 11):
                        col = COVE_BODY # faint heel scuff mark
                    out.putpixel((x, y), col)

                # 2. Floor Deco (tx = 1, 7): Beige Linoleum with dropped memo / sticky note
                elif tx in (1, 7):
                    base_col = get_beige_linoleum_pixel(px, py, phase=(tx == 7))
                    col = base_col

                    # Dropped white memo at (px=3..7, py=3..7)
                    if tx == 1 and 3 <= px <= 7 and 3 <= py <= 7:
                        if px in (3, 7) or py in (3, 7):
                            col = hex_to_rgba("#E2E8F0")
                        elif py == 5 and px in (4, 5, 6):
                            col = hex_to_rgba("#64748B")
                        else:
                            col = hex_to_rgba("#FFFFFF")

                    # Yellow sticky note at (px=10..13, py=9..12)
                    elif tx == 1 and 10 <= px <= 13 and 9 <= py <= 12:
                        col = hex_to_rgba("#D97706") if (px == 13 or py == 12) else hex_to_rgba("#FDE047")

                    # Yellow caution tape scrap at (px=4..8, py=8..12)
                    elif tx == 7 and 4 <= px <= 8 and 8 <= py <= 12:
                        col = hex_to_rgba("#1E293B") if (px + py) % 3 == 0 else hex_to_rgba("#EAB308")

                    out.putpixel((x, y), col)

                # 3. Special Floor (tx = 4, 10): Executive Boardroom Parquet
                elif tx in (4, 10):
                    sub_tile = ((px // 4) + (py // 4)) % 2
                    if px % 4 == 0 or py % 4 == 0:
                        out.putpixel((x, y), EXEC_DK)
                    elif sub_tile == 0:
                        col = EXEC_HI if (px % 4 == 1 or py % 4 == 1) else EXEC_BASE
                        out.putpixel((x, y), col)
                    else:
                        col = EXEC_BASE if (px % 4 == 1 or py % 4 == 1) else EXEC_SH
                        out.putpixel((x, y), col)

                # 4. Grass / Overgrowth (tx = 2, 8): Shredded papers & office plant tendrils
                elif tx in (2, 8):
                    if g > r + 10:
                        out.putpixel((x, y), hex_to_rgba("#FFFFFF") if (px + py) % 2 == 0 else hex_to_rgba("#22C55E"))
                    else:
                        out.putpixel((x, y), get_beige_linoleum_pixel(px, py, phase=(tx == 8)))

                # 5. Embers (tx = 3, 9): Chemical scorch on beige linoleum
                elif tx in (3, 9):
                    v = (r + g + b) // 3
                    if v < 80: out.putpixel((x, y), hex_to_rgba("#1C1917"))
                    elif v < 120: out.putpixel((x, y), hex_to_rgba("#44403C"))
                    else: out.putpixel((x, y), hex_to_rgba("#78716C"))

                else:
                    out.putpixel((x, y), (r, g, b, a))

            # ==================================================================
            # ROW 1: ENTRANCE, EXIT, WELLS, PEDESTAL, CHASM (y = 16..31)
            # ==================================================================
            elif ty == 1:
                # Stairwell Entrance / Exit (tx = 0, 1): Industrial concrete stairs with safety yellow tread nosings
                if tx in (0, 1):
                    v = (r + g + b) // 3
                    if v > 140: out.putpixel((x, y), hex_to_rgba("#EAB308"))
                    elif v > 90: out.putpixel((x, y), hex_to_rgba("#64748B"))
                    elif v > 50: out.putpixel((x, y), hex_to_rgba("#334155"))
                    else: out.putpixel((x, y), hex_to_rgba("#0F172A"))

                # Pedestal / Wells (tx = 2, 3, 4): Water cooler / stainless station
                elif tx in (2, 3, 4):
                    v = (r + g + b) // 3
                    if b > r + 10 or (v > 100 and px in (7, 8)):
                        out.putpixel((x, y), hex_to_rgba("#38BDF8"))
                    elif v > 160: out.putpixel((x, y), hex_to_rgba("#F1F5F9"))
                    elif v > 110: out.putpixel((x, y), hex_to_rgba("#94A3B8"))
                    elif v > 60: out.putpixel((x, y), hex_to_rgba("#475569"))
                    else: out.putpixel((x, y), hex_to_rgba("#1E293B"))

                else:
                    out.putpixel((x, y), (r, g, b, a))

            # ==================================================================
            # ROW 2: WATER STITCHING (y = 32..47)
            # ==================================================================
            elif ty == 2:
                if a == 255:
                    # Ground portion: seamless beige linoleum
                    out.putpixel((x, y), get_beige_linoleum_pixel(px, py))
                elif a == 128:
                    # Water edge: fluorescent chemical green edge
                    v = (r + g + b) // 3
                    if v > 140: out.putpixel((x, y), CHEM_EDGE1)
                    elif v > 110: out.putpixel((x, y), CHEM_EDGE2)
                    elif v > 80: out.putpixel((x, y), CHEM_EDGE3)
                    else: out.putpixel((x, y), CHEM_EDGE4)
                else:
                    out.putpixel((x, y), (0, 0, 0, 0))

            # ==================================================================
            # ROW 3: FLAT WALLS, DOORS, BOOKSHELVES (y = 48..63)
            # ==================================================================
            elif ty == 3:
                # Bookshelf (tx = 2, 6): Metal Filing Cabinet with Binders
                if tx in (2, 6):
                    v = (r + g + b) // 3
                    if px in (0, 15) or py in (0, 15) or py == 7:
                        out.putpixel((x, y), hex_to_rgba("#334155") if v > 80 else hex_to_rgba("#1E293B"))
                    elif 2 <= py <= 6:
                        binder_idx = (px - 2) // 3
                        if px % 3 == 0: out.putpixel((x, y), hex_to_rgba("#FFFFFF"))
                        elif binder_idx == 0: out.putpixel((x, y), hex_to_rgba("#EF4444"))
                        elif binder_idx == 1: out.putpixel((x, y), hex_to_rgba("#3B82F6"))
                        elif binder_idx == 2: out.putpixel((x, y), hex_to_rgba("#10B981"))
                        else: out.putpixel((x, y), hex_to_rgba("#F59E0B"))
                    elif 9 <= py <= 13:
                        if px < 8:
                            out.putpixel((x, y), hex_to_rgba("#F8FAFC") if py % 2 == 0 else hex_to_rgba("#CBD5E1"))
                        else:
                            out.putpixel((x, y), hex_to_rgba("#D4A373") if py % 2 == 0 else hex_to_rgba("#B5895B"))
                    else:
                        out.putpixel((x, y), hex_to_rgba("#1E293B"))

                # Doors (tx = 8, 9, 10, 11): Office Door with vision glass pane
                elif tx in (8, 9, 10, 11):
                    if px in (0, 1, 14, 15):
                        out.putpixel((x, y), hex_to_rgba("#1E293B") if px in (0, 15) else hex_to_rgba("#475569"))
                    elif tx == 9:
                        # Open doorway
                        out.putpixel((x, y), get_beige_linoleum_pixel(px, py))
                    else:
                        if 5 <= px <= 10 and 3 <= py <= 7:
                            if px in (5, 10) or py in (3, 7):
                                out.putpixel((x, y), hex_to_rgba("#0F172A"))
                            else:
                                out.putpixel((x, y), hex_to_rgba("#E0F2FE") if py == 4 else hex_to_rgba("#7DD3FC"))
                        elif px in (11, 12) and py in (9, 10):
                            if tx in (10, 11):
                                out.putpixel((x, y), hex_to_rgba("#EF4444") if tx == 10 else hex_to_rgba("#06B6D4"))
                            else:
                                out.putpixel((x, y), hex_to_rgba("#CBD5E1"))
                        elif py >= 13:
                            out.putpixel((x, y), hex_to_rgba("#94A3B8") if py == 13 else hex_to_rgba("#64748B"))
                        else:
                            out.putpixel((x, y), hex_to_rgba("#334155") if (px in (2, 13) or py == 2) else hex_to_rgba("#1E293B"))

                # Flat Bland Beige Drywall (tx = 0, 1, 4, 5) with Brown Cove Base
                else:
                    if py == 13: out.putpixel((x, y), COVE_HI)
                    elif py == 14: out.putpixel((x, y), COVE_BODY)
                    elif py == 15: out.putpixel((x, y), COVE_SH)
                    else:
                        # Smooth horizontal bland beige drywall (NO vertical border)
                        if py == 0: col = WALL_TOP
                        elif py <= 5: col = WALL_UPPER
                        elif py <= 9: col = WALL_MID
                        else: col = WALL_LOWER
                        out.putpixel((x, y), col)

            # ==================================================================
            # ROW 4: FLAT OTHER (y = 64..79)
            # ==================================================================
            elif ty == 4:
                # Chemical Drum (tx = 10): Straight-sided 55-gal steel barrel on beige floor!
                if tx == 10:
                    # Bounding box of drum: px = 3..12, py = 1..14
                    is_drum = False
                    # Top chime & lid: py = 1..2, px = 4..11
                    if py == 1 and 4 <= px <= 11:
                        is_drum = True
                        col = hex_to_rgba("#FFFFFF") if px in (7, 8) else (DRUM_CHIME_HI if px in (5, 6, 9) else DRUM_CHIME_MID)
                    elif py == 2 and 4 <= px <= 11:
                        is_drum = True
                        col = DRUM_STEEL_DK if px in (4, 11) else DRUM_STEEL_BASE
                    # Straight cylindrical body: py = 3..12, px = 3..12
                    elif 3 <= py <= 12 and 3 <= px <= 12:
                        is_drum = True
                        if px in (3, 12):
                            col = DRUM_STEEL_DK # straight vertical outline
                        elif py in (6, 9):
                            # Swedged rolling ring / rib
                            col = DRUM_CHIME_HI if px in (5, 6) else (DRUM_CHIME_MID if px in (4, 7, 8) else DRUM_STEEL_MID)
                        elif py in (7, 10):
                            col = DRUM_STEEL_DK # rib shadow
                        elif 4 <= py <= 5 and 7 <= px <= 8:
                            # Yellow hazard diamond
                            if py == 5 and px == 7:
                                col = DRUM_STEEL_DK # black symbol dot
                            else:
                                col = DRUM_HAZARD_HI if py == 4 else DRUM_HAZARD_YEL
                        else:
                            # Cylindrical lighting
                            col = DRUM_STEEL_HI if px in (5, 6) else (DRUM_STEEL_MID if px in (4, 7) else DRUM_STEEL_BASE)
                    # Bottom chime: py = 13, px = 4..11
                    elif py == 13 and 4 <= px <= 11:
                        is_drum = True
                        col = DRUM_STEEL_HI if px in (5, 6) else (DRUM_STEEL_MID if px in (4, 7, 8) else DRUM_STEEL_DK)
                    # Contact shadow: py = 14, px = 4..11
                    elif py == 14 and 4 <= px <= 11:
                        is_drum = True
                        col = DRUM_SHADOW

                    if is_drum:
                        out.putpixel((x, y), col)
                    else:
                        # Seamless beige linoleum background around the drum!
                        out.putpixel((x, y), get_beige_linoleum_pixel(px, py))

                # Statue (tx = 8, 9): Bronze corporate bust
                elif tx in (8, 9):
                    v = (r + g + b) // 3
                    if v > 160: out.putpixel((x, y), hex_to_rgba("#FDE68A"))
                    elif v > 110: out.putpixel((x, y), hex_to_rgba("#D97706"))
                    elif v > 60: out.putpixel((x, y), hex_to_rgba("#92400E"))
                    else: out.putpixel((x, y), hex_to_rgba("#451A03"))

                # Barricade (tx = 1): Cardboard boxes & desks
                elif tx in (1, 5):
                    v = (r + g + b) // 3
                    if v > 130: out.putpixel((x, y), hex_to_rgba("#D4A373"))
                    elif v > 80: out.putpixel((x, y), hex_to_rgba("#BC6C25"))
                    else: out.putpixel((x, y), hex_to_rgba("#78350F"))

                # Alchemy Pot (tx = 0): Coffee percolator station
                elif tx == 0:
                    v = (r + g + b) // 3
                    if v > 150: out.putpixel((x, y), hex_to_rgba("#F8FAFC"))
                    elif v > 90: out.putpixel((x, y), hex_to_rgba("#94A3B8"))
                    elif v > 50: out.putpixel((x, y), hex_to_rgba("#475569"))
                    else: out.putpixel((x, y), hex_to_rgba("#0F172A"))

                else:
                    out.putpixel((x, y), (r, g, b, a))

            # ==================================================================
            # ROWS 5 & 6: RAISED WALLS (y = 80..111)
            # ==================================================================
            elif ty in (5, 6):
                # Raised bookshelf (tx = 2, 6, 14)
                if tx in (2, 6, 14):
                    v = (r + g + b) // 3
                    if px in (0, 15) or py in (0, 15):
                        out.putpixel((x, y), hex_to_rgba("#334155"))
                    elif 3 <= py <= 6:
                        binder_idx = (px - 2) // 3
                        if px % 3 == 0: out.putpixel((x, y), hex_to_rgba("#FFFFFF"))
                        elif binder_idx == 0: out.putpixel((x, y), hex_to_rgba("#EF4444"))
                        elif binder_idx == 1: out.putpixel((x, y), hex_to_rgba("#3B82F6"))
                        else: out.putpixel((x, y), hex_to_rgba("#10B981"))
                    elif py == 13:
                        out.putpixel((x, y), COVE_HI)
                    elif py == 14:
                        out.putpixel((x, y), COVE_BODY)
                    elif py == 15:
                        out.putpixel((x, y), COVE_SH)
                    else:
                        out.putpixel((x, y), hex_to_rgba("#475569"))
                else:
                    # Bland Beige Drywall with Brown Cove Baseboard (NO vertical borders)
                    if py == 13: out.putpixel((x, y), COVE_HI)
                    elif py == 14: out.putpixel((x, y), COVE_BODY)
                    elif py == 15: out.putpixel((x, y), COVE_SH)
                    else:
                        # Check deco wall features
                        if ty == 5 and tx == 4 and 8 <= py <= 10 and 6 <= px <= 9:
                            # Electrical duplex wall outlet
                            if px in (7, 8) and py in (8, 10):
                                out.putpixel((x, y), hex_to_rgba("#0F172A"))
                            else:
                                out.putpixel((x, y), hex_to_rgba("#FFFFFF"))
                        elif ty == 5 and tx == 5 and 3 <= py <= 7 and 4 <= px <= 11:
                            # HVAC air vent grille
                            out.putpixel((x, y), hex_to_rgba("#0F172A") if py % 2 == 1 else hex_to_rgba("#94A3B8"))
                        elif ty == 5 and tx == 6 and 2 <= py <= 8 and 4 <= px <= 11:
                            # Framed OSHA compliance notice
                            if px in (4, 11) or py in (2, 8):
                                out.putpixel((x, y), hex_to_rgba("#D97706"))
                            else:
                                out.putpixel((x, y), hex_to_rgba("#FFFFFF") if py % 2 == 0 else hex_to_rgba("#64748B"))
                        else:
                            # Completely uniform horizontally across px=0..15 (NO vertical seams/borders)
                            if py == 0: col = WALL_TOP
                            elif py <= 5: col = WALL_UPPER
                            elif py <= 9: col = WALL_MID
                            else: col = WALL_LOWER
                            out.putpixel((x, y), col)

            # ==================================================================
            # ROW 7 & 8: RAISED DOORS & RAISED OTHER (y = 112..143)
            # ==================================================================
            elif ty in (7, 8):
                if ty == 7 and tx in (0, 1, 2, 3, 4):
                    if tx == 1:
                        # Open door threshold: door frame trim on sides + beige linoleum
                        if px in (0, 1):
                            out.putpixel((x, y), hex_to_rgba("#1E293B") if px == 0 else hex_to_rgba("#475569"))
                        elif px in (14, 15):
                            out.putpixel((x, y), hex_to_rgba("#475569") if px == 14 else hex_to_rgba("#1E293B"))
                        else:
                            out.putpixel((x, y), get_beige_linoleum_pixel(px, py))
                    else:
                        # Door panel with vision window
                        if 5 <= px <= 10 and 2 <= py <= 6:
                            out.putpixel((x, y), hex_to_rgba("#E0F2FE") if py == 3 else hex_to_rgba("#7DD3FC"))
                        elif px in (11, 12) and py in (8, 9):
                            out.putpixel((x, y), hex_to_rgba("#CBD5E1"))
                        elif py >= 12:
                            out.putpixel((x, y), hex_to_rgba("#64748B"))
                        else:
                            out.putpixel((x, y), hex_to_rgba("#334155") if (px in (1, 14) or py == 1) else hex_to_rgba("#1E293B"))
                else:
                    v = (r + g + b) // 3
                    if v > 160: out.putpixel((x, y), WALL_TOP)
                    elif v > 110: out.putpixel((x, y), WALL_UPPER)
                    elif v > 60: out.putpixel((x, y), WALL_MID)
                    else: out.putpixel((x, y), WALL_LOWER)

            # ==================================================================
            # ROWS 9..11: INTERNAL WALL TOPS (y = 144..191)
            # ==================================================================
            elif 9 <= ty <= 11:
                v = (r + g + b) // 3
                if v == 0:
                    out.putpixel((x, y), (0, 0, 0, 255))
                elif v > 160:
                    out.putpixel((x, y), WALL_TOP)
                elif v > 100:
                    out.putpixel((x, y), WALL_UPPER)
                elif v > 50:
                    out.putpixel((x, y), WALL_MID)
                else:
                    out.putpixel((x, y), WALL_LOWER)

            # ==================================================================
            # ROWS 12..15: OVERHANGS & UNDERHANGS (y = 192..255)
            # ==================================================================
            else:
                v = (r + g + b) // 3
                if v == 0:
                    out.putpixel((x, y), (0, 0, 0, a))
                elif v > 160:
                    out.putpixel((x, y), hex_to_rgba("#DFD7C9", a))
                elif v > 100:
                    out.putpixel((x, y), hex_to_rgba("#D5CCBD", a))
                elif v > 50:
                    out.putpixel((x, y), hex_to_rgba("#B8AD9C", a))
                else:
                    out.putpixel((x, y), hex_to_rgba("#4E3524", a))

    out.save(path)
    print("Saved environment/tiles_sewers.png with all requested adjustments.")

if __name__ == "__main__":
    convert_water0()
    convert_sewer_boss()
    convert_tiles_sewers()
