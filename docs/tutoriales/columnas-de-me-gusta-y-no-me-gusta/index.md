---
title: "Columna personalizada - Me gusta / No me gusta"
licencia: cc-by-sa
---

# Columna personalizada - Me gusta / No me gusta

:material-account: [Walter](https://t.me/Dunhill69){ target=_blank } · :material-link-variant: [Ver el original en Telegraph](https://telegra.ph/Columnas-de-me-gusta-y-no-me-gusta-07-09){ target=_blank }
{ .tut-datos }

---

Explicado por @janes\_morris

Primer método:

![Captura del tutorial](imagen01.png)

1) Primero como siempre creamos dos columnas personalizadas

![Captura del tutorial](imagen02.png)

1.a) Me gusta

![Captura del tutorial](imagen03.png)

1.b) No me gusta

2) Luego nos vamos a las reglas que tienen que estar ordenadas de arriba o de abajo así exactamente, la de me gusta da igual, pero la de no me gusta si no se le ponen esas dos reglas ordenadas así no sale.

![Captura del tutorial](imagen04.png)

3) Me gusta

Idéntico a esto

![Captura del tutorial](imagen05.png)

4) Sin valorar pero relacionada con no me gusta, idéntico a esto:

![Captura del tutorial](imagen06.png)

5) No me gusta, idéntico a esto:

![Captura del tutorial](imagen07.png)

Iconos empleados: [https://t.me/calibreconfiguraciones/112333/139539](https://t.me/calibreconfiguraciones/112333/139539)

<br>

Ir al mensaje: [https://t.me/calibreconfiguraciones/112333/139531](https://t.me/calibreconfiguraciones/112333/139531)

Segundo método:

![Captura del tutorial](imagen08.png)

![Captura del tutorial](imagen09.png)

![Captura del tutorial](imagen10.png)

![Captura del tutorial](imagen11.png)

Icono sin clasificar: [https://t.me/calibreconfiguraciones/112333/139647](https://t.me/calibreconfiguraciones/112333/139647)

![Captura del tutorial](imagen12.png)

![Captura del tutorial](imagen13.png)

Ir al mensaje: [https://t.me/calibreconfiguraciones/112333/139642](https://t.me/calibreconfiguraciones/112333/139642)

Por medio de una regla avanzada para versión de calibre 6,22

![Captura del tutorial](imagen14.jpg)

![Captura del tutorial](imagen15.jpg)

program:

r = $rating;

switch\_if(

r == '', 'sin calificar -1.png',

r \<=# 3, 'no me gusta -1.png',

'me gusta -1.png')

Usando los iconos compartidos por @jane\_morris

<br>

Ir al mensaje: [https://t.me/calibreconfiguraciones/112333/140243](https://t.me/calibreconfiguraciones/112333/140243)

Variaciones de @virus75

Si eliminamos el ícono para "sin calificar -1.png" de la regla, cuando no se clasifica, simplemente deja el espacio vacío.

![Captura del tutorial](imagen16.jpg)

program:

r = $rating;

switch\_if(

r == '', '',

r \<=# 3, 'no me gusta - 1.png',

'me gusta -1.png')

Para calibre 6,22

Ir al mensaje: [https://t.me/calibreconfiguraciones/112333/140440](https://t.me/calibreconfiguraciones/112333/140440)

También probé con las reglas de jane morris pero, eliminé la segunda regla y a la tercera regla le añadí una condición extra, para que no tenga en cuenta la opción de valoración "Sin calificar" Esta prueba la hice sobre la columna "Me gusta 2"

![Captura del tutorial](imagen17.jpg)

![Captura del tutorial](imagen18.jpg)

![Captura del tutorial](imagen19.jpg)

![Captura del tutorial](imagen20.jpg)

Ir al mensaje: [https://t.me/calibreconfiguraciones/112333/140445](https://t.me/calibreconfiguraciones/112333/140445)

<br>

Tercer método:

![Captura del tutorial](imagen21.png)

![Captura del tutorial](imagen22.png)

![Captura del tutorial](imagen23.png)

![Captura del tutorial](imagen24.png)

![Captura del tutorial](imagen25.png)

![Captura del tutorial](imagen26.png)

Ir al mensaje: [https://t.me/calibreconfiguraciones/112333/140172](https://t.me/calibreconfiguraciones/112333/140172)

## [Volver al inicio](https://telegra.ph/Indice-Calibre-en-Espa%C3%B1ol-10-03)

<br>

<br>

---

[:material-arrow-left: Volver al índice](../../alfabetico.md) · [:fontawesome-brands-telegram: Preguntar en el grupo](https://t.me/calibreconfiguraciones){ target=_blank }
