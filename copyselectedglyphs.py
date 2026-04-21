# MenuTitle: Copy Glyphs from Source to Target (Preserve Backgrounds)
# -*- coding: utf-8 -*-
__doc__ = """
Lets you choose a source and target font from open fonts,
and replaces outlines and anchors for specified glyphs in the target font’s
current master. Backgrounds and other layers are preserved.
"""

import GlyphsApp
from AppKit import NSAlert, NSTextField, NSApp

def ask_user_input(message, default=""):
	alert = NSAlert.alloc().init()
	alert.setMessageText_(message)
	text_field = NSTextField.alloc().initWithFrame_(((0, 0), (200, 24)))
	text_field.setStringValue_(default)
	alert.setAccessoryView_(text_field)
	alert.addButtonWithTitle_("OK")
	alert.addButtonWithTitle_("Cancel")
	response = alert.runModal()
	if response == 1000:  # OK clicked
		return text_field.stringValue()
	return None

def pick_font_dialog(prompt_text):
	all_fonts = Glyphs.fonts
	font_list = "\n".join(
		[f"{i}: {f.familyName or 'Unnamed'} — {f.filepath or '(unsaved)'}" for i, f in enumerate(all_fonts)]
	)
	alert_text = f"{prompt_text}\n\n{font_list}"
	response = ask_user_input(alert_text, "0")
	if response is None:
		return None
	try:
		index = int(response)
		return all_fonts[index]
	except:
		return None

def copy_glyph_data(source_font, target_font, glyph_names):
	target_master = target_font.selectedFontMaster
	target_master_name = target_master.name

	print(f"\n🔹 Copying from: {source_font.familyName}")
	print(f"🔹 Target font: {target_font.familyName}")
	print(f"🔹 Target master: {target_master_name}\n")

	for name in glyph_names:
		source_glyph = source_font.glyphs[name]
		target_glyph = target_font.glyphs[name]

		if not source_glyph:
			print(f"⚠️ Glyph '{name}' not in source font.")
			continue
		if not target_glyph:
			print(f"⚠️ Glyph '{name}' not in target font.")
			continue

		# Match master by name; fallback to first
		source_layer = None
		for m in source_font.masters:
			if m.name == target_master_name:
				source_layer = source_glyph.layers[m.id]
				break
		if not source_layer:
			source_layer = source_glyph.layers[source_font.masters[0].id]

		target_layer = target_glyph.layers[target_master.id]

		# Clear only outlines
		target_layer.shapes = []

		# Copy outlines/components
		for shape in source_layer.shapes:
			target_layer.shapes.append(shape.copy())

		# Copy anchors
		target_layer.anchors = []
		for anchor in source_layer.anchors:
			target_layer.anchors.append(anchor.copy())

		print(f"✅ Copied outlines & anchors for '{name}'")

	Glyphs.showNotification("Copy Glyphs", f"Copied {len(glyph_names)} glyph(s).")


def main():
	if len(Glyphs.fonts) < 2:
		Glyphs.showNotification("Copy Glyphs", "Open at least two fonts.")
		return

	source_font = pick_font_dialog("Select SOURCE font index:")
	if not source_font:
		Glyphs.showNotification("Copy Glyphs", "No valid source font selected.")
		return

	target_font = pick_font_dialog("Select TARGET font index:")
	if not target_font:
		Glyphs.showNotification("Copy Glyphs", "No valid target font selected.")
		return

	glyph_input = ask_user_input("Enter glyph names (comma or space separated):", "")
	if not glyph_input:
		Glyphs.showNotification("Copy Glyphs", "No glyphs specified.")
		return

	glyph_names = [g.strip() for g in glyph_input.replace(",", " ").split() if g.strip()]
	copy_glyph_data(source_font, target_font, glyph_names)

main()
