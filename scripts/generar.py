#!/usr/bin/env python3
"""Genera las páginas del índice a partir de datos/indice.yml y datos/temas.yml.

Uso (desde la carpeta del proyecto):
    python3 scripts/generar.py

Crea o reemplaza:
    docs/index.md          (a partir de scripts/plantilla_inicio.md)
    docs/alfabetico.md     (índice de la A a la Z)
    docs/temas/index.md    (tarjetas con todos los temas)
    docs/temas/<tema>.md   (una página por tema)

No edites esas páginas a mano: se pisan cada vez que corre el script.
"""
from __future__ import annotations

import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "datos"
DOCS = RAIZ / "docs"

AVISO = "<!-- Página generada por scripts/generar.py. No la edites a mano: edita datos/indice.yml -->\n"


# --------------------------------------------------------------------------- utilidades

def clave_orden(texto: str) -> str:
    """Orden alfabético en español: ignora tildes y signos iniciales, la Ñ va después de la N."""
    t = texto.lower().lstrip("¿¡«\"'(").replace("ñ", "n~")
    t = unicodedata.normalize("NFD", t)
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def letra_de(titulo: str) -> str:
    primera = titulo.lstrip("¿¡«\"'(")[:1].upper()
    if primera == "Ñ":
        return "Ñ"
    primera = unicodedata.normalize("NFD", primera)[:1]
    return primera if primera.isalpha() else "#"


def ancla_letra(letra: str) -> str:
    return {"Ñ": "letra-nn", "#": "letra-otros"}.get(letra, f"letra-{letra.lower()}")


def escapar(texto: str) -> str:
    """Evita que Markdown o HTML interpreten caracteres del título."""
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for c in "\\[]*_":
        texto = texto.replace(c, "\\" + c)
    return texto


def origen(url: str) -> str:
    if "telegra.ph" in url:
        return "Telegraph"
    if "teletype.in" in url:
        return "Teletype"
    if url.startswith(("http://", "https://")):
        return url.split("/")[2]
    return "En este sitio"


def renglon(t: dict) -> str:
    titulo = escapar(t["titulo"])
    if t.get("url"):
        url = t["url"]
        externo = url.startswith(("http://", "https://"))
        destino = "{ target=_blank rel=noopener }" if externo else ""
        partes = [f"[{titulo}]({url}){destino}"]
    else:
        partes = [f'<span class="tut-sin-enlace">{titulo}</span>']
    if t.get("autor"):
        partes.append(f'<span class="tut-autor">por {escapar(t["autor"])}</span>')
    if t.get("nota"):
        partes.append(f'<span class="tut-nota">{escapar(t["nota"])}</span>')
    if t.get("url"):
        partes.append(f'<span class="tut-origen">{origen(t["url"])}</span>')
    return "- " + " ".join(partes)


# --------------------------------------------------------------------------- carga y validación

def cargar():
    temas = yaml.safe_load((DATOS / "temas.yml").read_text(encoding="utf-8"))
    tutoriales = yaml.safe_load((DATOS / "indice.yml").read_text(encoding="utf-8")) or []

    errores = []
    vistos_url = {}
    for i, t in enumerate(tutoriales, 1):
        nombre = t.get("titulo") or f"(entrada {i} sin título)"
        if not t.get("titulo"):
            errores.append(f"Entrada {i}: falta el título.")
        if not t.get("temas"):
            errores.append(f"«{nombre}»: falta indicar al menos un tema.")
        for tema in t.get("temas", []):
            if tema not in temas:
                errores.append(f"«{nombre}»: el tema «{tema}» no existe en datos/temas.yml.")
        url = t.get("url")
        if url:
            if url in vistos_url:
                errores.append(f"«{nombre}»: el enlace está repetido (también en «{vistos_url[url]}»).")
            vistos_url[url] = nombre

    if errores:
        print("Hay problemas en datos/indice.yml:\n  - " + "\n  - ".join(errores), file=sys.stderr)
        sys.exit(1)

    tutoriales.sort(key=lambda t: clave_orden(t["titulo"]))
    return temas, tutoriales


