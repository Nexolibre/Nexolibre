#!/usr/bin/env python3
"""
Recorta y desenfoca las capturas del video del desarrollador para la vitrina
de /control-equipamiento-medico/. Quita la barra del navegador y la barra
lateral (logo, nombre del producto, cliente, sede, usuario) y desenfoca
columna de pacientes, números de acceso, IDs y datos del resonador.
El repo es público: ninguna captura entra sin pasar por acá.
Uso: python3 tools/control_capturas.py <carpeta-con-hi/> [salida]
"""
import sys
from PIL import Image, ImageFilter
S=sys.argv[1]  # carpeta con hi/tNNN.jpg extraídos del video (ffmpeg -ss NNN -frames:v 1)
OUT=sys.argv[2] if len(sys.argv)>2 else "assets/control"
K=1.5  # coords medidas a 1280 de ancho; el video es 1920
MAIN=(160,110,1280,720)
shots={
 "resumen":("t10",MAIN,[(725,600,1265,720)]),
 "equipos":("t70",MAIN,[]),
 "productividad":("t100",MAIN,[]),
 "metas":("t290",MAIN,[]),
 "ocupacion":("t360",MAIN,[(370,146,760,168)]),
 "linea-tiempo":("t420",MAIN,[(236,517,290,533)]),
 "worklist":("t575",MAIN,[(455,330,530,720)]+[(540,y-8,600,y+8) for y in (368,411,455,497,540,584,627,671,714)]),
 "turnos":("t590",MAIN,[]),
 "analisis":("t505",MAIN,[]),
 "criogenia":("t630",(245,75,1100,540),[(455,845,1095,960),(250,885,345,960)]),
}
for name,(src,crop,blurs) in shots.items():
    im=Image.open(f"{S}/hi/{src}.jpg").convert("RGB")
    for (x0,y0,x1,y1) in blurs:
        if name=="criogenia": y0-=720; y1-=720
        b=tuple(int(v*K) for v in (x0,y0,x1,y1))
        reg=im.crop(b).filter(ImageFilter.GaussianBlur(14))
        im.paste(reg,b)
    c=im.crop(tuple(int(v*K) for v in crop))
    c=c.resize((1400,int(c.height*1400/c.width)),Image.LANCZOS)
    c.save(f"{OUT}/{name}.webp",quality=80,method=6)
    print(name,c.size)
