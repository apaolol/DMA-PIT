from workflow import *
run([
md('''# Phase 4 - Recorded places and unusual weeks in Gaza
**DS312, Group 7 | Historical ACLED snapshot | November 24, 2026**

## S1. Purpose and reading guide
We group nearby recorded places with **DBSCAN** and screen completed district-weeks against earlier local activity. These complementary families support documentary review: where to look and which weeks deserve context. Neither estimates unrecorded harm, intent or legal responsibility.

Read S2 for inputs and validation, S3-S4 for geography, S5-S6 for unusual weeks, and S7 for findings and recommendations. Figure and table names are readable citations; use the notebook Outline to navigate. Phase 1-3 notebooks and source data are preserved. This separate report does not integrate all phases.

The rubric requires two families, a simple baseline, at least two settings per family, appropriate evaluation, interpretation, limitations and 3-5 recommendations. S4 compares geography with district totals; S5 supplies the simple temporal baseline. Without verified review labels, accuracy, F1 and causal claims would be inappropriate.'''),
md('''## S2. Inputs, timing and frozen design
Phase 2 created the four CSVs; Phase 3 loaded them without changing their populations. We verify those definitions again below. Files overlap and must not be added together.

| Input | Row and scope | Key | Useful information |
|---|---|---|---|
| events_clean | One Gaza-coded event, 2022-01-01 to 2025-09-30; includes coast | event ID | Cohort, district, political denominator, source/notes |
| gaza_week | One post-cutoff Gaza calendar week, including zeros/coast | area, Saturday | Context and reconciliation |
| district_week | One known district/calendar week, including zeros/coast | district, Saturday | Counts, shares and eligible history |
| focal_incidents | One post-cutoff land focal event | event ID | Coordinates, precision and traceability |

Focal means targeting flagged **and** the exact `Civilians (Palestine)` actor label in either actor field. Land excludes location labels starting `Coast of`; it is a coding rule, not a coastline test. Political violence is the recorded disorder label. Missing districts stay in Gaza totals.

| Feature | Available | Use / missing rule |
|---|---|---|
| Latitude/longitude in radians | Snapshot | Spatial distance only; Earth radius 6371.0088 km |
| Current focal/political count and share | After week closes | Screen current week; share undefined if political count is zero |
| Previous-week count / previous-four-week sum | Before current week | Require every preceding calendar week eligible; never bridge gaps |
| District | Snapshot | Separate temporal models, descriptive profiles |
| ID, source and notes | Snapshot | Traceability only; never distance or predictor inputs |

**Frozen before fitting:** spatial radii 0.5/0.75/1/1.25/1.5/2/3 km, min_samples 10/50, full and precision-1 populations. Retain 1 km/50 as a descriptive reference at the center of the neighboring 0.75-1.25 km check, not as an optimum; reject a single robust partition claim if it is unstable. Silhouette is a diagnostic, not a selection target. Compare precision and two equal-duration spatial time blocks separately.

Temporal windows are 8/12/16 earlier calendar weeks, |modified z| > 3.5, count MAD floor 1; shares use no count floor and flat shares are unscored. Keep 12 weeks as the prespecified middle-window reference, and report all windows on common coverage. Thresholds and windows will not be tuned against assessment outcomes.

Chronological blocks: first 52 completed weeks establish history, next 26 weeks provide internal tuning, remaining completed weeks provide retrospective assessment. Rolling baselines use only preceding eligible observations, including earlier assessment weeks as time advances. Optional Isolation Forest uses fixed district-specific fits on the first block, two small feature subsets and max_samples 32/auto; at least 40 complete eligible training rows required. Cutoffs use the 90th percentile of earlier tuning anomaly scores (a review budget, not an anomaly prevalence estimate). Choose the smallest feature subset and then the max_samples setting closest to the 10% tuning burden; ties favor 32. Freeze before assessment. No imputation/scaling is needed for these finite count features and tree models. This fixed-origin detector is an earlier-only comparison to rolling baselines.

**All these historical dates were already explored in Phase 3.** Later blocks are internal retrospective checks, not untouched final tests. New data and independent review are required for unseen evaluation. Alerts are issued after a completed week, not forecasts.'''),
code('''import os, sys, json, hashlib, platform
from pathlib import Path
os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sklearn
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score, adjusted_rand_score
from IPython.display import display, Markdown
%matplotlib inline
ROOT=Path.cwd()
assert (ROOT/'data/processed').is_dir(), 'Run from project root'
OUT=ROOT/'task4 tasks/implementation'
SEED=42; EARTH_KM=6371.0088
plt.rcParams.update({'figure.dpi':115,'axes.titlesize':11,'axes.labelsize':10,'font.size':10})
pd.set_option('display.max_columns',20)
pd.set_option('display.max_colwidth',90)
def report(text): display(Markdown(text))
def table(df,name):
    print(name); display(df)
    df.to_csv(OUT/(name.split(':')[0].replace(' ','_')+'.csv'),index=False)
def figure(fig,name):
    fig.tight_layout();fig.savefig(OUT/(name+'.png'),dpi=140,bbox_inches='tight');plt.show()
protected=json.loads((OUT/'protected_hashes.json').read_text())
def verify_protected():
    assert all(hashlib.sha256((ROOT/Path(p)).read_bytes()).hexdigest()==v for p,v in protected.items()), 'Protected file changed'
verify_protected()
print('Runtime:',sys.version.split()[0], '| pandas',pd.__version__,'| numpy',np.__version__,'| sklearn',sklearn.__version__)
(OUT/'runtime.json').write_text(json.dumps({'python':sys.version,'executable':sys.executable,'pandas':pd.__version__,'numpy':np.__version__,'sklearn':sklearn.__version__,'seed':SEED},indent=2))
def load(name,dates):
    df=pd.read_csv(ROOT/'data/processed'/name,parse_dates=dates)
    for c in df.columns:
        if c in ['complete_week','history_eligible','political_activity_recorded','targeting_flagged','political_violence','focal_event','geo_precision_1','time_precision_1','coastal_location','land_spatial_eligible','district_missing','high_fatalities_review']:
            vals=df[c].astype(str);assert vals.isin(['True','False']).all();df[c]=vals.map({'True':True,'False':False}).astype(bool)
    for c in ['geo_precision','time_precision']:
        if c in df:
            assert df[c].isin([1,2,3]).all();df[c]=pd.Categorical(df[c],categories=[1,2,3],ordered=True)
    return df
master=load('acled_events_clean.csv',['event_date','month_start','week_start'])
gw=load('acled_gaza_week.csv',['week_start','week_end'])
dw=load('acled_district_week.csv',['week_start','week_end'])
inc=load('acled_focal_incidents.csv',['event_date','month_start','week_start'])
assert [x.shape for x in [master,gw,dw,inc]]==[(26664,43),(104,13),(520,14),(10583,45)]
assert master.admin1.eq('Gaza Strip').all() and master.event_id_cnty.is_unique
assert master.targeting_flagged.equals(master.civilian_targeting.eq('Civilian targeting'))
focal=master.targeting_flagged & (master.actor1.eq('Civilians (Palestine)')|master.actor2.eq('Civilians (Palestine)'))
assert master.focal_event.equals(focal)
assert master.political_violence.equals(master.disorder_type.str.split(';').apply(lambda a:'Political violence' in [s.strip() for s in a]))
assert master.loc[focal,'political_violence'].all()
assert master.coastal_location.equals(master.location.str.startswith('Coast of'))
post=master.event_date.ge('2023-10-07')
assert master.land_spatial_eligible.equals(post & focal & ~master.coastal_location)
assert inc.event_id_cnty.tolist()==master.loc[master.land_spatial_eligible,'event_id_cnty'].tolist()
assert np.allclose(inc[['latitude_rad','longitude_rad']],np.radians(inc[['latitude','longitude']]))
assert inc.latitude.between(-90,90).all() and inc.longitude.between(-180,180).all()
assert inc.geo_precision_1.equals(inc.geo_precision.eq(1))
for w,area in [(gw,'admin1'),(dw,'admin2')]:
    assert not w.duplicated([area,'week_start']).any()
    assert w.week_end.equals(w.week_start+pd.Timedelta(days=6))
    assert w.complete_week.equals(w.week_end.le('2025-09-30'))
    assert w.history_eligible.equals(w.complete_week & w.political_events.gt(0))
    assert np.allclose(w.focal_share,w.focal_events/w.political_events.where(w.political_events.gt(0)),equal_nan=True)
    assert w.focal_events.le(w.political_events).all()
    for _,g in w.groupby(area):
        g=g.sort_values('week_start');h=g.focal_events.where(g.history_eligible)
        assert g.week_start.diff().dropna().eq(pd.Timedelta(days=7)).all()
        for c,expected in [('focal_count_for_history',h),('previous_week_focal',h.shift(1)),('previous_four_weeks_focal',h.shift(1).rolling(4).sum())]:
            assert np.allclose(g[c],expected,equal_nan=True)
    source=master.loc[post & master[area].notna()]
    expected=source.groupby([area,'week_start']).agg(recorded_events=('event_id_cnty','size'),political_events=('political_violence','sum'),focal_events=('focal_event','sum'))
    actual=w.set_index([area,'week_start'])[expected.columns]
    assert actual.equals(expected.reindex(actual.index,fill_value=0).astype(actual.dtypes))
weeks=sorted(gw.loc[gw.complete_week,'week_start'])
TRAIN_END=weeks[51]; TUNE_END=weeks[77]; ASSESS_START=weeks[78]
def block(date): return 'history' if date<=TRAIN_END else ('tuning' if date<=TUNE_END else 'assessment')
dw['block']=dw.week_start.map(block)
blocks=pd.DataFrame([{'block':n,'start':min(v),'last_week_start':max(v),'weeks':len(v)} for n in ['history','tuning','assessment'] if (v:=[d for d in weeks if block(d)==n])])
table(blocks,'Table 1: Chronological blocks')
table(dw.loc[~dw.complete_week,['admin2','week_start','week_end','focal_events','political_events']],'Table 2: Excluded partial weeks')
pops=pd.DataFrame({'population':['Gaza master','Gaza weeks','District weeks','Land focal','Precision-1 land focal'],'rows':[len(master),len(gw),len(dw),len(inc),int(inc.geo_precision_1.sum())]})
table(pops,'Table 3: Population accounting')
print('Missing district focal post-cutoff:',int(master.loc[post & master.admin2.isna(),'focal_event'].sum()))
print('All input, reconciliation, eligibility and lag assertions passed.')
'''),
md('''**Input interpretation (Tables 1-3).** The last week starts September 27, 2025 and is incomplete; all five district rows are excluded from scoring. Zero counts remain in the calendar, but a zero political denominator makes a share undefined and its count ineligible as local history. The three post-cutoff focal events without districts remain in Gaza totals. Table 1 fixes the chronological dates before modeling.''')
],2)
complete(2,'DMA_Phase4_Modeling.ipynb S1-S2 executed; all four shapes, cohort, land/radians, weekly counts, missing-district reconciliation and eligible lag assertions passed. Tables 1-3 record actual populations, excluded partial weeks and chronological dates. Design frozen before fitting; historical exploration disclosed.')
