/**
 * Empreinte courte et stable d'un texte (algorithme djb2), pour fabriquer un SKU manquant.
 * @param {string} text texte à résumer
 * @returns {string} empreinte en base 36
 */
function hash(text) {
  let h = 5381;
  for (let i = 0; i < text.length; i++) h = (h * 33) ^ text.charCodeAt(i);
  return (h >>> 0).toString(36);
}
