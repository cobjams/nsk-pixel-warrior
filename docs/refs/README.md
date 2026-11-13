# Visual Reference Library (`docs/refs/`)

This directory holds photo, concept, and pixel-art references used by visual modding agents alongside [`docs/VISUAL_CONVERSION_PLAN.md`](../VISUAL_CONVERSION_PLAN.md) and [`docs/texture_reference.json`](../texture_reference.json).

## Directory Structure

| Folder | Modding Phase | Target Assets |
| :--- | :--- | :--- |
| `offices/` | Phase 2.1 (Done) | `tiles_sewers.png`, `water0.png`, `custom_tiles/sewer_boss.png` |
| `factory/` | General Facility | Shared factory architecture, signage, and machine silhouettes |
| `sector2_screw_machine/` | Phase 2.2 | `tiles_prison.png`, `water1.png`, `custom_tiles/prison_quest.png`, `prison_exit.png` |
| `sector3_grind_ducts/` | Phase 2.3 | `tiles_caves.png`, `tiles_caves_crystal.png`, `tiles_caves_gnoll.png`, `water2.png`, `caves_*.png` |
| `sector4_heat_treat/` | Phase 2.4 | `tiles_city.png`, `water3.png`, `custom_tiles/city_quest.png`, `city_boss.png` |
| `sector5_assembly_rnd/` | Phase 2.5 | `tiles_halls.png`, `water4.png`, `custom_tiles/halls_special.png` |
| `items_tools_ppe/` | Phase 3 | `sprites/items.png`, `sprites/item_icons.png`, `sprites/amulet.png`, `terrain_features.png` |
| `mobs_npcs_bosses/` | Phase 4 | `sprites/*.png` (mutated workers, industrial bots, bosses, NPCs) |
| `ui_hud_effects/` | Phase 5 | `interfaces/*.png`, `effects/*.png`, `splashes/*` |

## File Naming Convention

Use lowercase `snake_case` filenames that identify **subject + material/detail + view** (avoid generic camera names like `IMG_1020.JPG` for new additions):

- **Environments:** `<surface_or_prop>_<material>_<detail>.<ext>`
  - Examples: `floor_oil_stained_concrete.jpg`, `wall_riveted_steel_hazard_stripe.png`, `liquid_amber_cutting_oil.jpg`, `chasm_ventilation_shaft.png`
- **Items & Tools:** `<category>_<item_name>_<style>.<ext>`
  - Examples: `tool_pipe_wrench.png`, `ppe_hazmat_suit_yellow.jpg`, `spray_solvent_bottle.png`, `bearing_infinite_precision_orb.png`
- **Enemies & NPCs:** `<sector>_<entity_name>_<pose_or_detail>.<ext>`
  - Examples: `s1_mutated_lab_rat.png`, `s2_rogue_roomba_bot.jpg`, `npc_vending_machine.jpg`, `boss_corrupted_foreman.png`
- **UI & Effects:** `<element>_<theme>.<ext>`
  - Examples: `hud_clipboard_steel_chrome.png`, `splash_factory_exterior_night.jpg`

## High-Priority Reference Checklist

1. **`sector2_screw_machine/`:** Oil-stained concrete floors, dark riveted steel walls with yellow/black hazard stripes, CNC screw machines, amber cutting oil pools, chain-link safety cages (`prison_quest` / `prison_exit`).
2. **`sector3_grind_ducts/`:** Galvanized sheet-metal air ducts, steel floor grating/catwalks, abrasive grey-cyan coolant sludge, spark/grinding wheel debris, subterranean crawlspace piping.
3. **`sector4_heat_treat/`:** Refractory furnace brick, copper/brass induction coils & manifolds, glowing orange quench oil tanks, blackened steel floor plates.
4. **`sector5_assembly_rnd/`:** Sterile white/titanium cleanroom panels, precision inspection benches, purple/magenta space-time rift distortions, cryogenic liquid tanks.
5. **`items_tools_ppe/`:** Industrial mop/wrench/crowbar/soldering-iron silhouettes, spray bottles & aerosol cans, clipboard/requisition forms, keycards/ID badges, break-room snacks, precision chrome ball bearing orb.
6. **`mobs_npcs_bosses/`:** Vintage soda/snack vending machine (`shopkeeper`), rogue floor-scrubber/Roomba bot, hazmat/welding/foreman silhouettes, mutated rats/slimes/insects, laser turret (`red_sentry`).
7. **`ui_hud_effects/`:** Retro industrial CRT/gauge HUD chrome, OSHA warning banners, industrial hazard badges, factory exterior/title vista.
