#!/usr/bin/env python3
"""
Comprime los PDFs del catálogo (assets/catalogo-nexolibre-{es,en,pt}.pdf)
recomprimiendo las imágenes embebidas: baja a máx 1100 px y reencoda JPEG q72.
Reduce ~9,8 MB -> ~3,1 MB por archivo sin perder páginas ni texto.

Requiere: pip install pymupdf pillow
Uso:      python3 tools/catalog_pdf/compress.py
Correr después de build_catalog.py + el print a PDF con Chrome headless.
"""
import fitz, io, os
from PIL import Image

MAXDIM = 1100
Q = 72
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def compress(path):
    doc = fitz.open(path)
    xrefs = {im[0] for p in doc for im in p.get_images(full=True)}
    done = 0
    for xref in xrefs:
        try:
            d = doc.extract_image(xref)
        except Exception:
            continue
        if not d:
            continue
        im = Image.open(io.BytesIO(d["image"]))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        w, h = im.size
        if max(w, h) > MAXDIM:
            s = MAXDIM / max(w, h)
            im = im.resize((int(w * s), int(h * s)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=Q, optimize=True)
        newb = buf.getvalue()
        if len(newb) < d["size"]:
            for p in doc:
                if any(i[0] == xref for i in p.get_images(full=True)):
                    p.replace_image(xref, stream=newb)
                    break
            done += 1
    tmp = path + ".tmp"
    doc.save(tmp, garbage=4, deflate=True, clean=True)
    doc.close()
    os.replace(tmp, path)
    return done, os.path.getsize(path)


def main():
    for lang in ("es", "en", "pt"):
        p = os.path.join(ROOT, f"assets/catalogo-nexolibre-{lang}.pdf")
        if not os.path.exists(p):
            print("  falta:", p)
            continue
        n, sz = compress(p)
        print(f"{lang}: {n} imágenes recomprimidas -> {sz/1e6:.2f} MB")


if __name__ == "__main__":
    main()
