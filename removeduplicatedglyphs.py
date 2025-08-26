# MenuTitle: Remove Duplicate Unicodes and Glyphs
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from GlyphsApp import Glyphs

def remove_duplicate_unicodes_and_glyphs(font):
    # Dictionary to track assigned unicodes
    unicode_dict = {}
    glyphs_to_remove = set()
    suffixes = (".001", ".002", ".003", ".004", ".005")
    
    # First pass: identify duplicate unicodes and glyphs to remove
    for glyph in font.glyphs:
        # Check for .001, .002 etc. glyphs
        if any(glyph.name.endswith(suffix) for suffix in suffixes):
            base_name = glyph.name.rsplit(".", 1)[0]
            if font.glyphs[base_name]:  # if the base glyph exists
                glyphs_to_remove.add(glyph.name)
                print(f"Marked for removal (duplicate glyph): {glyph.name}")
                continue
        
        # Check for duplicate unicodes (only if glyph has unicodes)
        if glyph.unicodes is not None:
            for unicode in glyph.unicodes:
                if unicode in unicode_dict:
                    print(f"Duplicate Unicode found: {unicode} in {glyph.name} (original in {unicode_dict[unicode]})")
                    glyph.setUnicode_(None)  # remove the duplicate unicode
                    # If this is a duplicate glyph (same name + duplicate unicode), mark for removal
                    if glyph.name == unicode_dict[unicode]:
                        glyphs_to_remove.add(glyph.name)
                else:
                    unicode_dict[unicode] = glyph.name
    
    # Second pass: remove marked glyphs
    if glyphs_to_remove:
        # Sort in reverse to avoid index shifting during deletion
        for glyph_name in sorted(glyphs_to_remove, reverse=True):
            if font.glyphs[glyph_name]:
                del font.glyphs[glyph_name]
                print(f"Removed glyph: {glyph_name}")
    
    return f"Removed {len(glyphs_to_remove)} duplicate glyphs and cleaned duplicate unicodes."

# Run the script
if __name__ == "__main__":
    font = Glyphs.font
    if font:
        result = remove_duplicate_unicodes_and_glyphs(font)
        print(result)
        Glyphs.showNotification(
            "Duplicate Cleanup Complete",
            result,
        )
    else:
        print("No font open in Glyphs.")