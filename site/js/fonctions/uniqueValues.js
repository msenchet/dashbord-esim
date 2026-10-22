/**
 * Valeurs distinctes d'un champ parmi les offres chargées (valeurs nulles exclues).
 * @param {string} key champ de l'offre (provider, country, validity, network…)
 * @returns {Array} valeurs uniques, dans l'ordre d'apparition
 */
function uniqueValues(key) {
  return [...new Set(OFFERS.map(o => o[key]).filter(v => v !== null))];
}
