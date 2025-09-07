#MenuTitle: Adjust Metrics by percentage in selected glyohs
# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

class SideBearingsAdjuster(object):
    def __init__(self):
        # Create the dialog window
        self.w = FloatingWindow((300, 180), "Adjust Side Bearings")
        
        # Add text and input fields
        self.w.text = TextBox((20, 20, -20, 20), "Adjust side bearings by percentage:")
        self.w.lsb_label = TextBox((20, 60, 100, 20), "LSB (%):")
        self.w.lsb_input = EditText((120, 55, 60, 25), "0")
        self.w.rsb_label = TextBox((20, 95, 100, 20), "RSB (%):")
        self.w.rsb_input = EditText((120, 90, 60, 25), "0")
        
        # Add apply button
        self.w.apply_button = Button((20, 135, -20, 25), "Apply to Selected Glyphs", callback=self.apply_adjustment)
        
        # Open the window
        self.w.open()
    
    def apply_adjustment(self, sender):
        try:
            # Get the percentage values from input fields
            lsb_percentage = float(self.w.lsb_input.get())
            rsb_percentage = float(self.w.rsb_input.get())
            
            # Get the current font and selected glyphs
            font = Glyphs.font
            selected_glyphs = font.selectedLayers
            
            # Apply the adjustment to each selected glyph
            for layer in selected_glyphs:
                glyph = layer.parent
                
                # Adjust LSB
                if lsb_percentage != 0:
                    current_lsb = layer.LSB
                    adjustment = current_lsb * (lsb_percentage / 100)
                    layer.LSB = current_lsb + adjustment
                
                # Adjust RSB
                if rsb_percentage != 0:
                    current_rsb = layer.RSB
                    adjustment = current_rsb * (rsb_percentage / 100)
                    layer.RSB = current_rsb + adjustment
                
                print(f"Adjusted {glyph.name}: LSB {lsb_percentage}%, RSB {rsb_percentage}%")
            
            # Update the font view
            font.enableUpdateInterface()
            
        except ValueError:
            # Handle invalid input
            Message("Please enter valid numbers for percentages", title="Input Error")
        except Exception as e:
            # Handle other errors
            Message(f"An error occurred: {str(e)}", title="Error")

# Run the script
SideBearingsAdjuster()