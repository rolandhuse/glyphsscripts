# Reorder OpenType features in Glyphs App to place ss01 before liga
font = Glyphs.font

if font:
    # Get the list of features
    features = font.features
    
    # Find ss01 and liga features
    ss01_feature = None
    liga_feature = None
    ss01_index = -1
    liga_index = -1
    
    for i, feature in enumerate(features):
        if feature.name == "ss01":
            ss01_feature = feature
            ss01_index = i
        elif feature.name == "liga":
            liga_feature = feature
            liga_index = i
    
    # Check if both features exist
    if ss01_feature and liga_feature:
        if ss01_index > liga_index:
            # Remove both features
            features.pop(ss01_index)
            features.pop(liga_index if liga_index < ss01_index else liga_index - 1)
            
            # Reinsert liga first, then ss01 before it
            features.insert(liga_index, liga_feature)
            features.insert(liga_index, ss01_feature)
            
            print("Reordered: ss01 now before liga")
        else:
            print("No reordering needed: ss01 is already before liga")
    else:
        missing = []
        if not ss01_feature:
            missing.append("ss01")
        if not liga_feature:
            missing.append("liga")
        print(f"Cannot reorder: Missing feature(s): {', '.join(missing)}")
else:
    print("No font open in Glyphs")