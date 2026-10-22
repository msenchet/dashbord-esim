/**
 * Pastille colorée du réseau : 4G (vert-bleu), 5G (violet), autre (gris).
 * @param {string} network réseau de l'offre
 * @returns {string} HTML de la pastille
 */
function networkBadge(network) {
  const kind = /^4g$/i.test(network) ? "net-4g" : /^5g$/i.test(network) ? "net-5g" : "net-other";
  return `<span class="badge ${kind}">${esc(network)}</span>`;
}
