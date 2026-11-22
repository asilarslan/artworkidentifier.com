#!/usr/bin/env python3
"""Static site generator for artworkidentifier.com (GitHub Pages).

    python3 build.py              # build from content/
    python3 build.py --refresh    # refresh app version / min iOS from the App Store
    python3 build.py --ping       # after deploying: tell IndexNow (Bing, Yandex, ...) about all URLs
    python3 tools/fetch_images.py # download artwork images listed in content/artworks.py

Store ratings are deliberately not shown (low sample, mostly from early versions).
Legal pages (privacy-policy.html, terms-of-use.html) are hand-written and not generated.
"""
import datetime
import hashlib
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content.home import HOME, LANGS  # noqa: E402
from content.guides import GUIDES, STYLES, MUSEUM_HUBS  # noqa: E402
from content.artworks import ART, MUSEUMS, MOVEMENTS  # noqa: E402
from content.tool import QUESTIONS, TEXT as TOOL  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://artworkidentifier.com"
APP_ID = "6642639717"
APP_NAME = "Artwork Identifier"
PLAY_ID = "com.artworkidentifier"
# App Store Connect → App Analytics → Campaigns shows this provider token.
PROVIDER_TOKEN = ""
INDEXNOW_KEY = "ee4ac2edc779d9549227e4774d1d3c71"
TODAY = datetime.date.today().isoformat()
SUPPORT = "asilarslan93@gmail.com"
RTL = set()
CREDITS = json.load(open(os.path.join(ROOT, "content", "art_credits.json")))

esc = html.escape


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def version(path):
    return hashlib.sha1(read(path).encode()).hexdigest()[:8]


def load_app(refresh):
    path = os.path.join(ROOT, "content", "app.json")
    if refresh or not os.path.exists(path):
        url = f"https://itunes.apple.com/lookup?id={APP_ID}&country=us"
        r = json.load(urllib.request.urlopen(url, timeout=20))["results"][0]
        data = {"min_os": r["minimumOsVersion"], "version": r["version"], "fetched": TODAY}
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    with open(path) as f:
        return json.load(f)


def store_url(campaign):
    q = f"?ct={campaign}&mt=8"
    if PROVIDER_TOKEN:
        q = f"?pt={PROVIDER_TOKEN}&ct={campaign}&mt=8"
    return f"https://apps.apple.com/app/apple-store/id{APP_ID}{q}"


def play_url(campaign):
    ref = urllib.parse.quote(f"utm_source=artworkidentifier.com&utm_medium=web&utm_campaign={campaign}", safe="")
    return f"https://play.google.com/store/apps/details?id={PLAY_ID}&referrer={ref}"


def svg_width(path, height=54):
    m = re.search(r'<svg[^>]*?width="([\d.]+)"[^>]*?height="([\d.]+)"', read(path)[:600])
    return round(float(m.group(1)) * height / float(m.group(2))) if m else 162


def badge(t, campaign):
    apple = f"assets/img/app-store-{t['badge']}.svg"
    play_w = 164 if t["play"] == "en" else 180
    return (f'<a class="badge" href="{store_url(campaign)}" rel="noopener">'
            f'<img src="/{apple}" alt="Download on the App Store" width="{svg_width(apple)}" height="54"></a>'
            f'<a class="badge" href="{play_url(campaign)}" rel="noopener">'
            f'<img src="/assets/img/play-{t["play"]}.webp" alt="Get it on Google Play" width="{play_w}" height="54"></a>')


def app_link(campaign, cls, inner):
    """One button that opens the App Store, or Google Play on Android (swapped in site.js)."""
    return (f'<a class="{cls}" href="{store_url(campaign)}" data-play="{esc(play_url(campaign))}" rel="noopener">'
            f'{inner}</a>')


def home_path(lang):
    return "/" if lang == "en" else f"/{lang}/"


def slug(path):
    return path.strip("/").replace("/", "-") or "home"


def qr(text, cls="qr", size=84):
    return (f'<div class="{cls}"><img src="/assets/img/qr-app-store.svg" alt="QR code" width="{size}" height="{size}" '
            f'loading="lazy"><span>{esc(text)}</span></div>')


