---
title: "Ver el estado de lectura de tu Kindle"
---

# Ver el estado de lectura de tu Kindle

:material-account: [Walter](https://t.me/Dunhill69){ target=_blank } · :material-link-variant: [Ver el original en Telegraph](https://telegra.ph/Ver-el-estado-de-lectura-de-tu-Kindle-07-25){ target=_blank }
{ .tut-datos }

---

¿Tienes un Kindle?

¿Alguna vez quisiste que Calibre mostrara el "Estado de lectura" de tus libros en una columna?

¿Automágicamente?

Entonces lo siguiente también podría ser para ti.

Debe ejecutar Calibre 0.7.40 o más reciente para usar esto.

También debe utilizar "Obtener anotaciones" de su Kindle. (Complemento Annotations, creo)

El siguiente ejemplo se basa en los siguientes requisitos de Kindler:

"Lo que quiero es una columna personalizada para mostrar la fecha de" Última apertura "si la última ubicación leyó\> 95%.

Si el libro muestra\> 0% pero \<95%, quiero el columna para mostrar "Leyendo"

Y si el libro está al 0% o sin abrir,

<br>

Cómo "Obtener anotaciones" de su Kindle:

Inicie Calibre,

conecte su Kindle, espere un poco,

haga clic en la flecha a la derecha del icono "Enviar al dispositivo", seleccione

"Obtener anotaciones"

y el "Estado del libro" del Kindle es agregado a los detalles del libro Calibre, en los comentarios.

<br>

Debe obtener anotaciones nuevas cada vez que conecte su Kindle para obtener información actualizada.

Este es solo un ejemplo de lo que podría obtener con mi K3:

<br>

25-12-2010

Última página leída: Ubicación 7365 (68%)

Ubicación 4603 • Marcar la

ubicación 4942 • Marcar la

ubicación 4980 • Marcar la

ubicación 5984 • Marcar la

ubicación 7363 • Marcar la ubicación

<br>

La forma mejor / más rápida, pero la más difícil, de obtener la información necesaria en una columna personalizada, es utilizar las funciones de plantilla de Python.

Suena aterrador, pero no se preocupe. Copiar / pegar es su ayuda.

<br>

Simplemente haga lo siguiente:

<br>

1) vaya a Preferencias -\> Avanzado -\> Funciones de plantilla.

2) en el cuadro Función escriba: kindle\_read\_status\_2

3) en el cuadro Recuento de argumentos escriba: 4

4) en el cuadro Documentación, pegue lo siguiente:

```
Check if the associated field contains a kindle annotation for percent read. 
If not, return no_page_read_str. 
If so, then compare that percent against is_read_pct. 
If the val is larger, then return is_read_str, 
if the val is >0 and < is_read_pct return is_reading_str. 
Otherwise return is_not_read_str. 

One usage: {comments:kindle_read_status(90,Read,Reading,Not Read)} 

( use the above when defining your custom column ) 

90 goes into variable is_read_pct. IF pct_read > 90 the book is "read" The text returned is
Read goes into the variable is_read_str. This ex. returns the text Read
Reading goes into variable is_reading_str. IF pct_read >0 book the text "Reading" is shown with the percentage shown as well.
Not Read goes into variable no_page_read_str. IF none of the above catch, then "Not Read" is shown.

Feel free to change the %, the text strings to suit your needs. 
Remember: Do this in the custom column definition.
```

5) En el cuadro Código de programa, pegue lo siguiente:

<br>

```
def evaluate(self, formatter, kwargs, mi, locals, val, is_read_pct, is_read_str,
                                is_reading_str, no_page_read_str):
        try:
                test_val = int(is_read_pct)
        except:
                return 'is_read_pct is not a number'

        import re
        mg = re.match('.*\s(\d+[-/]\d+[-/]\d+).*?Last Page Read: Location \d+ \((\d+)%\)', val, re.I + re.DOTALL);
        if mg is None:
                return no_page_read_str
        date = mg.group(1)
        pct = mg.group(2)
        try:
                f = int(pct)
                if f > test_val:
                        return is_read_str
                elif f > 0:
                        return is_reading_str + ': ' + pct + '%'
        except:
                pass
        return no_page_read_str
```

6) presione el botón Crear, luego el botón Aplicar.

7) Aún en Preferencias, elija Agregar sus propias columnas

8) Elija Agregar barra de columna personalizada en la parte inferior

9) ingrese lo siguiente en su columna personalizada:

Nombre de búsqueda: read\_status2

Encabezado de columna: Leer estado2

Tipo de columna: Columna construida a partir de otras columnas

Plantilla:

{comments:kindle\_read\_status\_2(90,Leído,Leyendo,No Leído)}

```
10) Elija Aplicar

11) Haga clic en Aceptar para la advertencia de reinicio

12) Apague Calibre

13) Inicie Calibre

Si siguió las instrucciones minuciosamente, debería tener una nueva columna que muestre el "Estado de lectura" de sus libros.
```

<br>

Fuente: [https://www.mobileread.com/forums/showpost.php?p=1353631&postcount=137](https://www.mobileread.com/forums/showpost.php?p=1353631&postcount=137)

Modificación [https://www.mobileread.com/forums/showpost.php?p=1361924&postcount=172](https://www.mobileread.com/forums/showpost.php?p=1361924&postcount=172)

<br>

<br>

## [Volver al inicio](https://telegra.ph/Indice-Calibre-en-Espa%C3%B1ol-10-03)

<br>

<br>

---

[:material-arrow-left: Volver al índice](../../alfabetico.md) · [:fontawesome-brands-telegram: Preguntar en el grupo](https://t.me/calibreconfiguraciones){ target=_blank }
