#!/usr/bin/env python3
"""
Genera landing pages por query (contenido SEO/GEO) bajo /reparacion/:
un hub + páginas por tipo de pieza (bobinas, gradientes, RF, fuentes/inyectores).
Apuntan a búsquedas reales: "reparación de bobinas MRI", "reparación de gradientes",
etc. Cada página es ES con data-en/data-pt para que i18n_build produzca /en/ y /pt/.

Reusa header/footer de index.html y clases CSS existentes (.subhero, .why-grid,
.why-card, .faq, .pchips, .ctaband). No agrega CSS nuevo.

Uso:  python3 tools/landing_build.py   (luego correr i18n_build.py)
"""
import os, json, html
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
BASE = "https://nexolibre.com"

_idx = BeautifulSoup(open(os.path.join(ROOT, "index.html"), encoding="utf-8").read(), "html.parser")
HEADER = str(_idx.find("header"))
FOOTER = str(_idx.find("footer"))


def esc(s):
    return html.escape(s or "", quote=True)


def L(es, en, pt):
    return f'data-es="{esc(es)}" data-en="{esc(en)}" data-pt="{esc(pt)}"'


def head(path, t, d, jsonld):
    url = f"{BASE}/{path}"
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title data-es="{esc(t[0])}" data-en="{esc(t[1])}" data-pt="{esc(t[2])}">{esc(t[0])}</title>
<meta name="description" content="{esc(d[0])}" data-es="{esc(d[0])}" data-en="{esc(d[1])}" data-pt="{esc(d[2])}" />
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
<meta property="og:title" content="{esc(t[0])}" />
<meta property="og:description" content="{esc(d[0])}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{BASE}/assets/og-image.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{esc(t[0])}" />
<meta name="twitter:description" content="{esc(d[0])}" />
<meta name="twitter:image" content="{BASE}/assets/og-image.jpg" />
{"".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False, separators=(",",":"))}</script>' for j in jsonld)}
</head>
<body>
{HEADER}
<main id="top">'''


TAIL = f'''</main>
{FOOTER}
<script src="/app.js" defer></script>
</body>
</html>'''

CHECK = ('<svg fill="none" height="24" stroke="currentColor" stroke-linecap="round" '
         'stroke-linejoin="round" stroke-width="2.1" viewbox="0 0 24 24" width="24">'
         '<path d="M20 6L9 17l-5-5"></path></svg>')

# proceso compartido (4 pasos)
PROCESO = [
    ("Evaluación y diagnóstico", "Evaluation & diagnosis", "Avaliação e diagnóstico",
     "Recibimos la pieza y diagnosticamos la falla —electrónica y cosmética— en nuestro laboratorio.",
     "We receive the part and diagnose the fault — electronic and cosmetic — in our laboratory.",
     "Recebemos a peça e diagnosticamos a falha — eletrônica e cosmética — em nosso laboratório."),
    ("Presupuesto y aprobación", "Quote & approval", "Orçamento e aprovação",
     "Enviamos presupuesto y tiempos estimados. Recién con tu aprobación avanzamos.",
     "We send a quote and estimated timeline. We only proceed once you approve.",
     "Enviamos orçamento e prazos estimados. Só avançamos com a sua aprovação."),
    ("Reparación", "Repair", "Reparo",
     "Reparación electrónica y cosmética, con el cliente informado en cada etapa.",
     "Electronic and cosmetic repair, keeping the client informed at every stage.",
     "Reparo eletrônico e cosmético, com o cliente informado em cada etapa."),
    ("Control de calidad + garantía", "QA + warranty", "Controle de qualidade + garantia",
     "Testeamos y documentamos la pieza antes de entregarla. Todas las reparaciones tienen 90 días de garantía.",
     "We test and document the part before delivery. Every repair carries a 90-day warranty.",
     "Testamos e documentamos a peça antes da entrega. Todos os reparos têm 90 dias de garantia."),
]

BRANDS = ["GE", "Siemens", "Philips", "Canon", "Hitachi", "Toshiba"]


def proceso_section():
    cards = ""
    for i, (es, en, pt, des, den, dpt) in enumerate(PROCESO, 1):
        cards += (f'<div class="why-card reveal"><span class="why-idx">0{i}</span>'
                  f'<div class="ti">{CHECK}</div>'
                  f'<h4 {L(es,en,pt)}>{esc(es)}</h4>'
                  f'<p {L(des,den,dpt)}>{esc(des)}</p></div>')
    return (f'<section class="split" style="padding-top:0"><div class="wrap">'
            f'<div class="sec-head reveal"><div class="eyebrow" {L("Cómo trabajamos","How we work","Como trabalhamos")}>Cómo trabajamos</div>'
            f'<h2 {L("Nuestro proceso de reparación","Our repair process","Nosso processo de reparo")}>Nuestro proceso de reparación</h2></div>'
            f'<div class="why-grid">{cards}</div></div></section>')


def brands_section():
    chips = "".join(f'<span class="pchip">{esc(b)}</span>' for b in BRANDS)
    chips += f'<span class="pchip" {L("y más","and more","e mais")}>y más</span>'
    return (f'<section class="split" style="padding-top:0"><div class="wrap">'
            f'<div class="sec-head reveal"><div class="eyebrow" {L("Multimarca","Multivendor","Multimarca")}>Multimarca</div>'
            f'<h2 {L("Marcas que reparamos","Brands we repair","Marcas que reparamos")}>Marcas que reparamos</h2></div>'
            f'<div class="pchips">{chips}</div></div></section>')


def faq_section(faqs):
    items = ""
    for q, a in faqs:
        items += (f'<details><summary {L(*q)}>{esc(q[0])}</summary>'
                  f'<p {L(*a)}>{esc(a[0])}</p></details>')
    return (f'<section class="split" id="faq" style="padding-top:0"><div class="wrap">'
            f'<div class="sec-head reveal" style="text-align:center;margin:0 auto 30px;max-width:640px">'
            f'<div class="eyebrow" style="justify-content:center" {L("Preguntas frecuentes","FAQ","Perguntas frequentes")}>Preguntas frecuentes</div>'
            f'<h2 {L("Preguntas frecuentes","Frequently asked questions","Perguntas frequentes")}>Preguntas frecuentes</h2></div>'
            f'<div class="faq reveal">{items}</div></div></section>')


def cta_section():
    wa = "https://wa.me/5491167410993?text=" + \
         "Hola%20Nexolibre%2C%20quer%C3%ADa%20consultar%20por%20una%20reparaci%C3%B3n"
    return (f'<section class="split"><div class="wrap"><div class="ctaband reveal" style="text-align:center">'
            f'<h2 style="max-width:24ch;margin:0 auto 12px" {L("¿Tenés una pieza para reparar?","Have a part to repair?","Tem uma peça para reparar?")}>¿Tenés una pieza para reparar?</h2>'
            f'<p style="margin:0 auto 22px;max-width:56ch" {L("Decinos la marca, el modelo y la falla. Te respondemos con evaluación y presupuesto a la brevedad.","Tell us the brand, model and fault. We reply with an evaluation and quote shortly.","Diga a marca, o modelo e a falha. Respondemos com avaliação e orçamento em breve.")}>Decinos la marca, el modelo y la falla.</p>'
            f'<div class="hero-cta" style="justify-content:center">'
            f'<a href="/contacto/" class="btn btn-primary" {L("Pedí tu cotización","Get a quote","Peça seu orçamento")}>Pedí tu cotización</a>'
            f'<a href="{wa}" target="_blank" rel="noopener" class="btn btn-ghost">WhatsApp</a>'
            f'</div></div></div></section>')


def what_section(title, lead, items):
    lis = ""
    for es, en, pt in items:
        lis += (f'<li><svg fill="none" height="18" stroke="currentColor" stroke-width="2.4" viewbox="0 0 24 24" '
                f'width="18"><path d="M20 6L9 17l-5-5"></path></svg><span {L(es,en,pt)}>{esc(es)}</span></li>')
    return (f'<section class="split" style="padding-top:24px"><div class="wrap">'
            f'<div class="sec-head reveal"><div class="eyebrow" {L("Qué recuperamos","What we recover","O que recuperamos")}>Qué recuperamos</div>'
            f'<h2 {L(*title)}>{esc(title[0])}</h2>'
            f'<p class="lead" {L(*lead)} style="margin-top:10px">{esc(lead[0])}</p></div>'
            f'<ul class="feat" style="max-width:760px">{lis}</ul></div></section>')


def hero(eye, h1, intro):
    return (f'<section class="subhero" style="padding-bottom:8px">'
            f'<div class="glow" style="width:520px;height:520px;background:rgba(241,144,0,.16);top:-180px;left:50%;transform:translateX(-50%)"></div>'
            f'<div class="wrap">'
            f'<div class="eyebrow reveal" style="justify-content:center" {L(*eye)}>{esc(eye[0])}</div>'
            f'<h1 class="reveal" {L(*h1)}>{esc(h1[0])}</h1>'
            f'<p class="lead reveal" style="max-width:72ch;margin:12px auto 0" {L(*intro)}>{esc(intro[0])}</p>'
            f'</div></section>')


def breadcrumb_ld(path, name):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Reparación", "item": BASE + "/reparacion/"},
        {"@type": "ListItem", "position": 3, "name": name, "item": f"{BASE}/{path}"}]}


def service_ld(path, name, desc):
    return {"@context": "https://schema.org", "@type": "Service", "serviceType": name,
            "name": name, "description": desc, "url": f"{BASE}/{path}",
            "provider": {"@id": BASE + "/#organization"},
            "areaServed": [{"@type": "Country", "name": c} for c in ("Argentina", "Chile", "Estados Unidos")]}


def faq_ld(path, faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "es",
            "mainEntity": [{"@type": "Question", "name": q[0],
                            "acceptedAnswer": {"@type": "Answer", "text": a[0]}} for q, a in faqs]}


def write(path, htmlstr):
    os.makedirs(os.path.join(ROOT, path), exist_ok=True)
    open(os.path.join(ROOT, path, "index.html"), "w", encoding="utf-8").write(htmlstr)


# ---------------- SPOKES ----------------
SPOKES = [
    {
        "slug": "reparacion/bobinas-mri",
        "t": ("Reparación de bobinas de resonancia (MRI coils) multimarca — Nexolibre",
              "MRI coil repair — multivendor — Nexolibre",
              "Reparo de bobinas de ressonância (MRI) multimarca — Nexolibre"),
        "d": ("Reparación y recuperación de bobinas de resonancia magnética (MRI coils) de todas las marcas. Reparación electrónica y cosmética en laboratorios propios, con 90 días de garantía. Argentina, Chile y USA.",
              "Repair and recovery of MRI coils from all brands. Electronic and cosmetic repair in our own labs, with a 90-day warranty. Argentina, Chile and the USA.",
              "Reparo e recuperação de bobinas de ressonância (MRI) de todas as marcas. Reparo eletrônico e cosmético em laboratórios próprios, com 90 dias de garantia. Argentina, Chile e EUA."),
        "eye": ("Reparación de bobinas MRI", "MRI coil repair", "Reparo de bobinas MRI"),
        "h1": ("Reparación de bobinas de resonancia magnética (MRI coils)",
               "MRI coil repair (resonance)",
               "Reparo de bobinas de ressonância magnética (MRI)"),
        "intro": ("Recuperamos bobinas de resonancia magnética que el circuito tradicional da por perdidas. Reparación electrónica y cosmética en nuestros laboratorios propios, testeada y con 90 días de garantía, para bobinas de cualquier marca.",
                  "We recover MRI coils that the traditional channel writes off. Electronic and cosmetic repair in our own labs, bench-tested and backed by a 90-day warranty, for coils of any brand.",
                  "Recuperamos bobinas de ressonância que o circuito tradicional dá como perdidas. Reparo eletrônico e cosmético em laboratórios próprios, testado e com 90 dias de garantia, para bobinas de qualquer marca."),
        "what_title": ("Bobinas MRI que reparamos", "MRI coils we repair", "Bobinas MRI que reparamos"),
        "what_lead": ("Bobinas de superficie, phased array, de cuadratura, articulares, de cabeza, columna, rodilla y cuerpo.",
                      "Surface, phased-array, quadrature, joint, head, spine, knee and body coils.",
                      "Bobinas de superfície, phased-array, de quadratura, articulares, de cabeça, coluna, joelho e corpo."),
        "what": [
            ("Bobinas articulares, de rodilla y hombro", "Joint, knee and shoulder coils", "Bobinas articulares, de joelho e ombro"),
            ("Bobinas de cabeza, columna y cuerpo", "Head, spine and body coils", "Bobinas de cabeça, coluna e corpo"),
            ("Bobinas phased array y de cuadratura", "Phased-array and quadrature coils", "Bobinas phased-array e de quadratura"),
            ("Conectores, cables y daño cosmético", "Connectors, cables and cosmetic damage", "Conectores, cabos e dano cosmético"),
        ],
        "faqs": [
            (("¿Reparan bobinas dadas por perdidas por el fabricante?", "Do you repair coils given up for lost by the manufacturer?", "Vocês reparam bobinas dadas como perdidas pelo fabricante?"),
             ("Sí. Nuestra especialidad es recuperar bobinas MRI que el circuito tradicional descarta, con reparación electrónica y cosmética y control de calidad antes de la entrega.", "Yes. Our specialty is recovering MRI coils that the traditional channel discards, with electronic and cosmetic repair and quality control before delivery.", "Sim. Nossa especialidade é recuperar bobinas MRI que o circuito tradicional descarta, com reparo eletrônico e cosmético e controle de qualidade antes da entrega.")),
            (("¿Cuánto tarda la reparación de una bobina?", "How long does a coil repair take?", "Quanto tempo leva o reparo de uma bobina?"),
             ("Según la falla, una bobina MRI suele repararse en 2 a 3 semanas, con presupuesto y tiempos informados antes de avanzar.", "Depending on the fault, an MRI coil is typically repaired in 2 to 3 weeks, with quote and timeline provided before proceeding.", "Conforme a falha, uma bobina MRI costuma ser reparada em 2 a 3 semanas, com orçamento e prazos informados antes de avançar.")),
            (("¿Qué garantía tiene la reparación?", "What warranty does the repair have?", "Qual a garantia do reparo?"),
             ("Todas nuestras reparaciones de bobinas incluyen 90 días de garantía.", "All our coil repairs include a 90-day warranty.", "Todos os nossos reparos de bobinas incluem 90 dias de garantia.")),
        ],
    },
    {
        "slug": "reparacion/gradientes",
        "t": ("Reparación de gradientes y amplificadores de MRI/CT — Nexolibre",
              "MRI/CT gradient & amplifier repair — Nexolibre",
              "Reparo de gradientes e amplificadores de MRI/CT — Nexolibre"),
        "d": ("Reparación de módulos y amplificadores de gradiente de resonancia (MRI) y tomografía (CT), multimarca, en laboratorios propios con 90 días de garantía. Argentina, Chile y USA.",
              "Repair of MRI and CT gradient modules and amplifiers, multivendor, in our own labs with a 90-day warranty. Argentina, Chile and the USA.",
              "Reparo de módulos e amplificadores de gradiente de MRI e CT, multimarca, em laboratórios próprios com 90 dias de garantia. Argentina, Chile e EUA."),
        "eye": ("Reparación de gradientes", "Gradient repair", "Reparo de gradientes"),
        "h1": ("Reparación de gradientes y amplificadores de gradiente",
               "Gradient and gradient-amplifier repair",
               "Reparo de gradientes e amplificadores de gradiente"),
        "intro": ("Reparamos módulos y amplificadores de gradiente de equipos de resonancia y tomografía. Diagnóstico a nivel de componente, reparación y control de calidad en laboratorios propios, con 90 días de garantía.",
                  "We repair gradient modules and amplifiers for MRI and CT systems. Component-level diagnosis, repair and quality control in our own labs, with a 90-day warranty.",
                  "Reparamos módulos e amplificadores de gradiente de equipamentos de MRI e CT. Diagnóstico em nível de componente, reparo e controle de qualidade em laboratórios próprios, com 90 dias de garantia."),
        "what_title": ("Qué reparamos en gradientes", "What we repair in gradients", "O que reparamos em gradientes"),
        "what_lead": ("Amplificadores de gradiente, placas de control y etapas de potencia.",
                      "Gradient amplifiers, control boards and power stages.",
                      "Amplificadores de gradiente, placas de controle e estágios de potência."),
        "what": [
            ("Amplificadores de gradiente (GPA)", "Gradient power amplifiers (GPA)", "Amplificadores de gradiente (GPA)"),
            ("Placas de control y drivers", "Control boards and drivers", "Placas de controle e drivers"),
            ("Etapas de potencia e IGBT", "Power stages and IGBTs", "Estágios de potência e IGBTs"),
            ("Fallas intermitentes y de refrigeración", "Intermittent and cooling faults", "Falhas intermitentes e de refrigeração"),
        ],
        "faqs": [
            (("¿Reparan amplificadores de gradiente a nivel de componente?", "Do you repair gradient amplifiers at component level?", "Vocês reparam amplificadores de gradiente em nível de componente?"),
             ("Sí. Diagnosticamos y reparamos a nivel de componente placas, drivers y etapas de potencia de amplificadores de gradiente, con testeo antes de la entrega.", "Yes. We diagnose and repair boards, drivers and power stages of gradient amplifiers at component level, with testing before delivery.", "Sim. Diagnosticamos e reparamos placas, drivers e estágios de potência de amplificadores de gradiente em nível de componente, com testes antes da entrega.")),
            (("¿Trabajan con todas las marcas?", "Do you work with all brands?", "Vocês trabalham com todas as marcas?"),
             ("Sí, trabajamos de forma multimarca (GE, Siemens, Philips, Canon, Hitachi, Toshiba y más).", "Yes, we work multivendor (GE, Siemens, Philips, Canon, Hitachi, Toshiba and more).", "Sim, trabalhamos de forma multimarca (GE, Siemens, Philips, Canon, Hitachi, Toshiba e mais).")),
        ],
    },
    {
        "slug": "reparacion/rf",
        "t": ("Reparación de módulos y amplificadores de RF de resonancia — Nexolibre",
              "MRI RF module & amplifier repair — Nexolibre",
              "Reparo de módulos e amplificadores de RF de MRI — Nexolibre"),
        "d": ("Reparación de módulos y amplificadores de radiofrecuencia (RF) de equipos de resonancia magnética, multimarca, en laboratorios propios con 90 días de garantía. Argentina, Chile y USA.",
              "Repair of RF modules and amplifiers for MRI systems, multivendor, in our own labs with a 90-day warranty. Argentina, Chile and the USA.",
              "Reparo de módulos e amplificadores de radiofrequência (RF) de MRI, multimarca, em laboratórios próprios com 90 dias de garantia. Argentina, Chile e EUA."),
        "eye": ("Reparación de RF", "RF repair", "Reparo de RF"),
        "h1": ("Reparación de módulos y amplificadores de RF",
               "RF module and amplifier repair",
               "Reparo de módulos e amplificadores de RF"),
        "intro": ("Reparamos cadenas de radiofrecuencia de resonancia magnética: amplificadores de RF, módulos de transmisión y recepción. Diagnóstico, reparación y testeo en laboratorios propios, con 90 días de garantía.",
                  "We repair MRI radiofrequency chains: RF amplifiers, transmit and receive modules. Diagnosis, repair and testing in our own labs, with a 90-day warranty.",
                  "Reparamos cadeias de radiofrequência de MRI: amplificadores de RF, módulos de transmissão e recepção. Diagnóstico, reparo e testes em laboratórios próprios, com 90 dias de garantia."),
        "what_title": ("Qué reparamos en RF", "What we repair in RF", "O que reparamos em RF"),
        "what_lead": ("Amplificadores de RF, módulos T/R y placas asociadas.",
                      "RF amplifiers, T/R modules and associated boards.",
                      "Amplificadores de RF, módulos T/R e placas associadas."),
        "what": [
            ("Amplificadores de potencia de RF (RFPA)", "RF power amplifiers (RFPA)", "Amplificadores de potência de RF (RFPA)"),
            ("Módulos de transmisión y recepción (T/R)", "Transmit/receive (T/R) modules", "Módulos de transmissão e recepção (T/R)"),
            ("Preamplificadores y placas de RF", "Preamplifiers and RF boards", "Pré-amplificadores e placas de RF"),
            ("Pérdida de señal y calentamiento", "Signal loss and overheating", "Perda de sinal e superaquecimento"),
        ],
        "faqs": [
            (("¿Reparan amplificadores de potencia de RF (RFPA)?", "Do you repair RF power amplifiers (RFPA)?", "Vocês reparam amplificadores de potência de RF (RFPA)?"),
             ("Sí. Reparamos RFPA, módulos T/R y preamplificadores de resonancia, con testeo funcional antes de la entrega y 90 días de garantía.", "Yes. We repair RFPAs, T/R modules and MRI preamplifiers, with functional testing before delivery and a 90-day warranty.", "Sim. Reparamos RFPAs, módulos T/R e pré-amplificadores de MRI, com testes funcionais antes da entrega e 90 dias de garantia.")),
            (("¿Cómo diagnostican una falla de RF?", "How do you diagnose an RF fault?", "Como vocês diagnosticam uma falha de RF?"),
             ("Evaluamos la cadena de radiofrecuencia a nivel de componente (potencia, ganancia, disipación) para aislar la causa —pérdida de señal, calentamiento o falla intermitente— antes de presupuestar. Trabajamos de forma multimarca: GE, Siemens, Philips, Canon, Hitachi y Toshiba.", "We evaluate the RF chain at component level (power, gain, dissipation) to isolate the cause —signal loss, overheating or intermittent failure— before quoting. We work multivendor: GE, Siemens, Philips, Canon, Hitachi and Toshiba.", "Avaliamos a cadeia de radiofrequência em nível de componente (potência, ganho, dissipação) para isolar a causa —perda de sinal, superaquecimento ou falha intermitente— antes de orçar. Trabalhamos de forma multimarca: GE, Siemens, Philips, Canon, Hitachi e Toshiba.")),
            (("¿Cuánto tarda la reparación y qué garantía tiene?", "How long does the repair take and what warranty?", "Quanto tempo leva o reparo e qual a garantia?"),
             ("Según la falla, la reparación suele completarse en 2 a 3 semanas, con presupuesto y tiempos informados antes de avanzar. Todas nuestras reparaciones incluyen 90 días de garantía.", "Depending on the fault, the repair is typically completed in 2 to 3 weeks, with quote and timeline provided before proceeding. All our repairs include a 90-day warranty.", "Conforme a falha, o reparo costuma ser concluído em 2 a 3 semanas, com orçamento e prazos informados antes de avançar. Todos os nossos reparos incluem 90 dias de garantia.")),
        ],
    },
    {
        "slug": "reparacion/fuentes-inyectores",
        "t": ("Reparación de fuentes de poder e inyectores de contraste — Nexolibre",
              "Power supply & contrast injector repair — Nexolibre",
              "Reparo de fontes e injetores de contraste — Nexolibre"),
        "d": ("Reparación de fuentes de poder de MRI/CT e inyectores de contraste, multimarca, en laboratorios propios con 90 días de garantía. Argentina, Chile y USA.",
              "Repair of MRI/CT power supplies and contrast injectors, multivendor, in our own labs with a 90-day warranty. Argentina, Chile and the USA.",
              "Reparo de fontes de MRI/CT e injetores de contraste, multimarca, em laboratórios próprios com 90 dias de garantia. Argentina, Chile e EUA."),
        "eye": ("Fuentes e inyectores", "Power supplies & injectors", "Fontes e injetores"),
        "h1": ("Reparación de fuentes de poder e inyectores de contraste",
               "Power supply and contrast injector repair",
               "Reparo de fontes de poder e injetores de contraste"),
        "intro": ("Reparamos fuentes de poder de resonancia y tomografía e inyectores de contraste. Diagnóstico a nivel de componente, reparación y testeo en laboratorios propios, con 90 días de garantía.",
                  "We repair MRI and CT power supplies and contrast injectors. Component-level diagnosis, repair and testing in our own labs, with a 90-day warranty.",
                  "Reparamos fontes de MRI e CT e injetores de contraste. Diagnóstico em nível de componente, reparo e testes em laboratórios próprios, com 90 dias de garantia."),
        "what_title": ("Qué reparamos", "What we repair", "O que reparamos"),
        "what_lead": ("Fuentes conmutadas, fuentes de alta tensión e inyectores de contraste.",
                      "Switching supplies, high-voltage supplies and contrast injectors.",
                      "Fontes chaveadas, fontes de alta tensão e injetores de contraste."),
        "what": [
            ("Fuentes de poder conmutadas y lineales", "Switching and linear power supplies", "Fontes chaveadas e lineares"),
            ("Fuentes de alta tensión", "High-voltage power supplies", "Fontes de alta tensão"),
            ("Inyectores de contraste (MRI/CT)", "Contrast injectors (MRI/CT)", "Injetores de contraste (MRI/CT)"),
            ("Placas de control y potencia", "Control and power boards", "Placas de controle e potência"),
        ],
        "faqs": [
            (("¿Reparan inyectores de contraste?", "Do you repair contrast injectors?", "Vocês reparam injetores de contraste?"),
             ("Sí. Reparamos inyectores de contraste de MRI y CT, además de fuentes de poder, con testeo y 90 días de garantía.", "Yes. We repair MRI and CT contrast injectors as well as power supplies, with testing and a 90-day warranty.", "Sim. Reparamos injetores de contraste de MRI e CT, além de fontes, com testes e 90 dias de garantia.")),
            (("¿Qué fallas de fuente de poder reparan?", "What power-supply faults do you repair?", "Quais falhas de fonte vocês reparam?"),
             ("Reparamos fuentes conmutadas, lineales y de alta tensión de MRI/CT: fallas de arranque, tensiones fuera de rango, ruido, sobrecalentamiento y placas de control o potencia dañadas. Diagnóstico a nivel de componente antes de presupuestar.", "We repair switching, linear and high-voltage MRI/CT supplies: no-start faults, out-of-range voltages, noise, overheating and damaged control or power boards. Component-level diagnosis before quoting.", "Reparamos fontes chaveadas, lineares e de alta tensão de MRI/CT: falhas de partida, tensões fora de faixa, ruído, superaquecimento e placas de controle ou potência danificadas. Diagnóstico em nível de componente antes de orçar.")),
            (("¿Trabajan con todas las marcas y dan garantía?", "Do you work with all brands and give warranty?", "Vocês trabalham com todas as marcas e dão garantia?"),
             ("Sí, trabajamos de forma multimarca (GE, Siemens, Philips, Canon, Hitachi, Toshiba y más) y todas las reparaciones incluyen 90 días de garantía, con la pieza testeada y documentada antes de la entrega.", "Yes, we work multivendor (GE, Siemens, Philips, Canon, Hitachi, Toshiba and more) and every repair includes a 90-day warranty, with the part tested and documented before delivery.", "Sim, trabalhamos de forma multimarca (GE, Siemens, Philips, Canon, Hitachi, Toshiba e mais) e todos os reparos incluem 90 dias de garantia, com a peça testada e documentada antes da entrega.")),
        ],
    },
]


def render_spoke(s):
    jsonld = [service_ld(s["slug"], s["h1"][0], s["d"][0]),
              breadcrumb_ld(s["slug"], s["eye"][0]),
              faq_ld(s["slug"], s["faqs"])]
    body = (hero(s["eye"], s["h1"], s["intro"])
            + what_section(s["what_title"], s["what_lead"], s["what"])
            + proceso_section()
            + brands_section()
            + faq_section(s["faqs"])
            + cta_section())
    write(s["slug"], head(s["slug"], s["t"], s["d"], jsonld) + body + TAIL)


def render_hub():
    cards = ""
    for s in SPOKES:
        cards += (f'<a class="tcard reveal" href="/{s["slug"]}/" style="text-decoration:none">'
                  f'<h4 {L(*s["eye"])}>{esc(s["eye"][0])}</h4>'
                  f'<p {L(*s["h1"])}>{esc(s["h1"][0])}</p></a>')
    t = ("Reparación y recuperación de piezas de MRI/CT multimarca — Nexolibre",
         "MRI/CT parts repair and recovery — multivendor — Nexolibre",
         "Reparo e recuperação de peças de MRI/CT multimarca — Nexolibre")
    d = ("Laboratorios propios que reparan y recuperan piezas críticas de resonancia (MRI) y tomografía (CT): bobinas, gradientes, RF, fuentes e inyectores. Multimarca, con 90 días de garantía. Argentina, Chile y USA.",
         "In-house labs that repair and recover critical MRI and CT parts: coils, gradients, RF, power supplies and injectors. Multivendor, with a 90-day warranty. Argentina, Chile and the USA.",
         "Laboratórios próprios que reparam e recuperam peças críticas de MRI e CT: bobinas, gradientes, RF, fontes e injetores. Multimarca, com 90 dias de garantia. Argentina, Chile e EUA.")
    body = (hero(("Reparación y recuperación", "Repair & recovery", "Reparo e recuperação"),
                 ("Reparación y recuperación de piezas de MRI/CT",
                  "MRI/CT parts repair and recovery",
                  "Reparo e recuperação de peças de MRI/CT"),
                 ("Reparamos y recuperamos piezas críticas de resonancia y tomografía que el circuito tradicional da por perdidas. Laboratorios propios en Argentina, Chile y Estados Unidos, multimarca y con 90 días de garantía.",
                  "We repair and recover critical MRI and CT parts that the traditional channel writes off. In-house labs in Argentina, Chile and the United States, multivendor and with a 90-day warranty.",
                  "Reparamos e recuperamos peças críticas de MRI e CT que o circuito tradicional dá como perdidas. Laboratórios próprios na Argentina, Chile e Estados Unidos, multimarca e com 90 dias de garantia."))
            + f'<section class="products"><div class="wrap"><div class="grid-3">{cards}</div></div></section>'
            + proceso_section()
            + brands_section()
            + cta_section())
    jsonld = [{"@context": "https://schema.org", "@type": "CollectionPage",
               "name": t[0], "url": BASE + "/reparacion/"},
              breadcrumb_ld("reparacion/", "Reparación")]
    # el breadcrumb del hub sólo hasta nivel 2
    jsonld[1]["itemListElement"] = jsonld[1]["itemListElement"][:2]
    write("reparacion", head("reparacion/", t, d, jsonld) + body + TAIL)


def main():
    render_hub()
    for s in SPOKES:
        render_spoke(s)
    print(f"{1 + len(SPOKES)} landings generadas: reparacion/ + " + ", ".join(s["slug"] for s in SPOKES))


if __name__ == "__main__":
    main()
