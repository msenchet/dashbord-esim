/**
 * Formate un entier avec l'espace des milliers : 5056 → « 5 056 ».
 * @param {number} value nombre à afficher
 * @returns {string} nombre formaté
 */
function fmtInt(value) {
  return value.toLocaleString("fr-FR");
}
