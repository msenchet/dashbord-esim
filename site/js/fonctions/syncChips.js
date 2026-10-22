/**
 * Met à jour l'aspect des pastilles d'après l'état (attribut aria-pressed).
 * @param {Object} ctrl contrôle créé par createChips
 */
function syncChips(ctrl) {
  ctrl.root.querySelectorAll(".chip").forEach(chip => {
    chip.setAttribute("aria-pressed", isChipOn(ctrl, chip.dataset.v));
  });
}