def tr_(d, lang):
    return d.get(lang) or d["en"]


def museums_in(lang):
    """Museum guides available in a language (falls back to English ones)."""
    own = [(k, m) for k, m in MUSEUMS.items() if lang in m["paths"]]
    return own if own else [(k, m) for k, m in MUSEUMS.items()]


def museum_hub(lang):
    return MUSEUM_HUBS[lang]["path"]


def guides_for(lang):
    return [g for g in GUIDES if g["lang"] == lang] or [g for g in GUIDES if g["lang"] == "en"]


def guide_alts(g):
    return {x["lang"]: x["path"] for x in GUIDES if x["key"] == g["key"]}


def header(lang, alts):
    t = HOME[lang]
    n = t["nav"]
    opts = "".join(
        f'<option value="{alts.get(l, home_path(l))}"{" selected" if l == lang else ""}>{HOME[l]["name"]}</option>'
        for l in LANGS)
    return f"""<header class="top"><div class="wrap">
<a class="brand" href="{home_path(lang)}"><img src="/assets/img/icon-64.png" alt="" width="32" height="32">Artwork Identifier</a>
<nav>
<a class="hide-sm" href="{museum_hub(lang)}">{n['museums']}</a>
<a class="hide-sm" href="{STYLES[lang]['path']}">{n['styles']}</a>
<a class="hide-sm" href="{TOOL[lang]['path']}">{n['tool']}</a>
<select class="lang" aria-label="Language">{opts}</select>
{app_link('web-nav-' + lang, 'get', n['get'])}
</nav></div></header>"""


def footer(lang):
    t = HOME[lang]
    guides = "".join(f'<li><a href="{g["path"]}">{esc(g["h1"])}</a></li>' for g in guides_for(lang))
    guides += f'<li><a href="{STYLES[lang]["path"]}">{esc(STYLES[lang]["h1"])}</a></li>'
    guides += f'<li><a href="{TOOL[lang]["path"]}">{esc(TOOL[lang]["h1"])}</a></li>'
    mus = "".join(f'<li><a href="{tr_(m["paths"], lang)}">{esc(tr_(m["name"], lang)[0].upper() + tr_(m["name"], lang)[1:])}</a></li>'
                  for k, m in museums_in(lang))
    langs = "".join(f'<li><a href="{home_path(l)}" hreflang="{l}">{HOME[l]["name"]}</a></li>' for l in LANGS)
    return f"""<footer><div class="wrap cols">
<div><div class="h">{t['footer_app']}</div><ul>
<li><a href="{store_url('web-footer-' + lang)}" rel="noopener">App Store</a></li>
<li><a href="{play_url('web-footer-' + lang)}" rel="noopener">Google Play</a></li>
<li><a href="mailto:{SUPPORT}">{t['support']}</a></li></ul></div>
<div><div class="h">{t['footer_museums']}</div><ul>{mus}</ul></div>
<div><div class="h">{t['footer_guides']}</div><ul>{guides}</ul></div>
<div><div class="h">Language</div><ul>{langs}</ul></div>
<div><div class="h">{t['footer_legal']}</div><ul>
<li><a href="/privacy-policy.html">{t['privacy']}</a></li>
<li><a href="/terms-of-use.html">{t['terms']}</a></li></ul>
<p style="margin-top:12px">© {datetime.date.today().year} {t['copyright']}</p></div>
</div></footer>"""


def sticky(lang, where):
    return f'<div class="sticky-cta">{app_link("web-sticky-" + where, "btn btn-primary", esc(HOME[lang]["sticky"]))}</div>'


def cta_band(lang, where, extra=""):
    t = HOME[lang]
    return f"""<section><div class="wrap"><div class="cta-band">
<h2>{esc(t['cta_h2'])}</h2><p>{esc(t['cta_p'])}</p>
<div class="ctas">{badge(t, 'web-bottom-' + where)}{extra}</div>
</div></div></section>"""


def faq_html(title, items):
    rows = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in items)
    return f'<h2>{esc(title)}</h2><div class="faq">{rows}</div>'


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


PD = {"tr": "Kamu malı", "fr": "Domaine public", "de": "Gemeinfrei", "es": "Dominio público"}


