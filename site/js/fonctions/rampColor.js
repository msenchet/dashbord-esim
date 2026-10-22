/**
 * Couleur de la rampe bleue pour une position entre 0 (clair) et 1 (foncé).
 * @param {number} t position, ramenée entre 0 et 1
 * @returns {string} couleur hexadécimale
 */
function rampColor(t) {
  return RAMP[Math.round(Math.max(0, Math.min(1, t)) * (RAMP.length - 1))];
}