# --------------------------------------------------------------------------- páginas

def pagina_alfabetica(tutoriales) -> str:
    por_letra = defaultdict(list)
    for t in tutoriales:
        por_letra[letra_de(t["titulo"])].append(t)
    letras = sorted(por_letra, key=clave_orden)

    salida = ["---", "title: Índice de la A a la Z", "---", AVISO,
              "# Índice de la A a la Z", "",
              f"{len(tutoriales)} tutoriales ordenados alfabéticamente. "
              "Escribí en el filtro para encontrar un tutorial al instante, o tocá una letra para saltar a ella.", ""]
    salida += ['<input type="search" id="tut-filtro" class="tut-filtro" '
               'placeholder="Filtrar: escribí parte del título o el autor…" autocomplete="off">',
               '<p id="tut-filtro-info" class="tut-filtro-info"></p>', ""]
    saltos = " ".join(f'<a href="#{ancla_letra(l)}">{l}</a>' for l in letras)
    salida += [f'<nav class="tut-letras">{saltos}</nav>', ""]
    for letra in letras:
        salida += [f"## {letra} {{ #{ancla_letra(letra)} }}", ""]
        salida += [renglon(t) for t in por_letra[letra]]
        salida.append("")
    return "\n".join(salida)


def paginas_temas(temas, tutoriales) -> dict[str, str]:
    por_tema = defaultdict(list)
    for t in tutoriales:
        for tema in t["temas"]:
            por_tema[tema].append(t)

    paginas = {}
    tarjetas = []
    for clave, info in temas.items():
        lista = por_tema.get(clave, [])
        icono = ":" + info["icono"].replace("/", "-") + ":"
        cuantos = f"{len(lista)} tutorial" + ("" if len(lista) == 1 else "es")
        tarjetas += [f"-   {icono}{{ .lg .middle }} **[{info['nombre']}]({clave}.md)**", "",
                     "    ---", "", f"    {cuantos}", ""]

        cuerpo = ["---", f"title: {info['nombre']}", "---", AVISO,
                  f"# {icono} {info['nombre']}", "", f"{cuantos} sobre este tema.", ""]
        cuerpo += [renglon(t) for t in lista] or ["*Todavía no hay tutoriales en este tema.*"]
        cuerpo += ["", "[:material-arrow-left: Todos los temas](index.md)", ""]
        paginas[f"{clave}.md"] = "\n".join(cuerpo)

    paginas["index.md"] = "\n".join(
        ["---", "title: Por tema", "---", AVISO, "# Tutoriales por tema", "",
         "Cada tutorial puede aparecer en más de un tema.", "",
         '<div class="grid cards" markdown>', ""] + tarjetas + ["</div>", ""])
    return paginas


def pagina_inicio(temas, tutoriales) -> str:
    plantilla = (RAIZ / "scripts" / "plantilla_inicio.md").read_text(encoding="utf-8")
    autores = {t["autor"] for t in tutoriales if t.get("autor")}
    return plantilla.format(
        total=len(tutoriales),
        temas=len(temas),
        autores=len(autores) + 1,  # +1 por los tutoriales sin autor indicado (Walter)
    )


def main():
    temas, tutoriales = cargar()
    (DOCS / "temas").mkdir(parents=True, exist_ok=True)

    (DOCS / "index.md").write_text(pagina_inicio(temas, tutoriales), encoding="utf-8")
    (DOCS / "alfabetico.md").write_text(pagina_alfabetica(tutoriales), encoding="utf-8")
    for nombre, contenido in paginas_temas(temas, tutoriales).items():
        (DOCS / "temas" / nombre).write_text(contenido, encoding="utf-8")

    print(f"Listo: {len(tutoriales)} tutoriales en {len(temas)} temas.")


if __name__ == "__main__":
    main()
