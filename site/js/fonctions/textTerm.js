/**
 * Critère de recherche texte : l'offre doit contenir le mot (sans tenir compte des accents).
 * @param {string} word mot déjà normalisé
 * @returns {{label: string, test: Function}} libellé affiché et test appliqué à une offre
 */
function textTerm(word) {
  return { label: `« ${word} »`, test: o => o._hay.includes(word) };
}
