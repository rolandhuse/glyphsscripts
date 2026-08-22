from GlyphsApp import *
from vanilla import *

class SequentialKerningDialog:
    def __init__(self):
        self.font = Glyphs.font
        self.master = self.font.selectedFontMaster
        self.master_id = self.master.id

        self.selected_layers = self.font.selectedLayers
        self.selected_glyphs = [layer.parent for layer in self.selected_layers if layer and layer.parent]

        self.w = Window((300, 160), "Sequential Kerning")
        self.w.label = TextBox((10, 10, -10, 20), "Enter positive kerning value:")
        self.w.input = EditText((10, 35, -10, 20), "10")
        self.w.preview = CheckBox((10, 60, -10, 20), "Open preview tab", value=True)
        self.w.macro = CheckBox((10, 80, -10, 20), "Report in Macro Window", value=True)
        self.w.overwrite = CheckBox((10, 105, -10, 20), "Overwrite existing pairs", value=False)
        self.w.applyButton = Button((10, 130, 110, 20), "Apply", callback=self.applyKerning)
        self.w.cancelButton = Button((-110, 130, -10, 20), "Cancel", callback=self.cancel)
        self.w.open()

    def applyKerning(self, sender):
        try:
            value = int(self.w.input.get())
            if value <= 0:
                Message("Error", "Please enter a positive kerning value.", OKButton="OK")
                return
        except ValueError:
            Message("Error", "Please enter a valid integer.", OKButton="OK")
            return

        open_tab = self.w.preview.get()
        report_macro = self.w.macro.get()
        overwrite = self.w.overwrite.get()

        if report_macro:
            Glyphs.clearLog()
            print(f"🔧 Applying sequential kerning value {value} on master: {self.master.name}")
            print(f"Selected glyphs in order: {[g.name for g in self.selected_glyphs]}\n")

        tab_pairs = []
        applied = 0
        skipped = 0

        # Step through selected glyphs in sequence
        i = 0
        while i < len(self.selected_glyphs) - 1:
            leftGlyph = self.selected_glyphs[i]
            rightGlyph = self.selected_glyphs[i + 1]

            # Skip if either is space
            if leftGlyph.name == "space" or rightGlyph.name == "space":
                i += 1
                continue

            # Determine kerning keys (group or glyph)
            leftGroup = leftGlyph.rightKerningGroup
            rightGroup = rightGlyph.leftKerningGroup

            leftKey = f"@MMK_L_{leftGroup}" if leftGroup else leftGlyph.name
            rightKey = f"@MMK_R_{rightGroup}" if rightGroup else rightGlyph.name

            # Check for existing kerning
            existing = self.font.kerningForPair(self.master_id, leftKey, rightKey)

            if existing is not None:
                if overwrite:
                    # Overwrite the existing value
                    self.font.setKerningForPair(self.master_id, leftKey, rightKey, value)
                    applied += 1
                    if report_macro:
                        print(f"🔁 Overwrote existing {existing} to {value}: {leftKey} - {rightKey}")
                    tab_pairs.append(f"/{leftGlyph.name}/{rightGlyph.name}")
                else:
                    skipped += 1
                    if report_macro:
                        print(f"⚠️ Skipped existing: {leftKey} - {rightKey} (value: {existing})")
                i += 1
                continue

            # Otherwise, apply new kerning
            self.font.setKerningForPair(self.master_id, leftKey, rightKey, value)
            applied += 1
            tab_pairs.append(f"/{leftGlyph.name}/{rightGlyph.name}")
            if report_macro:
                print(f"✅ Applied {value}: {leftKey} - {rightKey}")

            i += 1

        # Open preview tab
        if open_tab and tab_pairs:
            preview_string = "  ".join(tab_pairs)
            self.font.newTab(preview_string)

        # Final summary
        message = f"✅ Applied {value} to {applied} pair(s)."
        if skipped:
            message += f" Skipped {skipped} existing pair(s)."
        if report_macro:
            print("\n" + message)

        Message("Kerning Done", message, OKButton="OK")
        self.w.close()

    def cancel(self, sender):
        self.w.close()

# Run the dialog
SequentialKerningDialog()
