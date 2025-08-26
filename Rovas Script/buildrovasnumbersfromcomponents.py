# MenuTitle: Build Rovas Numerals 2-9 with Components and ss01
__doc__ = """
Creates Old Hungarian numerals 2–4 and 6–9 using components and properly adds ss01 feature.
Creates a dedicated lookup for Rovas numerals in the ss01 feature.
"""

from GlyphsApp import *

# Config
PUA_START = 0xE100  # PUA codepoints start
COMPONENT_SCALE = 0.9
X_OVERLAP = 0.2

# Composite numerals (excluding already defined base numerals)
composite_numerals = [
    ("two.rovas", ["one-rovas", "one-rovas"]),
    ("three.rovas", ["one-rovas"] * 3),
    ("four.rovas", ["one-rovas"] * 4),
    ("six.rovas", ["five-rovas", "one-rovas"]),
    ("seven.rovas", ["five-rovas", "one-rovas", "one-rovas"]),
    ("eight.rovas", ["five-rovas", "one-rovas", "one-rovas", "one-rovas"]),
    ("nine.rovas", ["five-rovas", "one-rovas", "one-rovas", "one-rovas", "one-rovas"]),
]

def create_composite_numerals(font):
    created = []
    for index, (glyph_name, components) in enumerate(composite_numerals):
        if glyph_name in font.glyphs:
            print(f"⚠️ {glyph_name} already exists, skipping.")
            continue

        g = GSGlyph(glyph_name)
        g.unicode = f"{PUA_START + index:X}"
        g.category = "Number"
        g.subCategory = "Decimal Digit"
        g.script = "Rovas"
        g.storeCategory = False
        g.storeSubCategory = False
        g.storeScript = False
        
        # Add ss01 feature tag to glyph (correct property name is 'tags')
        g.tags = ["ss01"]
        font.glyphs.append(g)

        for master in font.masters:
            layer = GSLayer()
            layer.associatedMasterId = master.id
            g.layers[master.id] = layer

            x_pos = 0
            for comp_name in components:
                if comp_name not in font.glyphs:
                    print(f"❌ Missing component glyph: {comp_name}")
                    continue
                comp = GSComponent(font.glyphs[comp_name])
                comp.scale = (COMPONENT_SCALE, COMPONENT_SCALE)
                comp.position = (x_pos, 0)
                layer.components.append(comp)
                width = font.glyphs[comp_name].layers[master.id].width
                if not width:  # Handle case where width might be None
                    width = 300
                x_pos += width * COMPONENT_SCALE * (1 - X_OVERLAP)

            layer.width = x_pos

        g.updateGlyphInfo()
        created.append(glyph_name)
        print(f"✅ Created {glyph_name}")

    return created

def ensure_ss01_feature(font, created_numerals):
    # Create the lookup first
    lookup_name = "ROVAS_NUMERALS"
    substitutions = [
        "sub two by two.rovas;",
        "sub three by three.rovas;",
        "sub four by four.rovas;",
        "sub six by six.rovas;",
        "sub seven by seven.rovas;",
        "sub eight by eight.rovas;",
        "sub nine by nine.rovas;"
    ]
    
    # Add any additional substitutions for newly created numerals
    for gname in created_numerals:
        base = gname.replace(".rovas", "")
        substitutions.append(f"sub {base} by {gname};")

    lookup_code = f"lookup {lookup_name} {{\n    " + "\n    ".join(substitutions) + f"\n}} {lookup_name};"

    # Check if feature already exists
    ss01_feature = next((f for f in font.features if f.name == "ss01"), None)
    
    if not ss01_feature:
        # Create new ss01 feature with the lookup
        ss01_feature = GSFeature()
        ss01_feature.name = "ss01"
        ss01_feature.code = f"{lookup_code}\n\nfeature ss01 {{\n    lookup {lookup_name};\n}} ss01;"
        font.features.append(ss01_feature)
        print("✅ Created ss01 feature with Rovas numerals lookup")
    else:
        # Check if lookup exists in feature
        if lookup_name not in ss01_feature.code:
            # Add lookup to the feature
            if "feature ss01" in ss01_feature.code:
                # Insert before feature block
                new_code = f"{lookup_code}\n\n{ss01_feature.code}"
            else:
                # Append to existing code
                new_code = f"{ss01_feature.code}\n\n{lookup_code}\nfeature ss01 {{\n    lookup {lookup_name};\n}} ss01;"
            ss01_feature.code = new_code
            print(f"✅ Added {lookup_name} lookup to ss01 feature")
        else:
            print(f"⚠️ Lookup {lookup_name} already exists in ss01 feature")

def clean_metadata(font):
    for g in font.glyphs:
        g.storeCategory = False
        g.storeSubCategory = False
        g.storeScript = False
        g.note = None

# Run script
font = Glyphs.font
if font:
    print("🚧 Building Rovas numerals 2–9...")
    created = create_composite_numerals(font)
    if created:
        ensure_ss01_feature(font, created)
    clean_metadata(font)

    font.newTab(" ".join(f"/{g}" for g in created))
    print("🎉 Done. Don't forget to enable the ss01 feature in your font's features!")
else:
    print("⚠️ No font open.")