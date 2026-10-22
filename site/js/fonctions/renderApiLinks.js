/**
 * Affiche les adresses complètes de l'API statique publiée avec la page.
 */
function renderApiLinks() {
  document.getElementById("api-links").innerHTML = API_LINKS.map(([path, description]) => {
    const url = new URL(path, location.href).href;
    return `<li><a href="${esc(url)}"><code>${esc(url)}</code></a> · ${description}</li>`;
  }).join("");
}
