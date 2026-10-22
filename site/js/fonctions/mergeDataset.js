/**
 * Ajoute ou remplace les offres chargées selon le mode d'import (un SKU existant est mis à jour).
 * @param {Object[]} incoming offres importées
 * @param {string} label nom de la source ajoutée à SOURCES
 * @returns {{added: number, updated: number}} offres ajoutées et mises à jour
 */
function mergeDataset(incoming, label) {
  const replace = imports.mode === "replace";
  // before : offres conservées avant fusion ; bySku : offres indexées par SKU.
  const before = replace ? 0 : OFFERS.length;
  const bySku = new Map(replace ? [] : OFFERS.map(o => [o.sku, o]));
  incoming.forEach(o => bySku.set(o.sku, o));
  OFFERS = [...bySku.values()];
  SOURCES = (replace ? [] : SOURCES).concat(label);
  const added = OFFERS.length - before;
  return { added, updated: incoming.length - added };
}
