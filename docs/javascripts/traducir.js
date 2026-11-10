/*
 * Botón de traducción: al elegir un idioma en el menú de idiomas del encabezado,
 * abre la página actual traducida por Google Traductor (dominio translate.goog).
 * "Español (original)" vuelve a la página sin traducir.
 */
(function () {
  "use strict";

  var IDIOMA_ORIGINAL = "es";
  var SUFIJO = ".translate.goog";

  // dunhill69.github.io  <->  dunhill69-github-io.translate.goog
  function hostAProxy(host) {
    return host.replace(/-/g, "--").replace(/\./g, "-") + SUFIJO;
  }
  function proxyAHost(host) {
    return host
      .slice(0, -SUFIJO.length)
      .replace(/--/g, "\u0000")
      .replace(/-/g, ".")
      .replace(/\u0000/g, "-");
  }

  // Dirección original (sin traducir) de la página que se está viendo.
  function urlOriginal() {
    var url = new URL(window.location.href);
    if (url.hostname.endsWith(SUFIJO)) {
      url.hostname = proxyAHost(url.hostname);
    } else if (url.hostname === "localhost" || url.hostname === "127.0.0.1") {
      // Vista previa local: se traduce la misma página del sitio publicado.
      var canonica = document.querySelector('link[rel="canonical"]');
      if (canonica) url = new URL(canonica.href);
    }
    ["_x_tr_sl", "_x_tr_tl", "_x_tr_hl", "_x_tr_pto"].forEach(function (p) {
      url.searchParams.delete(p);
    });
    return url;
  }

  function urlTraducida(idioma) {
    var url = urlOriginal();
    if (idioma === IDIOMA_ORIGINAL) return url.href;
    url.hostname = hostAProxy(url.hostname);
    url.searchParams.set("_x_tr_sl", IDIOMA_ORIGINAL);
    url.searchParams.set("_x_tr_tl", idioma);
    url.searchParams.set("_x_tr_hl", idioma);
    url.searchParams.set("_x_tr_pto", "wapp");
    return url.href;
  }

  // Se escucha en fase de captura para adelantarse a la navegación propia del tema.
  document.addEventListener(
    "click",
    function (evento) {
      var enlace = evento.target.closest && evento.target.closest("a[hreflang]");
      if (!enlace || !enlace.closest(".md-select")) return;
      evento.preventDefault();
      evento.stopImmediatePropagation();
      window.location.href = urlTraducida(enlace.getAttribute("hreflang"));
    },
    true
  );
})();
