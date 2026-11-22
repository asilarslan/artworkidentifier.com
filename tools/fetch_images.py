#!/usr/bin/env python3
"""Download public-domain / CC artwork images from Wikimedia Commons and record credits.

    python3 tools/fetch_images.py   # reads FILES from content/artworks.py, writes assets/art/*.webp + content/art_credits.json

Needs cwebp. Only Public domain, CC0 and CC BY/BY-SA licences are accepted (BY/BY-SA are credited on the page).
"""
import json, os, re, subprocess, sys, tempfile, urllib.parse, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from content.artworks import ART  # noqa: E402
UA = {"User-Agent": "ArtworkIdentifierSite/1.0 (asilarslan93@gmail.com)"}
OK = re.compile(r"^(Public domain|PD|CC0|CC BY(-SA)? \d)", re.I)

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()

credits_path = os.path.join(ROOT, "content", "art_credits.json")
credits = json.load(open(credits_path)) if os.path.exists(credits_path) else {}
for key, a in ART.items():
    out = os.path.join(ROOT, "assets", "art", key + ".webp")
    if os.path.exists(out) and key in credits and credits[key]["file"] == a["file"]:
        continue
    q = urllib.parse.urlencode({"action": "query", "format": "json", "prop": "imageinfo", "titles": "File:" + a["file"],
                                "iiprop": "url|extmetadata|size", "iiurlwidth": 1000,
                                "iiextmetadatafilter": "LicenseShortName|Artist"})
    p = next(iter(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values()))
    ii = p["imageinfo"][0]
    lic = ii["extmetadata"].get("LicenseShortName", {}).get("value", "")
    if not OK.match(lic):
        print("SKIP licence", key, lic); continue
    author = re.sub(r"<[^>]+>", "", ii["extmetadata"].get("Artist", {}).get("value", "")).strip()
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(ii["thumburl"])[1]) as tmp:
        tmp.write(get(ii["thumburl"])); tmp.flush()
        subprocess.run(["cwebp", "-quiet", "-q", "78", "-resize", "900", "0", tmp.name, "-o", out], check=True)
    w = 900; h = round(ii["height"] * 900 / ii["width"])
    credits[key] = {"file": a["file"], "license": lic, "author": author[:120], "page": ii["descriptionurl"], "w": w, "h": h}
    print("ok", key, lic)
json.dump(credits, open(credits_path, "w"), indent=1, ensure_ascii=False)
