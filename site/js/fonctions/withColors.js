/**
 * Donne à une série de barres une couleur par barre et un fin liseré de la couleur du fond.
 * @param {Object} trace série Plotly (modifiée)
 * @param {string[]} colors une couleur par barre
 * @returns {Object} la même série
 */
function withColors(trace, colors) {
  return Object.assign(trace, {
    marker: { color: colors, line: { color: css("--surface"), width: 1 } },
  });
}
