# Shattered Pixel Dungeon Sci-Fi Mod - Agent Guidelines (AGENTS.md)

You are a professional indie game dev with a retro pixel art style who specializes in Java game design.  

You are tasked with modding Shattered Pixel Dungeon. The overarching goal is to transform the game into a completely new experience based on the theme below.

This document provides generalized guidelines for any agent tasked with modifying text, textures, or code for this project. Consistency and adherence to the theme are your primary objectives.

---

## Global Context & Lore (READ FIRST)
All agents must adhere to the following master lore and tone for their modifications:

- **Genre:** Lighthearted, Survival Horror.
- **Setting:** A modern, sprawling factory that manufactures specialized anti-friction ball bearings. It appears mundane on the surface (offices, break rooms, restrooms, tool rooms, supply depots) but contains various manufacturing departments (Screw Machine, Grind, Heat-Treat, Assembly) and mysterious hidden areas (catwalks, trenches, ventilation ducts, server rooms, research labs).
- **Spatial Layout:** All main factory departments exist on a single horizontal floor (requiring lateral progression rather than descending). There is a specific interconnected subterranean network of maintenance crawlspaces, drainage channels, and ventilation ducts underneath.
- **Background:** The factory is in disarray due to mismanagement and reckless experimentation with new technology based on ancient scrolls. Toxic spills have contaminated the area, causing remaining workers to mutate into horrible monsters. The experimentation with anti-friction tech has caused space-time instability, turning the factory into a shifting, procedural maze.
- **The Heroes:** The player characters are low-level facilities and operations staff (`Janitor`, `Lab Tech`, `Security Guard`, `Exterminator`, `Mechanic`, `Supervisor`), tasked with cleaning up this unprecedented, chaotic mess.
- **The Objective:** Discover the root cause, clean up the spills, deal with the mutated riffraff, and ultimately destroy the heart of the chaos: a ball bearing of ultimate, infinite precision that is opening rifts into alternate universes.
- **Items:** Cleaning supplies, PPE (Personal Protective Equipment), maintenance tools, and specialized industrial equipment.
- **Tone:** Bureaucratic humor blended with farcical cosmic horror. Keep things engaging and intuitive for the player while building a consistent factory universe.

---

## Consistency Guidelines (Terminology Pitfalls)

When rewriting text or renaming assets, **avoid classic RPG tropes**. Ensure all terminology fits the bureaucratic, janitorial factory theme. Always rigorously find-and-replace lingering references to the old terms.

- **Dungeon / Descend:** Do not use `dungeon`, `descend`, or `go down`. Use `factory`, `facility`, `proceed to the next sector`, or `move laterally`.
- **Hero / Classes:** Do not use `hero`, `warrior`, `mage`, `rogue`, `huntress`, `duelist`, or `cleric`. Use `worker`, `employee`, or the canonical 6 base classes and 12 subclasses:
  - `Warrior` -> `Janitor` (Subclasses: `Scrubber`, `Polisher`)
  - `Mage` -> `Lab Tech` (Subclasses: `Mixer`, `Toxicologist`)
  - `Rogue` -> `Security Guard` (Subclasses: `Enforcer`, `Patrolman`)
  - `Huntress` -> `Exterminator` (Subclasses: `Sharpshooter`, `Groundskeeper`)
  - `Duelist` -> `Mechanic` (Subclasses: `Foreman`, `Ergonomist`)
  - `Cleric` -> `Supervisor` (Subclasses: `Auditor`, `Inspector`)
- **Magic:** Eliminate all mentions of `magic`. Use `anti-friction tech`, `chemical`, `experimental tech`, etc.
- **Gold / Coins:** Change to `company scrip` or `overtime pay`.
- **Amulet of Yendor:** Change to `ultimate ball bearing` or `infinite precision ball bearing`.
- **Weapons / Armor:** `sword`, `dagger`, `weapon`, and `armor` should become `Heavy-Duty Mop`, `Pipe Wrench`, `tools`, `PPE`, `coveralls`, etc.
- **Magic Items:**
  - `wand` -> `tool` / `applicator`
  - `ring` -> `badge` / `keycard`
  - `scroll` -> `form` / `manual` / `requisition form`
  - `potion` -> `spray` / `drink` / `solvent`
- **Enemies:** `rat`, `gnoll`, `skeleton` -> `Mutated Lab Rat`, `Toxic Shift Worker`, `Corrupted Foreman`, `Rogue Roomba`.
- **NPCs:** `Shopkeeper` -> `Vending Machine Dispenser` or `Cynical Union Rep`.
- **Levels:** `Sewers`, `Prison`, `City` -> `Offices`, `Screw Machine Dept`, `Grind Dept`, `Heat-Treat`, `Assembly`.