def credit(key, lang):
    c = CREDITS[key]
    lic = PD.get(lang, c["license"]) if c["license"].lower() == "public domain" else c["license"]
    who = f" · {esc(c['author'])}" if not c["license"].lower().startswith(("public domain", "pd")) and c["author"] else ""
    return (f'<a class="credit" href="{esc(c["page"])}" rel="noopener">{HOME[lang]["credit"]}: {esc(lic)}{who} · Wikimedia Commons</a>')


def art_img(key, alt, lang, *, eager=False, cls=""):
    c = CREDITS[key]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<figure class="art{(" " + cls) if cls else ""}"><img src="/assets/art/{key}.webp" alt="{esc(alt)}" width="{c["w"]}" '
            f'height="{c["h"]}" {load} decoding="async">{credit(key, lang)}</figure>')


def art_ld(key, lang, museum=None):
    a = ART[key]
    d = {"@type": "VisualArtwork", "name": tr_(a["t"], lang), "creator": {"@type": "Person", "name": a["artist"]},
         "dateCreated": a["year"], "image": f"{SITE}/assets/art/{key}.webp"}
    if museum:
        d["contentLocation"] = {"@type": "Museum", "name": tr_(museum["name"], "en").replace("the ", "").strip(),
                                "address": museum["city"]}
    return d


def page(lang, title, desc, path, body, *, alternates=None, jsonld=(), preload="", tool=False, og_type="website",
         robots="index, follow, max-image-preview:large"):
    t = HOME[lang]
    url = SITE + path
    alt = ""
    if alternates:
        alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{p}">' for l, p in alternates.items())
        if "en" in alternates:
            alt += f'<link rel="alternate" hreflang="x-default" href="{SITE}{alternates["en"]}">'
    scripts = f'<script src="/assets/site.js?v={version("assets/site.js")}" defer></script>'
    if tool:
        scripts += f'<script src="/assets/tool.js?v={version("assets/tool.js")}" defer></script>'
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
{alt}
<meta name="robots" content="{robots}">
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Artwork Identifier">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{t['locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/og.jpg">
<link rel="icon" href="/assets/img/icon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="manifest" href="/manifest.json">
{preload}
<style>{read('assets/site.css')}</style>
{''.join(ld(j) for j in jsonld)}
</head>
<body>
{body}
{scripts}
</body>
</html>
"""


def app_ld(app, lang):
    return [{
        "@context": "https://schema.org", "@type": "MobileApplication", "name": APP_NAME,
        "operatingSystem": f"iOS {app['min_os']} or later", "applicationCategory": "EducationalApplication",
        "url": SITE + home_path(lang), "downloadUrl": f"https://apps.apple.com/app/id{APP_ID}",
        "image": f"{SITE}/assets/img/icon-512.png",
        "screenshot": [f"{SITE}/assets/img/screen-{lang}-{i}.webp" for i in (1, 2, 3)],
        "softwareVersion": app["version"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    }, {
        "@context": "https://schema.org", "@type": "MobileApplication", "name": APP_NAME, "operatingSystem": "Android",
        "applicationCategory": "EducationalApplication", "url": SITE + home_path(lang),
        "downloadUrl": f"https://play.google.com/store/apps/details?id={PLAY_ID}",
        "image": f"{SITE}/assets/img/icon-512.png", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    }]


def device(n, alt, lang, eager=False, small=False):
    """App screen (rendered by tools/screens.js at iPhone 15/16 size) inside a thin modern iPhone frame."""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<div class="device{" small" if small else ""}"><img src="/assets/img/screen-{lang}-{n}.webp" alt="{esc(alt)}" '
            f'width="645" height="1398" {load}></div>')


def card(href, title, text, img=None):
    pic = f'<img src="/assets/art/{img}.webp" alt="" loading="lazy" decoding="async">' if img else ""
    return f'<a class="mcard" href="{href}">{pic}<b>{esc(title)}</b><span>{esc(text)}</span></a>'


def museum_cards(lang):
    out = []
    for k, m in museums_in(lang):
        name = tr_(m["name"], lang)
        out.append(card(tr_(m["paths"], lang), name[0].upper() + name[1:] + " · " + m["city"],
                        tr_(m["intro"], lang)[:110].rsplit(" ", 1)[0] + "…", m["works"][0]))
    return "".join(out)


def guide_cards(lang):
    out = [card(g["path"], g["h1"], g["desc"][:110].rsplit(" ", 1)[0] + "…", g.get("img")) for g in guides_for(lang)]
    out.append(card(STYLES[lang]["path"], STYLES[lang]["h1"], STYLES[lang]["desc"][:110].rsplit(" ", 1)[0] + "…", "starry-night"))
    out.append(card(TOOL[lang]["path"], TOOL[lang]["h1"], TOOL[lang]["desc"][:110].rsplit(" ", 1)[0] + "…", "composition-vii"))
    return "".join(out)


def build_home(lang, app):
    t = HOME[lang]
    fmt = {"min_os": app["min_os"]}
    examples = "".join(
        f'<figure>{device(i, t["shots_alt"][i - 1], lang)}'
        f'<figcaption><b>{esc(name)}</b>{esc(why)}</figcaption></figure>' for i, name, why in t["examples"])
    steps = "".join(f'<div class="card"><div class="num">{i}</div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>'
                    for i, (a, b) in enumerate(t["steps"], 1))
    feats = "".join(f'<div class="card"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in t["features"])
    strip = "".join(f'<a href="{STYLES[lang]["path"]}#{k}"><img src="/assets/art/{img}.webp" alt="{esc(tr_(n, lang))}" loading="lazy"><span>{esc(tr_(n, lang))}</span></a>'
                    for k, n, y, img, c in MOVEMENTS if img)
    alts = {l: home_path(l) for l in LANGS}
    body = f"""{header(lang, alts)}
