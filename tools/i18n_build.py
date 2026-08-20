#!/usr/bin/env python3
"""
Genera versiones estáticas por idioma del sitio a partir de las páginas ES
(que ya traen data-es/data-en/data-pt):

  ES  -> raíz            (/, /empresa/, ...)          [se regenera in place]
  EN  -> /en/...         (/en/, /en/empresa/, ...)
  PT  -> /pt/...

Cada salida tiene: texto "bakeado" al idioma, <html lang>, canonical propio,
set hreflang recíproco (es/en/pt/x-default), og:url/og:locale, y los links
internos con el prefijo de idioma. También regenera sitemap.xml con alternates.

El idioma se activa por URL: app.js lee <html data-i18n> y los botones ES/EN/PT
navegan a la URL del otro idioma.

Uso:  python3 tools/i18n_build.py
Editá siempre las páginas ES (la raíz) y volvé a correr esto.
"""
import os, re, datetime
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
BASE = "https://nexolibre.com"
LANGS = ["es", "en", "pt"]
OGLOC = {"es": "es_AR", "en": "en_US", "pt": "pt_BR"}

# rutas relativas de cada página ES (P termina en / o es "")
PAGES = ["", "empresa/", "servicios/", "productos/", "software/", "catalogo/",
         "contacto/", "monitoreo/"]

# prefijos de href que NO se localizan (assets, archivos, externos)
SKIP = ("/assets", "/styles.css", "/parts.json", "/sitemap", "/robots",
        "/llms", "/favicon", "/presentacion", "/CNAME", "/og-", "//")


def src_path(P):
    return os.path.join(ROOT, (P + "index.html") if P else "index.html")


def out_path(lang, P):
    pre = "" if lang == "es" else lang + "/"
    d = os.path.join(ROOT, pre + P)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "index.html")


def url_for(lang, P):
    pre = "" if lang == "es" else lang + "/"
    return f"{BASE}/{pre}{P}"


def bake(raw, lang, P):
    soup = BeautifulSoup(raw, "html.parser")

    # 1) texto al idioma
    for el in soup.select(f"[data-{lang}]"):
        val = el.get(f"data-{lang}")
        if val is None:
            continue
        el.clear()
        for node in list(BeautifulSoup(val, "html.parser").children):
            el.append(node)
    for el in soup.select(f"[data-{lang}-ph]"):
        el["placeholder"] = el.get(f"data-{lang}-ph")

    # 2) <html lang> + marca de idioma para app.js
    if soup.html:
        soup.html["lang"] = lang
        soup.html["data-i18n"] = lang

    head = soup.head
    # 3) canonical
    can = soup.find("link", rel="canonical")
    if can:
        can["href"] = url_for(lang, P)
    # og:url / og:locale
    ogu = soup.find("meta", attrs={"property": "og:url"})
    if ogu:
        ogu["content"] = url_for(lang, P)
    for m in soup.find_all("meta", attrs={"property": re.compile(r"^og:locale")}):
        m.decompose()
    if head:
        m = soup.new_tag("meta"); m["property"] = "og:locale"; m["content"] = OGLOC[lang]
        (can or head).insert_after(m) if can else head.append(m)
        for other in [l for l in LANGS if l != lang]:
            ma = soup.new_tag("meta"); ma["property"] = "og:locale:alternate"; ma["content"] = OGLOC[other]
            m.insert_after(ma)

    # 4) hreflang recíproco (reemplaza los existentes)
    for l in soup.find_all("link", rel="alternate", hreflang=True):
        l.decompose()
    if can:
        anchor = can
        pairs = [("es", url_for("es", P)), ("en", url_for("en", P)),
                 ("pt", url_for("pt", P)), ("x-default", url_for("es", P))]
        for hl, href in pairs:
            t = soup.new_tag("link", rel="alternate", href=href)
            t["hreflang"] = hl
            anchor.insert_after(t); anchor = t

    # 5) links internos con prefijo de idioma (solo en/pt)
    if lang != "es":
        for a in soup.find_all("a", href=True):
            h = a["href"]
            if h.startswith("/") and not h.startswith(SKIP):
                a["href"] = f"/{lang}{h}"

    return str(soup)


def build_sitemap():
    today = datetime.date.today().isoformat()
    prio = {"": "1.0", "catalogo/": "0.9", "servicios/": "0.9", "productos/": "0.9",
            "software/": "0.8", "monitoreo/": "0.8", "empresa/": "0.7", "contacto/": "0.6"}
    freq = {"": "weekly", "catalogo/": "daily", "productos/": "weekly"}
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for P in PAGES:
        out.append("  <url>")
        out.append(f"    <loc>{url_for('es', P)}</loc>")
        for hl, l in [("es", "es"), ("en", "en"), ("pt", "pt"), ("x-default", "es")]:
            out.append(f'    <xhtml:link rel="alternate" hreflang="{hl}" href="{url_for(l, P)}"/>')
        out.append(f"    <lastmod>{today}</lastmod>")
        out.append(f"    <changefreq>{freq.get(P,'monthly')}</changefreq>")
        out.append(f"    <priority>{prio.get(P,'0.6')}</priority>")
        out.append("  </url>")
    out.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")


def main():
    n = 0
    for P in PAGES:
        sp = src_path(P)
        if not os.path.exists(sp):
            print("  falta:", sp); continue
        raw = open(sp, encoding="utf-8").read()
        for lang in LANGS:
            html = bake(raw, lang, P)
            open(out_path(lang, P), "w", encoding="utf-8").write(html)
            n += 1
    build_sitemap()
    print(f"{n} páginas generadas ({len(PAGES)} × {len(LANGS)}) + sitemap.xml")


if __name__ == "__main__":
    main()
