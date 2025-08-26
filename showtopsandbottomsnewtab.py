# MenuTitle: List Glyphs with deviating tops annd bottoms
__doc__="""
Lists frrom selected glyphs with deviating tops
and bottoms in current master .
"""

import GlyphsApp
from GlyphsApp import *
from collections import defaultdict

def run():
    # Get current font and selected master
    font = Glyphs.font
    if not font:
        print("⚠️ No font open in Glyphs.")
        return
    
    master = font.selectedFontMaster
    if not master:
        print("⚠️ No master selected.")
        return
    
    # Vertical metrics parameters
    metrics = {
        "baseline": 0.0,
        "xHeight": master.xHeight,
        "capHeight": master.capHeight,
        "ascender": master.ascender,
        "descender": master.descender,
        "overshoot": 10.0  # Overshoot tolerance
    }
    
    # Storage for results
    deviations = defaultdict(list)
    values = {}
    
    # Check each selected glyph
    for layer in font.selectedLayers:
        glyph = layer.parent
        if not glyph:
            continue
        
        master_layer = glyph.layers[master.id]
        if not master_layer.bounds:
            continue
            
        # Calculate boundaries
        top = master_layer.bounds.origin.y + master_layer.bounds.size.height
        bottom = master_layer.bounds.origin.y
        
        # Check top metrics
        top_deviates = True
        top_metrics = [metrics["ascender"], metrics["capHeight"], metrics["xHeight"]]
        for m in top_metrics:
            if abs(top - m) <= metrics["overshoot"]:
                top_deviates = False
                break
        
        # Check bottom metrics
        bottom_deviates = True
        bottom_metrics = [metrics["baseline"], metrics["descender"]]
        for m in bottom_metrics:
            if abs(bottom - m) <= metrics["overshoot"]:
                bottom_deviates = False
                break
        
        # Record deviations
        if top_deviates or bottom_deviates:
            dev_info = []
            if top_deviates:
                deviations["Top"].append(glyph.name)
                top_values = ', '.join([f'{m:.1f}' for m in top_metrics])
                dev_info.append(f"Top: {top:.1f} (vs {top_values})")
            if bottom_deviates:
                deviations["Bottom"].append(glyph.name)
                bottom_values = ', '.join([f'{m:.1f}' for m in bottom_metrics])
                dev_info.append(f"Bottom: {bottom:.1f} (vs {bottom_values})")
            
            values[glyph.name] = dev_info
    
    # Print results
    print(f"\n🔍 Vertical Metrics in {master.name}:")
    for k, v in metrics.items():
        print(f"• {k:<10}: {v}")
    
    if not deviations:
        print("\n✅ All selected glyphs match vertical metrics.")
        return
    
    print("\n⚠️ Deviations found:")
    for category, glyphs in deviations.items():
        print(f"\n{category} deviations:")
        for glyph_name in sorted(glyphs):
            for line in values[glyph_name]:
                if category.lower() in line.lower():
                    print(f"{glyph_name}: {line}")
    
    # Open tab with deviating glyphs
    all_deviating = []
    for glyphs in deviations.values():
        all_deviating.extend(glyphs)
    
    if all_deviating:
        tab = font.newTab()
        tab.text = "/" + "/".join(sorted(set(all_deviating)))
        print(f"\n📂 Opened tab with {len(set(all_deviating))} deviating glyphs.")

# Run the script
run()
