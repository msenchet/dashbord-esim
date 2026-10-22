/**
 * Retire un mot de la barre de recherche (clic sur le ✕ de sa pastille).
 * @param {string} raw mot tel qu'il a été tapé
 */
function removeQueryToken(raw) {
  const tokens = state.search.match(TOKEN_RE) || [];
  const index = tokens.indexOf(raw);
  if (index >= 0) tokens.splice(index, 1);
  setSearch(tokens.join(" "));
}
