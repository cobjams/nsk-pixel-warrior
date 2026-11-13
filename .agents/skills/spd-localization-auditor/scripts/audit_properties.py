#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import os
import re
import subprocess
from typing import Dict, List, Optional, Tuple

MESSAGES_DIR = "core/src/main/assets/messages"

# Java java.util.Formatter syntax
PRINTF_TOKEN_RE = re.compile(
    r"%(?:(\d+)\$)?([-#+0,(<]*)?(\d+)?(?:\.(\d+))?(?:([bBhHsScCdoxXeEfgGaA%n])|([tT][HIklMSLNpzZsQBbhAaCYyjmdeRTrDFc]))"
)

FORBIDDEN_RPG_PATTERNS: List[Tuple[str, re.Pattern]] = [
    (term, re.compile(rf"\b{term}\b", re.IGNORECASE))
    for term in [
        "dungeon",
        "descend",
        "warrior",
        "mage",
        "rogue",
        "huntress",
        "duelist",
        "cleric",
        "berserker",
        "gladiator",
        "battlemage",
        "warlock",
        "assassin",
        "freerunner",
        "sniper",
        "warden",
        "champion",
        "monk",
        "paladin",
        "priest",
        "magic",
        "magical",
        "mana",
        "wand",
        "wands",
        "potion",
        "potions",
        "scroll",
        "scrolls",
        "yendor",
        "amulet",
    ]
]


def has_odd_trailing_backslashes(line: str) -> bool:
    count = 0
    for ch in reversed(line):
        if ch == "\\":
            count += 1
        else:
            break
    return (count % 2) == 1


