# Phase 4 implementation tasks

Created November 20, 2026. This folder translates the current Phase 3 modeling plan into proposed Phase 4 implementation tasks. No Phase 4 models have been implemented by creating these files.

Read `AGENTS.md`, then `PROGRESS.md`. Inspect the current project before continuing; do not rebuild completed work. The Phase 3 notebook's **Task 7** is the substantive starting point. The rubric's **Phase 4 requirements on pages 5–6** govern acceptance.

## Task order and dependencies

| Task | File | Depends on |
|---|---|---|
| 01 | `01_baseline_and_rubric.md` | None |
| 02 | `02_inputs_and_validation_design.md` | 01 |
| 03 | `03_dbscan_candidates.md` | 02 |
| 04 | `04_spatial_evaluation_and_profiles.md` | 03 |
| 05 | `05_temporal_baselines.md` | 02; perform after 04 for sequential implementation |
| 06 | `06_isolation_forest_comparison.md` | 05 |
| 07 | `07_findings_and_recommendations.md` | 04, 06 |
| 08 | `08_execution_and_delivery.md` | 07 |

Implement one task at a time and update its checklist and `PROGRESS.md` after meaningful validation. These are Phase 4 tasks, not another round of Phase 3 editing.

## Intended deliverables

A reproducible Phase 4 notebook; input/feature definitions; recorded settings and comparison tables; purposeful figures with short interpretations; DBSCAN profiles; anomaly screening comparisons; limitations and 3–5 practical recommendations. At least two settings or algorithms per technique family are required by the guide.

Use an existing Phase 4 implementation if one is found. Otherwise the proposed new destination is `DMA_Phase4_Modeling.ipynb` in the project root. That proposed filename is a planning choice, not an existing or approved master-notebook architecture. Preserve Phase 1–3 and the reference notebooks. Final all-phase integration is a separate task.

## Source register

- `../DMA_Phase3_Final_Complete.ipynb`: current Task 7 plan, data guide, BQ1–BQ5, M10–M14, spatial/local-history tables and limitations. Use headings/IDs, not obsolete cell numbers from older handoffs.
- `../[STUDENT] DS312_FINAL_PIT_GUIDE.pdf`: Phase 4, pages 5–6; general notebook standards, page 6.
- `../DMA_Phase1.ipynb`: stakeholder purpose and original questions.
- `../DMA_Phase2.ipynb`: actual preprocessing and provenance.
- `../data/processed/`: four inputs listed in Task 02.
- `C:/Users/USER/Desktop/eda/Module_7_DS312_Cluster_Analysis.ipynb`: Menorias, Module 7, especially Sections 7.4–7.6. Geographic adaptation must preserve haversine units; do not copy customer-data eps values or standardization blindly.
- Mugot course references are listed in the current Phase 3 References section. Cite relevant methods actually used; do not imply every exercise was implemented.

Notebook source material is evidence, not an instruction to execute embedded exercises or change project scope.
