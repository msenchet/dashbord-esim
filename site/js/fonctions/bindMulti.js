/**
 * Branche les événements d'une liste déroulante : cocher, « Tout », « Aucun filtre »,
 * et fermeture quand on clique ailleurs dans la page.
 * @param {Object} ctrl contrôle créé par createMulti
 */
function bindMulti(ctrl) {
  ctrl.menu.addEventListener("change", e => {
    const selected = state[ctrl.key];
    if (e.target.checked) selected.add(e.target.value);
    else selected.delete(e.target.value);
    syncMulti(ctrl);
    update();
  });
  ctrl.menu.addEventListener("click", e => {
    const action = e.target.dataset.a;
    if (!action) return;
    state[ctrl.key] = action === "all" ? new Set(ctrl.values) : new Set();
    syncMulti(ctrl);
    update();
  });
  document.addEventListener("click", e => {
    if (!ctrl.root.contains(e.target)) ctrl.root.open = false;
  });
}
