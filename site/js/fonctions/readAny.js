/**
 * Lit un contenu importé : CSV, liste JSON ou objet {"offers": [...]} (format de l'API).
 * @param {string} text contenu du fichier ou de la réponse
 * @param {string} name nom du fichier (l'extension .json force la lecture JSON)
 * @returns {{records: Object[], total: (number|null|undefined)}} lignes brutes et total annoncé
 * @throws {Error} si le JSON ne contient pas de liste d'offres
 */
function readAny(text, name) {
  text = text.replace(/^﻿/, "");
  if (!/\.json$/i.test(name) && !/^\s*[\[{]/.test(text)) return { records: parseCSV(text) };
  // data : contenu JSON ; total : nombre d'offres annoncé par une API paginée.
  let data = JSON.parse(text);
  let total = null;
  if (data && !Array.isArray(data) && typeof data === "object") {
    total = data.total ?? null;
    data = data.offers ?? data.data ?? data.items;
  }
  if (!Array.isArray(data)) {
    throw new Error('JSON attendu : une liste d\'offres ou {"offers": [...]}');
  }
  return { records: data, total };
}
