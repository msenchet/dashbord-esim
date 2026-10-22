/**
 * Devine le séparateur d'un CSV : celui qui découpe la première ligne en le plus de colonnes.
 * @param {string} firstLine première ligne du fichier (en-têtes)
 * @returns {string} séparateur choisi parmi CSV_DELIMITERS
 */
function detectDelimiter(firstLine) {
  return CSV_DELIMITERS.reduce((best, candidate) =>
    firstLine.split(candidate).length > firstLine.split(best).length ? candidate : best);
}