def parse_properties(text: str) -> Tuple[Dict[str, str], List[str]]:
    """Parse a Java .properties file preserving logical multiline values."""
    entries: Dict[str, str] = {}
    duplicates: List[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.lstrip()
        if not stripped or stripped.startswith("#") or stripped.startswith("!"):
            i += 1
            continue

        buf = raw
        while has_odd_trailing_backslashes(buf) and i + 1 < len(lines):
            i += 1
            buf = buf[:-1] + lines[i].lstrip()

        if "=" in buf:
            key, val = buf.split("=", 1)
            key = key.strip()
            if key in entries:
                duplicates.append(key)
            entries[key] = val
        i += 1

    return entries, duplicates


def load_git_file(ref: str, relpath: str) -> Optional[str]:
    try:
        return subprocess.check_output(
            ["git", "show", f"{ref}:{relpath}"],
            stderr=subprocess.DEVNULL,
        ).decode("utf-8")
    except Exception:
        return None


def extract_format_signature(val: str) -> Tuple[List[str], List[str]]:
    """Return (ordered normalized specifier signatures, stray invalid % errors)."""
    # Strip escaped newlines so they don't confuse anything
    tokens: List[str] = []
    stray: List[str] = []

    pos = 0
    while True:
        idx = val.find("%", pos)
        if idx == -1:
            break
        m = PRINTF_TOKEN_RE.match(val, idx)
        if not m:
            stray.append(val[idx : idx + 8])
            pos = idx + 1
            continue
        arg_idx, flags, _width, _prec, conv1, conv2 = m.groups()
        conv = conv1 or conv2
        if conv not in ("%", "n"):
            # Normalize conversion family (e.g. d, s, f) + explicit positional index if any
            prefix = f"{arg_idx}$" if arg_idx else ""
            # Treat '<' relative index explicitly
            if flags and "<" in flags:
                prefix = "<"
            tokens.append(f"%{prefix}{conv}")
        pos = m.end()

    return tokens, stray


def normalize_spec_sequence(tokens: List[str]) -> Tuple[Dict[int, str], int]:
    """Map 1-based argument slot -> conversion char."""
    slots: Dict[int, str] = {}
    next_seq = 1
    last_idx = 0
    for tok in tokens:
        body = tok[1:]
        conv = body[-1]
        rest = body[:-1]
        if rest == "<":
            slot = last_idx if last_idx > 0 else 1
        elif rest.endswith("$"):
            slot = int(rest[:-1])
        else:
            slot = next_seq
            next_seq += 1
        last_idx = slot
        slots[slot] = conv
    return slots, len(tokens)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit SPD English .properties files against vanilla baseline.")
    parser.add_argument("--baseline-ref", default="v3.3.8", help="Git ref for baseline comparison (default: v3.3.8)")
    parser.add_argument("--file", help="Single relative file under messages/ (e.g., actors/actors.properties)")
    parser.add_argument("--lore-report", action="store_true", help="Report lingering RPG terms and long UI labels")
    parser.add_argument("--strict-lore", action="store_true", help="Exit non-zero if already-edited keys have RPG terms")
    parser.add_argument("--max-name-len", type=int, default=28, help="Warn on .name/.title/.short_name longer than N")
    args = parser.parse_args()

    if args.file:
        files = [os.path.join(MESSAGES_DIR, args.file)]
    else:
        files = sorted(glob.glob(os.path.join(MESSAGES_DIR, "**/*.properties"), recursive=True))

    if not files:
        print("No .properties files found.")
        return 1

    hard_errors = 0
    edited_lore_hits = 0

    for path in files:
        rel = path.replace("\\", "/")
        with open(path, "r", encoding="utf-8") as f:
            cur_text = f.read()
        cur_entries, dupes = parse_properties(cur_text)

        base_text = load_git_file(args.baseline_ref, rel)
        base_entries: Dict[str, str] = {}
        if base_text is not None:
            base_entries, _ = parse_properties(base_text)

        file_errors: List[str] = []
        for d in dupes:
            file_errors.append(f"DUPLICATE KEY: {d}")

        if base_text is not None:
            missing = sorted(set(base_entries.keys()) - set(cur_entries.keys()))
            extra = sorted(set(cur_entries.keys()) - set(base_entries.keys()))
            for k in missing:
                file_errors.append(f"MISSING KEY: {k}")
            for k in extra:
                file_errors.append(f"EXTRA KEY: {k}")

        edited_count = 0
        lore_edited_samples: List[str] = []
        lore_untouched_count = 0
        long_names: List[Tuple[str, int, str]] = []

        for key, cur_val in cur_entries.items():
            cur_tokens, cur_stray = extract_format_signature(cur_val)
            base_val = base_entries.get(key)
            is_edited = base_val is None or cur_val != base_val
            if is_edited:
                edited_count += 1

            if base_val is not None:
                base_tokens, base_stray = extract_format_signature(base_val)
                cur_slots, _ = normalize_spec_sequence(cur_tokens)
                base_slots, _ = normalize_spec_sequence(base_tokens)
                # SPD Messages.get() only invokes String.format() when args.length > 0;
                # 0-arg vanilla strings legitimately contain unescaped literal '%'.
                is_formatted_in_base = len(base_slots) > 0 and len(base_stray) == 0
                if is_formatted_in_base:
                    if cur_stray:
                        file_errors.append(f"STRAY '%' in {key}: {cur_stray}")
                    if cur_slots != base_slots:
                        file_errors.append(
                            f"FORMAT MISMATCH in {key}: baseline={base_slots} vs current={cur_slots}"
                        )
                elif cur_slots != base_slots:
                    file_errors.append(
                        f"FORMAT MISMATCH in {key}: baseline={base_slots} vs current={cur_slots}"
                    )

                # Underscore highlight parity check
                base_underscores = base_val.count("_")
                cur_underscores = cur_val.count("_")
                if base_underscores % 2 == 0 and cur_underscores % 2 != 0:
                    file_errors.append(
                        f"UNBALANCED '_' HIGHLIGHT in {key} (count={cur_underscores})"
                    )
            elif cur_stray:
                file_errors.append(f"STRAY '%' in {key}: {cur_stray}")

            if args.lore_report:
                hits = [term for term, pat in FORBIDDEN_RPG_PATTERNS if pat.search(cur_val)]
                if hits:
                    if is_edited:
                        edited_lore_hits += 1
                        if len(lore_edited_samples) < 8:
                            lore_edited_samples.append(f"    {key} -> {hits}")
                    else:
                        lore_untouched_count += 1

                if key.endswith((".name", ".title", ".short_name")):
                    plain = cur_val.replace("_", "").replace("\\n", " ")
                    if len(plain) > args.max_name_len:
                        long_names.append((key, len(plain), plain))

        status = "FAIL" if file_errors else "PASS"
        print(f"[{status}] {rel} (keys={len(cur_entries)}, edited={edited_count})")
        for err in file_errors:
            print(f"  ERROR: {err}")
        hard_errors += len(file_errors)

        if args.lore_report:
            print(
                f"  Lore audit: {len(lore_edited_samples)} edited-key hit(s) shown"
                f" (total edited hits={edited_lore_hits if args.file else 'see summary'}), "
                f"{lore_untouched_count} untouched vanilla key(s) with RPG terms"
            )
            for sample in lore_edited_samples:
                print(sample)
            if long_names:
                print(f"  Long UI labels (>{args.max_name_len} chars): {len(long_names)} (showing up to 5)")
                for k, ln, txt in long_names[:5]:
                    print(f"    {k} ({ln}): {txt}")

    print(f"\nSummary: {hard_errors} hard error(s), {edited_lore_hits} edited-key lore hit(s).")
    if hard_errors > 0:
        return 1
    if args.strict_lore and edited_lore_hits > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
