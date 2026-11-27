from workflow import *
run([
md('''## S5. Which weeks differ from earlier local activity?
The simple baseline compares each completed district-week with its own preceding **8, 12 or 16 calendar weeks**, following Phase 3's local rule. The modified z-score is `0.6745 × (current − history median) / max(history MAD, 1)` for counts. MAD is the median absolute deviation from the history median; the one-event floor lets zero/flat count histories be scored without division by zero. A flag requires absolute score **greater than 3.5**. Positive means unusually high relative to recent local records; negative means unusually low.

For shares, use the same formula with the share MAD and **no one-event floor**; a zero MAD leaves the share unscored. Current and every preceding calendar week must be complete and have a positive political denominator. This preserves Phase 2's history rule, even when focal count is zero. Missing weeks are not skipped. Counts, denominators and shares stay beside every result. Counts and shares are different review signals, not independent corroborating labels.

The prespecified 12-week reference balances the shorter and longer windows; all three remain visible. Comparisons report both each setting's coverage and the common scored weeks, so extra alerts caused merely by extra coverage are distinguishable. Each baseline is available only after its current week closes. No future observation enters its median or MAD.'''),
code('''WINDOWS=[8,12,16]; Z_CUT=3.5
METRICS=['focal_events','political_events','focal_share']
def score_local(data,windows=WINDOWS):
    rows=[]
    for district,g in data.groupby('admin2',sort=True):
        g=g.sort_values('week_start').reset_index(drop=True)
        for w in windows:
            for i,row in g.iterrows():
                hist=g.iloc[max(0,i-w):i]
                for metric in METRICS:
                    median=mad=denom=z=np.nan
                    reason='scored'
                    if not row.complete_week:reason='partial current week'
                    elif row.political_events<=0:reason='undefined current denominator'
                    elif i<w:reason='insufficient earlier calendar weeks'
                    elif not hist.history_eligible.all():reason='ineligible earlier calendar week'
                    elif not np.isfinite(hist[metric]).all():reason='undefined history value'
                    if reason=='scored':
                        median=float(hist[metric].median());mad=float((hist[metric]-median).abs().median())
                        denom=max(mad,1.) if metric!='focal_share' else mad
                        if denom<=0:reason='flat share history'
                        else:z=.6745*(row[metric]-median)/denom
                    assert hist.empty or hist.week_start.max()<row.week_start
                    rows.append({'admin2':district,'week_start':row.week_start,'week_end':row.week_end,'block':row.block,'window':w,'metric':metric,'focal_events':row.focal_events,'political_events':row.political_events,'focal_share':row.focal_share,'previous_week_focal':row.previous_week_focal,'previous_four_weeks_focal':row.previous_four_weeks_focal,'baseline':median,'history_MAD':mad,'scale_used':denom,'score':z,'eligible':np.isfinite(z),'reason':reason,'alert':bool(abs(z)>Z_CUT) if np.isfinite(z) else False,'direction':'high' if z>Z_CUT else ('low' if z<-Z_CUT else 'none'),'history_start':hist.week_start.min() if len(hist) else pd.NaT,'history_end':hist.week_start.max() if len(hist) else pd.NaT})
    return pd.DataFrame(rows)
scores=score_local(dw)
assert scores.loc[scores.eligible,'history_end'].lt(scores.loc[scores.eligible,'week_start']).all()
# A future-data perturbation must not alter any earlier result.
changed=dw.copy();changed.loc[changed.week_start.ge(ASSESS_START),'focal_events']+=10000
check=score_local(changed)
assert np.allclose(scores.loc[scores.week_start.lt(ASSESS_START),'score'],check.loc[check.week_start.lt(ASSESS_START),'score'],equal_nan=True)
scores.to_csv(OUT/'temporal_scores.csv',index=False)
exclusions=scores.groupby(['window','metric','reason']).size().rename('rows').reset_index()
table(exclusions,'Table 12: Temporal coverage and exclusion reasons')
counts=scores.loc[scores.metric.eq('focal_events')].copy()
wide=counts.pivot(index=['admin2','week_start'],columns='window',values='score')
common=wide.dropna().index
counts['common_scored']=pd.MultiIndex.from_frame(counts[['admin2','week_start']]).isin(common)
burden=[]
for scope,mask in [('all',counts.week_start.notna()),('tuning',counts.block.eq('tuning')),('assessment',counts.block.eq('assessment'))]:
    for (w,d),g in counts.loc[mask].groupby(['window','admin2']):
        shared=g.loc[g.common_scored]
        burden.append({'block':scope,'window':w,'admin2':d,'scored':int(g.eligible.sum()),'high':int(g.direction.eq('high').sum()),'low':int(g.direction.eq('low').sum()),'alerts':int(g.alert.sum()),'alert_pct':100*g.alert.sum()/g.eligible.sum() if g.eligible.sum() else np.nan,'common_scored':len(shared),'common_alerts':int(shared.alert.sum())})
burden=pd.DataFrame(burden)
table(burden,'Table 13: Focal count alert burden')
overlap=[]
for a,b in [(8,12),(12,16),(8,16)]:
    paired=wide[[a,b]].dropna();fa=paired[a].abs().gt(Z_CUT);fb=paired[b].abs().gt(Z_CUT)
    overlap.append({'windows':f'{a} vs {b}','common_scored':len(paired),'alerts_a':int(fa.sum()),'alerts_b':int(fb.sum()),'both':int((fa&fb).sum()),'either':int((fa|fb).sum()),'alert_jaccard':(fa&fb).sum()/(fa|fb).sum() if (fa|fb).any() else np.nan})
table(pd.DataFrame(overlap).round(3),'Table 14: Window alert overlap')
# Transparent trough/rebound tag for interpretation; not an anomaly label.
recovery=[]
for district,g in dw.groupby('admin2'):
    g=g.sort_values('week_start');h=g.focal_events.where(g.history_eligible)
    recent=h.shift(1).rolling(4).median();older=h.shift(5).rolling(4).median()
    tag=recent.le(np.maximum(1,older*.25)) & g.focal_events.gt(np.maximum(5,recent*2)) & g.history_eligible
    recovery.extend([{'admin2':district,'week_start':d,'recent4_median':r,'preceding4_median':o,'trough_rebound_candidate':bool(t)} for d,r,o,t in zip(g.week_start,recent,older,tag)])
counts=counts.merge(pd.DataFrame(recovery),on=['admin2','week_start'],validate='many_to_one')
rec=counts.loc[counts.direction.eq('high')].groupby('window').agg(high_alerts=('alert','size'),trough_rebound_candidates=('trough_rebound_candidate','sum')).reset_index()
table(rec,'Table 15: High alerts after low recent history')
refcount=counts.loc[counts.window.eq(12)].copy()
examples=pd.concat([
    refcount.loc[refcount.direction.eq('high')].nlargest(3,'score').assign(example='highest upward scores'),
    refcount.loc[refcount.direction.eq('low')].nsmallest(2,'score').assign(example='lowest downward scores'),
    refcount.loc[refcount.eligible & ~refcount.alert].nlargest(3,'focal_events').assign(example='high-count non-alerts'),
    refcount.loc[refcount.week_end.le('2025-09-30')].nlargest(2,'focal_events').assign(example='absolute peaks')
],ignore_index=True)
examples=examples.drop_duplicates(['admin2','week_start','example'])
table(examples[['example','admin2','week_start','focal_events','political_events','focal_share','baseline','score','reason','direction','recent4_median','preceding4_median','trough_rebound_candidate']].round(3),'Table 16: Relative and absolute week examples')
traces=[]
for row in examples.itertuples():
    g=master.loc[master.admin2.eq(row.admin2)&master.week_start.eq(row.week_start)&master.focal_event].sort_values(['event_date','event_id_cnty'])
    assert len(g)==row.focal_events
    for e in g.head(2).itertuples():
        traces.append({'example':row.example,'admin2':row.admin2,'week_start':row.week_start,'event_id_cnty':e.event_id_cnty,'event_date':e.event_date,'location':e.location,'source':e.source,'notes':e.notes})
traces=pd.DataFrame(traces);traces.to_csv(OUT/'temporal_source_examples.csv',index=False)
# Full incident membership gives every selected week an auditable record set.
keys=examples[['admin2','week_start']].drop_duplicates()
master.loc[master.focal_event].merge(keys,on=['admin2','week_start'],validate='many_to_one')[['admin2','week_start','event_id_cnty','event_date','location','source','notes']].to_csv(OUT/'selected_week_focal_records.csv',index=False)
table(traces.drop(columns='notes').head(8),'Table 17: Week documentary entry records')
fig,axes=plt.subplots(5,1,figsize=(11,11),sharex=True)
for ax,(district,g) in zip(axes,refcount.groupby('admin2',sort=True)):
    g=g.sort_values('week_start')
    ax.plot(g.week_start,g.focal_events,color='#9aa5b1',lw=1,label='Current count')
    ax.plot(g.week_start,g.baseline,color='#245c85',lw=1.5,label='Previous 12-week median')
    for direction,color,marker in [('high','#b54c45','^'),('low','#b17b26','v')]:
        part=g.loc[g.direction.eq(direction)];ax.scatter(part.week_start,part.focal_events,c=color,marker=marker,s=30,label=f'{direction} screen')
    partial=g.loc[g.reason.eq('partial current week')];ax.scatter(partial.week_start,partial.focal_events,c='#333333',marker='x',label='Partial: excluded')
    ax.axvline(ASSESS_START,color='#666666',ls=':',lw=1);ax.set(title=district,ylabel='Focal records/week');ax.grid(axis='y',alpha=.2)
axes[0].legend(ncol=5,fontsize=8,loc='upper center',bbox_to_anchor=(.5,1.55))
axes[-1].set_xlabel('Completed week start (date); dotted line starts retrospective assessment')
axes[-1].xaxis.set_major_locator(mdates.MonthLocator(interval=3));axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
fig.suptitle('Figure 3. Which counts differ from the preceding local baseline?',y=1.02)
figure(fig,'Figure_3_temporal_baselines')
summary=counts.groupby('window').agg(scored=('eligible','sum'),alerts=('alert','sum'),common_scored=('common_scored','sum')).reset_index()
summary['alert_pct']=100*summary.alerts/summary.scored
summary['common_alerts']=[int(counts.loc[counts.window.eq(w)&counts.common_scored,'alert'].sum()) for w in summary.window]
table(summary.round(2),'Table 18: Window summary')
share_summary=scores.loc[scores.metric.eq('focal_share')].groupby('window').agg(scored=('eligible','sum'),alerts=('alert','sum')).reset_index()
table(share_summary,'Table 19: Share screening coverage')
report('**Figure 3 and Tables 12-19 interpretation.** The same absolute count can be ordinary during a sustained high period and unusual after a trough. Red/amber markers flag departures in either direction; they are review leads, not verified anomalies. Table 16 separates the largest raw counts from relative-history alerts and provides high-count non-alert comparisons. Table 15 uses a declared descriptive tag: preceding four-week median at most max(1, one-quarter of the prior four-week median), followed by a current count above max(5, twice the recent median). It identifies possible rebounds for review, not verified recovery. Baseline gaps retain ineligible calendar history; the final partial week is displayed but unscored. Shares may remain unscored for flat histories even where counts can be screened. Table 17 and the accompanying CSVs link examples to original event sources; no source adjudication has been performed.')
''')
],5)
complete(5,'S5 executed: 8/12/16-week district-specific earlier-only median/MAD for focal counts, political counts and shares; all rows retain raw counts, denominator, baseline, eligibility/reason, score and direction in temporal_scores.csv. Future-data perturbation and strict earlier-history assertions passed. Tables 12-19 cover burden by block/district, common coverage, overlap, rebounds, peaks/non-alert examples and traceable records; Figure 3 preserves gaps/partial exclusion.')
