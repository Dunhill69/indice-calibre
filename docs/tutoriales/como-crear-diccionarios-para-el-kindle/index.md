---
title: "Kindle - crear diccionarios"
licencia: cc-by-sa
---

# Kindle - crear diccionarios

:material-account: [Walter Paterno](https://t.me/Dunhill69){ target=_blank } · :material-link-variant: [Ver el original en Telegraph](https://telegra.ph/Como-crear-diccionarios-para-el-kindle-01-31){ target=_blank }
{ .tut-datos }

---

## Introducción a diccionarios

Un diccionario es un eBook Kindle (archivo MOBI) con etiquetas adicionales añadidas para permitir funciones de búsqueda y localización. Diccionarios eBooks:

- Contienen un índice principal: una lista de palabras o enunciados organizados por orden alfabético. Los lectores pueden buscar rápidamente en esta lista con solo escribir el principio de la palabra y seleccionar la entrada deseada.
- Están marcados como diccionarios. Los idiomas de origen y destino del diccionario deben estar definidos correctamente para que los dispositivos Kindle puedan utilizar el diccionario en búsquedas en el libro.

Por ejemplo, un diccionario de inglés (monolingüe) establece el inglés como el idioma de origen y de destino. Un diccionario de español-inglés establece el español como idioma de origen y el inglés como idioma de destino. Para crear un diccionario bidireccional y bilingüe, como de español-francés y francés-español, debe crear dos eBooks diferentes: uno para español-francés y otro para francés-español.

Un diccionario Kindle debe tener los mismos componentes que un eBook Kindle normal. Tiene que contener un archivo OPF y archivos HTML con CSS. Todos los diccionarios deben tener:

- Una imagen de portada
- Una página de derechos de autor
- Cualquier material inicial o las páginas finales relevantes (explicaciones de símbolos, apéndices, etc.)
- Definiciones de palabras (este es contenido principal del archivo)

Este formato no admite actualmente la tipografía mejorada.

<br>

## Pautas de metadatos

El archivo OPF de un diccionario es similar al de otros libros Kindle, excepto porque contiene etiquetas de metadatos especializadas en la sección \<x-metadata\>. Estas etiquetas extras del archivo OPF establecen el idioma de origen y el idioma de destino del diccionario. Si el diccionario tiene varios índices, el archivo OPF también especifica el nombre del índice de búsqueda primario.

- El elemento \<DictionaryInLanguage\> contiene el código de lenguaje ISO 639-1 del idioma de origen de un diccionario bilingüe. Es decir, para un diccionario español-francés, el idioma de origen es el español.
- El elemento \<DictionaryOutLanguage\> contiene el código de lenguaje ISO 639-1 del idioma destino de un diccionario bilingüe. Es decir, para un diccionario español-francés, el idioma de destino es el francés.
- El elemento \<DefaultLookupIndex\> indica qué índice se abrirá primero cuando el diccionario se utilice para búsquedas desde otro libro. Se debe especificar el índice predeterminado si el diccionario tiene más de un índice. El nombre del índice dentro de las etiquetas \<DefaultLookupIndex\> en el archivo OPF también debe aparecer como el valor del atributo name en los elementos \<idx:entry\> en el contenido del diccionario (consulte [más información sobre HTML](https://kdp.amazon.com/es_ES/help/topic/G2HXJS944GL88DNV#html)).

Por ejemplo, para un diccionario español-francés, el código del idioma de origen sería es; el código del idioma de destino fr, y el índice principal podría llamarse Spanish. Consulte una [lista de códigos de país](http://www.w3schools.com/tags/ref_language_codes.asp).

**Ejemplo: Metadatos de un diccionario bilingüe **

\<x-metadata\>

\<DictionaryInLanguage\>es\</DictionaryInLanguage\>

\<DictionaryOutLanguage\>fr\</DictionaryOutLanguage\>

\<DefaultLookupIndex\>Spanish\</DefaultLookupIndex\>

...

\</x-metadata\>

En un diccionario monolingüe, el mismo código de lenguaje debe aparecer dos veces: la primera vez para identificar el idioma de origen y otra vez para identificar el mismo idioma como idioma de destino. Para identificar una variante regional del idioma de origen o de destino, se debe agregar un sufijo regional al código ISO 639-1. Por ejemplo, en-gb indica inglés británico, mientras que en-us indica inglés estadounidense.

**Ejemplo: Metadatos de diccionario monolingüe, variante regional **

\<x-metadata\>

\<DictionaryInLanguage\>en-us\</DictionaryInLanguage\>

\<DictionaryOutLanguage\>en-us\</DictionaryOutLanguage\>

\<DefaultLookupIndex\>headword\</DefaultLookupIndex\>

...

\</x-metadata\>

## Pautas sobre texto

Un formato claro y sencillo es lo que mejor se adapta a las búsquedas en el libro. Amazon recomienda las siguientes funciones de contenido y formato para un diccionario con el fin de lograr una buena calidad:

- El lema (la palabra que estamos definiendo) es lo primero que debe aparecer en la entrada y debe diferenciarse del resto del contenido (puede tener su propia línea, estar alineada a la izquierda, en negrita, etc.).
- Cada entrada del diccionario debe contener una definición o una traducción en el caso de los diccionarios bilingües.
- Debe aparecer una línea horizontal entre cada entrada.
- Cada sección de una letra del alfabeto debe comenzar en una página nueva.
- Se deben evitar las imágenes (consulte las [restricciones para las imágenes](https://kdp.amazon.com/help?topicId=G75V4YX5X8GRGXWV)).
- Se deben evitar las tablas (consulte las [restricciones para las tablas](https://kdp.amazon.com/help?topicId=GZ8BAXASXKB5JVML)).
- No se debe forzar el color, el tamaño ni el tipo de fuente (consulte las [pautas de texto](https://kdp.amazon.com/help?topicId=GH4DRT75GWWAGBTU)).

<br>

## HTML básico para diccionarios

### Formato

Los diccionarios para Kindle deben tener formato MOBI 7 en lugar de KF8. Por esta razón, el diseño del diccionario debe ser el de columna simple. Las columnas múltiples y las barras laterales no son compatibles con el formato MOBI 7.

<br>

### Elemento frameset

Todos los diccionarios deben tener un elemento \<mbp:frameset\> como primer elemento secundario del elemento \<body\>. Este elemento frameset contiene todos los elementos \<idx:entry\> del diccionario.

El espacio de nombres para este elemento \<mbp:frameset\> es

xmlns:mbp="[http://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines\_ES.pdf](https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines_ES.pdf)" y se debe declarar en el elemento raíz \<html\> del documento XHTML.

**Ejemplo:**

\<html xmlns:math="http://exslt.org/math" xmlns:svg="http://www.w3.org/2000/svg" xmlns:tl="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"

xmlns:saxon="http://saxon.sf.net/" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xmlns:cx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:dc="http://purl.org/dc/elements/1.1/"

xmlns:mbp="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:mmc="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"\>

\<head\>\<meta http-equiv="Content-Type" content="text/html; charset=utf-8"\>\</head\>

\<body\>

\<mbp:frameset\>

\<idx:entry name="english" scriptable="yes" spell="yes"\>

\<idx:short\>\<a id="1"\>\</a\>

\<idx:orth value="aardvark"\>\<b\>aard•vark\</b\>

\<idx:infl\>

\<idx:iform value="aardvarks"\>\</idx:iform\>

\<idx:iform value="aardvark's"\>\</idx:iform\> \<idx:iform value="aardvarks'"\>\</idx:iform\>

\</idx:infl\>

\</idx:orth\>

\<p\> Mamífero nocturno de África subsahariana que se alimenta exclusivamente de hormigas y termitas. \</p\>

\</idx:short\>

\</idx:entry\>

\[...otras entradas…\]

\</mbp:frameset\>

\</body\>

\</html\>

### Índice de lemas

Para poder hacer un índice alfabético de lemas, es necesario utilizar etiquetas especiales que no sean HTML estándar. La fuente seguirá siendo XHTML válido con estas etiquetas agregadas \<idx\>.

\<idx:entry\>..\</idx:entry\>

La etiqueta \<idx:entry\> marca el alcance de cada entrada que será indexada. En un diccionario, cada lema con su definición debe estar entre \<idx:entry\> y \</idx:entry\>. Puede poner cualquier tipo de HTML dentro de esta etiqueta.

La etiqueta \<idx:entry\> puede llevar los atributos name, scriptable, y spell. El atributo name indica el índice al cual pertenece la palabra clave. El valor del atributo name debe ser el mismo que el nombre del índice principal que se encuentra en el OPF. El atributo scriptable permite que se pueda acceder a una entrada desde el índice. El único valor posible para el atributo scriptable es "yes". El atributo spell permite una búsqueda con caracteres comodín y la corrección ortográfica. El único valor posible para el atributo spell es "yes".

**Ejemplo:**

\<idx:entry name="english" scriptable="yes" spell="yes"\>

La etiqueta \<idx:entry\> también puede llevar un atributo id con el número secuencial que identifica la entrada. Este número debe coincidir con el atributo id en una etiqueta ancla utilizada para el enlace de referencias cruzadas:

**Ejemplo:**

\<idx:entry name="japanese" scriptable="yes" spell="yes" id="12345"\>

\<a id="12345"\>\</a\>

El número de identificación no se utiliza para una búsqueda en el libro. En cambio, la entidad de notación fonética que se indexará para su búsqueda deberá estar almacenada en el elemento \<idx:orth\> como se indica en las siguientes secciones.

**\<idx:orth\>..\</idx:orth\> **

La etiqueta \<idx:orth\> se usa para delimitar el término que aparecerá en la lista del índice y que podrá buscarse como una palabra clave. Este es el texto que los usuarios podrán ingresar en la ventana de búsqueda para encontrar una entrada.

**Ejemplo:**

\<idx:orth\>Etiqueta de la entrada en el índice\</idx:orth\>

Este es un ejemplo de una entrada muy simple que podría ser parte de un diccionario de inglés. En este ejemplo, la palabra "chair" aparece en la lista del índice y los usuarios pueden buscarla.

**Ejemplo:**

\<idx:entry\>

\<idx:orth\>silla\</idx:orth\>

Asiento con respaldo, por lo general con cuatro patas, y en que solo cabe una persona.

\<idx:entry\>

El atributo value puede ser usado en la etiqueta \<idx:orth\> para incluir un término oculto en la entrada. Este atributo mantiene la funcionalidad de búsqueda en presencia del formato especial que normalmente aparece en el lema en los diccionarios.

**Ejemplo:**

\<idx:orth value="Etiqueta de entrada oculta en el índice"\>Formato de visualización\</orth\>

Si quiere que el lema aparezca en el diccionario con un número en superíndice para indicar homógrafos, con un símbolo de marca registrada, con puntos medios para separar sílabas o con cualquier otro símbolo adicional, este formato especial deberá aparecer en el texto entre etiquetas \<idx:orth\> pero no en el texto que figura en el atributo value. El texto en el atributo value debe tener la forma exacta que se utilizará en la búsqueda. Si no se suministra un atributo value, la entrada entre las etiquetas \<idx:orth\> se indexará para la búsqueda. Si se incluyen puntos medios, números en superíndices o cualquier otro símbolo entre las etiquetas \< \<idx:orth\>, \>, entonces las búsquedas dentro del libro fallarán a menos que se proporcione un término oculto con este formato en el atributo value.

**Ejemplo:**

\<idx:orth value="Amazon"\>A•ma•zon®\<sup\>3\</sup\>\</orth\>

Si el diccionario utiliza más de un texto ortográfico, entonces el atributo format en la etiqueta \<orth\> puede usarse para identificar cada texto al elaborar el índice.

**Ejemplo:**

\<idx:orth format="script name"\>

Junto con este índice primario de lemas para todas las entradas del diccionario, la búsqueda dentro del libro también requiere un índice complementario de formas conjugadas para cada lema. Para elaborar el índice oculto con flexiones, se deberán agregar datos adicionales entre las etiquetas \<idx:orth\> según se indica a continuación.

## Conjugaciones para diccionarios

Los diccionarios deben elaborarse para que las distintas conjugaciones de una palabra raíz se dirijan todas a la misma entrada. Debe proporcionar una lista completa de formas conjugadas para cada lema. Si una entrada utiliza distintas ortografías, se deben añadir distintas formas conjugadas para cada ortografía.

### Índice con flexiones

Para crear un índice oculto con flexiones, dichas variantes deben estar entre las etiquetas \<idx:infl\> y \<idx:iform /\>, anidadas en el elemento \<idx:orth\>. Un usuario no puede buscar directamente en este índice; solo puede realizar búsquedas dentro del libro.

**\<idx:infl\>..\</idx:infl\> **

El elemento \<idx:infl\> puede contener múltiples elementos \<idx:iform /\>. Los elementos \<idx:iform /\> son siempre elementos vacíos y se utilizan solo para llevar atributos y no contenido visible. El atributo value indica las formas conjugadas que forman parte del índice con flexiones.

**Ejemplo:**

\<idx:orth\>escribir

\<idx:infl\>

\<idx:iform value="escribiendo" /\>

\<idx:iform value="escrito" /\>

\<idx:iform value="escrita" /\>

\</idx:infl\>

\</idx:orth\>

Las etiquetas \<idx:infl\> y \<idx:iform /\>, y el atributo value son obligatorios. El elemento \<idx:infl\> también puede llevar un atributo opcional inflgrp para señalar una parte del lenguaje, y el elemento \<idx:iform /\> puede llevar un atributo opcional name para indicar la categoría del paradigma de conjugación. Para idiomas que usan una conjugación extensiva, el incluir estas categorías opcionales agrandará el tamaño del índice con flexiones y puede ralentizar el rendimiento durante la búsqueda.

**Ejemplo:**

\<idx:orth\>escribir

\<idx:infl inflgrp="noun"\>

\<idx:iform name="plural" value="escritura" /\>

\</idx:infl\>

\<idx:infl inflgrp="verb"\>

\<idx:iform name="present participle" value="escribiendo" /\>

\<idx:iform name="past participle" value="escrito" /\>

\<idx:iform name="present 1ps" value="escribo" /\>

\</idx:infl\>

\</idx:orth\>

Los valores calificados como atributos de la etiqueta \<idx:iform /\> no serán visibles para el usuario, pero darán la información necesaria para redireccionar las formas conjugadas a las palabras claves asociadas a estas durante la búsqueda en el libro. Para informar al usuario sobre las partes del lenguaje o sobre los paradigmas de conjugación, se debe incluir texto adicional en el cuerpo de la entrada (esto es, junto con la definición y los ejemplos).

**\<idx:key\>..\</idx:key\> (OBSOLETO)**

Al igual que la etiqueta \<idx:infl\>, la etiqueta \<idx:key\> está diseñada para permitir la búsqueda de una entrada en el índice a través de una palabra alternativa. Sin embargo, la presencia de una etiqueta \<idx:key\> en un diccionario Kindle puede generar inestabilidad en la búsqueda y puede interferir con la operación del parámetro de coincidencia exacta. Por esta razón, el uso de la etiqueta \<idx:key\> en los diccionarios Kindle ha quedado obsoleto. En su lugar, las formas de búsqueda alternativa deben estar entre la etiquetas, \<idx:infl\> y \<idx:iform /\>.

<br>

### Parámetro de coincidencia exacta

Kindle utiliza de manera predeterminada un algoritmo de búsqueda difusa para hacer coincidir signos diacríticos durante la búsqueda de una palabra. Para las palabras con acentos y demás letras especiales, se debe usar el atributo exact="yes" en la etiqueta \<idx:iform /\> para forzar la coincidencia exacta con las letras con tiles, "ñ", etc.

**Ejemplo:**

\<idx:entry name="spanish" scriptable="yes" spell="yes"\>

\<a id="12345"\>\</a\>

\<idx:orth value="uña"\>\<b\>uña\</b\>

\<idx:infl\>

\<idx:iform value="uñas" exact="yes" /\>

\</idx:infl\>

\</idx:orth\>

Cuando se establece el parámetro exact como "yes" se fuerza al dispositivo a hacer coincidir uñas con el lema uña, y se prohíbe la coincidencia con una.

## Creación de un diccionario con Kindlegen

Al crear un diccionario con KindleGen mediante la línea de comandos, use la siguiente sintaxis:

kindlegen.exe \[nombre.opf\] -c2 –verbose -dont\_append\_source

Si las entradas del diccionario se encuentran en un solo archivo XHTML muy grande, KindleGen podría no ser capaz de elaborar el diccionario. Si no es posible elaborar el diccionario, este problema puede resolverse dividiendo el contenido del diccionario entre dos o más archivos XHTML.

[Consulte las pautas sobre el uso de KindleGen](https://kdp.amazon.com/help?topicId=G79CTKR8BX79E96L).

<br>

<br>

## Prueba de diccionarios de Kindle

### Prueba de formato

Amazon recomienda verificar si el diccionario convertido tiene el formato correcto para garantizar una buena calidad de lectura:

- Compruebe el formato de las definiciones página por página y lea varias de ellas (el formato del diccionario se puede comprobar con Kindle Previewer o cualquier dispositivo Kindle, aunque las pruebas de búsqueda requieren utilizar un dispositivo e-reader).
- Compruebe que no hay caracteres no permitidos, palabras partidas ni visualización inapropiada de caracteres acentuados, símbolos, guía de pronunciación, etc.
- Compruebe si hay errores tipográficos.
- Verifique que los enlaces (si los hubiera) funcionan correctamente. (Los enlaces estarán deshabilitados en la ventana de búsqueda dentro del libro, pero deben funcionar dentro del mismo diccionario).
- Si utiliza imágenes, compruebe que son nítidas y legibles.
- Compruebe si el color y el tipo de fuente no están forzados.

<br>

### Prueba de búsqueda

Amazon recomienda comprobar si las definiciones aparecen correctamente cuando se utilice el diccionario para buscar palabras en otros libros. Esta parte de la prueba puede efectuarse solamente con dispositivos e-reader (sin incluir Kindle Previewer) porque sólo estos dispositivos permiten que el usuario configure el diccionario que utilizará para las búsquedas.

- Transfiera por USB el diccionario al dispositivo e-reader. Deberá conectar el dispositivo a su equipo a través de un cable USB-miniUSB. Su equipo debería detectar el dispositivo. Aparecerá una ventana donde verá una carpeta llamada Documentos. Ponga el archivo del diccionario dentro de esta carpeta y luego desconecte su Kindle del equipo informático.
- Configure el diccionario que quiere probar como el diccionario predeterminado para búsquedas:Kindle Paperwhite: Vaya a Inicio \> Menú \> Configuración \> Opciones del dispositivo \> Idioma y diccionarios \> Diccionarios \> \[Idioma origen\]
- Busque varias palabras para ver qué definición aparece. Abra otro libro que no sea el del diccionario, seleccione una palabra y verifique la definición que aparece en la ventana de búsqueda. Si la búsqueda falla completamente, verifique si hay errores en las etiquetas de HTML. Sugerencias de palabras para buscar:Conjugaciones de verbos tanto regulares como irregularesEjemplos: andar, ando, andas, anda, andando, andado, etc
- Sustantivos, adjetivos, adverbios y sus conjugaciones y declinacionesEjemplos: gran, grande, grandes; rojo, rojos, roja, rojas, etc
- Convenciones gramaticales y de puntuación que se utilicen normalmente en el idiomaEjemplo: del, al; casar, casarse; solo, sólo, etc
- Compruebe la vista de índice del diccionario. Deberá abrir el diccionario e introducir una palabra en la ventana de búsqueda. Deberá aparecer una lista en orden alfabético de lemas que deberá actualizarse dinámicamente de acuerdo con las teclas que se pulsen. Al seleccionar un lema de la lista del índice, se tiene que llevar al usuario a la entrada del diccionario de dicho lema.

Fuente: [https://kdp.amazon.com/es\_ES/help/topic/G2HXJS944GL88DNV](https://kdp.amazon.com/es_ES/help/topic/G2HXJS944GL88DNV)

Ir al mensaje: [https://t.me/calibreconfiguraciones/1/11591](https://t.me/calibreconfiguraciones/1/11591)

---

## [Volver al inicio](https://telegra.ph/Indice-Calibre-en-Espa%C3%B1ol-10-03)

<br>

---

[:material-arrow-left: Volver al índice](../../alfabetico.md) · [:fontawesome-brands-telegram: Preguntar en el grupo](https://t.me/calibreconfiguraciones){ target=_blank }
