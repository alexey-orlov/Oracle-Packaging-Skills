#!/usr/bin/env python3
"""Find candidate photographs for one picture slot, from openly licensed sources only.

    search_photos.py "<search terms>" --out <dir> [--n 3] [--slot today]
                     [--source openverse|pexels|unsplash|auto] [--min-width 1600]
                     [--orientation landscape|any]

Downloads up to `--n` candidates into `--out`, each with a `.json` sidecar recording the source
page, the creator and the licence. Only licences that permit commercial use without attribution are
accepted (CC0, Public Domain Mark, the Pexels License, the Unsplash License); a result under any
other licence is dropped before it is downloaded, with a line on stderr saying so.

Exit codes: 0 candidates written · 1 the sources answered and had nothing · 2 everything found was
under a licence we may not use · 3 a source could not be reached (say "deferred", never "not
found") · 1 also for usage errors.
"""

from __future__ import annotations

import argparse
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from visuals_common import (  # noqa: E402
    EXIT_DEFERRED, EXIT_OK, Deferred, PHOTO_LICENCES,
    eprint, http_get, http_json, keychain, provenance_record,
    slugify, write_sidecar,
)

LETTERS = "ABCDEFGHIJ"


# ------------------------------------------------------------------------------------ openverse

def search_openverse(terms: str, want: int, min_width: int, orientation: str) -> list[dict]:
    """Openverse, restricted to CC0 and the Public Domain Mark. No key needed at this volume.

    A caution worth knowing before you read the results: Openverse's CC0/public-domain pool is
    dominated by Wikimedia, museum and government-archive material. It is good for machinery,
    infrastructure, vehicles, control rooms and industrial scenes, and thin on contemporary
    office/knowledge-work photography. When the terms describe a person at a screen, expect few or
    no usable candidates from here and say so rather than accepting a bad picture.
    """
    # Openverse's full-text search is strict: every word must appear, so a five-word description of
    # a scene returns nothing while its first two words return hundreds. Drop the trailing word
    # until it answers, and record the query that actually found each file.
    words = terms.split()
    data, used = None, terms
    while words:
        used = " ".join(words)
        data = http_json(
            "https://api.openverse.org/v1/images/"
            f"?q={urllib.parse.quote_plus(used)}&license=cc0,pdm&license_type=commercial"
            f"&size=large&page_size={max(want * 6, 12)}"
        )
        if data.get("results"):
            break
        if len(words) <= 2:
            break
        words = words[:-1]
    if used != terms:
        eprint(f"  openverse: nothing for the full phrase; answered on “{used}”")
    terms = used
    out, refused = [], 0
    for r in (data or {}).get("results", []):
        lic = (r.get("license") or "").lower()
        if lic not in PHOTO_LICENCES:
            refused += 1
            continue
        w, h = int(r.get("width") or 0), int(r.get("height") or 0)
        if w and w < min_width:
            continue
        if orientation == "landscape" and w and h and w < h:
            continue
        meta = PHOTO_LICENCES[lic]
        out.append(provenance_record(
            title=r.get("title"),
            creator=r.get("creator"),
            creator_url=r.get("creator_url"),
            source="Openverse / " + (r.get("source") or "?"),
            source_url=r.get("foreign_landing_url") or r.get("detail_url"),
            download_url=r.get("url"),
            licence=lic, licence_name=meta["name"], licence_url=meta["url"],
            attribution_required=meta["attribution_required"],
            width=w, height=h, terms=terms,
        ))
    if refused:
        eprint(f"  openverse: dropped {refused} result(s) under a licence we may not use")
    return out


# --------------------------------------------------------------------------------------- pexels

def search_pexels(terms: str, want: int, min_width: int, orientation: str) -> list[dict]:
    key = keychain("PEXELS_API_KEY")
    if not key:
        raise Deferred(
            "Pexels needs an API key and none is set: the environment variable PEXELS_API_KEY, "
            "or on a Mac the Keychain entry of that name "
            "(security add-generic-password -s PEXELS_API_KEY -a <you> -w <key>). "
            "Free at pexels.com/api."
        )
    q = urllib.parse.quote_plus(terms)
    url = (f"https://api.pexels.com/v1/search?query={q}&per_page={max(want * 4, 12)}"
           f"&size=large" + (f"&orientation=landscape" if orientation == "landscape" else ""))
    data = http_json(url, headers={"Authorization": key})
    meta = PHOTO_LICENCES["pexels"]
    out = []
    for p in data.get("photos", []):
        w, h = int(p.get("width") or 0), int(p.get("height") or 0)
        if w and w < min_width:
            continue
        src = p.get("src") or {}
        out.append(provenance_record(
            title=p.get("alt") or "-",
            creator=p.get("photographer"), creator_url=p.get("photographer_url"),
            source="Pexels", source_url=p.get("url"),
            download_url=src.get("large2x") or src.get("original") or src.get("large"),
            licence="pexels", licence_name=meta["name"], licence_url=meta["url"],
            attribution_required=meta["attribution_required"],
            width=w, height=h, terms=terms,
        ))
    return out


# ------------------------------------------------------------------------------------- unsplash

