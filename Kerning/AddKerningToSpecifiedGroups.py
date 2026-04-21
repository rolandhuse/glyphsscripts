# add code here# MenuTitle: Manual Kerning Adder
# -*- coding: utf-8 -*-
__doc__ = """
Add a fixed kerning value between specific glyphs or groups in the current master.
"""

import vanilla
from GlyphsApp import Glyphs, Message


class ManualKerner:

    def __init__(self):
        self.w = vanilla.FloatingWindow((400, 200), "Manual Kerning Adder")

        self.w.textLeft = vanilla.TextBox((15, 15, 120, 20), "Left glyphs/groups:")
        self.w.leftInput = vanilla.EditText((150, 15, -15, 22), "")

        self.w.leftIsGroup = vanilla.CheckBox((150, 40, 150, 20), "Left is group", value=False)

        self.w.textRight = vanilla.TextBox((15, 70, 120, 20), "Right glyphs/groups:")
        self.w.rightInput = vanilla.EditText((150, 70, -15, 22), "")

        self.w.rightIsGroup = vanilla.CheckBox((150, 95, 150, 20), "Right is group", value=False)

        self.w.textKern = vanilla.TextBox((15, 130, 120, 20), "Kerning value:")
        self.w.kernValue = vanilla.EditText((150, 130, 80, 22), "20")

        self.w.applyButton = vanilla.Button((-110, -30, -15, -10), "Apply", callback=self.applyKerning)

        self.w.open()

    def applyKerning(self, sender):
        font = Glyphs.font
        master = font.selectedFontMaster
        masterID = master.id

        try:
            kernValue = int(self.w.kernValue.get())
        except:
            Message("Invalid kerning value", "Please enter a numeric value.")
            return

        leftItems = [x.strip() for x in self.w.leftInput.get().split(",") if x.strip()]
        rightItems = [x.strip() for x in self.w.rightInput.get().split(",") if x.strip()]
        isLeftGroup = self.w.leftIsGroup.get()
        isRightGroup = self.w.rightIsGroup.get()

        kernedPairs = []

        for left in leftItems:
            leftKey = f"@MMK_L_{left}" if isLeftGroup else left
            for right in rightItems:
                rightKey = f"@MMK_R_{right}" if isRightGroup else right

                # Apply kerning
                font.setKerningForPair(masterID, leftKey, rightKey, kernValue)
                kernedPairs.append((leftKey, rightKey))

        # Build report
        report = f"✅ Applied {kernValue} units kerning to {len(kernedPairs)} pairs:\n"
        for l, r in kernedPairs:
            report += f"{l} ↔ {r}\n"

        Glyphs.clearLog()
        Glyphs.showMacroWindow()
        print(report)


ManualKerner()
a