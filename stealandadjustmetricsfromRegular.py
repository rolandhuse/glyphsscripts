#MenuTitle: Steal and Adjust Metrics Between Masters
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Presents a dialog to choose source and target masters, then copies LSB and RSB from source to target master for selected glyphs, adjusting based on half the weight difference.
"""

import GlyphsApp
from GlyphsApp import Glyphs, Message
from AppKit import NSTextField, NSAlert, NSAlertStyleInformational, NSAlertFirstButtonReturn
import traceback

def get_master_weight_value(master):
    """Get weight value from master name or custom parameters"""
    try:
        # Check for weight class custom parameter
        for param in master.customParameters:
            if param.name == "weightClass" and param.value is not None:
                try:
                    return int(param.value)
                except:
                    pass
    except:
        pass
    
    # Fallback: guess from master name
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
    else:
        return 400  # Default to regular

def get_master_stem_value(master):
    """Try to get vertical stem value from master"""
    try:
        # Check if master has stems defined
        if hasattr(master, 'stems') and master.stems:
            # Look for vertical stems (non-horizontal)
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
    
    # Add buttons
    alert.addButtonWithTitle_("OK")
    alert.addButtonWithTitle_("Cancel")
    
    # Create text field for input
    text_field = NSTextField.alloc().initWithFrame_(((0, 0), (200, 24)))
    text_field.setStringValue_(str(default_index + 1))
    alert.setAccessoryView_(text_field)
    
    # Run dialog
    result = alert.runModal()
    
    if result == NSAlertFirstButtonReturn:  # OK button
        try:
            input_value = text_field.stringValue()
            master_index = int(input_value) - 1
            if 0 <= master_index < len(font.masters):
                return font.masters[master_index]
            else:
                Message(title="Invalid Input", message="Please enter a valid master number (1 to {}).".format(len(font.masters)))
                return None
        except ValueError:
            Message(title="Invalid Input", message="Please enter a valid number.")
            return None
    return None

def main():
    try:
        # Get the current font
        font = Glyphs.font
        if not font:
            Message(title="No Font Open", message="No font is open. Please open a font and try again.")
            return

        # Get selected glyphs
        selected_glyphs = font.selectedLayers
        if not selected_glyphs or len(selected_glyphs) == 0:
            Message(title="No Glyphs Selected", message="No glyphs are selected. Please select at least one glyph in Font View or Edit View.")
            return

        # Get current master
        current_master = font.selectedFontMaster
        if not current_master:
            Message(title="No Master Selected", message="No master is selected. Please select a master and try again.")
            return

        # Create master list for display
        master_list = "\n".join([f"{i+1}. {master.name}" for i, master in enumerate(font.masters)])
        current_index = font.masters.index(current_master)
        
        # Get source master
        source_master = get_master_selection(
            font,
            "Select Source Master",
            f"Available masters:\n{master_list}\n\nEnter the number of the master to steal metrics FROM:",
            current_index
        )
        if not source_master:
            return
            
        # Get target master
        target_master = get_master_selection(
            font,
            "Select Target Master", 
            f"Available masters:\n{master_list}\n\nEnter the number of the master to apply metrics TO:",
            current_index
        )
        if not target_master:
            return

        print(f"Source master: {source_master.name}")
        print(f"Target master: {target_master.name}")

        # Estimate weight difference
        stem_source = get_master_stem_value(source_master)
        stem_target = get_master_stem_value(target_master)

        if stem_source is not None and stem_target is not None and stem_source > 0:
            delta = stem_target - stem_source
            percent_diff = (delta / stem_source) * 100
            print(f"Using stem values: Source={stem_source}, Target={stem_target}")
        else:
            # Fallback to weight class estimation
            weight_source = get_master_weight_value(source_master)
            weight_target = get_master_weight_value(target_master)
            
            stem_source_approx = weight_source / 5.0
            stem_target_approx = weight_target / 5.0
            
            delta = stem_target_approx - stem_source_approx
            percent_diff = ((weight_target - weight_source) / weight_source) * 100 if weight_source != 0 else 0
            
            print(f"Using weight class approximation: Source={weight_source}, Target={weight_target}")

        # Calculate sidebearing adjustment - APPLY ONLY HALF OF THE PERCENTAGE DIFFERENCE
        original_adjustment = -delta / 2.0
        half_percent_adjustment = original_adjustment * 0.5

        print(f"Estimated weight difference: {percent_diff:.2f}%")
        print(f"Half-percentage adjustment: {half_percent_adjustment:.2f}")

        # Apply metrics to selected glyphs
        processed_count = 0
        for layer in selected_glyphs:
            try:
                glyph = layer.parent
                if not glyph:
                    continue
                    
                # Get layers
                source_layer = glyph.layers[source_master.id]
                target_layer = glyph.layers[target_master.id]
                
                if not source_layer or not target_layer:
                    continue
                
                # Apply adjusted metrics
                new_LSB = source_layer.LSB + half_percent_adjustment
                new_RSB = source_layer.RSB + half_percent_adjustment
                
                target_layer.LSB = new_LSB
                target_layer.RSB = new_RSB
                
                print(f"Adjusted {glyph.name}: LSB={new_LSB:.2f}, RSB={new_RSB:.2f}")
                processed_count += 1
                
            except Exception as e:
                print(f"Error processing {glyph.name if 'glyph' in locals() else 'unknown'}: {e}")

        # Refresh and show completion
        Glyphs.redraw()
        
        if processed_count > 0:
            Message(
                title="Complete",
                message=f"Adjusted {processed_count} glyph(s)\nFrom: {source_master.name}\nTo: {target_master.name}\nAdjustment: {half_percent_adjustment:.1f} units",
                OKButton=None
            )
        else:
            Message(title="No Glyphs Processed", message="No glyphs were processed.")

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        Message(title="Error", message=f"An error occurred: {str(e)}")

# Run the main function
if __name__ == "__main__":
    main()