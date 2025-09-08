#MenuTitle: Roland Huse Font Info Prep
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Prepare Roland Huse Font Info
"""

from datetime import datetime, time

thisFont = Glyphs.font # frontmost font
selectedLayers = thisFont.selectedLayers # active layers of selected glyphs
Glyphs.clearLog() # clears log in Macro window

removableParameters = (
    "glyphOrder",
    "panose",
    "unicodeRanges",
    "macintoshFONDFamilyID",
    "macintoshFONDName",
    "openTypeHeadFlags",
    "descriptions",
    "licenses",
    "licenseURL",
    "sampleTexts",
    "uniqueID",
    "versionString",
    "openTypeOS2FamilyClass",
    "fsType",
    "vendorID",
    "blueFuzz",
    "blueScale",
    "blueShift",
    "postscriptForceBold",
    "postscriptIsFixedPitch",
    "postscriptUniqueID",
    "trademarks",
    "year",
)
removableProperties = (
    "postscriptFontName",
    "postscriptFullNames",
    "descriptions",
    "sampleTexts",
    "trademarks",
    "uniqueID",
    GSPropertyNameLicensesKey,
    GSPropertyNameLicenseURLKey,
)
setProperties = {
    GSPropertyNameVendorIDKey: "RHD",
    GSPropertyNameCopyrightsKey: "© 2025 Roland Huse Design. All rights reserved.",
    GSPropertyNameTrademarksKey: f"{thisFont.familyName} is a trademark of Roland Huse Design.",
    GSPropertyNameVersionStringKey: "Version %d.%03d",
    GSPropertyNameManufacturersKey: "Roland Huse Design",
    GSPropertyNameManufacturerURLKey: "https://www.rolandhuse.com/",
}
setParameters = {
    "Write DisplayStrings": 0,
    "Write lastChange": 0,
    "Export Mac Name Table Entries": 0,
    "Disable Subroutines": 1,
    "Use Typo Metrics": 1,
}

thisFont.disableUpdateInterface() # suppresses UI updates in Font View
try:
    # clear out parameters
    for parameterName in removableParameters:
        while thisFont.customParameters[parameterName]:
            del thisFont.customParameters[parameterName]
    
    # clear out properties
    for propertyName in removableProperties:
        while thisFont.properties[propertyName]:
            thisFont.removeObjectFromProperties_(thisFont.properties[propertyName])
        for thisInstance in thisFont.instances:
            while thisInstance.properties[propertyName]:
                thisInstance.removeObjectFromProperties_(thisInstance.properties[propertyName])
    
    # set version to 2.001
    thisFont.versionMajor = 2
    thisFont.versionMinor = 1
    
    # set font date to today noon
    today = datetime.now().date()
    noon = time(12, 0)
    thisFont.date = datetime.combine(today, noon)
    
    # update OT features
    thisFont.updateFeatures()
    
    # overwrite some properties
    for key in setProperties.keys():
        value = setProperties[key]
        thisFont.setProperty_value_languageTag_(key, value, None)
    
    for key in setParameters.keys():
        value = setParameters[key]
        thisFont.customParameters[key] = value

        
except Exception as e:
    Glyphs.showMacroWindow()
    print("\n⚠️ Error in script: Roland Huse Font Info Prep\n")
    import traceback
    print(traceback.format_exc())
    print()
    raise e
finally:
    thisFont.enableUpdateInterface() # re-enables UI updates in Font View