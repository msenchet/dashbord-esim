/*
 * Données injectées par build_site.py au moment de la génération (aucune fonction ici).
 */

/**
 * Offres d'origine au format « colonnes » compact :
 * - providers / countries / codes : listes de valeurs uniques (fournisseurs, pays, codes pays) ;
 * - provider / country : pour chaque offre, l'index dans ces listes ;
 * - sku, name, gb, validity, price, network, top_up : une valeur par offre
 *   (gb vaut null pour un forfait illimité, top_up vaut 1 si l'offre est rechargeable).
 */
const RAW = __DATA__;

/** Libellé de la source d'origine affiché dans le panneau « Données ». */
const BASE_LABEL = "Données d'origine (__FILES__ CSV)";
