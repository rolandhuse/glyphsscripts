# MenuTitle: Set Rovas Side Bearings
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from GlyphsApp import Glyphs, Message

__doc__ = """
Sets precise side bearings for all Rovas glyphs according to predefined values.
Handles both direct values (e.g., 50) and references to other glyphs (e.g., "=Cs-rovas").
"""

def set_rovas_sidebearings():
    font = Glyphs.font
    if not font:
        Message("No font open", "Please open a font first.", OKButton=None)
        return
    
    selected_layers = font.selectedLayers
    if not selected_layers:
        Message("No selection", "Please select Rovas glyphs to modify.", OKButton=None)
        return

    # Complete side bearing definitions for all Rovas glyphs
    rovas_sidebearings = {
        # ROVAS CAPITALS
        "A-rovas": (40, "=Cs-rovas"),
        "Aa-rovas": (40, "=Cs-rovas"),
        "B-rovas": (40, 40),
        "C-rovas": (40, 40),
        "Cs-rovas": (140, 140),
        "D-rovas": (60, 60),
        "Dz-rovas": ("=Cs-rovas", "=D-rovas"),
        "Dzs-rovas": ("=Zs-rovas", "=Zs-rovas"),
        "E-rovas": (80, 90),
        "Ee-rovas": (80, 90),
        "F-rovas": (110, 110),
        "G-rovas": ("=S-rovas", "=S-rovas"),
        "Gy-rovas": (60, 60),
        "H-rovas": (120, 120),
        "I-rovas": (60, 60),
        "Ii-rovas": (60, 60),
        "J-rovas": ("=Ii-rovas", "=Cs-rovas"),
        "K-rovas": (40, 40),
        "L-rovas": ("=S-rovas", "=S-rovas"),
        "Ly-rovas": ("=F-rovas", "=F-rovas"),
        "M-rovas": (60, "=Cs-rovas"),
        "N-rovas": (80, "=F-rovas"),
        "NY-rovas": ("=Cs-rovas", "=F-rovas"),
        "O-rovas": (80, "=F-rovas"),
        "Oo-rovas": (65, "=F-rovas"),
        "Oe-rovas": ("=Cs-rovas", "=B-rovas"),
        "Oee-rovas": (60, 50),
        "P-rovas": (120, "=Cs-rovas"),
        "Q-rovas": (135, 135),
        "R-rovas": ("=Cs-rovas", "=Cs-rovas"),
        "S-rovas": (30, 30),
        "Sz-rovas": ("=Cs-rovas+5", "=Cs-rovas+5"),
        "T-rovas": (40, "=Cs-rovas"),
        "Ty-rovas": ("=B-rovas", "=B-rovas"),
        "U-rovas": ("=Cs-rovas", "=Cs-rovas"),
        "Uu-rovas": ("=Cs-rovas", "=Cs-rovas"),
        "Ue-rovas": (130, "=Q-rovas"),
        "Uee-rovas": (60, 50),
        "V-rovas": ("=Cs-rovas", "=Cs-rovas"),
        "W-rovas": ("=Cs-rovas", "=Cs-rovas"),
        "X-rovas": ("=Cs-rovas", "=K-rovas"),
        "Y-rovas": ("=J-rovas", "=I-rovas"),
        "Z-rovas": ("=Cs-rovas", "=Cs-rovas"),
        "Zs-rovas": (40, 40),
        "EClosed-rovas": ("=E-rovas", "=E-rovas"),
        "Ak-rovas": ("=J-rovas", 60),
        
        # ROVAS LOWERCASE
        "a-rovas": (40, "=cs-rovas"),
        "aa-rovas": (40, "=cs-rovas"),
        "b-rovas": (40, 40),
        "c-rovas": (40, 40),
        "cs-rovas": (140, 140),
        "d-rovas": (60, 60),
        "dz-rovas": ("=cs-rovas", "=d-rovas"),
        "dzs-rovas": ("=zs-rovas", "=zs-rovas"),
        "e-rovas": (80, 90),
        "ee-rovas": (80, 90),
        "f-rovas": (110, 110),
        "g-rovas": ("=s-rovas", "=s-rovas"),
        "gy-rovas": (60, 60),
        "h-rovas": (120, 120),
        "i-rovas": (60, 60),
        "ii-rovas": (60, 60),
        "j-rovas": ("=ii-rovas", "=cs-rovas"),
        "k-rovas": (40, 40),
        "l-rovas": ("=s-rovas", "=s-rovas"),
        "ly-rovas": ("=f-rovas", "=f-rovas"),
        "m-rovas": (60, "=cs-rovas"),
        "n-rovas": (80, "=f-rovas"),
        "ny-rovas": ("=cs-rovas", "=f-rovas"),
        "o-rovas": (80, "=f-rovas"),
        "oo-rovas": (65, "=f-rovas"),
        "oe-rovas": ("=cs-rovas", "=b-rovas"),
        "oee-rovas": (60, 50),
        "p-rovas": (120, "=cs-rovas"),
        "q-rovas": (135, 135),
        "r-rovas": ("=cs-rovas", "=cs-rovas"),
        "s-rovas": (30, 30),
        "sz-rovas": ("=cs-rovas+5", "=cs-rovas+5"),
        "t-rovas": (40, "=cs-rovas"),
        "ty-rovas": ("=b-rovas", "=b-rovas"),
        "u-rovas": ("=cs-rovas", "=cs-rovas"),
        "uu-rovas": ("=cs-rovas", "=cs-rovas"),
        "ue-rovas": (130, "=q-rovas"),
        "uee-rovas": (60, 50),
        "v-rovas": ("=cs-rovas", "=cs-rovas"),
        "w-rovas": ("=cs-rovas", "=cs-rovas"),
        "x-rovas": ("=cs-rovas", "=k-rovas"),
        "y-rovas": ("=j-rovas", "=i-rovas"),
        "z-rovas": ("=cs-rovas", "=cs-rovas"),
        "zs-rovas": (40, 40),
        "eClosed-rovas": ("=e-rovas", "=e-rovas"),
        "ak-rovas": ("=j-rovas", 60),
    }

    modified_count = 0

    def resolve_sidebearing_value(value, current_layer):
        """Resolve side bearing values, handling both numbers and references"""
        if isinstance(value, str) and value.startswith("="):
            # Ensure exactly one '=' sign in the reference
            clean_value = "=" + value.lstrip("=")
            return clean_value  # Return the reference string with exactly one '='
        return value  # Return the numeric value

    for layer in font.selectedLayers:
        glyph = layer.parent
        glyph_name = glyph.name
        
        if glyph_name not in rovas_sidebearings:
            print(f"⚠️ Skipping {glyph_name} (not in Rovas definitions)")
            continue
            
        lsb, rsb = rovas_sidebearings[glyph_name]
        
        # Resolve values (handles both numbers and references)
        lsb_value = resolve_sidebearing_value(lsb, layer)
        rsb_value = resolve_sidebearing_value(rsb, layer)
        
        # Apply LSB
        if isinstance(lsb_value, str) and lsb_value.startswith("="):
            glyph.leftMetricsKey = lsb_value  # Set LSB as a reference at the glyph level
            print(f"✅ {glyph_name} [{layer.name}]: LSB={lsb_value} (Reference)")
        else:
            layer.LSB = float(lsb_value) if isinstance(lsb_value, (int, float)) else 0.0
            print(f"✅ {glyph_name} [{layer.name}]: LSB={lsb_value}")

        # Apply RSB
        if isinstance(rsb_value, str) and rsb_value.startswith("="):
            glyph.rightMetricsKey = rsb_value  # Set RSB as a reference at the glyph level
            print(f"✅ {glyph_name} [{layer.name}]: RSB={rsb_value} (Reference)")
        else:
            layer.RSB = float(rsb_value) if isinstance(rsb_value, (int, float)) else 0.0
            print(f"✅ {glyph_name} [{layer.name}]: RSB={rsb_value}")

        # Force Glyphs to update metrics
        layer.syncMetrics()

        # Maintain original shape width (Glyphs will automatically adjust width for referenced side bearings)
        if not (isinstance(rsb_value, str) and rsb_value.startswith("=")) and not (isinstance(lsb_value, str) and lsb_value.startswith("=")):
            layer.width = layer.bounds.size.width + layer.LSB + layer.RSB
        
        modified_count += 1

    Message(
        title="Rovas Metrics Set",
        message=f"Updated side bearings for {modified_count} glyph layers\n"
                f"References resolved: A-rovas→Cs-rovas, a-rovas→cs-rovas",
        OKButton=None
    )

if __name__ == "__main__":
    Glyphs.clearLog()
    print("### Setting Rovas Side Bearings ###\n")
    set_rovas_sidebearings()
    print("\n✅ Done. Check Macro Panel for details.")