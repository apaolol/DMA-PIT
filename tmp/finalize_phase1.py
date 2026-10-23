import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'DMA.ipynb'
old = json.loads(path.read_text(encoding='utf-8'))
cells = []
def md(s):
    cells.append({'cell_type':'markdown','id':f'phase1-{len(cells):02d}','metadata':{},'source':s.strip()+'\n'})
def code(s):
    cells.append({'cell_type':'code','id':f'phase1-{len(cells):02d}','metadata':{},'source':s.strip()+'\n','execution_count':None,'outputs':[]})

md('''# Patterns of Recorded Civilian Targeting in Gaza and the West Bank
## Phase 1: Dataset Selection and Business Problem
**DS312 - Data Mining and Application | Group 7 | A.Y. 2026-2027**  
**Finalized:** October 23, 2026

This project examines the recurrence, geographic concentration, methods, and recorded actor involvement in events targeting Palestinian civilians. It uses ACLED event records from January 1, 2022 to September 30, 2025 to identify places and periods that warrant further human rights investigation.''')

md('''### 1.1 Business Problem Canvas

| Item | Project definition |
|---|---|
| Context / organization | A human rights documentation team monitoring violence affecting Palestinian civilians. This is the proposed stakeholder context, not a claimed agency partnership. |
| Problem statement | Human rights researchers need reproducible evidence about where recorded violence targeting Palestinian civilians recurs and when it becomes unusually intense or persistent. This project will identify geographic concentrations, involved actors, and unusual periods to prioritize further documentary investigation. |
| Stakeholders | Human rights researchers, civilian-protection analysts, investigative journalists, and research coordinators. |
| Decision supported | Which locations, periods, and incident groups should receive closer source verification and contextual investigation? |
| Business questions | BQ1-BQ5 below. |
| Success criteria | Produce interpretable geographic clusters and a documented list of unusual district-weeks; compare results against simple baselines; assess stability across model settings and precision restrictions; and link each investigation recommendation to its supporting records. Report findings that do not remain robust. |
| Task type | Data mining: spatial clustering and temporal anomaly detection. |
| Risks and limitations | Underreporting, changing source coverage, approximate event locations, uncertain dates, structural missingness, and reported fatality estimates. The records do not capture every instance of civilian harm. Statistical patterns alone do not establish intent or criminal responsibility. |

**BQ1.** How do recorded Palestinian civilian-targeting counts and their share of recorded political violence change before and after October 7, 2023, separately in Gaza and the West Bank?

**BQ2.** Which recorded actors and event/sub-event types recur in the focal events, and which actor roles can be supported by the coding and incident notes?

**BQ3.** Where do focal events cluster geographically, and do those concentrations remain evident when location precision and time periods are varied?

**BQ4.** Which district-weeks show unusually high activity or sustained increases relative to earlier local observations?

**BQ5.** How sensitive are the patterns to cohort definitions, baselines, geographic aggregation, and reporting or precision limitations?

Gaza is the primary study area; the West Bank is a separate stratum, not an interchangeable control population. The broader motivation is to examine evidence relevant to systematic attacks on Palestinians. Here, a systematic pattern means measurable recurrence, persistence, concentration, or spread in recorded activity. The project does not use a genocide label or numerical genocide score. Specific intent and legal classification require a separate documentary and legal assessment.''')

md('''### 1.2 Dataset Description

| Attribute | Description |
|---|---|
| Dataset / producer | ACLED (Armed Conflict Location & Event Data), event-level records. |
| Source | [Official Data Export Tool](https://acleddata.com/conflict-data/data-export-tool?grain=disaggregated). |
| Download date | October 18, 2026. |
| Requested coverage | Palestine; January 1, 2022-September 30, 2025; all event types; no actor or civilian-targeting filter; one actor per row disabled; default fatality range 0-4,000. |
| Size | 58,842 records and 31 columns; 58,815 records fall within the land-based Gaza/West Bank scope. |
| Unit of observation | One coded event record. Multiple reported actions can be combined under ACLED's aggregation rules, so a row is not necessarily one attack, weapon release, or victim. |
| Collection method | Trained researchers code reported events using media, institutional reports, local partners, and selected verified sources. |
| Data types | Event identifiers, categorical actor/event/location fields, narrative text, numeric fatality estimates, date strings, coordinates, and precision codes. |
| Local raw file | `data/raw/acled_palestine_events_2022_2025.csv`. |
| Reproducibility | The dated original is preserved; filters and SHA-256 fingerprint are recorded in `data/metadata/acled_events_download_manifest.json`. Historical records may be revised by ACLED. |
| Licence | Subject to ACLED's EULA, Content Usage Terms, and Attribution Policy. The dataset is not licensed CC BY 4.0. Raw-data redistribution requires checking applicable permissions. |

The selected period provides approximately 21 months before October 7, 2023 and two years afterward. It ends at a complete month within the acquired account's available history. Results describe this historical snapshot, not current conditions.''')

