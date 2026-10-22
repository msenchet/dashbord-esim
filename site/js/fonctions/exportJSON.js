/**
 * Télécharge des offres en JSON avec la date, les sources et les statistiques.
 * @param {Object[]} rows offres à exporter
 */
function exportJSON(rows) {
  const content = {
    generated_at: new Date().toISOString(), sources: SOURCES, total: rows.length,
    stats: computeStats(rows), offers: rows.map(toApi),
  };
  download("offres_esim.json", JSON.stringify(content, null, 2), "application/json");
}
