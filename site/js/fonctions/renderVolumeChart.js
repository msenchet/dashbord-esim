/**
 * Dessine « Prix médian selon le volume de data » (rampe bleue, illimité en violet).
 * @param {Object[]} rows offres affichées
 */
function renderVolumeChart(rows) {
  // byVolume : prix des offres par volume (Infinity = illimité ; volumes inconnus ignorés).
  const byVolume = new Map();
  rows.forEach(o => {
    const key = o.unlimited ? Infinity : o.gb;
    if (key === null) return;
    if (!byVolume.has(key)) byVolume.set(key, []);
    byVolume.get(key).push(o.price);
  });
  const volumes = [...byVolume.keys()].sort((a, b) => a - b);
  const finite = volumes.filter(k => k !== Infinity).length;
  const trace = withColors({
    type: "bar",
    x: volumes.map(k => k === Infinity ? "Illimité" : k.toLocaleString("fr-FR") + " Go"),
    y: volumes.map(k => median(byVolume.get(k))),
    customdata: volumes.map(k => [byVolume.get(k).length, k === Infinity ? "unlimited" : k,
      `Prix médian : ${fmtEur(median(byVolume.get(k)))}<br>`
      + `${fmtInt(byVolume.get(k).length)} offres`]),
    hovertemplate: "<b>%{x}</b><br>%{customdata[2]}" + CLICK_HINT,
  }, volumes.map((k, i) => k === Infinity ? css("--c-violet")
    : rampColor(finite > 1 ? i / (finite - 1) : 1)));
  Plotly.react("c-volume", [trace], baseLayout({
    xaxis: { ...baseLayout().xaxis, type: "category", showgrid: false },
    yaxis: { ...baseLayout().yaxis, title: { text: "Prix médian (€)" } },
  }), PLOT_CONFIG);
}
