"""Build the approved revision from the immutable audit backup, without executing it."""
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
original = json.loads((WORK / 'DMA_Phase3_Final_Complete.original.ipynb').read_text(encoding='utf-8'))
cells = {i: copy.deepcopy(c) for i, c in enumerate(original['cells'], 1)}

def src(i):
    return ''.join(cells[i]['source'])

def put(i, text):
    cells[i]['source'] = text.strip() + '\n'

def md(i, text):
    assert cells[i]['cell_type'] == 'markdown', i
    put(i, text)

def replace(i, old, new):
    assert old in src(i), (i, old[:100])
    put(i, src(i).replace(old, new))

# Consolidate duplicated setup, redundant prevalence plot and administrative handoffs.
# The immutable backup retains every original contribution and output.
omit = {8,9,11,41,43,44,45,46,50,51,52,81,85,87,88,89,90,91,92,
        108,110,111,112,113,114,115,116,173,174,175,177}

md(1, '''# Phase 3 - Exploratory Data Analysis
## Patterns of Recorded Civilian Targeting in Gaza

**DS312 | Group 7 | Abdula, Aque, Bautro, Budlong, Mashburn, Orano, Pandi, Prollo**

Human-rights documentation teams need to decide which places, periods and incident groups deserve closer investigation. This notebook uses ACLED's recorded events to describe recurring patterns and identify useful starting points for that review; it does not determine intent, responsibility or legal classification.

**Scope.** We study Gaza-coded records from **January 1, 2022 to September 30, 2025**, from the snapshot downloaded October 18, 2026. Phase 1 originally included the West Bank, but Phase 2 narrowed the working study to Gaza after consultation. One row is one coded event record, which can summarize several reported actions; it is not necessarily one attack or one victim.

**How to read this report.** First we explain the data, then describe individual fields, compare groups, test two questions, and examine unusual weeks and geographic concentrations. Readers looking for the answers can go to [Task 6](#task-6); the supporting figures and tables are linked there, followed by the [modeling plan](#task-7).

| Question | What this Phase 3 report answers |
|---|---|
| BQ1 | How do recorded focal counts and shares differ before and from October 7, 2023? |
| BQ2 | Which recorded actors and event types recur among focal events? |
| BQ3 | Where are post-cutoff land focal events concentrated, and what changes with location precision? |
| BQ4 | Which district-weeks have high or sustained activity relative to recent local history? |
| BQ5 | Which findings change with periods, precision restrictions or analytical settings? |

The before/after comparison is descriptive. Temporal and spatial previews use the post-October 7 period; West Bank comparisons, verified actor roles and a full reporting-bias sensitivity study are outside this report.''')

md(2, '''## Reading guide and rubric coverage

| Task | Evidence in this notebook |
|---|---|
| [1. Describe the data](#task-1) | Profiles, distributions and category counts |
| [2. Compare groups](#task-2) | Rates, severity, actor cross-tabs, district/weekly comparisons and association matrices |
| [3. Visualization register](#task-3) | Links to the figures; each figure stays beside its interpretation |
| [4. Test two hypotheses](#task-4) | Period and event-type tests, uncertainty intervals and sensitivity checks |
| [5. Find patterns](#task-5) | Imbalance, unusual values/weeks, trends, calendar patterns, persistence and clusters |
| [6. Answer the questions](#task-6) | BQ1-BQ5 with exact evidence links |
| [7. Plan the next phase](#task-7) | Seven key insights and a proposed clustering/anomaly-detection plan |

**Three quantities that must not be confused:** a **count** is a number of records, a **rate** adjusts a count for time observed, and a **share** divides one group of records by a stated total. Larger counts do not automatically imply larger shares.''')

md(3, '''<a id="data-guide"></a>
## Data guide - what is being counted?

**Focal event** means an ACLED `Civilian targeting` flag **and** the exact label `Civilians (Palestine)` in either actor field. This project rule selects records for review, not all civilian harm. **Political violence** means that exact token appears in `disorder_type`, including records carrying more than one disorder label. Every focal record in this snapshot belongs to that political-violence group.

**Focal share** is focal events divided by political-violence records in the same group, place and period. A blank targeting label is retained in the source and means the flag was not recorded; it is not proof that civilians were unharmed.

### The four Phase 2 outputs

All files are loaded once from `data/processed/`; later sections name their source. These are related views of the same snapshot, not four independent datasets to add together.

| File / dataframe | One row and scope | Used for |
|---|---|---|
| `acled_events_clean.csv` / `master` | One Gaza-coded event; 26,664 rows, 43 columns; both periods | Distributions, period/actor/type comparisons and tests |
| `acled_gaza_week.csv` / `gaza_week` | One Gaza-wide Saturday-Friday week after the cutoff; 104 rows, 13 columns | Counts, shares, history, trends and groups of weeks |
| `acled_district_week.csv` / `district_week` | One known district and week; five districts x 104 weeks; 14 columns | District comparisons and local anomaly screening |
| `acled_focal_incidents.csv` / `incidents` | One post-cutoff land focal event; 10,583 rows, 45 columns | Spatial concentration, precision checks and DBSCAN |

There are **10,714 focal events across both periods**, including **10,651 from October 7 onward**. Four Gaza records lack a district (three focal), so district-week focal counts total **10,648**. The spatial file instead removes **68 post-cutoff focal records** with a location starting `Coast of `, leaving **10,583**; coastal records remain in Gaza-wide and known-district temporal totals. The master contains 701 coast-coded records across all types and periods.

### Preparation a reader needs to know

- Phase 2 retained original actor labels, structural blanks and reported fatality totals, and dropped the entirely empty `admin3` field. It did not impute actors, trim fatalities or delete repeated coordinates.
- `period` splits at **October 7, 2023**, included in the later period: **644 days before, 725 days from the cutoff**. `month_start` groups event calendar months; `week_start` begins on Saturday.
- The weekly calendar keeps zero-count weeks. The last week starts **September 27, 2025**, but observation ends September 30: it is partial, shown where useful and excluded from complete-week comparisons.
- `focal_share` is undefined when the political count is zero. `history_eligible` requires both a complete week and a positive political count; `focal_count_for_history` masks other weeks.
- `previous_week_focal` is the preceding calendar week's eligible count. `previous_four_weeks_focal` is the **sum of the preceding four calendar weeks**, shifted before summing; it is missing if any required history is unavailable. Both features are saved in the two weekly CSVs.
- `geo_precision` and `time_precision` are ordered source quality codes, not distances or measurements. Code 1 is the most precise category; a `geo_precision_1` filter keeps only that category, without making the coordinates exact incident points.

### Logs and review flags

**Inherited event log:** `fatalities_log1p`, saved in the event master and spatial file, is **ln(1 + reported event fatalities)**. Phase 2 created it so a long tail can be displayed more clearly while zero stays zero; for example, a raw count of 0 becomes 0 and 9 becomes about 2.30. It is not a count of civilian deaths.

**Inherited review flag:** `high_fatalities_review` marks fatalities **greater than 23**, the 99th percentile of the full Palestine raw export, not the Gaza-only percentile (39). A flag calls for checking the source; it does not remove or invalidate the record.

**New weekly logs:** the [grouping-of-weeks preview](#t5-week-clusters) creates log1p focal and political counts from `acled_gaza_week.csv` in Phase 3, then standardizes them for K-means. These are different from the inherited fatality log. A logarithmic axis or color scale elsewhere changes only how numbers are displayed.

**Runtime:** run from this project folder with NumPy, pandas, Matplotlib, seaborn, SciPy (with `MonteCarloMethod`) and scikit-learn installed. The setup restores dates and precision categories because CSV files do not preserve these types.''')

