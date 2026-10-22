/**
 * Filtre tout le dashboard (KPI, graphiques, tableaux) sur un fournisseur et remonte aux KPI.
 * @param {string} provider nom du fournisseur
 */
function filterDashboardByProvider(provider) {
  state.providers = new Set([provider]);
  syncMulti(controls.provider);
  update();
  document.getElementById("kpis").scrollIntoView({ behavior: "smooth", block: "start" });
}
