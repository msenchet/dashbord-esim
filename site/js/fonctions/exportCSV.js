/**
 * Télécharge des offres en CSV, colonnes de l'API, avec BOM pour Excel.
 * @param {Object[]} rows offres à exporter
 * @param {string} filename nom du fichier
 */
function exportCSV(rows, filename) {
  const keys = Object.keys(toApi(BASE[0]));
  const lines = [keys.join(",")]
    .concat(rows.map(toApi).map(record => keys.map(k => csvCell(record[k])).join(",")));
  download(filename, "﻿" + lines.join("\n"), "text/csv;charset=utf-8");
}
