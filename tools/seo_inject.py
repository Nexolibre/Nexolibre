#!/usr/bin/env python3
"""
Inyecta en cada página HTML un bloque SEO/GEO consistente, justo antes de </head>:
- canonical, robots, theme-color, hreflang
- Open Graph + Twitter Cards (reusa el <title> y la <meta description> de la página)
- Datos estructurados JSON-LD: Organization (en todas), WebSite+SearchAction (inicio),
  BreadcrumbList (subpáginas), Service (servicios), SoftwareApplication x3 (software).
Idempotente: si ya encuentra el marcador <!-- SEO/GEO --> reemplaza el bloque.
Uso:  python3 tools/seo_inject.py
"""
import re, json, os

BASE = "https://nexolibre.com"
OG_IMG = f"{BASE}/assets/og-image.png"
ORG_ID = f"{BASE}/#organization"
WEB_ID = f"{BASE}/#website"
MARK_A = "<!-- SEO/GEO inicio -->"
MARK_B = "<!-- SEO/GEO fin -->"

# === Datos de identidad (completar LinkedIn / GBP / dirección cuando los tengas) ===
SAMEAS = [
    "https://www.linkedin.com/company/nexo-libre/",
    "https://share.google/iyGj2og1TmS3GPTS4",
]
ADDRESS = None       # ej: {"@type":"PostalAddress","streetAddress":"...","addressLocality":"...","addressCountry":"AR"}

ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": ORG_ID,
    "name": "Nexolibre",
    "alternateName": "Nexolibre — Grupo Nexo",
    "url": f"{BASE}/",
    "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/nexolibre-logo.png"},
    "image": OG_IMG,
    "description": "Ingeniería médica multimarca para diagnóstico por imágenes: soporte técnico MRI/CT, "
                   "laboratorios propios de reparación con recuperación de piezas críticas, venta de equipos "
                   "y software con inteligencia artificial.",
    "parentOrganization": {"@type": "Organization", "name": "Grupo Nexo"},
    "email": "contacto@nexolibre.com",
    "telephone": "+5491167410993",
    "areaServed": [
        {"@type": "Country", "name": "Argentina"},
        {"@type": "Country", "name": "Chile"},
        {"@type": "Country", "name": "Estados Unidos"},
        {"@type": "Country", "name": "Colombia"},
    ],
    "contactPoint": [{
        "@type": "ContactPoint",
        "telephone": "+5491167410993",
        "email": "contacto@nexolibre.com",
        "contactType": "sales",
        "availableLanguage": ["es", "en", "pt"],
    }],
    "knowsAbout": [
        "Resonancia magnética (MRI)", "Tomografía computada (CT)", "Diagnóstico por imágenes",
        "Bobinas MRI", "Reparación de equipos médicos", "Recuperación de piezas críticas",
        "Módulos de RF y gradientes", "Inyectores y fuentes de poder",
        "Software con inteligencia artificial para radiología",
    ],
}
if SAMEAS:
    ORG["sameAs"] = SAMEAS
if ADDRESS:
    ORG["address"] = ADDRESS

WEBSITE = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": WEB_ID,
    "url": f"{BASE}/",
    "name": "Nexolibre",
    "inLanguage": ["es", "en", "pt"],
    "publisher": {"@id": ORG_ID},
    "potentialAction": {
        "@type": "SearchAction",
        "target": {"@type": "EntryPoint", "urlTemplate": f"{BASE}/catalogo.html?q={{search_term_string}}"},
        "query-input": "required name=search_term_string",
    },
}

SERVICE = {
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "Soporte técnico y reparación de equipos MRI/CT",
    "serviceType": "Ingeniería biomédica y reparación de resonancia magnética y tomografía",
    "provider": {"@id": ORG_ID},
    "areaServed": [
        {"@type": "Country", "name": "Argentina"},
        {"@type": "Country", "name": "Chile"},
        {"@type": "Country", "name": "Estados Unidos"},
    ],
    "description": "Soporte técnico, mantenimiento y reparación multimarca de equipos MRI y CT, con "
                   "laboratorios propios para restauración de bobinas, módulos de RF y gradientes, "
                   "fuentes de poder e inyectores.",
}