<main>
<section class="hero" data-hero><div class="wrap">
<div>
<h1>{esc(t['h1'])}</h1>
<p class="sub">{esc(t['sub'])}</p>
<div class="ctas">{badge(t, 'web-hero-' + lang)}</div>
<p class="compat">{esc(t['compat'].format(**fmt))}</p>
<p style="margin-top:14px"><a href="{museum_hub(lang)}" style="font-weight:600">{esc(t['museums_h2'])} →</a></p>
{qr(t['qr'])}
</div>
<div class="media">{device(1, t['hero_alt'], lang, eager=True)}</div>
</div></section>

<section><div class="wrap">
<h2>{esc(t['museums_h2'])}</h2><p class="lead">{esc(t['museums_lead'])}</p>
<div class="mcards">{museum_cards(lang)}</div>
</div></section>

<section class="alt"><div class="wrap">
<h2>{esc(t['styles_h2'])}</h2><p class="lead">{esc(t['styles_lead'])}</p>
<div class="strip">{strip}</div>
<div class="ctas"><a class="btn btn-primary" href="{STYLES[lang]['path']}">{esc(t['styles_btn'])}</a>
<a class="btn btn-ghost" href="{TOOL[lang]['path']}">{esc(t['tool_btn'])}</a></div>
</div></section>

<section><div class="wrap">
<h2>{esc(t['examples_h2'])}</h2><p class="lead">{esc(t['examples_lead'])}</p>
<div class="examples">{examples}</div>
</div></section>

<section id="how" class="alt"><div class="wrap">
<h2>{esc(t['how_h2'])}</h2>
<div class="grid3" style="margin-top:24px">{steps}</div>
<h2 style="margin-top:56px">{esc(t['features_h2'])}</h2>
<div class="grid3" style="margin-top:24px">{feats}</div>
</div></section>

<section><div class="wrap">
<h2>{esc(t['guides_h2'])}</h2>
<div class="mcards" style="margin-top:20px">{guide_cards(lang)}</div>
</div></section>

