/*
 * Démarrage de la page : branchement des contrôles puis premier affichage.
 * L'ordre compte : le thème avant le premier rendu, les contrôles avant refreshControls.
 */
applySavedTheme();
initControls();
bindPriceInputs();
bindResetButton();
bindTableEvents();
bindExportButtons();
bindImportEvents();
bindDragAndDrop();
renderApiLinks();
bindSummaryClose();
bindTheme();
refreshControls();
update();
renderSource();
loadSourceParam();
