# Task 01 - Baseline and evidence inventory

Category: read-only inspection now; backup and implementation tracking after approval.
Depends on: explicit implementation scope before modifying the notebook.

## Actions

- [x] Record SHA-256 hashes of the final notebook, merged reference, Phase 1/2 notebooks, rubric and four processed CSVs.
- [x] When implementation is approved, save a byte-for-byte backup of the final notebook outside its edit destination; never use the merged reference as the backup.
- [x] Inventory cell IDs, original positions, types, source hashes, execution counts and output hashes.
- [x] Confirm the baseline: 184 cells, 69 code cells, 30 saved figures. Investigate differences rather than assuming the audit is still current.
- [x] Identify protected interpretation paragraphs, including 'Result', 'Meaning', 'Limit', conclusions, handoff findings, BQ answers and hard-coded result registers.
- [x] Create a change log listing each proposed change, category A/B/C/D, exact approved scope, before/after location and validation.
- [x] Map each saved figure and table to its code cell, input dataframe, CSV, filters, denominator and derivations.
- [x] Do not execute notebook code during this inventory. Inspect saved outputs and independently read files if necessary.

## Inputs confirmed during audit

| CSV | Shape | Core scope |
|---|---|---|
| acled_events_clean.csv | 26,664 x 43 | All Gaza-coded events, 2022-01-01 through 2025-09-30 |
| acled_gaza_week.csv | 104 x 13 | Post-cutoff Gaza-wide weeks; 103 complete |
| acled_district_week.csv | 520 x 14 | Five known districts x 104 weeks |
| acled_focal_incidents.csv | 10,583 x 45 | Post-cutoff land focal incidents |

The audit independently verified source fields against the raw Gaza subset, raw manifest hash, focal and political flags, log1p fatalities, fatality flag, spatial IDs/radians, weekly counts and lag construction. Recheck if hashes differ.

## Acceptance

A stable inventory lets later work distinguish authorized markdown changes from changes to code, output, substantive text or references. No notebook content is modified by inventory work.

## Implementation progress - November 19, 2026

Completed and verified. Astra had already created the immutable notebook backup, baseline hashes, cell inventory and an unexecuted revision builder. The final notebook is still byte-identical to that backup; all reference/data hashes match. Added `implementation/evidence_inventory.json` with cell source, interpretation/result markers and saved-output types. Detailed plot/table provenance remains in Tasks 03/04/07 and the approved audit. No notebook cells were executed. See `implementation/PROGRESS.md` for authorization and next work.
