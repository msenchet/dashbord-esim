/**
 * Branche les boutons d'export : CSV de la liste filtrée, CSV et JSON des offres affichées.
 */
function bindExportButtons() {
  document.getElementById("download").addEventListener("click",
    () => exportCSV(tableRows, "offres_esim_filtrees.csv"));
  document.getElementById("export-csv").addEventListener("click",
    () => exportCSV(current, "offres_esim.csv"));
  document.getElementById("export-json").addEventListener("click", () => exportJSON(current));
}
