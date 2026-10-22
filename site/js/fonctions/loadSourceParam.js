/**
 * Avec « ?source=<url> » dans l'adresse, propose de charger les données de cette API.
 * Rien n'est chargé sans confirmation : un lien piégé ne peut pas afficher de fausses offres
 * à l'insu du visiteur.
 */
function loadSourceParam() {
  const source = new URLSearchParams(location.search).get("source");
  if (!source) return;
  imports.mode = "replace";
  syncChips(controls.importMode);
  document.getElementById("api-url").value = source;
  confirmExternalSource(source);
}