<section id="faq" class="alt"><div class="wrap narrow">{faq_html(t['faq_h2'], t['faq'])}</div></section>
{cta_band(lang, lang)}
</main>
{footer(lang)}
{sticky(lang, lang)}"""
    jsonld = [*app_ld(app, lang), {"@context": "https://schema.org", "@type": "WebSite", "name": APP_NAME,
                                   "url": SITE + home_path(lang), "inLanguage": lang}]
    out = page(lang, t["title"], t["desc"], home_path(lang), body, alternates=alts, jsonld=jsonld,
               preload=f'<link rel="preload" as="image" href="/assets/img/screen-{lang}-1.webp" fetchpriority="high">')
    write("index.html" if lang == "en" else f"{lang}/index.html", out)


def article(lang, *, path, title, desc, h1, intro, body_html, faq, alts, crumb, kind, top="", hero=None, shot=None,
            tool=False, extra_ld=(), related="", og=None):
    t = HOME[lang]
    where = slug(path)
    crumbs = (f'<nav class="crumbs"><a href="{home_path(lang)}">{t["home"]}</a> › '
              + (f'<a href="{crumb[1]}">{esc(crumb[0])}</a> › ' if crumb else "") + f'{esc(h1)}</nav>')
    inline = f'<div class="inline-cta"><p>{esc(t["inline_cta"])}</p>{badge(t, "web-inline-" + where)}</div>'
    shot_html = ""
    if shot:
        shot_html = (f'<div class="guide-shot">{device(shot, t["shots_alt"][shot - 1], lang, small=True)}'
                     f'<div><p>{esc(t["shot_cta"])}</p>{badge(t, "web-shot-" + where)}</div></div>')
    updated = f'<p style="font-size:.85rem;color:var(--muted);margin-top:10px">{t["updated"]}: {TODAY}</p>' if kind == "guide" else ""
    hero_html = f'<div class="wrap narrow" style="margin-top:18px">{art_img(hero, tr_(ART[hero]["t"], lang), lang, eager=True, cls="wide")}</div>' if hero else ""
    body = f"""{header(lang, alts)}
<main>
<section class="article" data-hero><div class="wrap narrow">
{crumbs}
<h1>{esc(h1)}</h1>
<p class="intro">{esc(intro)}</p>
{updated}
</div>{hero_html}</section>
{top}
<section style="padding-top:24px"><div class="wrap narrow prose">
{body_html}
{shot_html or inline}
<div id="faq">{faq_html(t['faq_h2'], faq) if faq else ''}</div>
</div></section>
{related}
{cta_band(lang, where, f'<a class="btn btn-ghost" href="{home_path(lang)}">{esc(t["back"])}</a>')}
</main>
{footer(lang)}
{sticky(lang, where)}"""
    crumbs_ld = [{"@type": "ListItem", "position": 1, "name": t["home"], "item": SITE + home_path(lang)}]
    if crumb:
        crumbs_ld.append({"@type": "ListItem", "position": 2, "name": crumb[0], "item": SITE + crumb[1]})
    crumbs_ld.append({"@type": "ListItem", "position": len(crumbs_ld) + 1, "name": h1, "item": SITE + path})
    jsonld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs_ld}, *extra_ld]
    if kind == "guide":
        jsonld.append({
            "@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc, "inLanguage": lang,
            "dateModified": TODAY, "mainEntityOfPage": SITE + path,
            "image": f"{SITE}/assets/art/{hero or og}.webp" if (hero or og) else f"{SITE}/assets/img/og.jpg",
            "author": {"@type": "Organization", "name": APP_NAME, "url": SITE + "/"},
            "publisher": {"@type": "Organization", "name": APP_NAME,
                          "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/icon-512.png"}}})
    out = page(lang, title, desc, path, body, alternates=alts if len(alts) > 1 else None, jsonld=jsonld, tool=tool,
               og_type="article" if kind == "guide" else "website")
    if hero or og:
        out = out.replace(f'content="{SITE}/assets/img/og.jpg"', f'content="{SITE}/assets/art/{hero or og}.webp"')
    write(path.strip("/") + "/index.html", out)


def related_museums(lang, skip=None):
    cards = "".join(card(tr_(m["paths"], lang), (tr_(m["name"], lang)[0].upper() + tr_(m["name"], lang)[1:]) + " · " + m["city"],
                         tr_(m["intro"], lang)[:100].rsplit(" ", 1)[0] + "…", m["works"][0])
                    for k, m in museums_in(lang) if k != skip)
    return f'<section class="alt"><div class="wrap"><h2>{HOME[lang]["related"]}</h2><div class="mcards" style="margin-top:20px">{cards}</div></div></section>'


# Names people actually search for, used in English <title>s.
SEO_NAMES = {"louvre": "Louvre", "orsay": "Musée d'Orsay", "met": "Met Museum", "uffizi": "Uffizi Gallery",
             "rijksmuseum": "Rijksmuseum", "prado": "Prado Museum", "national-gallery": "National Gallery London",
             "vatican": "Vatican Museums"}


def build_museum(key, lang):
    m = MUSEUMS[key]
    t = HOME[lang]
    name = tr_(m["name"], lang)
    Name = name[0].upper() + name[1:]
    n = len(m["works"])
    first = ", ".join(tr_(ART[w]["t"], lang) for w in m["works"][:3])
    items = []
    for i, w in enumerate(m["works"], 1):
        a = ART[w]
        title_ = tr_(a["t"], lang)
        items.append(f"""<article class="work" id="{w}"><div class="wimg">{art_img(w, f"{title_} — {a['artist']}", lang)}</div>
