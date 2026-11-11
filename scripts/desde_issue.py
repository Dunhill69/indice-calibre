#!/usr/bin/env python3
"""Convierte un formulario "Nuevo tutorial" (issue de GitHub) en un tutorial del sitio.

Lo ejecuta la automatización .github/workflows/tutorial-aprobado.yml cuando un
administrador pone la etiqueta "aprobado" en el issue. Lee los datos de variables
de entorno (nunca se ejecutan como código):

    ISSUE_BODY    texto del formulario
    ISSUE_NUMBER  número del issue
    ISSUE_USER    usuario de GitHub que lo envió

Crea docs/tutoriales/<nombre>/index.md con sus imágenes y agrega la línea en
datos/indice.yml. Escribe en la salida la ruta creada (para el comentario final).
"""
from __future__ import annotations

import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
INDICE = RAIZ / "datos" / "indice.yml"
TEMAS = RAIZ / "datos" / "temas.yml"
DESTINO = RAIZ / "docs" / "tutoriales"

IDIOMAS = {"Español": "es", "English": "en", "Português": "pt", "Français": "fr",
           "Italiano": "it", "Deutsch": "de", "Català": "ca"}

# Solo se descargan imágenes subidas a GitHub (las que se pegan en el formulario).
HOSTS_IMAGENES = ("github.com", "user-images.githubusercontent.com",
                  "private-user-images.githubusercontent.com", "githubusercontent.com")
MAX_IMAGEN = 10 * 1024 * 1024  # 10 MB


def error(mensaje: str):
    print(f"ERROR: {mensaje}", file=sys.stderr)
    sys.exit(1)


# --------------------------------------------------------------------------- formulario

def leer_campos(cuerpo: str) -> dict[str, str]:
    """El formulario llega como '### Etiqueta\\n\\nrespuesta' por cada campo."""
    campos = {}
    partes = re.split(r"^### (.+?)\s*$", cuerpo.replace("\r\n", "\n"), flags=re.M)
    for i in range(1, len(partes) - 1, 2):
        etiqueta = partes[i].strip().lower()
        valor = partes[i + 1].strip()
        if valor == "_No response_":
            valor = ""
        campos[etiqueta] = valor
    return campos


def campo(campos: dict, comienzo: str) -> str:
    for etiqueta, valor in campos.items():
        if etiqueta.startswith(comienzo):
            return valor
    return ""


# --------------------------------------------------------------------------- utilidades

def nombre_carpeta(titulo: str) -> str:
    t = unicodedata.normalize("NFD", titulo.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:70].strip("-")
    base = t or "tutorial"
    nombre, n = base, 2
    while (DESTINO / nombre).exists():
        nombre, n = f"{base}-{n}", n + 1
    return nombre


def host_permitido(url: str) -> bool:
    host = urllib.parse.urlparse(url).hostname or ""
    return url.startswith("https://") and any(host == h or host.endswith("." + h) for h in HOSTS_IMAGENES)


def bajar_imagen(url: str, carpeta: Path, numero: int) -> str | None:
    pedido = urllib.request.Request(url, headers={"User-Agent": "IndiceCalibreEnEspanol/1.0"})
    try:
        with urllib.request.urlopen(pedido, timeout=60) as r:
            tipo = (r.headers.get("Content-Type") or "").split(";")[0].strip()
            datos = r.read(MAX_IMAGEN + 1)
    except Exception as e:  # noqa: BLE001
        print(f"Aviso: no se pudo bajar {url}: {e}", file=sys.stderr)
        return None
    if len(datos) > MAX_IMAGEN or not tipo.startswith("image/"):
        print(f"Aviso: se omitió {url} (no es imagen o pesa más de 10 MB)", file=sys.stderr)
        return None
    extension = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif",
                 "image/webp": ".webp"}.get(tipo, ".png")
    nombre = f"imagen{numero:02d}{extension}"
    (carpeta / nombre).write_bytes(datos)
    return nombre