# Shared setup: one reader-facing data path and one union of integrity checks.
replace(4, '# Aliases retain the names used by the separate contribution notebooks.', '# Alternate weekly names used by the profiling tables refer to the same loaded data.')
replace(4, 'events, gaza_weekly, district_weekly = master, gaza_week, district_week', 'gaza_weekly, district_weekly = gaza_week, district_week\nBLUE, GREEN, RED, GREY = "#315A7D", "#4B8A78", "#8D3B42", "#8A8F98"\ncutoff = pd.Timestamp("2023-10-07")\npd.set_option("display.max_columns", None)\npd.set_option("display.max_colwidth", 100)')
replace(4, 'COVERAGE_START, COVERAGE_END = master.event_date.min(), master.event_date.max()', 'COVERAGE_START, COVERAGE_END = pd.Timestamp("2022-01-01"), pd.Timestamp("2025-09-30")')
md(5, '''### Check the snapshot before interpreting it

The table below checks the four inputs together, including their dates, scope, keys and totals. A failed check stops the notebook so the fixed narrative cannot silently describe a different dataset.''')
replace(6, '],columns=["Check","Phase 2 reference","Loaded value"])', ''' ("Period labels disagree with event dates",0,int((master.period != np.where(master.event_date.ge(CUTOFF), AFTER, BEFORE)).sum())),
 ("Duplicate event IDs",0,int(master.event_id_cnty.duplicated().sum())),
 ("Duplicate Gaza-week keys",0,int(gaza_week.duplicated(["admin1", "week_start"]).sum())),
 ("Duplicate district-week keys",0,int(district_week.duplicated(["admin2", "week_start"]).sum())),
 ("Focal records outside political violence",0,int((master.focal_event & ~master.political_violence).sum())),
 ("Unexpected political event types",0,int((~political.event_type.isin(EVENT_TYPES)).sum())),
 ("Political event-type count",5,int(political.event_type.nunique())),
 ("Coverage starts",COVERAGE_START,master.event_date.min()),
 ("Coverage ends",COVERAGE_END,master.event_date.max()),
],columns=["Check","Phase 2 reference","Loaded value"])''')
replace(6, 'print("All checks match Phase 2." if checks.Match.all() else "WARNING: reconcile the mismatched inputs before interpreting results.")', 'assert checks.Match.all(), "Input snapshot differs: reconcile the checks before interpreting results."\nprint("All snapshot checks match.")')
put(6, src(6) + '''
assert np.allclose(master.fatalities_log1p, np.log1p(master.fatalities))
assert master.focal_event.equals(master.targeting_flagged & (master.actor1.eq("Civilians (Palestine)") | master.actor2.eq("Civilians (Palestine)")))
assert master.political_violence.equals(master.disorder_type.str.split(";").apply(lambda labels: "Political violence" in [x.strip() for x in labels]))
assert master.high_fatalities_review.equals(master.fatalities.gt(23))
assert incidents.event_id_cnty.tolist() == master.loc[master.land_spatial_eligible, "event_id_cnty"].tolist()
assert np.allclose(incidents[["latitude_rad", "longitude_rad"]], np.radians(incidents[["latitude", "longitude"]]))
for weekly, area in [(gaza_week, "admin1"), (district_week, "admin2")]:
    assert weekly.history_eligible.equals(weekly.complete_week & weekly.political_events.gt(0))
    assert np.allclose(weekly.focal_share, weekly.focal_events / weekly.political_events.where(weekly.political_events.gt(0)), equal_nan=True)
    for _, part in weekly.sort_values("week_start").groupby(area):
        history = part.focal_events.where(part.history_eligible)
        assert np.allclose(part.focal_count_for_history, history, equal_nan=True)
        assert np.allclose(part.previous_week_focal, history.shift(1), equal_nan=True)
        assert np.allclose(part.previous_four_weeks_focal, history.shift(1).rolling(4).sum(), equal_nan=True)
print("Focal rule, fatality log/flag, spatial membership/radians and eligible lag features verified.")
''')

md(7, '''<a id="task-1"></a>
# Task 1 - What does the dataset contain?

Before comparing groups, we establish what a typical record looks like and where the data are uneven. This helps explain why later analyses use counts, medians, explicit denominators and quality restrictions.''')
md(10, '''The event master supplies event-level summaries, the weekly CSVs supply weekly profiles, and the spatial file is used only where stated. Tables provide detail; the short interpretation after each figure gives the main result and its limit.''')
md(12, '''<a id="t1-profiles"></a>
## 1.1 Field profiles and missing information

**Sources:** all columns of the event master and both weekly files; selected spatial/precision columns of the incident file. The tables report missing values and suitable summaries: dates get ranges, categories get their most common label, and numbers get minimum, median, mean and maximum.

The **median** is the middle value; the **mean** is the arithmetic average. A field with one constant value adds no variation here, and a blank value is not automatically a data-entry error.''')
replace(13, 'str(counts.index[0])[:38]', 'str(counts.index[0])')
md(16, '''**Reading the profiles.** The master has 43 columns, including 13 Phase 2 derived fields; four source fields (`iso`, `region`, `country`, `admin1`) are constant in this Gaza extract. Seven columns contain blanks, especially associated actors and the targeting field, while missing weekly history values usually mean the required eligible prior weeks are unavailable.

**Why blanks remain.** A blank second actor coincides with single-sided interaction coding, and an unrecorded targeting label is different from evidence of no civilian involvement; Phase 2 preserved these distinctions rather than filling values.''')
md(17, '''**Text and identifiers.** Event IDs identify records for source review, not model inputs. `notes`, `source` and `tags` provide documentary context; tags may contain multiple semicolon-separated labels, and repeated wording does not by itself establish duplicated events. `timestamp` is the record-update time, not the event date.''')
md(18, '''<a id="t1-fatalities"></a>
## 1.2 Reported fatalities - common values and rare extremes

**Source:** `acled_events_clean.csv`, all 26,664 records. Fatalities are reported totals for the whole event, not confirmed civilian deaths. The table includes percentiles: P90, for example, is the value at or below which 90% of records fall.

**Figure U1.** Left: small counts, with 11 or more grouped together; middle: cumulative share at or below a fatality count (an ECDF), with a symmetric-log axis that can include zero; right: the inherited `fatalities_log1p = ln(1 + fatalities)` field, with a separate log-scaled vertical count axis. The review line comes from Phase 2's full-export threshold of 23, not Gaza's own P99 of 39.''')
replace(19, 'display(master.nlargest(5, "fatalities")[["event_id_cnty", "event_date", "location", "sub_event_type", "fatalities"]])', '# Individual high-fatality records are reviewed in Task 5 (Figure P2).')
md(21, '''**Interpretation.** Two thirds of records report zero fatalities (66.1%), while 576 records above the review threshold account for 37.6% of the reported total, so the mean alone is a poor description of a typical record. Medians, percentiles and the log view make the distribution easier to compare, but high values require source review and are not removed.''')
md(22, '''<a id="t1-types"></a>
## 1.3 Event and sub-event types

**Source:** `acled_events_clean.csv`, all records. **Figure U2** shows the category counts and their shares of all 26,664 events; a sub-event type is a more detailed label within an event type. This is the composition of the whole dataset, not the focal share within each type.''')
md(25, '''**Interpretation.** Explosions/Remote violence accounts for 76.0% of all records, and air/drone strikes plus shelling/artillery/missile attacks together account for 74.9%. Several categories are very small, so later comparisons show their sample sizes and the hypothesis test uses simulation to handle sparse counts.''')
md(26, '''<a id="t1-actors"></a>
## 1.4 Recorded actor labels

**Source:** `acled_events_clean.csv`, with a separate focal-only subset for panel B. **Figure U3** compares actor labels and actor types; blank actor2 values are shown explicitly because the corresponding records describe single-sided interactions. Actor1 and actor2 are recorded positions in the coding, not verified legal or operational roles.''')
md(29, '''**Interpretation.** Actor2 is blank in 32.4% of all records, but every focal record lists Civilians (Palestine) there, while Military Forces of Israel (2022-) appears as actor1 in 97.9% of focal records. The civilian label is part of the focal rule and the Israeli-forces labels change by date, so these are descriptions of coded records rather than independently verified roles.''')
replace(30, 'period comparisons are in Section 3.9.', 'period comparisons follow in Task 2.')
md(31, '''**Reading the flag tables.** These are shares of **all event records**: `targeting_flagged` indicates the recorded source flag, `political_violence` selects the later comparison group, and `focal_event` adds the exact civilian-actor rule. They have different meanings and should not be used interchangeably.''')
md(32, '''<a id="t1-precision"></a>
## 1.5 Location and date precision

**Sources:** the event master and land focal-incident file. **Figure U4** compares the proportions in each recorded precision category; code 1 is the most precise category. The spatial file is already a post-cutoff focal subset, so differences from the all-period master reflect both cohort selection and recording precision.''')
replace(34, 'Figure 5.', 'Figure U4.')
md(35, '''**Interpretation.** Date precision is code 1 for 99.2% of master records, whereas location precision is code 1 for only 53.7%; the land focal subset retains a higher 71.6% at location precision 1. Restricting to that subset removes about 28% of spatial incidents and changes which places contribute records, so both full and restricted spatial views are needed.''')
md(36, '''<a id="t1-area-time"></a>
## 1.6 Where and when all events are recorded

**Source:** `acled_events_clean.csv`, both periods and all event types. **Figure U5** shows district counts, retaining a missing-district category, and totals by event-calendar month. These totals are neither post-cutoff focal counts nor time-adjusted rates.''')
replace(38, 'Figure 6.', 'Figure U5.')
md(39, '''**Interpretation.** Gaza City has the most records (8,036), and monthly recording increases markedly around October 2023, with a visible trough in February 2025. The pattern motivates period and district comparisons, but recorded volume can reflect reporting coverage as well as activity and does not explain why a change happened.''')