SOFTWARE_APPS = [
    ("Gauss Connect", "Plataforma de monitoreo y gestión integral del área de diagnóstico por imágenes."),
    ("RadDictate", "Dictado de informes radiológicos asistido por inteligencia artificial."),
    ("SubtleIA", "Mejora de imagen con IA para MRI, CT y PET-CT: menor dosis y menor tiempo de adquisición."),
]
def software_ld():
    out = []
    for name, desc in SOFTWARE_APPS:
        out.append({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": name,
            "applicationCategory": "HealthApplication",
            "operatingSystem": "Web",
            "description": desc,
            "provider": {"@id": ORG_ID},
            "offers": {"@type": "Offer", "availability": "https://schema.org/InStock", "priceCurrency": "USD"},
        })
    return out

def breadcrumb(name, path):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": f"{BASE}/{path}"},
        ],
    }

# page -> (path, og_type, breadcrumb_name|None, [extra ld objects])
PAGES = {
    "index.html":     ("",               "website", None,                 [WEBSITE]),
    "empresa.html":   ("empresa.html",   "website", "Empresa",            []),
    "servicios.html": ("servicios.html", "website", "Servicios",          [SERVICE]),
    "productos.html": ("productos.html", "website", "Productos",          []),
    "software.html":  ("software.html",  "website", "Software con IA",    software_ld()),
    "catalogo.html":  ("catalogo.html",  "website", "Catálogo de partes", []),
    "contacto.html":  ("contacto.html",  "website", "Contacto",           []),
}

def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")

def build_block(fname):
    path, ogtype, bc, extras = PAGES[fname]
    url = f"{BASE}/{path}" if path else f"{BASE}/"
    html = open(fname, encoding="utf-8").read()
    title = re.search(r"<title>(.*?)</title>", html, re.S).group(1).strip()
    desc = re.search(r'name="description"\s+content="(.*?)"', html, re.S).group(1).strip()

    lds = [ORG] + extras
    if bc:
        lds.append(breadcrumb(bc, path))

    lines = [MARK_A,
        f'<link rel="canonical" href="{url}" />',
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />',
        '<meta name="theme-color" content="#F19000" />',
        '<meta name="author" content="Nexolibre" />',
        f'<link rel="alternate" hreflang="es" href="{url}" />',
        f'<link rel="alternate" hreflang="x-default" href="{url}" />',
        f'<meta property="og:type" content="{ogtype}" />',
        '<meta property="og:site_name" content="Nexolibre" />',
        '<meta property="og:locale" content="es_AR" />',
        '<meta property="og:locale:alternate" content="en_US" />',
        '<meta property="og:locale:alternate" content="pt_BR" />',
        f'<meta property="og:title" content="{esc(title)}" />',
        f'<meta property="og:description" content="{esc(desc)}" />',
        f'<meta property="og:url" content="{url}" />',
        f'<meta property="og:image" content="{OG_IMG}" />',
        '<meta property="og:image:width" content="1200" />',
        '<meta property="og:image:height" content="630" />',
        '<meta property="og:image:alt" content="Nexolibre — Ingeniería médica multimarca MRI/CT y software con IA" />',
        '<meta name="twitter:card" content="summary_large_image" />',
        f'<meta name="twitter:title" content="{esc(title)}" />',
        f'<meta name="twitter:description" content="{esc(desc)}" />',
        f'<meta name="twitter:image" content="{OG_IMG}" />',
    ]
    for ld in lds:
        lines.append('<script type="application/ld+json">' +
                     json.dumps(ld, ensure_ascii=False, separators=(",", ":")) + '</script>')
    lines.append(MARK_B)
    return "\n".join(lines), html

def main():
    for fname in PAGES:
        if not os.path.exists(fname):
            print("salteo (no existe):", fname); continue
        block, html = build_block(fname)
        # quitar bloque previo si existe
        html = re.sub(re.escape(MARK_A) + r".*?" + re.escape(MARK_B) + r"\n?", "", html, flags=re.S)
        html = html.replace("</head>", block + "\n</head>", 1)
        open(fname, "w", encoding="utf-8").write(html)
        print(f"  {fname}: bloque SEO/GEO inyectado")
    print("Listo.")

if __name__ == "__main__":
    main()
