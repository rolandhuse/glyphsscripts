#MenuTitle: Steal and Adjust Metrics and Kerning Between Masters
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Presents a dialog to choose source and target masters and adjustment percentage, then copies LSB, RSB, and kerning from source to target master for selected glyphs, adjusting based on (percentage / 100) * half the weight difference.
"""
import GlyphsApp
from GlyphsApp import Glyphs, Message
from AppKit import NSTextField, NSAlert, NSAlertStyleInformational, NSAlertFirstButtonReturn
import traceback

def get_master_weight_value(master):
    """Get weight value from master name or custom parameters"""
    try:
        for param in master.customParameters:
            if param.name == "weightClass" and param.value is not None:
                try:
                    return int(param.value)
                except:
                    pass
    except:
        pass
    name_lower = master.name.lower()
    if "thin" in name_lower or "hairline" in name_lower:
        return 100
    elif "extralight" in name_lower or "ultralight" in name_lower:
        return 200
    elif "light" in name_lower:
        return 300
    elif "regular" in name_lower or "normal" in name_lower or "book" in name_lower:
        return 400
    elif "medium" in name_lower:
        return 500
    elif "semibold" in name_lower or "demibold" in name_lower:
        return 600
    elif "bold" in name_lower:
        return 700
    elif "extrabold" in name_lower or "ultrabold" in name_lower:
        return 800
    elif "black" in name_lower or "heavy" in name_lower:
        return 900
    return 400  # Default to regular

def get_master_stem_value(master):
    """Try to get vertical stem value from master"""
    try:
        if hasattr(master, 'stems') and master.stems:
            for stem in master.stems:
                if not stem.horizontal:
                    return stem.position
        return None
    except:
        return None

def get_master_selection(font, title, prompt, default_index):
    """Get master selection from user"""
    alert = NSAlert.alloc().init()
    alert.setMessageText_(title)
    alert.setInformativeText_(prompt)
    alert.setAlertStyle_(NSAlertStyleInformational)
    alert.addButtonWithTitle_("OK")
    alert.addButtonWithTitle_("Cancel")
    text_field = NSTextField.alloc().initWithFrame_(((0, 0), (200, 24)))
    text_field.setStringValue_(str(default_index + 1))
    alert.setAccessoryView_(text_field)
    result = alert.runModal()
    if result == NSAlertFirstButtonReturn:
        try:
            master_index = int(text_field.stringValue()) - 1
            if 0 <= master_index < len(font.masters):
                return font.masters[master_index]
            else:
                Message(title="Invalid Input", message=f"Please enter a valid master number (1 to {len(font.masters)}).")
                return None
        except ValueError:
            Message(title="Invalid Input", message="Please enter a valid number.")
            return None
    return None

def get_percentage(default=50):
    """Get percentage adjustment from user"""
    alert = NSAlert.alloc().init()
    alert.setMessageText_("Select Adjustment Percentage")
    alert.setInformativeText_(
        "Enter the percentage (e.g., 50 for 50%) of the half-weight difference to apply to sidebearings and kerning.\n"
        "Positive values adjust in the direction of weight change (e.g., decrease sidebearings/less negative kerning for bolder, increase for lighter).\n"
        "Negative values reverse the direction (e.g., increase sidebearings/more negative kerning for bolder)."
    )
    alert.setAlertStyle_(NSAlertStyleInformational)
    alert.addButtonWithTitle_("OK")
    alert.addButtonWithTitle_("Cancel")
    text_field = NSTextField.alloc().initWithFrame_(((0, 0), (200, 24)))
    text_field.setStringValue_(str(default))
    alert.setAccessoryView_(text_field)
    result = alert.runModal()
    if result == NSAlertFirstButtonReturn:
        try:
            return float(text_field.stringValue())
        except ValueError:
            Message(title="Invalid Input", message="Please enter a valid number for percentage.")
            return None
    return None

def get_glyph_groups(font, glyph):
    """Get left and right kerning groups for a glyph"""
    left_group = glyph.leftKerningGroup
    right_group = glyph.rightKerningGroup
    return left_group, right_group

def adjust_kerning(font, source_master_id, target_master_id, glyphs, adjustment):
    """Copy and adjust kerning pairs for selected glyphs"""
    processed_pairs = 0
    extreme_kerning_pairs = []
    try:
        source_kerning = font.kerning.get(source_master_id, {})
        target_kerning = font.kerning.get(target_master_id, {})
        if not target_kerning:
            font.kerning[target_master_id] = {}
            target_kerning = font.kerning[target_master_id]

        for layer in glyphs:
            glyph = layer.parent
            if not glyph:
                continue
            glyph_name = glyph.name
            left_group, right_group = get_glyph_groups(font, glyph)

            # Check kerning pairs involving this glyph or its groups
            for left_key in [glyph_name, f"@MMK_L_{left_group}" if left_group else None]:
                if not left_key or left_key not in source_kerning:
                    continue
                for right_key in source_kerning[left_key]:
                    if right_key.startswith("@MMK_R_"):
                        # Group-to-group or glyph-to-group
                        right_glyph_or_group = right_key
                    else:
                        # Glyph-to-glyph
                        right_glyph = font.glyphs[right_key]
                        right_glyph_group = right_glyph.rightKerningGroup if right_glyph else None
                        right_glyph_or_group = right_key if right_glyph and (not right_glyph_group or f"@MMK_R_{right_glyph_group}" not in source_kerning[left_key]) else None
                    if not right_glyph_or_group:
                        continue

                    # Get source kerning value
                    kerning_value = source_kerning[left_key].get(right_glyph_or_group, 0)
                    if kerning_value == 0:
                        continue

                    # Adjust kerning value
                    new_kerning = kerning_value + adjustment
                    # Warn if kerning is extreme (e.g., > 200 or < -200)
                    if abs(new_kerning) > 200:
                        extreme_kerning_pairs.append(f"{left_key} -> {right_glyph_or_group}: {new_kerning:.2f}")

                    # Apply to target master
                    if left_key not in target_kerning:
                        target_kerning[left_key] = {}
                    target_kerning[left_key][right_glyph_or_group] = new_kerning
                    print(f"Adjusted kerning {left_key} -> {right_glyph_or_group}: {kerning_value:.2f} to {new_kerning:.2f}")
                    processed_pairs += 1

        return processed_pairs, extreme_kerning_pairs
    except Exception as e:
        print(f"Error adjusting kerning: {e}")
        return processed_pairs, extreme_kerning_pairs

def main():
    try:
        font = Glyphs.font
        if not font:
            Message(title="No Font Open", message="No font is open. Please open a font and try again.")
            return
        
        selected_glyphs = font.selectedLayers
        if not selected_glyphs or len(selected_glyphs) == 0:
            Message(title="No Glyphs Selected", message="No glyphs are selected. Please select at least one glyph.")
            return
        
        current_master = font.selectedFontMaster
        if not current_master:
            Message(title="No Master Selected", message="No master is selected. Please select a master.")
            return
        
        master_list = "\n".join([f"{i+1}. {master.name}" for i, master in enumerate(font.masters)])
        current_index = font.masters.index(current_master)
        
        source_master = get_master_selection(
            font, "Select Source Master",
            f"Available masters:\n{master_list}\n\nEnter the number of the master to steal metrics and kerning FROM:",
            current_index
        )
        if not source_master:
            return
            
        target_master = get_master_selection(
            font, "Select Target Master",
            f"Available masters:\n{master_list}\n\nEnter the number of the master to apply metrics and kerning TO:",
            current_index
        )
        if not target_master:
            return
        
        percentage = get_percentage()
        if percentage is None:
            return
        
        print(f"Source master: {source_master.name}")
        print(f"Target master: {target_master.name}")
        print(f"Adjustment percentage: {percentage}%")
        
        # Estimate weight difference
        stem_source = get_master_stem_value(source_master)
        stem_target = get_master_stem_value(target_master)
        if stem_source is not None and stem_target is not None and stem_source > 0:
            delta = stem_target - stem_source
            percent_diff = (delta / stem_source) * 100
            print(f"Using stem values: Source={stem_source}, Target={stem_target}")
        else:
            weight_source = get_master_weight_value(source_master)
            weight_target = get_master_weight_value(target_master)
            stem_source_approx = weight_source / 5.0
            stem_target_approx = weight_target / 5.0
            delta = stem_target_approx - stem_source_approx
            percent_diff = ((weight_target - weight_source) / weight_source) * 100 if weight_source != 0 else 0
            print(f"Using weight class approximation: Source={weight_source}, Target={weight_target}")
        
        # Calculate adjustment
        adjustment = (-delta / 2.0) * (percentage / 100.0)
        print(f"Estimated weight difference: {percent_diff:.2f}%")
        print(f"Adjustment for sidebearings and kerning: {adjustment:.2f}")
        
        # Apply metrics to selected glyphs
        processed_glyphs = 0
        negative_sb_glyphs = []
        for layer in selected_glyphs:
            try:
                glyph = layer.parent
                if not glyph:
                    continue
                    
                source_layer = glyph.layers[source_master.id]
                target_layer = glyph.layers[target_master.id]
                
                if not source_layer or not target_layer:
                    continue
                
                new_LSB = source_layer.LSB + adjustment
                new_RSB = source_layer.RSB + adjustment
                
                if new_LSB < 0 or new_RSB < 0:
                    negative_sb_glyphs.append(glyph.name)
                    new_LSB = max(0, new_LSB)
                    new_RSB = max(0, new_RSB)
                
                target_layer.LSB = new_LSB
                target_layer.RSB = new_RSB
                
                print(f"Adjusted {glyph.name}: LSB={new_LSB:.2f}, RSB={new_RSB:.2f}")
                processed_glyphs += 1
                
            except Exception as e:
                print(f"Error processing {glyph.name if 'glyph' in locals() else 'unknown'}: {e}")
        
        # Adjust kerning
        processed_pairs, extreme_kerning_pairs = adjust_kerning(font, source_master.id, target_master.id, selected_glyphs, adjustment)
        
        Glyphs.redraw()
        
        message = (
            f"Adjusted {processed_glyphs} glyph(s) and {processed_pairs} kerning pair(s)\n"
            f"From: {source_master.name}\nTo: {target_master.name}\nPercentage: {percentage}%\n"
            f"Adjustment: {adjustment:.1f} units"
        )
        if negative_sb_glyphs:
            message += f"\n\nWarning: Negative sidebearings detected in {', '.join(negative_sb_glyphs)} and clamped to 0."
        if extreme_kerning_pairs:
            message += f"\n\nWarning: Extreme kerning values detected in {', '.join(extreme_kerning_pairs)}."
        
        if processed_glyphs > 0 or processed_pairs > 0:
            Message(title="Complete", message=message, OKButton=None)
        else:
            Message(title="No Changes Applied", message="No glyphs or kerning pairs were processed.")
            
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        Message(title="Error", message=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()