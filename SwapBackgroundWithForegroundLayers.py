# MenuTitle: Swap Foreground and Background (Selected Glyphs, Keep Anchors)
# -*- coding: utf-8 -*-

from GlyphsApp import *

font = Glyphs.font
selectedLayers = font.selectedLayers

if not selectedLayers:
    Message("No glyphs selected", "Please select one or more glyphs.")
else:
    font.disableUpdateInterface()

    for layer in selectedLayers:
        glyph = layer.parent

        for master in font.masters:
            fg = glyph.layers[master.id]
            bg = fg.background

            # Copy shapes
            fg_shapes = [s.copy() for s in fg.shapes]
            bg_shapes = [s.copy() for s in bg.shapes]

            # Clear shapes (anchors are NOT part of shapes)
            fg.shapes.clear()
            bg.shapes.clear()

            # Background → Foreground
            for s in bg_shapes:
                fg.shapes.append(s)

            # Foreground → Background
            for s in fg_shapes:
                bg.shapes.append(s)

    font.enableUpdateInterface()
