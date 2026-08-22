#!/usr/bin/env python3
"""
Generador del Catálogo PDF de Nexolibre (para enviar a clientes).

Lee ../../parts.json y produce 3 HTML listos para imprimir a PDF (ES / EN / PT-BR),
con el sistema de diseño de marca (~/.claude/NEXOLIBRE-BRAND.md, tema claro):
crema #f7f5f1, títulos Exo con acento naranja #ef8f03, cuerpo Helvetica, fichas
enmarcadas tipo "instrumento". NUNCA muestra precio. No se publica en la web.

Uso:
    python3 tools/catalog_pdf/build_catalog.py
    # -> tools/catalog_pdf/out/catalogo-nexolibre-{es,en,pt}.html
    # Abrí cada uno en el navegador -> Imprimir -> Guardar como PDF (A4).

PDF por CLI (opcional, si tenés weasyprint):
    pip install weasyprint
    python3 tools/catalog_pdf/build_catalog.py --pdf
Sin dependencias externas para el HTML (solo stdlib).
"""
import os, re, json, html, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT  = os.path.join(HERE, "out")
# Ruta relativa desde out/ hacia los assets del repo (para que las fotos carguen)
ASSET_REL = "../../../assets"

# ---- Idiomas: etiquetas de UI (los datos técnicos de cada parte quedan como están) ----
LANGS = {
    "es": {
        "code": "es",
        "cover_kicker": "Ingeniería médica multimarca · MRI / CT",
        "cover_title": ["Catálogo de", "partes"],          # 2ª palabra en naranja
        "cover_sub": "Bobinas, amplificadores, electrónica y repuestos críticos para diagnóstico por imágenes.",
        "cover_meta": "Edición",
        "toc": "Contenido",
        "count_parts": "partes disponibles",
        "f_marca": "Marca", "f_modelo": "Modelo compatible", "f_parte": "N° de parte",
        "f_estado": "Estado", "f_disp": "Disponibilidad", "f_ubic": "Ubicación",
        "f_gar": "Garantía", "f_ref": "Ref", "f_cat": "Categoría",
        "gar_suffix": "días", "no_photo": "Foto a solicitud",
        "cta": "Consultá disponibilidad y precio",
        "contact": "Escribinos para cotizar o reservar cualquier ítem de este catálogo.",
        "member": "Nexolibre es miembro de Grupo Nexo",
        "otros": "Otros",
    },
    "en": {
        "code": "en",
        "cover_kicker": "Multi-brand medical engineering · MRI / CT",
        "cover_title": ["Parts", "catalog"],
        "cover_sub": "Coils, amplifiers, electronics and critical spare parts for diagnostic imaging.",
        "cover_meta": "Edition",
        "toc": "Contents",
        "count_parts": "parts available",
        "f_marca": "Brand", "f_modelo": "Compatible model", "f_parte": "Part No.",
        "f_estado": "Condition", "f_disp": "Availability", "f_ubic": "Location",
        "f_gar": "Warranty", "f_ref": "Ref", "f_cat": "Category",
        "gar_suffix": "days", "no_photo": "Photo on request",
        "cta": "Ask for availability and pricing",
        "contact": "Contact us to quote or reserve any item in this catalog.",
        "member": "Nexolibre is a member of Grupo Nexo",
        "otros": "Others",
    },
    "pt": {
        "code": "pt-BR",
        "cover_kicker": "Engenharia médica multimarca · MRI / CT",
        "cover_title": ["Catálogo de", "peças"],
        "cover_sub": "Bobinas, amplificadores, eletrônica e peças críticas para diagnóstico por imagem.",
        "cover_meta": "Edição",
        "toc": "Conteúdo",
        "count_parts": "peças disponíveis",
        "f_marca": "Marca", "f_modelo": "Modelo compatível", "f_parte": "Nº da peça",
        "f_estado": "Condição", "f_disp": "Disponibilidade", "f_ubic": "Localização",
        "f_gar": "Garantia", "f_ref": "Ref", "f_cat": "Categoria",
        "gar_suffix": "dias", "no_photo": "Foto sob consulta",
        "cta": "Consulte disponibilidade e preço",
        "contact": "Fale conosco para cotar ou reservar qualquer item deste catálogo.",
        "member": "Nexolibre é membro do Grupo Nexo",
        "otros": "Outros",
    },
}