md('''### 1.3 Dataset Evaluation and Complexity

ACLED event-level data were selected because actor labels, civilian-targeting flags, incident descriptions, and geographic/date precision directly support the research questions. Weekly aggregated data omit the incident detail required for these questions. The previously considered UCDP-derived source-count dataset supports a different reporting-coverage problem and has different event definitions and coverage; combining its rows with ACLED would risk double counting. ACLED is therefore the principal dataset.

The dataset exceeds the guide's approximate minimums of 5,000 rows and 10 columns and connects to a concrete investigation-prioritization decision. It is feasible for the project because the scope is bounded and two complementary technique families address the questions.

**Dataset Complexity Statement.** This is one principal dataset containing 58,842 records and 31 fields, including narratives, dates, geospatial information, actor variants, and patterned missingness. All 58,842 `admin3` values are absent; 12,359 second-actor fields are missing; 19,086 records have location precision codes above 1; 308 have date precision codes above 1; and 27 maritime records fall outside the land-based scope. There are no exact duplicate rows or repeated event IDs. These issues require domain-aware interpretation, reversible actor mappings, explicit scope rules, and precision-sensitive analysis. They support an advanced-complexity proposal, with the final tier dependent on how well the issues are handled and assessed by the instructor.''')

md('''### 1.4 Initial Data Load

The following cells load and inspect the original CSV. Type parsing and scope checks use an in-memory copy; the raw file is not modified. The notebook runs from the project folder or any child folder with `pandas` and Jupyter/IPython installed.''')

code('''from pathlib import Path
import hashlib
import json
import pandas as pd
from IPython.display import display

ROOT = next((p for p in [Path.cwd(), *Path.cwd().parents]
             if (p / 'data/raw/acled_palestine_events_2022_2025.csv').is_file()), None)
if ROOT is None:
    raise FileNotFoundError('Run this notebook from the project folder containing data/raw/.')
DATA_PATH = ROOT / 'data/raw/acled_palestine_events_2022_2025.csv'
raw = pd.read_csv(DATA_PATH, low_memory=False)
raw_hash = hashlib.sha256(DATA_PATH.read_bytes()).hexdigest()
manifest = json.loads((ROOT / 'data/metadata/acled_events_download_manifest.json').read_text(encoding='utf-8'))
assert raw_hash == manifest['sha256'], 'CSV differs from the documented download.'
assert raw.shape == (manifest['rows'], len(manifest['columns'])), 'Download dimensions differ from manifest.'
print('Source: ACLED | Downloaded October 18, 2026')
display(raw.head())''')
code('''print('Dataset shape:', raw.shape)
raw.info()''')
code('''profile = pd.DataFrame({
    'field': raw.columns,
    'observed_type': [str(raw[c].dtype) for c in raw],
    'missing_count': [int(raw[c].isna().sum()) for c in raw],
    'missing_percent': [round(100 * raw[c].isna().mean(), 2) for c in raw],
    'distinct_values': [int(raw[c].nunique()) for c in raw],
})
display(profile)
print('Exact duplicate rows:', int(raw.duplicated().sum()))
print('Repeated event IDs:', int(raw.event_id_cnty.duplicated().sum()))
print('Event-date range:', raw.event_date.min(), 'to', raw.event_date.max())
display(raw.groupby(['country', 'admin1'], dropna=False).size().rename('records').reset_index())''')

dictionary = ''.join(old['cells'][9]['source'])
dictionary = dictionary.replace('### 1.6 Data dictionary','### 1.5 Data Dictionary')
dictionary = dictionary.replace('The **observed dtype and missingness** are shown above. The types below describe analytical meaning; integer codes are categories, not continuous measurements.', 'The profile above reports actual imported types and missingness. The types below describe analytical meaning; numeric identifiers and precision codes are not continuous measurements.')
md(dictionary)

