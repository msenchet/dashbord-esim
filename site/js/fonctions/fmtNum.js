/**
 * Formate un nombre avec au plus 3 décimales et la virgule : 0.5 → « 0,5 ».
 * @param {number} value nombre à afficher
 * @returns {string} nombre formaté
 */
function fmtNum(value) {
  return value.toLocaleString("fr-FR", { maximumFractionDigits: 3 });
}
