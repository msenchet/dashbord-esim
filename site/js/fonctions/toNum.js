/**
 * Convertit un nombre écrit avec une virgule ou un point : « 2,5 » → 2.5.
 * @param {string|number} text nombre écrit
 * @returns {number} le nombre
 */
function toNum(text) {
  return Number(String(text).replace(",", "."));
}
