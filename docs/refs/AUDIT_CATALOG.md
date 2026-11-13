# Factory Reference Library — Audit Catalog

Consolidated quality verification catalog for all 7 target visual reference folders supporting [`docs/VISUAL_CONVERSION_PLAN.md`](../VISUAL_CONVERSION_PLAN.md).

## Verification Summary

- **Total Target Folders:** 7 / 7
- **Total Verified Images:** 46 (7.08 MB total)
- **Automated Checks:** All 46 files pass `PIL.Image.verify()` and `load()`, have non-zero dimensions `<= 1024px`, are `>= 10 KB` (no empty/stub downloads), and match their folder `INDEX.md` 1-to-1.
- **Visual Spot-Checks:** 26 images visually inspected via `read_file` across all 7 folders; all match the retro-industrial / survival-horror factory theme with no blank, watermarked-diagram, or off-topic files.

| Folder | File Count | Status | Target Phase (`VISUAL_CONVERSION_PLAN.md`) | Gathering Worker |
| :--- | :---: | :--- | :--- | :--- |
| [`sector2_screw_machine/`](sector2_screw_machine/INDEX.md) | 6 | Verified (PIL + Visual) | [Phase 2.2](../VISUAL_CONVERSION_PLAN.md) | `refs-sectors-2-3` |
| [`sector3_grind_ducts/`](sector3_grind_ducts/INDEX.md) | 6 | Verified (PIL + Visual) | [Phase 2.3](../VISUAL_CONVERSION_PLAN.md) | `refs-sectors-2-3` |
| [`sector4_heat_treat/`](sector4_heat_treat/INDEX.md) | 6 | Verified (PIL + Visual) | [Phase 2.4](../VISUAL_CONVERSION_PLAN.md) | `refs-sectors-4-5` |
| [`sector5_assembly_rnd/`](sector5_assembly_rnd/INDEX.md) | 6 | Verified (PIL + Visual) | [Phase 2.5](../VISUAL_CONVERSION_PLAN.md) | `refs-sectors-4-5` |
| [`items_tools_ppe/`](items_tools_ppe/INDEX.md) | 10 | Verified (PIL + Visual) | [Phase 3](../VISUAL_CONVERSION_PLAN.md) | `refs-items-ppe` |
| [`mobs_npcs_bosses/`](mobs_npcs_bosses/INDEX.md) | 6 | Verified (PIL + Visual) | [Phase 4](../VISUAL_CONVERSION_PLAN.md) | `refs-mobs-ui` |
| [`ui_hud_effects/`](ui_hud_effects/INDEX.md) | 6 | Verified (PIL + Visual) | [Phase 5](../VISUAL_CONVERSION_PLAN.md) | `refs-mobs-ui` |
| **Total** | **46** | **All Verified** | **Phases 2.2 – 5** | **4 workers** |

---

## Complete Reference Catalog

### Sector 2 — Screw Machine Dept ([`sector2_screw_machine/INDEX.md`](sector2_screw_machine/INDEX.md))

**Target Phase:** [Phase 2.2](../VISUAL_CONVERSION_PLAN.md) | **Files:** 6

