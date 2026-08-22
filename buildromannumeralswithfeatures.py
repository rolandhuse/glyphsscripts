# MenuTitle: Build Roman Numerals (glyphs + ss01 feature)
# -*- coding: utf-8 -*-
__doc__ = """
Complete Roman numeral setup.
1. Builds rnNull + 30 composites from the Latin caps I V X L C D M
2. Writes the 'romanNumerals' feature prefix (glyph classes)
3. Writes the ss01 feature (place-value contextual logic, 1-3999)
Safe to re-run. Existing rn* glyphs are kept; prefix and ss01 are rewritten.
"""

from GlyphsApp import Glyphs, GSGlyph, GSLayer, GSComponent
from GlyphsApp import GSFeature, GSFeaturePrefix, Message
from Foundation import NSPoint

BASES = "IVXLCDM"

SEQUENCES = [
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
    "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC",
    "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM",
    "M", "MM", "MMM",
]

PREFIX_NAME = "romanNumerals"

PREFIX_CODE = """@dAll  = [zero one two three four five six seven eight nine];
@rnAll = [rnNull rnI rnII rnIII rnIV rnV rnVI rnVII rnVIII rnIX
          rnX rnXX rnXXX rnXL rnL rnLX rnLXX rnLXXX rnXC
          rnC rnCC rnCCC rnCD rnD rnDC rnDCC rnDCCC rnCM
          rnM rnMM rnMMM];
"""

SS01_CODE = """lookup rnP4 {
    ignore sub @dAll @dAll';
    ignore sub @dAll' @dAll @dAll @dAll @dAll;
    sub zero'  @dAll @dAll @dAll by rnNull;
    sub one'   @dAll @dAll @dAll by rnM;
    sub two'   @dAll @dAll @dAll by rnMM;
    sub three' @dAll @dAll @dAll by rnMMM;
} rnP4;

lookup rnP3 {
    ignore sub @dAll @dAll';
    ignore sub @dAll' @dAll @dAll @dAll;
    sub zero'  @dAll @dAll by rnNull;
    sub one'   @dAll @dAll by rnC;
    sub two'   @dAll @dAll by rnCC;
    sub three' @dAll @dAll by rnCCC;
    sub four'  @dAll @dAll by rnCD;
    sub five'  @dAll @dAll by rnD;
    sub six'   @dAll @dAll by rnDC;
    sub seven' @dAll @dAll by rnDCC;
    sub eight' @dAll @dAll by rnDCCC;
    sub nine'  @dAll @dAll by rnCM;
} rnP3;

lookup rnP2 {
    ignore sub @dAll @dAll';
    ignore sub @dAll' @dAll @dAll;
    sub zero'  @dAll by rnNull;
    sub one'   @dAll by rnX;
    sub two'   @dAll by rnXX;
    sub three' @dAll by rnXXX;
    sub four'  @dAll by rnXL;
    sub five'  @dAll by rnL;
    sub six'   @dAll by rnLX;
    sub seven' @dAll by rnLXX;
    sub eight' @dAll by rnLXXX;
    sub nine'  @dAll by rnXC;
} rnP2;

lookup rnP1 {
    ignore sub @dAll @dAll';
    ignore sub @dAll' @dAll;
    sub @rnAll zero' by rnNull;
    sub one'   by rnI;
    sub two'   by rnII;
    sub three' by rnIII;
    sub four'  by rnIV;
    sub five'  by rnV;
    sub six'   by rnVI;
    sub seven' by rnVII;
    sub eight' by rnVIII;
    sub nine'  by rnIX;
} rnP1;
"""


def get_layer(glyph, master_id):
    layer = glyph.layers[master_id]
    if layer is None:
        layer = GSLayer()
        layer.associatedMasterId = master_id
        glyph.layers[master_id] = layer
        layer = glyph.layers[master_id]
    return layer


def build_glyphs(font):
    missing = [b for b in BASES if not font.glyphs[b]]
    if missing:
        print("STOP - missing base glyphs: %s" % ", ".join(missing))
        return None

    created = 0
    skipped = 0

    if font.glyphs["rnNull"]:
        skipped += 1
    else:
        g = GSGlyph("rnNull")
        font.glyphs.append(g)
        g = font.glyphs["rnNull"]
        g.export = True
        for master in font.masters:
            layer = get_layer(g, master.id)
            layer.shapes = []
            layer.width = 0
        created += 1
        print("   + rnNull")

    for seq in SEQUENCES:
        name = "rn" + seq
        if font.glyphs[name]:
            skipped += 1
            continue
        g = GSGlyph(name)
        font.glyphs.append(g)
        g = font.glyphs[name]
        g.export = True
        for master in font.masters:
            layer = get_layer(g, master.id)
            layer.shapes = []
            x = 0
            for letter in seq:
                comp = GSComponent(letter)
                comp.automaticAlignment = False
                comp.position = NSPoint(x, 0)
                layer.shapes.append(comp)
                x += font.glyphs[letter].layers[master.id].width
            layer.width = x
        created += 1
        print("   + %s" % name)

    return (created, skipped)


def write_prefix(font):
    keep = [p for p in font.featurePrefixes if p.name != PREFIX_NAME]
    prefix = GSFeaturePrefix()
    prefix.name = PREFIX_NAME
    prefix.code = PREFIX_CODE
    font.featurePrefixes = [prefix] + keep
    print("   > prefix '%s' written (first in list)" % PREFIX_NAME)


def write_ss01(font):
    had_old = any(f.name == "ss01" for f in font.features)
    keep = [f for f in font.features if f.name != "ss01"]
    feature = GSFeature()
    feature.name = "ss01"
    feature.code = SS01_CODE
    feature.automatic = False
    font.features = keep + [feature]
    if had_old:
        print("   > ss01 replaced (automatic generation OFF)")
    else:
        print("   > ss01 created (automatic generation OFF)")


font = Glyphs.font

if not font:
    print("No font open.")
else:
    font.disableUpdateInterface()
    try:
        result = build_glyphs(font)
        if result is not None:
            write_prefix(font)
            write_ss01(font)
    finally:
        font.enableUpdateInterface()

    if result is not None:
        created, skipped = result
        print("")
        print("Done. %i glyphs created, %i already present." % (created, skipped))
        print("Now hit Compile in Font Info > Features, then test with ss01 on.")

        Message(
            title="Roman numerals ready",
            message=(
                "%i glyphs created, %i already there.\n\n"
                "Next: Font Info > Features > Compile, "
                "then turn on ss01 in the test tab."
            ) % (created, skipped),
            OKButton="Got it",
        )

        font.newTab("2025 1994 3999 4 40 400 4000 12345 0")