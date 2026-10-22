/**
 * Écrit une valeur dans une cellule CSV (textes entre guillemets, vide pour null).
 * @param {*} value valeur
 * @returns {string} cellule CSV
 */
function csvCell(value) {
  if (value === null) return "";
  return typeof value === "string" ? `"${value.replace(/"/g, '""')}"` : String(value);
}
