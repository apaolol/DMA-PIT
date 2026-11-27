# 02 â€” Verify inputs and freeze the evaluation design

Depends on: 01. Status: Complete.

- [x] Trace Phase 2 creation and Phase 3 loading of `acled_events_clean.csv`, `acled_gaza_week.csv`, `acled_district_week.csv`, `acled_focal_incidents.csv` under `data/processed/`. Record row unit, scope, key, useful fields and actual shape. Do not join or add these overlapping populations indiscriminately.
- [x] Restore date/boolean/category types explicitly; verify focal logic, spatial membership, radians, keys, complete weeks, positive political denominators and lag eligibility against source code.
- [x] Define spatial input as post-cutoff land focal coordinates; retain full and precision-1 populations with IDs for comparison.
- [x] Define district-week alert timing: after the current completed week, using only eligible earlier history for thresholds/fitting. Exclude the final partial week from scoring; display any excluded weeks explicitly.
- [x] Specify chronological training/tuning/assessment blocks with actual dates after inspecting history availability. Use rolling/expanding earlier-only fits. Include a feature/availability table and how unavailable history is handled.
- [x] Freeze candidate grids, review criteria and settings-selection rules before examining assessment-block results. Disclose that all historical data have already been seen in Phase 3.

Acceptance: data assertions pass; no changes to CSVs; validation design is documented without fictional unseen-test claims. No fitted imputer/scaler/threshold sees later assessment records. Preserve zero-count weeks and undefined shares rather than filling them indiscriminately.
