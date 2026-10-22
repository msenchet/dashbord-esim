/**
 * Branche les interactions des tableaux : clic sur une valeur ou une pastille, tri par en-tête,
 * saisie dans la recherche, pages précédente et suivante.
 */
function bindTableEvents() {
  document.addEventListener("click", e => {
    const cell = e.target.closest(".cell-pick, .pick[data-f]");
    if (cell) {
      togglePick(cell.dataset.f, cell.dataset.v);
      if (cell.closest("#t-providers")) {
        document.getElementById("offers-title")
          .scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }
    const queryChip = e.target.closest(".pick.query");
    if (queryChip) return removeQueryToken(queryChip.dataset.raw);
    if (e.target.id === "clear-picks") { state.picks = {}; setSearch(""); }
  });
  document.getElementById("t-offers").addEventListener("click", e => {
    const th = e.target.closest("th[data-k]");
    if (!th) return;
    state.sortDir = state.sortKey === th.dataset.k ? -state.sortDir : 1;
    state.sortKey = th.dataset.k;
    state.page = 0;
    renderOffers(current);
  });
  searchEl.addEventListener("input", e => {
    state.search = e.target.value;
    state.page = 0;
    renderOffers(current);
  });
  document.getElementById("prev").addEventListener("click", () => {
    state.page--;
    renderOffers(current);
  });
  document.getElementById("next").addEventListener("click", () => {
    state.page++;
    renderOffers(current);
  });
}
