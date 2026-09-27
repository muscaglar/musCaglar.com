// Runs before the page is drawn, so that a saved light or dark choice never flashes the wrong way.
try {
  var t = localStorage.getItem("theme");
  if (t === "light" || t === "dark") document.documentElement.dataset.theme = t;
} catch (e) {}
