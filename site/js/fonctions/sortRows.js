/**
 * Trie les offres selon la colonne et le sens choisis dans state (valeurs vides en dernier).
 * @param {Object[]} rows offres (la liste est triée sur place)
 * @returns {Object[]} la même liste, triée
 */
function sortRows(rows) {
  const column = OFFER_COLUMNS.find(c => c.key === state.sortKey);
  const key = column.sortBy || state.sortKey;
  return rows.sort((a, b) => {
    const x = a[key] ?? Infinity;
    const y = b[key] ?? Infinity;
    const order = typeof x === "string" && typeof y === "string" ? x.localeCompare(y, "fr") : x - y;
    return order * state.sortDir;
  });
}
