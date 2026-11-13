package com.shatteredpixel.shatteredpixeldungeon;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Zero-dependency headless smoke tests for assets, sprite sheet bounds,
 * message bundle formatting, and canonical mod class definitions.
 *
 * Run directly via:
 *   java core/src/test/java/com/shatteredpixel/shatteredpixeldungeon/HeadlessAssetAndStringSmokeTest.java
 * or via Gradle:
 *   ./gradlew :core:smokeTest
 */
public class HeadlessAssetAndStringSmokeTest {

    private static final Path ASSETS_DIR = Paths.get("core/src/main/assets");
    private static final Path ASSETS_JAVA = Paths.get("core/src/main/java/com/shatteredpixel/shatteredpixeldungeon/Assets.java");
    private static final Path ITEM_SHEET_JAVA = Paths.get("core/src/main/java/com/shatteredpixel/shatteredpixeldungeon/sprites/ItemSpriteSheet.java");

    private static final Pattern STRING_LITERAL = Pattern.compile("\"([^\"]+)\"");
    private static final Pattern PRINTF_TOKEN = Pattern.compile(
            "%(?:(\\d+)\\$)?([-#+0,(<]*)?(\\d+)?(?:\\.(\\d+))?(?:([bBhHsScCdoxXeEfgGaA%n])|([tT][HIklMSLNpzZsQBbhAaCYyjmdeRTrDFc]))"
    );

    private static int passed = 0;
    private static final List<String> failures = new ArrayList<>();

    public static void main(String[] args) throws Exception {
        if (!Files.exists(ASSETS_DIR)) {
            throw new IllegalStateException("Expected working directory at repo root; missing " + ASSETS_DIR.toAbsolutePath());
        }

        runCheck("checkAssetsFileReferences", HeadlessAssetAndStringSmokeTest::checkAssetsFileReferences);
        runCheck("checkItemAndTileSheetBounds", HeadlessAssetAndStringSmokeTest::checkItemAndTileSheetBounds);
        runCheck("checkAllMessageBundlesFormatCleanly", HeadlessAssetAndStringSmokeTest::checkAllMessageBundlesFormatCleanly);
        runCheck("checkCanonicalClassesPresent", HeadlessAssetAndStringSmokeTest::checkCanonicalClassesPresent);

        System.out.println("Smoke test summary: " + passed + " check(s) passed, " + failures.size() + " failed.");
        if (!failures.isEmpty()) {
            for (String f : failures) {
                System.err.println("FAIL: " + f);
            }
            System.exit(1);
        }
    }

    @FunctionalInterface
    private interface Check {
        void run() throws Exception;
    }

    private static void runCheck(String name, Check check) {
        try {
            check.run();
            passed++;
            System.out.println("[PASS] " + name);
        } catch (Throwable t) {
            failures.add(name + ": " + t.getMessage());
            t.printStackTrace(System.err);
        }
    }

    private static void checkAssetsFileReferences() throws IOException {
        String src = Files.readString(ASSETS_JAVA, StandardCharsets.UTF_8);
        Matcher m = STRING_LITERAL.matcher(src);
        Set<String> checkedPaths = new HashSet<>();
        int imageCount = 0;

        while (m.find()) {
            String val = m.group(1);
            if (!val.contains("/")) {
                continue;
            }
            if (val.startsWith("messages/")) {
                Path prop = ASSETS_DIR.resolve(val + ".properties");
                if (!Files.isRegularFile(prop)) {
                    throw new AssertionError("Missing message bundle referenced in Assets.java: " + prop);
                }
                continue;
            }
            // Legacy unused constant in upstream Assets.java (Fireball.java loads fireball-short/tall.png)
            if ("effects/fireball.png".equals(val)) {
                continue;
            }
            if (!checkedPaths.add(val)) {
                continue;
            }
            Path assetPath = ASSETS_DIR.resolve(val);
            if (!Files.isRegularFile(assetPath)) {
                throw new AssertionError("Missing asset referenced in Assets.java: " + assetPath);
            }
            if (val.endsWith(".png") || val.endsWith(".jpg")) {
                BufferedImage img = ImageIO.read(assetPath.toFile());
                if (img == null || img.getWidth() <= 0 || img.getHeight() <= 0) {
                    throw new AssertionError("Corrupt or unreadable image asset: " + assetPath);
                }
                imageCount++;
            }
        }
        System.out.println("  Verified " + checkedPaths.size() + " asset paths (" + imageCount + " decoded images).");
    }

