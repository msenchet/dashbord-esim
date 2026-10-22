/**
 * Crée tous les contrôles de filtre et d'import, branche leurs événements
 * et remplit ceux dont les choix sont fixes (forfait, mode d'import).
 */
function initControls() {
  controls = {
    provider: createMulti("f-provider", "providers", "Tous"),
    country: createMulti("f-country", "countries", "Toutes"),
    validity: createChips("f-validity", state, "validity", { multiple: true, numeric: true }),
    network: createChips("f-network", state, "network", { multiple: true }),
    kind: createChips("f-kind", state, "kind"),
    importMode: createChips("import-mode", imports, "mode"),
  };
  Object.values(controls).forEach(ctrl => {
    if (ctrl.type === "multi") bindMulti(ctrl);
    else bindChips(ctrl);
  });
  setChipOptions(controls.kind, KIND_OPTIONS);
  setChipOptions(controls.importMode, IMPORT_MODE_OPTIONS);
}
