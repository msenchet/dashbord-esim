/**
 * Filtre la liste « Toutes les offres » (valeurs cliquées et/ou recherche), ferme le résumé
 * et fait défiler la page jusqu'à la liste.
 * @param {{picks: Object, search: string}} target filtres à appliquer, par exemple
 *   {picks: {provider: "Airalo"}} ou {search: "prix>=20 prix<25"}
 */
function showInList({ picks = {}, search = "" }) {
  state.picks = Object.fromEntries(Object.entries(picks).map(([f, v]) => [f, new Set([v])]));
  searchEl.value = search;
  state.search = search;
  state.page = 0;
  renderOffers(current);
  if (summaryEl.open) summaryEl.close();
  document.getElementById("offers-title").scrollIntoView({ behavior: "smooth", block: "start" });
}
