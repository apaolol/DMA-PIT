# Task 04 - Business-question evidence and answers

Category: A for separate evidence blocks/anchors; C for rewriting answers, adding conclusions or correcting claims; D for new supporting tables.
Depends on: Tasks 01-03. Reconcile substantive issues in Task 06 before endorsing affected claims.

## First pass: preserve answer wording

Keep c178-182 verbatim except approved formatting. Add a separate 'Evidence' block to each answer with task, subsection, figure/table description and internal links. Do not cite a whole notebook where a local output exists. Do not imply a plot displays a statistic that only appears in a supporting table.

| Answer | Source and population | Exact evidence |
|---|---|---|
| BQ1, c178 | events_clean; political records by period | Task 2 §3.1 c48 period table and share/rate panels; Task 4 §4.3 c96 test/effects; §4.3.1 c99 intervals and within-type comparison |
| BQ2, c179 | events_clean; focal records, both periods | Task 2 §3.6 c63 sub-event/event-type table and actor/sub-event cross-tab/heatmap; Task 1 §3.8.4 c27 actor tables and c28 Figure 3B |
| BQ3, c180 | focal_incidents; full and precision-1 | Task 5 §7 c162 district and concentration tables; Chart 10 c164 spatial comparison; Chart 11 c167 precision composition/Lorenz curves |
| BQ4, c181 | gaza_week and district_week | Task 2 §4.4 c72 Gaza series; §4.3 c69 district totals/highest-week table and heatmap; §4.6 c78 left Spearman matrix |
| BQ5, c182 | events_clean, with spatial file for optional spatial sensitivity | Task 2 §3.5 c60 precision/period plot and robustness tables; §4.1 c66 period/type table; spatial evidence c162/164/167; settings evidence c169/171 only if discussed |

## Claim-level cautions

### BQ1

- c48 calculates counts x 7 / calendar days. 'Weekly average' is not a mean over weekly CSV rows. Correcting wording needs C approval.
- Distinguish descriptive counts/shares from inferential test results and recording limitations.

### BQ2

- 92.5% is the share of focal events that are Explosions, not the focal prevalence within Explosions. c51 is not a direct plot of this percentage.
- Use c63's focal cross-tab for composition and c27/c63 for actors.
- State incident-note verification of actor roles is deferred if revising content; no legal/causal role claims.

### BQ3

- Exact district/top-ten percentages are in c162, not directly on the maps.
- Precision filtering changes population; top-ten coordinates may be re-ranked within each subset.
- Do not import the incorrect 0.61 Gini from other prose into this answer.

### BQ4

- Existing 3,451 Gaza City total is from all district weeks in c69. Do not cite complete-week c155, which gives 3,411.
- Existing answer lacks the most direct local-history evidence: Task 5 §4.2 district check c137-138 (95 scored weeks per district, 50/475 flagged overall, highest upward-score records).
- Adding local anomaly findings needs C approval and acknowledgment of recovery effects/history-policy issues.
- Spearman 0.70/0.66 in c78 is not ACF 0.76 in c151.

### BQ5

- Existing '(Chart 5)' supports precision shares only, not all claims in the paragraph.
- c66 provides counts from which 61.9%/92.6% focal composition can be derived, but its plotted composition uses all political records. State the calculation if approved rather than mislabeling the plot.
- District rankings within each precision level and pre-cutoff North Gaza/Gaza City counts lack a directly displayed matching table. They were checked against CSVs during audit; flag the presentation gap.
- A new supporting table requires D approval. Adding/removing claims requires C approval.
- Broader cohort, baseline, geography, reporting and temporal spatial sensitivity remain only partially addressed. State limits rather than claiming complete robustness.

## Optional content pass, only with C approval

Use a consistent structure: direct answer; supporting evidence; qualification/unanswered part. Tie BQ4 to local anomalies; explain the revised Gaza-only questions and deferred Phase 1 elements. Do not add unsupported interpretations or weaken existing caveats.

## Acceptance

Every numerical claim has a directly supporting output or an explicit derivation/evidence-gap note. All links resolve to the correct population and denominator. A generic source list and ambiguous chart numbers no longer substitute for evidence.

## Implementation progress

Implemented in the revision candidate using Astra's existing draft. All BQ evidence destinations resolve; direct BQ5 tables supplied. Static checks passed; final execution and visual validation are tracked in Task 09. Full changes were explicitly authorized by the user.

## Final validation status

Complete. The authorized revision is saved in `DMA_Phase3_Final_Complete.ipynb`. Task 09 verified 56 consecutive code executions, 29 figures, no saved errors/warnings, valid notebook schema and 43 internal-link destinations. Reference/data hashes are unchanged. All figure contact sheets were visually inspected; see `implementation/COMPLETION_REPORT.md`.