def search_unsplash(terms: str, want: int, min_width: int, orientation: str) -> list[dict]:
    """Official API when a key is set — the environment variable UNSPLASH_ACCESS_KEY, or on a Mac
    the Keychain entry of that name; otherwise the public search endpoint, which answers 307
    "Authorization required" without one — i.e. deferred."""
    q = urllib.parse.quote_plus(terms)
    key = keychain("UNSPLASH_ACCESS_KEY")
    if key:
        url = (f"https://api.unsplash.com/search/photos?query={q}&per_page={max(want * 4, 12)}"
               + (f"&orientation=landscape" if orientation == "landscape" else ""))
        data = http_json(url, headers={"Authorization": f"Client-ID {key}"})
    else:
        url = (f"https://unsplash.com/napi/search/photos?query={q}&per_page={max(want * 4, 12)}")
        data = http_json(url)  # raises Deferred on the 307/401 this endpoint gives without a key
    meta = PHOTO_LICENCES["unsplash"]
    out = []
    for p in (data.get("results") or []):
        w, h = int(p.get("width") or 0), int(p.get("height") or 0)
        if w and w < min_width:
            continue
        if orientation == "landscape" and w and h and w < h:
            continue
        user = p.get("user") or {}
        urls = p.get("urls") or {}
        out.append(provenance_record(
            title=p.get("alt_description") or p.get("description") or "-",
            creator=user.get("name"), creator_url=(user.get("links") or {}).get("html"),
            source="Unsplash", source_url=(p.get("links") or {}).get("html"),
            download_url=urls.get("raw") and urls["raw"] + "&w=2000" or urls.get("full"),
            licence="unsplash", licence_name=meta["name"], licence_url=meta["url"],
            attribution_required=meta["attribution_required"],
            width=w, height=h, terms=terms,
        ))
    return out


SOURCES = {"openverse": search_openverse, "pexels": search_pexels, "unsplash": search_unsplash}
# `auto` order: the sources that carry contemporary working-life photography first, then the
# archival pool. Each is tried until enough candidates are in hand.
AUTO_ORDER = ["pexels", "unsplash", "openverse"]


# ----------------------------------------------------------------------------------------- run

def download(rec: dict, out_dir: str, slot: str, letter: str) -> str | None:
    url = rec.get("download_url")
    if not url or url == "-":
        return None
    ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp"):
        ext = ".jpg"
    name = f"{slugify(slot)}-{letter}-{slugify(rec.get('title') or 'photo', 32)}{ext}"
    path = os.path.join(out_dir, name)
    try:
        blob = http_get(url, timeout=40)
    except Deferred as exc:
        eprint(f"  could not download {letter}: {exc}")
        return None
    except FileNotFoundError:
        eprint(f"  candidate {letter} has gone from the source (404); skipped")
        return None
    if len(blob) < 8000:
        eprint(f"  candidate {letter} came back suspiciously small ({len(blob)} bytes); skipped")
        return None
    with open(path, "wb") as fh:
        fh.write(blob)
    rec["file"] = path
    rec["slot"] = slot
    rec["kind"] = "photo"
    write_sidecar(path, rec)
    return path


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", help="the search terms, in one quoted string")
    ap.add_argument("--out", required=True, help="directory to write the candidates into")
    ap.add_argument("--n", type=int, default=3, help="how many candidates to download (default 3)")
    ap.add_argument("--slot", default="photo", help="the slot these are for, e.g. today / tomorrow")
    ap.add_argument("--source", default="auto", choices=["auto", *SOURCES])
    ap.add_argument("--min-width", type=int, default=1600)
    ap.add_argument("--orientation", default="landscape", choices=["landscape", "any"])
    args = ap.parse_args(argv)

    os.makedirs(args.out, exist_ok=True)
    order = AUTO_ORDER if args.source == "auto" else [args.source]

    found: list[dict] = []
    deferred: list[str] = []
    reached_any = False
    for name in order:
        if len(found) >= args.n:
            break
        try:
            hits = SOURCES[name](args.terms, args.n - len(found), args.min_width, args.orientation)
            reached_any = True
        except Deferred as exc:
            deferred.append(f"{name}: {exc}")
            eprint(f"  {name}: deferred — {exc}")
            continue
        eprint(f"  {name}: {len(hits)} usable result(s)")
        seen = {r.get("download_url") for r in found}
        for h in hits:
            if h.get("download_url") not in seen:
                found.append(h)
                seen.add(h.get("download_url"))
            if len(found) >= args.n:
                break

    if not reached_any:
        eprint("\nNo source could be reached. This is DEFERRED, not 'nothing found' — tell the "
               "owner the search could not run and why, and retry; never record it as an empty result.")
        for d in deferred:
            eprint("  - " + d)
        return EXIT_DEFERRED

    written = []
    for i, rec in enumerate(found[: args.n]):
        p = download(rec, args.out, args.slot, LETTERS[i])
        if p:
            written.append((LETTERS[i], rec, p))

    print(f"slot: {args.slot}   terms: {args.terms}")
    for letter, rec, path in written:
        print(f"  {letter}  {os.path.basename(path)}")
        print(f"     {rec['title'][:70]}")
        print(f"     {rec['creator']} · {rec['source']} · {rec['licence_name']} · "
              f"{rec['width']}×{rec['height']}")
        print(f"     {rec['source_url']}")
    if deferred:
        print("\ndeferred sources (not failures of the search — they were unreachable or need a key):")
        for d in deferred:
            print("  - " + d)
    if not written:
        if deferred:
            # Some sources never answered. The item is NOT settled: saying "nothing found" here
            # would close it forever on the strength of a missing key or a timeout.
            print("\nDEFERRED, not empty: the source(s) that answered had nothing under an allowed "
                  "licence, and the ones that carry this kind of picture could not be reached (see "
                  "above). Tell the owner which source is missing and what it needs, and retry.")
            return EXIT_DEFERRED
        print("\nnothing usable found under an allowed licence. Widen or change the terms and run "
              "again; do not lower the licence bar.")
        return 1
    print(f"\n{len(written)} candidate(s) in {args.out}")
    return EXIT_OK


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(130)
