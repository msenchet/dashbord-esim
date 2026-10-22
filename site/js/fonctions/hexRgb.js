/**
 * Décompose une couleur « #rrggbb » en ses trois composantes.
 * @param {string} hex couleur hexadécimale
 * @returns {number[]} [rouge, vert, bleu], de 0 à 255
 */
function hexRgb(hex) {
  return [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16));
}