md(40, '''<a id="task-2"></a>
# Task 2 - How do groups differ?

The first task described all records; this task asks whether the focal proportion, reported severity and timing differ between groups. We now use political-violence records for focal-share comparisons, and switch explicitly to weekly CSVs for temporal analyses.''')
md(42, '''**Source guide:** event comparisons use `master`, filtered to `political_violence` unless marked focal-only; district comparisons use `district_week`; Gaza-wide series use `gaza_week`. Counts are never added across event and weekly tables because those are two views of the same events.

The event-type prevalence comparison is presented once, with its statistical intervals and test, in [Task 4, Figure H2](#t4-type-test).''')
md(47, '''<a id="t2-period"></a>
## 2.1 Before and from October 7: counts, shares and rates

**Source:** political-violence records in `acled_events_clean.csv`, split by `period`. The periods cover 644 and 725 days, so **Figure B1** compares **count x 7 / calendar days** rather than raw totals alone. The table also gives focal shares; [Figure H1](#t4-period-figure) shows those shares with uncertainty intervals.''')
s = src(48)
prefix = s[:s.index('fig, axes =')]
right = s[s.index('x = np.arange(len(t1))'):]
put(48, prefix + 'fig, ax = plt.subplots(figsize=(9, 5))\n' + right)
md(49, '''**Interpretation.** The focal share rises from 16.2% (63/389 political records) to 47.6% (10,651/22,364), while the calendar-adjusted rate rises from 0.68 to 102.8 focal events per week. The earlier period contains only 63 focal records, and neither the rate nor share difference separates changes in activity from changes in documentation.''')
md(53, '''<a id="t2-fatality-status"></a>
## 2.2 Reported fatalities by focal status

**Source:** political-violence records from the event master, including zeros. **Figure B2** uses an ECDF: at any fatality count on the horizontal axis, the line shows the share of that group at or below it. Tables also split the comparison by period.''')
md(55, '''**Interpretation.** About 31% of focal records report zero fatalities, compared with 86% of other political-violence records, and the medians are 2 and 0. This compares reported event totals, not civilian deaths, and a recorded zero may also mean no fatality figure was available.''')
md(56, '''<a id="t2-severity"></a>
## 2.3 How often is a fatality recorded, and how large is the total?

**Source:** event-master political records grouped by event type and focal status. **Figure B3** separates two questions: left, the share reporting at least one fatality; right, the distribution **only among positive-fatality records**. Groups with fewer than 30 records remain in the table but are omitted from the figure; box centers show medians and boxes the middle half of values.''')
md(58, '''**Interpretation.** Within Explosions, 69% of focal records report a fatality versus 8% of non-focal records, yet both positive-fatality groups have median 3. The main difference is therefore how often a fatality is recorded, rather than a higher conditional median; all totals still refer to entire event records.''')
md(59, '''<a id="t2-precision"></a>
## 2.4 Does location precision change the focal share?

**Source:** event-master political records, grouped by `period` and `geo_precision`. **Figure B4** keeps each group's own political-record denominator; the supporting tables check the later period within districts and within Explosions. Precision is a recording characteristic, so this is a sensitivity comparison, not evidence that precision causes targeting.''')
md(61, '''**Interpretation.** From the cutoff onward, focal share is 59.6% at precision 1 versus 31.7% at precision 2, with the same ordering before the cutoff (21.7% versus 14.2%). The later-period gap also appears within districts and within Explosions, supporting a precision sensitivity check while leaving reporting and coding explanations unresolved.''')
md(62, '''<a id="t2-actor-types"></a>
## 2.5 Which actor labels and sub-event types occur together?

**Source:** all-period focal records from `acled_events_clean.csv`. **Figure B5** is a cross-tab heatmap: each cell counts one actor1/sub-event combination, the five most frequent actors have their own rows, and the rest share a display-only row. Color uses a log scale so smaller combinations remain visible; blank cells mean zero recorded events.''')
md(64, '''**Interpretation.** Military Forces of Israel (2022-) is the actor1 label in 10,493 of 10,714 focal records, including 8,392 air/drone-strike and 1,436 shelling records for that actor. Across all focal actors the corresponding totals are 8,420 and 1,442, and the coding alone does not verify operational roles or responsibility.''')
md(65, '''<a id="t2-composition"></a>
## 2.6 Did the mix of event types change?

**Source:** event-master political records, grouped by period and type. **Figure B6** shows each type's share of all political records within its period, so each bar sums to 100%; the accompanying table also records focal counts within each type. The separate question of whether focal prevalence changed **inside** a type is tested in [Figure H1](#t4-period-figure).''')
s = src(66)
s = s[:s.index('\nax = axes[1]')]
s = s.replace('fig, axes = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [1.3, 1]})\nax = axes[0]', 'fig, ax = plt.subplots(figsize=(11, 5))')
put(66, s + '\nplt.tight_layout(); plt.show()')
md(67, '''**Interpretation.** Explosions/Remote violence rises from 77% to 89% of political-violence records, while Battles falls from 14% to 7%. Because the mix changes, the overall focal-share difference needs both this composition view and the within-type test rather than either alone.''')
md(68, '''<a id="t2-district-counts"></a>
## 2.7 Where and when are district focal counts high?

**Source:** `acled_district_week.csv`, post-cutoff known districts. **Figure B7** shows district-week focal counts, with the partial final week greyed out and excluded from the color scale; the supporting totals and highest-week table include all 104 weeks. A pale or zero cell means few or no recorded focal events, not evidence of no harm.''')
md(70, '''**Interpretation.** Gaza City has the largest recorded district-week peak, 102 focal events in the week starting November 4, 2023, and the early-2025 decline appears across districts. Counts show volume rather than the focal proportion, which is examined separately in Figure B9.''')
md(71, '''<a id="t2-weekly"></a>
## 2.8 Do Gaza-wide counts and focal share move together?

**Source:** `acled_gaza_week.csv`; the dashed pooled share uses matching post-cutoff political records from the master. **Figure B8** puts counts above and focal/political share below on the same time axis; complete weeks form the lines and hollow markers show the final partial week. The shaded interval covers the five lowest focal-count weeks.''')
md(73, '''**Interpretation.** Gaza-wide focal counts peak at 254 in the week starting October 28, 2023 and fall to 15-23 in the five lowest weeks of early 2025, but the focal share does not fall in parallel. Low counts and high shares can coexist when the political-record denominator is small, so the two signals must be read together without assigning a cause to the dip.''')
md(74, '''<a id="t2-district-shares"></a>
## 2.9 How does focal share vary within districts?

**Source:** `acled_district_week.csv`, **103 complete weeks per district**. **Figure B9** compares a district's focal events with its own political events: grey is the weekly share, red is the sum of focal events over the current and preceding three weeks divided by the matching political sum, and the dashed line is the complete-period pooled share. This four-week smoothing includes the current week and is not the inherited preceding-four-week history feature; gaps indicate zero political denominators.''')
md(76, '''**Interpretation.** Across complete weeks, pooled focal share ranges from 40.4% in North Gaza to 52.1% in Deir El Balah, while Gaza City is 50.0% (3,411/6,825). Weekly shares fluctuate much more than the four-week pooled line, especially with small denominators, and North Gaza has two complete weeks with undefined shares.''')
md(77, '''<a id="t2-association"></a>
## 2.10 Which measures move together, and which categories are associated?

**Figure B10 uses two sources and two different measures.** Left: `acled_gaza_week.csv`, complete weeks, with **Spearman rank correlation** from -1 to +1 (opposite to similar ordering of high/low values). Right: political records from `acled_events_clean.csv`, with **Cramer's V** from 0 to 1 (weaker to stronger categorical association, without a direction).

The two history fields on the left are inherited eligible prior-week counts and the sum of four preceding weeks. Early unavailable history reduces the number of pairs; the pair-count table makes that explicit. A dagger marks built-in count/share or overlapping-window relationships, and a double dagger marks current counts compared with their earlier values.

On the right, records missing either category are omitted for that pair. Sub-event type is nested in event type, so their perfect association is built into the labels; sparse categories can inflate uncorrected V. Neither matrix demonstrates causation.''')
replace(78, 'display((sparse * 100).round(0).fillna("").astype(str).replace({"nan": ""}))', 'display((sparse * 100).round(0).astype(object).where(sparse.notna(), ""))\nprint("Weekly pairwise sample sizes")\ndisplay(n_pair)')
replace(78, 'sparse cells inflate V', 'sparse cells can inflate V')
md(79, '''**Interpretation.** Weekly focal counts have Spearman correlations of 0.70 with the previous week and 0.66 with the preceding four-week total, while focal status is associated with sub-event type (V=0.56), event type (0.32) and precision (0.28). These values motivate history and quality checks, but overlapping definitions, time dependence and sparse categories limit what they establish.''')
md(80, '''The comparisons identify differences worth examining more carefully. Next, the chart register provides navigation, and Task 4 tests the period and event-type questions while keeping effect size and assumptions visible.''')

