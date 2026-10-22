/**
 * Libellé lisible d'une valeur cliquée : « 30 » → « 30 j », « true » → « Oui ».
 * @param {string} field colonne cliquée
 * @param {string} value valeur texte (voir pickValue)
 * @returns {string} libellé affiché
 */
function pickLabel(field, value) {
  if (field === "validity") return value === "null" ? "—" : value + " j";
  if (field === "topUp") return value === "true" ? "Oui" : "Non";
  return value;
}
