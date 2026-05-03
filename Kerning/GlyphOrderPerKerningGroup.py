# MenuTitle: Set Glyph Order from Kerning Groups (Strict, Bidirectional, No Marks)

from GlyphsApp import Glyphs

font = Glyphs.font
if not font:
    print("No font open")
else:
    master = font.selectedFontMaster

    # key = (leftGroup, rightGroup)
    pairs = {}

    def sort_key(glyph_name):
        g = font.glyphs[glyph_name]
        uni = g.unicode

        if not uni:
            return (5, glyph_name)

        code = int(uni, 16)

        if 0x61 <= code <= 0x7A:
            return (0, code)
        elif 0x41 <= code <= 0x5A:
            return (1, code)
        elif 0x30 <= code <= 0x39:
            return (2, code)
        elif 0x20 <= code <= 0x2F or 0x3A <= code <= 0x40:
            return (3, code)
        else:
            return (4, code)

    # --- Collect glyphs ---
    for g in font.glyphs:
        if not g.export:
            continue

        # Ignore combining/mark glyphs entirely
        if g.category == "Mark":
            continue

        layer = g.layers[master.id]
        if layer is None:
            continue

        if layer.LSB is None or layer.RSB is None:
            continue

        left_group = g.leftKerningGroup
        right_group = g.rightKerningGroup

        # Ignore glyphs missing BOTH groups
        if not left_group and not right_group:
            continue

        key = (left_group, right_group)
        pairs.setdefault(key, []).append(g.name)

    # --- One representative per (left,right) pair ---
    representatives = []

    for key, glyph_list in pairs.items():
        sorted_glyphs = sorted(glyph_list, key=sort_key)
        representatives.append(sorted_glyphs[0])

    # --- Final global order ---
    representatives = sorted(representatives, key=sort_key)

    font.customParameters["glyphOrder"] = representatives

    print("Glyph Order updated with %d entries." % len(representatives))
