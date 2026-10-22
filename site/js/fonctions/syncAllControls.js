/**
 * Remet l'affichage de tous les contrôles en accord avec l'état (après une réinitialisation).
 */
function syncAllControls() {
  Object.values(controls).forEach(ctrl => {
    if (ctrl.type === "multi") syncMulti(ctrl);
    else syncChips(ctrl);
  });
  syncPrice();
}
