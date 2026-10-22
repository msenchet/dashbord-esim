/**
 * Affiche dans les deux champs de prix les bornes actuelles du filtre.
 */
function syncPrice() {
  pminEl.value = state.pmin;
  pmaxEl.value = state.pmax;
}
