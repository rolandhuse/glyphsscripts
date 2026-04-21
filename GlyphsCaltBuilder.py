# GlyphsCaltBuilder.py  —  paste into Glyphs 3 Macro Panel and run
# Builds: init feature, fina feature, calt feature (SS cycling only, no UC/LC swap)
# Auto-detects .ss01/.ss02/... and .init/.fina per master
# Writes classes directly to Font Info > Classes
# Writes features directly to Font Info > Features

import re

font = Glyphs.font
if not font:
    print("No font open.")
else:
    master = font.selectedFontMaster
    print(f"Building features for master: {master.name}\n")

    # ── helpers: upsert class / feature into font ────────────────────────────
    def set_class(name, members):
        """Create or overwrite a glyph class in Font Info > Classes."""
        code = " ".join(members)
        for cls in font.classes:
            if cls.name == name:
                cls.code = code
                return
        cls = GSClass()
        cls.name = name
        cls.code = code
        font.classes.append(cls)

    def set_feature(tag, code):
        """Create or overwrite a feature in Font Info > Features."""
        for feat in font.features:
            if feat.name == tag:
                feat.code = code
                return
        feat = GSFeature()
        feat.name = tag
        feat.code = code
        font.features.append(feat)

    # ── 1. Collect glyph names present in this master ────────────────────────
    def has_layer(glyph_name):
        g = font.glyphs[glyph_name]
        if not g or not g.export:
            return False
        layer = g.layers[master.id]
        return layer and (layer.paths or layer.components)

    all_names = [g.name for g in font.glyphs if has_layer(g.name)]

    # ── 2. Detect suffix groups ──────────────────────────────────────────────
    base_to_suffixes = {}
    for name in all_names:
        if "." in name:
            dot = name.index(".")
            base = name[:dot]
            suffix = name[dot:]
            base_to_suffixes.setdefault(base, set()).add(suffix)

    all_ss_suffixes = sorted(
        {s for sfxs in base_to_suffixes.values() for s in sfxs
         if re.fullmatch(r'\.ss\d{2}', s)},
        key=lambda s: int(s[3:])
    )
    print(f"SS suffixes found: {all_ss_suffixes or 'none'}")

    # ── 3. All base glyphs (letters) ─────────────────────────────────────────
    # A "base" is any glyph without a dot suffix
    base_glyphs = [n for n in all_names if "." not in n]

    # Bases that have at least one SS variant
    bases_with_ss = [b for b in base_glyphs
                     if any(has_layer(b + s) for s in all_ss_suffixes)]
    bases_without_ss = [b for b in base_glyphs if b not in bases_with_ss]

    def has_variant(base, suffix):
        return suffix in base_to_suffixes.get(base, set()) and has_layer(base + suffix)

    def has_init(base): return has_variant(base, ".init")
    def has_fina(base): return has_variant(base, ".fina")

    bases_with_init = [b for b in base_glyphs if has_init(b)]
    bases_with_fina = [b for b in base_glyphs if has_fina(b)]

    # ── 4. All cycling glyphs (bases + all their SS variants) ────────────────
    all_ss_forms = [b + s for b in bases_with_ss for s in all_ss_suffixes
                    if has_layer(b + s)]
    all_cycling = sorted(set(base_glyphs) | set(all_ss_forms))

    # Non-cycling glyphs (punct, marks, ligatures, .init/.fina forms, etc.)
    all_letter_set = set(base_glyphs) | set(all_ss_forms)
    init_fina_forms = (
        [b + ".init" for b in bases_with_init] +
        [b + ".fina" for b in bases_with_fina]
    )
    not_letter = [n for n in all_names
                  if n not in all_letter_set and n not in init_fina_forms]

    # ── 5. Build per-SS-level class data ─────────────────────────────────────
    # For each suffix level, which bases have that variant?
    ss_level_data = []
    for sfx in all_ss_suffixes:
        bases_at_level = [b for b in bases_with_ss if has_layer(b + sfx)]
        if bases_at_level:
            ss_forms = [b + sfx for b in bases_at_level]
            ss_level_data.append((sfx, bases_at_level, ss_forms))

    # ── 6. Write glyph classes to Font Info > Classes ───────────────────────
    set_class("AllBase",     base_glyphs)
    set_class("Base_withSS", bases_with_ss)
    set_class("Base_noSS",   bases_without_ss)

    for sfx, bases_at_level, ss_forms in ss_level_data:
        tag = sfx[1:].upper()  # ".ss01" → "SS01"
        set_class(f"Base_with{tag}", bases_at_level)
        set_class(f"{tag}_all",      ss_forms)

    if bases_with_init:
        set_class("Base_withInit", bases_with_init)
        set_class("Init_all",      [b + ".init" for b in bases_with_init])
    if bases_with_fina:
        set_class("Base_withFina", bases_with_fina)
        set_class("Fina_all",      [b + ".fina" for b in bases_with_fina])

    # Base_backtrack: AllBase + .init forms, so glyph after .init enters cycle
    if bases_with_init:
        set_class("Base_backtrack", base_glyphs + [b + ".init" for b in bases_with_init])
        base_bt = "@Base_backtrack"
    else:
        base_bt = "@AllBase"

    set_class("AllCycling", all_cycling)
    set_class("NotLetter",  not_letter)

    print(f"  Classes written: {len(font.classes)} total in font")

    # ── 7. Build feature code strings ────────────────────────────────────────
    def L(*args):
        return "\n".join(args)

    def emit_chain(lookup_name, backtrack_class, sub_lookup):
        rules = []
        for n in range(4, 0, -1):
            nl = " ".join(["@NotLetter"] * n)
            rules.append(f"    sub {backtrack_class} {nl} @AllCycling' lookup {sub_lookup};")
        rules.append(f"    sub {backtrack_class} @AllCycling' lookup {sub_lookup};")
        return L(
            f"lookup {lookup_name} {{",
            *rules,
            f"}} {lookup_name};"
        )

    # ── init feature ─────────────────────────────────────────────────────────
    if bases_with_init:
        set_feature("init", "sub @Base_withInit' by @Init_all;")
        print("  Feature written: init")

    # ── fina feature ─────────────────────────────────────────────────────────
    if bases_with_fina:
        set_feature("fina", "sub @Base_withFina' by @Fina_all;")
        print("  Feature written: fina")

    # ── calt feature ─────────────────────────────────────────────────────────
    calt_blocks = []

    for i, (sfx, bases_at_level, ss_forms) in enumerate(ss_level_data):
        tag = sfx[1:].upper()

        # sub lookups
        calt_blocks.append(L(
            f"lookup sub_Base_to_{tag} {{",
            f"    sub @Base_with{tag} by @{tag}_all;",
            f"}} sub_Base_to_{tag};"
        ))

        if i + 1 < len(ss_level_data):
            next_sfx, _, _ = ss_level_data[i + 1]
            next_tag = next_sfx[1:].upper()
            shared = [b for b in bases_at_level if has_layer(b + next_sfx)]
            if shared:
                sub_rules = "\n".join(
                    f"    sub {b + sfx} by {b + next_sfx};" for b in shared
                )
                calt_blocks.append(L(
                    f"lookup sub_{tag}_to_{next_tag} {{",
                    sub_rules,
                    f"}} sub_{tag}_to_{next_tag};"
                ))

        calt_blocks.append(L(
            f"lookup sub_{tag}_to_Base {{",
            f"    sub @{tag}_all by @Base_with{tag};",
            f"}} sub_{tag}_to_Base;"
        ))

    calt_blocks.append("")  # spacer before chain lookups

    for i, (sfx, bases_at_level, ss_forms) in enumerate(ss_level_data):
        tag = sfx[1:].upper()
        calt_blocks.append(emit_chain(f"chain_Base_to_{tag}", base_bt, f"sub_Base_to_{tag}"))

        if i + 1 < len(ss_level_data):
            next_sfx, _, _ = ss_level_data[i + 1]
            next_tag = next_sfx[1:].upper()
            shared = [b for b in bases_at_level if has_layer(b + next_sfx)]
            if shared:
                calt_blocks.append(emit_chain(f"chain_{tag}_to_{next_tag}", f"@{tag}_all", f"sub_{tag}_to_{next_tag}"))

        calt_blocks.append(emit_chain(f"chain_{tag}_to_Base", f"@{tag}_all", f"sub_{tag}_to_Base"))

    # feature block (lookup refs only — lookups are defined above in same feature)
    feature_lines = []
    for i, (sfx, bases_at_level, ss_forms) in enumerate(ss_level_data):
        tag = sfx[1:].upper()
        feature_lines.append(f"    lookup chain_Base_to_{tag};")
        if i + 1 < len(ss_level_data):
            next_sfx, _, _ = ss_level_data[i + 1]
            next_tag = next_sfx[1:].upper()
            shared = [b for b in bases_at_level if has_layer(b + next_sfx)]
            if shared:
                feature_lines.append(f"    lookup chain_{tag}_to_{next_tag};")
        feature_lines.append(f"    lookup chain_{tag}_to_Base;")

    calt_code = "\n\n".join(calt_blocks) + "\n\n" + "\n".join(feature_lines)
    set_feature("calt", calt_code)
    print("  Feature written: calt")

    print("\nDone. Open Font Info > Classes and Features to review.")

