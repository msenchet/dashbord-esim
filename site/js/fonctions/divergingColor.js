/**
 * Couleur bleu ↔ rouge selon l'écart à la moyenne : bleu en dessous, rouge au-dessus,
 * plus intense quand l'écart grandit (part d'un gris neutre).
 * @param {number} value valeur à colorer
 * @param {number} mid moyenne de référence
 * @param {number} spread écart qui donne l'intensité maximale
 * @returns {string} couleur « #rrggbb »
 */
function divergingColor(value, mid, spread) {
  // d : écart relatif ramené entre -1 et 1.
  const d = spread > 0 ? Math.max(-1, Math.min(1, (value - mid) / spread)) : 0;
  return mixHex(css("--div-mid"), css(d < 0 ? "--c-blue" : "--c-red"), 0.45 + 0.55 * Math.abs(d));
}
