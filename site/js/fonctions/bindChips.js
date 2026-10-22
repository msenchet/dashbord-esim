/**
 * Branche le clic sur les pastilles d'un groupe, puis rafraîchit la page.
 * @param {Object} ctrl contrôle créé par createChips
 */
function bindChips(ctrl) {
  ctrl.root.addEventListener("click", e => {
    const chip = e.target.closest(".chip");
    if (!chip) return;
    pickChip(ctrl, chip.dataset.v);
    syncChips(ctrl);
    update();
  });
}
