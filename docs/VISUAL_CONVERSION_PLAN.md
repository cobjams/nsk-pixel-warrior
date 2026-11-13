# Shattered Pixel Dungeon Sci-Fi / Industrial Mod — Visual Conversion Plan & Style Guide

> **Living Document for AI Agents & Contributors**
> Always read this file and [`docs/texture_reference.json`](./texture_reference.json) before modifying any textures. Update the **Phase Progress Tracker** below whenever an asset or batch is completed.

---

## 1. Core Creative Direction & Tone

- **Genre & Tone:** Lighthearted Survival Horror meets Mundane Corporate Bureaucracy (with subtle sci-fi trope nods: *Half-Life* Black Mesa facilities, *Alien* Nostromo industrial grit, *Portal* OSHA apathy, *Space Quest* janitorial heroics).
- **Setting:** A sprawling, horizontal ball-bearing manufacturing plant where reckless R&D experimentation with an **Infinite Precision Ball Bearing** has ruptured space-time and spilled mutagenic chemicals across the facility.
- **Playable Crew:** Six low-level blue-collar/support employees stuck cleaning up management's disaster.

---

## 2. Finalized 6-Class Roster & Visual Identity

Class and subclass names are intentionally concise (1 word, or 2 short words for `Lab Tech`) to fit UI buttons, badges, and status tabs cleanly while mapping 1-to-1 to Shattered Pixel Dungeon's mechanics:

