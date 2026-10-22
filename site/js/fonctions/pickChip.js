/**
 * Applique le clic sur une pastille : bascule (choix multiple) ou remplace (choix unique).
 * @param {Object} ctrl contrôle créé par createChips
 * @param {string} raw valeur de la pastille cliquée
 */
function pickChip(ctrl, raw) {
  if (!ctrl.multiple) {
    ctrl.store[ctrl.key] = raw;
    return;
  }
  const selected = ctrl.store[ctrl.key];
  const value = chipValue(ctrl, raw);
  if (selected.has(value)) selected.delete(value);
  else selected.add(value);
}