# ---- Normalización trilingüe de valores de campos de opción ----
VAL = {
    "estado": {
        "usado": {"es": "Usado", "en": "Used", "pt": "Usado"},
        "used": {"es": "Usado", "en": "Used", "pt": "Usado"},
        "new": {"es": "Nuevo", "en": "New", "pt": "Novo"},
        "nuevo": {"es": "Nuevo", "en": "New", "pt": "Novo"},
        "for parts or not working": {"es": "Para repuestos", "en": "For parts", "pt": "Para peças"},
    },
    "disponibilidad": {
        "en stock": {"es": "En stock", "en": "In stock", "pt": "Em estoque"},
        "sin stock": {"es": "Sin stock", "en": "Out of stock", "pt": "Sem estoque"},
        "a pedido": {"es": "A pedido", "en": "On request", "pt": "Sob encomenda"},
    },
    "categoria": {
        "bobina": {"es": "Bobina", "en": "Coil", "pt": "Bobina"},
        "otro": {"es": "Otro", "en": "Other", "pt": "Outro"},
    },
}

def loc_val(campo, valor, lang):
    if not valor:
        return ""
    m = VAL.get(campo, {}).get(str(valor).strip().lower())
    return m[lang] if m else str(valor)

def e(s):
    return html.escape(str(s if s is not None else ""))

def imgs_of(p):
    raw = str(p.get("imagen") or "")
    files = [s.strip() for s in re.split(r"[;,\n]+", raw) if s.strip()]
    out = []
    for f in files:
        if re.match(r"^https?://", f, re.I):
            out.append(f)
        else:
            out.append(f"{ASSET_REL}/parts/{f}")
    return out

def modalidad_key(p):
    return (p.get("modalidad") or "").strip()

