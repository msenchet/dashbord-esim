/**
 * Lit la valeur actuelle d'une variable CSS (couleur du thème clair ou sombre).
 * @param {string} name nom de la variable, par exemple « --c-blue »
 * @returns {string} sa valeur, par exemple « #2a78d6 »
 */
function css(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}
