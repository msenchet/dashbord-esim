/**
 * Bouton de cellule cliquable qui ajoute la valeur comme filtre.
 * @param {string} field colonne (voir PICK_FIELDS)
 * @param {Object} offer offre ou ligne de fournisseur
 * @param {string} html contenu affiché (déjà échappé)
 * @returns {string} HTML du bouton
 */
function cellPick(field, offer, html) {
  const value = pickValue(field, offer);
  return `<button type="button" class="cell-pick" data-f="${field}" data-v="${esc(value)}"
    aria-pressed="${isPicked(field, value)}"
    title="Filtrer : ${esc(PICK_FIELDS[field])} = ${esc(pickLabel(field, value))}">`
    + `${html}</button>`;
}
