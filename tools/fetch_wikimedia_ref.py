#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import os
import re
import ssl
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from PIL import Image

USER_AGENT = "SPDModReferenceBot/1.0 (local workspace)"
SSL_CTX = ssl._create_unverified_context()
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
HTML_TAG_RE = re.compile(r"<[^>]+>")


def http_get_bytes(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
        return resp.read()


def commons_query(params: Dict[str, Any]) -> Dict[str, Any]:
    params = {**params, "format": "json"}
    qs = urllib.parse.urlencode(params)
    raw = http_get_bytes(f"{COMMONS_API}?{qs}")
    return json.loads(raw.decode("utf-8"))


def search_commons(query: str, limit: int) -> int:
    data = commons_query(
        {
            "action": "query",
            "list": "search",
            "srnamespace": 6,
            "srsearch": query,
            "srlimit": limit,
        }
    )
    results: List[Dict[str, Any]] = data.get("query", {}).get("search", [])
    if not results:
        print(f"No Wikimedia Commons results for: {query}")
        return 1
    for idx, item in enumerate(results, 1):
        title = item.get("title", "")
        snippet = HTML_TAG_RE.sub("", item.get("snippet", "")).strip()
        print(f"{idx}. {title}")
        if snippet:
            print(f"   {snippet[:160]}")
    return 0


def save_normalized_image(raw_bytes: bytes, output_path: str, max_size: int) -> Image.Image:
    im = Image.open(io.BytesIO(raw_bytes))
    ext = os.path.splitext(output_path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        elif im.mode == "L":
            im = im.convert("RGB")
    elif ext == ".png":
        if im.mode not in ("RGBA", "RGB"):
            im = im.convert("RGBA")
    else:
        im = im.convert("RGB")

    im.thumbnail((max_size, max_size), Image.LANCZOS)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    save_kwargs: Dict[str, Any] = {"quality": 90} if ext in (".jpg", ".jpeg") else {}
    im.save(output_path, **save_kwargs)
    return im


def download_commons_file(title: str, output_path: str, max_size: int) -> int:
    if not title.startswith("File:"):
        title = f"File:{title}"
    data = commons_query(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata",
            "iiurlwidth": max_size,
        }
    )
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {})
    if "missing" in page or not page.get("imageinfo"):
        print(f"ERROR: Could not find imageinfo for {title}")
        return 1

    info = page["imageinfo"][0]
    dl_url: Optional[str] = info.get("thumburl") or info.get("url")
    desc_url: str = info.get("descriptionurl", "")
    if not dl_url:
        print(f"ERROR: No downloadable URL for {title}")
        return 1

    raw = http_get_bytes(dl_url)
    im = save_normalized_image(raw, output_path, max_size)
    size_bytes = os.path.getsize(output_path)
    print(f"Saved {output_path} ({im.width}x{im.height}, {size_bytes} bytes)")
    print(f"Source: {desc_url or dl_url}")
    return 0


def download_direct_url(url: str, output_path: str, max_size: int) -> int:
    raw = http_get_bytes(url)
    im = save_normalized_image(raw, output_path, max_size)
    size_bytes = os.path.getsize(output_path)
    print(f"Saved {output_path} ({im.width}x{im.height}, {size_bytes} bytes)")
    print(f"Source: {url}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Search and fetch reference images into docs/refs/.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--search", help="Search Wikimedia Commons File: namespace")
    group.add_argument("--download", help="Wikimedia Commons File:... title to download")
    group.add_argument("--url", help="Direct image URL to download")
    parser.add_argument("--limit", type=int, default=8, help="Max search results (default: 8)")
    parser.add_argument("--output", help="Destination image path inside docs/refs/")
    parser.add_argument("--max-size", type=int, default=1024, help="Max width/height px (default: 1024)")
    args = parser.parse_args()

    if args.search:
        return search_commons(args.search, args.limit)
    if not args.output:
        parser.error("--output is required with --download or --url")
    if args.download:
        return download_commons_file(args.download, args.output, args.max_size)
    return download_direct_url(args.url, args.output, args.max_size)


if __name__ == "__main__":
    raise SystemExit(main())
