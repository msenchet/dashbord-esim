/**
 * Ouvre le résumé d'un fournisseur (clic sur une barre des graphiques par fournisseur).
 * @param {string} provider nom du fournisseur
 */
function providerSummary(provider) {
  openSummary({
    kind: "Fournisseur", title: provider, groupBy: "country",
    rows: current.filter(o => o.provider === provider),
    list: { picks: { provider } },
    global: () => filterDashboardByProvider(provider),
  });
}
