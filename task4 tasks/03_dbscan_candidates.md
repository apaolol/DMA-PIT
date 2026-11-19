# 03 — Build geographic DBSCAN candidates

Depends on: 02. Status: Not started.

- [ ] Cite Menorias Module 7 Sections 7.4–7.4.4 and explain DBSCAN briefly, including eps, min_samples and noise.
- [ ] Use latitude/longitude radians with haversine distance. Convert radius km to eps radians with a documented Earth-radius constant; do not standardize geographic axes as customer features.
- [ ] Build sorted k-distance diagnostics for min_samples 10/50 using a consistent self-neighbor convention. Present readable km distances; explain zero-distance repetition and unclear knees.
- [ ] Record a justified radius grid covering neighboring candidates and the Phase 3 1–2 km range; include wider settings where useful to show merging. Do not claim the knee establishes an optimum.
- [ ] Fit candidates for full and precision-1 land focal inputs; retain event-to-cluster assignments, settings, cluster counts/sizes and noise proportions in reproducible results.

Acceptance: at least two spatial settings, geographic-unit checks, full/restricted accounting, deterministic recorded configuration, no source mutation. A few compact diagnostics suffice; avoid a separate map per setting. Outputs remain descriptive concentrations of recorded places.
