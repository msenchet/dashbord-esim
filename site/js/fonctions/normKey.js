/**
 * Normalise un nom de colonne importé et applique les alias :
 * « Validité (jours) » → validity_days.
 * @param {string} key nom de colonne d'origine
 * @returns {string} nom interne
 */
function normKey(key) {
  // text : nom sans accents, en minuscules, avec « _ » comme seul séparateur.
  const text = String(key).normalize("NFKD").replace(/[^\x00-\x7f]/g, "").trim().toLowerCase()
    .replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
  return ALIASES[text] || text;
}
