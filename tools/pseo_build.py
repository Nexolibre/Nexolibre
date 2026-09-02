#!/usr/bin/env python3
"""
Genera páginas programáticas SEO (directorio por marca / categoría) bajo
/repuestos/ a partir de parts.json. Cada página es ES con data-en/data-pt para
que tools/i18n_build.py produzca /en/ y /pt/.

Uso:  python3 tools/pseo_build.py   (luego correr i18n_build.py)
"""
import os, json, re, html
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
BASE = "https://nexolibre.com"
PARTS = json.load(open(os.path.join(ROOT, "parts.json"), encoding="utf-8"))

# header y footer compartidos, tomados de index.html
_idx = BeautifulSoup(open(os.path.join(ROOT, "index.html"), encoding="utf-8").read(), "html.parser")
HEADER = str(_idx.find("header"))
FOOTER = str(_idx.find("footer"))

def esc(s): return html.escape(s or "", quote=True)
def slugify(s): return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")

def imgs_of(p):
    out = []
    for f in re.split(r"[;,\n]+", str(p.get("imagen") or "")):
        f = f.strip()
        if f: out.append(f if re.match(r"^https?://", f) else "/assets/parts/" + f)
    return out

def L(es, en, pt):
    return f'data-es="{esc(es)}" data-en="{esc(en)}" data-pt="{esc(pt)}"'

def card(p):
    ii = imgs_of(p)
    img = (f'<img src="{esc(ii[0])}" alt="{esc((p.get("marca","")+" "+p.get("nombre","")).strip())}" loading="lazy" decoding="async">'
           if ii else '<div class="pcard-ph"></div>')
    meta = []
    if p.get("modelo_compatible"): meta.append(f'<span {L("Compatible","Fits","Compatível")}>Compatible</span>: ' + esc(p["modelo_compatible"]))
    if p.get("nro_parte") and p["nro_parte"] != "-": meta.append(f'<span {L("N° parte","Part No.","Nº peça")}>N° parte</span>: ' + esc(p["nro_parte"]))
    if p.get("ubicacion"): meta.append(f'<span {L("Ubicación","Location","Localização")}>Ubicación</span>: ' + esc(p["ubicacion"]))
    ref = esc(p.get("ref") or p.get("nombre") or "")
    return (f'<article class="pcard"><div class="pcard-img">{img}</div>'
            f'<div class="pcard-b"><h3>{esc(p.get("nombre",""))}</h3>'
            f'<div class="pcard-m">{"<br>".join(meta)}</div>'
            f'<a class="btn btn-primary" style="padding:8px 15px;font-size:14px" href="/contacto/?parte={ref}" '
            f'{L("Consultar","Ask","Consultar")}>Consultar</a></div></article>')

