# MenuTitle: Build Roman Figures
__doc__="""
Builds roman numerals with their unicode.
"""
# Fixed Python Script for Glyphs App (Roman Numerals with Correct Unicode Handling)
import traceback
from GlyphsApp import *
from GlyphsApp.plugins import *

def create_roman_glyphs(font):
    roman_mappings = [
        # Format: (Unicode string, Glyph Name, Components)
        ("2160", "Ⅰ", ["I"]),      # Roman Numeral 1
        ("2164", "Ⅴ", ["V"]),      # Roman Numeral 5
        ("2169", "Ⅹ", ["X"]),      # Roman Numeral 10
        ("216C", "Ⅼ", ["L"]),      # Roman Numeral 50
        ("216D", "Ⅽ", ["C"]),      # Roman Numeral 100
        ("216E", "Ⅾ", ["D"]),      # Roman Numeral 500
        ("216F", "Ⅿ", ["M"]),      # Roman Numeral 1000
        
        # Composites
        ("2161", "Ⅱ", ["I", "I"]),          # Roman Numeral 2
        ("2162", "Ⅲ", ["I", "I", "I"]),     # Roman Numeral 3
        ("2163", "Ⅳ", ["I", "V"]),          # Roman Numeral 4
        ("2165", "Ⅵ", ["V", "I"]),          # Roman Numeral 6
        ("2166", "Ⅶ", ["V", "I", "I"]),     # Roman Numeral 7
        ("2167", "Ⅷ", ["V", "I", "I", "I"]),# Roman Numeral 8
        ("2168", "Ⅸ", ["I", "X"]),          # Roman Numeral 9
        ("216A", "Ⅺ", ["X", "I"]),          # Roman Numeral 11
        ("216B", "Ⅻ", ["X", "I", "I"]),     # Roman Numeral 12
    ]

    for unicode_str, glyph_name, components in roman_mappings:
        try:
            if font.glyphs[glyph_name]:
                print(f"⚠️ Skipping {glyph_name}: Exists.")
                continue

            new_glyph = GSGlyph()
            new_glyph.name = glyph_name
            new_glyph.unicode = unicode_str  # Correct: Assign as string "2160", not integer
            new_glyph.productionName = f"uni{unicode_str}"  # e.g., "uni2160"
            font.glyphs.append(new_glyph)
            print(f"✅ Created {glyph_name} (U+{unicode_str})")

            # Build layers for each master
            for master in font.masters:
                master_id = master.id
                new_layer = GSLayer()
                new_layer.associatedMasterId = master_id
                x_position = 0

                for component_name in components:
                    component_glyph = font.glyphs[component_name]
                    if not component_glyph:
                        print(f"   ⚠️ Missing component: {component_name}")
                        continue

                    component = GSComponent(component_name)
                    component.automaticAlignment = True
                    component.position = (x_position, 0)
                    new_layer.components.append(component)

                    # Update x_position with component width
                    component_layer = component_glyph.layers[master_id]
                    x_position += component_layer.width

                new_layer.width = x_position
                new_glyph.layers[master_id] = new_layer

        except Exception as e:
            print(f"❌ Error in {glyph_name}: {e}")
            traceback.print_exc()

# Run
if __name__ == "__main__":
    font = Glyphs.font
    if font:
        create_roman_glyphs(font)
    else:
        print("⚠️ No font open.")
