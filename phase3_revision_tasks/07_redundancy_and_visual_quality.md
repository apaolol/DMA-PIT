# Task 07 - Redundancy and visual quality

Category: D recommendations only. Removing plots/tables/analysis is prohibited unless the user explicitly changes that restriction.
Depends on: Tasks 01, 04 and 06. Preserve contributor work and unique analytical content.

## Highest-value consolidation proposals

| Cells | Recommendation | Unique content to preserve |
|---|---|---|
| c51 versus c103 | Prefer c103 for event-type prevalence | Wilson intervals and residuals; preserve any unique c51 table information |
| c48 left versus c99 left | Consolidate repeated period proportions | c48 right calendar-adjusted weekly rates; c99 intervals |
| c66 right versus c99 right | Consolidate within-type comparison | c66 left period event-type composition; c99 intervals |
| c20 versus c127 left | Optional combined fatality-distribution narrative | Zeros/log1p in c20; conditional positive-fatality scope if retained; c127 right top-record review |
| c122 left versus prior share plots | Consider reducing repeated share display | Minority-count panel, post-cutoff slices and modeling relevance |
| c72 versus c144 | Optional consolidation only | Monthly summary uses month of week start, not event calendar month; count/share interpretation |
| c6/46/92/116 | One union of integrity checks if approved | Unique period-label, duplicate-key, outside-denominator and spatial checks |
| c91 | Redundant preview candidate | Confirm no later analysis depends on this events variable before removal |
| c19/125 | Consolidate repeated fatality summary values | Top-1% concentration and flagged-group details |
| c81/107/174-175/178-182 | Reduce repeated narrative through approved reorganization | Unique caveats, evidence and assigned contributions; no silent deletion |

## Keep distinct

- c28 actor marginals/missingness and c63 actor-sub-event combinations; only focal-actor marginal panel substantially overlaps.
- c72 counts/shares, c135 anomaly rules and c160 cluster timing: same series, different questions.
- c69 counts, c75 within-district focal prevalence and c155 geographic share/variability: different denominators.
- c78 Spearman relationships and c151 multi-lag ACF/first differences.
- c164 maps and c167 quantified concentration/precision composition.
- c106 compact test summary, c157 silhouette comparison and c169 DBSCAN grid.
- Hypothesis contingency tables can legitimately repeat descriptive counts to make tests self-contained.

## Visual defects / improvements

- [x] c155: fix overlapping legend and x-axis label.
- [x] c122: avoid proportion ticks above 100%; do not represent zero minority counts as positive 0.5 without explicit disclosure.
- [x] c24/28/78: inspect dense labels at normal notebook width, not just full-resolution images.
- [x] Wide profiles/registers: assess truncation and horizontal scrolling; keep exact data accessible.
- [x] c78: resolve saved incompatible-fill pandas warning only with code/output permission.
- [x] c148: resolve saved deprecated dayofweek warning only with code/output permission.
- [x] Check plot titles, units, legends, numerator/denominator, partial-week symbols and small-group markings.
- [x] Keep spatial panels on comparable scales; do not invent basemap boundaries.

## Acceptance

No removal without an explicit approved list. Every retained figure has a distinct stated contribution, an evidence link and adjacent interpretation. At least eight purposeful visualizations remain, but eight is a minimum, not a target that justifies losing analysis. Update all citations after consolidation; preserve an approved archive if required.

## Implementation progress

Implemented in the revision candidate using Astra's existing draft. One loader, consolidated checks/comparison panels, distinct remaining figures. Static checks passed; final execution and visual validation are tracked in Task 09. Full changes were explicitly authorized by the user.

## Final validation status

Complete. The authorized revision is saved in `DMA_Phase3_Final_Complete.ipynb`. Task 09 verified 56 consecutive code executions, 29 figures, no saved errors/warnings, valid notebook schema and 43 internal-link destinations. Reference/data hashes are unchanged. All figure contact sheets were visually inspected; see `implementation/COMPLETION_REPORT.md`.
