# MenuTitle: Build Rovas Script with Features
# -*- coding: utf-8 -*-
"""
Generates Old Hungarian Rovas letters and numerals with proper Unicode and OpenType features.
Adds to existing ss01/liga features without overwriting them, and tags glyphs for sorting in the main Glyphs view.
Also handles mirrored punctuation for RTL scripts.
"""

import traceback
from GlyphsApp import *
from GlyphsApp.plugins import *

def create_rovas_glyphs(font):
    rovas_data = [
        ("A", "A", "10C80"), ("Á", "AA", "10C81"), ("B", "B", "10C82"), ("C", "C", "10C84"),
        ("CS", "CS", "10C86"), ("D", "D", "10C87"), ("Dz", "DZ", "10CB3"), ("Dzs", "DZS", "10CB4"),
        ("E", "E", "10C89"), ("É", "EE", "10C8B"), ("F", "F", "10C8C"), ("G", "G", "10C8D"),
        ("GY", "GY", "10C8E"), ("H", "H", "10C8F"), ("I", "I", "10C90"), ("Í", "II", "10C91"),
        ("J", "J", "10C92"), ("K", "K", "10C93"), ("L", "L", "10C96"), ("LY", "LY", "10C97"),
        ("M", "M", "10C98"), ("N", "N", "10C99"), ("NY", "NY", "10C9A"), ("O", "O", "10C9B"),
        ("Ó", "OO", "10C9C"), ("Ö", "OE", "10C9E"), ("Ő", "OEE", "10C9F"), ("P", "P", "10CA0"),
        ("Q", "Q", "10CB5"), ("R", "R", "10CA2"), ("S", "S", "10CA4"), ("SZ", "SZ", "10CA5"),
        ("T", "T", "10CA6"), ("TY", "TY", "10CA8"), ("U", "U", "10CAA"), ("Ú", "UU", "10CAB"),
        ("Ü", "UE", "10CAD"), ("Ű", "UEE", "10CB9"), ("V", "V", "10CAE"), ("W", "W", "10CB6"),
        ("X", "X", "10CB7"), ("Y", "Y", "10CB8"), ("Z", "Z", "10CAF"), ("ZS", "ZS", "10CB0"),
        ("a", "a", "10CC0"), ("á", "aa", "10CC1"), ("b", "b", "10CC2"), ("c", "c", "10CC4"),
        ("cs", "cs", "10CC6"), ("d", "d", "10CC7"), ("dz", "dz", "10CF3"), ("dzs", "dzs", "10CF4"),
        ("e", "e", "10CC9"), ("é", "ee", "10CCB"), ("f", "f", "10CCC"), ("g", "g", "10CCD"),
        ("gy", "gy", "10CCE"), ("h", "h", "10CCF"), ("i", "i", "10CD0"), ("í", "ii", "10CD1"),
        ("j", "j", "10CD2"), ("k", "k", "10CD3"), ("l", "l", "10CD6"), ("ly", "ly", "10CD7"),
        ("m", "m", "10CD8"), ("n", "n", "10CD9"), ("ny", "ny", "10CDA"), ("o", "o", "10CDB"),
        ("ó", "oo", "10CDC"), ("ö", "oe", "10CDE"), ("ő", "oee", "10CDF"), ("p", "p", "10CE0"),
        ("q", "q", "10CF5"), ("r", "r", "10CE2"), ("s", "s", "10CE4"), ("sz", "sz", "10CE5"),
        ("t", "t", "10CE6"), ("ty", "ty", "10CE8"), ("u", "u", "10CEA"), ("ú", "uu", "10CEB"),
        ("ü", "ue", "10CED"), ("ű", "uee", "10CF9"), ("v", "v", "10CEE"), ("w", "w", "10CF6"),
        ("x", "x", "10CF7"), ("y", "y", "10CF8"), ("z", "z", "10CEF"), ("zs", "zs", "10CF0"),
    ]

    for char, name, unicode_hex in rovas_data:
        glyph_name = f"{name}.rovas"
        if font.glyphs[glyph_name]:
            print(f"⚠️ Skipping {glyph_name}: Already exists.")
            continue

        try:
            g = GSGlyph(glyph_name)
            g.unicode = unicode_hex
            g.productionName = f"uni{unicode_hex}"
            font.glyphs.append(g)
            print(f"✅ Created {glyph_name}")

            for master in font.masters:
                layer = GSLayer()
                layer.associatedMasterId = master.id
                g.layers[master.id] = layer
                layer.width = 600

        except Exception as e:
            print(f"❌ Error in {glyph_name}: {e}")
            traceback.print_exc()

