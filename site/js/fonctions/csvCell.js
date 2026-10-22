/**
 * Écrit une valeur dans une cellule CSV (textes entre guillemets, vide pour null).
 * Un texte qui commence par = + - @ (formule pour Excel) est précédé d'une apostrophe,
 * pour qu'un fichier importé piégé ne puisse pas exécuter de formule à l'ouverture.
 * @param {*} value valeur
 * @returns {string} cellule CSV
 */
function csvCell(value) {
  if (value === null) return "";
  if (typeof value !== "string") return String(value);
  const safe = CSV_FORMULA_RE.test(value) ? "'" + value : value;
  return `"${safe.replace(/"/g, '""')}"`;
}
