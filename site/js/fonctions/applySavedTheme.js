/**
 * Applique le thème (clair ou sombre) mémorisé lors d'une visite précédente, s'il existe.
 */
function applySavedTheme() {
  try {
    const saved = localStorage.getItem("theme");
    if (saved) rootEl.dataset.theme = saved;
  } catch (e) {
    // Stockage indisponible (navigation privée…) : on garde le thème du système.
  }
}
