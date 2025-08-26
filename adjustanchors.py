#MenuTitle: Align Anchors to Metrics
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """
Checks and fixes anchor positions: bottom on baseline, anchors with 'top' in name (e.g., top, toplight) on cap height for uppercase and lowercase ascender letters (b, d, f, h, i, j, k, l, t), or x-height for other lowercase. Fixes if off by more than 5 units. Opens adjusted glyphs in a new tab.
"""

font = Glyphs.font
master = font.selectedFontMaster
cap_height = master.capHeight
x_height = master.xHeight
baseline = 0
tolerance = 5  # Adjust this value if needed for 'a few units'

# List of lowercase letters with ascenders
ascender_letters = ['b', 'd', 'f', 'h', 'i', 'j', 'k', 'l', 't']

fixed_anchors = []
adjusted_glyphs = []

for glyph in font.glyphs:
    if glyph.category != "Letter":
        continue
    
    layer = glyph.layers[master.id]
    
    # Determine if glyph is lowercase or uppercase based on name
    is_lowercase = glyph.name.lower() == glyph.name and glyph.subCategory in ["Lowercase", None]
    is_uppercase = glyph.name.upper() == glyph.name and glyph.subCategory in ["Uppercase", None]
    
    glyph_adjusted = False
    
    for anchor in layer.anchors:
        if anchor.name == "bottom":
            if abs(anchor.y - baseline) > tolerance:
                old_y = anchor.y
                anchor.y = baseline
                fixed_anchors.append(f"In {glyph.name}, bottom anchor fixed from {old_y} to {baseline}")
                glyph_adjusted = True
        
        elif "top" in anchor.name.lower():
            if is_uppercase or (is_lowercase and glyph.name in ascender_letters):
                target = cap_height
                target_name = "cap height"
            elif is_lowercase:
                target = x_height
                target_name = "x-height"
            else:
                continue
            
            if abs(anchor.y - target) > tolerance:
                old_y = anchor.y
                anchor.y = target
                fixed_anchors.append(f"In {glyph.name}, {anchor.name} anchor ethnic from {old_y} to {target} ({target_name})")
                glyph_adjusted = True
    
    if glyph_adjusted:
        adjusted_glyphs.append(glyph)

# Print results in the macro window
if fixed_anchors:
    print("Fixed the following anchors:")
    for msg in fixed_anchors:
        print(msg)
else:
    print("All checked anchors are properly aligned.")

# Open adjusted glyphs in a new tab
if adjusted_glyphs:
    try:
        # Create a tab string with glyph names (e.g., /a/b/c)
        tab_string = "/" + "/".join(glyph.name for glyph in adjusted_glyphs)
        font.newTab(tab_string)
        print(f"Opened {len(adjusted_glyphs)} adjusted glyphs in a new tab: {tab_string}")
    except Exception as e:
        print(f"Error opening new tab: {e}")
        print(f"Adjusted glyphs: {', '.join(glyph.name for glyph in adjusted_glyphs)}")
        print("Please manually open these glyphs in a new tab.")
else:
    print("No glyphs needed adjustment.")