| Engine ID | Sprite Sheet | Mod Class Name | Subclasses | Starting Gear & Silhouette | Head / Accessory (`y % 15 < 8`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `warrior` | `sprites/warrior.png` | **Janitor** | `Scrubber` / `Polisher` | Broken Safety Badge, Rusty Pipe Wrench | Blue/grey trucker cap with visor, scruffy 5-o'clock shadow |
| `mage` | `sprites/mage.png` | **Lab Tech** | `Mixer` / `Toxicologist` | Industrial Chemical Sprayer | Teal/green safety goggles or half-face respirator, messy hair |
| `rogue` | `sprites/rogue.png` | **Security Guard** | `Enforcer` / `Patrolman` | CCTV Jammer, Screwdriver | Peaked security service cap with visor, veteran mustache |
| `huntress` | `sprites/huntress.png` | **Exterminator** | `Sharpshooter` / `Groundskeeper` | Pneumatic Nailgun, Work Gloves | Yellow/orange pest-control visor cap, protective ear/eye gear |
| `duelist` | `sprites/duelist.png` | **Mechanic** | `Foreman` / `Ergonomist` | Soldering Iron, Heavy Bolts | Welding goggles pushed up on forehead / bandana, grease smudge |
| `cleric` | `sprites/cleric.png` | **Supervisor** | `Auditor` / `Inspector` | Employee Handbook, Heavy Flashlight | Neat side-part / glasses, union headset or safety helmet |

---

## 3. Hero Sprite Sheet Technical Specification (`256x128`, Mode `P`)

All 6 hero sheets (`warrior.png`, `mage.png`, `rogue.png`, `huntress.png`, `duelist.png`, `cleric.png`) share identical geometry defined in [`HeroSprite.java`](../core/src/main/java/com/shatteredpixel/shatteredpixeldungeon/sprites/HeroSprite.java):

- **Canvas Dimensions:** `256 x 128` pixels, **Indexed Color (`P`-mode)** with transparency at palette index `0`.
- **Frame Size:** `12 x 15` pixels (`FRAME_WIDTH = 12`, `FRAME_HEIGHT = 15`), **21 frames per row** (`x = 0..251`).
- **Armor Tiers (7 rows, `y = 0..104`):**
  - **Row 0 (`y = 0..14`) — Tier 0 (Unarmored):** Standard grey/white undershirt & dark work slacks.
  - **Row 1 (`y = 15..29`) — Tier 1 (`cotton coveralls`):** Classic institutional navy/slate-blue janitor jumpsuit.
  - **Row 2 (`y = 30..44`) — Tier 2 (`heavy-duty apron`):** Brown/ochre chemical-resistant rubberized apron & thick gloves.
  - **Row 3 (`y = 45..59`) — Tier 3 (`kevlar vest`):** Steel-grey/olive ballistic & puncture-resistant maintenance vest.
  - **Row 4 (`y = 60..74`) — Tier 4 (`riot gear`):** Dark charcoal/cobalt polycarbonate security plating with shoulder pads.
  - **Row 5 (`y = 75..89`) — Tier 5 (`hazmat suit`):** High-visibility OSHA Hazard Yellow (`#F2C12E`) / Safety Orange sealed containment suit.
  - **Row 6 (`y = 90..104`) — Tier 6 (Class Rig):** Unique per class (`janitor's exoskeleton`, `lab tech's coat`, `security guard's uniform`, `exterminator's jacket`, `mechanic's rig`, `supervisor's vest`).
- **Frame-by-Frame Anatomy (12px `HeroSprite` frames):**
  - **Frames 0–1 (`x = 0..23`):** `idle` (Frame 0 faces right; Frame 1 mirrors the head `y % 15 < 8` horizontally to look back).
  - **Frames 2–7 (`x = 24..95`):** `run` cycle. **Frames 4 (`x = 48..59`) and 7 (`x = 84..95`) shift the head 1 pixel lower (`dy = +1`)** for the run bob.
  - **Frames 8–12 (`x = 96..155`):** `die` animation (greyscale skull/ghost). **Never tint or alter these frames across armor tiers.**
  - **Frames 13–15 (`x = 156..191`):** `attack` / `zap` (Frame 13 shifts head `dx = -1`; Frame 14 `dx = 0`; Frame 15 shifts head `dx = +1`).
  - **Frames 16–17 (`x = 192..215`):** `operate` (head tilted down 1px).
  - **Frame 18 (`x = 216..227`):** `fly` / leap.
  - **Frames 19–20 (`x = 228..251`):** `read` requisition form/manual.

---

## 4. Master Factory Color Palette System

Use these reference hex ramps when constructing or re-paletting assets in **Pixel Workbench** (`generate_color_ramp` / `replace_color`):

### Global Industrial & OSHA Accents
- **OSHA Hazard Yellow:** `#6E4C08` (shadow) $\rightarrow$ `#B88414` (mid) $\rightarrow$ `#F2C12E` (base) $\rightarrow$ `#FFF08A` (highlight)
- **Safety Orange:** `#6B2307` $\rightarrow$ `#A83E10` $\rightarrow$ `#E86A17` $\rightarrow$ `#FFA756`
- **Biohazard / Coolant Green:** `#164214` $\rightarrow$ `#2D8A22` $\rightarrow$ `#58D62E` $\rightarrow$ `#B4FF8C`
- **High-Voltage / Arc Cyan:** `#0F3847` $\rightarrow$ `#1A7A99` $\rightarrow$ `#2CE8F5` $\rightarrow$ `#B8FFFF`
- **Security Laser / Alarm Red:** `#4D0A0A` $\rightarrow$ `#991717` $\rightarrow$ `#E02424` $\rightarrow$ `#FF8080`
- **Brushed Steel / Conduit:** `#22262B` $\rightarrow$ `#454D57` $\rightarrow$ `#7A8694` $\rightarrow$ `#B8C4D1`

### Sector Environment Palettes
1. **Sector 1 — Offices (`tiles_sewers.png`, `water0.png`):**
   - Warm beige/cream institutional VCT linoleum (`#B5A88F`, `#CDC0A6`, `#E2D6BE`), smooth continuous bland beige drywall (`#8C7F6E`, `#B3A694`, `#D9CCBA`) without vertical tile borders, dark brown commercial cove base molding (`#4E3524`), chemical coolant runoff (`water0.png`), straight-sided blue steel industrial chemical drum (`FLAT_REGION_DECO`).
2. **Sector 2 — Screw Machine Dept (`tiles_prison.png`, `water1.png`):**
   - Oil-stained dark concrete (`#33363B`, `#4F545C`), heavy riveted iron bulkheads with hazard stripes, dark amber/brown cutting oil (`water1.png`).
3. **Sector 3 — Grind Dept & Subterranean Ducts (`tiles_caves.png`, `water2.png`):**
   - Industrial steel grating & oxidized metallic dust (`#423833`, `#6B5B52`, `#8C7A6B`), galvanized ventilation shafts, abrasive grey-cyan coolant sludge (`water2.png`).
4. **Sector 4 — Heat-Treat Dept (`tiles_city.png`, `water3.png`):**
   - Refractory furnace brick & brass/copper manifolds (`#52291D`, `#8C482B`, `#C97A3E`), glowing induction coils, glowing orange/amber quench oil (`water3.png`).
5. **Sector 5 — Precision Assembly & R&D Labs (`tiles_halls.png`, `water4.png`):**
   - Cleanroom white/sterile titanium panels (`#5E6472`, `#9EA8B8`, `#D6E0EB`) fractured by anti-friction purple/magenta space-time rifts (`#4A154B`, `#9B26B6`, `#E066FF`), cryogenic/void liquid (`water4.png`).

---

## 5. Phased Execution & Progress Tracker

### Phase 0: Reference Automation, Class Unification & Style Guide
- [x] Unify the 6 playable classes (`Janitor`, `Lab Tech`, `Custodian`, `Exterminator`, `Mechanic`, `Supervisor`) and 12 subclasses across `actors.properties`, `items.properties`, `misc.properties`, and `AGENTS.md`.
- [x] Clean up 245 lingering RPG class/subclass mentions in `actors.properties` ability/spell/talent descriptions.
- [x] Expand [`docs/texture_reference.json`](./texture_reference.json) with complete item coordinates (`items.png`), mini-icon coordinates (`item_icons.png` 128x64), mob sprite metadata + lore names, hero 12x15 frame anatomy, terrain features, UI sheets, and effects.
- [x] Document master visual plan and style guide in `docs/VISUAL_CONVERSION_PLAN.md`.

### Phase 1: The Playable Crew (`sprites/warrior.png` .. `cleric.png`, `avatars.png`)
- [x] **1.1** `sprites/warrior.png` (**Janitor**) + shared PPE Tiers 0–5 body template
- [x] **1.2** `sprites/mage.png` (**Lab Tech**)
- [x] **1.3** `sprites/rogue.png` (**Security Guard**)
- [x] **1.4** `sprites/huntress.png` (**Exterminator**)
- [x] **1.5** `sprites/duelist.png` (**Mechanic**)
- [x] **1.6** `sprites/cleric.png` (**Supervisor**)
- [x] **1.7** `sprites/avatars.png` (24x32 character select & surface portraits) & `sprites/pet.png`

### Phase 2: Factory Environments, Terrain Features & Liquids (`environment/*.png`)
- [x] **2.1** Sector 1: `tiles_sewers.png`, `water0.png`, `custom_tiles/sewer_boss.png` (Offices)
- [ ] **2.2** Sector 2: `tiles_prison.png`, `water1.png`, `custom_tiles/prison_quest.png`, `custom_tiles/prison_exit.png` (Screw Machine Dept)
- [ ] **2.3** Sector 3: `tiles_caves.png`, `tiles_caves_crystal.png`, `tiles_caves_gnoll.png`, `water2.png`, `custom_tiles/caves_*.png` (Grind Dept & Subterranean Ducts)
- [ ] **2.4** Sector 4: `tiles_city.png`, `water3.png`, `custom_tiles/city_*.png` (Heat-Treat Dept)
- [ ] **2.5** Sector 5: `tiles_halls.png`, `water4.png`, `custom_tiles/halls_special.png` (Precision Assembly & R&D Labs)
- [ ] **2.6** `terrain_features.png` (Industrial traps, chemical spills/canisters, trash/mold overgrowth)

### Phase 3: Items, Tools, PPE & Consumables (`sprites/items.png`, `item_icons.png`, `amulet.png`)
- [ ] **3.1** Rows 1–4: Placeholders, Company Scrip (`GOLD`), Lockers/Crates (`CHEST`), Keycards (`KEY`), & **Infinite Precision Ball Bearing** (`AMULET` + `sprites/amulet.png`)
- [ ] **3.2** Rows 5–12: Melee Maintenance Tools (Mops, Wrenches, Soldering Irons, Crowbars) & Thrown Hardware (Bolts, Bearings, Sawblades)
- [ ] **3.3** Rows 13–14: PPE Coveralls & Class Rigs
- [ ] **3.4** Rows 15–20: Chemical Applicators (Wands), Security Badges (Rings), & Workplace Artifacts (Employee Handbook, Lunchbox, etc.)
- [ ] **3.5** Rows 21–32: Requisition Forms (Scrolls), Solvents/Sprays (Potions), Break-Room Snacks (Food), Bombs, Bags & Manuals + `sprites/item_icons.png`

### Phase 4: Enemies, Mutated Riffraff, NPCs & Bosses (`sprites/*.png`)
- [ ] **4.1** NPCs & Interactive Objects (`shopkeeper.png`, `ghost.png`, `wandmaker.png`, `blacksmith.png`, `demon.png`, `ratking.png`, `sheep.png`, `wards.png`, `red_sentry.png`)
- [ ] **4.2** Sector 1 Enemies & Boss (`rat.png`, `snake.png`, `gnoll.png`, `crab.png`, `slime.png`, `goo.png`)
- [ ] **4.3** Sector 2 Enemies & Boss (`skeleton.png`, `thief.png`, `swarm.png`, `dm100.png`, `guard.png`, `necromancer.png`, `tengu.png`)
- [ ] **4.4** Sector 3 Enemies & Boss (`bat.png`, `brute.png`, `shaman.png`, `spinner.png`, `dm200.png`, `dm300.png`, `pylon.png`, crystal/fungal/gnoll sub-quest sprites)
- [ ] **4.5** Sector 4 Enemies & Boss (`elemental.png`, `warlock.png`, `monk.png`, `golem.png`, `statue.png`, `ghoul.png`, `undead.png`, `king.png`)
- [ ] **4.6** Sector 5 Enemies & Final Boss (`succubus.png`, `eye.png`, `scorpio.png`, `ripper.png`, `spawner.png`, `larva.png`, `yog.png`, `yog_fists.png`)

### Phase 5: UI Chrome, HUD, Effects & Splash Art (`interfaces/`, `effects/`, `splashes/`)
- [ ] **5.1** Core UI Panels (`chrome.png`, `status_pane.png`, `toolbar.png`, `menu_pane.png`, `menu_button.png`, `boss_hp.png`, `banners.png`)
- [ ] **5.2** Icons, Buffs & Badges (`icons.png`, `hero_icons.png`, `talent_icons.png`, `buffs.png`, `large_buffs.png`, `badges.png`, `locked_badge.png`)
- [ ] **5.3** Visual Effects (`effects.png`, `specks.png`, `spell_icons.png`, `text_icons.png`, `fireball-*.png`)
- [ ] **5.4** Title & Splash Art (`arcs1.png`, `arcs2.png`, `surface.png`, `splashes/title/*.png`, `splashes/*.jpg`)

---

## 6. Mandatory Pixel Workbench Workflow for Agents

Whenever editing any PNG in `core/src/main/assets/`:
1. **Inspect & Checkpoint:** Open the sprite in **Pixel Workbench** (`init_workspace` / `inspect_sprite`) and call `checkpoint_workspace`.
2. **Preserve Mode & Dimensions:** Keep `P`-mode sprites in `P`-mode (edit palette indices directly or use `replace_color` / `apply_ascii_grid`) and **never** alter canvas dimensions or frame bounding boxes.
3. **Validate:** Run `regression_report` and `inspect_animation` (for multi-frame character sheets) and verify with `"include_preview_image": true`.
4. **Update Docs:** Mark completed items in this file and update `"status": "done"` in [`docs/texture_reference.json`](./texture_reference.json).
