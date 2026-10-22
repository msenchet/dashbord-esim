/**
 * Remet tous les filtres, la recherche et le tri à leurs valeurs initiales.
 */
function resetState() {
  Object.assign(state, defaultState(priceMin, priceMax));
}
