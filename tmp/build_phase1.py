import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cells = []

def md(text):
    cells.append({'cell_type': 'markdown', 'id': f'p1-{len(cells):02d}', 'metadata': {}, 'source': textwrap.dedent(text).strip() + '\n'})

def code(text):
    cells.append({'cell_type': 'code', 'id': f'p1-{len(cells):02d}', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': textwrap.dedent(text).strip() + '\n'})

md('''
# Patterns of Recorded Violence Affecting Palestinians
## Phase 1: Dataset Selection and Business Problem
**DS312 - Data Mining and Application | Group 7 | A.Y. 2026-2027**  
**Prepared:** October 18, 2026 (Asia/Singapore)  
**Group deadline:** October 25, 2026  
**Team members and instructor approval:** To be supplied by the group.

This project examines the persistence, composition, and temporal concentration of recorded violence in Gaza and the West Bank. Its purpose is to support human rights researchers in identifying periods that warrant closer investigation and triangulation with documentary evidence.

**Data source: ACLED (Armed Conflict Location & Event Data), downloaded October 18, 2026.**

> **Important acquisition finding:** The signed-in account could download weekly aggregated data, but the event-level export displayed a request for additional access. The CSV used here is a genuine ACLED aggregate export, not individual incident records. It has no actor names, event IDs, narrative notes, or comprehensive civilian-targeting flag. The questions below are deliberately restricted to what the downloaded data can support. Actor attribution and incident-level clustering remain dependent on additional access.
''')

md('''
### 1.1 Research purpose and connection to genocide evidence

**Proposed research question:** How do the frequency, persistence, and composition of recorded violence in Gaza change after October 7, 2023, compared with earlier periods, and how do the patterns differ from the West Bank?

The broader motivation is to examine evidence relevant to allegations of systematic attacks on Palestinians. In this study, *systematic pattern* is an operational description of repeated or sustained recorded activity, not a legal classification. We will measure active weeks, consecutive runs, changes in weekly counts, event-type composition, and reported fatalities. We will not assume the outcome before examining the data.

Genocide requires prohibited acts together with specific intent to destroy a protected group, in whole or in part. Statistical patterns can contribute contextual evidence, but do not by themselves establish intent. The UN Independent International Commission of Inquiry concluded in September 2025 that Israel had committed genocide in Gaza. That is the Commission's attributed legal assessment, not a finding produced by this notebook and not a substitute for analysing statements, policies, orders, and conduct.

The quantitative component will therefore examine recorded patterns. A separate evidence discussion can map the findings and their limitations to the Commission's legal framework. There is no invented genocide score, no genocide/not-genocide training label, and no claim that a high anomaly score proves intent.

Sources: [UN Commission of Inquiry, A/HRC/60/CRP.3](https://www.un.org/unispal/document/commission-of-inquiry-report-genocide-in-gaza-a-hrc-60-crp-3/); [ACLED fatalities methodology](https://acleddata.com/methodology/fatalities).
''')

md('''
### 1.2 Business Problem Canvas

| Required item | Project definition |
|---|---|
| Context / organization | A hypothetical human rights research and civilian-protection monitoring team. No actual agency partnership is claimed. |
| Problem statement | Researchers need reproducible evidence about when recorded violence against civilians and other forms of political violence become unusually intense or persistent. This project will identify and compare sustained periods and unusual weeks in Gaza and the West Bank to guide subsequent documentary investigation. |
| Stakeholders | Human rights researchers, civilian-protection analysts, investigative journalists, and research coordinators. |
| Decision supported | Which periods and broad regional patterns should receive closer verification and supplementary evidence collection? |
| Business questions | BQ1-BQ5 below. |
| Success criteria | Reproducible scope and quality checks; interpretable weekly profiles; comparison of two technique families with explicit baselines; sensitivity checks; and traceable recommendations for further investigation. Useful results include a finding that a proposed pattern is not robust. |
| Task type | Data mining: clustering and temporal anomaly detection. Any later predictive model is optional. |
| Risks and limitations | Aggregation removes incident detail and actors. Recorded events are affected by reporting and coding. Absence of a row is not proof that no harm occurred. Two regional centroids cannot reveal local attack hotspots. Reported fatalities do not identify all civilian victims. |

**BQ1.** How do weekly political-violence counts and reported fatalities change before and after October 7, 2023, separately in Gaza and the West Bank?

**BQ2.** How persistent are weeks containing the coded *Violence against civilians* event type, and how do event-type shares change across periods?

**BQ3.** Which weeks have unusually high counts or fatalities relative to a trailing historical baseline, and which form sustained runs rather than isolated peaks?

**BQ4.** Can weeks be grouped into interpretable profiles using violence counts and event-type composition, and do profile frequencies change across periods?

**BQ5.** Do the apparent patterns persist under alternative baselines, boundary-week exclusions, missing-row assumptions, and separate regional analyses?

**Interpretation rule:** The *Violence against civilians* event type is narrower than all civilian targeting, which can also be coded under other event types. The aggregate cannot recover the missing targeting flag. Country and region identify where events were coded, not the identity or nationality of every victim or perpetrator.
''')

md('''
### 1.3 Candidate problems and dataset evaluation

This is a documented analytical comparison for the group's review. It does not claim that a team brainstorming meeting or instructor consultation has already occurred.

| Candidate | Decision and analytical value | Limitations | Selection |
|---|---|---|---|
| ACLED event-level: repeated civilian targeting | Most direct of these options for actor, incident, and targeting analysis. | Event-level access was unavailable to the signed-in account on October 18. Its row count and missingness have not been measured. | Preferred extension, not falsely claimed as acquired. |
| ACLED aggregated: persistence and escalation | Downloaded official CSV; permits longitudinal comparison, weekly profiles, and anomaly detection. | Coarse geography; no actors or targeting flag. Cannot establish attack attribution, intent, or infrastructure destruction. | Selected feasible Phase 1 dataset, subject to instructor approval of the revised scope. |
| Existing UCDP-derived ConflictStats CSV: reporting coverage | Already available locally; 5,282 rows and 17 columns with event locations, fatality estimates, and source counts. | Different event definitions and reporting scope; source counts cannot establish media bias. Does not by itself answer the new broader question. | Retained unchanged as an evaluated alternative, not merged with ACLED event counts. |

UNOSAT structural damage and WHO healthcare-attack data would be valuable extensions for the wider genocide-evidence question. They have not been acquired or joined in this Phase 1 submission. Their proposed use does not imply that the ACLED CSV measures infrastructure destruction.

The long requested baseline (2016-2026) allows comparison with multiple earlier periods rather than treating 2022-2023 as a universal normal. It is not a claim that coverage, population, or reporting conditions are constant across ten years. A shorter 2022-September 2026 aggregate query returned 3,921 rows in the website preview, below the guide's approximate minimum. The final export covers the longer, substantively useful history; rows have not been duplicated or expanded to manufacture volume.
''')

md('''
### 1.4 Acquisition, provenance, and access

| Item | Recorded information |
|---|---|
| Producer | ACLED (Armed Conflict Location & Event Data). |
| Download route | Signed-in official Data Export Tool, **Aggregated** tab, Download CSV. |
| Requested filters | Country: Palestine; January 1, 2016 through September 30, 2026; all event types; no actor filter. |
| Download date | October 18, 2026, Asia/Singapore. |
| Local original | `data/raw/acled_palestine_aggregated_2016_2026.csv` (byte-preserved copy of the browser download). |
| Unit of observation | One populated week x Admin1 x event-subtype aggregate, with its event and disorder categories. One row can represent many incidents. |
| Collection method | ACLED researchers code reported incidents; the platform aggregates them. Researchers use media, institutional reporting, and local sources. These are recorded observations, not a census of every act of violence. |
| Update policy | ACLED is revised over time. This project freezes a dated download and records its SHA-256 fingerprint. |
| Licence | ACLED EULA, Content Usage Terms, and Attribution Policy. **Do not label this CSV CC BY 4.0.** Local academic analysis is distinct from redistributing the raw dataset. Check account/institutional permissions before public release. |

Sources: [Data Export Tool guide](https://acleddata.com/use-access/data-export-tool-user-guide), [aggregate schema](https://acleddata.com/use-access/how-use-acleds-aggregated-data), [terms](https://acleddata.com/terms-and-conditions), [attribution](https://acleddata.com/attributionpolicy).

The aggregate guide calls its exposure measure `population_best`; this actual download calls it `population_exposure`. We preserve the actual header and record that documentation difference. Exposure is not a unique-victim count or an appropriate population denominator, and will not be summed across rows or weeks.
''')

md('''
### 1.5 Initial data load

Run this notebook from the project folder, or any child folder. Only `pandas` and the normal Jupyter/IPython environment are needed. The cells load the saved CSV without network requests or account credentials. They inspect the original without overwriting it.
''')

code('''
from pathlib import Path
import hashlib
import json
import platform
import pandas as pd
from IPython.display import display, Markdown

roots = [Path.cwd(), *Path.cwd().parents]
ROOT = next((p for p in roots if (p / 'data/raw/acled_palestine_aggregated_2016_2026.csv').is_file()), None)
if ROOT is None:
    raise FileNotFoundError('Open the notebook from the DMA PIT project folder containing data/raw/.')
DATA_PATH = ROOT / 'data/raw/acled_palestine_aggregated_2016_2026.csv'
MANIFEST_PATH = ROOT / 'data/metadata/acled_download_manifest.json'
raw = pd.read_csv(DATA_PATH)
original_hash = hashlib.sha256(DATA_PATH.read_bytes()).hexdigest()
print('Source: ACLED; downloaded October 18, 2026; weekly aggregated data.')
print('Python:', platform.python_version(), '| pandas:', pd.__version__)
print('File:', DATA_PATH.name)
print('SHA-256:', original_hash)
display(raw.head())
''')

code('''
print('raw.shape:', raw.shape)
print('Rows are aggregates, NOT individual incidents. Columns:', len(raw.columns))
raw.info()
''')

code('''
expected = {'week', 'region', 'country', 'admin1', 'event_type', 'sub_event_type',
            'events', 'fatalities', 'population_exposure', 'disorder_type',
            'centroid_latitude', 'centroid_longitude'}
assert expected.issubset(raw.columns), f'Missing required columns: {expected - set(raw.columns)}'
assert len(raw) > 0, 'The downloaded file contains no data.'
schema = pd.DataFrame({
    'column': raw.columns,
    'observed_dtype': [str(raw[c].dtype) for c in raw],
    'null_cells': [int(raw[c].isna().sum()) for c in raw],
    'blank_or_whitespace_cells': [int(raw[c].astype('string').str.fullmatch(r'\\s*', na=False).sum()) for c in raw],
    'distinct_non_null': [int(raw[c].nunique(dropna=True)) for c in raw]
})
display(schema)
print('Exact duplicate rows:', int(raw.duplicated().sum()))
print('Duplicate aggregate keys:', int(raw.duplicated(['week', 'country', 'admin1', 'event_type', 'sub_event_type']).sum()))
display(raw.groupby(['region', 'country', 'admin1'], dropna=False).size().rename('aggregate_rows').reset_index())
''')

md('''
### 1.6 Data dictionary for the downloaded file

| Column | Intended analytical type | Meaning and use |
|---|---|---|
| `week` | Date | Saturday bucket label; not an incident date. |
| `region` | Category | Broad geographic area. |
| `country` | Category | Coded territory; used for scope. |
| `admin1` | Category | Broad administrative area. |
| `event_type` | Category | Broad event class. |
| `sub_event_type` | Category | More detailed event class. |
| `events` | Integer count | Recorded incidents represented by row. |
| `fatalities` | Integer estimate | Reported deaths across represented incidents. |
| `population_exposure` | Numeric estimate | Exposure measure; do not sum. |
| `disorder_type` | Category/multiple labels | Higher-level grouping. |
| `centroid_latitude` | Numeric coordinate | Administrative centroid, not attack location. |
| `centroid_longitude` | Numeric coordinate | Administrative centroid, not attack location. |

Definitions: [ACLED aggregate documentation](https://acleddata.com/use-access/how-use-acleds-aggregated-data). Numeric-looking source strings and dates are parsed only in an in-memory audit copy below. Full cleaning belongs in Phase 2.
''')

code('''
# Audit copy only; preserve original CSV bytes and raw values.
audit = raw.copy()
audit['week_parsed'] = pd.to_datetime(raw['week'], errors='coerce')
audit['exposure_numeric'] = pd.to_numeric(raw['population_exposure'].astype('string').str.replace(',', '', regex=False), errors='coerce')
scope_mask = audit['country'].eq('Palestine') & audit['admin1'].isin(['Gaza Strip', 'West Bank'])
scoped = audit.loc[scope_mask].copy()
outside = audit.loc[~scope_mask].copy()
start = pd.Timestamp('2016-01-01')
end = pd.Timestamp('2026-09-30')
scoped['bucket_end'] = scoped['week_parsed'] + pd.Timedelta(days=6)
interior = scoped.loc[scoped['week_parsed'].ge(start) & scoped['bucket_end'].le(end)].copy()

summary = pd.DataFrame([
    ('Downloaded aggregate rows', len(raw)),
    ('Downloaded columns', len(raw.columns)),
    ('Rows in Palestine / Gaza or West Bank', len(scoped)),
    ('Out-of-scope rows retained in original', len(outside)),
    ('Interior full-week aggregate rows', len(interior)),
    ('Boundary-week rows excluded from interior view', len(scoped) - len(interior)),
    ('Distinct weekly labels in raw file', raw['week'].nunique()),
    ('Invalid dates', audit['week_parsed'].isna().sum()),
    ('Exposure strings containing commas', raw['population_exposure'].astype('string').str.contains(',', regex=False, na=False).sum()),
    ('Unparseable exposure after separator handling', audit['exposure_numeric'].isna().sum()),
], columns=['audit_item', 'observed_value'])
display(summary)
print('Observed raw week labels:', audit.week_parsed.min().date(), 'to', audit.week_parsed.max().date())
print('Complete-week analysis labels:', interior.week_parsed.min().date(), 'to', interior.week_parsed.max().date())
print('Complete-week analysis ends:', interior.bucket_end.max().date())
display(scoped.groupby('admin1').agg(aggregate_rows=('events', 'size'), represented_recorded_events=('events', 'sum')).reset_index())
display(outside.groupby(['region', 'country', 'admin1'], dropna=False).size().rename('outside_scope_rows').reset_index())
''')

md('''
### 1.7 What the first inspection means

The export contains Eastern Mediterranean Sea records even though Palestine was selected. This is an observed scope issue, not evidence of a confirmed ACLED error. Preserve those original rows, log their exclusion from the Palestine analysis, and do not silently treat maritime locations as Gaza.

The requested period begins January 1, 2016, but a weekly label can precede that date because weeks run Saturday-Friday. Similarly, the last requested day falls inside a weekly bucket. We cannot reconstruct exact incident dates from the export. Use the interior full-week view for primary comparisons, and report the boundary exclusion. Do not describe the first bucket as proof that the request downloaded every incident in December 2015.

`population_exposure` contains thousands separators and is read as text. `week` is also initially text. These are genuine type-handling tasks. No missing cells or exact duplicates should be invented: the inspection reports what exists. Combined disorder labels need explicit membership handling rather than assuming every row has one of three mutually exclusive strings.

Only two geographic centroids remain after the scope restriction. Clustering those coordinates would simply recover Gaza versus the West Bank, not identify neighbourhood hotspots. The feasible clustering unit is a weekly violence profile.
''')

code('''
diagnostics = {
    'null_cells': int(raw.isna().sum().sum()),
    'negative_event_counts': int((pd.to_numeric(raw.events, errors='coerce') < 0).sum()),
    'negative_fatality_estimates': int((pd.to_numeric(raw.fatalities, errors='coerce') < 0).sum()),
    'non_saturday_labels': int((audit.week_parsed.dt.dayofweek.ne(5) & audit.week_parsed.notna()).sum()),
    'zero_event_rows': int((raw.events == 0).sum()),
    'distinct_in_scope_centroids': int(scoped[['centroid_latitude', 'centroid_longitude']].drop_duplicates().shape[0]),
    'multiple_disorder_labels': int(raw.disorder_type.str.contains(';', regex=False, na=False).sum()),
}
display(pd.Series(diagnostics, name='observed_count').to_frame())
display(raw['disorder_type'].value_counts(dropna=False).rename_axis('disorder_type').to_frame('aggregate_rows'))
display(raw[['events', 'fatalities']].describe().T)
print('Extreme values are review candidates, not automatic deletion candidates.')
assert hashlib.sha256(DATA_PATH.read_bytes()).hexdigest() == original_hash, 'Raw file changed.'
if MANIFEST_PATH.exists():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
    assert manifest['sha256'] == original_hash, 'Manifest and CSV do not match.'
    print('Download manifest fingerprint verified.')
''')

md('''
### 1.8 Dataset suitability and complexity statement

The following assessment uses the downloaded aggregate, not the event-level schema advertised on another page. Raw row count, analytically scoped row count, and represented incident totals are different quantities.
''')

code('''
criteria = pd.DataFrame([
    ('Approx. 5,000 rows', f'{len(raw):,} downloaded; {len(scoped):,} in geographic scope; {len(interior):,} interior-week rows', 'Meets numerical minimum' if len(interior) >= 5000 else 'Needs instructor review'),
    ('Approx. 10 columns, mixed types', f'{len(raw.columns)} columns; categories, counts, date strings, coordinates', 'Meets numerical minimum'),
    ('Real preprocessing issues', 'Comma-formatted exposure; date parsing; maritime scope; boundary weeks; combined labels; time dependence', 'Observed, but limited missingness/duplicate complexity'),
    ('Real decision relevance', 'Identify sustained periods and weeks for further human rights investigation', 'Fits revised temporal scope'),
    ('Original actor/incident questions', 'Actor names, targeting flag, precision codes, and incident notes absent', 'Not answerable with this export'),
    ('Source documentation', 'Official CSV, filter recipe, acquisition date, fingerprint, definitions, terms', 'Documented'),
    ('Instructor approval', 'No approval is claimed in this notebook', 'Pending'),
], columns=['criterion', 'evidence', 'assessment'])
display(criteria)
display(Markdown(
    f'**Complexity statement.** The downloaded table has **{len(raw):,} rows and {len(raw.columns)} columns**, '
    f'with **{len(scoped):,} geographically relevant rows** and **{len(interior):,} interior-week rows**. '
    f'There are **{diagnostics["null_cells"]:,} null cells** and **{int(raw.duplicated().sum()):,} exact duplicate rows**. '
    'Genuine work includes geographic scope validation, week-boundary treatment, date and numeric parsing, '
    'compound category handling, and interpretation of dependent repeated observations. '
    'The aggregate is structurally fairly clean and lacks event-level text or precise geography. '
    '**We do not claim the advanced tier or a guaranteed score.** Ask the instructor whether this '
    'longitudinal aggregate provides sufficient complexity; event-level access or a justified second source '
    'would strengthen the project. Never add artificial errors or expand rows into synthetic incidents.'
))
''')

md('''
### 1.9 Preliminary data mining plan

**Analysis population.** Preserve all original rows. In Phase 2, make a documented Palestine-only view, remove boundary buckets from primary comparisons, and retain Gaza and the West Bank as separate strata. Analyse political violence as the main population; peaceful demonstrations and strategic developments are context, not interchangeable violence counts. Use membership tests for compound disorder labels. Review subtype-to-event mappings before aggregating.

**Observation units.** Raw rows are week-area-subtype aggregates. Build one interpretable profile per complete week per area: total recorded political-violence events; subtype shares; the count and share coded *Violence against civilians*; active-week indicators; and reported fatalities. Sum event counts, not row counts, when measuring activity. Do not call the narrower event-type share a comprehensive civilian-targeting rate. Fatalities are reported estimates across the row's incidents, not deaths attributed to a particular actor.

**Missing combinations.** Inspect whether absent week/subtype combinations mean zero recorded activity or missing coverage. Make no automatic zero-fill claim in Phase 1. In Phase 2, distinguish a completed recorded-count panel from actual absence of violence, and compare zero-fill and missing-data treatments. Build the Saturday calendar explicitly before measuring consecutive runs.

| Technique family | Candidate methods/settings | Purpose and features | Baseline and evaluation |
|---|---|---|---|
| Clustering | K-means with k=2, 3, 4, 5; compare agglomerative clustering. | Discover weekly profiles from log-transformed counts and event-type shares, separately by area. Run sensitivity with and without fatality estimates. Do not cluster two centroids. | Compare to a single-profile descriptive baseline. Use silhouette where defined, minimum cluster size, profile interpretability, and stability under block resampling/settings. Report time dependence and small effective sample size. |
| Temporal anomaly detection | Trailing median/MAD rule, windows of 26 and 52 weeks; compare Isolation Forest on weekly profiles using contamination 0.01 and 0.05. | Flag unusual weeks and quantify persistence of flagged runs. Inputs and reference distributions must use only preceding observations for prospective evaluation. | Compare with a simple trailing historical quantile rule. Evaluate agreement, sensitivity, alert concentration and run lengths, plus manual review of a documented shortlist. Anomalies have no verified genocide label; no genocide-detection accuracy is reported. |

**Validation.** Use 2016-2021 for initial calibration, 2022 through September 2023 for validation, and October 2023 onward for a chronological evaluation. The transition week containing October 7 must be treated explicitly, not assigned by a monthly shortcut. Keep the final evaluation period untouched when choosing settings. If a model is later refitted to the entire series for descriptive exploration, label that result retrospective and keep it separate from held-out evaluation. Fit scaling, transforms, and imputations inside training only.

The long post-October period may represent a different regime. A model fitted on earlier years can identify departure from its baseline, not prove the cause of the departure. Compare earlier escalation periods and acknowledge changes in recording and conflict conditions.

**Planned statistical questions for Phase 3.** (H1) Weekly violence counts have a different distribution across the pre/post periods within each area. (H2) The proportion of represented political-violence events in the narrower *Violence against civilians* class changes across periods. Account for serial dependence with block resampling or an appropriate count/time-series model; avoid treating thousands of category rows as independent observations. Report effect sizes, uncertainty, multiple-comparison handling, and limitations. A pre/post association is not a causal estimate.
''')

md('''
### 1.10 Interpretation, evidence gaps, and extensions

| Desired claim | What this file can establish | Additional evidence needed |
|---|---|---|
| Violence is repeated or sustained | Persistence of recorded weekly counts and event classes. | Robustness to reporting, temporal baselines, and aggregation choices. |
| A particular actor targeted Palestinian civilians | Not identifiable from this aggregate. | Licensed event-level actor, civilian-targeting and narrative data; source verification. |
| Damage is geographically widespread within Gaza | Not identifiable from one Gaza centroid. | UNOSAT building-level damage layers and denominators. |
| Life-sustaining systems were attacked or deprived | Not measured comprehensively by these fields. | WHO healthcare incidents/functionality, IPC food-security evidence, OCHA access data, and policy chronology. |
| Genocidal intent exists | Not an output of this dataset or anomaly score. | Contextual and legal assessment of acts, statements, orders, policies, conduct, and alternative explanations. |

For an eventual multi-source design, join compatible **area-period aggregates**, not unmatched incident tables. Keep each producer's event totals separate because definitions differ and the same underlying incident can appear in multiple sources. Do not infer a hospital attack from a nearby administrative centroid. Do not infer nationality, combatant status, or intent from age, sex, or location alone.

### 1.11 Deliverables and completion checklist

| Phase 1 requirement | Status in this notebook |
|---|---|
| Problem statement and canvas | Completed for the available aggregate scope. |
| 3-5 specific questions | Five questions, with answerability limits. |
| Dataset comparison and selection reasons | Included; unavailable event-level data explicitly distinguished. |
| Source, size, types, collection, range, licence | Included with actual inspection outputs and provenance manifest. |
| Data dictionary | All 12 downloaded fields covered. |
| At least two candidate technique families | Clustering and temporal anomaly detection, with baselines and validation. |
| Initial `.head()`, `.info()`, `.shape` | Executed above on the actual downloaded CSV. |
| Complexity statement | Evidence-based; no guaranteed tier claimed. |
| Instructor approval | **Pending.** Confirm acceptability of the aggregate's revised scope and complexity. |
| Team names and contributions | Group must supply authentic names and contributions. No individual contribution report is fabricated. |

The group submission deadline is October 25, 2026. The guide gives conflicting individual deadlines (one day after the group deadline in the timeline, three days after in Section 8.1); clarify with the instructor.

**Decision for consultation:** Proceed with the feasible temporal study if the instructor accepts the aggregate. If the central requirement remains attribution of civilian targeting to named actors, obtain event-level access before finalizing; this export cannot answer that question. No conclusion about systematic targeting or genocide is asserted by Phase 1.
''')

md('''
### 1.12 References

1. ACLED. *Palestine weekly aggregated data*. Downloaded October 18, 2026. Requested period: January 1, 2016-September 30, 2026. [Official export tool](https://acleddata.com/conflict-data/data-export-tool?grain=aggregated). File fingerprint and counts are saved in `data/metadata/acled_download_manifest.json`.
2. ACLED. [How to use ACLED's Aggregated Data](https://acleddata.com/use-access/how-use-acleds-aggregated-data). Definitions of row grain, week, centroids, counts, and exposure.
3. ACLED. [Codebook](https://acleddata.com/methodology/acled-codebook) and [Fatalities](https://acleddata.com/methodology/fatalities). Event classes, reporting and fatality limitations.
4. ACLED. [Data Export Tool: User guide](https://acleddata.com/use-access/data-export-tool-user-guide). Access levels and export distinctions.
5. ACLED. [Terms and Conditions](https://acleddata.com/terms-and-conditions), [EULA](https://acleddata.com/eula), and [Attribution Policy](https://acleddata.com/attributionpolicy).
6. UN Independent International Commission of Inquiry. (2025). *Legal analysis of the conduct of Israel in Gaza pursuant to the Convention on the Prevention and Punishment of the Crime of Genocide*, A/HRC/60/CRP.3. [Report](https://www.un.org/unispal/document/commission-of-inquiry-report-genocide-in-gaza-a-hrc-60-crp-3/). Used for attributed legal context, not as a model label.
7. DS312 course materials supplied locally: *[STUDENT] DS312_FINAL_PIT_GUIDE.pdf*, pp. 1-3 (Phase 1), pp. 5-6 (future methods and validation), p. 7 (individual reports); *G7 DS312 PIT TOPICS.pdf* (candidate topics).
8. ConflictStats. [Israel and Palestine: events and estimated deaths recorded by UCDP](https://conflictstats.com/country/israel-and-palestine/). Existing local alternative: `israel-and-palestine (1).csv`; retained separately.

Web documentation consulted October 18, 2026. Source: ACLED. This notebook is a student research proposal, not an ACLED product or an endorsed legal assessment.
''')

nb = {'cells': cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python', 'version': '3'}, 'title': 'DS312 Phase 1 - Patterns of Recorded Violence Affecting Palestinians'}, 'nbformat': 4, 'nbformat_minor': 5}
(ROOT / 'DMA.ipynb').write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
print(f'Created DMA.ipynb: {len(cells)} cells')
