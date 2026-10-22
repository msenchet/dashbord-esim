/**
 * Nettoie des lignes importées (CSV ou JSON) et les convertit en offres.
 * Les lignes sans prix lisible sont ignorées ; un SKU en double garde sa dernière version.
 * @param {Object[]} records lignes brutes
 * @param {string} sourceName nom du fichier (fournisseur par défaut)
 * @returns {Object[]} les offres valides
 * @throws {Error} si aucune ligne n'a de colonne de prix
 */
function cleanRecords(records, sourceName) {
  const fallback = providerFromName(sourceName);
  // bySku : offres indexées par SKU ; hasPrice : au moins une ligne a une colonne prix.
  const bySku = new Map();
  let hasPrice = false;
  records.forEach(raw => {
    const record = normalizeRecord(raw);
    if ("price" in record) hasPrice = true;
    const offer = recordToOffer(record, fallback);
    if (offer) bySku.set(offer.sku, offer);
  });
  if (records.length && !hasPrice) {
    throw new Error("colonne de prix introuvable (attendu : price ou prix)");
  }
  return [...bySku.values()];
}
