# Índice Calibre en Español

Índice de tutoriales de Calibre escritos por los miembros del grupo de Telegram
[Calibre en Español](https://t.me/calibreconfiguraciones).

**Sitio:** https://dunhill69.github.io/indice-calibre/

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
python3 scripts/importar_telegraph.py --simular   # ver qué haría
python3 scripts/importar_telegraph.py             # copiar todos
```

Después hay que subir a GitHub la carpeta `docs/tutoriales` y el archivo `datos/indice.yml`.
Cada copia mantiene el enlace al original en Telegraph.

## Vista previa en tu computadora (opcional)

```bash
pip install -r requirements.txt
python3 scripts/generar.py
mkdocs serve
```

Y abrí http://127.0.0.1:8000 en el navegador.

## Licencia

Cada tutorial pertenece a su autor. Salvo indicación contraria, el contenido se comparte bajo
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.es).