md(82, '''<a id="task-3"></a>
# Task 3 - Figure register

Figures remain beside their explanations rather than being repeated here. Each identifier below links to its question, source and interpretation; multi-panel figures count as one figure.''')
md(83, 'REGISTER_PLACEHOLDER')

md(84, '''<a id="task-4"></a>
# Task 4 - Test the period and event-type differences

The earlier comparisons describe the observed records. Here we ask whether their category counts depart from what a simple equal-share model would predict, while recognizing that events are related across time and place.''')
md(86, '''## 4.1 Hypotheses and how to read the tests

**Source:** political-violence records from `acled_events_clean.csv`; one observation is one coded event.

| Item | Hypothesis A: period | Hypothesis B: event type |
|---|---|---|
| Null hypothesis (H0) | Focal share is the same before and from October 7 | Focal share is the same across the five types |
| Alternative (H1) | The two shares differ | At least one type's share differs |
| Primary method | Pearson chi-square on a 2 x 2 count table | Chi-square statistic with a Monte Carlo p-value on a 5 x 2 table |
| Sparse-count check | Smallest expected count 183.17 | Smallest expected count 3.30; four of ten cells below 5 |
| Sensitivity checks | Fisher exact, continuity correction and within-type comparisons | Pool the two rare types; compare the two focal-containing types |

An **expected count** is what the equal-share model predicts for a table cell. A **p-value** measures how unusual the observed statistic would be under that model and its assumptions; it is not the probability that H0 is true. Monte Carlo uses 99,999 simulated tables with the same margins and a fixed seed; its smallest reported estimate here is 0.00001.

We use **0.025** as the decision threshold for each of two primary tests (0.05 divided by two, the Bonferroni adjustment). Effect sizes show the magnitude: percentage-point difference, share ratio (called a risk ratio in the output), odds ratio and phi/V; 95% intervals show uncertainty under the model. These ratios concern recorded-event classification, not an individual's risk of harm.

Large expected counts support the usual chi-square approximation but do not establish independence. The tests and intervals treat records as independent even though events can cluster, so their inferential calibration is limited; we use them as exploratory evidence and do not claim causation. 'Pearson chi-square' is a categorical association test, not Pearson's numeric correlation coefficient.''')
md(93, '''The helpers below build the count tables, check expected counts, compute Wilson intervals for proportions and format p-values without claiming precision below the simulation limit.''')
replace(94, 'return f"p < {floor:.5f}" if np.isclose(p, floor) else f"p = {p:.5f}"', 'return f"p = {floor:.5f} (simulation floor)" if np.isclose(p, floor) else f"p = {p:.5f}"')
replace(94, 'the check that decides which p-value procedure is valid', 'the sparse-cell check for the p-value approximation') if 'the check that decides which p-value procedure is valid' in src(94) else None
replace(94, 'Print the sparse-cell diagnostic that decides which p-value procedure is valid.', 'Print the expected-count diagnostic; this does not check independence.')
md(95, '''<a id="t4-period-test"></a>
## 4.2 Hypothesis A - Is focal share different between periods?

We test the two period shares with Pearson chi-square without continuity correction, since expected counts are large, and show Fisher exact and corrected results as sensitivity checks. Period length matters for the earlier weekly rates, but a proportion uses the records within its own period as denominator.''')
md(97, '''**Test result.** The test rejects equal shares (chi-square=151.60, p about 7.8e-35): the observed difference is 31.4 percentage points, with a model-based 95% interval of 27.7-35.1 points. The small phi value (0.082) coexists with a large share difference because the two period groups are highly unequal in size; neither statistic resolves changes in recording coverage.''')
md(98, '''<a id="t4-period-figure"></a>
### Figure H1 - Overall difference and within-type comparison

The left panel shows period shares with 95% Wilson intervals. The right panel repeats the comparison within the two types containing focal records, using chi-square when expected counts are sufficient and Fisher exact otherwise; this checks whether the overall difference is solely a change in the event-type mix.''')
replace(99, '# the large-sample test is valid only when every expected count is at least 5', '# expected-count check for the large-sample approximation')
md(100, '''**Interpretation.** Focal share rises overall from 16.2% to 47.6% and within Explosions from 13.1% to 49.4%, so the overall difference is not solely a change in event-type composition. Violence against civilians is already near 100% in both periods, with only 24 earlier records; these intervals and tests still rely on the independence assumption discussed above.''')
md(101, '''<a id="t4-type-test"></a>
## 4.3 Hypothesis B - Does focal share differ by event type?

We retain all five political-violence event types and use Monte Carlo simulation because Protests and Riots have sparse expected counts. **Figure H2** shows each type's focal share with Wilson intervals and a residual heatmap: a positive residual means more records than the equal-share model expects, and a negative one means fewer. Residuals are descriptive contributions to the statistic, not separately corrected hypothesis tests.''')
md(104, '''**Interpretation.** Equal focal shares are rejected (chi-square=2,394.76, Monte Carlo estimate **p=0.00001**, the simulation floor, V=0.32): Violence against civilians is 99.3% focal, Explosions 48.9%, and Battles 0%, with the largest residual departures in the first and last of those groups. Pooling rare types and comparing the two focal-containing types retain the conclusion, but the civilian-actor requirement makes part of this association structural and the test does not establish causation.''')
md(105, '''<a id="t4-summary"></a>
## 4.4 Test summary

This compact table collects the computed statistics rather than introducing another comparison. Both primary decisions use the adjusted 0.025 threshold.''')
md(107, '''**What the tests establish.** Period and event type are associated with focal classification in this snapshot, and the period difference also occurs within Explosions. They do not distinguish activity from reporting changes or verify actor roles; next we examine how concentrated, persistent and unusual the recorded patterns are.''')

