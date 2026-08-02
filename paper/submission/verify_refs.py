#!/usr/bin/env python3
"""
Re-verify every entry in refs.bib against CrossRef.

For each @article, fetch the DOI's authoritative record and compare the
stored title, journal, year, volume and first author. Any disagreement
is printed and the script exits non-zero.

This exists because the paper argues that numbers which cannot be
re-derived from a source should not be trusted, and a hand-typed
bibliography is exactly such a number. Run it before submission:

    python3 verify_refs.py
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

BIB = Path(__file__).parent / "refs.bib"
UA = {"User-Agent": "genesis-audit/1.0 (mailto:mikarina@avadigital.ai)"}


def norm(s):
    s = re.sub(r"\{|\}|\\[`'\"^~]", "", str(s or "")).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def parse_bib(text):
    out = []
    for m in re.finditer(r"@article\{([^,]+),(.*?)\n\}", text, re.S):
        key, body = m.group(1), m.group(2)
        d = dict(re.findall(r"(\w+)\s*=\s*\{(.*?)\}(?:,|\s*$)", body, re.S))
        d["_key"] = key
        out.append(d)
    return out


def main():
    entries = parse_bib(BIB.read_text(encoding="utf-8"))
    print(f"verifying {len(entries)} entries against CrossRef\n")
    bad = 0
    for e in entries:
        doi = e.get("doi")
        if not doi:
            print(f"[NO DOI]  {e['_key']}")
            bad += 1
            continue
        try:
            req = urllib.request.Request(
                "https://api.crossref.org/works/" + doi, headers=UA)
            m = json.load(urllib.request.urlopen(req, timeout=30))["message"]
        except Exception as ex:
            print(f"[FETCH]   {e['_key']}: {doi} -> {ex}")
            bad += 1
            continue

        problems = []
        ct = (m.get("title") or [""])[0]
        if norm(ct) != norm(e.get("title")):
            problems.append(f"title: bib={e.get('title')!r} crossref={ct!r}")
        cy = str((m.get("issued", {}).get("date-parts") or [[None]])[0][0])
        if cy != str(e.get("year")):
            problems.append(f"year: bib={e.get('year')} crossref={cy}")
        cj = (m.get("container-title") or [""])[0]
        if cj and norm(cj) != norm(e.get("journal")):
            problems.append(f"journal: bib={e.get('journal')!r} crossref={cj!r}")
        if m.get("volume") and e.get("volume") and \
                str(m["volume"]) != str(e["volume"]):
            problems.append(f"volume: bib={e['volume']} crossref={m['volume']}")
        auth = m.get("author") or []
        if auth and auth[0].get("family"):
            if norm(auth[0]["family"]) not in norm(e.get("author")):
                problems.append(
                    f"first author {auth[0]['family']!r} not in bib author field")

        if problems:
            bad += 1
            print(f"[MISMATCH] {e['_key']} ({doi})")
            for p in problems:
                print(f"           {p}")
        else:
            print(f"[ok]      {e['_key']:14} {doi}")
        time.sleep(0.3)

    print()
    if bad:
        print(f"FAILED: {bad} of {len(entries)} entries need attention")
        return 1
    print(f"All {len(entries)} entries verified against CrossRef.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