def head(path, t_es, t_en, t_pt, d_es, d_en, d_pt, jsonld):
    url = f"{BASE}/{path}"
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title data-es="{esc(t_es)}" data-en="{esc(t_en)}" data-pt="{esc(t_pt)}">{esc(t_es)}</title>
<meta name="description" content="{esc(d_es)}" data-es="{esc(d_es)}" data-en="{esc(d_en)}" data-pt="{esc(d_pt)}" />
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Exo:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/styles.css" />
<link rel="canonical" href="{url}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="theme-color" content="#F19000" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Nexolibre" />
<meta property="og:title" content="{esc(t_es)}" />
<meta property="og:description" content="{esc(d_es)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{BASE}/assets/og-image.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{esc(t_es)}" />
<meta name="twitter:description" content="{esc(d_es)}" />
<meta name="twitter:image" content="{BASE}/assets/og-image.jpg" />
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False, separators=(",",":"))}</script>
</head>
<body>
{HEADER}
<main id="top">'''

TAIL = f'''</main>
{FOOTER}
<script src="/app.js" defer></script>
</body>
</html>'''

def recovered_and_faq():
    """Bloque de contenido (por qué piezas recuperadas) + FAQ con schema.
    Suma texto sustantivo para que las páginas de listado no sean 'thin'."""
    li = "".join(
        f'<li><svg fill="none" height="18" stroke="currentColor" stroke-width="2.4" viewbox="0 0 24 24" width="18"><path d="M20 6L9 17l-5-5"></path></svg><span {L(es,en,pt)}>{esc(es)}</span></li>'
        for es, en, pt in [
            ("Testeadas y con control de calidad antes de la entrega", "Bench-tested and QA'd before delivery", "Testadas e com controle de qualidade antes da entrega"),
            ("90 días de garantía en todas las reparaciones", "90-day warranty on every repair", "90 dias de garantia em todos os reparos"),
            ("Multimarca, sin atarte al OEM", "Multivendor, no OEM lock-in", "Multimarca, sem prender você ao OEM"),
            ("Sourcing internacional + recuperación a pedido", "International sourcing + recovery on demand", "Sourcing internacional + recuperação sob demanda"),
        ])
    faqs = [
        (("¿Las piezas recuperadas tienen garantía?", "Do recovered parts have a warranty?", "As peças recuperadas têm garantia?"),
         ("Sí. Todas nuestras reparaciones y piezas recuperadas incluyen 90 días de garantía, y cada pieza se testea y documenta antes de la entrega.", "Yes. All our repairs and recovered parts include a 90-day warranty, and every part is tested and documented before delivery.", "Sim. Todos os nossos reparos e peças recuperadas incluem 90 dias de garantia, e cada peça é testada e documentada antes da entrega.")),
        (("¿Qué pasa si no está la pieza que busco?", "What if the part I need isn't listed?", "E se a peça que procuro não estiver na lista?"),
         ("La conseguimos por sourcing internacional o la recuperamos a pedido en nuestros laboratorios de Argentina, Chile y Estados Unidos. Escribinos con la marca, el modelo y el número de parte.", "We source it internationally or recover it on demand in our labs in Argentina, Chile and the United States. Send us the brand, model and part number.", "Conseguimos por sourcing internacional ou recuperamos sob demanda em nossos laboratórios na Argentina, Chile e Estados Unidos. Envie a marca, o modelo e o número da peça.")),
    ]
    det = "".join(f'<details><summary {L(*q)}>{esc(q[0])}</summary><p {L(*a)}>{esc(a[0])}</p></details>' for q, a in faqs)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "es",
          "mainEntity": [{"@type": "Question", "name": q[0], "acceptedAnswer": {"@type": "Answer", "text": a[0]}} for q, a in faqs]}
    return f'''
<section class="split" style="padding-top:8px"><div class="wrap">
  <div class="sec-head reveal"><div class="eyebrow" {L("Piezas recuperadas","Recovered parts","Peças recuperadas")}>Piezas recuperadas</div>
  <h2 {L("Por qué elegir piezas recuperadas y testeadas","Why choose recovered, tested parts","Por que escolher peças recuperadas e testadas")}>Por qué elegir piezas recuperadas y testeadas</h2></div>
  <p class="lead" style="max-width:72ch" {L("Recuperar una pieza en lugar de comprarla nueva evita el downtime del equipo y reduce fuertemente el costo. En nuestros laboratorios propios de Argentina, Chile y Estados Unidos reparamos y testeamos cada pieza antes de entregarla, con control de calidad documentado y 90 días de garantía. Trabajamos de forma multimarca —GE, Siemens, Philips, Canon, Hitachi, Toshiba— sin atar al cliente al OEM.","Recovering a part instead of buying it new avoids equipment downtime and sharply reduces cost. In our own labs in Argentina, Chile and the United States we repair and test every part before delivery, with documented quality control and a 90-day warranty. We work multivendor —GE, Siemens, Philips, Canon, Hitachi, Toshiba— with no OEM lock-in.","Recuperar uma peça em vez de comprá-la nova evita o downtime do equipamento e reduz fortemente o custo. Em nossos laboratórios próprios na Argentina, Chile e Estados Unidos reparamos e testamos cada peça antes da entrega, com controle de qualidade documentado e 90 dias de garantia. Trabalhamos de forma multimarca —GE, Siemens, Philips, Canon, Hitachi, Toshiba— sem prender o cliente ao OEM.")}>Recuperar una pieza en lugar de comprarla nueva evita el downtime del equipo y reduce fuertemente el costo. En nuestros laboratorios propios de Argentina, Chile y Estados Unidos reparamos y testeamos cada pieza antes de entregarla, con control de calidad documentado y 90 días de garantía. Trabajamos de forma multimarca —GE, Siemens, Philips, Canon, Hitachi, Toshiba— sin atar al cliente al OEM.</p>
  <ul class="feat" style="max-width:760px;margin-top:12px">{li}</ul>
  <div class="faq reveal" style="margin-top:26px">{det}</div>
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",",":"))}</script>
</div></section>'''


def page(path, t_es,t_en,t_pt, d_es,d_en,d_pt, eyebrow, h1_es,h1_en,h1_pt,
         intro_es,intro_en,intro_pt, items, models, related, jsonld):
    grid = "".join(card(p) for p in items)
    mod = ""
    if models:
        chips = "".join(f'<span class="pchip">{esc(m)}</span>' for m in models)
        mod = (f'<section class="pseo-sec"><div class="wrap"><h2 {L("Modelos compatibles","Compatible models","Modelos compatíveis")}>Modelos compatibles</h2>'
               f'<div class="pchips">{chips}</div></div></section>')
    rel = ""
    if related:
        links = "".join(f'<a class="pchip pchip-link" href="{href}" {L(es,en,pt)}>{esc(es)}</a>' for href,es,en,pt in related)
        rel = (f'<section class="pseo-sec"><div class="wrap"><h2 {L("Seguí explorando","Keep exploring","Continue explorando")}>Seguí explorando</h2>'
               f'<div class="pchips">{links}</div></div></section>')
    body = f'''
