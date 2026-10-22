/**
 * Convertit une offre au format d'export de l'API Python (mêmes noms de champs).
 * @param {Object} o offre
 * @returns {Object} offre exportable
 */
function toApi(o) {
  return {
    sku: o.sku, provider: o.provider, product_name: o.name, country_code: o.code,
    country_name: o.country, data_gb: o.gb, data_display: o.display, is_unlimited: o.unlimited,
    validity_days: o.validity, price: o.price, currency: o.currency,
    price_per_gb: o.perGb === null ? null : Math.round(o.perGb * 1e4) / 1e4,
    network: o.network, top_up: o.topUp,
  };
}
