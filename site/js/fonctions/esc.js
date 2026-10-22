/**
 * Échappe un texte avant de l'insérer dans du HTML (protège contre les données importées).
 * @param {*} text texte à protéger
 * @returns {string} texte où & < > " sont remplacés par leurs entités HTML
 */
function esc(text) {
  const entities = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" };
  return String(text).replace(/[&<>"]/g, c => entities[c]);
}
