# Notas de mantenimiento

Notas para quien administra el índice. Para visitantes, ver el [README](README.md).

**Sitio:** https://dunhill69.github.io/indice-calibre/

## Flujo de trabajo habitual

1. Trabajar siempre en la carpeta clonada por GitHub Desktop (`~/Documentos/GitHub/indice-calibre`).
2. Hacer los cambios (o correr los scripts).
3. En GitHub Desktop: escribir un resumen → **Commit to main** → **Push origin**.
4. El sitio se publica solo en uno o dos minutos (pestaña **Actions**). Si no se ve el cambio, recargar con Ctrl+Shift+R.

> En esta compu, los scripts se corren con `/usr/bin/python3` (el `python3` de Miniforge no tiene PyYAML).

## Cómo está armado

| Carpeta / archivo | Para qué sirve |
|---|---|
| `datos/indice.yml` | **La lista de tutoriales.** Es el único archivo que hay que tocar para agregar o corregir uno. |
| `datos/temas.yml` | Los temas (categorías) y sus íconos. |
| `docs/colaborar.md` | Página "Cómo colaborar". |
| `scripts/plantilla_inicio.md` | Texto de la página de inicio. |
| `scripts/importar_telegraph.py` | Copia tutoriales de Telegraph al sitio, con imágenes (ver abajo). |
| `docs/tutoriales/` | Tutoriales copiados al sitio, cada uno en su carpeta con sus imágenes. |
| `scripts/generar.py` | Arma las páginas del índice (A–Z y por tema) a partir de los datos. |
| `mkdocs.yml` | Configuración del sitio: nombre, colores, menú, idiomas del traductor. |
| `.github/workflows/publicar.yml` | Publica el sitio solo cada vez que se sube un cambio. |

## Tutoriales enviados por el formulario

1. Alguien completa el formulario **Nuevo tutorial** (pestaña Issues).
2. Si está bien, ponele la etiqueta **`aprobado`**.
3. La automatización crea la página con sus imágenes, la suma al índice, publica el sitio
   y le avisa al autor. Si algo falla, deja un comentario en el issue.

## Agregar un tutorial a mano

Agregá una línea en `datos/indice.yml` (en cualquier lugar, se ordena solo):

```yaml
- {titulo: "Nombre del tutorial", url: "https://telegra.ph/...", autor: "@usuario", temas: [apariencia]}
```

Al guardar el cambio en GitHub, el sitio se actualiza en uno o dos minutos.
Si algo está mal (un tema que no existe, un enlace repetido), la publicación falla y en la pestaña
**Actions** se ve el motivo en español.

## Copiar tutoriales de Telegraph al sitio

Todos los tutoriales del índice cuentan con la aprobación de sus autores, así que se copian todos.
Cada copia conserva el nombre del autor y el enlace al original.

```bash
/usr/bin/python3 scripts/importar_telegraph.py --simular   # ver qué haría
/usr/bin/python3 scripts/importar_telegraph.py    # copiar todos
```

Después: Commit y Push desde GitHub Desktop.

## Vista previa en tu computadora (opcional)

```bash
pip install -r requirements.txt
python3 scripts/generar.py
mkdocs serve
```

Y abrí http://127.0.0.1:8000 en el navegador.
