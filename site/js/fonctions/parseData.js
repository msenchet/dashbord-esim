/**
 * Lit le volume de data (en Go) et détecte l'illimité, comme esim/parse_data_gb.py.
 * @param {*} gb valeur de la colonne data_gb (nombre ou texte avec unité)
 * @param {string|null} display libellé affiché (« 3 Go », « Illimité »)
 * @returns {Array} [volume en Go ou null, est illimité]
 */
function parseData(gb, display) {
  if ([display, gb].some(v => typeof v === "string" && UNLIMITED_RE.test(v))) return [null, true];
  if (!isBlank(gb)) {
    // number : valeur numérique ; match : unité éventuellement écrite à côté.
    const number = parsePrice(gb);
    const match = String(gb).match(VOLUME_RE);
    const unit = ((match && match[2]) || "go").toLowerCase();
    if (!isNaN(number)) return [number * UNIT_TO_GB[unit], false];
  }
  if (typeof display === "string") {
    const match = display.match(VOLUME_RE);
    if (match) {
      return [Number(match[1].replace(",", ".")) * UNIT_TO_GB[(match[2] || "go").toLowerCase()],
        false];
    }
  }
  return [null, false];
}