md(109, '''<a id="task-5"></a>
# Task 5 - Which patterns deserve closer review?

This task moves from group differences to practical review questions: where comparisons have few examples, which records or weeks stand out, whether patterns repeat, and how events concentrate in time and space. Each method is a descriptive screening tool, not a verified label of an important or harmful event.''')
md(117, '''### How unusual weeks are screened

A **median** describes the middle week; **MAD**, the median absolute deviation from that median, describes typical variation. A modified z-score compares a week with that baseline: `0.6745 x (count - median) / MAD`; values beyond +/-3.5 are flagged for review, not declared errors ([method reference](#ref-outliers)).

We compare the whole complete period with a rolling baseline using only the **previous eight calendar weeks**. Counts use a minimum MAD of one event to avoid division by zero; shares use their own MAD with no one-event floor, and a flat share history is left unscored. Missing/ineligible history is never bridged by skipping weeks.''')
put(118, '''Z_CUT = 3.5

def robust_z(s):
    """Descriptive whole-series modified z-score; flat series are unscored."""
    med = s.median()
    mad = (s - med).abs().median()
    return 0.6745 * (s - med) / mad if mad > 0 else pd.Series(np.nan, index=s.index)

def trailing_robust_z(s, window=8, mad_floor=1.0):
    """Previous calendar weeks only; any missing current/history value leaves no score."""
    vals = s.to_numpy(float)
    out = np.full(len(vals), np.nan)
    for i in range(window, len(vals)):
        hist = vals[i-window:i]
        if not np.isfinite(vals[i]) or not np.isfinite(hist).all():
            continue
        med = np.median(hist)
        mad = max(float(np.median(np.abs(hist-med))), mad_floor)
        if mad > 0:
            out[i] = 0.6745 * (vals[i]-med) / mad
    return pd.Series(out, index=s.index)
''')
md(119, '''<a id="t5-imbalance"></a>
## 5.1 Are some groups too small for reliable comparison?

**Sources:** political records from the master, plus zero-count summaries from both weekly files. The table contrasts focal and non-focal examples in each slice; **Figure P1** focuses on the smaller class, adding information beyond the earlier share plots. A minority count of zero means that class is absent, not merely uncommon.''')
md(121, '''### Figure P1 - Size of the smaller class

The horizontal axis uses a symmetric-log scale with a linear region near zero, so zero remains zero and very different sample sizes fit on one display. Shares and majority/minority ratios remain in the preceding table.''')
put(122, '''plot_df = imb.iloc[::-1]
fig, ax = plt.subplots(figsize=(12, 5))
ax.barh(plot_df.index, plot_df["Minority count"], color=C_OTHER)
for y, (_, r) in enumerate(plot_df.iterrows()):
    ax.annotate(f"{r['Minority count']:,.0f} ({r['Minority class']})",
                (r["Minority count"], y), xytext=(6, 0), textcoords="offset points", va="center", fontsize=9)
ax.set_xscale("symlog", linthresh=1)
ax.set_xlim(0, 100000)
ax.set_xlabel("Records in the smaller class (symlog scale; zero shown at zero)")
ax.set_ylabel("Political-violence record subset")
ax.set_title("How many examples does the smaller class have?")
ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
plt.tight_layout(); plt.show()
''')
md(123, '''**Interpretation.** The full political-record split is nearly balanced, but the earlier period has only 63 focal examples, later Violence against civilians has only six non-focal examples, and later Battles has no focal examples. These structural and small-sample limitations matter more than the overall balance; North Gaza also has zero-count district-weeks, where a political denominator of zero leaves focal share undefined.''')
md(124, '''<a id="t5-fatality-review"></a>
## 5.2 Which high-fatality records need review?

**Source:** `acled_events_clean.csv`, all periods; `high_fatalities_review` selects reported totals of 24 or more. [Figure U1](#t1-fatalities) already establishes the overall distribution, so this section adds record identity, flagged-group composition and timing rather than repeating that distribution.''')
s=src(125)
start=s.index('fat_summary = pd.DataFrame')
end=s.index('print("Flagged records by event type')
put(125, s[:start] + '''review_detail = pd.Series({
    "Gaza IQR upper fence (Q3 + 1.5 x IQR)": f.quantile(.75) + 1.5 * (f.quantile(.75)-f.quantile(.25)),
    "Records selected in top 1% (floor of 1% x n)": len(top1),
    "Share of reported fatalities in that top 1%": top1.fatalities.sum() / f.sum(),
    "Flagged records that are focal": int(flag.focal_event.sum()),
}).to_frame("value")
display(review_detail)
''' + s[end:])
md(126, '''### Figure P2 - The largest recorded fatality totals

These are individual event records, identified by date and location. The table retains IDs and sources so the numbers can be checked against the underlying reports.''')
s=src(127)
prefix=s[s.index('top = master.nlargest'):s.index('fig, axes')]
body=s[s.index('ax.barh(range(len(top))'):]
put(127, prefix + '''display(top.iloc[::-1][["event_id_cnty", "event_date", "location", "fatalities", "source"]])
fig, ax = plt.subplots(figsize=(12, 6))
''' + body)
md(128, '''**Interpretation.** The largest recorded total is 471 and the three largest records fall in October-November 2023, while 422 of the 576 flagged records are focal. Large totals may reflect how reports were aggregated as well as event severity, so retain them and review their notes and sources rather than treating them as automatically wrong.''')
md(129, '''<a id="t5-fatality-time"></a>
### Figure P3 - When are flagged records concentrated?

**Source:** the master's high-fatality subset, grouped by event-calendar quarter and focal status. The table also divides flagged records by all event records in that quarter; the chart shows counts from Q4 2023 onward, when flagged records occur.''')
md(131, '''**Interpretation.** Q4 2023 contains 281 of the 576 flagged records, or 7.7% of that quarter's records, compared with 2.6% in Q1 2024 and 1.7% or less in later quarters. Sensitivity analyses that exclude flagged records would therefore affect the early period disproportionately; the flag is a review threshold, not verification of the totals.''')
md(132, '''<a id="t5-unusual-weeks"></a>
## 5.3 Which Gaza-wide weeks stand out?

**Source:** `acled_gaza_week.csv`, 103 complete weeks; all of these meet Phase 2's political-activity history rule. We compare whole-period scores with the preceding-eight-week rule; the first eight weeks lack a trailing score, and the final partial week is shown but not scored. Both counts and shares are screened, with the scale-specific MAD handling explained above.''')
replace(133, 'trailing_robust_z(gwc[c], window=8)', 'trailing_robust_z(gwc[c], window=8, mad_floor=0.0 if c == "focal_share" else 1.0)')
md(134, '''### Figure P4 - Whole-period versus recent-history count flags

Red points are unusual against the whole-period baseline; orange diamonds are flagged only against recent history. The shaded band belongs to the whole-period count baseline, so a point can sit inside that band and still be unusual relative to its preceding eight weeks.''')
md(136, '''**Interpretation.** The whole-period rule flags three early high focal-count weeks, whereas the trailing rule flags 13 focal-count weeks, including several rises after the early-2025 trough. A recovery can look unusually high relative to a short low baseline, so these flags are review leads rather than evidence of a new underlying cause.''')
# New local-history method uses inherited eligibility; preserve original behavior as explicit sensitivity.
replace(137, '# Same trailing 8-week rule, applied inside each district (complete weeks only).', '# Same trailing rule by district; primary scores require eligible current and prior weeks.')
replace(137, 'dwc["tz_focal"] = dwc.groupby("admin2").focal_events.transform(lambda s: trailing_robust_z(s, window=8))', '''dwc["tz_focal"] = dwc.groupby("admin2").focal_count_for_history.transform(lambda s: trailing_robust_z(s, window=8))
dwc["tz_raw_complete"] = dwc.groupby("admin2").focal_events.transform(lambda s: trailing_robust_z(s, window=8))
baseline_sensitivity = pd.DataFrame([
    {"Baseline policy": label, "Scored district-weeks": int(dwc[col].notna().sum()),
     "Flagged district-weeks": int(dwc[col].abs().gt(Z_CUT).sum())}
    for label, col in [("Phase 2 eligible history (primary)", "tz_focal"),
                       ("All complete-week counts (sensitivity)", "tz_raw_complete")]
])
display(baseline_sensitivity)''')
md(138, '''**Interpretation.** With Phase 2's eligibility rule, 48 of 465 scored district-weeks are flagged (10.3%); retaining zero-political weeks in the baseline instead gives 50 of 475 (10.5%). The difference is confined to North Gaza's missing eligible history, and several of the highest upward scores elsewhere still follow the early-2025 trough, so both baseline policy and recovery effects matter.''')
replace(139, 'None: no event is counted twice.', 'No repeated IDs; this alone cannot exclude real-world event overlap.')
replace(139, 'All inside: no impossible locations.', 'All inside the rough box; this does not verify each location.')
replace(139, 'Date is not exact for these; weekly counts can shift by a week.', 'Lower date precision can move records between time bins; sensitivity is not tested here.')
md(140, '''**Reading the quality checks.** IDs and coordinates are complete and the coordinates pass the rough geographic screen, but these checks do not establish that every real-world event is distinct or exactly located. Most records have date precision 1, yet date sensitivity remains untested, and repeated spatial coordinates describe named-place concentrations rather than exact incident points.''')
md(141, '''<a id="t5-trends"></a>
## 5.4 Is there a longer-term direction?

**Source:** `acled_gaza_week.csv`, complete weeks. Here a month receives all counts from weeks **starting in that month**, unlike the event-calendar-month totals in Task 1; first/last months and four/five-week months therefore have different exposure. The table reports monthly sums, number of weeks, quarterly weekly means and exploratory rank trends over time.''')
replace(142, 'display(mo.T.round(3))', 'display(mo.round(3))')
replace(142, '"p (rough)": p,', '"p (rough)": f"{p:.2e}",')
md(143, '''### Figure P5 - Monthly grouped counts and pooled share

Bars use the left count axis; the line uses the right share axis. The pooled share divides the monthly grouped focal sum by the matching political sum, rather than averaging weekly percentages; the two axes should not be compared by their vertical heights.''')
md(145, '''**Interpretation.** Focal counts have little monotonic trend over complete weeks (Spearman rho=0.10), while political counts decrease (rho=-0.55) and focal share increases (rho=0.51). The series contains a marked trough and recovery rather than a smooth trend, and the reported exploratory p-values do not account for dependence between neighboring weeks.''')
md(146, '''## 5.5 Calendar patterns and persistence

A recurring calendar pattern is different from persistence: the former repeats at a calendar interval, while the latter means nearby weeks resemble one another. We inspect both without assuming that either proves future predictability.''')
md(147, '''<a id="t5-seasonality"></a>
### Figure P6 - Do calendar months or weekdays repeat?

**Sources:** `acled_gaza_week.csv` complete-week means by start-month/year (left), and all post-cutoff focal records in the event master by event weekday (right). The weekday chart includes dates in the final partial week and uses counts, not rates adjusted for the number of each weekday in the window.''')
replace(148, '.dt.dayofweek', '.dt.day_of_week')
md(149, '''**Interpretation.** The nine shared calendar months of 2024 and 2025 do not align in their mean weekly focal counts (rho=-0.30), and the busiest weekday has about 1.11 times the count of the quietest. This exploration finds no clear recurring calendar pattern, but the short, uneven observation window does not establish that seasonality is absent.''')
md(150, '''<a id="t5-persistence"></a>
### Figure P7 - How long does week-to-week resemblance persist?

**Source:** `acled_gaza_week.csv`, complete-week focal counts. **Autocorrelation (ACF)** compares the series with itself shifted back by one, two or more weeks; the second panel applies it to week-to-week changes. The shaded range is an approximate reference under no autocorrelation, not a formal seasonal test or a guarantee of predictive skill.''')
replace(151, 'A 52-week cycle cannot be checked: the table spans only', 'Annual repetition is not reliably established here: the table spans only')
md(152, '''**Interpretation.** Focal-count autocorrelation is 0.76 at one week and remains above the approximate band through six weeks, whereas changes are mostly within the band apart from a negative lag-1 value. This supports evaluating prior-week history, but shifts in the series level can create persistence without demonstrating reliable forecasts.''')
md(153, '''## 5.6 Districts, groups of weeks and spatial concentrations

We now distinguish three units: districts summarized over time, complete Gaza-wide weeks grouped by their recorded activity, and incident coordinates grouped geographically. A cluster here means similarity or proximity under a stated algorithm, not a verified cause or legal pattern.''')
md(154, '''<a id="t5-district-profile"></a>
### Figure P8 - District contribution and variability

**Source:** `acled_district_week.csv`, complete weeks. Left: each district's focal events over the current and preceding three weeks divided by **all known districts' focal events** in those weeks; this is geographic contribution, not the political-denominator focal share in Figure B9. Right: median weekly count versus **coefficient of variation (SD/mean)**, a measure of variability relative to typical volume; bubble area represents total count.''')
replace(155, 'bbox_to_anchor=(0.5, -0.14)', 'bbox_to_anchor=(0.5, -0.30)')
replace(155, 'plt.tight_layout(); plt.show()', 'plt.tight_layout(); fig.subplots_adjust(bottom=0.30); plt.show()')
md(156, '''**Interpretation.** In complete weeks, Gaza City contributes 3,411 focal events (32.3% of known-district focal events), while North Gaza has the highest relative variability (0.83) and six zero-focal weeks. The unequal volumes and variability favor district-specific baselines, and these totals intentionally exclude the partial week.''')
md(158, '''**Choosing a descriptive grouping.** The silhouette score compares how similar a week is to its assigned group versus other groups; higher values indicate clearer separation for these features. Although k=2 scores highest (0.67), k=3 (0.51) is retained to describe low weeks and distinguish the remaining activity/share patterns, not to claim a true number of regimes.''')
md(159, '''### Figure P9 - Groups of complete weeks and their timing

The scatter shows raw focal/political counts for readability, but group assignments use the transformed three-feature input described above. Group A/B/C names follow increasing median focal count; the timeline shows whether similar weeks occur together.''')
md(161, '''**Interpretation.** The three descriptive groups contain eight low weeks from January 18-March 8, 2025, 51 lower-share weeks, and 44 higher-share weeks, with median focal counts of 21.5, 92 and 123.5 respectively. Their strong temporal ordering suggests level shifts, but overlapping count/share information and the chosen scaling mean these are exploratory labels, not validated regimes or predictions.''')
md(163, '''<a id="t5-spatial-map"></a>
### Figure P10 - Where are land focal incidents concentrated?

**Source:** `acled_focal_incidents.csv`, post-cutoff land focal events, then `geo_precision_1=True`. The preceding tables count coordinate pairs and district shares; the maps use the same extent, color scale and bubble-size rule for both subsets. Coordinates can represent named places, and there is no basemap or inferred boundary.''')
md(165, '''**Interpretation.** The 10,583 incidents occupy 101 coordinate pairs, while the precision-1 restriction retains 7,576 incidents on 95 pairs and a similar broad spatial shape. The loss is uneven across places, so apparent concentration must be read alongside coverage loss and cannot be interpreted as exact incident locations.''')
md(166, '''<a id="t5-concentration"></a>
### Figure P11 - How uneven is the distribution across coordinates?

**Source:** the spatial file, grouped by latitude/longitude, with full and precision-1 subsets. Left: the 12 largest full-subset coordinates split by precision; right: a **Lorenz curve**, which accumulates incidents from the least to most populated coordinates, with the diagonal representing equal counts everywhere. **Gini** summarizes that inequality (0 means equal); each subset uses its own occupied coordinate set, so this is not a fixed-location comparison.''')
md(168, '''**Interpretation.** The top ten coordinates hold 33.8% of full-subset incidents versus 38.1% within precision 1, and the corresponding Gini values round to 0.57 and 0.60. Precision filtering therefore sharpens concentration among retained coordinates, but changes both the incidents and occupied places being compared.''')
md(170, '''<a id="t5-dbscan"></a>
### Figure P12 - How sensitive is spatial clustering to its settings?

**Source:** full and precision-1 spatial incidents, including repeated coordinate rows. **DBSCAN** connects dense nearby observations: radius (`eps`) sets neighborhood distance and `min_samples` sets how many observations are needed for a dense neighborhood; isolated observations are called noise. Distances use haversine on radians with radius converted from kilometers, and the grid compares 0.25-3 km with min_samples 10/50 ([method reference](#ref-dbscan)).

The table reports clusters, unclustered share and the largest cluster's share of all incidents. These are descriptive sensitivity measures, not predictive scores.''')
md(172, '''**Interpretation.** With min_samples=10, the full subset has 81 clusters at both 0.25 and 0.5 km, but their noise shares differ; cluster counts fall to 19 at 2 km and one at 3 km. Repeated named-place coordinates strongly shape this result, so 1-2 km is a range worth investigating against district summaries and precision restrictions, not an established optimal setting.''')

