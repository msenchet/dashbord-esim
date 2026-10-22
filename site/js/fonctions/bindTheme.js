/**
 * Branche le bouton « Thème » et redessine la page si le système change de thème.
 */
function bindTheme() {
  document.getElementById("theme-toggle").addEventListener("click", toggleTheme);
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", update);
}
