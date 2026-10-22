/**
 * Branche le clic sur les barres d'un graphique (une seule fois par graphique).
 * Un graphique jamais affiché n'a pas encore l'API d'événements Plotly : on réessaiera.
 * @param {string} id identifiant du graphique
 * @param {Function} handler fonction appelée avec le point cliqué
 */
function bindChartClick(id, handler) {
  const chart = document.getElementById(id);
  if (chart._clickBound || !chart.on) return;
  chart.on("plotly_click", event => {
    const point = event.points && event.points[0];
    if (point) handler(point);
  });
  chart._clickBound = true;
}
