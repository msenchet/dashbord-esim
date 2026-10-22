/**
 * Applique les filtres du haut de page aux offres chargées.
 * @returns {Object[]} les offres retenues
 */
function filtered() {
  return OFFERS.filter(o =>
    (!state.providers.size || state.providers.has(o.provider)) &&
    (!state.countries.size || state.countries.has(o.country)) &&
    (!state.validity.size || state.validity.has(o.validity)) &&
    (!state.network.size || state.network.has(o.network)) &&
    (state.kind === "all" || (state.kind === "unlimited") === o.unlimited) &&
    o.price >= state.pmin && o.price <= state.pmax);
}
