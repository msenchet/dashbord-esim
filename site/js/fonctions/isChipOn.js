/**
 * Indique si une pastille est actuellement sélectionnée.
 * @param {Object} ctrl contrôle créé par createChips
 * @param {string} raw valeur de la pastille (attribut data-v)
 * @returns {boolean} true si elle est active
 */
function isChipOn(ctrl, raw) {
  const current = ctrl.store[ctrl.key];
  return ctrl.multiple ? current.has(chipValue(ctrl, raw)) : current === raw;
}