<section class="subhero" style="padding-bottom:8px">
  <div class="glow" style="width:520px;height:520px;background:rgba(241,144,0,.16);top:-180px;left:50%;transform:translateX(-50%)"></div>
  <div class="wrap">
    <div class="eyebrow reveal" style="justify-content:center" {L(*eyebrow)}>{esc(eyebrow[0])}</div>
    <h1 class="reveal" {L(h1_es,h1_en,h1_pt)}>{esc(h1_es)}</h1>
    <p class="lead reveal" style="max-width:70ch;margin:0 auto" {L(intro_es,intro_en,intro_pt)}>{esc(intro_es)}</p>
  </div>
</section>
<section class="products" style="padding-top:32px"><div class="wrap">
  <div class="pgrid">{grid}</div>
</div></section>
{mod}
{recovered_and_faq()}
{rel}
<section class="split"><div class="wrap"><div class="ctaband reveal" style="text-align:center">
  <h2 style="max-width:22ch;margin:0 auto 12px" {L("¿No ves la pieza que buscás?","Can’t find the part you need?","Não encontra a peça que procura?")}>¿No ves la pieza que buscás?</h2>
  <p style="margin:0 auto 22px;max-width:56ch" {L("Sourcing internacional y laboratorios propios: conseguimos y testeamos la pieza que necesitás.","International sourcing and in-house labs: we find and test the part you need.","Sourcing internacional e laboratórios próprios: encontramos e testamos a peça que você precisa.")}>Sourcing internacional y laboratorios propios: conseguimos y testeamos la pieza que necesitás.</p>
  <div class="hero-cta" style="justify-content:center">
    <a href="/contacto/" class="btn btn-primary" {L("Contactanos","Contact us","Fale conosco")}>Contactanos</a>
    <a href="/catalogo/" class="btn btn-ghost" {L("Ver catálogo completo","Browse full catalog","Ver catálogo completo")}>Ver catálogo completo</a>
  </div>
