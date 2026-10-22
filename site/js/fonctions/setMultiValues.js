/**
 * Remplace les valeurs proposées par une liste déroulante (après un import par exemple).
 * Les valeurs cochées qui n'existent plus sont décochées.
 * @param {Object} ctrl contrôle créé par createMulti
 * @param {string[]} values nouvelles valeurs, déjà triées
 */
function setMultiValues(ctrl, values) {
  ctrl.values = values;
  state[ctrl.key] = new Set([...state[ctrl.key]].filter(v => values.includes(v)));
  ctrl.menu.innerHTML = `<div class="menu-actions">
      <button class="btn" data-a="all" type="button">Tout</button>
      <button class="btn" data-a="none" type="button">Aucun filtre</button></div>` +
    values.map(v => `<label><input type="checkbox" value="${esc(v)}"> ${esc(v)}</label>`).join("");
  syncMulti(ctrl);
}
