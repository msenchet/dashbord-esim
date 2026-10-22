/**
 * Remplace le texte de la recherche, revient à la première page et réaffiche la liste.
 * @param {string} value nouveau texte
 */
function setSearch(value) {
  searchEl.value = value;
  state.search = value;
  state.page = 0;
  renderOffers(current);
}
