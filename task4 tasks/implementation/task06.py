from workflow import *
run([
md('''## S6. Does Isolation Forest add useful review leads?
Isolation Forest repeatedly splits feature values; records isolated with fewer splits receive stronger anomaly scores. It can find unusual combinations, but does not explain causes or supply verified anomaly labels. We test a small, district-specific design rather than pooling very different districts.

Four candidates use 100 trees, seed 42 and `max_samples` 32/auto, with either **current focal count + previous-week count** or those two plus the **preceding-four-week total**. Counts and shares share a numerator, so this comparison omits political counts and ratios rather than duplicating them. Features are finite raw counts; no learned preprocessing, imputation or scaling is applied. IDs, dates, notes and review flags are excluded.

Fits use only the first 52 weeks, requiring at least 40 eligible finite rows per district. Missing lag history is excluded, not imputed. Models stay fixed during the tuning and assessment blocks. Their alert cutoffs are the 90th percentile of earlier tuning anomaly scores (`higher` quantile, flag strictly above), with at least 15 tuning rows. This implements an approximate 10% review budget without pretending that 10% are true anomalies. The frozen selection rule favors the smallest subset, then tuning burden closest to 10%, then max_samples 32. Assessment outcomes cannot change that choice. This fixed-origin alternative is compared with the rolling 12-week baseline on identical assessable weeks.'''),
code('''from sklearn.ensemble import IsolationForest
FEATURE_SETS={'count_lag1':['focal_events','previous_week_focal'],
              'count_lag1_prior4':['focal_events','previous_week_focal','previous_four_weeks_focal']}
if_models={}; if_candidates=[]; if_coverage=[]; if_tuning=[]
for district,g in dw.groupby('admin2',sort=True):
    g=g.sort_values('week_start')
    for feature_name,features in FEATURE_SETS.items():
        finite=np.isfinite(g[features]).all(axis=1)
        usable=g.history_eligible & finite
        train=g.loc[g.block.eq('history')&usable];tune=g.loc[g.block.eq('tuning')&usable]
        if_coverage.append({'admin2':district,'features':feature_name,'history_calendar_rows':int(g.block.eq('history').sum()),'training_rows':len(train),'tuning_calendar_rows':int(g.block.eq('tuning').sum()),'tuning_rows':len(tune),'excluded_history':int(g.block.eq('history').sum())-len(train),'excluded_tuning':int(g.block.eq('tuning').sum())-len(tune),'feasible':len(train)>=40 and len(tune)>=15})
        if len(train)<40 or len(tune)<15:continue
        assert train.week_start.max()<tune.week_start.min() and tune.week_start.max()<ASSESS_START
        for sample in [32,'auto']:
            name=feature_name+'__'+str(sample)
            model=IsolationForest(n_estimators=100,max_samples=sample,contamination='auto',random_state=SEED,n_jobs=1).fit(train[features])
            anomaly=-model.score_samples(tune[features]);cutoff=float(np.quantile(anomaly,.9,method='higher'))
            if_models[(district,name)]={'model':model,'features':features,'cutoff':cutoff,'training_rows':len(train),'train_end':train.week_start.max(),'calibration_end':tune.week_start.max()}
            rate=float(np.mean(anomaly>cutoff))
            if_candidates.append({'candidate':name,'admin2':district,'feature_count':len(features),'max_samples':str(sample),'training_rows':len(train),'tuning_rows':len(tune),'cutoff':cutoff,'tuning_alerts':int((anomaly>cutoff).sum()),'tuning_rate':rate})
            if_tuning.extend([{'admin2':district,'candidate':name,'week_start':d,'anomaly_score':s,'cutoff':cutoff,'alert':s>cutoff} for d,s in zip(tune.week_start,anomaly)])
table(pd.DataFrame(if_coverage),'Table 21: Forest history feasibility')
if_candidates=pd.DataFrame(if_candidates)
assert not if_candidates.empty,'No defensible comparison: record deferral instead'
table(if_candidates.round(4),'Table 22: Forest tuning candidates')
choice=if_candidates.groupby('candidate').agg(feature_count=('feature_count','first'),districts=('admin2','nunique'),mean_tuning_rate=('tuning_rate','mean')).reset_index()
choice['budget_distance']=(choice.mean_tuning_rate-.1).abs();choice['sample_tie']=choice.candidate.str.endswith('__32').map({True:0,False:1})
choice=choice.sort_values(['feature_count','budget_distance','sample_tie','candidate'])
SELECTED_IF=choice.iloc[0].candidate
(OUT/'forest_frozen_choice.json').write_text(json.dumps({'candidate':SELECTED_IF,'calibration_end':str(TUNE_END.date()),'assessment_start':str(ASSESS_START.date()),'criterion':'smallest feature set; tuning burden nearest 10%; tie max_samples 32','cutoffs':{d:v['cutoff'] for (d,n),v in if_models.items() if n==SELECTED_IF}},indent=2))
pd.DataFrame(if_tuning).to_csv(OUT/'forest_tuning_scores.csv',index=False)
report(f'**Frozen decision before assessment:** {SELECTED_IF}. Table 21 records actual feasible training and tuning sizes, including missing-lag/history exclusions. The calibration burden is a budget check, not model accuracy. Assessment will now be scored without changing these fits or cutoffs.')
'''),
code('''if_rows=[]
for (district,name),spec in if_models.items():
    g=dw.loc[dw.admin2.eq(district)&dw.block.eq('assessment')].copy()
    finite=np.isfinite(g[spec['features']]).all(axis=1)
    eligible=g.history_eligible & finite
    anomaly=pd.Series(np.nan,index=g.index)
    anomaly.loc[eligible]=-spec['model'].score_samples(g.loc[eligible,spec['features']])
    assert spec['train_end']<spec['calibration_end']<g.week_start.min()
    for i,row in g.iterrows():
        if_rows.append({'admin2':district,'candidate':name,'week_start':row.week_start,'focal_events':row.focal_events,'political_events':row.political_events,'focal_share':row.focal_share,'previous_week_focal':row.previous_week_focal,'previous_four_weeks_focal':row.previous_four_weeks_focal,'eligible':bool(eligible.loc[i]),'reason':'scored' if eligible.loc[i] else ('partial current week' if not row.complete_week else 'ineligible current or lag history'),'anomaly_score':anomaly.loc[i],'cutoff':spec['cutoff'],'if_alert':bool(anomaly.loc[i]>spec['cutoff']) if eligible.loc[i] else False,'training_rows':spec['training_rows'],'train_end':spec['train_end'],'calibration_end':spec['calibration_end']})
if_scores=pd.DataFrame(if_rows)
if_scores.to_csv(OUT/'forest_assessment_scores.csv',index=False)
comparisons=[]; paired_all=[]
base=refcount.loc[refcount.block.eq('assessment'),['admin2','week_start','eligible','score','alert','direction','baseline','reason']].rename(columns={'eligible':'mad_eligible','score':'mad_score','alert':'mad_alert','reason':'mad_reason'})
for name,g in if_scores.groupby('candidate'):
    paired=g.merge(base,on=['admin2','week_start'],validate='one_to_one')
    paired['common']=paired.eligible & paired.mad_eligible
    paired_all.append(paired)
    for district,q in paired.groupby('admin2'):
        c=q.loc[q.common];union=(c.if_alert|c.mad_alert).sum()
        comparisons.append({'candidate':name,'admin2':district,'assessment_calendar_rows':len(q),'forest_scored':int(q.eligible.sum()),'mad_scored':int(q.mad_eligible.sum()),'common_scored':len(c),'forest_alerts':int(c.if_alert.sum()),'mad_alerts':int(c.mad_alert.sum()),'both':int((c.if_alert&c.mad_alert).sum()),'forest_only':int((c.if_alert&~c.mad_alert).sum()),'mad_only':int((c.mad_alert&~c.if_alert).sum()),'neither':int((~c.if_alert&~c.mad_alert).sum()),'alert_jaccard':(c.if_alert&c.mad_alert).sum()/union if union else np.nan})
if_comparison=pd.DataFrame(comparisons)
table(if_comparison.round(3),'Table 23: Forest versus MAD on common assessment weeks')
paired_all=pd.concat(paired_all,ignore_index=True)
paired=paired_all.loc[paired_all.candidate.eq(SELECTED_IF)&paired_all.common].copy()
assert paired.week_start.ge(ASSESS_START).all() and paired.week_start.le(weeks[-1]).all()
selected_comparison=if_comparison.loc[if_comparison.candidate.eq(SELECTED_IF)].copy()
totals=selected_comparison[['common_scored','forest_alerts','mad_alerts','both','forest_only','mad_only','neither']].sum()
print('Selected candidate assessment totals:',totals.to_dict())
if_examples=pd.concat([paired.loc[paired.if_alert & ~paired.mad_alert].nlargest(3,'anomaly_score').assign(category='Forest only'),paired.loc[paired.mad_alert].nlargest(2,'mad_score').assign(category='MAD flagged'),paired.loc[~paired.if_alert & ~paired.mad_alert].nlargest(2,'focal_events').assign(category='Neither; high raw count')],ignore_index=True)
table(if_examples[['category','admin2','week_start','focal_events','political_events','focal_share','previous_week_focal','anomaly_score','cutoff','mad_score','direction','baseline']].round(3),'Table 24: Forest comparison examples')
forest_traces=master.loc[master.focal_event].merge(if_examples[['admin2','week_start','category']].drop_duplicates(),on=['admin2','week_start'],validate='many_to_many')[['category','admin2','week_start','event_id_cnty','event_date','location','source','notes']]
forest_traces.to_csv(OUT/'forest_example_records.csv',index=False)
first=forest_traces.groupby(['category','admin2','week_start'],sort=False).head(1).copy();first['notes_excerpt']=first.notes.str.slice(0,150)
table(first.drop(columns='notes'),'Table 25: Forest documentary entry records')
fig,axes=plt.subplots(1,2,figsize=(11,4))
x=np.arange(len(selected_comparison));n=selected_comparison.common_scored.to_numpy()
axes[0].barh(x-.17,100*selected_comparison.mad_alerts/n,height=.32,color='#245c85',label='12-week MAD')
axes[0].barh(x+.17,100*selected_comparison.forest_alerts/n,height=.32,color='#b54c45',label='Forest')
axes[0].set(yticks=x,yticklabels=selected_comparison.admin2,xlabel='Alerts / common scored weeks (%)',title='Review burden on identical weeks');axes[0].legend(fontsize=8)
parts=[('both','Both','#825b9e'),('forest_only','Forest only','#b54c45'),('mad_only','MAD only','#245c85'),('neither','Neither','#c3cbd2')]
left=np.zeros(len(selected_comparison))
for col,label,color in parts:
    values=selected_comparison[col].to_numpy();axes[1].barh(x,values,left=left,color=color,label=label);left+=values
axes[1].set(yticks=x,yticklabels=selected_comparison.admin2,xlabel='Common scored district-weeks (records)',title='Which leads overlap?');axes[1].legend(fontsize=8,ncol=2)
fig.suptitle('Figure 4. Does the forest change the assessment review list?',y=1.04)
figure(fig,'Figure_4_forest_comparison')
report(f'**Figure 4 and Tables 23-25 interpretation.** On {int(totals.common_scored)} common district-weeks, the selected forest flags {int(totals.forest_alerts)}, the 12-week rule flags {int(totals.mad_alerts)}, and {int(totals.both)} overlap. There are {int(totals.forest_only)} forest-only leads. Different burden or disagreement is not better detection: no independent labels tell us which leads merit review. Table 24 shows the actual feature values and baseline comparison; Table 25 and forest_example_records.csv retain documentary entries. The model learned from a short early block and its score distribution can drift; a tuning budget need not hold later.')
'''),
md('''**Decision: retain the median/MAD screen as the primary method; retain the forest comparison as experimental evidence only.** The forest supplies different candidates but does not establish added documentary value or superiority. Its small per-district training sets, changing activity levels and lack of independent review labels do not justify operational replacement. The transparent rule exposes the local baseline and direction directly. An independent reviewer can assess both lists before deciding whether the extra method is useful; precision/recall are deferred until suitable labels exist.''')
],6)
complete(6,'S6 executed: district-specific earlier-only Isolation Forest, 4 candidates (2 small feature subsets x 32/auto samples), 100 trees and seed 42. Tables 21-22 document feasibility and tuning-only cutoff/choice; forest_frozen_choice.json records frozen settings. Assessment fits/cutoffs unchanged; Table 23 and Figure 4 compare common eligible weeks with 12-week MAD, Tables 24-25 trace examples. Retain MAD primary; forest experimental only, no claimed superiority or label-based metrics.')
