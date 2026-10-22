/**
 * Regroupe les offres par fournisseur et calcule leurs indicateurs.
 * @param {Object[]} rows offres
 * @returns {Object[]} une ligne par fournisseur (provider, count, share en %, mean, min, max,
 *   unlimited, perGb), triée du plus grand nombre d'offres au plus petit
 */
function byProvider(rows) {
  const groups = new Map();
  rows.forEach(o => {
    if (!groups.has(o.provider)) groups.set(o.provider, []);
    groups.get(o.provider).push(o);
  });
  return [...groups].map(([provider, list]) => {
    // prices : prix des offres ; limited : offres dont le prix au Go est connu.
    const prices = list.map(o => o.price);
    const limited = list.filter(o => o.perGb !== null);
    return {
      provider, count: list.length, share: list.length / rows.length * 100,
      mean: mean(prices), min: Math.min(...prices), max: Math.max(...prices),
      unlimited: list.filter(o => o.unlimited).length,
      perGb: limited.length ? mean(limited.map(o => o.perGb)) : null,
    };
  }).sort((a, b) => b.count - a.count);
}