| Reference Image | Dimensions & Format | Target Game Assets | Visual Notes | Source |
| :--- | :--- | :--- | :--- | :--- |
| [`floor_oil_stained_concrete.jpg`](sector2_screw_machine/floor_oil_stained_concrete.jpg) | 797x1024 (JPEG/RGB, 340.8 KB) | `environment/tiles_prison.png` (floor tiles) | Top-down grey concrete slab with dark motor/machining oil puddles, iridescent sheen, and soaked stain halo (`#33363B` / `#4F545C` base concrete with dark oil contrast). | [Source](https://commons.wikimedia.org/wiki/File:2006-10-24_oil-puddle.jpg) |
| [`wall_riveted_steel_hazard.jpg`](sector2_screw_machine/wall_riveted_steel_hazard.jpg) | 384x672 (JPEG/RGB, 116.6 KB) | `environment/tiles_prison.png` (bulkhead walls, OSHA trim) | Vertical riveted dark steel plates painted with weathered OSHA yellow-and-black diagonal hazard stripes (`#6E4C08` -> `#F2C12E` over dark iron). | [Source](https://images.stockcake.com/public/2/0/e/20e5c6f7-1794-40d2-90ef-b96287a2e500_large/industrial-hazard-pattern-stockcake.jpg) |
| [`prop_cnc_screw_machine.jpg`](sector2_screw_machine/prop_cnc_screw_machine.jpg) | 1024x768 (JPEG/RGB, 193.1 KB) | `environment/tiles_prison.png` (wall/room machinery props), `environment/custom_tiles/prison_quest.png` | Close-up inside a CNC Swiss-type automatic screw machine showing spindle, gang tooling, articulated blue/orange coolant nozzles, and sheet-metal chip tray. | [Source](https://commons.wikimedia.org/wiki/File:CNC_Swiss_turn_001.jpg) |
| [`liquid_amber_cutting_oil.jpg`](sector2_screw_machine/liquid_amber_cutting_oil.jpg) | 960x720 (JPEG/RGB, 178.0 KB) | `environment/water1.png` (amber cutting oil pools) | Concentrated stream of translucent amber-brown neat cutting oil pouring from a flat nozzle onto a machined steel spline shaft. | [Source](https://commons.wikimedia.org/wiki/File:Milling_splineprofile.JPG) |
| [`door_chainlink_tool_crib.jpg`](sector2_screw_machine/door_chainlink_tool_crib.jpg) | 650x682 (JPEG/RGB, 155.6 KB) | `environment/tiles_prison.png` (locked doors/bars), `environment/custom_tiles/prison_quest.png`, `environment/custom_tiles/prison_exit.png` | Industrial wire-mesh security partition cage with hinged gate, padlock hasp, hazard placard, shelving, and chemical drum inside. | [Source](https://wwcannon.com/wp-content/uploads/2024/12/WireCrafters-Secure-Storage-Enclosure.jpg) |
| [`prop_bar_stock_rack.jpg`](sector2_screw_machine/prop_bar_stock_rack.jpg) | 800x744 (JPEG/RGB, 160.3 KB) | `environment/tiles_prison.png` (storage/obstacle props) | Double-sided steel cantilever bar-stock storage rack loaded with bundled steel rods, tubes, and wrapped metal stock. | [Source](https://www.fordulrich.com/Customer-Content/www/products/Photos/Full/Cantilever_Rack-double_sided.jpg) |

---

### Sector 3 — Grind Dept & Subterranean Ducts ([`sector3_grind_ducts/INDEX.md`](sector3_grind_ducts/INDEX.md))

**Target Phase:** [Phase 2.3](../VISUAL_CONVERSION_PLAN.md) | **Files:** 6

| Reference Image | Dimensions & Format | Target Game Assets | Visual Notes | Source |
| :--- | :--- | :--- | :--- | :--- |
| [`floor_steel_grating_catwalk.jpg`](sector3_grind_ducts/floor_steel_grating_catwalk.jpg) | 1024x768 (JPEG/RGB, 261.4 KB) | `environment/tiles_caves.png` (catwalk/grating floor tiles) | Close-up angled view of galvanized press-locked industrial steel floor grating over a dark wet sub-floor void. | [Source](https://commons.wikimedia.org/wiki/File:Press_grating.jpg) |
| [`wall_galvanized_air_duct.jpg`](sector3_grind_ducts/wall_galvanized_air_duct.jpg) | 586x545 (JPEG/RGB, 71.9 KB) | `environment/tiles_caves.png` (ductwork walls & transitions) | Interconnected rectangular galvanized sheet-metal HVAC ventilation ducts with bolted flange joints and threaded-rod ceiling hangers. | [Source](https://commons.wikimedia.org/wiki/File:Duct_connected_01.jpg) |
| [`liquid_grey_coolant_sludge.jpg`](sector3_grind_ducts/liquid_grey_coolant_sludge.jpg) | 1024x656 (JPEG/RGB, 202.7 KB) | `environment/water2.png` (grey-cyan coolant sludge pools) | Thick metallic-grey abrasive grinding sludge mixed with wet emulsion coolant pooling inside a steel containment drum. | [Source](https://weima.com/wp-content/uploads/2023/02/schleifschlamm_verpressung_web-5.jpg) |
| [`prop_cylindrical_grinder.jpg`](sector3_grind_ducts/prop_cylindrical_grinder.jpg) | 915x749 (JPEG/RGB, 91.4 KB) | `environment/tiles_caves.png` (grinder machinery props), `environment/custom_tiles/caves_boss.png` | Industrial cylindrical grinding machine with red wheel guard, green/grey abrasive grinding wheel, coolant nozzles, and precision steel shaft. | [Source](https://commons.wikimedia.org/wiki/File:Cylindrical_grinder.jpg) |
| [`chasm_subterranean_pipe_trench.jpg`](sector3_grind_ducts/chasm_subterranean_pipe_trench.jpg) | 1024x768 (JPEG/RGB, 198.7 KB) | `environment/tiles_caves.png` (chasm / crawlspace pit tiles), `environment/custom_tiles/caves_quest.png` | Subterranean concrete utility crawlspace trench lined with heavy color-coded industrial pipes, brackets, and cable trays receding into darkness. | [Source](https://commons.wikimedia.org/wiki/File:Ginza_common_utility_duct.jpg) |
| [`prop_conveyor_hopper.jpg`](sector3_grind_ducts/prop_conveyor_hopper.jpg) | 577x1024 (JPEG/RGB, 133.4 KB) | `environment/tiles_caves.png` / `environment/custom_tiles/caves_boss.png` (machinery props) | Blue inclined industrial metal chip conveyor with control box and emergency stop discharging swarf into a steel scrap hopper. | [Source](https://storage1210.cdn-immedia.net/sites/default/files/styles/640x1136_crop/public/2022-06/chips-conveying_0.jpg) |

---

### Sector 4 — Heat-Treat Dept ([`sector4_heat_treat/INDEX.md`](sector4_heat_treat/INDEX.md))

**Target Phase:** [Phase 2.4](../VISUAL_CONVERSION_PLAN.md) | **Files:** 6

| Reference Image | Dimensions & Format | Target Game Assets | Visual Notes | Source |
| :--- | :--- | :--- | :--- | :--- |
| [`wall_refractory_furnace_brick.jpg`](sector4_heat_treat/wall_refractory_furnace_brick.jpg) | 1024x768 (JPEG/RGB, 185.6 KB) | `tiles_city.png` (wall & overhang tiles) | Close-up curved refractory firebrick furnace lining showing staggered brick courses, recessed mortar seams, and heat-weathered mineral texture. | [Source](https://commons.wikimedia.org/wiki/File:Refractory_bricks_lining.jpg) |
| [`prop_induction_heating_coil.jpg`](sector4_heat_treat/prop_induction_heating_coil.jpg) | 393x530 (JPEG/RGB, 32.2 KB) | `tiles_city.png` (wall deco / brazier / forge prop), `city_quest.png` | Glowing orange-yellow copper induction heating coil heating a cylindrical steel billet to red-hot (769 deg) with brass compression fittings above. | [Source](https://commons.wikimedia.org/wiki/File:A_metallic_piece_is_heated_te_red-hot_state_by_inductin_heating.jpg) |
| [`liquid_glowing_quench_oil.jpg`](sector4_heat_treat/liquid_glowing_quench_oil.jpg) | 1024x739 (JPEG/RGB, 273.6 KB) | `water3.png`, `tiles_city.png` (glowing heat-treat accents) | Incandescent orange-amber steel castings emerging from a heat-treatment furnace onto a refractory brick hearth cart beside a cooling blower. | [Source](https://commons.wikimedia.org/wiki/File:Castings_fresh_from_the_heat_treatment_furnace.jpg) |
| [`floor_blackened_steel_plate.jpg`](sector4_heat_treat/floor_blackened_steel_plate.jpg) | 1024x768 (JPEG/RGB, 399.0 KB) | `tiles_city.png` (floor, special floor, chasm lip) | High-contrast industrial diamond-plate steel flooring texture with raised lozenge treads and directional specular highlights for pixel-grid tiling. | [Source](https://commons.wikimedia.org/wiki/File:Tread_Plate_BW.JPG) |
| [`prop_brass_manifold_pipes.jpg`](sector4_heat_treat/prop_brass_manifold_pipes.jpg) | 1024x768 (JPEG/RGB, 280.3 KB) | `tiles_city.png` (wall pipes, valve props), `city_quest.png` | Dense industrial high-pressure manifold array featuring brass/bronze valve bonnets, square pipe distribution blocks, and red/blue handwheels. | [Source](https://commons.wikimedia.org/wiki/File:B-39_high_pressure_air_manifold_controls_2.JPG) |
| [`boss_heat_treat_furnace_core.jpg`](sector4_heat_treat/boss_heat_treat_furnace_core.jpg) | 1024x682 (JPEG/RGB, 138.2 KB) | `custom_tiles/city_boss.png`, `tiles_city.png` (boss arena furnace) | Industrial steel box heat-treating furnace exterior with pitched exhaust hood, glowing orange slit beneath the furnace door, and heavy plant machinery. | [Source](https://commons.wikimedia.org/wiki/File:Werkplaats_Mechelen_1985_staalovens.jpg) |

---

### Sector 5 — Precision Assembly & R&D Labs ([`sector5_assembly_rnd/INDEX.md`](sector5_assembly_rnd/INDEX.md))

**Target Phase:** [Phase 2.5](../VISUAL_CONVERSION_PLAN.md) | **Files:** 6

| Reference Image | Dimensions & Format | Target Game Assets | Visual Notes | Source |
| :--- | :--- | :--- | :--- | :--- |
| [`wall_cleanroom_white_panels.jpg`](sector5_assembly_rnd/wall_cleanroom_white_panels.jpg) | 1024x373 (JPEG/RGB, 167.0 KB) | `tiles_halls.png` (wall & overhang tiles) | Large aerospace cleanroom interior showing white and slate-grey modular wall panels, vertical panel seams, and a wall-sized HEPA filter bank. | [Source](https://commons.wikimedia.org/wiki/File:Clean_Room_at_Goddard_Space_Flight_Center_(4422310573).jpg) |
| [`floor_antistatic_lab_tile.jpg`](sector5_assembly_rnd/floor_antistatic_lab_tile.jpg) | 1024x667 (JPEG/RGB, 259.9 KB) | `tiles_halls.png` (floor & ESD zone accents) | Glossy light-grey cleanroom laboratory flooring with blue antistatic ESD floor mat, yellow-black hazard tape perimeter, and cleanroom equipment racks. | [Source](https://commons.wikimedia.org/wiki/File:KSC-03PD-0766.jpg) |
| [`prop_ball_bearing_assembly.jpg`](sector5_assembly_rnd/prop_ball_bearing_assembly.jpg) | 1024x1024 (JPEG/RGB, 160.9 KB) | `halls_special.png`, `tiles_halls.png` (precision bearing props / boss floor motifs) | Overhead precision angular-contact steel ball bearing (`B7009CTA P4UL`) clearly showing machined inner/outer raceways, retainer cage, and polished steel balls. | [Source](https://commons.wikimedia.org/wiki/File:B7009CTA_P4UL.jpg) |
| [`liquid_cryogenic_nitrogen.jpg`](sector5_assembly_rnd/liquid_cryogenic_nitrogen.jpg) | 1024x763 (JPEG/RGB, 175.0 KB) | `water4.png`, `tiles_halls.png` (cryogenic spill / mist accents) | Brushed stainless steel cryogenic dewar pouring boiling liquid nitrogen vapor over a superconductor track in a laboratory setup. | [Source](https://commons.wikimedia.org/wiki/File:Heidelberg_-_Max-Planck-Institut_f%C3%BCr_Kernphysik_-_Laboratorium_-_Fl%C3%BCssigstickstoff.JPG) |
| [`effect_plasma_vacuum_chamber.jpg`](sector5_assembly_rnd/effect_plasma_vacuum_chamber.jpg) | 768x1024 (JPEG/RGB, 60.8 KB) | `tiles_halls.png` (chasm / rift tiles), `halls_special.png` | Vivid purple-magenta plasma glow discharge ring inside a dark circular vacuum chamber viewport, ideal for anti-friction space-time rifts. | [Source](https://commons.wikimedia.org/wiki/File:Plasma_source.jpg) |
| [`prop_cleanroom_glovebox.jpg`](sector5_assembly_rnd/prop_cleanroom_glovebox.jpg) | 1024x682 (JPEG/RGB, 188.7 KB) | `tiles_halls.png` (lab bench / containment prop), `halls_special.png` | Brushed stainless steel R&D containment glovebox with bolted viewport frame, circular glove ports, gauges, and cylindrical airlock antechambers. | [Source](https://commons.wikimedia.org/wiki/File:New_glovebox_design_(7597561206).jpg) |

---

### Items, Maintenance Tools, PPE & Bearing ([`items_tools_ppe/INDEX.md`](items_tools_ppe/INDEX.md))

**Target Phase:** [Phase 3](../VISUAL_CONVERSION_PLAN.md) | **Files:** 10

| Reference Image | Dimensions & Format | Target Game Assets | Visual Notes | Source |
| :--- | :--- | :--- | :--- | :--- |
| [`tool_industrial_mop_bucket.jpg`](items_tools_ppe/tool_industrial_mop_bucket.jpg) | 818x1024 (JPEG/RGB, 97.3 KB) | `sprites/items.png` (Phase 3.2: Melee Maintenance Tools — Heavy-Duty Mop / Janitor gear), `environment/terrain_features.png` | Commercial janitorial yellow side-press wringer bucket cart with blue/red dual buckets and grey caster frame on clean white background; OSHA yellow/blue plastic color and wringer silhouette reference. | [Source](https://commons.wikimedia.org/wiki/File:MopWringer-45.jpg) |
| [`tool_heavy_pipe_wrench.jpg`](items_tools_ppe/tool_heavy_pipe_wrench.jpg) | 1024x295 (JPEG/RGB, 49.6 KB) | `sprites/items.png` (Phase 3.2: `WORN_SHORTSWORD` / `MACE` / `SWORD` — Janitor's Pipe Wrench & heavy melee tools) | Heavy-duty 14-inch Ridgid Stillson cast-iron pipe wrench with red I-beam handle, knurled adjustment nut, and serrated steel jaws on white background; clear diagonal weapon icon silhouette. | [Source](https://commons.wikimedia.org/wiki/File:Straight_Pipe_Wrench_3C.jpg) |
| [`tool_crowbar_prybar.jpg`](items_tools_ppe/tool_crowbar_prybar.jpg) | 243x1024 (JPEG/RGB, 70.8 KB) | `sprites/items.png` (Phase 3.2: `DAGGER` / `SHORTSWORD` / `LONGSWORD` — Steel Wrecking Crowbar / Prybar) | Forged dark steel gooseneck wrecking crowbar with split nail-puller claw and beveled pry tip; clean linear silhouette for diagonal 16x16 tool sprites. | [Source](https://commons.wikimedia.org/wiki/File:Standard_Crowbar_Black.jpg) |
| [`tool_soldering_iron_station.jpg`](items_tools_ppe/tool_soldering_iron_station.jpg) | 1024x686 (JPEG/RGB, 170.7 KB) | `sprites/items.png` (Phase 3.2 & 3.4: Mechanic's Soldering Iron & electrical maintenance applicators) | Yellow-handled electronic soldering iron resting in coiled spring holder with black base tray and cleaning sponge; industrial yellow/black casing and metallic coil detail reference. | [Source](https://commons.wikimedia.org/wiki/File:Soldering_iron_in_holder.jpg) |
| [`tool_pneumatic_nailgun.jpg`](items_tools_ppe/tool_pneumatic_nailgun.jpg) | 1024x683 (JPEG/RGB, 182.9 KB) | `sprites/items.png` (Phase 3.2: `SPIRIT_BOW` / `CROSSBOW` / thrown hardware — Exterminator's Pneumatic Nailgun) | Close-up of yellow pneumatic framing nail gun with brushed aluminum angled nail magazine, black nosepiece, and red safety tip. | [Source](https://commons.wikimedia.org/wiki/File:Nail_gun.jpg) |
| [`ppe_yellow_hazmat_suit.jpg`](items_tools_ppe/ppe_yellow_hazmat_suit.jpg) | 686x1024 (JPEG/RGB, 129.5 KB) | `sprites/items.png` (`ARMOR_PLATE` — Tier 5 Hazmat Suit), `sprites/warrior.png`..`cleric.png` (Row 5 PPE) | Full-body high-visibility OSHA Hazard Yellow chemical containment hazmat suits with sealed hoods, clear faceplates, orange straps, and black chemical gloves. | [Source](https://commons.wikimedia.org/wiki/File:MHE_-_KBH_Brandvaesen_-_HAZMAT_3a.jpg) |
| [`ppe_kevlar_safety_vest.jpg`](items_tools_ppe/ppe_kevlar_safety_vest.jpg) | 678x1024 (JPEG/RGB, 59.5 KB) | `sprites/items.png` (`ARMOR_MAIL` — Tier 3 Kevlar Vest, `ARMOR_SCALE` — Tier 4 Riot Gear), `sprites/warrior.png`..`cleric.png` (Rows 3–4) | Clean matte-black protective Kevlar vest on neutral backdrop showing shoulder straps, padded torso armor silhouette, and dual side retention straps. | [Source](https://commons.wikimedia.org/wiki/File:NIJ_LVLIIIA_Kogelvrij_vest,_BA8001.jpg) |
| [`ppe_welding_goggles_helmet.jpg`](items_tools_ppe/ppe_welding_goggles_helmet.jpg) | 1024x485 (JPEG/RGB, 108.2 KB) | `sprites/items.png` (Mechanic/Supervisor PPE & `ARMOR_DUELIST` / `ARMOR_CLERIC` class rigs), `sprites/avatars.png` | Industrial matte-black and grey welding helmet with flip-up rectangular dark-tinted filter visor and red side accent panel; hard-surface PPE silhouette reference. | [Source](https://commons.wikimedia.org/wiki/File:Welding_helmet.jpg) |
| [`spray_chemical_trigger_bottle.jpg`](items_tools_ppe/spray_chemical_trigger_bottle.jpg) | 583x1024 (JPEG/RGB, 40.1 KB) | `sprites/items.png` (`POTION_*` — Chemical Sprays / Solvents, `POTION_HOLDER`, `WAND_*` — Chemical Applicators / Sprayers) | Isolated translucent red plastic trigger spray bottle on solid black background; crisp bottle, collar, nozzle, and trigger silhouette ideal for re-paletting across 12 spray/solvent colors. | [Source](https://commons.wikimedia.org/wiki/File:Red_Spray_bottle_1440426.png) |
| [`bearing_infinite_precision_chrome.jpg`](items_tools_ppe/bearing_infinite_precision_chrome.jpg) | 1024x684 (JPEG/RGB, 57.8 KB) | `sprites/items.png` (`AMULET` — Row 4, Col 14), `sprites/amulet.png` (Phase 3.1: Infinite Precision Ball Bearing) | Mirror-finish 60mm polished chrome steel ball bearing sphere on clean light grey backdrop with crisp specular highlight and deep horizon reflection. | [Source](https://commons.wikimedia.org/wiki/File:Polished_steel_ball_60mm_diameter.jpg) |

---

### Mobs, NPCs & Bosses ([`mobs_npcs_bosses/INDEX.md`](mobs_npcs_bosses/INDEX.md))

**Target Phase:** [Phase 4](../VISUAL_CONVERSION_PLAN.md) | **Files:** 6

| Reference Image | Dimensions & Format | Target Game Assets | Visual Notes | Source |
| :--- | :--- | :--- | :--- | :--- |
| [`boss_heavy_excavator_loader.jpg`](mobs_npcs_bosses/boss_heavy_excavator_loader.jpg) | 1024x682 (JPEG/RGB, 177.8 KB) | `sprites/dm300.png`, `sprites/dm200.png` (Corrupted Mech / Heavy Factory Loader Boss) | 1024x682. Articulated white industrial robot arm inside a safety-glass manufacturing cell with control HMI, yellow/red emergency-stop button, and heavy chain-drive mechanism. | [Source](https://commons.wikimedia.org/wiki/File:Robot_arm_operates_machine_in_factory_setting.jpg) |
| [`mob_autonomous_floor_scrubber.jpg`](mobs_npcs_bosses/mob_autonomous_floor_scrubber.jpg) | 771x1024 (JPEG/RGB, 262.1 KB) | `sprites/guard.png`, `sprites/thief.png` (Rogue Roomba / Autonomous Floor Scrubber Bot) | 771x1024. Teal-blue autonomous industrial floor scrubber featuring cylindrical top LiDAR beacon, red e-stop button, caster wheels, and bottom rotary brush/squeegee deck. | [Source](https://commons.wikimedia.org/wiki/File:X4_ROVR_Autonomous_Floor_Scrubber_in_Morrisons,_Worthing_2025-12-08.jpg) |
| [`mob_high_voltage_tesla_arc.jpg`](mobs_npcs_bosses/mob_high_voltage_tesla_arc.jpg) | 800x450 (JPEG/RGB, 77.0 KB) | `sprites/dm100.png`, `sprites/pylon.png` (High-Voltage Arc Turret / Power Pylon) | 800x450. Long-exposure shot of copper secondary coil and aluminum toroid discharging branching violet-cyan electrical arcs against a ribbed steel industrial shutter door. | [Source](https://commons.wikimedia.org/wiki/File:Tesla_coil_with_a_long-exposure.jpg) |
| [`mob_laboratory_white_rat.jpg`](mobs_npcs_bosses/mob_laboratory_white_rat.jpg) | 1024x682 (JPEG/RGB, 155.2 KB) | `sprites/rat.png` (Mutated Lab Rat) | 1024x682. Crisp close-up of an albino Wistar laboratory rat held in a gloved hand; shows pink ears/snout/claws, red eyes, and dense white fur for Sector 1 mutated lab rat sprites. | [Source](https://commons.wikimedia.org/wiki/File:Wistar_rat.jpg) |
| [`npc_snack_vending_machine.jpg`](mobs_npcs_bosses/npc_snack_vending_machine.jpg) | 768x1024 (JPEG/RGB, 242.7 KB) | `sprites/shopkeeper.png` (Vending Machine Dispenser) | 768x1024. Glass-front snack and beverage vending machine with illuminated product coils, numeric selection screen, bill/coin acceptor, and bottom retrieval chute. | [Source](https://commons.wikimedia.org/wiki/File:Snack_and_soda_water_vending_machine,_Leningrad_Railway_Station,_Moscow_November_2022.jpg) |
| [`prop_industrial_security_camera.jpg`](mobs_npcs_bosses/prop_industrial_security_camera.jpg) | 1024x768 (JPEG/RGB, 138.1 KB) | `sprites/red_sentry.png`, `sprites/wards.png` (CCTV Security Turret / Surveillance Ward) | 1024x768. Wall-mounted weathered grey-white dome CCTV turret on a heavy metal bracket with dark tinted hemisphere housing and exposed conduit wiring. | [Source](https://commons.wikimedia.org/wiki/File:CCTV_dome_camera.jpg) |

---

### UI, HUD & Effects ([`ui_hud_effects/INDEX.md`](ui_hud_effects/INDEX.md))

**Target Phase:** [Phase 5](../VISUAL_CONVERSION_PLAN.md) | **Files:** 6

| Reference Image | Dimensions & Format | Target Game Assets | Visual Notes | Source |
| :--- | :--- | :--- | :--- | :--- |
| [`effect_toxic_chemical_drum_spill.jpg`](ui_hud_effects/effect_toxic_chemical_drum_spill.jpg) | 468x306 (JPEG/RGB, 88.5 KB) | `effects/effects.png`, `effects/specks.png`, `environment/terrain_features.png` (Toxic Chemical Spill & Hazard Effects) | 468x306. Hazmat-suited workers in yellow hardhats amidst rusted, crushed, and leaking 55-gallon chemical drums (yellow, blue, and blackened steel barrels). | [Source](https://commons.wikimedia.org/wiki/File:Valleyofdrums.jpg) |
| [`hud_green_crt_oscilloscope.jpg`](ui_hud_effects/hud_green_crt_oscilloscope.jpg) | 800x738 (JPEG/RGB, 134.6 KB) | `interfaces/status_pane.png`, `interfaces/boss_hp.png`, `interfaces/toolbar.png` (CRT Readout & Waveform Meters) | 800x738. Tektronix analog CRT oscilloscope bezel displaying glowing phosphor triangular and square wave traces over an illuminated measurement graticule. | [Source](https://commons.wikimedia.org/wiki/File:Triangular_wave_and_square_wave_on_oscilloscope_screen.jpg) |
| [`hud_industrial_control_panel.jpg`](ui_hud_effects/hud_industrial_control_panel.jpg) | 1024x757 (JPEG/RGB, 206.1 KB) | `interfaces/chrome.png`, `interfaces/menu_pane.png`, `interfaces/menu_button.png` (Retro Steel Control Panel Chrome) | 1024x757. Weathered industrial steel electrical switchgear cabinets with circular analog dial gauges, bolted housings, red/white stamped labels, and heavy throw levers. | [Source](https://commons.wikimedia.org/wiki/File:Geevor_tin_mine_electrical_switchgear.jpg) |
| [`hud_osha_warning_signage.jpg`](ui_hud_effects/hud_osha_warning_signage.jpg) | 416x402 (JPEG/RGB, 55.8 KB) | `interfaces/banners.png`, `interfaces/icons.png`, `interfaces/badges.png` (OSHA Caution & Hazard Banners) | 416x402. Industrial workplace safety placards featuring DANGER Electric Hazard, WARNING Toxic Hazard (skull & crossbones), NOTICE Fire Door, DANGER Flammable Materials, and Safety First. | [Source](https://commons.wikimedia.org/wiki/File:Workplace_Safety_Signs.jpg) |
| [`hud_punched_timecard_rack.jpg`](ui_hud_effects/hud_punched_timecard_rack.jpg) | 1024x611 (JPEG/RGB, 174.1 KB) | `interfaces/menu_pane.png`, `interfaces/icons.png`, `interfaces/badges.png` (Employee Punch Clock / Timecard Rack) | 1024x611. Wall-mounted dark metal multi-column employee timecard rack holding gridded paper punch cards against an institutional office wall. | [Source](https://commons.wikimedia.org/wiki/File:Time_card_holder.jpg) |
| [`splash_factory_exterior_night.jpg`](ui_hud_effects/splash_factory_exterior_night.jpg) | 1024x717 (JPEG/RGB, 141.6 KB) | `splashes/title/*.png`, `splashes/*.jpg`, `interfaces/surface.png` (Factory Exterior Night Vista) | 1024x717. Industrial manufacturing plant exterior at night illuminated by harsh white floodlights and red obstruction beacons, with illuminated steam/smoke plumes rising from smokestacks. | [Source](https://commons.wikimedia.org/wiki/File:Heavy_night_industrial_light_pollution.jpg) |
