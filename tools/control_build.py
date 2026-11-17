#!/usr/bin/env python3
"""
Genera el cluster SEO/GEO del panel de control de equipos de diagnóstico por
imágenes (el SaaS de monitoreo), bajo /control-equipamiento-medico/:

  /control-equipamiento-medico/                                   pilar
  /control-equipamiento-medico/productividad-diagnostico-por-imagenes/
  /control-equipamiento-medico/tablero-pacs-dicom/
  /control-equipamiento-medico/hospitales-clinicas-multisede/

Por qué un cluster aparte y no reescribir /monitoreo/: /monitoreo/ ya rankea
por "sistema de monitoreo criogénico MRI". Si le cambiamos el foco perdemos esa
posición. El pilar nuevo apunta a búsquedas amplias ("sistema de control de
equipamiento médico", "software de gestión de equipos de diagnóstico por
imágenes", "dashboard PACS") y enlaza a /monitoreo/ para la parte de criogenia.

Regla de contenido: sólo funciones que se ven en el video del desarrollador
(nov 2026). Nada de cifras de mejora inventadas. Los números del panel de
ejemplo son ficticios y lo dice en pantalla.

Cada página es ES con data-en/data-pt; i18n_build.py genera /en/ y /pt/.
Uso:  python3 tools/control_build.py && python3 tools/i18n_build.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from landing_build import head, TAIL, L, esc, write, faq_section, CHECK, BASE  # noqa: E402

HUB = "control-equipamiento-medico"
ORG = {"@id": BASE + "/#organization"}
WA = ("https://wa.me/5491167410993?text=" +
      "Hola%20Nexolibre%2C%20quiero%20ver%20una%20demo%20del%20panel%20de%20control%20de%20equipos")

# --------------------------------------------------------------------------
# Piezas visuales
# --------------------------------------------------------------------------

# Panel de ejemplo hecho en HTML (no captura): las capturas reales del video
# tienen nombres de clientes, médicos y pacientes, que no pueden ir a un sitio
# público. Estilos con prefijo .cx- para no chocar con styles.css.
CX_STYLE = """<style>
.cx-panel{background:#16130f;border:1px solid rgba(255,255,255,.08);border-radius:18px;padding:18px;color:#ece6dc;
  box-shadow:0 30px 60px -30px rgba(0,0,0,.55);font-size:13px;max-width:1040px;margin:0 auto}
