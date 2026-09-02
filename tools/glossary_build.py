#!/usr/bin/env python3
"""
Genera /glosario/ : términos del dominio (MRI/CT) con <dl> y schema DefinedTermSet.
Mejora la desambiguación de entidades para motores de IA (GEO) y suma una sección
de fuentes autoritativas (FDA, RSNA, ACR) para 'citations'.

ES con data-en/data-pt para que i18n_build produzca /en/ y /pt/.
Uso:  python3 tools/glossary_build.py   (luego correr i18n_build.py)
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


# (término es/en/pt, definición es/en/pt)
TERMS = [
    (("Bobina (MRI coil)", "Coil (MRI coil)", "Bobina (MRI coil)"),
     ("Antena de radiofrecuencia que transmite y recibe la señal en resonancia magnética. Existen bobinas de superficie, phased array, de cuadratura, articulares, de cabeza, columna y cuerpo.",
      "Radiofrequency antenna that transmits and receives the signal in MRI. Types include surface, phased-array, quadrature, joint, head, spine and body coils.",
      "Antena de radiofrequência que transmite e recebe o sinal na ressonância magnética. Há bobinas de superfície, phased-array, de quadratura, articulares, de cabeça, coluna e corpo.")),
    (("Gradiente", "Gradient", "Gradiente"),
     ("Sistema que genera campos magnéticos variables para codificar espacialmente la imagen de MRI. Incluye amplificadores de gradiente (GPA) y placas de control.",
      "System that generates varying magnetic fields to spatially encode the MRI image. Includes gradient power amplifiers (GPA) and control boards.",
      "Sistema que gera campos magnéticos variáveis para codificar espacialmente a imagem de MRI. Inclui amplificadores de gradiente (GPA) e placas de controle.")),
    (("Radiofrecuencia (RF)", "Radiofrequency (RF)", "Radiofrequência (RF)"),
     ("Cadena que emite y recibe pulsos de RF en resonancia magnética. Incluye amplificadores de potencia (RFPA) y módulos de transmisión y recepción (T/R).",
      "Chain that emits and receives RF pulses in MRI. Includes power amplifiers (RFPA) and transmit/receive (T/R) modules.",
      "Cadeia que emite e recebe pulsos de RF na ressonância magnética. Inclui amplificadores de potência (RFPA) e módulos de transmissão e recepção (T/R).")),
    (("Quench", "Quench", "Quench"),
     ("Pérdida súbita de la superconductividad del imán de MRI, que libera el helio a la atmósfera. Es un evento crítico que se busca prevenir con monitoreo.",
      "Sudden loss of the MRI magnet's superconductivity, releasing helium to the atmosphere. A critical event that monitoring aims to prevent.",
      "Perda súbita da supercondutividade do ímã de MRI, que libera o hélio para a atmosfera. É um evento crítico que se busca prevenir com monitoramento.")),
    (("Cold head", "Cold head", "Cold head"),
     ("Cabezal frío del sistema criogénico que mantiene el imán superconductor a temperatura de helio líquido. Su falla puede derivar en pérdida de helio.",
      "Cold head of the cryogenic system that keeps the superconducting magnet at liquid-helium temperature. Its failure can lead to helium loss.",
      "Cabeçote frio do sistema criogênico que mantém o ímã supercondutor à temperatura de hélio líquido. Sua falha pode levar à perda de hélio.")),
    (("Helio", "Helium", "Hélio"),
     ("Gas criogénico que enfría el imán superconductor de MRI. Su nivel es un indicador clave del estado del equipo.",
      "Cryogenic gas that cools the MRI superconducting magnet. Its level is a key indicator of equipment health.",
      "Gás criogênico que resfria o ímã supercondutor de MRI. Seu nível é um indicador-chave do estado do equipamento.")),
    (("Magneto / imán", "Magnet", "Magneto / ímã"),
     ("Imán superconductor que genera el campo magnético principal de un resonador, medido en Tesla (por ejemplo 0,3T, 1,5T o 3T).",
      "Superconducting magnet that generates an MRI scanner's main magnetic field, measured in Tesla (e.g. 0.3T, 1.5T or 3T).",
      "Ímã supercondutor que gera o campo magnético principal de um ressonador, medido em Tesla (por exemplo 0,3T, 1,5T ou 3T).")),
    (("Inyector de contraste", "Contrast injector", "Injetor de contraste"),
     ("Equipo que administra medio de contraste de forma controlada en estudios de resonancia magnética y tomografía.",
      "Device that delivers contrast media in a controlled way during MRI and CT studies.",
      "Equipamento que administra meio de contraste de forma controlada em estudos de ressonância e tomografia.")),
    (("DICOM", "DICOM", "DICOM"),
     ("Estándar internacional para almacenar, transmitir y visualizar imágenes médicas.",
      "International standard for storing, transmitting and viewing medical images.",
      "Padrão internacional para armazenar, transmitir e visualizar imagens médicas.")),
    (("PACS", "PACS", "PACS"),
     ("Sistema de archivo y comunicación de imágenes médicas (Picture Archiving and Communication System).",
      "Picture Archiving and Communication System for medical images.",
      "Sistema de arquivamento e comunicação de imagens médicas (PACS).")),
    (("RIS", "RIS", "RIS"),
     ("Sistema de información radiológica para la gestión de estudios, agendas y flujos de trabajo.",
      "Radiology Information System for managing studies, scheduling and workflows.",
      "Sistema de informação radiológica para gestão de estudos, agendas e fluxos de trabalho.")),
    (("MRI (resonancia magnética)", "MRI (magnetic resonance)", "MRI (ressonância magnética)"),
     ("Modalidad de diagnóstico por imágenes que usa campos magnéticos y radiofrecuencia, sin radiación ionizante.",
      "Diagnostic imaging modality that uses magnetic fields and radiofrequency, with no ionizing radiation.",
      "Modalidade de diagnóstico por imagem que usa campos magnéticos e radiofrequência, sem radiação ionizante.")),
    (("CT (tomografía computada)", "CT (computed tomography)", "CT (tomografia computadorizada)"),
     ("Modalidad que usa rayos X para producir imágenes transversales del cuerpo.",
      "Modality that uses X-rays to produce cross-sectional images of the body.",
      "Modalidade que usa raios X para produzir imagens transversais do corpo.")),
]

SOURCES = [
    ("U.S. Food and Drug Administration (FDA)", "https://www.fda.gov/"),
    ("Radiological Society of North America (RSNA)", "https://www.rsna.org/"),
    ("American College of Radiology (ACR)", "https://www.acr.org/"),
    ("RadiologyInfo.org", "https://www.radiologyinfo.org/"),
]


def build():
    url = f"{BASE}/glosario/"
    t = ("Glosario MRI/CT: bobina, gradiente, RF, quench y más — Nexolibre",
         "MRI/CT glossary: coil, gradient, RF, quench and more — Nexolibre",
         "Glossário MRI/CT: bobina, gradiente, RF, quench e mais — Nexolibre")
    d = ("Glosario de términos de resonancia magnética (MRI) y tomografía (CT): bobina, gradiente, RF, quench, cold head, helio, DICOM, PACS y más, explicados por Nexolibre.",
         "Glossary of MRI and CT terms: coil, gradient, RF, quench, cold head, helium, DICOM, PACS and more, explained by Nexolibre.",
         "Glossário de termos de MRI e CT: bobina, gradiente, RF, quench, cold head, hélio, DICOM, PACS e mais, explicados pela Nexolibre.")

    dl = ""
    for (tes, ten, tpt), (des, den, dpt) in TERMS:
        dl += (f'<dt {L(tes,ten,tpt)}>{esc(tes)}</dt>'
               f'<dd {L(des,den,dpt)}>{esc(des)}</dd>')
    srcs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in SOURCES)

    defined = {"@context": "https://schema.org", "@type": "DefinedTermSet",
               "@id": url + "#glosario", "name": "Glosario MRI/CT — Nexolibre", "url": url,
               "hasDefinedTerm": [{"@type": "DefinedTerm", "name": tes, "description": des,
                                   "inDefinedTermSet": url + "#glosario"}
                                  for (tes, _, _), (des, _, _) in TERMS]}
    crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Glosario", "item": url}]}

    head = f'''<!DOCTYPE html>
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
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">{json.dumps(defined, ensure_ascii=False, separators=(",",":"))}</script>
<script type="application/ld+json">{json.dumps(crumb, ensure_ascii=False, separators=(",",":"))}</script>
</head>
<body>
{HEADER}
<main id="top">
<section class="subhero" style="padding-bottom:8px">
<div class="glow" style="width:520px;height:520px;background:rgba(241,144,0,.16);top:-180px;left:50%;transform:translateX(-50%)"></div>
<div class="wrap">
<div class="eyebrow reveal" style="justify-content:center" {L("Glosario","Glossary","Glossário")}>Glosario</div>
<h1 class="reveal" {L("Glosario de términos MRI/CT","MRI/CT glossary","Glossário de termos MRI/CT")}>Glosario de términos MRI/CT</h1>
<p class="lead reveal" style="max-width:70ch;margin:12px auto 0" {L("Definiciones claras de los términos de resonancia magnética y tomografía con los que trabajamos a diario.","Clear definitions of the MRI and CT terms we work with every day.","Definições claras dos termos de MRI e CT com os quais trabalhamos diariamente.")}>Definiciones claras de los términos de resonancia magnética y tomografía con los que trabajamos a diario.</p>
</div>
</section>
<section class="split" style="padding-top:32px"><div class="wrap">
<dl class="glossary">{dl}</dl>
<h2 {L("Fuentes y referencias","Sources and references","Fontes e referências")} style="margin-top:40px">Fuentes y referencias</h2>
<ul class="src-list">{srcs}</ul>
</div></section>
{_idx_cta()}
</main>
{FOOTER}
<script src="/app.js" defer></script>
</body>
</html>'''
    os.makedirs(os.path.join(ROOT, "glosario"), exist_ok=True)
    open(os.path.join(ROOT, "glosario", "index.html"), "w", encoding="utf-8").write(head)
    print("glosario/ generado (" + str(len(TERMS)) + " términos + " + str(len(SOURCES)) + " fuentes)")


def _idx_cta():
    return (f'<section class="split" style="padding-top:0"><div class="wrap"><div class="ctaband reveal" style="text-align:center">'
            f'<h2 style="max-width:24ch;margin:0 auto 12px" {L("¿Necesitás reparar o conseguir una pieza?","Need to repair or source a part?","Precisa reparar ou conseguir uma peça?")}>¿Necesitás reparar o conseguir una pieza?</h2>'
            f'<div class="hero-cta" style="justify-content:center;margin-top:8px">'
            f'<a href="/reparacion/" class="btn btn-primary" {L("Ver reparaciones","See repairs","Ver reparos")}>Ver reparaciones</a>'
            f'<a href="/catalogo/" class="btn btn-ghost" {L("Ver catálogo","Browse catalog","Ver catálogo")}>Ver catálogo</a>'
            f'</div></div></div></section>')


if __name__ == "__main__":
    build()