def localizar_imagenes(texto: str, carpeta: Path) -> tuple[str, int]:
    """Baja las imágenes pegadas en el formulario y cambia los enlaces por archivos locales."""
    contador = 0
    cache: dict[str, str] = {}

    def reemplazar(url: str) -> str:
        nonlocal contador
        if not host_permitido(url):
            return url
        if url not in cache:
            local = bajar_imagen(url, carpeta, contador + 1)
            if local:
                contador += 1
            cache[url] = local or url
        return cache[url]

    def markdown_img(m):
        alt, url = m.group(1) or "Captura del tutorial", m.group(2)
        if not host_permitido(url):  # imágenes de otros sitios: solo como enlace
            return f"[Imagen externa: {alt}]({url})"
        return f"![{alt}]({reemplazar(url)})"
    # ![texto](url)
    texto = re.sub(r"!\[([^\]]*)\]\((\S+?)\)", markdown_img, texto)
    # <img ... src="url" ...>
    def img_html(m):
        alt = re.search(r'alt="([^"]*)"', m.group(0))
        alt = (alt.group(1) if alt else "") or "Captura del tutorial"
        if not host_permitido(m.group(1)):
            return f"[Imagen externa: {alt}]({m.group(1)})"
        return f"![{alt}]({reemplazar(m.group(1))})"
    texto = re.sub(r'<img\b[^>]*?\bsrc="([^"]+)"[^>]*>', img_html, texto)
    return texto, contador


def limpiar_html(texto: str) -> str:
    """Quita HTML peligroso (scripts, marcos, estilos y atributos on...=)."""
    texto = re.sub(r"<(script|style|iframe|object|embed|form)\b.*?</\1\s*>", "", texto, flags=re.S | re.I)
    texto = re.sub(r"<(script|style|iframe|object|embed|form|meta|link)\b[^>]*>", "", texto, flags=re.I)
    texto = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)", "", texto, flags=re.I)
    texto = re.sub(r"javascript:", "", texto, flags=re.I)
    return texto


# --------------------------------------------------------------------------- principal

def main():
    cuerpo = os.environ.get("ISSUE_BODY", "")
    numero = os.environ.get("ISSUE_NUMBER", "")
    usuario = os.environ.get("ISSUE_USER", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "Dunhill69/indice-calibre")
    if not cuerpo:
        error("el issue no tiene contenido.")

    campos = leer_campos(cuerpo)
    titulo = re.sub(r"<[^>]*>", "", campo(campos, "título del tutorial"))
    titulo = re.sub(r"[<>\[\]`*_#]", "", titulo).replace("\n", " ").strip()
    idioma_txt = campo(campos, "idioma")
    temas_txt = campo(campos, "tema")
    autor = campo(campos, "nombre a mostrar") or (f"@{usuario}" if usuario else "")
    contenido = limpiar_html(campo(campos, "contenido"))

    if not titulo:
        error("falta el título.")
    if not contenido:
        error("falta el contenido.")

    temas_def = yaml.safe_load(TEMAS.read_text(encoding="utf-8"))
    temas = [clave for clave, info in temas_def.items() if info["nombre"] in temas_txt]
    if not temas:
        error(f"no se reconoció ningún tema en «{temas_txt}».")
    idioma = IDIOMAS.get(idioma_txt, "otro")

    carpeta_nombre = nombre_carpeta(titulo)
    carpeta = DESTINO / carpeta_nombre
    carpeta.mkdir(parents=True)
    contenido, imagenes = localizar_imagenes(contenido, carpeta)

    issue_url = f"https://github.com/{repo}/issues/{numero}" if numero else ""
    autor_md = autor.replace("[", "").replace("]", "")
    if usuario:
        autor_md = f"[{autor_md}](https://github.com/{usuario}){{ target=_blank }}"
    datos = [f":material-account: {autor_md}"]
    if issue_url:
        datos.append(f":material-github: [Propuesta original #{numero}]({issue_url}){{ target=_blank }}")
    titulo_yaml = titulo.replace("\\", "\\\\").replace('"', '\\"')

    pagina = "\n".join([
        "---", f'title: "{titulo_yaml}"', "licencia: cc-by-sa", "---", "",
        f"# {titulo}", "",
        " · ".join(datos), "{ .tut-datos }", "", "---", "",
        contenido.strip(), "", "---", "",
        "[:material-arrow-left: Volver al índice](../../alfabetico.md)", "",
    ])
    (carpeta / "index.md").write_text(pagina, encoding="utf-8")

    linea = {"titulo": titulo, "url": f"tutoriales/{carpeta_nombre}/index.md",
             "autor": autor, "temas": temas}
    if idioma != "es":
        linea["idioma"] = idioma
    texto_linea = "- " + yaml.safe_dump(linea, allow_unicode=True, default_flow_style=True,
                                         sort_keys=False, width=10_000).strip()
    with INDICE.open("a", encoding="utf-8") as f:
        f.write(("" if INDICE.read_text(encoding="utf-8").endswith("\n") else "\n") + texto_linea + "\n")

    print(f"tutoriales/{carpeta_nombre}/")
    print(f"Tutorial creado con {imagenes} imágenes.", file=sys.stderr)


if __name__ == "__main__":
    main()
