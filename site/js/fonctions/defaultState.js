/**
 * Valeurs initiales des filtres, de la recherche, du tri et de la pagination.
 * @param {number} pmin prix minimum du filtre
 * @param {number} pmax prix maximum du filtre
 * @returns {Object} état neuf :
 *   providers / countries / validity / network : valeurs cochées (vide = pas de filtre) ;
 *   kind : « all », « limited » ou « unlimited » ; pmin / pmax : bornes de prix ;
 *   search : texte de la recherche ; picks : valeurs cliquées dans les tableaux, par colonne ;
 *   page : page affichée ; sortKey / sortDir : colonne et sens du tri
 *   (1 croissant, -1 décroissant).
 */
function defaultState(pmin, pmax) {
  return {
    providers: new Set(), countries: new Set(), validity: new Set(), network: new Set(),
    kind: "all", pmin, pmax, search: "", picks: {}, page: 0, sortKey: "price", sortDir: 1,
  };
}