    private static void checkItemAndTileSheetBounds() throws IOException {
        BufferedImage itemsImg = ImageIO.read(ASSETS_DIR.resolve("sprites/items.png").toFile());
        BufferedImage iconsImg = ImageIO.read(ASSETS_DIR.resolve("sprites/item_icons.png").toFile());
        if (itemsImg.getWidth() != 256 || itemsImg.getHeight() != 512) {
            throw new AssertionError("sprites/items.png expected 256x512, got " + itemsImg.getWidth() + "x" + itemsImg.getHeight());
        }
        if (iconsImg.getWidth() != 128 || iconsImg.getHeight() != 64) {
            throw new AssertionError("sprites/item_icons.png expected 128x64, got " + iconsImg.getWidth() + "x" + iconsImg.getHeight());
        }

        String itemSrc = Files.readString(ITEM_SHEET_JAVA, StandardCharsets.UTF_8);
        Matcher itemRect = Pattern.compile("assignItemRect\\(\\s*\\w+\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)\\s*\\)").matcher(itemSrc);
        int itemCount = 0;
        while (itemRect.find()) {
            int w = Integer.parseInt(itemRect.group(1));
            int h = Integer.parseInt(itemRect.group(2));
            if (w <= 0 || w > 16 || h <= 0 || h > 16) {
                throw new AssertionError("assignItemRect out of 16x16 cell bounds: " + w + "x" + h);
            }
            itemCount++;
        }

        Matcher iconRect = Pattern.compile("assignIconRect\\(\\s*\\w+\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)\\s*\\)").matcher(itemSrc);
        int iconCount = 0;
        while (iconRect.find()) {
            int w = Integer.parseInt(iconRect.group(1));
            int h = Integer.parseInt(iconRect.group(2));
            if (w <= 0 || w > 8 || h <= 0 || h > 8) {
                throw new AssertionError("assignIconRect out of 8x8 cell bounds: " + w + "x" + h);
            }
            iconCount++;
        }

        for (String hero : Arrays.asList("warrior.png", "mage.png", "rogue.png", "huntress.png", "duelist.png", "cleric.png")) {
            BufferedImage hImg = ImageIO.read(ASSETS_DIR.resolve("sprites/" + hero).toFile());
            if (hImg.getWidth() != 256 || hImg.getHeight() != 128) {
                throw new AssertionError("Hero sheet " + hero + " expected 256x128, got " + hImg.getWidth() + "x" + hImg.getHeight());
            }
        }

        for (String env : Arrays.asList("tiles_sewers.png", "tiles_prison.png", "tiles_caves.png", "tiles_city.png", "tiles_halls.png")) {
            BufferedImage eImg = ImageIO.read(ASSETS_DIR.resolve("environment/" + env).toFile());
            if (eImg.getWidth() != 256 || eImg.getHeight() != 256) {
                throw new AssertionError("Tilesheet " + env + " expected 256x256, got " + eImg.getWidth() + "x" + eImg.getHeight());
            }
        }

        for (int i = 0; i < 5; i++) {
            BufferedImage wImg = ImageIO.read(ASSETS_DIR.resolve("environment/water" + i + ".png").toFile());
            if (wImg.getWidth() != 32 || wImg.getHeight() != 32) {
                throw new AssertionError("Water texture water" + i + ".png expected 32x32, got " + wImg.getWidth() + "x" + wImg.getHeight());
            }
        }

        System.out.println("  Verified " + itemCount + " item rects, " + iconCount + " icon rects, 6 hero sheets, 5 tilesheets, 5 water textures.");
    }

    private static void checkAllMessageBundlesFormatCleanly() throws IOException {
        Path msgRoot = ASSETS_DIR.resolve("messages");
        List<Path> propFiles;
        try (Stream<Path> walk = Files.walk(msgRoot)) {
            propFiles = walk.filter(p -> p.toString().endsWith(".properties")).sorted().collect(Collectors.toList());
        }
        if (propFiles.isEmpty()) {
            throw new AssertionError("No .properties files found under " + msgRoot);
        }

        int totalKeys = 0;
        for (Path p : propFiles) {
            checkNoDuplicateKeys(p);

            Properties props = new Properties();
            try (BufferedReader br = new BufferedReader(new InputStreamReader(Files.newInputStream(p), StandardCharsets.UTF_8))) {
                props.load(br);
            }

            for (String key : props.stringPropertyNames()) {
                String val = props.getProperty(key);
                totalKeys++;
                Object[] syntheticArgs = buildSyntheticArgs(val, p + "#" + key);
                if (syntheticArgs.length > 0) {
                    try {
                        String.format(Locale.ENGLISH, val, syntheticArgs);
                    } catch (RuntimeException ex) {
                        throw new AssertionError("String.format failed for " + p + " key '" + key + "': " + ex.getMessage(), ex);
                    }
                }
            }
        }
        System.out.println("  Formatted and validated " + totalKeys + " message keys across " + propFiles.size() + " bundles.");
    }

