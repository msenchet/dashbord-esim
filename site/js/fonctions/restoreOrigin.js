/**
 * Oublie les imports et recharge les données d'origine.
 */
function restoreOrigin() {
  OFFERS = BASE;
  SOURCES = [BASE_LABEL];
  refreshControls();
  update();
  renderSource();
  setStatus("Données d'origine rechargées.", "ok");
}
