# add code here#MenuTitle: Round Kerning to Multiples of 5
# -*- coding: utf-8 -*-
__doc__ = """
Rounds all kerning values in all masters to the nearest multiple of 5. Skips invalid glyph pairs and optimizes to prevent freezing.
"""

import GlyphsApp
from AppKit import NSApp
import time

font = Glyphs.font  # Current font
round_value = 5

def process_kerning_batch(master, left, right_pairs, batch_size=100):
    """Process kerning pairs in batches with progress feedback."""
    count = 0
    for right, current_value in right_pairs.items():
        # Check if right is a valid glyph or group
        right_glyph = font.glyphForId_(right) if right.startswith("@") or font.glyphs[right] else None
        if not right_glyph and not right.startswith("@"):
            print(f"Skipping invalid right glyph ID: {right} for left: {left}")
            continue
        
        # Only update if the rounded value differs
        new_value = round_value * round(current_value / round_value)
        if new_value != current_value:
            try:
                font.setKerningForPair(master.id, left, right, new_value)
                count += 1
                if count % batch_size == 0:
                    # Force UI update and small delay to prevent freezing
                    NSApp.updateWindows()
                    time.sleep(0.01)  # Brief pause to allow Glyphs to breathe
            except Exception as e:
                print(f"Error setting kerning for pair {left}, {right}: {e}")
    return count

if font is None:
    print("No font open.")
else:
    # Disable UI updates to reduce overhead
    Glyphs.font.disableUpdateInterface()
    try:
        total_updated = 0
        for master in font.masters:
            print(f"Processing master: {master.name}")
            master_kerning = font.kerning.get(master.id, {})
            for left in list(master_kerning.keys()):
                # Check if left is a valid glyph or group
                left_glyph = font.glyphForId_(left) if left.startswith("@") or font.glyphs[left] else None
                if not left_glyph and not left.startswith("@"):
                    print(f"Skipping invalid left glyph ID: {left}")
                    continue
                # Process right-side pairs in batches
                updated = process_kerning_batch(master, left, master_kerning[left])
                total_updated += updated
                if updated > 0:
                    print(f"Updated {updated} pairs for left: {left} in master: {master.name}")
        print(f"Finished: Rounded {total_updated} kerning values to multiples of 5 in all masters.")
    finally:
        # Re-enable UI updates
        Glyphs.font.enableUpdateInterface()