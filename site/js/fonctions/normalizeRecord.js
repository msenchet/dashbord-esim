/**
 * Renomme les colonnes d'une ligne importée avec leurs noms internes (premier doublon gardé).
 * @param {Object} raw ligne telle que lue dans le fichier
 * @returns {Object} ligne avec les clés normalisées
 */
function normalizeRecord(raw) {
  const record = {};
  Object.entries(raw).forEach(([key, value]) => {
    const name = normKey(key);
    if (!(name in record)) record[name] = value;
  });
  return record;
}
