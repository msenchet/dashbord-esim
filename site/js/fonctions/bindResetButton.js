/**
 * Branche le bouton « Réinitialiser » : filtres, recherche, critères cliqués et tri effacés.
 */
function bindResetButton() {
  document.getElementById("reset").addEventListener("click", () => {
    resetState();
    syncAllControls();
    searchEl.value = "";
    update();
  });
}
