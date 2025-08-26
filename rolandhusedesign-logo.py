#MenuTitle: Build Roland Huse Design Logo Glyph
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Adds a new logo glyph into apple (uniF8FF) based on provided SVG data.
"""

def drawPenDataInLayer(thisLayer, penData, closePath=True, verbose=False):
    for thisPath in penData:
        if verbose: print()
        pen = thisLayer.getPen()
        pen.moveTo(thisPath[0])
        if verbose: print("MOVETO:", thisPath[0])
        for thisSegment in thisPath[1:]:
            if len(thisSegment) == 2: # lineto (2 coordinates: x,y)
                if verbose: print("LINE:", thisSegment)
                pen.lineTo(thisSegment)
            elif len(thisSegment) == 3: # curveto (3 x/y tuples)
                if verbose: print("CURVE:", thisSegment)
                pen.curveTo(
                    thisSegment[0],
                    thisSegment[1],
                    thisSegment[2]
                )
            else:
                print(f"Path drawing error. Could not process this segment: {thisSegment}\n")
        if closePath:
            pen.closePath()
        pen.endPath()

def drawLogoInLayer(thisLayer, s=1000):
    # Scale factor to convert from SVG viewBox (1692.6) to font UPM (s)
    scale = s / 1692.6
    
    # Convert SVG coordinates to Glyphs coordinates (invert Y axis)
    def svg_to_glyphs(x, y):
        return (x * scale, (1692.6 - y) * scale)
    
    # Create paths from SVG data
    newLogo = []
    
    # Right top element
    path1 = [
        (1434.8, 633.8),    # M1434.8,633.8
        (1488.8, 539.8),    # l54-94
        (1441.8, 513.8),    # l-47-26
        (1413.8, 565.8),    # l-28,52
        (1261.8, 491.8),    # l-152-74
        (1016.8, 539.8),    # l-245,48
        (1026.8, 591.8),    # l10,52
        (1255.8, 547.8),    # l229-44
        (1434.8, 633.8)     # l179,86 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path1])
    
    # Center small element
    path2 = [
        (924.8, 319.8),     # M924.8,319.8
        (863.8, 258.8),     # l-61-61
        (838.8, 306.8),     # l-25,48
        (924.8, 319.8)      # l86,13 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path2])
    
    # Main center complex shape
    path3 = [
        (831.8, 474.8),     # M831.8,474.8
        (885.8, 472.8),     # l54-2
        (883.8, 427.8),     # l-2-45
        (1012.8, 360.8),    # l129-67
        (1200.8, 374.8),    # l188,14
        (1067.8, 173.8),    # l-133-201
        (955.8, 223.8),     # l-112,50
        (843.8, 155.8),     # l-112-68
        (658.8, 308.8),     # l-185,153
        (626.8, 237.8),     # l-32-71
        (676.8, 196.8),     # l50-41
        (687.8, 216.8),     # l11,20
        (730.8, 181.8),     # l43-35
        (690.8, 120.8),     # l-40-61
        (561.8, 222.8),     # l-129,102
        (636.8, 393.8),     # l75,171
        (846.8, 220.8),     # l210-173
        (951.8, 281.8),     # l105,61
        (1051.8, 239.8),    # l100-42
        (1102.8, 316.8),    # l51,77
        (998.8, 308.8),     # l-104-8
        (828.8, 398.8),     # l-170,90
        (831.8, 474.8)      # l3,76 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path3])
    
    # Right middle complex shape
    path4 = [
        (1395.8, 1157.8),   # M1395.8,1157.8
        (1574.8, 1006.8),   # l179-151
        (1553.8, 729.8),    # l-21-277
        (1642.8, 774.8),    # l89,45
        (1666.8, 727.8),    # l24-47
        (1493.8, 641.8),    # l-173-86
        (1520.8, 984.8),    # l27,343
        (1451.8, 1040.8),   # l-69,56
        (1452.8, 727.8),    # l1-313
        (1321.8, 1025.8),   # l-131,298
        (1273.8, 958.8),    # l-48-67
        (1416.8, 675.8),    # l143-283
        (1271.8, 680.8),    # l-145,5
        (1171.8, 864.8),    # l-100,184
        (1153.8, 796.8),    # l-18-68
        (1271.8, 598.8),    # l118-198
        (1143.8, 606.8),    # l-128,8
        (1146.8, 659.8),    # l3,53
        (1171.8, 656.8),    # l25-3
        (1094.8, 788.8),    # l-77,132
        (1154.8, 1003.8),   # l60,215
        (1304.8, 732.8),    # l150-271
        (1329.8, 732.8),    # h25
        (1212.8, 963.8),    # l-118,230
        (1334.8, 1132.8),   # l122,169
        (1400.8, 981.8),    # l66-151
        (1395.8, 1157.8)    # l-4,177 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path4])
    
    # Various smaller elements
    path5 = [
        (1067.8, 669.8),    # M1067.8,669.8
        (1088.8, 621.8),    # l21-48
        (981.8, 574.8),     # l-107-47
        (960.8, 623.8),     # l-21,49
        (1067.8, 669.8)     # l107,46 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path5])
    
    path6 = [
        (808.8, 555.8),     # M808.8,555.8
        (893.8, 533.8),     # l85-22
        (880.8, 482.8),     # l-13-51
        (795.8, 504.8),     # l-85,22
        (808.8, 555.8)      # l13,51 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path6])
    
    path7 = [
        (1023.8, 768.8),    # M1023.8,768.8
        (1061.8, 732.8),    # l38-36
        (937.8, 600.8),     # l-124-132
        (896.8, 633.8),     # l-41,33
        (1023.8, 768.8)     # l127,135 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path7])
    
    # Vertical rectangle
    path8 = [
        (802.8, 619.8),     # M802.8,619.8
        (802.8, 566.8),     # v-53
        (888.8, 566.8),     # h86
        (888.8, 619.8),     # v53
        (802.8, 619.8)      # h-86 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path8])
    
    # Complex shape with lines
    path9 = [
        (695.8, 509.8),     # M695.8,509.8
        (763.8, 377.8),     # l68-132
        (715.8, 352.8),     # l-48-25
        (667.8, 445.8),     # l-48,93
        (615.8, 428.8),     # l-52-17
        (626.8, 397.8),     # l11-31
        (577.8, 378.8),     # l-49-19
        (545.8, 459.8),     # l-32,81
        (695.8, 509.8)      # l150,50 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path9])
    
    # Diagonal shapes
    path10 = [
        (967.8, 849.8),     # M967.8,849.8
        (1013.8, 820.8),    # l46-29
        (926.8, 672.8),     # l-87-148
        (880.8, 698.8),     # l-46,26
        (967.8, 849.8)      # l87,151 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path10])
    
    # Vertical rectangle
    path11 = [
        (818.8, 792.8),     # M818.8,792.8
        (818.8, 653.8),     # v-139
        (871.8, 653.8),     # h53
        (871.8, 792.8),     # v139
        (818.8, 792.8)      # h-53 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path11])
    
    path12 = [
        (923.8, 972.8),     # M923.8,972.8
        (975.8, 958.8),     # l52-14
        (924.8, 784.8),     # l-51-174
        (873.8, 799.8),     # l-51,15
        (923.8, 972.8)      # l50,173 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path12])
    
    # Left side elements
    path13 = [
        (624.8, 669.8),     # M624.8,669.8
        (731.8, 623.8),     # l107-46
        (710.8, 574.8),     # l-21-49
        (603.8, 621.8),     # l-107,47
        (624.8, 669.8)      # l21,48 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path13])
    
    path14 = [
        (667.8, 768.8),     # M667.8,768.8
        (795.8, 633.8),     # l128-135
        (754.8, 600.8),     # l-41-33
        (630.8, 732.8),     # l-124,132
        (667.8, 768.8)      # l37,36 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path14])
    
    path15 = [
        (722.8, 849.8),     # M722.8,849.8
        (811.8, 698.8),     # l89-151
        (765.8, 672.8),     # l-46-26
        (678.8, 820.8),     # l-87,148
        (722.8, 849.8)      # l44,29 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path15])
    
    # Vertical rectangle
    path16 = [
        (818.8, 985.8),     # M818.8,985.8
        (818.8, 823.8),     # v-162
        (871.8, 823.8),     # h53
        (871.8, 985.8),     # v162
        (818.8, 985.8)      # h-53 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path16])
    
    path17 = [
        (768.8, 972.8),     # M768.8,972.8
        (818.8, 799.8),     # l50-173
        (767.8, 784.8),     # l-51-15
        (717.8, 958.8),     # l-51,174
        (768.8, 972.8)      # l51,14 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path17])
    
    # Left top element
    path18 = [
        (257.8, 633.8),     # M257.8,633.8
        (436.8, 547.8),     # l179-86
        (665.8, 591.8),     # l229,44
        (675.8, 539.8),     # l10-52
        (430.8, 491.8),     # l-245-48
        (278.8, 565.8),     # l-152,74
        (250.8, 513.8),     # l-28-52
        (203.8, 539.8),     # l-47,26
        (257.8, 633.8)      # l54,94 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path18])
    
    # Top center decorative element
    path19 = [
        (848.8, 1482.8),    # M848.8,1482.8
        (787.8, 1394.8),    # l-61-88
        (834.8, 1244.8),    # l47-150
        (745.8, 1285.8),    # l-89,41
        (789.8, 1161.8),    # l44-124
        (848.8, 1186.8),    # l59,25
        (905.8, 1164.8),    # l57-22
        (948.8, 1285.8),    # l43,121
        (863.8, 1244.8),    # l-85-41
        (907.8, 1390.8),    # l44,146
        (848.8, 1482.8)     # l-59,92 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path19])
    
    # Large complex shape (left side)
    path20 = [
        (49.8, 774.8),      # M49.8,774.8
        (138.8, 729.8),     # l89-45
        (117.8, 1006.8),    # l-21,277
        (296.8, 1157.8),    # l179,151
        (292.8, 980.8),     # l-4-177
        (358.8, 1131.8),    # l66,151
        (480.8, 962.8),     # l122-169
        (362.8, 732.8),     # l-118-230
        (387.8, 732.8),     # h25
        (537.8, 1003.8),    # l150,271
        (597.8, 788.8),     # l60-215
        (520.8, 656.8),     # l-77-132
        (545.8, 659.8),     # l25,3
        (548.8, 606.8),     # l3-53
        (420.8, 598.8),     # l-128-8
        (538.8, 796.8),     # l118,198
        (520.8, 864.8),     # l-18,68
        (420.8, 680.8),     # l-100-184
        (275.8, 675.8),     # l-145-5
        (418.8, 958.8),     # l143,283
        (370.8, 1025.8),    # l-48,67
        (239.8, 727.8),     # l-131-298
        (240.8, 1040.8),    # l1,313
        (171.8, 984.8),     # l-69-56
        (198.8, 641.8),     # l27-343
        (25.8, 727.8),      # l-173,86
        (49.8, 774.8)       # l24,47 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path20])
    
    # Complex bottom shape
    path21 = [
        (848.8, 1571.8),    # M848.8,1571.8
        (963.8, 1397.8),    # l115-174
        (946.8, 1338.8),    # l-17-59
        (1040.8, 1385.8),   # l94,47
        (940.8, 1103.8),    # l-100-282
        (1024.8, 1064.8),   # l84-39
        (1042.8, 1221.8),   # l18,157
        (1124.8, 1196.8),   # l82-25
        (1081.8, 1254.8),   # l-43,58
        (1171.8, 1294.8),   # l90,40
        (1200.8, 1250.8),   # l29-44
        (1166.8, 1230.8),   # l-34-20
        (1216.8, 1161.8),   # l50-69
        (1249.8, 1194.8),   # l33,33
        (1282.8, 1157.8),   # l33-37
        (1212.8, 1075.8),   # l-70-82
        (1171.8, 1131.8),   # l-41,56
        (1086.8, 1158.8),   # l-85,27
        (1070.8, 982.8),    # l-16-176
        (935.8, 1046.8),    # l-135,64
        (912.8, 984.8),     # l-23-62
        (863.8, 1002.8),    # l-49,18
        (902.8, 1111.8),    # l39,109
        (848.8, 1132.8),    # l-54,21
        (794.8, 1111.8),    # l-53-21
        (830.8, 1002.8),    # l36-109
        (782.8, 984.8),     # l-48-18
        (758.8, 1046.8),    # l-24,62
        (622.8, 982.8),     # l-136-64
        (607.8, 1158.8),    # l-15,176
        (549.8, 1140.8),    # l-58-18
        (502.8, 1075.8),    # l-47-65
        (433.8, 1157.8),    # l-69,82
        (465.8, 1194.8),    # l32,37
        (499.8, 1161.8),    # l34-33
        (549.8, 1230.8),    # l50,69
        (513.8, 1250.8),    # l-36,20
        (543.8, 1294.8),    # l30,44
        (633.8, 1254.8),    # l90-40
        (596.8, 1205.8),    # l-37-49
        (652.8, 1221.8),    # l56,16
        (669.8, 1064.8),    # l17-157
        (758.8, 1103.8),    # l87,39
        (658.8, 1381.8),    # l-100,278
        (753.8, 1336.8),    # l95-45
        (734.8, 1405.8),    # l-19,69
        (848.8, 1571.8)     # l114,166 (close)
    ]
    newLogo.append([svg_to_glyphs(x, y) for x, y in path21])
    
    drawPenDataInLayer(thisLayer, newLogo, closePath=True, verbose=False)
    thisLayer.cleanUpPaths()
    thisLayer.correctPathDirection()
    thisLayer.syncMetrics()
    thisLayer.updateMetrics()

thisFont = Glyphs.font # frontmost font
Glyphs.clearLog() # clears log in Macro window

thisFont.disableUpdateInterface() # suppresses UI updates in Font View
try:
    logoGlyph = thisFont.glyphs["rolandhusedesign"]
    if not logoGlyph:
        print("🆕 Creating new logo glyph...")
        logoGlyph = GSGlyph()
        logoGlyph.name = "rolandhusedesign"
        thisFont.glyphs.append(logoGlyph)
    else:
        print("✅ Updating existing rolandhusedesign glyph...")
    
    print("⚙️ Setting production Unicode, name, category, script...")
    logoGlyph.unicode = "F8FF"
    logoGlyph.productionName = "rolandhusedesign"
    logoGlyph.storeProductionName = True
    logoGlyph.script = "latin"
    logoGlyph.storeScript = True
    logoGlyph.category = "Symbol"
    logoGlyph.storeCategory = True
    
    print("↔️ Setting LSB & RSB = 75")
    logoGlyph.leftMetricsKey = "=75"
    logoGlyph.rightMetricsKey = "=|"
    
    print("✍️ Drawing the new logo on every relevant layer:")
    for thisLayer in logoGlyph.layers:
        print("  ✌️ Layer:", thisLayer.name)
        thisLayer.clear()
        if thisLayer.isMasterLayer or thisLayer.isSpecialLayer:
            drawLogoInLayer(thisLayer, s=thisFont.upm)
    
    thisFont.newTab("/rolandhusedesign")

except Exception as e:
    Glyphs.showMacroWindow()
    print("\n⚠️ Error in script: Add Roland Huse Design Logo to font\n")
    import traceback
    print(traceback.format_exc())
    print()
    raise e
finally:
    thisFont.enableUpdateInterface() # re-enables UI updates in Font View