<div><h3><span class="wn">{i}</span>{esc(title_)}</h3><p class="meta">{esc(a['artist'])} · {esc(a['year'])}</p>
<p><b>{t['look']}:</b> {esc(tr_(a['d'], lang))}</p></div></article>""")
    tips = "".join(f"<li>{esc(x)}</li>" for x in tr_(m["tips"], lang))
    top = f'<section style="padding:8px 0 0"><div class="wrap narrow"><h2>{t["list_h2"]}</h2><div class="works">{"".join(items)}</div></div></section>'
    body_html = f'<h2>{t["tips_h2"]}</h2><ul>{tips}</ul>'
    alts = dict(m["paths"])
    ld_list = {"@context": "https://schema.org", "@type": "ItemList", "name": t["museum_h1"].format(n=n, name=name),
               "itemListElement": [{"@type": "ListItem", "position": i, "item": art_ld(w, lang, m)} for i, w in enumerate(m["works"], 1)]}
    article(lang, path=m["paths"][lang], title=t["museum_title"].format(n=n, name=SEO_NAMES[key] if lang == "en" else Name, city=m["city"]),
            desc=t["museum_desc"].format(n=n, name=name, city=m["city"], works=first),
            h1=t["museum_h1"].format(n=n, name=name if not t["museum_h1"].startswith("{name}") else Name),
            intro=tr_(m["intro"], lang), body_html=body_html, faq=None, alts=alts, crumb=(t["museums_hub"], museum_hub(lang)),
            kind="guide", top=top, og=m["works"][0], extra_ld=[ld_list], related=related_museums(lang, key))


def build_museum_hub(lang):
    t = HOME[lang]
    h = MUSEUM_HUBS[lang]
    alts = {l: MUSEUM_HUBS[l]["path"] for l in LANGS}
    body = f"""{header(lang, alts)}
