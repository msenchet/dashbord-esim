/**
 * Ajoute ou retire une valeur cliquée, puis réaffiche la liste des offres.
 * Deux valeurs d'une même colonne se combinent en « ou », des colonnes différentes en « et ».
 * @param {string} field colonne
 * @param {string} value valeur texte
 */
function togglePick(field, value) {
  const selected = state.picks[field] || (state.picks[field] = new Set());
  if (selected.has(value)) selected.delete(value);
  else selected.add(value);
  if (!selected.size) delete state.picks[field];
  state.page = 0;
  renderOffers(current);
}
