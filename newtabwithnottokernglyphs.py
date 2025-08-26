# MenuTitle: New Tab With Glyphs Not To Be Kerned & Give Them Generous Spacing
"""
Opens a new tab with specified symbol glyphs, removes them from kerning groups,
and sets LSB="=80" and RSB="=|" as string values (not formulas) using NSString to prevent formula parsing.
"""
from GlyphsApp import *
import objc

# List of glyphs to process
glyph_names = [
    "periodcentered.loclCAT",
    "periodcentered.loclCAT.case",
    "paragraph", "section", "copyright", "registered", "published",
    "trademark", "degree", "bar", "brokenbar", "dagger", "daggerdbl",
    "estimated", "numero", "servicemark",
    "florin", "Euro", "bitcoin", "cent", "currency", "dollar",
    "sterling", "yen",
    "logicalnot", "asciicircum", "infinity", "emptyset", "integral",
    "increment", "product", "summation", "radical", "mu", "partialdiff",
    "upArrow", "northEastArrow", "rightArrow", "southEastArrow",
    "downArrow", "southWestArrow", "leftArrow", "northWestArrow",
    "leftRightArrow", "upDownArrow"
]

def process_glyphs(font):
    NSString = objc.lookUpClass("NSString")
    
    # Get existing glyphs
    existing_glyphs = [name for name in glyph_names if font.glyphs[name]]
    
    if not existing_glyphs:
        print("⚠️ None of the specified glyphs exist in the font")
        return
    
    for glyph_name in existing_glyphs:
        glyph = font.glyphs[glyph_name]
        
        # Remove kerning groups
        glyph.leftKerningGroup = None
        glyph.rightKerningGroup = None
        
        for layer in glyph.layers:
            print(f"Initial metrics for {glyph_name} on layer {layer.name}: "
                  f"LSB='{layer.leftMetricsKey}', RSB='{layer.rightMetricsKey}'")
            
            # Clear existing keys and spacing
            layer.leftMetricsKey = None
            layer.rightMetricsKey = None
            layer.LSB = 0
            layer.RSB = 0

            # Use NSString to avoid Glyphs formula parsing
            layer.setValue_forKey_(NSString.stringWithString_("=80"), "leftMetricsKey")
            layer.setValue_forKey_(NSString.stringWithString_("=|"), "rightMetricsKey")

            # Confirm
            if layer.leftMetricsKey != "=80" or layer.rightMetricsKey != "=|":
                print(f"⚠️ Warning: Could not assign exact keys. Got LSB='{layer.leftMetricsKey}', RSB='{layer.rightMetricsKey}'")
            else:
                print(f"✅ Metrics for {glyph_name} on layer {layer.name} set correctly: "
                      f"LSB='{layer.leftMetricsKey}', RSB='{layer.rightMetricsKey}'")
    
    # Open tab
    tab = font.newTab()
    tab.text = "/" + "/".join(existing_glyphs)

    print(f"✅ Processed {len(existing_glyphs)} glyphs:")
    print(", ".join(existing_glyphs))
    print("Set LSB='=80' and RSB='=|' as literal strings for all layers")

# Run if font is open
if Glyphs.font:
    process_glyphs(Glyphs.font)
else:
    print("⚠️ No font open")
