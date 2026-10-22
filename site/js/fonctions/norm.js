/**
 * Normalise un texte pour la recherche : sans accents et en minuscules (« Émirats » → « emirats »).
 * @param {*} text texte (null et undefined donnent une chaîne vide)
 * @returns {string} texte normalisé
 */
function norm(text) {
  return String(text ?? "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
}
