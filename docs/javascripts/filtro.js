/*
 * Filtro instantáneo del índice A–Z: oculta los tutoriales que no coinciden
 * con lo escrito (sin distinguir mayúsculas ni tildes) y las letras vacías.
 */
(function () {
  "use strict";

  function normalizar(texto) {
    return texto
      .toLowerCase()
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "");
  }

  function iniciar() {
    var campo = document.getElementById("tut-filtro");
    if (!campo) return;
    var info = document.getElementById("tut-filtro-info");
    var contenido = campo.closest(".md-content__inner") || document;
    var titulos = contenido.querySelectorAll('h2[id^="letra-"]');
    var letras = contenido.querySelector(".tut-letras");

    function aplicar() {
      var palabras = normalizar(campo.value).split(/\s+/).filter(Boolean);
      var visibles = 0;

      titulos.forEach(function (h2) {
        var lista = h2.nextElementSibling;
        if (!lista || lista.tagName !== "UL") return;
        var enLetra = 0;
        lista.querySelectorAll(":scope > li").forEach(function (li) {
          var texto = normalizar(li.textContent);
          var coincide = palabras.every(function (p) { return texto.indexOf(p) !== -1; });
          li.hidden = !coincide;
          if (coincide) enLetra++;
        });
        h2.hidden = lista.hidden = enLetra === 0;
        visibles += enLetra;
      });

      if (letras) letras.hidden = palabras.length > 0;
      info.textContent = palabras.length
        ? visibles === 0
          ? "No hay tutoriales que coincidan. Probá con otra palabra o preguntá en el grupo."
          : visibles + (visibles === 1 ? " tutorial encontrado." : " tutoriales encontrados.")
        : "";
    }

    campo.addEventListener("input", aplicar);
  }

  // Compatible con la navegación instantánea del tema Material.
  if (typeof document$ !== "undefined") {
    document$.subscribe(iniciar);
  } else {
    document.addEventListener("DOMContentLoaded", iniciar);
  }
})();
