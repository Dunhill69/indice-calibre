#!/usr/bin/env python3
"""Marca la licencia de cada tutorial copiado en docs/tutoriales/.

Agrega al encabezado de cada index.md la línea  licencia: cc-by-sa  o  licencia: autorizacion
  - cc-by-sa:     tutoriales propios (autor Walter / Dunhill69) y los enviados por el formulario
  - autorizacion: tutoriales de otros autores copiados de Telegraph (publicados con su autorización)

Se puede correr las veces que haga falta; no cambia los que ya tienen licencia.
Para cambiar uno a mano, editá la línea "licencia:" de su index.md.

Uso:  /usr/bin/python3 scripts/marcar_licencias.py
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MIOS = ("dunhill69", "dunhill", "walter")

cuenta = {"cc-by-sa": 0, "autorizacion": 0, "ya tenía": 0}
for archivo in sorted((RAIZ / "docs" / "tutoriales").glob("*/index.md")):
    texto = archivo.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    if not m:
        continue
    if re.search(r"^licencia:", m.group(1), re.M):
        cuenta["ya tenía"] += 1
        continue
    autor = re.search(r":material-account: \[?([^\]\n]*)\]?(?:\(([^)]*)\))?", texto)
    copiado_de_telegraph = "Ver el original en Telegraph" in texto
    if not copiado_de_telegraph:
        licencia = "cc-by-sa"  # enviado por el formulario (aceptó la licencia)
    elif not autor:
        licencia = "cc-by-sa"  # sin autor indicado: tutorial propio
    else:
        quien = " ".join(filter(None, autor.groups())).lower()
        licencia = "cc-by-sa" if any(n in quien for n in MIOS) else "autorizacion"
    nuevo = f"---\n{m.group(1)}\nlicencia: {licencia}\n---\n" + texto[m.end():]
    archivo.write_text(nuevo, encoding="utf-8")
    cuenta[licencia] += 1

print(f"Propios / formulario (CC BY-SA): {cuenta['cc-by-sa']}")
print(f"De otros autores (con autorización): {cuenta['autorizacion']}")
print(f"Ya marcados antes: {cuenta['ya tenía']}")
