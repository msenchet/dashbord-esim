/*
 * État de la page, modifié par les fonctions (aucune fonction définie ici).
 * Ce fichier est placé après config.js et avant les fonctions dans la page générée.
 */

/** Offres d'origine, reconstruites à partir des données compactes RAW. */
const BASE = decodeRaw(RAW);

/** Offres actuellement chargées (origine + imports éventuels). */
let OFFERS = BASE;

/** Noms lisibles des sources chargées, dans l'ordre d'import. */
let SOURCES = [BASE_LABEL];

/** Prix minimal et maximal (arrondis à l'euro) des offres chargées : bornes du filtre prix. */
let priceMin = 0;
let priceMax = 0;

/** Filtres, recherche, tri et page courante (voir defaultState pour le détail des champs). */
const state = defaultState(0, 0);

/** Réglages de l'import : mode « append » (ajouter) ou « replace » (remplacer). */
const imports = { mode: "append" };

/** Offres retenues par les filtres du haut de page (base des KPI et des graphiques). */
let current = [];

/** Offres du tableau « Toutes les offres » après recherche et tri (base de l'export CSV). */
let tableRows = [];

/** Dernier HTML des pastilles de critères, pour ne pas le réécrire inutilement. */
let lastPicksHtml = "";

/** Compteur d'entrées/sorties du glisser-déposer (le survol traverse plusieurs éléments). */
let dragDepth = 0;

/** Contrôles de filtre (listes déroulantes et pastilles), créés par initControls. */
let controls = null;

/** Éléments de la page utilisés souvent. */
const rootEl = document.documentElement;            // <html>, porte le thème clair/sombre
const searchEl = document.getElementById("search");  // barre de recherche des offres
const summaryEl = document.getElementById("summary"); // panneau de résumé (dialog)
const statusEl = document.getElementById("import-status"); // message d'import
const pminEl = document.getElementById("f-pmin");    // prix minimum du filtre
const pmaxEl = document.getElementById("f-pmax");    // prix maximum du filtre
const fileInput = document.getElementById("file-input"); // sélecteur de fichiers caché
