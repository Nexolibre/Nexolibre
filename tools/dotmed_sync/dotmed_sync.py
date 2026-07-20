#!/usr/bin/env python3
"""
Sincroniza el catálogo de Nexolibre con DOTmed (API oficial de vendedor).

Compara el catálogo (parts.json) con tus listings de DOTmed y:
  · publica las piezas marcadas para DOTmed que aún no están,
  · borra de DOTmed las que ya no están en el catálogo (vendidas),
  · re-edita las que están en ambos → refresca la fecha para que no expiren.

El match se hace por SKU = Ref del catálogo (ej. NX-AR-001).
SEGURIDAD: solo toca listings cuyo SKU empieza con el prefijo configurado,
así nunca borra publicaciones que hayas creado a mano en DOTmed.

Credenciales (NO van en el código): variable de entorno
  DOTMED_AUTH = "tu_secret_key:tu-email@dominio.com"

Modo:
  Por defecto corre en SIMULACIÓN (muestra el plan, no modifica nada).
  Para aplicar de verdad: DOTMED_APPLY=1
"""
import os, json, re, time, urllib.parse, urllib.request, urllib.error

HERE  = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG   = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
AUTH  = os.environ.get("DOTMED_AUTH", "").strip()
APPLY = os.environ.get("DOTMED_APPLY", "").strip() == "1"
API   = "https://api.dotmed.com/ajax/requests/api/v2"


