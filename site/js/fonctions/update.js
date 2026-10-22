/**
 * Recalcule les offres filtrées et redessine KPI, graphiques et tableaux.
 * Sans résultat, affiche le message « Aucune offre ne correspond aux filtres ».
 */
function update() {
  current = filtered();
  const empty = current.length === 0;
  document.getElementById("content").hidden = empty;
  document.getElementById("empty").hidden = !empty;
  if (empty) {
    document.getElementById("kpis").innerHTML = "";
    return;
  }
  renderKpis(current);
  const prov = byProvider(current);
  renderCharts(current, prov);
  renderProviderTable(prov);
  renderOffers(current);
}
