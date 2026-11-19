# Task 06 - Statistical and numerical corrections

Category: C/D recommendations only under existing restrictions. No implementation without specific authorization.
Depends on: Task 01; coordinate decisions with Tasks 04 and 08.

## Required decision log

For each issue record: existing statement/code, supporting evidence, proposed correction, affected cells/outputs, approval and validation. Never edit a number only in one repeated location.

| Issue | Locations | Verified evidence / proposed review |
|---|---|---|
| Mixed complete/all-week district scope | c75-76 | Complete-week Gaza City 3,411/6,825; Deir El Balah 2,257/4,335 (~52.1%). Prose uses all-week 3,451/6,903 and 2,278/4,361 (52.2%). Align prose to actual plotted population if approved |
| Mixed district-profile totals/share | c155-156, c174 | Complete-week Gaza City 3,411 and 32.2767% (~32.3%); prose/register 3,451/32.4% are all-week. Do not change valid all-week BQ4 total without changing its declared scope |
| Monte Carlo floor formatting | c94, c102-106, figure c103 | Formatter reports p < 0.00001 at attainable floor 1/(99,999+1). Correct reporting of the simulated estimate/resolution; synchronize code, outputs and interpretation only with approval |
| Event-type percentage | c25 versus c24 | 20,276/26,664 = 76.0426%, rounds to 76.0%, not 76.1% |
| Precision-1 Gini | c168, c174-175 versus c162/167 | 0.6049019063 rounds directly to 0.60; saved plot shows 0.60, prose says 0.61. Avoid double rounding |
| DBSCAN 'identical results' | c172 versus c169/171 | 0.25/0.5 km cluster counts agree, but full-subset noise differs; narrow statement to supported agreement |
| Actor attribution ambiguity | c64 versus c63 | Overall focal totals 8,420 air/drone and 1,442 shelling; dominant actor-specific counts are 8,392/1,436. Clarify what each count describes |
| History-policy mismatch | c118/137 | Uses raw complete-week focal counts, including North Gaza zero-political weeks 2025-02-01/08. Phase 2 history excludes these. Decide whether to retain and disclose or change baseline; don't silently mask/change alerts |
| MAD floor applied to proportions | c118/133 | mad_floor=1.0 on 0-1 shares prevents ±3.5 flags. Review separate scale-appropriate handling; count-plot findings are distinct |
| Seasonality strength and absent caption | c148-149, c174-175 | No direct interpretation; limited calendar comparison does not establish absence of seasonality or justify categorical exclusion of seasonal terms |
| Independence wording | c86/98 and test interpretations | Large expected counts address sparse-cell approximation, not independence of events. Keep exploratory dependence caveat adjacent to conclusions |
| Mix-change overstatement | c100 | Within-type rise shows the overall difference is not solely composition; does not prove composition has no contribution |
| Cramer's V wording | c77-79 and sparse table labels | Sparse cells can inflate uncorrected V; not an unconditional guaranteed effect. Avoid universal strength thresholds |
| Risk-ratio interpretation | c96-97 | Ratio describes focal classification among recorded political events, not civilian population risk |
| Quality checks overclaim | c139-140 | Unique IDs do not prove no event duplication; rough bounding box does not prove correct locations; low imprecision prevalence alone does not establish weekly stability |
| ACF/seasonality inference | c151-152, c174-175 | Approximate white-noise band and short lag window are descriptive; first differences include a lag-1 exception; no formal proof of seasonal absence |
| Gini comparison populations | c162/167 | Full and precision-1 Gini use their own occupied coordinates (101 versus 95). Explain or recommend fixed-support sensitivity; don't silently change denominator |
| Trend p-value display | c142 | Rounding gives 0.000 for very small p-values; clarify these are rounded, dependence-sensitive exploratory values |
| K-means interpretation | c157-161 | Count/share features overlap mathematically; scaling/clustering uses full historical data for description, not predictive validation |

## Modeling safeguards

- Existing anomaly flags are screening outputs, not validated ground-truth labels; avoid circular evaluation of a future detector against them without qualification.
- All explored periods are observed data; do not later call them untouched test data.
- No definitive radius optimality follows from the descriptive DBSCAN grid alone.

## Acceptance

Each issue is either corrected under explicit approval with synchronized evidence, or recorded as unresolved. Do not mark the notebook submission-ready while known substantive contradictions persist. If authorized reruns are needed, first use a controlled working copy and review output changes; never execute the reference notebook.

## Implementation progress

Implemented in the revision candidate using Astra's existing draft. Simulation floor and eligible-history policy corrected; raw policy retained as sensitivity. Static checks passed; final execution and visual validation are tracked in Task 09. Full changes were explicitly authorized by the user.

## Final validation status

Complete. The authorized revision is saved in `DMA_Phase3_Final_Complete.ipynb`. Task 09 verified 56 consecutive code executions, 29 figures, no saved errors/warnings, valid notebook schema and 43 internal-link destinations. Reference/data hashes are unchanged. All figure contact sheets were visually inspected; see `implementation/COMPLETION_REPORT.md`.
