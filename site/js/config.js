/*
 * Constantes du dashboard (aucune fonction ici). Chaque constante est décrite au-dessus.
 */

/** Seuil (€) au-delà duquel une offre est « chère » : KPI dédié, barres et prix en orange. */
const THRESHOLD = 100;

/** Nombre d'offres affichées par page dans le tableau « Toutes les offres ». */
const PAGE_SIZE = 50;

/** Nombre d'éléments listés dans le résumé (destinations, fournisseurs, offres). */
const TOP_N = 5;

/** Largeur (€) d'une tranche de l'histogramme des prix. */
const HIST_STEP = 5;

/**
 * Noms de colonnes acceptés à l'import (déjà normalisés : minuscules, sans accent)
 * associés au nom interne. Mêmes règles que esim/config.py.
 */
const ALIASES = {
  fournisseur: "provider", operateur: "provider",
  offre: "product_name", nom: "product_name", name: "product_name",
  pays: "country_name", destination: "country_name", country: "country_name",
  data: "data_display", volume: "data_display", data_go: "data_gb", go: "data_gb",
  validite: "validity_days", validite_jours: "validity_days", validity: "validity_days",
  duree: "validity_days",
  prix: "price", prix_eur: "price",
  reseau: "network", recharge: "top_up", devise: "currency", illimite: "is_unlimited",
};

/** Valeurs texte considérées comme « vrai » (colonnes recharge et illimité). */
const TRUE_WORDS = ["oui", "yes", "true", "1", "vrai"];

/** Reconnaît un forfait illimité dans un libellé (« Illimité », « unlimited », « ∞ »). */
const UNLIMITED_RE = /illimit|unlimited|∞/i;

/** Extrait un volume et son unité : groupe 1 = nombre, groupe 2 = unité (Go par défaut). */
const VOLUME_RE = /(\d+(?:[.,]\d+)?)\s*(to|tb|go|gb|mo|mb)?/i;

/** Facteur de conversion de chaque unité de volume vers le Go. */
const UNIT_TO_GB = { to: 1000, tb: 1000, go: 1, gb: 1, mo: 0.001, mb: 0.001 };

/** Séparateurs de colonnes essayés pour lire un CSV importé. */
const CSV_DELIMITERS = [",", ";", "\t", "|"];

/** Rampe bleue (clair → foncé) des graphiques de magnitude (nombre d'offres, volume). */
const RAMP = ["#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab",
  "#184f95"];

/** Réglages Plotly communs : pas de barre d'outils, graphiques redimensionnés automatiquement. */
const PLOT_CONFIG = { displayModeBar: false, responsive: true };

/** Fin d'infobulle commune à tous les graphiques (invitation au clic). */
const CLICK_HINT = "<br><i>Clique pour le résumé</i><extra></extra>";

/* ---------- Recherche multicritère ---------- */

/** Unité écrite après un nombre → champ de l'offre comparé (« 20€ », « 5go », « 30j »). */
const UNIT_FIELD = {
  "€": "price", eur: "price", euro: "price", euros: "price",
  go: "gb", gb: "gb", mo: "gb",
  j: "validity", jour: "validity", jours: "validity",
};

/** Préfixe écrit avant un nombre → champ comparé (« prix<20 », « data>=5 », « validite=30 »). */
const PREFIX_FIELD = {
  prix: "price", price: "price", data: "gb", volume: "gb", validite: "validity", duree: "validity",
};

/** Libellé et suffixe d'unité affichés pour chaque champ numérique. */
const FIELD_LABEL = { price: ["Prix", " €"], gb: ["Data", " Go"], validity: ["Validité", " j"] };

/**
 * Mots-clés de la recherche : libellé affiché, champ de l'offre et valeur attendue
 * (comparée après normalisation : true → "true", « 4G » → "4g").
 */
const KEYWORDS = {
  illimite: { label: "Illimité", field: "unlimited", value: "true" },
  illimites: { label: "Illimité", field: "unlimited", value: "true" },
  unlimited: { label: "Illimité", field: "unlimited", value: "true" },
  limite: { label: "Volume limité", field: "unlimited", value: "false" },
  recharge: { label: "Rechargeable", field: "topUp", value: "true" },
  rechargeable: { label: "Rechargeable", field: "topUp", value: "true" },
  "4g": { label: "Réseau 4G", field: "network", value: "4g" },
  "5g": { label: "Réseau 5G", field: "network", value: "5g" },
};

/** Symbole affiché pour chaque opérateur de comparaison. */
const OP_LABEL = { "<": "<", "<=": "≤", ">": ">", ">=": "≥", "=": "=" };

/**
 * Forme d'un critère numérique : préfixe, opérateur, nombre, borne haute, unité.
 * Ex. « prix<20 », « >=5go », « 10-30€ », « 30j ».
 */
const TERM_RE = new RegExp("^(?:([a-z]+)[:=]?)?(<=|>=|<|>|=)?(\\d+(?:[.,]\\d+)?)"
  + "(?:-(\\d+(?:[.,]\\d+)?))?(€|[a-z]+)?$");

/** Découpe la recherche en mots, en gardant ensemble un texte entre guillemets. */
const TOKEN_RE = /-?"[^"]*"|\S+/g;

/** Début de texte qu'Excel exécuterait comme une formule (neutralisé dans les exports CSV). */
const CSV_FORMULA_RE = /^[=+\-@\t\r]/;

/* ---------- Tableaux ---------- */

/** Colonnes cliquables (filtre par valeur) et leur nom affiché dans les pastilles. */
const PICK_FIELDS = {
  provider: "Fournisseur", country: "Destination", display: "Data", validity: "Validité",
  network: "Réseau", topUp: "Recharge",
};

/**
 * Colonnes du tableau « Toutes les offres » :
 * key = champ affiché, label = titre, sortBy = champ de tri s'il diffère,
 * numeric = aligné à droite.
 */
const OFFER_COLUMNS = [
  { key: "provider", label: "Fournisseur" },
  { key: "name", label: "Offre" },
  { key: "country", label: "Destination" },
  { key: "display", label: "Data", sortBy: "gb" },
  { key: "validity", label: "Validité", numeric: true },
  { key: "price", label: "Prix", numeric: true },
  { key: "perGb", label: "€/Go", numeric: true },
  { key: "network", label: "Réseau" },
  { key: "topUp", label: "Recharge" },
];

/** Choix du filtre « Forfait » : [valeur, libellé]. */
const KIND_OPTIONS = [["all", "Tous"], ["limited", "Volume limité"], ["unlimited", "Illimité"]];

/** Choix du mode d'import : [valeur, libellé]. */
const IMPORT_MODE_OPTIONS = [["append", "Ajouter"], ["replace", "Remplacer"]];

/** Fichiers de l'API statique publiée avec la page : [chemin, description]. */
const API_LINKS = [
  ["api/offers.json", "toutes les offres (JSON)"],
  ["api/offers.csv", "toutes les offres (CSV)"],
  ["api/stats.json", "les 6 statistiques + KPIs bonus"],
  ["api/providers.json", "répartition par fournisseur"],
  ["api/index.json", "description de l'API"],
];