    private static void checkNoDuplicateKeys(Path p) throws IOException {
        List<String> lines = Files.readAllLines(p, StandardCharsets.UTF_8);
        Set<String> seen = new HashSet<>();
        boolean inContinuation = false;
        for (int i = 0; i < lines.size(); i++) {
            String raw = lines.get(i);
            if (inContinuation) {
                inContinuation = hasOddTrailingBackslashes(raw);
                continue;
            }
            String trimmed = raw.trim();
            if (trimmed.isEmpty() || trimmed.startsWith("#") || trimmed.startsWith("!")) {
                continue;
            }
            int eq = raw.indexOf('=');
            if (eq > 0) {
                String key = raw.substring(0, eq).trim();
                if (!seen.add(key)) {
                    throw new AssertionError("Duplicate key '" + key + "' in " + p + " at line " + (i + 1));
                }
            }
            inContinuation = hasOddTrailingBackslashes(raw);
        }
    }

    private static boolean hasOddTrailingBackslashes(String line) {
        int count = 0;
        for (int i = line.length() - 1; i >= 0 && line.charAt(i) == '\\'; i--) {
            count++;
        }
        return (count % 2) == 1;
    }

    private static Object[] buildSyntheticArgs(String val, String ctx) {
        Map<Integer, Object> slotValues = new HashMap<>();
        Matcher m = PRINTF_TOKEN.matcher(val);
        int nextSeq = 1;
        int lastSlot = 0;
        int maxSlot = 0;

        while (m.find()) {
            String idxGroup = m.group(1);
            String flags = m.group(2);
            String conv = m.group(5) != null ? m.group(5) : m.group(6);
            if ("%".equals(conv) || "n".equals(conv)) {
                continue;
            }
            int slot;
            if (flags != null && flags.contains("<")) {
                slot = lastSlot > 0 ? lastSlot : 1;
            } else if (idxGroup != null) {
                slot = Integer.parseInt(idxGroup);
            } else {
                slot = nextSeq++;
            }
            lastSlot = slot;
            if (slot > maxSlot) {
                maxSlot = slot;
            }
            slotValues.put(slot, sampleValueForConversion(conv.charAt(0)));
        }

        if (maxSlot == 0) {
            return new Object[0];
        }
        Object[] args = new Object[maxSlot];
        for (int s = 1; s <= maxSlot; s++) {
            args[s - 1] = slotValues.getOrDefault(s, "test");
        }
        return args;
    }

    private static Object sampleValueForConversion(char conv) {
        switch (Character.toLowerCase(conv)) {
            case 'd':
            case 'o':
            case 'x':
                return 42;
            case 'e':
            case 'f':
            case 'g':
            case 'a':
                return 3.14;
            case 'c':
                return 'A';
            case 'b':
                return Boolean.TRUE;
            case 't':
                return 0L;
            default:
                return "test";
        }
    }

    private static void checkCanonicalClassesPresent() throws IOException {
        Path actorsPath = ASSETS_DIR.resolve("messages/actors/actors.properties");
        Properties props = new Properties();
        try (BufferedReader br = new BufferedReader(new InputStreamReader(Files.newInputStream(actorsPath), StandardCharsets.UTF_8))) {
            props.load(br);
        }

        Map<String, String> expectedClasses = new LinkedHashMap<>();
        expectedClasses.put("actors.hero.heroclass.warrior", "janitor");
        expectedClasses.put("actors.hero.heroclass.mage", "lab tech");
        expectedClasses.put("actors.hero.heroclass.rogue", "security guard");
        expectedClasses.put("actors.hero.heroclass.huntress", "exterminator");
        expectedClasses.put("actors.hero.heroclass.duelist", "mechanic");
        expectedClasses.put("actors.hero.heroclass.cleric", "supervisor");

        expectedClasses.put("actors.hero.herosubclass.berserker", "scrubber");
        expectedClasses.put("actors.hero.herosubclass.gladiator", "polisher");
        expectedClasses.put("actors.hero.herosubclass.battlemage", "mixer");
        expectedClasses.put("actors.hero.herosubclass.warlock", "toxicologist");
        expectedClasses.put("actors.hero.herosubclass.assassin", "enforcer");
        expectedClasses.put("actors.hero.herosubclass.freerunner", "patrolman");
        expectedClasses.put("actors.hero.herosubclass.sniper", "sharpshooter");
        expectedClasses.put("actors.hero.herosubclass.warden", "groundskeeper");
        expectedClasses.put("actors.hero.herosubclass.champion", "foreman");
        expectedClasses.put("actors.hero.herosubclass.monk", "ergonomist");
        expectedClasses.put("actors.hero.herosubclass.priest", "auditor");
        expectedClasses.put("actors.hero.herosubclass.paladin", "inspector");

        for (Map.Entry<String, String> entry : expectedClasses.entrySet()) {
            String actual = props.getProperty(entry.getKey());
            if (!entry.getValue().equalsIgnoreCase(actual == null ? "" : actual.trim())) {
                throw new AssertionError("Expected " + entry.getKey() + "=" + entry.getValue() + ", got '" + actual + "'");
            }
        }
        System.out.println("  Verified all 6 canonical classes and 12 subclasses in actors.properties.");
    }
}
