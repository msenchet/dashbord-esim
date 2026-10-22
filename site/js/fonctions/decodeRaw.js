/**
 * Reconstruit la liste des offres à partir du format colonnes compact injecté dans la page.
 * @param {Object} raw données compactes (voir RAW dans donnees.js)
 * @returns {Object[]} les offres complètes
 */
function decodeRaw(raw) {
  return raw.price.map((price, i) => makeOffer({
    sku: raw.sku[i],
    provider: raw.providers[raw.provider[i]],
    country: raw.countries[raw.country[i]],
    code: raw.codes[raw.country[i]],
    name: raw.name[i],
    gb: raw.gb[i],
    unlimited: raw.gb[i] === null,
    validity: raw.validity[i],
    price,
    network: raw.network[i],
    topUp: raw.top_up[i] === 1,
    currency: "EUR",
  }));
}
