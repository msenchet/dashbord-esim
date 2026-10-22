/**
 * Recalcule les choix des filtres et les bornes de prix d'après les offres chargées.
 * Appelée au démarrage et après chaque import.
 */
function refreshControls() {
  setMultiValues(controls.provider, sortFr(uniqueValues("provider")));
  setMultiValues(controls.country, sortFr(uniqueValues("country")));
  // validities / networks : choix disponibles ; les sélections disparues sont retirées.
  const validities = uniqueValues("validity").sort((a, b) => a - b);
  const networks = sortFr(uniqueValues("network"));
  state.validity = new Set([...state.validity].filter(v => validities.includes(v)));
  state.network = new Set([...state.network].filter(v => networks.includes(v)));
  setChipOptions(controls.validity, validities.map(v => [v, v + " j"]));
  setChipOptions(controls.network, networks.map(v => [v, v]));
  // low / high : prix extrêmes des offres chargées.
  let low = Infinity;
  let high = -Infinity;
  OFFERS.forEach(o => { low = Math.min(low, o.price); high = Math.max(high, o.price); });
  priceMin = Math.floor(low);
  priceMax = Math.ceil(high);
  state.pmin = priceMin;
  state.pmax = priceMax;
  syncPrice();
}
