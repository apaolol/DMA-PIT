# Task 03 - Data provenance and reader definitions

Category: A for separate explanatory markdown; C if changing interpretations; D for loader changes.
Depends on: Tasks 01-02.

## Opening context

- [x] Explain that Phase 1 included Gaza and West Bank, but Phase 2 narrowed the study to Gaza after consultation.
- [x] State snapshot coverage, observation unit and the research decision: prioritizing places/periods/incident groups for documentary review.
- [x] Explain the exact focal rule before Task 1: civilian-targeting flag plus exact 'Civilians (Palestine)' label in either actor field.
- [x] Define political violence as an exact token in semicolon-separated disorder labels, not an assumed event-type list.
- [x] Identify all four CSV filenames, row units, scopes and notebook aliases.

## Inherited variables versus Phase 3 derivations

| Variable/decision | Origin | Reader explanation |
|---|---|---|
| fatalities_log1p | Phase 2 c50; events_clean and inherited in focal_incidents | Natural log(1 + reported event fatalities); reduces tail compression problems while keeping zero at zero; Phase 3 c20 displays it |
| high_fatalities_review | Phase 2 c43; event/spatial outputs | Fatalities >23, from full Palestine export P99; Gaza-only P99 is 39; review flag, not deletion or invalidity |
| period, month_start, week_start | Phase 2 c48-50 | Cutoff includes Oct 7 in later period; calendar months; Saturday-Friday weeks |
| focal_share | Phase 2 weekly outputs | Focal/political events in matching area/week; undefined with zero denominator |
| complete_week | Phase 2 weekly outputs | Week ends within Sep 30, 2025 coverage; final start Sep 27 is partial |
| history_eligible | Phase 2 c63; both weekly CSVs | Complete week AND positive political count |
| focal_count_for_history | Phase 2 c63 | Focal count masked where history is ineligible |
| previous_week_focal | Phase 2 c65 | Preceding eligible calendar week's count; not current count |
| previous_four_weeks_focal | Phase 2 c65 | SUM of preceding four calendar weeks after shift; missing if history insufficient/ineligible |
| district_missing | Phase 2 clean master | Four events retained in Gaza totals, excluded from district aggregation; three are focal |
| coastal_location / land_spatial_eligible | Phase 2 c55 | Location starts 'Coast of '; spatial eligibility is post-cutoff focal and not coast-coded |
| latitude_rad, longitude_rad | Phase 2 c69; spatial CSV | Coordinates converted to radians; c169 instead recomputes radians from degrees |
| Weekly log-counts | Phase 3 c157, from gaza_week | log1p(focal_events), log1p(political_events), plus unlogged focal_share; StandardScaler then K-means; not saved Phase 2 log-count columns |
| share_4w | Phase 3 c75, district_week | Current and prior three weeks' focal sum / matching political sum |
| share4 | Phase 3 c155, district_week | District four-week focal sum / all known districts' four-week focal sum; NOT political-denominator focal share |
| modified z-scores | Phase 3 c118/133/137 | Global or preceding-eight-week median/MAD screening; not inherited Phase 2 features |

## Scope reconciliations

- 10,714 all-period focal events; 10,651 post-cutoff Gaza focal events.
- District-week focal total 10,648: excludes three focal events with missing districts.
- Land spatial total 10,583: excludes 68 post-cutoff coast-coded focal events.
- 7,576 precision-1 spatial incidents on 95 coordinates versus 10,583 on 101 in full spatial subset.
- All Gaza coast-coded events: 701. Do not confuse these with 68 spatial exclusions or 27 separately coded maritime raw records.
- Explain structural missingness, retained source labels and empty admin3 removal; no actor imputation, fatality trimming or coordinate deduplication.

## Local notes needed

- Before c20: distinguish log1p values, logarithmic axes and log color scales.
- Before c78: explain eligible lag sums and pairwise sample sizes.
- Before c137: disclose that current anomaly code uses raw complete-week counts, not history-eligible counts; see Task 06.
- Before c144: month of week start differs from event-calendar-month aggregation in c38.
- Before c155: define the changed share denominator and coefficient of variation.
- Before c157: explain K-means inputs, scaling, silhouette and mathematical dependence among counts/share.
- Before c162-171: explain occupied-coordinate populations, Gini/Lorenz, haversine radius and min_samples; verify precision-code meanings from supplied documentation rather than inventing definitions.

## Acceptance

A reader can understand each important variable without opening Phase 2. Every derived quantity states its formula/meaning, CSV origin or Phase 3 creation point, population and analytical purpose.

## Implementation progress

Implemented in the revision candidate using Astra's existing draft. Four CSV sources, logs, history and denominator explanations present. Static checks passed; final execution and visual validation are tracked in Task 09. Full changes were explicitly authorized by the user.

## Final validation status

Complete. The authorized revision is saved in `DMA_Phase3_Final_Complete.ipynb`. Task 09 verified 56 consecutive code executions, 29 figures, no saved errors/warnings, valid notebook schema and 43 internal-link destinations. Reference/data hashes are unchanged. All figure contact sheets were visually inspected; see `implementation/COMPLETION_REPORT.md`.
