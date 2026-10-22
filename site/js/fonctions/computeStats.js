/**
 * Calcule les indicateurs, avec les mêmes formules que esim/compute_stats.py.
 * La data moyenne et le prix au Go excluent l'illimité et les volumes inconnus.
 * @param {Object[]} rows offres
 * @returns {Object} total_offers, offers_over_100, price_min, price_max, price_mean,
 *   data_mean_gb, unlimited_offers, providers, price_per_gb_mean (null si non calculable)
 */
function computeStats(rows) {
  let min = Infinity;
  let max = -Infinity;
  rows.forEach(o => { min = Math.min(min, o.price); max = Math.max(max, o.price); });
  // withGb : offres à volume connu ; withPerGb : offres dont le prix au Go est calculable.
  const withGb = rows.filter(o => o.gb !== null);
  const withPerGb = rows.filter(o => o.perGb !== null);
  return {
    total_offers: rows.length,
    offers_over_100: rows.filter(o => o.price > THRESHOLD).length,
    price_min: min,
    price_max: max,
    price_mean: mean(rows.map(o => o.price)),
    data_mean_gb: withGb.length ? mean(withGb.map(o => o.gb)) : null,
    unlimited_offers: rows.filter(o => o.unlimited).length,
    providers: new Set(rows.map(o => o.provider)).size,
    price_per_gb_mean: withPerGb.length ? mean(withPerGb.map(o => o.perGb)) : null,
  };
}