.cx-top{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;margin-bottom:14px}
.cx-title{font-family:Exo,sans-serif;font-weight:700;font-size:15px;color:#fff}
.cx-live{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:#9be3b5}
.cx-live i{width:8px;height:8px;border-radius:50%;background:#2fd27a;box-shadow:0 0 0 4px rgba(47,210,122,.18)}
.cx-chips{display:flex;flex-wrap:wrap;gap:6px}
.cx-chip{border:1px solid rgba(255,255,255,.12);border-radius:999px;padding:3px 10px;font-size:12px;color:#cfc7ba}
.cx-chip.on{background:#ef8f03;border-color:#ef8f03;color:#1b150d;font-weight:700}
.cx-kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px}
.cx-k{background:#1f1b16;border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:12px}
.cx-k small{display:block;color:#a79f93;font-size:11px;text-transform:uppercase;letter-spacing:.04em}
.cx-k b{display:block;font-family:Exo,sans-serif;font-size:24px;color:#fff;margin-top:4px}
.cx-k span{font-size:11px;color:#a79f93}
.cx-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.cx-eq{background:#1f1b16;border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:12px}
.cx-eq header{all:unset;display:flex;justify-content:space-between;align-items:center;gap:6px}
.cx-eq h5{font-size:13px;color:#fff;margin:0}
.cx-mod{font-size:10px;font-weight:700;border-radius:6px;padding:2px 6px;background:rgba(239,143,3,.18);color:#ffb23e}
.cx-st{font-size:11px;color:#9be3b5}.cx-st.off{color:#f0a3a3}
.cx-row{display:flex;justify-content:space-between;margin-top:8px;color:#a79f93;font-size:12px}
.cx-row b{color:#fff;font-weight:600}
.cx-bar{height:6px;border-radius:6px;background:rgba(255,255,255,.08);margin-top:8px;overflow:hidden}
.cx-bar i{display:block;height:100%;background:linear-gradient(90deg,#ef8f03,#ffb23e)}
.cx-spark{display:flex;align-items:flex-end;gap:3px;height:34px;margin-top:8px}
.cx-spark i{flex:1;background:rgba(239,143,3,.55);border-radius:2px 2px 0 0}
.cx-note{margin-top:10px;font-size:11px;color:#8f877b;text-align:right}
.cx-feats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.cx-f{border:1px solid var(--border);border-radius:16px;padding:20px;background:var(--surface)}
.cx-f h3{font-size:17px;margin:8px 0 6px}
.cx-f p{color:var(--muted);font-size:14.5px}
.cx-f .ti{color:var(--accent)}
.cx-aud{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.cx-aud .cx-f ul{margin:10px 0 0 18px;color:var(--muted);font-size:14.5px}
.cx-aud .cx-f li{margin:4px 0}
.cx-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;counter-reset:cx}
.cx-kpitable{width:100%;border-collapse:collapse;font-size:14.5px}
.cx-kpitable th,.cx-kpitable td{border-bottom:1px solid var(--border);padding:10px 8px;text-align:left;vertical-align:top}
.cx-kpitable th{font-family:Exo,sans-serif;color:var(--text);width:30%}
.cx-kpitable td{color:var(--muted)}
.cx-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
@media (max-width:900px){.cx-kpis{grid-template-columns:repeat(2,1fr)}.cx-grid,.cx-feats,.cx-aud,.cx-steps{grid-template-columns:1fr 1fr}}
@media (max-width:600px){.cx-grid .cx-eq:nth-child(n+4){display:none}.cx-k span{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.cx-grid,.cx-feats,.cx-aud,.cx-steps{grid-template-columns:1fr}.cx-kpitable th{width:40%}}
</style>"""


def hace(es):
    """'hace 3 días' -> (es, '3 days ago', 'há 3 dias')."""
    n = es.replace("hace ", "")
    return es, n.replace("días", "days") + " ago", "há " + n.replace("días", "dias")


def mock_panel():
    """Panel ilustrativo con datos ficticios."""
    eqs = [  # (nombre, modalidad, sede, exámenes, utilización %, mediana, últ. examen, activo, chispa)
        ("Resonador 1.5T", "RM", "Sede Centro", 346, 44, "14 min", "hace 12 min", True, [5, 7, 6, 8, 9, 7, 8, 10, 9, 8]),
        ("Tomógrafo 64", "TC", "Sede Centro", 398, 38, "5 min", "hace 4 min", True, [6, 8, 7, 9, 8, 9, 10, 9, 8, 9]),
        ("Ecógrafo 2", "US", "Sede Norte", 393, 61, "22 min", "hace 25 min", True, [4, 6, 7, 6, 8, 7, 6, 8, 7, 9]),
        ("Mamógrafo", "MG", "Sede Norte", 116, 29, "4 min", "hace 2 h", True, [3, 4, 2, 5, 4, 3, 5, 4, 3, 4]),
        ("Rayos X digital", "DX", "Sede Sur", 518, 52, "1 min", "hace 6 min", True, [7, 8, 9, 8, 10, 9, 8, 9, 10, 9]),
        ("Resonador 3T", "RM", "Sede Sur", 0, 0, "—", "hace 3 días", False, [6, 5, 6, 4, 1, 0, 0, 0, 0, 0]),
    ]
    cards = ""
    for n, m, s, ex, u, med, last, on, sp in eqs:
        bars = "".join(f'<i style="height:{max(v,0.5)*10}%"></i>' for v in sp)
        st = (f'<span class="cx-st" {L("● Activo","● Active","● Ativo")}>● Activo</span>' if on else
              f'<span class="cx-st off" {L("● Sin estudios","● No studies","● Sem estudos")}>● Sin estudios</span>')
        cards += (f'<div class="cx-eq"><header><h5>{esc(n)}</h5><span class="cx-mod">{m}</span></header>'
                  f'<div class="cx-row"><span>{esc(s)}</span>{st}</div>'
                  f'<div class="cx-spark">{bars}</div>'
                  f'<div class="cx-row"><span {L("Exámenes (30 d)","Exams (30 d)","Exames (30 d)")}>Exámenes (30 d)</span><b>{ex}</b></div>'
                  f'<div class="cx-row"><span {L("Utilización","Utilization","Utilização")}>Utilización</span><b>{u}%</b></div>'
                  f'<div class="cx-bar"><i style="width:{u}%"></i></div>'
                  f'<div class="cx-row"><span {L("Duración mediana","Median duration","Duração mediana")}>Duración mediana</span><b>{med}</b></div>'
                  f'<div class="cx-row"><span {L("Último examen","Last exam","Último exame")}>Último examen</span><b {L(*hace(last))}>{esc(last)}</b></div>'
                  f'</div>')
    kpis = [
        (("Equipos conectados", "Connected units", "Equipamentos conectados"), "58", ("en 3 sedes", "across 3 sites", "em 3 unidades")),
        (("Exámenes del período", "Exams this period", "Exames do período"), "7.580", ("RM · TC · US · DX · MG · …", "MR · CT · US · DX · MG · …", "RM · TC · US · DX · MG · …")),
        (("Exámenes por hora", "Exams per hour", "Exames por hora"), "6,3", ("sólo horas activas", "active hours only", "só horas ativas")),
        (("Meta del mes", "Monthly goal", "Meta do mês"), "109%", ("adelantado", "ahead of plan", "adiantado")),
    ]
    k = "".join(f'<div class="cx-k"><small {L(*a)}>{esc(a[0])}</small><b>{v}</b><span {L(*c)}>{esc(c[0])}</span></div>'
                for a, v, c in kpis)
    chips = "".join(f'<span class="cx-chip{" on" if i == 0 else ""}" {L(*c)}>{esc(c[0])}</span>' for i, c in enumerate([
        ("Todas las sedes", "All sites", "Todas as unidades"), ("Últimos 30 días", "Last 30 days", "Últimos 30 dias"),
        ("Todas las modalidades", "All modalities", "Todas as modalidades")]))
    return (f'<div class="cx-panel" role="img" aria-label="Panel de ejemplo con datos ficticios">'
            f'<div class="cx-top"><span class="cx-title" {L("Resumen · Red de diagnóstico (ejemplo)","Overview · Imaging network (example)","Resumo · Rede de diagnóstico (exemplo)")}>Resumen · Red de diagnóstico (ejemplo)</span>'
            f'<span class="cx-live"><i></i><span {L("Datos desde el PACS","Data from PACS","Dados do PACS")}>Datos desde el PACS</span></span></div>'
            f'<div class="cx-chips" style="margin-bottom:12px">{chips}</div>'
            f'<div class="cx-kpis">{k}</div><div class="cx-grid">{cards}</div>'
            f'<div class="cx-note" {L("Panel ilustrativo con datos ficticios. Las pantallas reales se ven en la demo.","Illustrative panel with fictitious data. The real screens are shown in the demo.","Painel ilustrativo com dados fictícios. As telas reais são mostradas na demo.")}>Panel ilustrativo con datos ficticios. Las pantallas reales se ven en la demo.</div>'
            f'</div>')


# --------------------------------------------------------------------------
# Bloques reutilizables
# --------------------------------------------------------------------------

def sec_head(eye, h2, lead=None, center=False):
    st = ' style="text-align:center;margin:0 auto 30px;max-width:760px"' if center else ''
    ej = ' style="justify-content:center"' if center else ''
    out = (f'<div class="sec-head reveal"{st}><div class="eyebrow"{ej} {L(*eye)}>{esc(eye[0])}</div>'
           f'<h2 {L(*h2)}>{esc(h2[0])}</h2>')
    if lead:
        out += f'<p class="lead" style="margin-top:10px" {L(*lead)}>{esc(lead[0])}</p>'
    return out + '</div>'


def section(inner, top=True):
    pad = '' if top else ' style="padding-top:0"'
    return f'<section class="split"{pad}><div class="wrap">{inner}</div></section>'


def hero(eye, h1, intro, ctas=True):
    btns = ""
    if ctas:
        btns = (f'<div class="hero-cta reveal" style="justify-content:center;margin-top:22px">'
                f'<a href="/contacto/" class="btn btn-primary" {L("Pedí una demo","Book a demo","Peça uma demo")}>Pedí una demo</a>'
                f'<a href="{WA}" target="_blank" rel="noopener" class="btn btn-ghost">WhatsApp</a></div>')
    return (f'<section class="subhero" style="padding-bottom:8px">'
            f'<div class="glow" style="width:520px;height:520px;background:rgba(241,144,0,.16);top:-180px;left:50%;transform:translateX(-50%)"></div>'
            f'<div class="wrap" style="position:relative;z-index:1">'
            f'<div class="eyebrow reveal" style="justify-content:center" {L(*eye)}>{esc(eye[0])}</div>'
            f'<h1 class="reveal" style="max-width:24ch;margin-inline:auto" {L(*h1)}>{esc(h1[0])}</h1>'
            f'<p class="lead reveal" style="max-width:72ch;margin:12px auto 0" {L(*intro)}>{esc(intro[0])}</p>'
            f'{btns}</div></section>')


def feature_cards(items, cls="cx-feats"):
    out = ""
    for t, d in items:
        out += (f'<div class="cx-f reveal"><div class="ti">{CHECK}</div>'
                f'<h3 {L(*t)}>{esc(t[0])}</h3><p {L(*d)}>{esc(d[0])}</p></div>')
    return f'<div class="{cls}">{out}</div>'


def bullets(items, max_w="760px"):
    lis = ""
    for es, en, pt in items:
        lis += (f'<li><svg fill="none" height="18" stroke="currentColor" stroke-width="2.4" viewbox="0 0 24 24" '
                f'width="18"><path d="M20 6L9 17l-5-5"></path></svg><span {L(es,en,pt)}>{esc(es)}</span></li>')
    return f'<ul class="feat" style="max-width:{max_w}">{lis}</ul>'


def chips(items):
    return '<div class="pchips">' + "".join(
        f'<span class="pchip" {L(*c)}>{esc(c[0])}</span>' if isinstance(c, tuple) else f'<span class="pchip">{esc(c)}</span>'
        for c in items) + '</div>'


def kpi_table(rows):
    trs = "".join(f'<tr><th {L(*a)}>{esc(a[0])}</th><td {L(*b)}>{esc(b[0])}</td></tr>' for a, b in rows)
    return f'<div class="reveal" style="overflow-x:auto"><table class="cx-kpitable">{trs}</table></div>'


def cta(h=("¿Cuántos equipos y sedes tenés?", "How many units and sites do you run?", "Quantos equipamentos e unidades você tem?"),
        p=("Contanos qué modalidades usás y dónde están. Te mostramos el panel funcionando y cómo se conecta a tu PACS.",
           "Tell us which modalities you use and where they are. We show you the panel running and how it connects to your PACS.",
           "Conte quais modalidades você usa e onde estão. Mostramos o painel funcionando e como se conecta ao seu PACS.")):
    return (f'<section class="split"><div class="wrap"><div class="ctaband reveal" style="text-align:center">'
            f'<h2 style="max-width:26ch;margin:0 auto 12px" {L(*h)}>{esc(h[0])}</h2>'
            f'<p style="margin:0 auto 22px;max-width:60ch" {L(*p)}>{esc(p[0])}</p>'
            f'<div class="hero-cta" style="justify-content:center">'
            f'<a href="/contacto/" class="btn btn-primary" {L("Pedí una demo","Book a demo","Peça uma demo")}>Pedí una demo</a>'
            f'<a href="{WA}" target="_blank" rel="noopener" class="btn btn-ghost">WhatsApp</a>'
            f'</div></div></div></section>')


def related(current):
    cards = ""
    for s in SPOKES + [CRYO]:
        if s["slug"] == current:
            continue
        cards += (f'<a class="tcard reveal" href="/{s["slug"]}/" style="text-decoration:none">'
                  f'<h4 {L(*s["eye"])}>{esc(s["eye"][0])}</h4>'
                  f'<p {L(*s["card"])}>{esc(s["card"][0])}</p></a>')
    if current != HUB:
        cards = (f'<a class="tcard reveal" href="/{HUB}/" style="text-decoration:none">'
                 f'<h4 {L("Sistema de control de equipamiento médico","Medical equipment control system","Sistema de controle de equipamentos médicos")}>Sistema de control de equipamiento médico</h4>'
                 f'<p {L(*PILLAR_CARD)}>{esc(PILLAR_CARD[0])}</p></a>') + cards
    return section(sec_head(("Seguí leyendo", "Keep reading", "Continue lendo"),
                            ("Todo lo que podés controlar desde el panel", "Everything you can control from the panel", "Tudo o que você pode controlar pelo painel"))
                   + f'<div class="cx-links">{cards}</div>', top=False)


# --------------------------------------------------------------------------
# JSON-LD
# --------------------------------------------------------------------------

FEATURE_LIST = [
    "Panel en vivo de todos los equipos de diagnóstico por imágenes conectados al PACS",
    "Detección automática de equipos a partir de los datos DICOM",
    "Vista multisede y multicliente con filtro por sede, modalidad y equipo",
    "Exámenes por día, por modalidad, por equipo y por hora",
    "Utilización, duración mediana de estudios y tiempo de cambio de paciente por equipo",
    "Metas mensuales por equipo con proyección de cierre",
    "Mapa de calor de ocupación semanal por hora y día",
    "Línea de tiempo por equipo con series y secuencias de cada estudio",
    "Worklist: programado vs. realizado, puntualidad y pacientes no presentados",
    "Productividad por turno (mañana, tarde, noche)",
    "Comparación entre períodos por protocolo",
    "Ranking de médicos solicitantes",
    "Monitoreo de criogenia y acceso remoto para resonadores",
]


def software_ld(path, desc):
    return {"@context": "https://schema.org", "@type": "SoftwareApplication",
            "@id": f"{BASE}/{HUB}/#software",
            "name": "Gauss Connect — sistema de control de equipamiento de diagnóstico por imágenes",
            "alternateName": ["Sistema de control de equipamiento médico", "Panel de control de equipos de diagnóstico por imágenes",
                              "Medical imaging equipment monitoring software"],
            "applicationCategory": "HealthApplication", "applicationSubCategory": "Radiology operations analytics",
            "operatingSystem": "Web", "url": f"{BASE}/{path}", "description": desc,
            "featureList": FEATURE_LIST, "inLanguage": ["es", "en", "pt"],
            "audience": {"@type": "Audience", "audienceType": "Hospitales, clínicas, sanatorios y centros de diagnóstico por imágenes"},
            "provider": ORG, "areaServed": {"@type": "Place", "name": "Worldwide"}}


def webpage_ld(path, name, about=True):
    j = {"@context": "https://schema.org", "@type": "WebPage", "@id": f"{BASE}/{path}#webpage",
         "url": f"{BASE}/{path}", "name": name, "inLanguage": "es",
         "isPartOf": {"@id": BASE + "/#website"}, "datePublished": "2026-11-17", "dateModified": "2026-11-17"}
    if about:
        j["about"] = {"@id": f"{BASE}/{HUB}/#software"}
    return j


def crumbs(path, name):
    items = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"},
             {"@type": "ListItem", "position": 2, "name": "Software", "item": BASE + "/software/"},
             {"@type": "ListItem", "position": 3, "name": "Control de equipamiento médico", "item": f"{BASE}/{HUB}/"}]
    if path != HUB + "/":
        items.append({"@type": "ListItem", "position": 4, "name": name, "item": f"{BASE}/{path}"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "es",
            "mainEntity": [{"@type": "Question", "name": q[0],
                            "acceptedAnswer": {"@type": "Answer", "text": a[0]}} for q, a in faqs]}


def page(path, t, d, jsonld, body):
    """head() de landing_build + estilos del panel. El body va en theme-dark
    como /monitoreo/, para que el pilar y la página de criogenia se sientan una
    misma línea de producto."""
    h = head(path, t, d, jsonld).replace("</head>", CX_STYLE + "\n</head>", 1).replace("<body>", '<body class="theme-dark">', 1)
    # El header viene de index.html con "Inicio" activo; acá corresponde Software.
    h = h.replace('<a class="active" data-en="Home"', '<a data-en="Home"', 1).replace('<a class="nav-soft"', '<a class="nav-soft active"', 1)
    write(path.rstrip("/"), h + body + TAIL)


# --------------------------------------------------------------------------
# Contenido compartido
# --------------------------------------------------------------------------

MODALIDADES = [
    ("Resonancia magnética (RM)", "MRI", "Ressonância magnética (RM)"),
    ("Tomografía computada (TC)", "CT", "Tomografia computadorizada (TC)"),
    ("Rayos X digital (DX · CR)", "Digital X-ray (DX · CR)", "Raio-X digital (DX · CR)"),
    ("Ecografía (US)", "Ultrasound (US)", "Ultrassonografia (US)"),
    ("Mamografía (MG)", "Mammography (MG)", "Mamografia (MG)"),
    ("Angiografía", "Angiography", "Angiografia"),
    ("Fluoroscopía (RF)", "Fluoroscopy (RF)", "Fluoroscopia (RF)"),
    ("Medicina nuclear (NM)", "Nuclear medicine (NM)", "Medicina nuclear (NM)"),
    ("PET", "PET", "PET"),
    ("Densitometría", "Bone densitometry", "Densitometria"),
]
MARCAS = ["GE HealthCare", "Siemens Healthineers", "Philips", "Canon", "Fujifilm", "Samsung", "Carestream",
          ("y cualquier equipo que envíe DICOM", "and any unit that sends DICOM", "e qualquer equipamento que envie DICOM")]

FUNCIONES = [
    (("Resumen de toda la red", "Network-wide overview", "Resumo de toda a rede"),
     ("Clientes, sedes, equipos y exámenes del período en una sola pantalla, con el detalle por modalidad. Pasás de la red completa a una sede o a un equipo con un clic.",
      "Clients, sites, units and exams for the period on one screen, broken down by modality. Go from the whole network to one site or one unit in a click.",
      "Clientes, unidades, equipamentos e exames do período em uma só tela, com detalhe por modalidade. Você vai da rede inteira a uma unidade ou equipamento com um clique.")),
    (("Registro automático de equipos", "Automatic equipment registry", "Registro automático de equipamentos"),
     ("Cada equipo que envía imágenes al PACS aparece solo, con su modalidad, fabricante y modelo. Le ponés un alias y ves su tarjeta: exámenes, tendencia, utilización y hace cuánto hizo el último estudio.",
      "Every unit that sends images to the PACS shows up on its own, with modality, manufacturer and model. Give it an alias and see its card: exams, trend, utilization and how long since its last study.",
      "Cada equipamento que envia imagens ao PACS aparece sozinho, com modalidade, fabricante e modelo. Você dá um apelido e vê o cartão: exames, tendência, utilização e há quanto tempo fez o último estudo.")),
    (("Panel de productividad", "Productivity dashboard", "Painel de produtividade"),
     ("Exámenes totales, promedio por día, exámenes por hora, horas laborales, duración mediana, estudios atípicos y tipos sin clasificar. Con tendencia diaria, semanal o mensual.",
      "Total exams, daily average, exams per hour, working hours, median duration, atypical studies and unclassified types. With daily, weekly or monthly trends.",
      "Exames totais, média por dia, exames por hora, horas trabalhadas, duração mediana, estudos atípicos e tipos sem classificação. Com tendência diária, semanal ou mensal.")),
    (("Metas y proyección del mes", "Monthly goals and forecast", "Metas e projeção do mês"),
     ("Cargás una meta por equipo y el panel te dice si vas adelantado o atrasado, cuántos exámenes por día necesitás para llegar y cómo viene la trayectoria del mes.",
      "Set a goal per unit and the panel tells you whether you are ahead or behind, how many exams per day you need to get there and how the month is trending.",
      "Defina uma meta por equipamento e o painel mostra se você está adiantado ou atrasado, quantos exames por dia faltam e como vai a trajetória do mês.")),
    (("Ocupación y tiempos muertos", "Occupancy and idle time", "Ocupação e tempo ocioso"),
     ("Tasa de ocupación, horas de sala inactiva por día y tiempo promedio de cambio de paciente, con un mapa de calor semanal por hora para ver qué franjas quedan vacías.",
      "Occupancy rate, idle room hours per day and average patient changeover time, with a weekly heat map by hour to see which slots sit empty.",
      "Taxa de ocupação, horas de sala parada por dia e tempo médio de troca de paciente, com mapa de calor semanal por hora para ver quais faixas ficam vazias.")),
    (("Línea de tiempo por equipo", "Per-unit timeline", "Linha do tempo por equipamento"),
     ("El día de cada equipo, estudio por estudio. Hacés clic en un examen y ves sus series y secuencias, la duración real y la eficiencia contra el protocolo.",
      "Each unit's day, study by study. Click an exam to see its series and sequences, the real duration and efficiency against protocol.",
      "O dia de cada equipamento, estudo por estudo. Clique em um exame e veja séries e sequências, a duração real e a eficiência contra o protocolo.")),
    (("Worklist: programado vs. realizado", "Worklist: scheduled vs. performed", "Worklist: agendado vs. realizado"),
     ("Pacientes programados, confirmados, pendientes y no presentados, porcentaje atendido a tiempo y retraso promedio.",
      "Scheduled, confirmed, pending and no-show patients, on-time percentage and average delay.",
      "Pacientes agendados, confirmados, pendentes e faltantes, porcentagem atendida no horário e atraso médio.")),
    (("Turnos y productividad", "Shifts and productivity", "Turnos e produtividade"),
     ("Exámenes, duración promedio y exámenes por hora de cada turno (mañana, tarde, noche), el turno más activo, la hora pico y lo que se hizo fuera de turno.",
      "Exams, average duration and exams per hour for each shift (morning, afternoon, night), the busiest shift, the peak hour and work done off-shift.",
      "Exames, duração média e exames por hora de cada turno (manhã, tarde, noite), o turno mais ativo, o horário de pico e o que foi feito fora de turno.")),
    (("Comparación entre períodos", "Period comparison", "Comparação entre períodos"),
     ("Dos períodos lado a lado: volumen, tiempo de estudio y rotación, y el tiempo de cada protocolo, para medir si un cambio funcionó.",
      "Two periods side by side: volume, study time and turnaround, and time per protocol, to measure whether a change worked.",
      "Dois períodos lado a lado: volume, tempo de estudo e giro, e o tempo de cada protocolo, para medir se uma mudança funcionou.")),
    (("Médicos solicitantes", "Referring physicians", "Médicos solicitantes"),
     ("Quiénes derivan más estudios, de qué modalidades y protocolos, y cuánto tiempo de equipo representan.",
      "Who refers the most studies, for which modalities and protocols, and how much scanner time they represent.",
      "Quem encaminha mais estudos, de quais modalidades e protocolos, e quanto tempo de equipamento representam.")),
    (("Criogenia y acceso remoto en resonancia", "MRI cryogenics and remote access", "Criogenia e acesso remoto em ressonância"),
     ("Para los resonadores: nivel y presión de helio, temperaturas del cold head y del shield, flujo de agua y estado del compresor, con historial, alertas y acceso remoto a la consola.",
      "For MRI scanners: helium level and pressure, cold head and shield temperatures, water flow and compressor status, with history, alerts and remote console access.",
      "Para os ressonadores: nível e pressão de hélio, temperaturas do cold head e do shield, fluxo de água e estado do compressor, com histórico, alertas e acesso remoto ao console.")),
    (("Multisede, multiusuario, multilingüe", "Multi-site, multi-user, multilingual", "Multiunidade, multiusuário, multilíngue"),
     ("Acceso web con usuario propio, selector de cliente y sede, e interfaz en varios idiomas. Lo usan igual la dirección, la jefatura del servicio y la ingeniería biomédica.",
      "Web access with personal logins, client and site selector, and a multilingual interface. Management, department heads and biomedical engineering use the same panel.",
      "Acesso web com usuário próprio, seletor de cliente e unidade, e interface em vários idiomas. Direção, chefia do serviço e engenharia clínica usam o mesmo painel.")),
]

PILLAR_CARD = ("Panel en vivo de todos tus equipos de imágenes conectados al PACS, sin importar cuántos ni en cuántas sedes.",
               "Live panel of all your imaging units connected to the PACS, however many and across however many sites.",
               "Painel ao vivo de todos os seus equipamentos de imagem conectados ao PACS, quantos forem e em quantas unidades.")

CRYO = {"slug": "monitoreo",
        "eye": ("Monitoreo de criogenia MRI", "MRI cryogenics monitoring", "Monitoramento de criogenia MRI"),
        "card": ("Helio, cold head, presión del magneto y riesgo de quench, vigilados 24/7 en cada resonador.",
                 "Helium, cold head, magnet pressure and quench risk, watched 24/7 on every MRI.",
                 "Hélio, cold head, pressão do magneto e risco de quench, vigiados 24/7 em cada ressonador.")}


# --------------------------------------------------------------------------
# Spokes
# --------------------------------------------------------------------------

SPOKES = [
    {
        "slug": f"{HUB}/productividad-diagnostico-por-imagenes",
        "eye": ("Productividad en diagnóstico por imágenes", "Imaging productivity", "Produtividade em diagnóstico por imagem"),
        "card": ("Los indicadores que mueven la producción: exámenes por hora, utilización, rotación, metas y turnos.",
                 "The KPIs that drive output: exams per hour, utilization, turnaround, goals and shifts.",
                 "Os indicadores que movem a produção: exames por hora, utilização, giro, metas e turnos."),
        "t": ("Software de productividad para diagnóstico por imágenes: KPIs por equipo — Nexolibre",
              "Radiology productivity software: per-unit imaging KPIs — Nexolibre",
              "Software de produtividade para diagnóstico por imagem: KPIs por equipamento — Nexolibre"),
        "d": ("Medí la producción de cada resonador, tomógrafo, ecógrafo y rayos X: exámenes por hora, utilización, tiempo de cambio de paciente, metas mensuales y turnos. Indicadores de gestión del servicio de imágenes en un panel.",
              "Measure the output of every MRI, CT, ultrasound and X-ray unit: exams per hour, utilization, patient changeover time, monthly goals and shifts. Imaging department KPIs in one panel.",
              "Meça a produção de cada ressonador, tomógrafo, ultrassom e raio-X: exames por hora, utilização, tempo de troca de paciente, metas mensais e turnos. Indicadores de gestão do serviço de imagem em um painel."),
        "h1": ("Indicadores de productividad para tu servicio de diagnóstico por imágenes",
               "Productivity KPIs for your imaging department",
               "Indicadores de produtividade para o seu serviço de diagnóstico por imagem"),
        "intro": ("Cuánto produce cada equipo, cuánto tiempo pasa parado entre paciente y paciente y si vas a llegar a la meta del mes. Los indicadores de gestión del servicio de imágenes salen solos de los estudios que ya llegan a tu PACS.",
                  "How much each unit produces, how long it sits idle between patients and whether you will hit this month's goal. Imaging department KPIs come straight from the studies already reaching your PACS.",
                  "Quanto produz cada equipamento, quanto tempo fica parado entre um paciente e outro e se você vai chegar à meta do mês. Os indicadores de gestão do serviço de imagem saem sozinhos dos estudos que já chegam ao seu PACS."),
        "sections": "productividad",
        "faqs": [
            (("¿Qué indicadores de productividad mide el sistema?", "Which productivity KPIs does the system measure?", "Quais indicadores de produtividade o sistema mede?"),
             ("Exámenes totales y por día, exámenes por hora activa, horas laborales, duración mediana y promedio por estudio, tiempo de cambio de paciente, utilización por equipo, ocupación por franja horaria, estudios atípicos, cumplimiento de la meta mensual y productividad por turno.",
              "Total and daily exams, exams per active hour, working hours, median and average study duration, patient changeover time, utilization per unit, occupancy by time slot, atypical studies, monthly goal attainment and productivity per shift.",
              "Exames totais e por dia, exames por hora ativa, horas trabalhadas, duração mediana e média por estudo, tempo de troca de paciente, utilização por equipamento, ocupação por faixa horária, estudos atípicos, cumprimento da meta mensal e produtividade por turno.")),
            (("¿Hay que cargar datos a mano?", "Do we need to enter data by hand?", "É preciso carregar dados manualmente?"),
             ("No. Los indicadores se calculan a partir de los estudios que los equipos ya envían al PACS. Lo único que se configura es lo que es decisión tuya: alias de los equipos, metas mensuales y horarios de los turnos.",
              "No. KPIs are calculated from the studies the units already send to the PACS. The only things you configure are your own decisions: unit aliases, monthly goals and shift hours.",
              "Não. Os indicadores são calculados a partir dos estudos que os equipamentos já enviam ao PACS. Só se configura o que é decisão sua: apelidos dos equipamentos, metas mensais e horários dos turnos.")),
            (("¿Cómo calcula si voy a llegar a la meta del mes?", "How does it tell whether I will hit the monthly goal?", "Como calcula se vou chegar à meta do mês?"),
             ("Proyecta el cierre del mes con tres métodos: el ritmo histórico, el ritmo reciente ponderado y un ajuste por la capacidad de trabajo planificada que queda. Te muestra el estado (adelantado o atrasado) y cuántos exámenes por día necesitás para llegar.",
              "It forecasts month-end with three methods: historical pace, weighted recent pace and an adjustment for the planned working capacity left. It shows the status (ahead or behind) and how many exams per day you need.",
              "Projeta o fechamento do mês com três métodos: ritmo histórico, ritmo recente ponderado e um ajuste pela capacidade de trabalho planejada que resta. Mostra o status (adiantado ou atrasado) e quantos exames por dia são necessários.")),
            (("¿Sirve para comparar turnos, equipos o períodos?", "Can it compare shifts, units or periods?", "Serve para comparar turnos, equipamentos ou períodos?"),
             ("Sí. Podés comparar equipos entre sí, turnos de mañana, tarde y noche, y dos períodos cualquiera lado a lado, incluso protocolo por protocolo.",
              "Yes. You can compare units with each other, morning, afternoon and night shifts, and any two periods side by side, even protocol by protocol.",
              "Sim. Você pode comparar equipamentos entre si, turnos da manhã, tarde e noite, e dois períodos quaisquer lado a lado, até protocolo por protocolo.")),
        ],
    },
    {
        "slug": f"{HUB}/tablero-pacs-dicom",
        "eye": ("Tablero conectado a PACS y DICOM", "PACS & DICOM dashboard", "Painel conectado a PACS e DICOM"),
        "card": ("Cómo el panel lee los datos DICOM de tu PACS para mostrarte cada equipo, estudio y protocolo.",
                 "How the panel reads your PACS's DICOM data to show every unit, study and protocol.",
                 "Como o painel lê os dados DICOM do seu PACS para mostrar cada equipamento, estudo e protocolo."),
        "t": ("Dashboard PACS / DICOM para controlar equipos y estudios — Nexolibre",
              "PACS / DICOM dashboard to control imaging units and studies — Nexolibre",
              "Dashboard PACS / DICOM para controlar equipamentos e estudos — Nexolibre"),
        "d": ("Tablero de control conectado a tu PACS: detecta cada equipo por sus datos DICOM y muestra exámenes, protocolos, series y tiempos por modalidad, equipo y sede. Multimarca, para RM, TC, RX, ecografía y mamografía.",
              "Control dashboard connected to your PACS: detects every unit from its DICOM data and shows exams, protocols, series and times by modality, unit and site. Multivendor, for MRI, CT, X-ray, ultrasound and mammography.",
              "Painel de controle conectado ao seu PACS: detecta cada equipamento pelos dados DICOM e mostra exames, protocolos, séries e tempos por modalidade, equipamento e unidade. Multimarca, para RM, TC, RX, ultrassom e mamografia."),
        "h1": ("Un tablero de control que lee tu PACS y te muestra cada equipo",
               "A control dashboard that reads your PACS and shows you every unit",
               "Um painel de controle que lê o seu PACS e mostra cada equipamento"),
        "intro": ("Tu PACS ya guarda, en cada estudio, qué equipo lo hizo, a qué hora, con qué protocolo y cuánto duró. El panel convierte esos datos DICOM en un tablero en vivo de todo tu parque de imágenes, de cualquier marca.",
                  "Your PACS already stores, in every study, which unit acquired it, when, with which protocol and how long it took. The panel turns that DICOM data into a live dashboard of your entire imaging fleet, from any vendor.",
                  "Seu PACS já guarda, em cada estudo, qual equipamento o fez, a que horas, com qual protocolo e quanto durou. O painel transforma esses dados DICOM em um painel ao vivo de todo o seu parque de imagem, de qualquer marca."),
        "sections": "pacs",
        "faqs": [
            (("¿Con qué PACS funciona?", "Which PACS does it work with?", "Com qual PACS funciona?"),
             ("Trabaja sobre el estándar DICOM, que comparten los PACS y los equipos de todas las marcas. En la evaluación inicial revisamos tu PACS y tu red para definir la conexión.",
              "It works on the DICOM standard, shared by PACS and imaging units from every vendor. During the initial assessment we review your PACS and network to define the connection.",
              "Funciona sobre o padrão DICOM, comum aos PACS e equipamentos de todas as marcas. Na avaliação inicial revisamos seu PACS e sua rede para definir a conexão.")),
            (("¿Reemplaza a mi PACS o a mi RIS?", "Does it replace my PACS or RIS?", "Substitui o meu PACS ou RIS?"),
             ("No. El PACS sigue siendo donde se guardan y se informan las imágenes. El panel se suma por encima para darte el control de la operación: equipos, producción, tiempos y metas.",
              "No. The PACS is still where images are stored and reported. The panel sits on top to give you control of operations: units, output, times and goals.",
              "Não. O PACS continua sendo onde as imagens são guardadas e laudadas. O painel se soma por cima para dar o controle da operação: equipamentos, produção, tempos e metas.")),
            (("¿Qué pasa con los equipos de distintas marcas?", "What about units from different vendors?", "E os equipamentos de marcas diferentes?"),
             ("Aparecen todos en el mismo tablero. El panel identifica el fabricante y el modelo de cada equipo a partir de los datos DICOM, y vos le ponés el nombre con el que lo conoce tu equipo.",
              "They all appear on the same dashboard. The panel identifies each unit's manufacturer and model from the DICOM data, and you give it the name your team knows it by.",
              "Todos aparecem no mesmo painel. O painel identifica fabricante e modelo de cada equipamento pelos dados DICOM, e você dá o nome pelo qual sua equipe o conhece.")),
            (("¿Puedo ver el detalle de un estudio puntual?", "Can I see the detail of a single study?", "Posso ver o detalhe de um estudo específico?"),
             ("Sí. Desde la línea de tiempo de cada equipo abrís un estudio y ves sus series o secuencias con horario de inicio y fin, duración y la eficiencia contra lo esperado por protocolo.",
              "Yes. From each unit's timeline you open a study and see its series or sequences with start and end times, duration and efficiency against the protocol's expected time.",
              "Sim. Pela linha do tempo de cada equipamento você abre um estudo e vê suas séries ou sequências com horário de início e fim, duração e eficiência contra o esperado pelo protocolo.")),
        ],
    },
    {
        "slug": f"{HUB}/hospitales-clinicas-multisede",
        "eye": ("Hospitales, clínicas y redes multisede", "Hospitals, clinics and multi-site networks", "Hospitais, clínicas e redes multiunidade"),
        "card": ("Una sola vista para todas tus sedes y equipos, para la dirección, el servicio y la ingeniería.",
                 "One view for all your sites and units, for management, the department and engineering.",
                 "Uma só visão para todas as suas unidades e equipamentos, para direção, serviço e engenharia."),
        "t": ("Control de equipamiento médico para hospitales, clínicas y sanatorios multisede — Nexolibre",
              "Medical equipment control for hospitals, clinics and multi-site imaging networks — Nexolibre",
              "Controle de equipamentos médicos para hospitais, clínicas e redes multiunidade — Nexolibre"),
        "d": ("Gestión del equipamiento de diagnóstico por imágenes en hospitales, clínicas, sanatorios y redes con varias sedes: todos los equipos en un panel, metas por equipo y comparación entre sedes. Sin límite de equipos.",
              "Imaging equipment management for hospitals, clinics and multi-site networks: every unit on one panel, per-unit goals and site-by-site comparison. No limit on units.",
              "Gestão de equipamentos de diagnóstico por imagem em hospitais, clínicas e redes com várias unidades: todos os equipamentos em um painel, metas por equipamento e comparação entre unidades. Sem limite de equipamentos."),
        "h1": ("Control del equipamiento de imágenes para hospitales, clínicas y redes con varias sedes",
               "Imaging equipment control for hospitals, clinics and multi-site networks",
               "Controle dos equipamentos de imagem para hospitais, clínicas e redes com várias unidades"),
        "intro": ("Dos equipos o cincuenta, una sede o diez: el panel muestra todo tu parque de diagnóstico por imágenes en una sola pantalla y te deja bajar a cada sede, modalidad o equipo cuando lo necesitás.",
                  "Two units or fifty, one site or ten: the panel shows your entire imaging fleet on one screen and lets you drill down to any site, modality or unit when you need to.",
                  "Dois equipamentos ou cinquenta, uma unidade ou dez: o painel mostra todo o seu parque de diagnóstico por imagem em uma só tela e permite descer a cada unidade, modalidade ou equipamento quando precisar."),
        "sections": "multisede",
        "faqs": [
            (("¿Hay un límite de equipos o de sedes?", "Is there a limit on units or sites?", "Existe limite de equipamentos ou unidades?"),
             ("No. El panel está pensado para crecer con tu red: cada equipo nuevo que envía estudios al PACS aparece en el registro, y cada sede se suma al selector.",
              "No. The panel is built to grow with your network: every new unit that sends studies to the PACS shows up in the registry, and each site joins the selector.",
              "Não. O painel foi pensado para crescer com sua rede: cada novo equipamento que envia estudos ao PACS aparece no registro, e cada unidade entra no seletor.")),
            (("¿Quién lo usa dentro de la institución?", "Who uses it inside the institution?", "Quem usa dentro da instituição?"),
             ("La dirección y la gerencia, para ver producción y metas de toda la red; la jefatura del servicio de imágenes, para organizar turnos y agenda; y la ingeniería biomédica, para detectar equipos que dejaron de producir y vigilar la criogenia de los resonadores.",
              "Management, to see output and goals across the network; the imaging department head, to organize shifts and scheduling; and biomedical engineering, to spot units that stopped producing and watch MRI cryogenics.",
              "A direção e a gerência, para ver produção e metas de toda a rede; a chefia do serviço de imagem, para organizar turnos e agenda; e a engenharia clínica, para detectar equipamentos que pararam de produzir e vigiar a criogenia dos ressonadores.")),
            (("¿Sirve para un centro de diagnóstico chico?", "Is it useful for a small imaging center?", "Serve para um centro de diagnóstico pequeno?"),
             ("Sí. Con uno o dos equipos ya te sirve para medir la ocupación real, los tiempos muertos y el cumplimiento de la agenda. La vista multisede se activa cuando sumás sedes.",
              "Yes. With one or two units it already measures real occupancy, idle time and schedule compliance. The multi-site view switches on as you add sites.",
              "Sim. Com um ou dois equipamentos já mede a ocupação real, o tempo ocioso e o cumprimento da agenda. A visão multiunidade se ativa quando você soma unidades.")),
            (("¿En qué países está disponible?", "In which countries is it available?", "Em quais países está disponível?"),
             ("El panel es web y se usa desde cualquier país. Nexolibre da implementación y soporte con equipo propio en Latinoamérica y Estados Unidos, en español, inglés y portugués.",
              "The panel is web-based and can be used from any country. Nexolibre provides implementation and support with its own team in Latin America and the United States, in Spanish, English and Portuguese.",
              "O painel é web e pode ser usado de qualquer país. A Nexolibre faz implantação e suporte com equipe própria na América Latina e nos Estados Unidos, em espanhol, inglês e português.")),
        ],
    },
]


# --------------------------------------------------------------------------
# Secciones propias de cada spoke
# --------------------------------------------------------------------------

def sec_productividad():
    rows = [
        (("Exámenes por hora", "Exams per hour", "Exames por hora"),
         ("Estudios realizados dividido las horas en que el equipo estuvo efectivamente trabajando. Es la medida más directa del rendimiento de una sala.",
          "Studies performed divided by the hours the unit was actually working. The most direct measure of a room's throughput.",
          "Estudos realizados divididos pelas horas em que o equipamento esteve efetivamente trabalhando. É a medida mais direta do rendimento de uma sala.")),
        (("Utilización y ocupación", "Utilization and occupancy", "Utilização e ocupação"),
         ("Qué parte del horario disponible el equipo estuvo adquiriendo imágenes. El mapa de calor por hora y día muestra qué franjas quedan vacías.",
          "What share of available hours the unit spent acquiring images. The hour-by-day heat map shows which slots stay empty.",
          "Que parte do horário disponível o equipamento passou adquirindo imagens. O mapa de calor por hora e dia mostra quais faixas ficam vazias.")),
        (("Tiempo de cambio de paciente", "Patient changeover time", "Tempo de troca de paciente"),
         ("El intervalo entre el fin de un estudio y el inicio del siguiente en el mismo equipo: posicionamiento, preparación y tiempo muerto. Los valores altos señalan ausentes o huecos en la agenda.",
          "The gap between the end of one study and the start of the next on the same unit: positioning, preparation and dead time. High values flag no-shows or gaps in the schedule.",
          "O intervalo entre o fim de um estudo e o início do seguinte no mesmo equipamento: posicionamento, preparo e tempo morto. Valores altos indicam faltas ou buracos na agenda.")),
        (("Duración por protocolo", "Duration per protocol", "Duração por protocolo"),
         ("Mediana y promedio de cada descripción de estudio, y la lista de estudios que tardaron mucho más de lo normal para revisarlos uno por uno.",
          "Median and average for each study description, and the list of studies that took far longer than usual so you can review them one by one.",
          "Mediana e média de cada descrição de estudo, e a lista de estudos que demoraram muito mais que o normal para revisá-los um a um.")),
        (("Meta mensual y proyección", "Monthly goal and forecast", "Meta mensal e projeção"),
         ("Exámenes hechos contra la meta del mes por equipo, proyección de cierre y exámenes por día necesarios para llegar.",
          "Exams done against the unit's monthly goal, month-end forecast and exams per day needed to get there.",
          "Exames feitos contra a meta do mês por equipamento, projeção de fechamento e exames por dia necessários para chegar.")),
        (("Productividad por turno", "Productivity per shift", "Produtividade por turno"),
         ("Exámenes, duración promedio y exámenes por hora de mañana, tarde y noche, con la hora pico y lo realizado fuera de turno.",
          "Exams, average duration and exams per hour for morning, afternoon and night, with the peak hour and work done off-shift.",
          "Exames, duração média e exames por hora de manhã, tarde e noite, com o horário de pico e o realizado fora de turno.")),
        (("Puntualidad y ausentismo", "Punctuality and no-shows", "Pontualidade e faltas"),
         ("Desde la worklist: pacientes programados contra atendidos, no presentados, porcentaje atendido a tiempo y retraso promedio.",
          "From the worklist: scheduled vs. seen patients, no-shows, on-time percentage and average delay.",
          "Pela worklist: pacientes agendados contra atendidos, faltas, porcentagem atendida no horário e atraso médio.")),
    ]
    beneficios = [
        ("Detectás qué equipo, qué turno y qué franja horaria están por debajo de su capacidad, con datos y no por intuición.",
         "See which unit, shift and time slot are running below capacity, with data instead of gut feeling.",
         "Você identifica qual equipamento, turno e faixa horária estão abaixo da capacidade, com dados e não por intuição."),
        ("Ajustás la agenda donde el tiempo de cambio de paciente o los ausentes se comen las horas de equipo.",
         "Adjust the schedule where changeover time or no-shows eat into scanner hours.",
         "Você ajusta a agenda onde o tempo de troca ou as faltas consomem as horas de equipamento."),
        ("Sabés a mitad de mes si vas a llegar a la meta, cuando todavía hay tiempo de corregir.",
         "Know mid-month whether you will hit the goal, while there is still time to correct course.",
         "Você sabe no meio do mês se vai chegar à meta, quando ainda há tempo de corrigir."),
        ("Medís el efecto de cada cambio (un protocolo nuevo, un turno extra) comparando dos períodos.",
         "Measure the effect of every change (a new protocol, an extra shift) by comparing two periods.",
         "Você mede o efeito de cada mudança (um protocolo novo, um turno extra) comparando dois períodos."),
        ("Unificás el criterio: todas las sedes y todos los equipos medidos con los mismos indicadores.",
         "One standard: every site and unit measured with the same KPIs.",
         "Você unifica o critério: todas as unidades e equipamentos medidos com os mesmos indicadores."),
    ]
    return (section(sec_head(("Indicadores", "KPIs", "Indicadores"),
                             ("Los indicadores de gestión que ves en el panel", "The management KPIs you see on the panel", "Os indicadores de gestão que você vê no painel"),
                             ("Todos calculados por equipo, por modalidad y por sede, y filtrables por período.",
                              "All calculated per unit, per modality and per site, and filterable by period.",
                              "Todos calculados por equipamento, por modalidade e por unidade, e filtráveis por período.")) + kpi_table(rows))
            + section(sec_head(("Beneficios", "Benefits", "Benefícios"),
                               ("Qué cambia cuando medís la producción de cada equipo", "What changes when you measure each unit's output", "O que muda quando você mede a produção de cada equipamento"))
                      + bullets(beneficios), top=False))


def sec_pacs():
    pasos = [
        (("1 · Conexión al PACS", "1 · PACS connection", "1 · Conexão ao PACS"),
         ("Se conecta al flujo DICOM de tu institución. No hace falta tocar los equipos ni cambiar cómo trabajan los técnicos.",
          "It connects to your institution's DICOM flow. No need to touch the scanners or change how technologists work.",
          "Conecta-se ao fluxo DICOM da sua instituição. Não é preciso mexer nos equipamentos nem mudar como os técnicos trabalham.")),
        (("2 · Detección de equipos", "2 · Unit detection", "2 · Detecção de equipamentos"),
         ("Cada equipo que envía imágenes aparece en el registro con su modalidad, fabricante y modelo. Vos le asignás alias y sede.",
          "Every unit sending images appears in the registry with modality, manufacturer and model. You assign an alias and site.",
          "Cada equipamento que envia imagens aparece no registro com modalidade, fabricante e modelo. Você atribui apelido e unidade.")),
        (("3 · Tablero en vivo", "3 · Live dashboard", "3 · Painel ao vivo"),
         ("Exámenes, tiempos, protocolos y metas de todos tus equipos, por sede y por modalidad, en un solo lugar.",
          "Exams, times, protocols and goals for all your units, by site and modality, in one place.",
          "Exames, tempos, protocolos e metas de todos os seus equipamentos, por unidade e modalidade, em um só lugar.")),
    ]
    datos = [
        (("Equipo, fabricante y modelo", "Unit, manufacturer and model", "Equipamento, fabricante e modelo"),
         ("Para armar solo el registro de equipos y separar la producción de cada uno, aunque sean de marcas distintas.",
          "To build the unit registry automatically and split output per unit, even across vendors.",
          "Para montar sozinho o registro de equipamentos e separar a produção de cada um, mesmo de marcas diferentes.")),
        (("Modalidad", "Modality", "Modalidade"),
         ("RM, TC, CR, DX, US, MG, NM, PT, RF y más, para ver la producción por tipo de equipo.",
          "MR, CT, CR, DX, US, MG, NM, PT, RF and more, to see output by type of unit.",
          "RM, TC, CR, DX, US, MG, NM, PT, RF e mais, para ver a produção por tipo de equipamento.")),
        (("Descripción del estudio y protocolo", "Study description and protocol", "Descrição do estudo e protocolo"),
         ("Para saber qué estudios se hacen más, cuánto dura cada uno y cuáles quedan sin clasificar.",
          "To know which studies are done most, how long each takes and which remain unclassified.",
          "Para saber quais estudos são mais feitos, quanto dura cada um e quais ficam sem classificação.")),
        (("Series, secuencias y horarios", "Series, sequences and timestamps", "Séries, sequências e horários"),
         ("Para reconstruir la línea de tiempo del equipo, la duración real de cada estudio y los huecos entre pacientes.",
          "To rebuild the unit's timeline, the real duration of each study and the gaps between patients.",
          "Para reconstruir a linha do tempo do equipamento, a duração real de cada estudo e os intervalos entre pacientes.")),
        (("Médico solicitante", "Referring physician", "Médico solicitante"),
         ("Para ver de dónde viene la demanda y qué tiempo de equipo representa cada derivador.",
          "To see where demand comes from and how much scanner time each referrer represents.",
          "Para ver de onde vem a demanda e quanto tempo de equipamento representa cada solicitante.")),
    ]
    return (section(sec_head(("Cómo funciona", "How it works", "Como funciona"),
                             ("De los datos DICOM al tablero, en tres pasos", "From DICOM data to dashboard, in three steps", "Dos dados DICOM ao painel, em três passos"))
                    + feature_cards(pasos, "cx-steps"))
            + section(sec_head(("Qué datos usa", "Which data it uses", "Quais dados usa"),
                               ("Lo que el panel aprovecha de cada estudio DICOM", "What the panel uses from each DICOM study", "O que o painel aproveita de cada estudo DICOM"),
                               ("Son datos que el PACS ya tiene. El panel los ordena para que la operación se vea de un vistazo.",
                                "This is data your PACS already holds. The panel organizes it so operations can be seen at a glance.",
                                "São dados que o PACS já tem. O painel os organiza para que a operação seja vista num relance.")) + kpi_table(datos), top=False)
            + section(sec_head(("Multimarca", "Multivendor", "Multimarca"),
                               ("Equipos de cualquier marca en el mismo tablero", "Units from any vendor on the same dashboard", "Equipamentos de qualquer marca no mesmo painel"))
                      + chips(MARCAS), top=False))


def sec_multisede():
    roles = [
        (("Dirección y gerencia", "Management", "Direção e gerência"),
         [("Producción de toda la red y de cada sede en una pantalla", "Output of the whole network and each site on one screen", "Produção de toda a rede e de cada unidade em uma tela"),
          ("Metas por equipo con proyección de cierre de mes", "Per-unit goals with month-end forecast", "Metas por equipamento com projeção de fechamento"),
          ("Comparación entre sedes y entre períodos", "Comparison across sites and periods", "Comparação entre unidades e períodos")]),
        (("Jefatura del servicio de imágenes", "Imaging department head", "Chefia do serviço de imagem"),
         [("Ocupación por franja horaria y tiempos muertos", "Occupancy by time slot and idle time", "Ocupação por faixa horária e tempo ocioso"),
          ("Productividad por turno y hora pico", "Productivity per shift and peak hour", "Produtividade por turno e horário de pico"),
          ("Puntualidad, ausentes y duración por protocolo", "Punctuality, no-shows and duration per protocol", "Pontualidade, faltas e duração por protocolo")]),
        (("Ingeniería biomédica", "Biomedical engineering", "Engenharia clínica"),
         [("Inventario vivo de equipos detectados por sede", "Live inventory of units detected per site", "Inventário vivo de equipamentos detectados por unidade"),
          ("Equipos activos e inactivos, y hace cuánto hicieron el último estudio", "Active and inactive units, and time since their last study", "Equipamentos ativos e inativos, e há quanto tempo fizeram o último estudo"),
          ("Criogenia y acceso remoto de los resonadores", "MRI cryogenics and remote access", "Criogenia e acesso remoto dos ressonadores")]),
    ]
    cards = ""
    for t, items in roles:
        lis = "".join(f'<li {L(*i)}>{esc(i[0])}</li>' for i in items)
        cards += f'<div class="cx-f reveal"><div class="ti">{CHECK}</div><h3 {L(*t)}>{esc(t[0])}</h3><ul>{lis}</ul></div>'
    tipos = [
        (("Hospitales", "Hospitals", "Hospitais"),
         ("Servicios de imágenes con muchas modalidades y demanda de guardia, internación y ambulatorio: ves qué equipo absorbe qué parte de la demanda.",
          "Imaging departments with many modalities and demand from ER, inpatient and outpatient: see which unit absorbs which share of demand.",
          "Serviços de imagem com muitas modalidades e demanda de pronto-socorro, internação e ambulatório: você vê qual equipamento absorve qual parte da demanda.")),
        (("Clínicas y sanatorios", "Clinics and private hospitals", "Clínicas e sanatórios"),
         ("Cada hora de resonador o tomógrafo cuenta. El panel muestra dónde se pierde capacidad y si la agenda se cumple.",
          "Every MRI or CT hour counts. The panel shows where capacity is lost and whether the schedule is met.",
          "Cada hora de ressonador ou tomógrafo conta. O painel mostra onde se perde capacidade e se a agenda é cumprida.")),
        (("Centros y redes de diagnóstico", "Imaging centers and networks", "Centros e redes de diagnóstico"),
         ("Varias sedes, marcas distintas y un solo criterio de medición: comparás sedes y equipos con los mismos indicadores.",
          "Several sites, different vendors and one measurement standard: compare sites and units with the same KPIs.",
          "Várias unidades, marcas diferentes e um só critério de medição: compare unidades e equipamentos com os mesmos indicadores.")),
    ]
    return (section(sec_head(("Para cada institución", "For every institution", "Para cada instituição"),
                             ("Un panel que se adapta al tamaño de tu red", "A panel that fits the size of your network", "Um painel que se adapta ao tamanho da sua rede"))
                    + feature_cards(tipos))
            + section(sec_head(("Para cada rol", "For every role", "Para cada função"),
                               ("La misma información, tres miradas", "The same data, three perspectives", "A mesma informação, três olhares"))
                      + f'<div class="cx-aud">{cards}</div>', top=False)
            + section(sec_head(("Modalidades", "Modalities", "Modalidades"),
                               ("Todas las modalidades conectadas al PACS", "Every modality connected to the PACS", "Todas as modalidades conectadas ao PACS"))
                      + chips(MODALIDADES), top=False))


SECS = {"productividad": sec_productividad, "pacs": sec_pacs, "multisede": sec_multisede}


def render_spoke(s):
    path = s["slug"] + "/"
    jsonld = [webpage_ld(path, s["t"][0]), crumbs(path, s["eye"][0]), faq_ld(s["faqs"])]
    body = (hero(s["eye"], s["h1"], s["intro"])
            + section(mock_panel(), top=False)
            + SECS[s["sections"]]()
            + faq_section(s["faqs"])
            + related(s["slug"])
            + cta())
    page(path, s["t"], s["d"], jsonld, body)


# --------------------------------------------------------------------------
# Pilar
# --------------------------------------------------------------------------

def render_hub():
    path = HUB + "/"
    t = ("Sistema de control de equipamiento médico para diagnóstico por imágenes — Nexolibre",
         "Medical imaging equipment monitoring and control software — Nexolibre",
         "Sistema de controle de equipamentos médicos para diagnóstico por imagem — Nexolibre")
    d = ("Panel en vivo de todos tus equipos de diagnóstico por imágenes conectados al PACS/DICOM: resonancia, tomografía, rayos X, ecografía y mamografía. Producción, ocupación y metas por equipo y por sede, sin límite de equipos.",
         "Live panel of every imaging unit connected to your PACS/DICOM: MRI, CT, X-ray, ultrasound and mammography. Output, occupancy and goals per unit and per site, with no limit on units.",
         "Painel ao vivo de todos os seus equipamentos de diagnóstico por imagem conectados ao PACS/DICOM: ressonância, tomografia, raio-X, ultrassom e mamografia. Produção, ocupação e metas por equipamento e por unidade, sem limite de equipamentos.")
    faqs = [
        (("¿Qué es un sistema de control de equipamiento médico?", "What is a medical equipment control system?", "O que é um sistema de controle de equipamentos médicos?"),
         ("Es un software que reúne en un panel el estado y la producción de los equipos médicos de una institución. En diagnóstico por imágenes, el de Nexolibre se conecta al PACS y muestra, para cada resonador, tomógrafo, rayos X, ecógrafo o mamógrafo, cuántos estudios hace, cuánto tiempo está ocupado o parado y si cumple su meta.",
          "It is software that brings the status and output of an institution's medical equipment into one panel. In diagnostic imaging, Nexolibre's connects to the PACS and shows, for every MRI, CT, X-ray, ultrasound or mammography unit, how many studies it performs, how long it is busy or idle and whether it meets its goal.",
          "É um software que reúne em um painel o estado e a produção dos equipamentos médicos de uma instituição. Em diagnóstico por imagem, o da Nexolibre se conecta ao PACS e mostra, para cada ressonador, tomógrafo, raio-X, ultrassom ou mamógrafo, quantos estudos faz, quanto tempo fica ocupado ou parado e se cumpre sua meta.")),
        (("¿Cuántos equipos y sedes puedo conectar?", "How many units and sites can I connect?", "Quantos equipamentos e unidades posso conectar?"),
         ("Todos los que tengas. Cada equipo que envía estudios al PACS aparece en el registro, y el panel se organiza por cliente, sede, modalidad y equipo.",
          "As many as you have. Every unit that sends studies to the PACS appears in the registry, and the panel is organized by client, site, modality and unit.",
          "Todos os que você tiver. Cada equipamento que envia estudos ao PACS aparece no registro, e o painel se organiza por cliente, unidade, modalidade e equipamento.")),
        (("¿Funciona con equipos de cualquier marca?", "Does it work with units from any vendor?", "Funciona com equipamentos de qualquer marca?"),
         ("Sí. Se basa en el estándar DICOM, así que conviven en el mismo panel equipos de GE, Siemens, Philips, Canon, Fujifilm, Samsung, Carestream y otros.",
          "Yes. It is based on the DICOM standard, so units from GE, Siemens, Philips, Canon, Fujifilm, Samsung, Carestream and others sit on the same panel.",
          "Sim. É baseado no padrão DICOM, então equipamentos GE, Siemens, Philips, Canon, Fujifilm, Samsung, Carestream e outros convivem no mesmo painel.")),
        (("¿Qué modalidades cubre?", "Which modalities does it cover?", "Quais modalidades cobre?"),
         ("Todas las que llegan al PACS: resonancia, tomografía, rayos X digital, ecografía, mamografía, angiografía, fluoroscopía, medicina nuclear y PET, entre otras.",
          "Every modality that reaches the PACS: MRI, CT, digital X-ray, ultrasound, mammography, angiography, fluoroscopy, nuclear medicine and PET, among others.",
          "Todas as que chegam ao PACS: ressonância, tomografia, raio-X digital, ultrassom, mamografia, angiografia, fluoroscopia, medicina nuclear e PET, entre outras.")),
        (("¿Qué diferencia hay con el monitoreo de criogenia?", "How is it different from cryogenics monitoring?", "Qual a diferença com o monitoramento de criogenia?"),
         ("El monitoreo de criogenia vigila la parte técnica del resonador (helio, cold head, presión, compresor). El panel de control suma la producción de todos los equipos de imágenes. Se usan juntos: en el mismo sistema ves la criogenia de tus resonadores y la producción de todo tu parque.",
          "Cryogenics monitoring watches the MRI's technical side (helium, cold head, pressure, compressor). The control panel adds the output of every imaging unit. They work together: in the same system you see your MRIs' cryogenics and your entire fleet's output.",
          "O monitoramento de criogenia vigia a parte técnica do ressonador (hélio, cold head, pressão, compressor). O painel de controle soma a produção de todos os equipamentos de imagem. São usados juntos: no mesmo sistema você vê a criogenia dos ressonadores e a produção de todo o parque.")),
        (("¿Hay que instalar algo en las computadoras?", "Do we need to install anything on computers?", "É preciso instalar algo nos computadores?"),
         ("No. El panel es web: se entra con usuario y contraseña desde el navegador. La conexión con el PACS se define en la implementación con tu equipo de sistemas.",
          "No. The panel is web-based: you log in with a username and password from the browser. The PACS connection is defined during implementation with your IT team.",
          "Não. O painel é web: entra-se com usuário e senha pelo navegador. A conexão com o PACS é definida na implantação com sua equipe de TI.")),
        (("¿En qué países está disponible?", "In which countries is it available?", "Em quais países está disponível?"),
         ("En todo el mundo, en español, inglés y portugués. Nexolibre hace la implementación y el soporte con equipo propio en Latinoamérica y Estados Unidos.",
          "Worldwide, in Spanish, English and Portuguese. Nexolibre handles implementation and support with its own team in Latin America and the United States.",
          "No mundo todo, em espanhol, inglês e português. A Nexolibre faz a implantação e o suporte com equipe própria na América Latina e nos Estados Unidos.")),
    ]
    beneficios = [
        (("Ves todo, en vivo", "See everything, live", "Veja tudo, ao vivo"),
         ("Todos tus equipos de imágenes en una pantalla, con el último estudio de cada uno. Si un equipo dejó de producir, lo ves sin esperar el reporte de fin de mes.",
          "All your imaging units on one screen, with each one's latest study. If a unit stops producing, you see it without waiting for the month-end report.",
          "Todos os seus equipamentos de imagem em uma tela, com o último estudo de cada um. Se um equipamento parou de produzir, você vê sem esperar o relatório do fim do mês.")),
        (("Sacás más de cada equipo", "Get more from every unit", "Tire mais de cada equipamento"),
         ("La ocupación por hora, los tiempos entre pacientes y la duración por protocolo te muestran dónde hay capacidad libre antes de pensar en comprar otro equipo.",
          "Hourly occupancy, time between patients and duration per protocol show where there is free capacity before you think of buying another unit.",
          "A ocupação por hora, o tempo entre pacientes e a duração por protocolo mostram onde há capacidade livre antes de pensar em comprar outro equipamento.")),
        (("Llegás a la meta", "Hit your goals", "Chegue à meta"),
         ("Meta por equipo, proyección del mes y exámenes por día necesarios: sabés a tiempo si hay que reforzar un turno.",
          "Goal per unit, monthly forecast and exams per day needed: know in time whether a shift needs reinforcing.",
          "Meta por equipamento, projeção do mês e exames por dia necessários: você sabe a tempo se precisa reforçar um turno.")),
        (("Una sola medida para todas las sedes", "One standard across sites", "Um só critério para todas as unidades"),
         ("Mismos indicadores en todas tus sedes y en todas las marcas. Comparás de igual a igual y decidís con datos.",
          "The same KPIs across every site and vendor. Compare like for like and decide with data.",
          "Os mesmos indicadores em todas as unidades e marcas. Compare de igual para igual e decida com dados.")),
        (("Agenda que se cumple", "A schedule that holds", "Agenda que se cumpre"),
         ("La worklist cruza lo programado con lo realizado: ausentes, demoras y estudios fuera de turno quedan a la vista.",
          "The worklist matches scheduled against performed: no-shows, delays and off-shift studies are in plain sight.",
          "A worklist cruza o agendado com o realizado: faltas, atrasos e estudos fora de turno ficam à vista.")),
        (("Resonadores protegidos", "Protected MRI scanners", "Ressonadores protegidos"),
         ("En el mismo sistema, la criogenia de cada resonador con historial y alertas, y acceso remoto a la consola para el soporte técnico.",
          "In the same system, each MRI's cryogenics with history and alerts, and remote console access for technical support.",
          "No mesmo sistema, a criogenia de cada ressonador com histórico e alertas, e acesso remoto ao console para o suporte técnico.")),
    ]
    body = (hero(("Sistema de control de equipamiento médico", "Medical equipment control system", "Sistema de controle de equipamentos médicos"),
                 ("Todos tus equipos de diagnóstico por imágenes, en un solo panel en vivo",
                  "All your diagnostic imaging units on one live panel",
                  "Todos os seus equipamentos de diagnóstico por imagem em um só painel ao vivo"),
                 ("Conectado a tu PACS, el panel reconoce cada resonador, tomógrafo, rayos X, ecógrafo y mamógrafo que envía estudios, y te muestra en vivo cuánto produce, cuánto tiempo está parado y si llega a la meta del mes. Sin importar cuántos equipos tengas ni en cuántas sedes estén.",
                  "Connected to your PACS, the panel recognizes every MRI, CT, X-ray, ultrasound and mammography unit that sends studies, and shows you live how much it produces, how long it sits idle and whether it will hit this month's goal. However many units you have and however many sites they are in.",
                  "Conectado ao seu PACS, o painel reconhece cada ressonador, tomógrafo, raio-X, ultrassom e mamógrafo que envia estudos e mostra ao vivo quanto produz, quanto tempo fica parado e se chega à meta do mês. Não importa quantos equipamentos você tenha nem em quantas unidades estejam."))
            + section(mock_panel(), top=False)
            + section(sec_head(("Beneficios", "Benefits", "Benefícios"),
                               ("Control total sobre la producción de tus equipos", "Full control over your units' output", "Controle total sobre a produção dos seus equipamentos"),
                               ("Para hospitales, clínicas, sanatorios y centros de diagnóstico que necesitan saber qué pasa en cada sala sin recorrer las sedes.",
                                "For hospitals, clinics and imaging centers that need to know what happens in every room without touring every site.",
                                "Para hospitais, clínicas, sanatórios e centros de diagnóstico que precisam saber o que acontece em cada sala sem percorrer as unidades."))
                      + feature_cards(beneficios))
            + section(sec_head(("Funciones", "Features", "Funcionalidades"),
                               ("Qué ves en el panel", "What you see on the panel", "O que você vê no painel"),
                               ("Todo sale de los estudios que tus equipos ya envían al PACS.",
                                "Everything comes from the studies your units already send to the PACS.",
                                "Tudo vem dos estudos que seus equipamentos já enviam ao PACS."))
                      + feature_cards(FUNCIONES), top=False)
            + section(sec_head(("Modalidades y marcas", "Modalities and vendors", "Modalidades e marcas"),
                               ("Cualquier equipo que envíe DICOM", "Any unit that sends DICOM", "Qualquer equipamento que envie DICOM"))
                      + chips(MODALIDADES) + '<div style="height:14px"></div>' + chips(MARCAS), top=False)
            + faq_section(faqs)
            + related(HUB)
            + cta())
    desc = d[0]
    jsonld = [software_ld(path, desc), webpage_ld(path, t[0]), crumbs(path, ""), faq_ld(faqs)]
    page(path, t, d, jsonld, body)


def main():
    render_hub()
    for s in SPOKES:
        render_spoke(s)
    print(f"{1 + len(SPOKES)} páginas: /{HUB}/ + " + ", ".join(s["slug"].split("/")[-1] for s in SPOKES))


if __name__ == "__main__":
    main()
