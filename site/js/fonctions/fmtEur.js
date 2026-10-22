/**
 * Formate un montant en euros à la française : 1234.5 → « 1 234,50 € ».
 * @param {number} value montant à afficher
 * @param {number} [digits=2] nombre de décimales
 * @returns {string} montant formaté
 */
function fmtEur(value, digits = 2) {
  return value.toLocaleString("fr-FR", {
    minimumFractionDigits: digits, maximumFractionDigits: digits,
  }) + " €";
}
