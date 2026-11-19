# Phase 3 revision completion report

All nine tasks are complete. The user authorized code, output, plot and interpretation revisions and validation. The original audit notebook remains recoverable in `DMA_Phase3_Final_Complete.original.ipynb`.

## Delivered notebook

`C:\Users\USER\Desktop\DMA PIT\DMA_Phase3_Final_Complete.ipynb`

- 161 cells (previously 184); 56 executed code cells (previously 69).
- 29 figure groups (previously 30), with additional duplicate panels removed and unique analytical contributions retained.
- One four-CSV loader and one union of snapshot checks.
- Plain-language definitions, source scopes, logs, history eligibility and denominators before analysis.
- No mid-report handoff sections or full bibliographies; one final reference section.
- BQ1-BQ5 rewritten with exact internal evidence links and a new computed BQ5 supporting table.
- Seven closing insights and a two-family modeling plan, clearly distinguished from completed predictive validation.

## Corrections and analytical decisions

- Period rate panel retained; redundant period-share panel consolidated into H1.
- Event-type prevalence figure consolidated into H2 with intervals/residuals; composition retained separately.
- Repeated positive-fatality ECDF removed while the top-record review remains.
- Imbalance plot focuses on minority counts, using symlog to represent zero honestly.
- Complete-week district prose corrected to the actual plotted totals; all-week totals explicitly named where used.
- Event-type percentage corrected to 76.0%, precision-1 Gini to 0.60, and actor-specific sub-event counts distinguished from overall counts.
- Monte Carlo reports p=0.00001 at the simulation floor, consistently in code, outputs and prose.
- Local anomaly screening now uses Phase 2 eligible current/history values: 48/465 (10.3%). Original complete-count policy retained as sensitivity: 50/475 (10.5%).
- Proportional MAD uses its own scale, with flat windows unscored: 11 trailing share flags, zero whole-period share flags.
- Statistical/seasonal/quality overclaims qualified; missing seasonality interpretation supplied.
- District plot legend overlap corrected; pandas warning-producing operations updated.
- All contributions remain in the original backup; repeated handoff/register prose was consolidated into reader-facing answers and closing insights under the authorized scope.

## Validation

- Executed all 56 code cells in one fresh local kernel, consecutively and without errors.
- No stderr warning outputs saved in the revised notebook.
- All snapshot/feature checks embedded in the notebook passed, including dates, key uniqueness, focal rule, fatality logs/flags, spatial membership/radians and eligible lag construction.
- Notebook schema validated; 29 saved PNG figures verified.
- All 43 referenced internal destinations exist; anchor IDs are unique.
- All 29 figures inspected using five contact sheets; changed panels and district legend reviewed.
- HTML export generated for review in `revision.preview.html`; an initial local-template export error was fixed without rerunning already-passing analytical cells.
- Final source/data hash comparison passed: merged reference, Phase 1, Phase 2, rubric, manifest/raw/processed data remain unchanged.
- No code writes a CSV.

## Limits retained in the report

No independent anomaly ground truth, verified actor-role conclusions, demonstrated annual seasonality, complete reporting-bias sensitivity or untouched predictive test data is claimed. Future modeling and documentary review remain proposed next work.

## Plot consolidation - November 20, 2026

Completed the user-authorized consolidation using existing plots only. Main report now has 14 figure groups (M1-M14), with 13 supporting figures (A1-A13) in an appendix before References. Five composites reuse the original drawing code for period rates/shares, weekly anomaly counts/share, calendar/ACF, district heatmap/variability, and spatial maps/Lorenz curves. Supporting figures are rendered at their original computation points and displayed later to preserve variable state. No new statistical analyses were introduced.

Interpretations, main figure register, BQ/closing-insight links and explicit non-focal definition were updated. Added a short explanation of the univariate distribution choices. Shared axes retained for spatial precision comparisons, weekly timelines and ACF panels.

Validation: all 74 code cells executed sequentially, no saved error or warning outputs; 14 main and 13 appendix PNG outputs verified. All 55 internal destinations resolve. Plot previews inspected, including all five full-size composites; spatial/ACF shared-scale issues found in QA were corrected and rerun. Reference/data hashes unchanged. Tables retain their analysis results; missing saved imbalance-table output was regenerated. Final destination reopened and verified byte-identical to `consolidation.executed.ipynb`.

Backup: `before_plot_consolidation.ipynb`. Map: `plot_consolidation_map.json`. Results: `consolidation_validation.json`. HTML review: `consolidation.preview.html`. The complete notebook has 206 cells because appendix displays and their interpretations are retained, while the main figure count is reduced from 29 to 14.

## Navigation and local Task 1 table interpretations - November 20, 2026

Replaced custom HTML fragment targets with the notebook renderer's native heading IDs throughout the document, including appendix/source/back links. Method references now have actual headings. Verified all 110 rendered internal links have one exact heading target; Appendix A4 resolves to A4 - Event-type composition by period. This verifies rendered HTML destinations; a particular editor's navigation behavior is not directly exercised.

Split multi-table Task 1 code cells at their existing display statements, preserving calculation order, and unrolled the three flag displays. Added 28 short markdown interpretations, each immediately after exactly one displayed table; removed the old combined profile/text interpretation paragraphs. All 78 table outputs match the previous version's displayed values, and all 27 PNG figure outputs are byte-identical. No data or analysis values changed.

Executed all code cells successfully, validated notebook schema, checked no saved error/warning outputs, verified reference/data hashes, and saved/reopened the exact destination. Backup: before_navigation_table_fix.ipynb. Details: navigation_validation.json, navigation_mapping.json; HTML review: navigation.preview.html.

## VS Code navigation correction - November 20, 2026

Reproduced the A4 misnavigation in the actual VS Code notebook: valid HTML fragments scrolled near the limitations section. The previous exported-HTML validation did not establish editor click behavior. Replaced figure/calculation links with VS Code native links to unique saved execution numbers. Prose-only navigation references are now named text, with instructions to use the notebook Outline. These links are VS Code-specific and depend on saved execution numbers; rerunning cells out of order may require the Outline instead.

Verified A4 by clicking from section 2.6 to the actual A4 figure (cell 227, execution 89). Verified the A8 appendix return link opens its original quarter calculations/table (cell 154, execution 63). All direct links resolve to unique existing saved code cells; notebook schema validated. All code cells, outputs, and execution counts are exactly unchanged from before_vscode_link_fix.ipynb. No rerun needed for markdown-only changes. Link inventory: vscode_navigation_validation.json. Implementation: fix_vscode_navigation.py.
