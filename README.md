# artworkidentifier.com

Website for **Artwork Identifier** (iOS [id6642639717](https://apps.apple.com/app/id6642639717), Android [com.artworkidentifier](https://play.google.com/store/apps/details?id=com.artworkidentifier)). GitHub Pages, repo root, `main` = live.

## Build

```bash
python3 build.py              # regenerate all pages
python3 build.py --refresh    # refresh app version / min iOS
python3 build.py --ping       # after a deploy: submit all URLs to IndexNow
python3 tools/fetch_images.py # download new artwork images (Wikimedia Commons, PD/CC only) + credits
```

| Path | Source |
|---|---|
| `/`, `/tr/`, `/fr/`, `/de/`, `/es/` | `content/home.py` |
| Museum guides (`/museums/…`, `/tr/muzeler/…`, `/fr/musees/…`, `/de/museen/…`, `/es/museos/…`) | `content/artworks.py` (`MUSEUMS`, `ART`) |
| Art styles guide (`/art-styles/` + 4 languages) | `content/artworks.py` (`MOVEMENTS`) |
| Art style finder (`/art-style-finder/` + 4 languages) | `content/tool.py` + `assets/tool.js` |
| Guides (identify a painting, is my painting valuable) | `content/guides.py` |

Images: `assets/art/<key>.webp`, credits in `content/art_credits.json` and shown under every image. Only public-domain, CC0 or CC BY/BY-SA files are used.

## Content rules

- Store ratings are not shown; no invented reviews.
- Give museum wings/areas, not room numbers (they change).

App screens on the site (`assets/img/screen-<lang>-<n>.webp`) are rendered by `tools/screens.js` from `tools/screens.html` at iPhone 15/16 size; they mirror the app's chat screen.
