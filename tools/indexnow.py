#!/usr/bin/env python3
"""
Avisa a los buscadores (Bing, Yandex, Seznam) que las URLs del sitemap
cambiaron, vía el protocolo IndexNow. Acelera la re-indexación tras cada deploy
— clave para aparecer rápido en Bing y, por lo tanto, en motores de IA
(ChatGPT/Copilot usan el índice de Bing).

La key vive en https://nexolibre.com/<KEY>.txt (archivo en la raíz del repo).

Uso:  python3 tools/indexnow.py
Correr después de git push (cuando GitHub Pages ya publicó los cambios).
"""
import os, re, json, glob, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
HOST = "nexolibre.com"
ENDPOINT = "https://api.indexnow.org/indexnow"


def find_key():
    for f in glob.glob(os.path.join(ROOT, "*.txt")):
        name = os.path.basename(f)[:-4]
        if re.fullmatch(r"[0-9a-f]{32}", name):
            return name
    return None


def sitemap_urls():
    p = os.path.join(ROOT, "sitemap.xml")
    xml = open(p, encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", xml)


def main():
    key = find_key()
    if not key:
        print("No encontré la key IndexNow (<32hex>.txt en la raíz).")
        return
    urls = sitemap_urls()
    if not urls:
        print("Sitemap sin URLs.")
        return
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow: {r.status} — {len(urls)} URLs enviadas a Bing/Yandex.")
    except Exception as e:
        print(f"IndexNow falló: {e}")


if __name__ == "__main__":
    main()
