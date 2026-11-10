#!/usr/bin/env python3
"""Copia tutoriales de Telegraph al sitio, con sus imágenes.

Para cada tutorial de datos/indice.yml que apunte a telegra.ph:
  1. Lee la página con la API pública de Telegraph.
  2. La convierte a Markdown en docs/tutoriales/<nombre>/index.md
  3. Descarga sus imágenes a esa misma carpeta.
  4. Cambia el enlace en datos/indice.yml para que apunte a la copia
     (y guarda el enlace de Telegraph en el campo "original").

Copia todos los tutoriales del índice: estar en el índice implica que el autor
aprobó su publicación. Cada copia conserva el nombre del autor y el enlace al original.

Uso (desde la carpeta del proyecto):
    python3 scripts/importar_telegraph.py --simular     # muestra qué haría, sin tocar nada
    python3 scripts/importar_telegraph.py               # copia todos
    python3 scripts/importar_telegraph.py --solo-mios   # copia solo los tuyos
    python3 scripts/importar_telegraph.py --autor "@Inatxo"   # solo los de ese autor
    python3 scripts/importar_telegraph.py --url https://telegra.ph/Algo-01-01   # solo uno

Se puede correr varias veces: lo que ya está copiado se saltea.
Solo usa la biblioteca estándar de Python y PyYAML (python3-yaml en Linux Mint).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
INDICE = RAIZ / "datos" / "indice.yml"
DESTINO = RAIZ / "docs" / "tutoriales"

API = "https://api.telegra.ph/getPage/{ruta}?return_content=true"
AGENTE = "IndiceCalibreEnEspanol/1.0 (+https://github.com/Dunhill69/indice-calibre)"

# Cómo reconocer los tutoriales propios en los datos de Telegraph.
MIS_NOMBRES = {"walter", "dunhill", "dunhill69"}
MI_ENLACE = "dunhill69"


# --------------------------------------------------------------------------- red

def descargar(url: str, intentos: int = 3) -> bytes:
    ultimo_error = None
    for intento in range(intentos):
        try:
            pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE})
            with urllib.request.urlopen(pedido, timeout=30) as respuesta:
                return respuesta.read()
        except (urllib.error.URLError, TimeoutError) as e:
            ultimo_error = e
            time.sleep(1.5 * (intento + 1))
    raise RuntimeError(f"no se pudo descargar {url}: {ultimo_error}")


def leer_pagina(url_telegraph: str) -> dict:
    ruta = urllib.parse.urlparse(url_telegraph).path.strip("/")
    datos = json.loads(descargar(API.format(ruta=ruta)))
    if not datos.get("ok"):
        raise RuntimeError(f"Telegraph respondió con error: {datos.get('error')}")
    return datos["result"]


# --------------------------------------------------------------------------- utilidades

def nombre_carpeta(url_telegraph: str) -> str:
    """telegra.ph/Abrir-libro-al-azar-09-19  ->  abrir-libro-al-azar"""
    ruta = urllib.parse.unquote(urllib.parse.urlparse(url_telegraph).path.strip("/"))
    ruta = re.sub(r"-\d{2}-\d{2}(-\d+)?$", "", ruta)  # quita la fecha MM-DD del final
    ruta = unicodedata.normalize("NFD", ruta.lower())
    ruta = "".join(c for c in ruta if unicodedata.category(c) != "Mn")
    ruta = re.sub(r"[^a-z0-9]+", "-", ruta).strip("-")
    return ruta or "tutorial"


def es_mio(pagina: dict) -> bool:
    nombre = (pagina.get("author_name") or "").strip().lower()
    enlace = (pagina.get("author_url") or "").lower()
    return nombre in MIS_NOMBRES or MI_ENLACE in enlace


def autor_coincide(pagina: dict, entrada: dict, autores: set[str]) -> bool:
    if not autores:
        return False
    candidatos = {
        (entrada.get("autor") or "").lower().lstrip("@"),
        (pagina.get("author_name") or "").lower().lstrip("@"),
        (pagina.get("author_url") or "").lower().rstrip("/").rsplit("/", 1)[-1],
    }
    return bool(candidatos & autores)


# --------------------------------------------------------------------------- Telegraph -> Markdown

ESCAPAR = re.compile(r"([\\`*_\[\]<>|])")


def texto_seguro(texto: str) -> str:
    return ESCAPAR.sub(r"\\\1", texto)


class Conversor:
    """Convierte los nodos de Telegraph (texto o {tag, attrs, children}) a Markdown."""

    def __init__(self, carpeta: Path, base: str):
        self.carpeta = carpeta
        self.base = base
        self.imagenes = 0
        self.avisos: list[str] = []

    # ---- imágenes
    def guardar_imagen(self, src: str) -> str:
        url = urllib.parse.urljoin(self.base, src)
        if not url.startswith(("http://", "https://")):
            return src
        try:
            datos = descargar(url)
        except RuntimeError as e:
            self.avisos.append(str(e))
            return url  # se deja el enlace remoto
        extension = Path(urllib.parse.urlparse(url).path).suffix.lower() or ".jpg"
        if extension not in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}:
            extension = ".jpg"
        self.imagenes += 1
        nombre = f"imagen{self.imagenes:02d}{extension}"
        (self.carpeta / nombre).write_bytes(datos)
        return nombre

    # ---- texto en línea
    def en_linea(self, nodos) -> str:
        partes = []
        for n in nodos or []:
            if isinstance(n, str):
                partes.append(texto_seguro(n))
                continue
            tag = n.get("tag")
            hijos = n.get("children")
            dentro = self.en_linea(hijos)
            if tag in ("b", "strong"):
                partes.append(f"**{dentro}**" if dentro.strip() else dentro)
            elif tag in ("i", "em"):
                partes.append(f"*{dentro}*" if dentro.strip() else dentro)
            elif tag == "u":
                partes.append(f"<u>{dentro}</u>")
            elif tag == "s":
                partes.append(f"<s>{dentro}</s>")
            elif tag == "code":
                crudo = "".join(h for h in (hijos or []) if isinstance(h, str))
                partes.append(f"`{crudo}`")
            elif tag == "br":
                partes.append("<br>\n")
            elif tag == "a":
                href = (n.get("attrs") or {}).get("href", "")
                href = urllib.parse.urljoin(self.base, href) if href.startswith("/") else href
                partes.append(f"[{dentro}]({href})" if href else dentro)
            elif tag == "img":
                partes.append(self.imagen(n, ""))
            else:
                partes.append(dentro)
        return "".join(partes)

    def imagen(self, nodo, leyenda: str) -> str:
        src = (nodo.get("attrs") or {}).get("src", "")
        if not src:
            return ""
        archivo = self.guardar_imagen(src)
        alternativo = re.sub(r"[\[\]\\*_`<>]", "", leyenda) or "Captura del tutorial"
        return f"![{alternativo}]({archivo})"

    # ---- bloques
    def bloques(self, nodos) -> list[str]:
        salida: list[str] = []
        for n in nodos or []:
            if isinstance(n, str):
                if n.strip():
                    salida.append(texto_seguro(n.strip()))
                continue
            tag = n.get("tag")
            hijos = n.get("children")
            if tag == "p":
                texto = self.en_linea(hijos).strip()
                if texto:
                    salida.append(texto)
            elif tag == "h3":
                salida.append("## " + self.en_linea(hijos).strip())
            elif tag == "h4":
                salida.append("### " + self.en_linea(hijos).strip())
            elif tag in ("blockquote", "aside"):
                texto = self.en_linea(hijos).strip()
                salida.append("\n".join("> " + linea for linea in texto.splitlines()))
            elif tag in ("ul", "ol"):
                renglones = []
                for i, li in enumerate([h for h in hijos or [] if isinstance(h, dict)], 1):
                    marca = f"{i}." if tag == "ol" else "-"
                    texto = self.en_linea(li.get("children")).strip().replace("\n", "\n   ")
                    renglones.append(f"{marca} {texto}")
                salida.append("\n".join(renglones))
            elif tag == "pre":
                crudo = self.texto_crudo(hijos)
                salida.append("```\n" + crudo.rstrip("\n") + "\n```")
            elif tag == "hr":
                salida.append("---")
            elif tag == "figure":
                salida.append(self.figura(hijos))
            elif tag == "img":
                salida.append(self.imagen(n, ""))
            elif tag in ("iframe", "video"):
                src = (n.get("attrs") or {}).get("src", "")
                if src:
                    src = urllib.parse.urljoin(self.base, src)
                    salida.append(f"[:material-play-circle: Ver video]({src}){{ target=_blank }}")
            else:
                texto = self.en_linea([n]).strip()
                if texto:
                    salida.append(texto)
        return [s for s in salida if s.strip()]

    def figura(self, hijos) -> str:
        imagen = next((h for h in hijos or [] if isinstance(h, dict) and h.get("tag") == "img"), None)
        video = next((h for h in hijos or [] if isinstance(h, dict) and h.get("tag") in ("iframe", "video")), None)
        pie = next((h for h in hijos or [] if isinstance(h, dict) and h.get("tag") == "figcaption"), None)
        leyenda = self.en_linea(pie.get("children")).strip() if pie else ""
        partes = []
        if imagen:
            partes.append(self.imagen(imagen, self.texto_crudo(pie.get("children")) if pie else ""))
        elif video:
            partes += self.bloques([video])
        if leyenda:
            partes.append(f"<small>{leyenda}</small>" if "\n" not in leyenda else leyenda)
        return "  \n".join(partes)

    def texto_crudo(self, nodos) -> str:
        partes = []
        for n in nodos or []:
            if isinstance(n, str):
                partes.append(n)
            elif n.get("tag") == "br":
                partes.append("\n")
            else:
                partes.append(self.texto_crudo(n.get("children")))
        return "".join(partes)


def escribir_tutorial(entrada: dict, pagina: dict, carpeta: Path, url: str) -> Conversor:
    carpeta.mkdir(parents=True, exist_ok=True)
    conv = Conversor(carpeta, base="https://telegra.ph/")
    cuerpo = conv.bloques(pagina.get("content"))

    titulo = entrada["titulo"]
    autor = entrada.get("autor") or pagina.get("author_name") or ""
    enlace_autor = pagina.get("author_url") or ""
    titulo_yaml = titulo.replace('"', '\\"')

    cabecera = ['---', f'title: "{titulo_yaml}"', '---', '',
                f'# {texto_seguro(titulo)}', '']
    datos = []
    if autor:
        datos.append(f":material-account: [{texto_seguro(autor)}]({enlace_autor}){{ target=_blank }}"
                     if enlace_autor.startswith("http") else f":material-account: {texto_seguro(autor)}")
    datos.append(f":material-link-variant: [Ver el original en Telegraph]({url}){{ target=_blank }}")
    cabecera += [' · '.join(datos), '{ .tut-datos }', '', '---', '', '']

    pie = ['', '---', '',
           '[:material-arrow-left: Volver al índice](../../alfabetico.md) · '
           '[:fontawesome-brands-telegram: Preguntar en el grupo](https://t.me/calibreconfiguraciones){ target=_blank }', '']

    (carpeta / "index.md").write_text("\n".join(cabecera) + "\n\n".join(cuerpo) + "\n" + "\n".join(pie),
                                      encoding="utf-8")
    return conv


# --------------------------------------------------------------------------- indice.yml

def actualizar_indice(cambios: dict[str, str]) -> None:
    """Reemplaza url: "telegraph" por url: "tutoriales/x/index.md", original: "telegraph".
    Se edita el texto (no se vuelve a escribir el YAML) para conservar comentarios y orden."""
    texto = INDICE.read_text(encoding="utf-8")
    for viejo, nuevo in cambios.items():
        buscado = f'url: "{viejo}"'
        if buscado not in texto:
            print(f"  ! No encontré el enlace en indice.yml: {viejo}")
            continue
        texto = texto.replace(buscado, f'url: "{nuevo}", original: "{viejo}"', 1)
    INDICE.write_text(texto, encoding="utf-8")


# --------------------------------------------------------------------------- principal

def main():
    p = argparse.ArgumentParser(description="Copia tutoriales de Telegraph al sitio, con imágenes.")
    p.add_argument("--simular", action="store_true", help="mostrar qué haría, sin descargar ni cambiar nada")
    p.add_argument("--solo-mios", action="store_true", help="copiar solo los tutoriales propios")
    p.add_argument("--autor", action="append", default=[], help="copiar solo los de este autor (se puede repetir)")
    p.add_argument("--url", action="append", default=[], help="copiar solo este tutorial (se puede repetir)")
    args = p.parse_args()

    autores = {a.lower().lstrip("@") for a in args.autor}
    entradas = yaml.safe_load(INDICE.read_text(encoding="utf-8")) or []
    pendientes = [e for e in entradas
                  if "telegra.ph/" in (e.get("url") or "")
                  and (not args.url or e["url"] in args.url)]

    print(f"Tutoriales de Telegraph sin copiar: {len(pendientes)}\n")
    cambios, ajenos, errores = {}, [], []

    for n, entrada in enumerate(pendientes, 1):
        url = entrada["url"]
        print(f"[{n}/{len(pendientes)}] {entrada['titulo']}")
        try:
            pagina = leer_pagina(url)
        except RuntimeError as e:
            print(f"  ✗ {e}")
            errores.append((entrada["titulo"], str(e)))
            continue

        if args.solo_mios or autores:
            permitido = (args.solo_mios and es_mio(pagina)) or autor_coincide(pagina, entrada, autores)
        else:
            permitido = True
        if not permitido:
            quien = pagina.get("author_name") or entrada.get("autor") or "sin autor"
            print(f"  · Salteado: es de {quien}")
            ajenos.append((entrada["titulo"], quien, pagina.get("author_url") or ""))
            continue

        carpeta = DESTINO / nombre_carpeta(url)
        if args.simular:
            print(f"  → Se copiaría en docs/tutoriales/{carpeta.name}/")
            continue

        conv = escribir_tutorial(entrada, pagina, carpeta, url)
        cambios[url] = f"tutoriales/{carpeta.name}/index.md"
        actualizar_indice({url: cambios[url]})  # se guarda enseguida, por si se corta
        print(f"  ✓ Copiado ({conv.imagenes} imágenes)")
        for aviso in conv.avisos:
            print(f"  ! {aviso}")
        time.sleep(0.4)  # para no saturar a Telegraph


    print("\n================ Resumen ================")
    print(f"Copiados: {len(cambios)}" + ("  (simulación: no se copió nada)" if args.simular else ""))
    if errores:
        print(f"Con error: {len(errores)}")
        for t, e in errores:
            print(f"  - {t}: {e}")
    if ajenos:
        print(f"\nSalteados por el filtro de autor: {len(ajenos)}")
        for t, quien, enlace in ajenos:
            print(f"  - {t}  ·  {quien} {enlace}")
    if cambios:
        print("\nSe actualizó datos/indice.yml. Subí a GitHub:")
        print("  - la carpeta docs/tutoriales (completa)")
        print("  - el archivo datos/indice.yml")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nInterrumpido. Podés volver a correrlo: lo ya copiado se saltea.")