# ---------------------------------------------------------------- utilidades
def _req(url, data=None, method="GET"):
    headers = {"X-DOTMED-AUTH": AUTH, "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data, ensure_ascii=False).encode("utf-8")
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8", "ignore") or "{}")
    except urllib.error.HTTPError as e:
        detalle = ""
        try: detalle = e.read().decode("utf-8", "ignore")[:300]
        except Exception: pass
        raise SystemExit(f"! DOTmed HTTP {e.code}: {detalle}")


def precio_num(v):
    """'1.200,00' -> 1200.0 ; 'Consultar' -> None"""
    if v is None: return None
    s = str(v).strip()
    if not s or not re.search(r"\d", s): return None      # 'Consultar', '', etc.
    s = re.sub(r"[^\d.,]", "", s)
    if "," in s and "." in s:          # formato es-AR: 1.200,00
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:                      # 1200,50
        s = s.replace(",", ".")
    try:
        n = float(s)
        return n if n > 0 else None
    except ValueError:
        return None


def mapear(tabla, valor, default):
    v = (valor or "").strip().lower()
    if not v: return default
    if v in tabla: return tabla[v]
    for k, out in tabla.items():        # coincidencia parcial
        if k in v: return out
    return default


def imagenes(p):
    base = CFG["base_url_imagenes"]
    out = []
    for f in re.split(r"[;,\n]+", str(p.get("imagen") or "")):
        f = f.strip()
        if not f: continue
        out.append(f if re.match(r"^https?://", f, re.I) else base + f)
    return out[:8]


def a_listing(p):
    """Convierte una pieza del catálogo en un listing de DOTmed (tipo 'part')."""
    cat  = mapear(CFG["categorias"], p.get("categoria") or p.get("modalidad"),
                  CFG["categoria_default"])
    cond = mapear(CFG["condiciones"], p.get("estado"), CFG["condicion_default"])
    marca = (p.get("marca") or "").strip()
    comentarios = " · ".join(x for x in [
        p.get("descripcion"),
        f"Ubicación: {p.get('ubicacion')}" if p.get("ubicacion") else None,
        f"Garantía: {int(p['garantia'])} días" if p.get("garantia") else None,
    ] if x)
    L = {
        "sku": p["ref"],
        "type": "part",
        "wanted": "For Sale",
        "category": cat,
        "mfg": marca,
        "part_mfg": marca,
        "model": (p.get("modelo_compatible") or marca or "N/A")[:128],
        "part_number": (p.get("nro_parte") or "N/A")[:128],
        "part_description_or_item_name": (p.get("nombre") or "")[:128],
        "condition": cond,
        "comments": comentarios or (p.get("nombre") or ""),
        "quantity": CFG.get("quantity_default", 1),
        "currency": CFG.get("moneda", "US Dollars"),
        "in_stock": "y" if "stock" in (p.get("disponibilidad") or "").lower() else "n",
        "make_offer": CFG.get("make_offer", "y"),
        "auto_renew": CFG.get("auto_renew", "1"),
    }
    precio = precio_num(p.get("precio"))
    if precio: L["price"] = f"{precio:.2f}"
    imgs = imagenes(p)
    if imgs: L["images"] = imgs
    return L


def publicables(parts):
    """Piezas marcadas para DOTmed. Si el flag no existe todavía en parts.json,
    avisa y no publica nada (para no publicar de más por accidente)."""
    con_flag = [p for p in parts if "dotmed" in p]
    if not con_flag:
        print("! parts.json todavía no trae el campo 'dotmed' (flag 'Publicar en DOTmed').")
        print("  Agregá esa línea al paso 'Seleccionar' del flujo y volvé a correr.")
        return []
    def si(v): return str(v).strip().lower() in ("true", "1", "si", "sí", "yes", "y")
    return [p for p in con_flag if si(p.get("dotmed")) and p.get("ref")]


# ---------------------------------------------------------------- DOTmed API
def listings_actuales():
    """Todos los listings vigentes, indexados por SKU."""
    porsku, page = {}, 1
    while page <= 50:
        q = urllib.parse.urlencode({"status": "running", "limit": 200,
                                    "page": page, "detailed": 1})
        data = _req(f"{API}/listings.json?{q}")
        lote = data.get("listings") or []
        for l in lote:
            sku = (l.get("sku") or "").strip()
            if sku: porsku[sku] = l
        if len(lote) < 200: break
        page += 1; time.sleep(0.3)
    return porsku


def add_edit(lote):
    return _req(f"{API}/add.json", data={"listings": {"listing": lote}}, method="POST")


def borrar(listing_id):
    return _req(f"{API}/delete.json?listing={urllib.parse.quote(str(listing_id))}")


# ---------------------------------------------------------------- main
def main():
    if not AUTH:
        raise SystemExit("Falta DOTMED_AUTH ('secret_key:email') en el entorno.")

    parts = json.load(open(os.path.join(ROOT, "parts.json"), encoding="utf-8"))
    quiero = {p["ref"]: a_listing(p) for p in publicables(parts)}
    print(f"Catálogo: {len(parts)} piezas · marcadas para DOTmed: {len(quiero)}")
    if not quiero:
        return

    actuales = listings_actuales()
    prefijo  = CFG.get("prefijo_sku", "NX-")
    mios     = {s: l for s, l in actuales.items() if s.startswith(prefijo)}
    print(f"DOTmed: {len(actuales)} listings vigentes ({len(mios)} gestionados por el agente)")

    alta      = [sku for sku in quiero if sku not in mios]
    actualiza = [sku for sku in quiero if sku in mios]
    baja      = [sku for sku in mios if sku not in quiero]

    print(f"\nPLAN → publicar {len(alta)} · actualizar/refrescar {len(actualiza)} · borrar {len(baja)}")
    for s in alta[:10]:      print(f"  + {s}  {quiero[s]['part_description_or_item_name'][:52]}")
    if len(alta) > 10:       print(f"    … y {len(alta)-10} más")
    for s in baja[:10]:      print(f"  - {s}  (ya no está en el catálogo)")
    if len(baja) > 10:       print(f"    … y {len(baja)-10} más")

    if not APPLY:
        print("\n(SIMULACIÓN — no se modificó nada. Para aplicar: DOTMED_APPLY=1)")
        return

    # altas + actualizaciones van juntas: add.json crea o edita según el SKU
    lote = [quiero[s] for s in alta + actualiza]
    for i in range(0, len(lote), 50):
        chunk = lote[i:i+50]
        r = add_edit(chunk)
        print(f"  add/edit {i+1}-{i+len(chunk)}: {json.dumps(r, ensure_ascii=False)[:200]}")
        time.sleep(1)

    for s in baja:
        lid = mios[s].get("id")
        if not lid: continue
        r = borrar(lid)
        print(f"  borrado {s} (#{lid}): {json.dumps(r, ensure_ascii=False)[:120]}")
        time.sleep(0.5)

    print("\nSincronización aplicada.")


if __name__ == "__main__":
    main()
