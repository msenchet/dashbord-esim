/**
 * Convertit la valeur texte d'une pastille dans le type attendu (nombre ou texte).
 * @param {Object} ctrl contrôle créé par createChips
 * @param {string} raw valeur lue dans l'attribut data-v
 * @returns {number|string} valeur convertie
 */
function chipValue(ctrl, raw) {
  return ctrl.numeric ? Number(raw) : raw;
}