</div></div></section>'''
    os.makedirs(os.path.join(ROOT, path), exist_ok=True)
    open(os.path.join(ROOT, path, "index.html"), "w", encoding="utf-8").write(head(path, t_es,t_en,t_pt, d_es,d_en,d_pt, jsonld)+body+TAIL)

def itemlist_ld(url, items, name):
    return {"@context":"https://schema.org","@type":"CollectionPage","name":name,"url":BASE+"/"+url,
            "mainEntity":{"@type":"ItemList","numberOfItems":len(items),
              "itemListElement":[{"@type":"ListItem","position":i+1,
                "item":{"@type":"Product","name":((p.get("marca","")+" "+p.get("nombre","")).strip()),
                        "brand":p.get("marca") or None,"sku":p.get("ref") or None}} for i,p in enumerate(items[:60])]}}

def main():
    norm=lambda s:(s or "").strip()
    brands=["GE","Philips","Siemens","Picker"]
    generated=[]
    # marcas con >=3 piezas
    facets=[]
    for b in brands:
        items=[p for p in PARTS if norm(p.get("marca"))==b]
        if len(items)>=3: facets.append(("brand",b,items))
    # bobinas
    bob=[p for p in PARTS if norm(p.get("categoria"))=="Bobina"]
    facets.append(("cat","Bobina",bob))

    # links relacionados (todas las facetas + catálogo)
    def rel_links(exclude_slug):
        r=[]
        for kind,key,items in facets:
            slug="repuestos/"+(slugify(key) if kind=="brand" else "bobinas")
            if slug==exclude_slug: continue
            if kind=="brand": r.append(("/"+slug+"/",f"Repuestos {key}",f"{key} parts",f"Peças {key}"))
            else: r.append(("/"+slug+"/","Bobinas MRI","MRI coils","Bobinas MRI"))
        r.append(("/catalogo/","Catálogo completo","Full catalog","Catálogo completo"))
        return r

    for kind,key,items in facets:
        models=sorted({norm(p.get("modelo_compatible")) for p in items if norm(p.get("modelo_compatible"))})
        n=len(items)
        if kind=="brand":
            slug=f"repuestos/{slugify(key)}"
            t=(f"Repuestos {key} para MRI/CT recuperados y testeados — Nexolibre",
               f"{key} MRI/CT parts — recovered & tested — Nexolibre",
               f"Peças {key} para MRI/CT recuperadas e testadas — Nexolibre")
            d=(f"{n} repuestos {key} para resonancia (MRI) y tomografía (CT): bobinas y piezas críticas recuperadas y testeadas en laboratorios propios. Garantía y soporte en AR, CL y USA.",
               f"{n} {key} MRI/CT spare parts: coils and critical parts recovered and tested in our own labs. Warranty and support in Argentina, Chile and the USA.",
               f"{n} peças {key} para MRI/CT: bobinas e peças críticas recuperadas e testadas em laboratórios próprios. Garantia e suporte na AR, CL e EUA.")
            h1=(f"Repuestos {key} para MRI/CT", f"{key} MRI/CT parts", f"Peças {key} para MRI/CT")
            eye=(f"Repuestos {key}", f"{key} parts", f"Peças {key}")
            intro=(f"En Nexolibre recuperamos, testeamos y vendemos repuestos {key} para equipos de resonancia magnética y tomografía. Contamos con {n} piezas {key} en stock o a pedido, con garantía y soporte técnico local en Argentina, Chile y Estados Unidos.",
                   f"At Nexolibre we recover, test and sell {key} spare parts for MRI and CT systems. We have {n} {key} parts in stock or sourced on demand, with warranty and local technical support in Argentina, Chile and the United States.",
                   f"Na Nexolibre recuperamos, testamos e vendemos peças {key} para equipamentos de ressonância magnética e tomografia. Temos {n} peças {key} em estoque ou sob encomenda, com garantia e suporte técnico local na Argentina, Chile e Estados Unidos.")
        else:
            slug="repuestos/bobinas"
            t=("Bobinas MRI recuperadas y testeadas (todas las marcas) — Nexolibre",
               "MRI coils — recovered & tested (all brands) — Nexolibre",
               "Bobinas MRI recuperadas e testadas (todas as marcas) — Nexolibre")
            d=(f"{n} bobinas de resonancia magnética (MRI) recuperadas y testeadas: GE, Philips, Siemens y más. Restauradas en laboratorios propios, con garantía. AR · CL · USA.",
               f"{n} MRI coils recovered and tested: GE, Philips, Siemens and more. Restored in our own labs, with warranty. Argentina · Chile · USA.",
               f"{n} bobinas de ressonância (MRI) recuperadas e testadas: GE, Philips, Siemens e mais. Restauradas em laboratórios próprios, com garantia. AR · CL · EUA.")
            h1=("Bobinas MRI recuperadas y testeadas","Recovered & tested MRI coils","Bobinas MRI recuperadas e testadas")
            eye=("Bobinas MRI","MRI coils","Bobinas MRI")
            intro=(f"Especialistas en restauración de bobinas de resonancia magnética. {n} bobinas MRI de las principales marcas (GE, Philips, Siemens, Picker) recuperadas y testeadas en nuestros laboratorios de Argentina, Chile y Estados Unidos, con garantía.",
                   f"Specialists in MRI coil restoration. {n} MRI coils from the leading brands (GE, Philips, Siemens, Picker) recovered and tested in our labs in Argentina, Chile and the United States, with warranty.",
                   f"Especialistas em restauração de bobinas de ressonância. {n} bobinas MRI das principais marcas (GE, Philips, Siemens, Picker) recuperadas e testadas em nossos laboratórios na Argentina, Chile e Estados Unidos, com garantia.")
        page(slug, *t, *d, eye, *h1, *intro, items, models, rel_links(slug),
             itemlist_ld(slug, items, t[0]))
        generated.append(slug)

    # HUB /repuestos/
    hub_items=[]
    hub_cards=""
    for kind,key,items in facets:
        slug="repuestos/"+(slugify(key) if kind=="brand" else "bobinas")
        name=(f"Repuestos {key}","Bobinas MRI") if kind=="brand" else ("Bobinas MRI","MRI coils","Bobinas MRI")
        if kind=="brand": es,en,pt=f"Repuestos {key}",f"{key} parts",f"Peças {key}"
        else: es,en,pt="Bobinas MRI","MRI coils","Bobinas MRI"
        hub_cards+=(f'<a class="tcard reveal" href="/{slug}/" style="text-decoration:none">'
                    f'<h4 {L(es,en,pt)}>{esc(es)}</h4>'
                    f'<p {L(f"{len(items)} piezas disponibles",f"{len(items)} parts available",f"{len(items)} peças disponíveis")}>{len(items)} piezas disponibles</p></a>')
    hub_body=f'''
