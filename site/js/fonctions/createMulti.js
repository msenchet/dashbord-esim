/**
 * Crée la description d'une liste à cocher déroulante (fournisseurs, destinations).
 * @param {string} id identifiant de l'élément <details> dans la page
 * @param {string} key champ de state contenant les valeurs cochées
 * @param {string} allLabel texte affiché quand rien n'est coché (« Tous », « Toutes »)
 * @returns {Object} contrôle : root, menu, key, allLabel, values (valeurs proposées)
 */
function createMulti(id, key, allLabel) {
  const root = document.getElementById(id);
  return { type: "multi", root, menu: root.querySelector(".menu"), key, allLabel, values: [] };
}
