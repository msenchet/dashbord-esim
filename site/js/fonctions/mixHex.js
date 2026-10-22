/**
 * Mélange deux couleurs : t = 0 donne a, t = 1 donne b.
 * @param {string} a première couleur « #rrggbb »
 * @param {string} b seconde couleur « #rrggbb »
 * @param {number} t proportion de b, entre 0 et 1
 * @returns {string} couleur mélangée « #rrggbb »
 */
function mixHex(a, b, t) {
  const from = hexRgb(a);
  const to = hexRgb(b);
  return "#" + from.map((v, i) =>
    Math.round(v + (to[i] - v) * t).toString(16).padStart(2, "0")).join("");
}
