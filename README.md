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
| `scripts/generar.py` | Arma las páginas del índice (A–Z y por tema) a partir de los datos. |
| `mkdocs.yml` | Configuración del sitio: nombre, colores, menú, idiomas del traductor. |
| `.github/workflows/publicar.yml` | Publica el sitio solo cada vez que se sube un cambio. |

## Agregar un tutorial

Agregá una línea en `datos/indice.yml` (en cualquier lugar, se ordena solo):

```yaml
- {titulo: "Nombre del tutorial", url: "https://telegra.ph/...", autor: "@usuario", temas: [apariencia]}
```

Al guardar el cambio en GitHub, el sitio se actualiza en uno o dos minutos.
Si algo está mal (un tema que no existe, un enlace repetido), la publicación falla y en la pestaña
**Actions** se ve el motivo en español.

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
