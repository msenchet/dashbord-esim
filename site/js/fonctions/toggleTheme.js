/**
 * Bascule entre thème clair et sombre, le mémorise si possible et redessine les graphiques.
 */
function toggleTheme() {
  const dark = rootEl.dataset.theme
    ? rootEl.dataset.theme === "dark"
    : matchMedia("(prefers-color-scheme: dark)").matches;
  rootEl.dataset.theme = dark ? "light" : "dark";
  try {
    localStorage.setItem("theme", rootEl.dataset.theme);
  } catch (e) {
    // Stockage indisponible : le choix vaut seulement pour cette visite.
  }
  update();
}
