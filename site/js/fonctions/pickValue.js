/**
 * Valeur d'une offre pour un filtre par clic, toujours en texte (« 30 », « true », « 5G »).
 * @param {string} field colonne cliquée (voir PICK_FIELDS)
 * @param {Object} offer offre ou ligne de fournisseur
 * @returns {string} valeur comparée
 */
function pickValue(field, offer) {
  return String(offer[field]);
}