# --------------------------------- CSS ---------------------------------
CSS = """
@page { size: A4; margin: 14mm 12mm 16mm 12mm; }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
:root{
  --bg:#f7f5f1; --card:#ffffff; --ink:#211c16; --title:#645d56;
  --ink2:#625d57; --ink3:#8c867d; --orange:#ef8f03; --orange-dk:#d97e00;
  --border:rgba(20,16,10,.12); --border-soft:rgba(20,16,10,.08);
}
html,body{margin:0;padding:0;background:var(--bg);color:var(--ink);
  font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:10.5px;line-height:1.45;}
h1,h2,h3{font-family:'Exo','Helvetica Neue',sans-serif;letter-spacing:-.02em;
  color:var(--title);margin:0;font-weight:800;line-height:1.02;}
.o{color:var(--orange);}
.kicker{font-weight:700;text-transform:uppercase;letter-spacing:.16em;color:var(--orange);
  font-size:9px;display:flex;align-items:center;gap:7px;}
.kicker::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--orange);display:inline-block;}

/* ---- Portada ---- */
.cover{position:relative;height:265mm;display:flex;flex-direction:column;justify-content:center;
  padding:0 6mm;overflow:hidden;page-break-after:always;
  background:
    radial-gradient(120mm 120mm at 88% 8%, rgba(239,143,3,.16), transparent 60%),
    radial-gradient(rgba(20,16,10,.05) 1px, transparent 1px);
  background-size:auto, 22px 22px;}
.cover .wm{position:absolute;top:-30mm;right:-6mm;font-family:'Exo';font-weight:900;
  font-size:170mm;color:rgba(100,93,86,.06);line-height:1;z-index:0;}
.cover .inner{position:relative;z-index:1;}
.cover .logo{height:15mm;margin-bottom:16mm;}
.cover h1{font-size:58px;font-weight:900;margin:6mm 0 4mm;}
.cover .sub{font-size:14px;color:var(--ink2);max-width:150mm;}
.cover .meta{margin-top:20mm;font-size:11px;color:var(--ink3);}

/* ---- Secciones ---- */
.section{page-break-before:always;padding-top:2mm;}
.section-head{display:flex;align-items:baseline;justify-content:space-between;
  border-bottom:2px solid var(--orange);padding-bottom:3mm;margin-bottom:5mm;}
.section-head h2{font-size:26px;font-weight:900;}
.section-head .n{font-size:11px;color:var(--ink3);}

/* ---- Grilla de fichas ---- */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:5mm;}
.part{border:1px solid var(--border);border-radius:16px;background:var(--card);overflow:hidden;
  page-break-inside:avoid;box-shadow:0 1px 3px rgba(20,16,10,.05),0 10px 24px -18px rgba(20,16,10,.22);}
.instr{border-bottom:1px solid var(--border-soft);background:#fbfaf7;}
.instr .bar{display:flex;align-items:center;gap:6px;padding:4px 9px;border-bottom:1px solid var(--border-soft);}
.instr .bar .dot{width:7px;height:7px;border-radius:50%;background:var(--orange);}
.instr .bar .lbl{font-size:8px;font-weight:700;text-transform:uppercase;letter-spacing:.14em;color:var(--ink3);}
.instr .ph{height:44mm;display:flex;align-items:center;justify-content:center;background:#f4f1ec;}
.instr .ph img{max-width:100%;max-height:44mm;object-fit:contain;}
.instr .ph.empty{color:var(--ink3);font-size:9px;letter-spacing:.06em;}
.body{padding:7px 10px 10px;}
.body h3{font-size:12.5px;font-weight:800;color:var(--ink);line-height:1.15;margin-bottom:4px;}
.chips{display:flex;flex-wrap:wrap;gap:4px;margin:4px 0 6px;}
.chip{font-size:8px;border:1px solid var(--border);border-radius:30px;padding:2px 8px 2px 6px;
  color:var(--ink2);display:flex;align-items:center;gap:4px;}
.chip::before{content:"";width:5px;height:5px;border-radius:50%;background:var(--orange);}
.chip.ref{border-color:var(--orange);color:var(--orange-dk);font-weight:700;}
dl{display:grid;grid-template-columns:auto 1fr;gap:1px 8px;margin:0;font-size:9px;}
dt{color:var(--ink3);}
dd{margin:0;color:var(--ink);}
.desc{margin-top:6px;font-size:9px;color:var(--ink2);border-top:1px solid var(--border-soft);padding-top:5px;}

/* ---- Cierre ---- */
.closing{page-break-before:always;padding-top:30mm;text-align:center;}
.closing h2{font-size:30px;font-weight:900;margin-bottom:5mm;}
.closing .cta{display:inline-block;background:var(--orange);color:#fff;font-weight:700;
  padding:9px 22px;border-radius:12px;font-size:12px;margin:6mm 0;}
.closing p{color:var(--ink2);max-width:130mm;margin:0 auto;font-size:11px;}
.footer{margin-top:26mm;padding-top:6mm;border-top:1px solid var(--border);color:var(--ink3);font-size:9px;}
.footer .member{font-weight:700;color:var(--ink2);}
"""

def part_card(p, L):
    imgs = imgs_of(p)
    ref = p.get("ref") or ""
    cat = loc_val("categoria", p.get("categoria"), L["code"][:2]) or (p.get("modalidad") or "")
    if imgs:
        ph = f'<div class="ph"><img src="{e(imgs[0])}" alt=""></div>'
    else:
        ph = f'<div class="ph empty">{e(L["no_photo"])}</div>'
    bar_lbl = e(ref or cat or "Nexolibre")
    lang2 = L["code"][:2]

    rows = []
    def row(lbl, val):
        if val:
            rows.append(f"<dt>{e(lbl)}</dt><dd>{e(val)}</dd>")
    row(L["f_marca"], p.get("marca"))
    row(L["f_modelo"], p.get("modelo_compatible"))
    row(L["f_parte"], p.get("nro_parte"))
    row(L["f_estado"], loc_val("estado", p.get("estado"), lang2))
    row(L["f_disp"], loc_val("disponibilidad", p.get("disponibilidad"), lang2))
    row(L["f_ubic"], p.get("ubicacion"))
    if p.get("garantia"):
        try:
            g = int(float(p["garantia"]))
            row(L["f_gar"], f'{g} {L["gar_suffix"]}')
        except Exception:
            pass

    chips = []
    if ref:
        chips.append(f'<span class="chip ref">{e(ref)}</span>')
    if p.get("modalidad"):
        chips.append(f'<span class="chip">{e(p["modalidad"])}</span>')
    if cat and cat != p.get("modalidad"):
        chips.append(f'<span class="chip">{e(cat)}</span>')
    chips_html = f'<div class="chips">{"".join(chips)}</div>' if chips else ""

    desc = p.get("descripcion")
    desc_html = f'<div class="desc">{e(desc)}</div>' if desc else ""

    return f"""<div class="part">
  <div class="instr">
    <div class="bar"><span class="dot"></span><span class="lbl">{bar_lbl}</span></div>
    {ph}
  </div>
  <div class="body">
    <h3>{e(p.get("nombre") or "—")}</h3>
    {chips_html}
    <dl>{"".join(rows)}</dl>
    {desc_html}
  </div>
</div>"""