def create_rovas_numerals(font):
    numeral_data = [
        ("one.rovas", "1", "10CFA"),
        ("five.rovas", "5", "10CFB"),
        ("ten.rovas", "10", "10CFC"),
        ("fifty.rovas", "50", "10CFD"),
        ("hundred.rovas", "100", "10CFE"),
        ("fivehundred.rovas", "500", "10CBF"),
        ("thousand.rovas", "1000", "10CFF"),
    ]

    for glyph_name, components, unicode_hex in numeral_data:
        if font.glyphs[glyph_name]:
            print(f"⚠️ Skipping {glyph_name}: Already exists.")
            continue

        try:
            numeral_glyph = GSGlyph(glyph_name)
            numeral_glyph.productionName = glyph_name
            numeral_glyph.unicode = unicode_hex

            numeral_layer = GSLayer()
            numeral_layer.associatedMasterId = font.masters[0].id
            numeral_glyph.layers[font.masters[0].id] = numeral_layer

            if isinstance(components, str):
                components = [components]

            for comp_name in components:
                if comp_name in font.glyphs:
                    comp_glyph = font.glyphs[comp_name]
                    component = GSComponent(comp_glyph)
                    numeral_layer.components.append(component)

            numeral_glyph.storeCategory = True
            numeral_glyph.category = "Number"
            numeral_glyph.storeSubCategory = True
            numeral_glyph.subCategory = "Decimal Digit"
            numeral_glyph.note = "Old Hungarian (Rovás) numeral"
            numeral_glyph.updateGlyphInfo()

            font.glyphs.append(numeral_glyph)
            print(f"✅ Created {glyph_name}")

        except Exception as e:
            print(f"❌ Error in creating {glyph_name}: {e}")
            traceback.print_exc()

def create_mirrored_punctuation(font):
    punctuation_data = [
        ("comma", "comma.rtlm"),
        ("semicolon", "semicolon.rtlm"),
        ("question", "question.rtlm"),
        ("numbersign", "numbersign.rtlm"),
        ("percent", "percent.rtlm"),
    ]

    for original, mirrored in punctuation_data:
        if mirrored in font.glyphs:
            print(f"⚠️ Skipping {mirrored}: Already exists.")
            continue

        try:
            if original not in font.glyphs:
                original_glyph = GSGlyph(original)
                original_glyph.category = "Punctuation"
                original_glyph.subCategory = "Other Punctuation"
                font.glyphs.append(original_glyph)
                print(f"✅ Created placeholder for {original}")
            else:
                original_glyph = font.glyphs[original]

            mirrored_glyph = GSGlyph(mirrored)
            mirrored_glyph.productionName = f"{original}.rtlm"
            mirrored_layer = GSLayer()
            mirrored_layer.associatedMasterId = font.masters[0].id
            mirrored_glyph.layers[font.masters[0].id] = mirrored_layer

            component = GSComponent(original_glyph)
            mirrored_layer.components.append(component)

            for comp in mirrored_layer.components:
                width = comp.layer.width
                comp.transform = (-1, 0, 0, 1, width, 0)

            font.glyphs.append(mirrored_glyph)
            print(f"✅ Created {mirrored} (mirrored version of {original})")

        except Exception as e:
            print(f"❌ Error in creating mirrored {mirrored}: {e}")
            traceback.print_exc()

def add_opentype_features(font):
    liga_rules = """
        sub zero one-rovas by ten-rovas;
        sub zero zero one-rovas by hundred-rovas;  
        sub zero five-rovas by fifty-rovas;
        sub zero zero five-rovas by fivehundred-rovas;
        sub zero zero zero one-rovas by thousand-rovas;
    """

    rtlm_rules = """
        sub comma by comma.rtlm;
        sub semicolon by semicolon.rtlm;
        sub question by question.rtlm;
        sub numbersign by numbersign.rtlm;
        sub percent by percent.rtlm;
    """

    def update_feature(feature_name, rules):
        existing = font.features[feature_name] if feature_name in font.features else None
        if existing:
            if rules.strip() not in existing.code:
                existing.code += "\n" + rules
                print(f"✅ Updated existing {feature_name} feature")
            else:
                print(f"⚠️ {feature_name} already contains rules.")
        else:
            new_feature = GSFeature()
            new_feature.name = feature_name
            new_feature.code = rules
            font.features.append(new_feature)
            print(f"✅ Created new {feature_name} feature")

    update_feature("liga", liga_rules)
    update_feature("rtlm", rtlm_rules)

def tag_rovas_glyphs(font):
    try:
        font.disableUpdateInterface()
        for glyph in font.glyphs:
            if not glyph.unicode:
                continue
            code = int(glyph.unicode, 16)
            if code in (0x10CFA, 0x10CFB, 0x10CFC, 0x10CFD, 0x10CFE, 0x10CBF, 0x10CFF):
                glyph.script = "Rovas"
                glyph.category = "Number"
                glyph.subCategory = "Decimal Digit"
            elif 0x10C80 <= code <= 0x10CFF:
                glyph.script = "Rovas"
                glyph.category = "Letter"
                glyph.subCategory = "Uppercase Letter"
            elif code in (0x2E41, 0x2E42):
                glyph.script = "Rovas"
                glyph.category = "Punctuation"
                glyph.subCategory = "Other Punctuation"
            glyph.updateGlyphInfo()
    finally:
        font.enableUpdateInterface()

# Run
font = Glyphs.font
if font:
    create_rovas_glyphs(font)
    create_rovas_numerals(font)
    create_mirrored_punctuation(font)
    add_opentype_features(font)
    tag_rovas_glyphs(font)

    Message(
        title="Rovas Script Added",
        message="Old Hungarian Rovas glyphs, numerals, mirrored punctuation, and features have been added. Sorting tags are applied.",
        OKButton="Nice!"
    )

    font.newTab("𐲏𐳉𐳖𐳖𐳜")
    print("🎉 Done! Rovas glyphs and features created.")
else:
    print("⚠️ No font open.")