md(176, '''<a id="task-6"></a>
# Task 6 - Answers to the business questions

Each answer below names its population and links to the exact evidence in this notebook. Counts describe this historical ACLED snapshot; they are not a complete measure of civilian harm.''')
md(178, '''## BQ1 - How do counts and shares differ between periods?

**Answer.** Among Gaza political-violence records, focal share is **16.2% before October 7, 2023 (63/389)** and **47.6% from that date (10,651/22,364)**. Adjusting each total for the 644/725 calendar days gives **0.68 versus 102.8 focal events per seven days**, rather than a mean of weekly CSV rows.

**Evidence:** [Task 2, Figure B1 and period table](#t2-period) for counts, shares and rates; [Task 4, Hypothesis A results](#t4-period-test) for the test/effect sizes; [Figure H1](#t4-period-figure) for uncertainty intervals and the within-type comparison.

**Meaning and limit.** The increase also appears within Explosions, so it is not solely a change in event-type mix; the sparse earlier cohort and changing recording coverage prevent a causal explanation.''')
md(179, '''## BQ2 - Which actor labels and event types recur?

**Answer.** Among **10,714 focal records across both periods**, Explosions/Remote violence accounts for **9,906 (92.5%)** and Violence against civilians for **808 (7.5%)**. Air/drone strike is the largest sub-event type (**8,420; 78.6%**), followed by shelling/artillery/missile attack (**1,442**) and Attack (**792**); Civilians (Palestine) appears as actor2 in every focal record, while Military Forces of Israel (2022-) appears as actor1 in **10,493 (97.9%)**.

**Evidence:** [Task 2, Figure B5 and focal cross-tabs](#t2-actor-types) for event/sub-event combinations and actor counts; [Task 1, Figure U3 and actor tables](#t1-actors) for actor marginals. These percentages describe composition **within focal events**, not the focal prevalence within each event type shown in [Figure H2](#t4-type-test).

**Meaning and limit.** The civilian label is required by the focal rule and one actor label dominates; assigning roles beyond the recorded labels still requires incident-note verification.''')
md(180, '''## BQ3 - Where are land focal events concentrated?

**Answer.** Among **10,583 post-cutoff land focal incidents**, Gaza City accounts for **32.5%**, Khan Yunis **21.5%**, and Deir El Balah **21.4%**. The top ten coordinate pairs hold **33.8%** of incidents; after restricting to precision 1, the top ten within that subset hold **38.1%**, but only **7,576 incidents remain** (about 28% excluded).

**Evidence:** [Task 5 spatial concentration tables](#t5-spatial-tables) for district/top-ten percentages and retained counts; [Figure P10](#t5-spatial-map) for the full/restricted maps; [Figure P11](#t5-concentration) for uneven precision and concentration.

**Meaning and limit.** The broad geography persists but concentration changes with selection; repeated named-place coordinates are not exact attack points, and temporal stability of spatial clusters has not been established.''')
md(181, '''## BQ4 - Which district-weeks have high or sustained activity?

**Answer.** The Gaza-wide peak is **254 focal events** in the week starting **October 28, 2023**; the largest district-week is **Gaza City, November 4, 2023, with 102**. Gaza City totals **3,451 focal events across all 104 weeks**, or **3,411 across complete weeks only**; Gaza-wide focal counts also correlate with the previous week (**Spearman 0.70**) and preceding four-week total (**0.66**).

Relative to recent **eligible local history**, **48 of 465 scored district-weeks (10.3%)** exceed the screening threshold. The largest upward score is Khan Yunis on March 29, 2025 (**48 focal events**); several other high scores follow the early-2025 trough, illustrating how a recovery can trigger a short-window alert.

**Evidence:** [Figure B8](#t2-weekly) for the Gaza peak; [Figure B7 and district tables](#t2-district-counts) for all-week totals/peak; [Figure P8](#t5-district-profile) for complete-week totals; [Figure B10, left](#t2-association) for Spearman history relationships; [Task 5 local-history tables](#t5-local-history) for the 48/465 flags and named district-weeks.

**Meaning and limit.** Absolute peaks and unusual local weeks are different questions, and these screening flags are leads for investigation rather than verified anomaly labels.''')
md(182, '''## BQ5 - Which findings change under restrictions or settings?

**Answer.** Precision materially changes focal prevalence: the later-period share is **59.6% at precision 1 versus 31.7% at precision 2**, compared with **21.7% versus 14.2%** before the cutoff. Explosions remains the dominant type among focal events (**61.9% before; 92.6% after**), and Gaza City has the most later-period focal events within both precision categories; before the cutoff, North Gaza has **28** focal records versus Gaza City's **10**, from a total of only 63.

Spatial top-ten concentration rises from **33.8% to 38.1%** under precision 1; DBSCAN merges from many clusters into one as radius increases, while changing local-history eligibility changes district-week flags from **50/475 to 48/465**. These comparisons show that definitions and settings affect what stands out.

**Evidence:** [Figure B4 and precision tables](#t2-precision) for precision-specific prevalence; [BQ5 supporting tables](#bq5-evidence) below for focal composition and district rankings; [spatial tables](#t5-spatial-tables) for top-ten shares; [Figure P12 and grid](#t5-dbscan) for spatial settings; [local-history comparison](#t5-local-history) for baseline eligibility.

**Limit.** These checks do not fully test alternative focal definitions, reporting coverage, geographic aggregation or temporal spatial stability; those remain explicit follow-up questions.''')
md(183, '''<a id="limitations"></a>
# Limitations and reproducibility

- **Recorded coverage:** ACLED records are not all events or all civilian harm; changes in documentation can change counts and shares.
- **Meaning of fields:** fatality totals belong to entire event records; actor positions, targeting labels and precision codes do not independently verify roles, intent or exact locations.
- **Dependence and selection:** related events limit independence-based tests; precision restrictions change the observed population, and categorical associations can be partly built into the focal rule.
- **Screening, not ground truth:** anomaly flags, K-means groups and DBSCAN clusters depend on settings and have not been validated as important events. The short historical window does not rule out seasonality.
- **What remains untested:** verified actor roles, reporting-bias effects, alternative cohort definitions, and stability across time/geographic aggregation require further analysis and source review.

To reproduce the analysis, start from the project folder and run the notebook from top to bottom using the supplied four CSVs. The initial checks stop on snapshot mismatches; randomized procedures use seed 42, Monte Carlo uses 99,999 resamples, and incomplete weeks are excluded from scoring. No notebook cell writes back to a source CSV.

The data source is the ACLED Palestine event export downloaded October 18, 2026, with a raw-file manifest in `data/metadata/`. Phase 2's country/area filter, retained blanks and derived features are summarized in the [data guide](#data-guide); runtime versions are printed below.''')
md(184, '''<a id="task-7"></a>
# Task 7 - Key insights and modeling plan

## Seven insights to carry into Phase 4

1. **Account for unequal periods and a sparse earlier cohort.** The period contrast is large, but only 63 earlier focal records support it; use it as descriptive context, with temporal modeling based on post-cutoff history ([B1](#t2-period), [H1](#t4-period-figure)).
2. **Separate definition from discovery.** Actor and event-type patterns partly reflect the focal rule; retain original labels for explanation, not as proof of roles or a shortcut target ([B5](#t2-actor-types), [H2](#t4-type-test)).
3. **Retain and review the fatality tail.** Most records report zero fatalities, while flagged high totals contribute disproportionately; use robust summaries and source verification rather than automatic deletion ([U1](#t1-fatalities), [P2-P3](#t5-fatality-review)).
4. **Carry precision sensitivity into spatial work.** The restriction removes about 28% of land focal incidents and changes concentration, so present full and restricted results together ([P10](#t5-spatial-map), [P11](#t5-concentration)).
5. **Use local history and test recovery effects.** Counts persist over time, but an eight-week baseline can flag recovery from a trough; compare longer windows and preserve eligibility rules ([P4](#t5-unusual-weeks), [local checks](#t5-local-history), [P7](#t5-persistence)).
6. **Use district-specific comparisons and both counts and shares.** Districts differ in volume/variability, and a high share can occur with few records; retain denominators with alerts ([B8](#t2-weekly), [B9](#t2-district-shares), [P8](#t5-district-profile)).
7. **Treat spatial clusters as concentrations of recorded places.** Repeated coordinates and radius choices strongly determine cluster size; compare DBSCAN against simple district totals and investigate stability ([spatial tables](#t5-spatial-tables), [P12](#t5-dbscan)).

## Proposed techniques and evaluation

The two selected technique families are **spatial clustering** and **temporal anomaly detection**, continuing the Phase 1 plan within Phase 2's revised Gaza/post-cutoff scope. The work below is a plan, not completed predictive validation.

| Technique | Inputs and purpose | Baseline / comparisons | How to judge usefulness |
|---|---|---|---|
| DBSCAN | Post-cutoff land focal coordinates in radians; identify geographic concentrations for documentary review | District-count summaries; radii around 1-2 km plus the wider explored range, min_samples 10/50, full versus precision 1 | Cluster/noise proportions, sensitivity of membership and concentration, source review of selected places; useful only if it adds stable detail beyond district totals |
| District-week anomaly detection | Assess a completed week's focal activity against eligible earlier weeks; optionally add political counts, focal share, lag1 and previous-four-week sum for Isolation Forest | Trailing median/MAD as the transparent baseline; compare windows such as 8/12/16 weeks and an Isolation Forest alternative | Alert burden per district, consistency across settings, review of high/low alerts and unflagged comparison weeks, and sensitivity to recovery/zero-denominator history |

**Timing and leakage.** The proposed alert is retrospective, produced after the current week closes, not a forecast of next week's harm. Fit any learned model or transformation on earlier weeks only and tune settings using rolling chronological validation within the post-cutoff period; full-period EDA and K-means here have already seen the snapshot, so none of it is an untouched final test set. Future newly collected data would be needed for a genuinely unseen assessment.

**Feature choices.** Prior-week and prior-four-week counts are motivated by persistence, while district, denominators and precision are needed to interpret coverage. Counts and their ratios share information, so compare smaller feature sets rather than assuming each is independent; do not use record IDs, source-update timestamps or the review flag as direct predictors of an unverified target. Calendar effects remain a sensitivity question rather than a demonstrated seasonal mechanism.

**No verified anomaly labels.** Rule-based flags are not ground truth for evaluating another detector, and accuracy against those flags would be circular. Start with alert burden, stability and documented review; calculate precision/recall only if an independent review process supplies suitable labels, and describe that process.

**First experiment.** Compare eligible district-specific trailing baselines at 8, 12 and 16 weeks, recording which alerts are trough recoveries and how results change with history eligibility; in parallel, compare spatial settings with district totals and the precision-1 subset. Proceed to a more complex method only if it adds interpretable, stable review candidates that the simple baseline misses, with each candidate linked to event IDs, notes and sources.''')

