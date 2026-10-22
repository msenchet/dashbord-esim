/**
 * Avec « ?source=<url> » dans l'adresse, remplace les données par celles de cette API.
 */
function loadSourceParam() {
  const source = new URLSearchParams(location.search).get("source");
  if (!source) return;
  imports.mode = "replace";
  syncChips(controls.importMode);
  document.getElementById("api-url").value = source;
  importUrl(source);
}
