/**
 * Déduit un nom de fournisseur d'un nom de fichier : « super_sim.csv » → « Super Sim ».
 * @param {string} name nom ou chemin du fichier
 * @returns {string} nom de fournisseur
 */
function providerFromName(name) {
  return String(name).split(/[\\/]/).pop().replace(/\.[^.]+$/, "")
    .replace(/[_-]/g, " ").trim()
    .replace(/\S+/g, word => word[0].toUpperCase() + word.slice(1).toLowerCase());
}
