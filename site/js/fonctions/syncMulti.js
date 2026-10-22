/**
 * Met à jour une liste déroulante d'après l'état : texte du résumé et cases cochées.
 * @param {Object} ctrl contrôle créé par createMulti
 */
function syncMulti(ctrl) {
  const selected = state[ctrl.key];
  const count = selected.size;
  ctrl.root.querySelector("summary").textContent =
    count === 0 ? ctrl.allLabel : count === 1 ? [...selected][0] : `${count} sélectionnés`;
  ctrl.menu.querySelectorAll("input").forEach(cb => { cb.checked = selected.has(cb.value); });
}