<main>
<section class="article" data-hero><div class="wrap">
<nav class="crumbs"><a href="{home_path(lang)}">{t['home']}</a> › {esc(h['h1'])}</nav>
<h1>{esc(h['h1'])}</h1><p class="intro">{esc(h['intro'])}</p>
<div class="mcards" style="margin-top:28px">{museum_cards(lang)}</div>
</div></section>
{cta_band(lang, slug(h['path']))}
</main>
{footer(lang)}
{sticky(lang, slug(h['path']))}"""
    items = [{"@type": "ListItem", "position": i, "url": SITE + tr_(m["paths"], lang), "name": tr_(m["name"], lang)}
             for i, (k, m) in enumerate(museums_in(lang), 1)]
    write(h["path"].strip("/") + "/index.html",
          page(lang, h["title"], h["desc"], h["path"], body, alternates=alts,
               jsonld=[{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": items}]))


def build_styles(lang):
    s = STYLES[lang]
    toc = "".join(f'<a href="#{k}">{esc(tr_(n, lang))}</a>' for k, n, y, img, c in MOVEMENTS)
    secs = []
    for k, n, y, img, c in MOVEMENTS:
        pic = ""
        if img:
            a = ART[img]
            pic = f'{art_img(img, tr_(a["t"], lang), lang)}<p class="meta">{s["example"]}: <i>{esc(tr_(a["t"], lang))}</i>, {esc(a["artist"])}, {esc(a["year"])}</p>'
        secs.append(f'<section class="mv" id="{k}"><h2>{esc(tr_(n, lang))}</h2><p class="meta">{s["years"]}: {esc(y)}</p>'
                    f'<p><b>{s["clue"]}:</b> {esc(tr_(c, lang))}</p>{pic}</section>')
    top = f'<section style="padding:8px 0 0"><div class="wrap narrow"><nav class="toc">{toc}</nav>{"".join(secs)}</div></section>'
    article(lang, path=s["path"], title=s["title"], desc=s["desc"], h1=s["h1"], intro=s["intro"],
            body_html=f'<p><a href="{TOOL[lang]["path"]}">{esc(TOOL[lang]["h1"])} →</a></p>', faq=None,
            alts={l: STYLES[l]["path"] for l in LANGS}, crumb=None, kind="guide", top=top, hero=None,
            related=related_museums(lang))


def build_tool(lang):
    tt = TOOL[lang]
    qs = []
    for qkey, opts in QUESTIONS:
        btns = "".join(f'<button type="button" data-m="{" ".join(ms)}" aria-pressed="false">{esc(tt["o"][o])}</button>' for o, ms in opts)
        qs.append(f'<div class="q"><p>{esc(tt["q"][qkey])}</p><div class="opts">{btns}</div></div>')
    cards = []
    for k, n, y, img, c in MOVEMENTS:
        pic = f'<img src="/assets/art/{img}.webp" alt="" loading="lazy">' if img else ""
        cards.append(f'<a class="mvcard" data-key="{k}" href="{STYLES[lang]["path"]}#{k}" hidden>{pic}<div><b>{esc(tr_(n, lang))}</b>'
                     f'<span>{esc(y)}</span><p>{esc(tr_(c, lang))}</p><em>{esc(tt["more"])}</em></div></a>')
    data = json.dumps({"need": tt["need"]}, ensure_ascii=False)
    tool_html = f"""<div class="tool" data-tool data-result="{esc(tt['result'])}">
<script type="application/json" class="tool-i18n">{data}</script>
{''.join(qs)}
<div class="result" data-out aria-live="polite"><div class="lvl" data-lvl>{esc(tt['need'])}</div><div class="mvcards">{''.join(cards)}</div></div>
<div class="upsell"><strong>{esc(tt['upsell'])}</strong><p>{esc(tt['upsell_p'])}</p>
{app_link('web-tool-' + lang, 'btn btn-primary', esc(tt['btn']))}{qr(HOME[lang]['qr'], 'qr-mini', 72)}</div>
<p style="margin-top:12px"><button type="button" class="btn btn-ghost" data-reset style="min-height:40px">{esc(tt['reset'])}</button></p>
</div>"""
    top = f'<section class="alt" style="padding:32px 0"><div class="wrap narrow">{tool_html}</div></section>'
    ld_app = {"@context": "https://schema.org", "@type": "WebApplication", "name": tt["h1"], "url": SITE + tt["path"],
              "applicationCategory": "EducationalApplication", "operatingSystem": "Any (web browser)",
              "isAccessibleForFree": True, "inLanguage": lang, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    article(lang, path=tt["path"], title=tt["title"], desc=tt["desc"], h1=tt["h1"], intro=tt["intro"], body_html=tt["body"],
            faq=tt["faq"], alts={l: TOOL[l]["path"] for l in LANGS}, crumb=None, kind="tool", top=top, tool=True,
            extra_ld=[ld_app], related=related_museums(lang))


def build_guide(g):
    lang = g["lang"]
    t = HOME[lang]
    article(lang, path=g["path"], title=g["title"], desc=g["desc"], h1=g["h1"], intro=g["intro"], body_html=g["body"],
            faq=g["faq"], alts=guide_alts(g), crumb=None, kind="guide", hero=g.get("img"), shot=g.get("shot"),
            related=related_museums(lang))


def build_get():
    """QR target: Android opens Google Play, everything else the App Store."""
    ios, play = store_url("web-qr"), play_url("web-qr")
    write("get/index.html", f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Get Artwork Identifier</title><meta name="robots" content="noindex">
<script>location.replace(/android/i.test(navigator.userAgent) ? {json.dumps(play)} : {json.dumps(ios)});</script>
</head><body style="font-family:-apple-system,sans-serif;text-align:center;padding:40px">
<p><a href="{esc(ios)}">App Store</a> · <a href="{esc(play)}">Google Play</a></p></body></html>
""")


