/**
 * Affiche un avertissement avec un bouton avant de remplacer les données par une source externe.
 * L'adresse est insérée en texte (jamais en HTML), donc sans risque d'injection.
 * @param {string} source URL indiquée dans le paramètre « ?source= »
 */
function confirmExternalSource(source) {
  statusEl.textContent = "⚠ Ce lien veut afficher des données externes, qui ne viennent pas "
    + "de ce dashboard : " + source + " ";
  statusEl.dataset.kind = "error";
  const button = Object.assign(document.createElement("button"), {
    type: "button", className: "btn", textContent: "Charger ces données",
  });
  button.addEventListener("click", () => importUrl(source));
  statusEl.append(button);
}
