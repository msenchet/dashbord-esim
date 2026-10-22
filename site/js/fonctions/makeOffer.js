/**
 * Complète une offre avec ses champs calculés : libellé de volume, prix au Go, texte de recherche.
 * @param {Object} offer offre (sku, provider, country, code, name, gb, unlimited, validity,
 *   price, network, topUp, currency, display facultatif) ; elle est modifiée
 * @returns {Object} la même offre, complétée
 */
function makeOffer(offer) {
  offer.unlimited = !!offer.unlimited;
  if (offer.unlimited) offer.gb = null;
  offer.display = offer.display
    || (offer.unlimited ? "Illimité" : offer.gb === null ? "N/C" : offer.gb + " Go");
  // perGb : prix au Go, null pour l'illimité ou un volume nul/inconnu.
  offer.perGb = offer.gb > 0 ? offer.price / offer.gb : null;
  // _hay : texte normalisé dans lequel la recherche cherche les mots tapés.
  offer._hay = norm([offer.provider, offer.name, offer.country, offer.code, offer.network,
    offer.display, offer.sku].join(" "));
  return offer;
}
