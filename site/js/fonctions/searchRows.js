/**
 * Applique la recherche multicritère et les valeurs cliquées, met à jour les pastilles
 * de critères, puis trie le résultat.
 * @param {Object[]} rows offres retenues par les filtres du haut
 * @returns {Object[]} offres du tableau « Toutes les offres »
 */
function searchRows(rows) {
  const criteria = parseQuery(state.search);
  const picks = Object.entries(state.picks);
  const kept = rows.filter(o => criteria.every(c => c.test(o))
    && picks.every(([field, values]) => values.has(pickValue(field, o))));
  renderCriteria(criteria, picks);
  return sortRows(kept);
}