md('''### 1.6 Scope and Initial Feasibility Findings

The primary candidate cohort consists of in-scope events carrying the `Civilian targeting` label and the recorded actor label `Civilians (Palestine)`. It remains a coded subset of recorded events, not a complete measure of harm to Palestinian civilians. Cohort membership and actor roles will be validated during preprocessing.

The original 27 maritime records will be retained in the raw file and excluded from the land-based analysis. Missing actor/association fields and the blank targeting flag must be interpreted using the codebook, not filled with invented identities or treated as proof that civilians were unharmed. The completely absent `admin3` field will not be imputed into fictitious locations.''')
code('''inspection = raw.copy()
inspection['date_parsed'] = pd.to_datetime(raw.event_date, errors='coerce')
in_scope = raw.country.eq('Palestine') & raw.admin1.isin(['Gaza Strip', 'West Bank'])
scoped = inspection.loc[in_scope].copy()
target_flag = scoped.civilian_targeting.eq('Civilian targeting')
palestinian_civilian_label = (
    scoped.actor1.fillna('').eq('Civilians (Palestine)') |
    scoped.actor2.fillna('').eq('Civilians (Palestine)')
)
candidate = scoped.loc[target_flag & palestinian_civilian_label].copy()
display(pd.DataFrame({
    'in_scope_events': scoped.groupby('admin1').size(),
    'candidate_targeting_events': candidate.groupby('admin1').size(),
}))
print('Candidate cohort:', len(candidate))
print('Invalid dates:', int(inspection.date_parsed.isna().sum()))
print('Location precision codes:')
display(pd.crosstab(scoped.admin1, scoped.geo_precision))
candidate_periods = candidate.assign(period=candidate.date_parsed.ge('2023-10-07').map({False: 'Before Oct 7, 2023', True: 'Oct 7, 2023 onward'}))
display(pd.crosstab(candidate_periods.admin1, candidate_periods.period))
assert hashlib.sha256(DATA_PATH.read_bytes()).hexdigest() == raw_hash, 'Original file was modified.' ''')
md('''The candidate cohort contains **17,047 records**: 10,714 in Gaza and 6,333 in the West Bank. Both regional subsets retain substantial event volume. Gaza has only 63 candidate events before October 7, 2023, compared with 10,651 afterward, so temporal models need explicit sparse-baseline treatment. These are feasibility observations, not evidence of causation or a legal finding.''')

md('''### 1.7 Preliminary Data Mining Plan

**Preparation.** Parse dates; validate event IDs, categories, coordinates, and scope; distinguish structural absence from missing information; and retain original actor labels alongside any reviewed groupings. Analyse Gaza and the West Bank separately. Review actor-role rules before attributing actions. Precise-looking coordinates may still be named-place centroids.

**Analysis tables.** Prepare an incident table for geographic analysis and a district-week table for temporal analysis. Candidate features include week/month, period, targeting counts, total recorded political-violence counts, targeting shares, active weeks, lagged counts, and trailing four-week activity. Define denominator and numerator from the same area-period population. Distinguish zero recorded activity from uncertain coverage before completing absent district-week combinations.

| Technique family | Candidate methods/settings | Reason for use | Baseline and evaluation |
|---|---|---|---|
| Spatial clustering | DBSCAN with haversine distance; radii 2, 5, 10 km and minimum points 5 or 10. Compare settings, time periods, and higher-precision subsets. | Identify concentrations of recorded focal events and describe their persistence and composition. | Compare with simple district/grid summaries. Assess cluster size, noise, interpretability and stability. Repeated centroid coordinates must not be mistaken for repeated attacks on one building. |
| Temporal anomaly detection | Trailing median/MAD with 26/52-week windows; compare Isolation Forest using contamination settings 0.01/0.05. | Identify unusual district-week intensity and sustained increases. | Compare with a trailing historical quantile rule. Assess agreement, alert runs, parameter sensitivity and source-reviewed examples; no verified genocide/anomaly labels are available for accuracy claims. |

**Validation and leakage control.** Use 2022 for initial calibration, January-September 2023 for parameter selection, and October 7, 2023-September 2025 for chronological evaluation of prospectively framed alerts. Handle October 1-6 and boundary weeks explicitly. Use preceding observations only for rolling reference windows; fit transformations on training data. For sparse or zero-MAD baselines, define a fallback count/quantile rule and compare windows. Spatial exploration of the full period is retrospective and will be labelled accordingly.

**Interpretation.** Report effect sizes and uncertainty, keep spatial/temporal dependence in resampling, and test sensitivity to recording precision. Fatalities are reported event totals rather than automatically Palestinian civilian deaths. Predicting targeting from fields that already encode its label would be circular and is not the primary task. The final outputs will be cluster maps, event timelines, model comparisons and a traceable investigation shortlist.''')

md('''### 1.8 References

1. ACLED. *Palestine event-level records, January 1, 2022-September 30, 2025*. Downloaded October 18, 2026 through the [Data Export Tool](https://acleddata.com/conflict-data/data-export-tool?grain=disaggregated). Source: ACLED (Armed Conflict Location & Event Data).
2. ACLED. [Codebook](https://acleddata.com/methodology/acled-codebook) and [Fatalities methodology](https://acleddata.com/methodology/fatalities). Definitions and interpretation limitations.
3. ACLED. [Export Tool guide](https://acleddata.com/use-access/data-export-tool-user-guide), [Terms and Conditions](https://acleddata.com/terms-and-conditions), and [Attribution Policy](https://acleddata.com/attributionpolicy).
4. DS312. *Final Project Guide*, A.Y. 2026-2027, pp. 1-3: Phase 1 requirements and dataset-selection criteria. Supplied course document.

Documentation consulted October 18, 2026. **Dataset/problem approval: awaiting instructor consultation.**''')

old['cells'] = cells
path.write_text(json.dumps(old,indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
print('Finalized notebook:',len(cells),'cells;',sum(c['cell_type']=='code' for c in cells),'code cells')