# Supplemental prose placed before code so definitions precede their use.
before = {
137: [('markdown', '''<a id="t5-local-history"></a>
### District-week screening and baseline sensitivity

**Source:** `acled_district_week.csv`, complete weeks. Primary scores use the saved `focal_count_for_history`, requiring an eligible current week and eight eligible preceding calendar weeks; North Gaza's two complete zero-political weeks and affected windows therefore remain unscored. The comparison table also retains the original all-complete-count policy as a sensitivity check, making its effect visible.''')],
139: [('markdown', '''### Data-quality checks behind the patterns

**Sources:** the event master, Gaza-week file and spatial incident file. These checks look for missing/duplicate identifiers and broad coordinate or coverage problems; they screen the files rather than verifying every real-world event.''')],
157: [('markdown', '''<a id="t5-week-clusters"></a>
### Grouping complete weeks by recorded activity

**Source:** `acled_gaza_week.csv`, 103 complete weeks. We create **ln(1 + focal count)** and **ln(1 + political count)** here in Phase 3 to reduce the influence of large counts, then combine them with the unlogged focal share. These weekly logs are not Phase 2's `fatalities_log1p` variable.

**StandardScaler** subtracts each feature's mean and divides by its standard deviation so different units do not dominate distance. **K-means** groups weeks with similar standardized values; it is fitted to the full historical period only for description, and the count/share features overlap mathematically. We compare k=2-5 before describing three groups.''')],
162: [('markdown', '''<a id="t5-spatial-tables"></a>
### Spatial input and concentration tables

**Source:** `acled_focal_incidents.csv`, post-cutoff land focal incidents. We count incidents at each coordinate pair and repeat the calculation for precision 1; top-ten/top-twenty lists are ranked separately within each subset. District percentages below use land focal incidents, not the district-week denominator; the accompanying Gini and Lorenz comparison uses each subset's own occupied coordinates.''')],
169: [],
}

