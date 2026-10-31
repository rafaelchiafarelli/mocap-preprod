## 2. The neutral fixture film root

- **Depends on:** 1
- **Contract:** `tests/fixtures/film/`, a film root with no film
  material, built from `mocap-contracts/fixtures/` and the writer's neutral
  sample: `film.json`, `script.fountain`, a few bible items in each map,
  `bible/scene-index.json`, two change sets, an annotation with a shot,
  `settings/front-matter.json`, and a stub `analysis/` (readiness report,
  brief and worklist with neutral task ids). Every JSON file reads with
  `mocap_contracts`.
- **Tests:** every record reads; scene numbers and ids used across files
  resolve
