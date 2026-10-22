/**
 * Crée la description d'un groupe de pastilles (validité, réseau, forfait, mode d'import).
 * @param {string} id identifiant du conteneur dans la page
 * @param {Object} store objet qui porte la valeur (state ou imports)
 * @param {string} key champ de store modifié par les pastilles
 * @param {Object} [options] multiple : plusieurs choix possibles (Set) ;
 *   numeric : valeurs converties en nombre
 * @returns {Object} contrôle : root, store, key, multiple, numeric
 */
function createChips(id, store, key, options = {}) {
  return {
    type: "chips", root: document.getElementById(id), store, key,
    multiple: !!options.multiple, numeric: !!options.numeric,
  };
}