# Move the DBSCAN introduction ahead of the computational grid as well as the plot.
before[169] = [('markdown', src(170))]
omit.add(170)

bq5code = '''# Direct supporting evidence for BQ5; all values are computed from the event master.
focal_all = master.loc[master.focal_event]
focal_type_period = pd.crosstab(focal_all.period, focal_all.event_type).reindex([BEFORE, AFTER], fill_value=0)
print("Focal-event composition by period (denominator: all focal events in that period)")
display(focal_type_period)
display(focal_type_period.div(focal_type_period.sum(axis=1), axis=0).mul(100).round(1).add_suffix(" (%)"))
post_focal_evidence = focal_all.loc[focal_all.period.eq(AFTER) & focal_all.geo_precision.isin([1, 2])]
print("Post-cutoff focal counts by known district and precision")
display(pd.crosstab(post_focal_evidence.admin2, post_focal_evidence.geo_precision))
print("Pre-cutoff focal counts by known district")
display(focal_all.loc[focal_all.period.eq(BEFORE)].groupby("admin2").size().rename("Focal events").to_frame())
'''
after = {182: [('markdown', '''<a id="bq5-evidence"></a>
### Supporting tables for BQ5

These tables display the focal-composition and district-ranking claims directly, rather than citing a precision-share plot that uses a different denominator. **Source:** `acled_events_clean.csv`; the labels specify the period, focal restriction and precision subset.'''), ('code', bq5code)]}

refs = '''<a id="references"></a>
# References

1. **ACLED.** Palestine event-level export, January 1, 2022-September 30, 2025, downloaded October 18, 2026; raw file `data/raw/acled_palestine_events_2022_2025.csv` and manifest `data/metadata/acled_events_download_manifest.json`. [Codebook](https://acleddata.com/methodology/acled-codebook) provides source definitions; use of the data remains subject to ACLED's terms.
2. **Group 7.** `DMA_Phase1.ipynb`, business problem and original BQ1-BQ5; `DMA_Phase2.ipynb`, revised Gaza scope, preprocessing and four processed outputs. This report summarizes the dependencies needed to read Phase 3 independently.
3. **DS312.** `[STUDENT] DS312_FINAL_PIT_GUIDE.pdf`, Phase 3 requirements (page 5), 1st Semester A.Y. 2026-2027, Instructor Nicole S. Menorias; `Phase3_EDA_Guide_G7.pdf`, supporting course guide.
4. **Group 7 contributions.** Univariate, bivariate/multivariate, hypothesis-testing, pattern-spotting and BQ-answer work integrated here; `DMA_Phase3_EDA_Bivariate_Multivariate_Merged.ipynb` was consulted as a read-only comparison reference.
5. **Mugot, C. J. S.** *EDA Bivariate Analysis of Categorical Variables*, 2026, course reference for categorical analysis/Monte Carlo testing.
6. <a id="ref-outliers"></a>**Iglewicz, B. and Hoaglin, D. (1993).** *How to Detect and Handle Outliers*. Modified z-score screening reference; the eight-week window and count MAD floor are project choices, not universal thresholds.
7. <a id="ref-dbscan"></a>**Ester, M., Kriegel, H.-P., Sander, J. and Xu, X. (1996).** *A density-based algorithm for discovering clusters in large spatial databases with noise*. DBSCAN method reference.
8. **Software references.** SciPy: `chi2_contingency`, `MonteCarloMethod`, `fisher_exact`, `binomtest`, `spearmanr`; scikit-learn: `DBSCAN`, `KMeans`, `StandardScaler`, `silhouette_score`. The printed runtime versions identify the implementation used for this notebook's saved run.
'''

register = [
('U1','Reported fatality distribution','t1-fatalities','Event master, all records'),
('U2','Event/sub-event composition','t1-types','Event master, all records'),
('U3','Actor labels and missingness','t1-actors','Event master, all and focal-only'),
('U4','Precision profiles','t1-precision','Event master and land focal incidents'),
('U5','District and calendar-month counts','t1-area-time','Event master, all records'),
('B1','Calendar-adjusted period rates','t2-period','Master political records'),
('B2','Fatalities by focal status','t2-fatality-status','Master political records'),
('B3','Fatality occurrence/conditional totals','t2-severity','Master political records; positive-only right'),
('B4','Precision and period focal shares','t2-precision','Master political records'),
('B5','Actor/sub-event cross-tab','t2-actor-types','Master focal records'),
('B6','Period event-type composition','t2-composition','Master political records'),
('B7','District-week counts','t2-district-counts','District-week; partial column masked'),
('B8','Weekly counts and share','t2-weekly','Gaza-week; partial marked; master pooled share'),
('B9','Within-district focal prevalence','t2-district-shares','District-week, complete'),
('B10','Spearman / categorical association','t2-association','Gaza-week complete / master political'),
('H1','Period and within-type shares with intervals','t4-period-figure','Master political records'),
('H2','Event-type shares and test residuals','t4-type-test','Master political records'),
('P1','Smaller-class sample sizes','t5-imbalance','Master political subsets'),
('P2','Largest fatality records','t5-fatality-review','Event master'),
('P3','Timing of fatality flags','t5-fatality-time','Master flagged records'),
('P4','Global versus trailing count flags','t5-unusual-weeks','Gaza-week, complete; partial shown'),
('P5','Month-of-week-start totals/share','t5-trends','Gaza-week, complete'),
('P6','Calendar months and weekdays','t5-seasonality','Gaza-week complete / master post-cutoff focal'),
('P7','Count/change autocorrelation','t5-persistence','Gaza-week, complete'),
('P8','District contribution/variability','t5-district-profile','District-week, complete'),
('P9','Groups of weeks','t5-week-clusters','Gaza-week, complete; derived logs/scaling'),
('P10','Full/precision-1 spatial comparison','t5-spatial-map','Land focal incidents and precision-1 subset'),
('P11','Coordinate concentration','t5-concentration','Land focal incidents and precision-1 subset'),
('P12','DBSCAN setting sensitivity','t5-dbscan','Land focal incidents and precision-1 subset'),
]
md(83, '| Figure | Question / evidence | Source and scope |\n|---|---|---|\n' + '\n'.join(f'| {a} | [{b}](#{c}) | {d} |' for a,b,c,d in register) + '\n\nThe 29 figures exceed the eight-visualization minimum. Each retained comparison has a distinct role; duplicated prevalence panels are consolidated into H1/H2 rather than repeated in Task 2.')

# Correct legacy figure numbers in retained titles without changing their substantive content.
for i,a,b in [(20,'Figure 1.','Figure U1.'),(24,'Figure 2.','Figure U2.'),(28,'Figure 3.','Figure U3.')]:
    replace(i,a,b)

def new_cell(kind, text, ident):
    c = {'cell_type':kind,'id':ident,'metadata':{},'source':text.strip()+'\n'}
    if kind=='code': c.update(execution_count=None,outputs=[])
    return c

result=[]
for i in range(1,185):
    if i in {183,184}: continue  # explicit final order below
    if i in omit: continue
    for j,(kind,text) in enumerate(before.get(i,[])):
        result.append(new_cell(kind,text,f'p3-before-{i}-{j}'))
    c=cells[i]
    c['metadata']['phase3_original_cell']=i
    if c['cell_type']=='code':c['outputs']=[];c['execution_count']=None
    result.append(c)
    for j,(kind,text) in enumerate(after.get(i,[])):
        result.append(new_cell(kind,text,f'p3-after-{i}-{j}'))
result.extend([cells[184],cells[183]])
result.append(new_cell('code', '''import platform
from importlib.metadata import version
print("Python", platform.python_version())
for package in ["numpy", "pandas", "matplotlib", "seaborn", "scipy", "scikit-learn"]:
    print(package, version(package))
''', 'p3-runtime'))
result.append(new_cell('markdown',refs,'p3-references'))

# Serialize sources as standard line arrays and keep IDs stable for retained cells.
for c in result:
    if isinstance(c['source'],str): c['source']=c['source'].splitlines(keepends=True)
    if 'id' not in c: c['id']='p3-'+hashlib.sha256(''.join(c['source']).encode()).hexdigest()[:12]
original['cells']=result
original['metadata']['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}
draft=WORK/'revision.candidate.ipynb'
draft.write_text(json.dumps(original,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
(WORK/'revision_map.json').write_text(json.dumps([
    {'position':i,'id':c['id'],'original_cell':c['metadata'].get('phase3_original_cell'),'type':c['cell_type']}
    for i,c in enumerate(result,1)],indent=2))
(WORK/'consolidation_log.json').write_text(json.dumps({'omitted_original_cells':sorted(omit),'retained_figures':register,'authorization':'User explicitly authorized all listed revisions, interpretation rewrites, code/plot/output changes and validation rerun on November 19, 2026.'},indent=2))
print('Built candidate:',len(result),'cells;',sum(c['cell_type']=='code' for c in result),'code cells')
print(draft)
