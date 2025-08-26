# MenuTitle: Set Rovas Kerning Groups
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Sets left and right kerning groups for all selected glyphs. In the case of compounds, will use the groups of the base components, otherwise makes an informed guess based on a built-in dictionary.
"""

# Copyright: Georg Seifert, 2010, www.schriftgestaltung.de Version 1.0
from GlyphsApp import Glyphs, Message

import traceback
verbose = False

alwaysExclude = (
	".notdef",
	".null",
	"CR",
)

Keys = [

	# ROVAS
   "AA-rovas",
   "A-rovas",
   "B-rovas",
   "C-rovas",
   "CS-rovas",
   "D-rovas",
   "DZ-rovas",
   "DZS-rovas",
   "E-rovas",
   "EE-rovas",
   "F-rovas",
   "G-rovas",
   "GY-rovas",
   "H-rovas",
   "I-rovas",
   "II-rovas",
   "J-rovas",
   "K-rovas",
   "L-rovas",
   "LY-rovas",
   "M-rovas",
   "N-rovas",
   "NY-rovas",
   "O-rovas",
   "OO-rovas",
   "OE-rovas",
   "OEE-rovas",
   "P-rovas",
   "Q-rovas",
   "R-rovas",
   "S-rovas",
   "SZ-rovas",
   "T-rovas",
   "TY-rovas",
   "U-rovas",
   "UU-rovas",
   "UE-rovas",
   "UEE-rovas",
   "V-rovas",
   "W-rovas",
   "X-rovas",
   "Y-rovas",
   "Z-rovas",
   "ZS-rovas",
   "aa-rovas",
   "a-rovas",
   "b-rovas",
   "c-rovas",
   "cs-rovas",
   "d-rovas",
   "dz-rovas",
   "dzs-rovas",
   "e-rovas",
   "ee-rovas",
   "f-rovas",
   "g-rovas",
   "gy-rovas",
   "h-rovas",
   "i-rovas",
   "ii-rovas",
   "j-rovas",
   "k-rovas",
   "l-rovas",
   "ly-rovas",
   "m-rovas",
   "n-rovas",
   "ny-rovas",
   "o-rovas",
   "oo-rovas",
   "oe-rovas",
   "oee-rovas",
   "p-rovas",
   "q-rovas",
   "r-rovas",
   "s-rovas",
   "sz-rovas",
   "t-rovas",
   "ty-rovas",
   "u-rovas",
   "uu-rovas",
   "ue-rovas",
   "uee-rovas",
   "v-rovas",
   "w-rovas",
   "x-rovas",
   "y-rovas",
   "z-rovas",
   "zs-rovas",
   "AA-rovas",
   "A-rovas",
   "B-rovas",
   "C-rovas",
   "CS-rovas",
   "D-rovas",
   "DZ-rovas",
   "DZS-rovas",
   "E-rovas",
   "EE-rovas",
   "F-rovas",
   "G-rovas",
   "GY-rovas",
   "H-rovas",
   "I-rovas",
   "II-rovas",
   "J-rovas",
   "K-rovas",
   "L-rovas",
   "LY-rovas",
   "M-rovas",
   "N-rovas",
   "NY-rovas",
   "O-rovas",
   "OO-rovas",
   "OE-rovas",
   "OEE-rovas",
   "P-rovas",
   "Q-rovas",
   "R-rovas",
   "S-rovas",
   "SZ-rovas",
   "T-rovas",
   "TY-rovas",
   "U-rovas",
   "UU-rovas",
   "UE-rovas",
   "UEE-rovas",
   "V-rovas",
   "W-rovas",
   "X-rovas",
   "Y-rovas",
   "Z-rovas",
   "ZS-rovas",
   "aa-rovas",
   "a-rovas",
   "b-rovas",
   "c-rovas",
   "cs-rovas",
   "d-rovas",
   "dz-rovas",
   "dzs-rovas",
   "e-rovas",
   "ee-rovas",
   "f-rovas",
   "g-rovas",
   "gy-rovas",
   "h-rovas",
   "i-rovas",
   "ii-rovas",
   "j-rovas",
   "k-rovas",
   "l-rovas",
   "ly-rovas",
   "m-rovas",
   "n-rovas",
   "ny-rovas",
   "o-rovas",
   "oo-rovas",
   "oe-rovas",
   "oee-rovas",
   "p-rovas",
   "q-rovas",
   "r-rovas",
   "s-rovas",
   "sz-rovas",
   "t-rovas",
   "ty-rovas",
   "u-rovas",
   "uu-rovas",
   "ue-rovas",
   "uee-rovas",
   "v-rovas",
   "w-rovas",
   "x-rovas",
   "y-rovas",
   "z-rovas",
   "zs-rovas"

	# PUNCTUATION
	
	"comma",
	"semicolon",
	"ellipsis",
	"softhyphen",
	"quoteleft",
	"quoteright",
	"quotedblright",
	"quotesinglbase",
	"quotedblbase",
	"guilsinglleft",
	"guilsinglright",
	"endash",
	"emdash",
	"periodcentered",
	"perthousand",
    "percent"
	"semicolon",
	"quotedblbase"
    "comma.rtlm",
    "semicolon.rtlm"
    "percent.rtlm"
]

DefaultKeys = {
    # ROVAS
    "A-rovas": ("","Cs-rovas"),
    "AA-rovas": ("","Cs-rovas"),
    "B-rovas": ("B-rovas","B-rovas"),
    "C-rovas": ("",""),
    "Cs-rovas": ("Cs-rovas","Cs-rovas"),
    "D-rovas": ("","D-rovas"),
    "DZ-rovas": ("Cs-rovas","D-rovas"),
    "DZS-rovas": ("",""),
    "E-rovas": ("E-rovas","E-rovas"),
    "EClosed-rovas": ("E-rovas","E-rovas"),
    "EE-rovas": ("","E-rovas"),
    "F-rovas": ("F-rovas","F-rovas"),
    "G-rovas": ("S-rovas","S-rovas"),
    "GY-rovas": ("",""),
    "H-rovas": ("",""),
    "I-rovas": ("I-rovas","I-rovas"),
    "Ii-rovas": ("Ii-rovas","Ii-rovas"),
    "J-rovas": ("J-rovas","Cs-rovas"),
    "K-rovas": ("","K-rovas"),
    "Ak-rovas": ("J-rovas",""),
    "L-rovas": ("S-rovas","S-rovas"),
    "LY-rovas": ("F-rovas","F-rovas"),
    "M-rovas": ("","Cs-rovas"),
    "N-rovas": ("","F-rovas"),
    "NY-rovas": ("Cs-rovas","F-rovas"),
    "O-rovas": ("O-rovas","F-rovas"),
    "OO-rovas": ("O-rovas","O-rovas"),
    "OE-rovas": ("Cs-rovas","B-rovas"),
    "OEE-rovas": ("",""),
    "P-rovas": ("","Cs-rovas"),
    "Q-rovas": ("",""),
    "R-rovas": ("Cs-rovas","Cs-rovas"),
    "S-rovas": ("S-rovas","S-rovas"),
    "SZ-rovas": ("Cs-rovas","Cs-rovas"),
    "T-rovas": ("","Cs-rovas"),
    "TY-rovas": ("B-rovas","B-rovas"),
    "U-rovas": ("Cs-rovas","Cs-rovas"),
    "UU-rovas": ("Cs-rovas","Cs-rovas"),
    "UE-rovas": ("",""),
    "UEE-rovas": ("",""),
    "V-rovas": ("Cs-rovas","Cs-rovas"),
    "W-rovas": ("Cs-rovas","Cs-rovas"),
    "X-rovas": ("Cs-rovas","K-rovas"),
    "Y-rovas": ("J-rovas","I-rovas"),
    "Z-rovas": ("Cs-rovas","Cs-rovas"),
    "ZS-rovas": ("T-rovas",""),
    "a-rovas": ("","cs-rovas"),
    "aa-rovas": ("","cs-rovas"),
    "b-rovas": ("b-rovas","b-rovas"),
    "c-rovas": ("",""),
    "cs-rovas": ("cs-rovas","cs-rovas"),
    "d-rovas": ("","d-rovas"),
    "dz-rovas": ("cs-rovas","d-rovas"),
    "dzs-rovas": ("",""),
    "e-rovas": ("e-rovas","e-rovas"),
    "eclosed-rovas": ("e-rovas","e-rovas"),
    "ee-rovas": ("","e-rovas"),
    "f-rovas": ("f-rovas","f-rovas"),
    "g-rovas": ("s-rovas","s-rovas"),
    "gy-rovas": ("",""),
    "h-rovas": ("",""),
    "i-rovas": ("i-rovas","i-rovas"),
    "ii-rovas": ("ii-rovas","ii-rovas"),
    "j-rovas": ("j-rovas","cs-rovas"),
    "k-rovas": ("","k-rovas"),
    "ak-rovas": ("j-rovas",""),
    "l-rovas": ("s-rovas","s-rovas"),
    "ly-rovas": ("f-rovas","f-rovas"),
    "m-rovas": ("","cs-rovas"),
    "n-rovas": ("","f-rovas"),
    "ny-rovas": ("cs-rovas","f-rovas"),
    "o-rovas": ("o-rovas","f-rovas"),
    "oo-rovas": ("o-rovas","o-rovas"),
    "oe-rovas": ("cs-rovas","b-rovas"),
    "oee-rovas": ("",""),
    "p-rovas": ("","cs-rovas"),
    "q-rovas": ("",""),
    "r-rovas": ("cs-rovas","cs-rovas"),
    "s-rovas": ("s-rovas","s-rovas"),
    "sz-rovas": ("cs-rovas","cs-rovas"),
    "t-rovas": ("","cs-rovas"),
    "ty-rovas": ("b-rovas","b-rovas"),
    "u-rovas": ("cs-rovas","cs-rovas"),
    "uu-rovas": ("cs-rovas","cs-rovas"),
    "ue-rovas": ("",""),
    "uee-rovas": ("",""),
    "v-rovas": ("cs-rovas","cs-rovas"),
    "w-rovas": ("cs-rovas","cs-rovas"),
    "x-rovas": ("cs-rovas","k-rovas"),
    "y-rovas": ("j-rovas","i-rovas"),
    "z-rovas": ("cs-rovas","cs-rovas"),
    "zs-rovas": ("t-rovas",""),
    
	

	# PUNCTUATION
	"comma": ("period", "period"),
	"semicolon": ("colon", "colon"),
	"ellipsis": ("period", "period"),
	"softhyphen": ("hyphen", "hyphen"),
	"quoteleft": ("quotedblleft", "quotedblleft"),
	"quoteright": ("quotedblleft", "quotedblleft"),
	"quotedblright": ("quotedblleft", "quotedblleft"),
	"quotesinglbase": ("period", "period"),
	"quotedblbase": ("period", "period"),
	"guilsinglleft": ("guillemetleft", "guillemetleft"),
	"guilsinglright": ("guillemetright", "guillemetright"),
	"guillemetleft": ("guillemetleft", "guillemetleft"),
	"guillemetright": ("guillemetright", "guillemetright"),
	"endash": ("hyphen", "hyphen"),
	"emdash": ("hyphen", "hyphen"),
	"periodcentered": ("anoteleia", "anoteleia"),
	"cent": ("o", "c"),
	"perthousand": ("percent", "percent"),
	"semicolon": ("colon", "colon"),
	"quotedblbase": ("period", "period"),
    "comma.rtlm": ("period", "period"),
    "semicolon.rtlm": ("colon", "colon"),
    "percent.rtlm": ("percent", "percent"),


}


def KeysForGlyph(glyph):
    """Get left and right kerning groups for a glyph."""
    if glyph is None:
        return (None, None)
    
    left_key = glyph.leftKerningGroup
    right_key = glyph.rightKerningGroup
    
    # Convert empty strings to None
    left_key = left_key if left_key else None
    right_key = right_key if right_key else None
    
    return (left_key, right_key)

def updateKeyGlyphsForSelected():
    """Update kerning groups for all selected glyphs, overriding existing groups."""
    countL, countR = 0, 0
    font = Glyphs.font
    if not font:
        Message("No font open", "Please open a font first.", OKButton=None)
        return
    
    selected_layers = font.selectedLayers
    if not selected_layers:
        Message("No glyphs selected", "Please select some glyphs first.", OKButton=None)
        return
    
    for layer in selected_layers:
        glyph = layer.parent
        if glyph.name in alwaysExclude:
            glyph.leftKerningGroup = None
            glyph.rightKerningGroup = None
            print(f"🔠 {glyph.name}: 🚫 ↔️ 🚫 (excluded)")
            continue

        left_key = None
        right_key = None
        
        # For compound glyphs, use components' kerning groups
        if layer.components and not layer.paths:
            first_component = layer.components[0].component
            if first_component:
                left_key = KeysForGlyph(first_component)[0]
                if not left_key and first_component.name in DefaultKeys:
                    left_key = DefaultKeys[first_component.name][0]
                
                # Find last non-mark component for right side
                last_component = None
                for component in reversed(layer.components):
                    if component.component.category != "Mark":
                        last_component = component.component
                        break
                
                if last_component:
                    right_key = KeysForGlyph(last_component)[1]
                    if not right_key and last_component.name in DefaultKeys:
                        right_key = DefaultKeys[last_component.name][1]
        
        # For ligatures (names with underscores)
        elif "_" in glyph.name:
            parts = glyph.name.split("_")
            first_part = font.glyphs[parts[0]]
            last_part = font.glyphs[parts[-1]]
            
            if first_part:
                left_key = KeysForGlyph(first_part)[0]
            if last_part:
                right_key = KeysForGlyph(last_part)[1]
        
        # Use default groups if still not found
        if not left_key and glyph.name in DefaultKeys:
            left_key = DefaultKeys[glyph.name][0]
        if not right_key and glyph.name in DefaultKeys:
            right_key = DefaultKeys[glyph.name][1]
        
        # Fallback to glyph name if no group found
        left_key = left_key or glyph.name
        right_key = right_key or glyph.name
        
        # Override existing groups
        glyph.leftKerningGroup = left_key
        glyph.rightKerningGroup = right_key
        
        countL += 1
        countR += 1
        
        print(f"🔠 {glyph.name}: {left_key} ↔️ {right_key}")

    Message(
        title="Kerning Groups Updated",
        message=f"Set {countL} left and {countR} right groups in {len(selected_layers)} glyphs.\nSee Macro Panel for details.",
        OKButton=None
    )

def main():
    Glyphs.clearLog()
    print("### Setting Rovas Kerning Groups ###\n")
    updateKeyGlyphsForSelected()
    print("\n✅ Done.")

if __name__ == "__main__":
    main()