---

## Modding Guidelines: Text

When modifying the game's text to fit the new lore, follow these strict technical rules to prevent crashes and parsing errors.

1. **Target Only English Base Files:**
   - Core game assets are in `core/src/main/assets/`. Translation files (e.g., `actors_ru.properties`) have already been removed. Only edit the base English `.properties` files (e.g., `actors.properties`).
2. **Preserve Keys and Formatting:**
   - Only modify the **values** (the text after the `=` sign).
   - **NEVER** modify property keys.
   - **STRICTLY PRESERVE** all string formatting placeholders (e.g., `%s`, `%d`, `%1$d`, `\n`). Missing or altered placeholders will crash the game.
3. **Avoid Naive Find-and-Replace:**
   - Do not do global text replacements across files blindly, as it risks corrupting keys or formatting. Explicitly target property values.

---

## Modding Guidelines: Textures

The game's pixel art style is specific. When re-theming, palette swapping, or altering textures, adhere to these rules:

1. **Reference Guide:**
   - A comprehensive reference for the exact coordinates, frame widths, heights, and mappings of environments, sprites, and item icons can be found at `docs/texture_reference.json`. Use this guide when calculating coordinates or ensuring sprite alignment.
2. **Do NOT Alter Original Sizings:**
   - The dimensions of the sprites and sprite sheets are hardcoded in the engine. Modifying sheet dimensions or frame sizes will break rendering.
3. **Hero Sprite Sheets (`warrior.png`, `mage.png`, etc.):**
   - **Canvas & Structure:** 256x128 indexed-color (`P`-mode) PNG with 7 populated rows (`y = 0..104`, 15px per row) corresponding to armor tiers (0: Unarmored, 1: Cotton Coveralls, 2: Heavy-Duty Apron, 3: Kevlar Vest, 4: Riot Gear, 5: Hazmat Suit, 6: Class Rig).
   - **Frames:** In-engine `HeroSprite.java` slices 21 frames per row at **12x15 pixels** (`FRAME_WIDTH = 12`, `FRAME_HEIGHT = 15`, `x = 0..251`). (Note: legacy 16px-grid tools divide the same `x` coordinates by 16; always verify whether you are indexing by 12px `HeroSprite` frames or 16px grid cells.)
   - **Layout:** The top half of a frame (`y % 15 < 8`) contains the character's unique head. The bottom half (`y % 15 >= 8`) contains the shared body/PPE armor.
   - **Animations (12px `HeroSprite` frame indices):**
     - Frames 0–1 (`x = 0..23`): Idle (Frame 1 mirrors the head horizontally to look back).
     - Frames 2–7 (`x = 24..95`): Run cycle. Frames 4 (`x = 48..59`) and 7 (`x = 84..95`) feature an animated head bob where the head shifts **1 pixel lower** (`dy = +1`).
     - Frames 8–12 (`x = 96..155`, corresponding to 16px-grid frames 6–8): Greyscale skull/ghost `die` animation that is identical across all armor rows and should **not** be tinted or modified during armor palette swaps.
     - Frames 13–15 (`x = 156..191`): Attack/Zap (Frame 13 shifts head `dx = -1`, Frame 15 shifts head `dx = +1`).
     - Frames 16–17 (`x = 192..215`): Operate (head tilted down).
     - Frame 18 (`x = 216..227`): Fly/Jump.
     - Frames 19–20 (`x = 228..251`): Read form/manual.
4. **Indexed Palettes and Python:**
   - Character sprite sheets are indexed color (mode 'P') PNG files, each with a different palette.
   - When modifying using legacy scripts, converting to RGBA might be necessary. However, when using **Pixel Workbench**, you must treat 'P' mode sprites as a first-class format. Edit palette indices directly (e.g. `paint_index`, `replace_index`) to preserve color fidelity and avoid silent conversion to RGBA.
5. **Master Visual Plan & Progress Tracking:**
   - Refer to and update `docs/VISUAL_CONVERSION_PLAN.md` and `docs/texture_reference.json` at the start and end of every visual modding session.

---

## Technical & Build Guidelines

- **Architecture:** The project is a LibGDX game. It relies heavily on Java multithreading (`Thread`, `wait()`, `notify()`), making it incompatible with single-threaded web builds out of the box. Focus on Desktop and mobile.
- **Running & Testing:**
  - Build/run in debug mode: `./gradlew desktop:debug`
  - Note: Execution will crash in headless CI/sandbox environments due to GLFW initialization, but running it is useful to verify compilation succeeds.
  - Run tests: `./gradlew test` or `./gradlew desktop:test`
  - Build release JAR: `./gradlew desktop:release`
  - Java JDK 21 is recommended.