def build(lang, parts):
    L = LANGS[lang]
    # agrupar por modalidad (None -> "Otros"), ordenar por marca+ref
    groups = {}
    for p in parts:
        k = modalidad_key(p) or L["otros"]
        groups.setdefault(k, []).append(p)
    # secciones: primero las modalidades reales, "Otros" al final
    def sort_key(k):
        return (k == L["otros"], k)
    secciones = sorted(groups.keys(), key=sort_key)
    for k in groups:
        groups[k].sort(key=lambda p: (str(p.get("marca") or "~"), str(p.get("ref") or "~")))

    total = len(parts)
    year = datetime.date.today().year

    cover = f"""<div class="cover">
  <div class="wm">NX</div>
  <div class="inner">
    <img class="logo" src="{ASSET_REL}/nexolibre-logo.png" alt="Nexolibre">
    <div class="kicker">{e(L["cover_kicker"])}</div>
    <h1>{e(L["cover_title"][0])} <span class="o">{e(L["cover_title"][1])}</span></h1>
    <div class="sub">{e(L["cover_sub"])}</div>
    <div class="meta">{e(L["cover_meta"])} {year} · {total} {e(L["count_parts"])}</div>
  </div>
</div>"""

    secs_html = []
    for i, k in enumerate(secciones, 1):
        cards = "".join(part_card(p, L) for p in groups[k])
        secs_html.append(f"""<div class="section">
  <div class="section-head">
    <h2>{e(k)}</h2><span class="n">{len(groups[k])} {e(L["count_parts"])}</span>
  </div>
  <div class="grid">{cards}</div>
</div>""")

    closing = f"""<div class="closing">
  <div class="kicker" style="justify-content:center">{e(L["cover_kicker"])}</div>
  <h2>{e(L["cta"])}</h2>
  <div class="cta">nexolibre.com</div>
  <p>{e(L["contact"])}</p>
  <div class="footer">
    <div class="member">{e(L["member"])}</div>
    <div>© {year} Nexolibre · MRI / CT · Argentina · Chile · Colombia · USA</div>
  </div>
</div>"""

    return f"""<!doctype html>
<html lang="{L['code']}"><head><meta charset="utf-8">
<title>Nexolibre — {e(' '.join(L['cover_title']))}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Exo:wght@700;800;900&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>{cover}{''.join(secs_html)}{closing}</body></html>"""

def main():
    parts = json.load(open(os.path.join(ROOT, "parts.json"), encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    want_pdf = "--pdf" in sys.argv
    written = []
    for lang in LANGS:
        htmlstr = build(lang, parts)
        path = os.path.join(OUT, f"catalogo-nexolibre-{lang}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(htmlstr)
        written.append(path)
        if want_pdf:
            try:
                from weasyprint import HTML
                pdf = path.replace(".html", ".pdf")
                HTML(path).write_pdf(pdf)
                written.append(pdf)
            except Exception as ex:
                print(f"  ! PDF de {lang} falló ({ex}). Abrí el HTML e imprimí a PDF.")
    print(f"Catálogo generado ({len(parts)} partes):")
    for w in written:
        print("  ·", os.path.relpath(w, ROOT))
    if not want_pdf:
        print("\nAbrí cada HTML en el navegador -> Imprimir -> Guardar como PDF (A4).")

if __name__ == "__main__":
    main()