def build_404():
    body = f"""{header('en', {})}
<main><section class="article"><div class="wrap narrow">
<h1>Page not found</h1>
<p class="intro">The page you're looking for doesn't exist. Try a museum guide or the art styles guide.</p>
<div class="ctas"><a class="btn btn-primary" href="/museums/">Museum guides</a><a class="btn btn-ghost" href="/art-styles/">Art styles</a></div>
</div></section></main>
{footer('en')}"""
    write("404.html", page("en", "Page not found | Artwork Identifier", "This page doesn't exist.", "/404.html", body,
                           robots="noindex"))


def all_urls():
    e = [(home_path(l), "1.0" if l == "en" else "0.9", {x: home_path(x) for x in LANGS}) for l in LANGS]
    e += [(MUSEUM_HUBS[l]["path"], "0.8", {x: MUSEUM_HUBS[x]["path"] for x in LANGS}) for l in LANGS]
    e += [(STYLES[l]["path"], "0.8", {x: STYLES[x]["path"] for x in LANGS}) for l in LANGS]
    e += [(TOOL[l]["path"], "0.8", {x: TOOL[x]["path"] for x in LANGS}) for l in LANGS]
    for m in MUSEUMS.values():
        e += [(p, "0.8", dict(m["paths"]) if len(m["paths"]) > 1 else {}) for p in m["paths"].values()]
    e += [(g["path"], "0.7", guide_alts(g) if len(guide_alts(g)) > 1 else {}) for g in GUIDES]
    e += [("/privacy-policy.html", "0.3", {}), ("/terms-of-use.html", "0.3", {})]
    return e


def build_meta():
    rows = []
    for path, prio, alts in all_urls():
        x = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{p}"/>' for l, p in alts.items())
        if "en" in alts:
            x += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{alts["en"]}"/>'
        rows.append(f"  <url>\n    <loc>{SITE}{path}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{prio}</priority>{x}\n  </url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(rows) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write(f"{INDEXNOW_KEY}.txt", INDEXNOW_KEY)
    write("manifest.json", json.dumps({
        "name": APP_NAME, "short_name": APP_NAME,
        "description": "Identify any painting or artwork from a photo, plus museum guides and an art styles guide.",
        "start_url": "/", "display": "browser", "background_color": "#ffffff", "theme_color": "#ffffff",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}],
        "related_applications": [{"platform": "itunes", "url": f"https://apps.apple.com/app/id{APP_ID}"},
                                 {"platform": "play", "id": PLAY_ID,
                                  "url": f"https://play.google.com/store/apps/details?id={PLAY_ID}"}],
    }, indent=2) + "\n")


def ping_indexnow():
    body = json.dumps({"host": urllib.parse.urlparse(SITE).netloc, "key": INDEXNOW_KEY,
                       "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt",
                       "urlList": [SITE + p for p, _, _ in all_urls()]}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    print("IndexNow:", urllib.request.urlopen(req, timeout=20).status)


def main():
    if "--ping" in sys.argv:
        return ping_indexnow()
    app = load_app("--refresh" in sys.argv)
    for lang in LANGS:
        build_home(lang, app)
        build_museum_hub(lang)
        build_styles(lang)
        build_tool(lang)
    for key, m in MUSEUMS.items():
        for lang in m["paths"]:
            build_museum(key, lang)
    for g in GUIDES:
        build_guide(g)
    build_get()
    build_404()
    build_meta()
    print(f"Built {len(LANGS)} languages, {sum(len(m['paths']) for m in MUSEUMS.values())} museum pages, "
          f"{len(GUIDES)} guides, {len(ART)} artworks")


if __name__ == "__main__":
    main()