<section class="subhero"><div class="glow" style="width:520px;height:520px;background:rgba(241,144,0,.16);top:-180px;left:50%;transform:translateX(-50%)"></div>
  <div class="wrap">
    <div class="eyebrow reveal" style="justify-content:center" {L("Repuestos MRI/CT","MRI/CT parts","Peças MRI/CT")}>Repuestos MRI/CT</div>
    <h1 class="reveal" {L("Repuestos MRI/CT por marca","MRI/CT parts by brand","Peças MRI/CT por marca")}>Repuestos MRI/CT por marca</h1>
    <p class="lead reveal" style="max-width:66ch;margin:0 auto" {L("Explorá nuestros repuestos de resonancia y tomografía por marca y tipo. Piezas recuperadas y testeadas en laboratorios propios, con garantía y soporte en Argentina, Chile y USA.","Browse our MRI and CT spare parts by brand and type. Parts recovered and tested in our own labs, with warranty and support in Argentina, Chile and the USA.","Explore nossas peças de MRI e CT por marca e tipo. Peças recuperadas e testadas em laboratórios próprios, com garantia e suporte na Argentina, Chile e EUA.")}>Explorá nuestros repuestos de resonancia y tomografía por marca y tipo.</p>
  </div></section>
<section class="products"><div class="wrap"><div class="grid-3">{hub_cards}</div>
  <div style="text-align:center;margin-top:32px"><a href="/catalogo/" class="btn btn-primary" {L("Ver catálogo completo","Browse full catalog","Ver catálogo completo")}>Ver catálogo completo</a></div>
</div></section>
{recovered_and_faq()}'''
    hub_ld={"@context":"https://schema.org","@type":"CollectionPage","name":"Repuestos MRI/CT por marca","url":BASE+"/repuestos/"}
    os.makedirs(os.path.join(ROOT,"repuestos"),exist_ok=True)
    open(os.path.join(ROOT,"repuestos","index.html"),"w",encoding="utf-8").write(
        head("repuestos/",
             "Repuestos MRI/CT por marca — bobinas GE, Philips, Siemens — Nexolibre",
             "MRI/CT parts by brand — GE, Philips, Siemens coils — Nexolibre",
             "Peças MRI/CT por marca — bobinas GE, Philips, Siemens — Nexolibre",
             "Repuestos de resonancia (MRI) y tomografía (CT) por marca: bobinas GE, Philips, Siemens, Picker y más. Recuperados y testeados, con garantía. AR·CL·USA.",
             "MRI and CT spare parts by brand: GE, Philips, Siemens, Picker coils and more. Recovered and tested, with warranty. Argentina·Chile·USA.",
             "Peças de MRI e CT por marca: bobinas GE, Philips, Siemens, Picker e mais. Recuperadas e testadas, com garantia. AR·CL·EUA.",
             hub_ld)+hub_body+TAIL)
    generated.append("repuestos")
    print(f"{len(generated)} páginas programáticas: "+", ".join(generated))

if __name__ == "__main__":
    main()
