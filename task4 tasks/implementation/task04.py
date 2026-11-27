from workflow import *
run([
md('''## S4. Does clustering add detail beyond district totals?
We compare neighboring settings by **co-membership Jaccard**: among event pairs grouped together by either setting, what fraction are grouped together by both? It ignores label numbers and does not count pairs of noise records as a group. Noise-status agreement is shown separately. This measures sensitivity, not accuracy against true labels.

Silhouette compares within-group and between-group distances; it is calculated only on non-noise records with at least two groups. To limit cost, use a uniform sample of up to 1,500 event records without replacement (seed 42), reporting represented groups. A group lost in sampling is not silently presented as fully evaluated. Dense repeated coordinates can produce high silhouettes even when radius sensitivity is substantial (Menorias Sections 7.5-7.6).'''),
code('''def pair_jaccard(a,b):
    a=np.asarray(a);b=np.asarray(b)
    choose=lambda x:np.sum(np.asarray(x,dtype=float)*(np.asarray(x,dtype=float)-1)/2)
    pa=choose(pd.Series(a[a>=0]).value_counts());pb=choose(pd.Series(b[b>=0]).value_counts())
    mask=(a>=0)&(b>=0)
    inter=choose(pd.DataFrame({'a':a[mask],'b':b[mask]}).value_counts())
    return inter/(pa+pb-inter) if pa+pb-inter else np.nan
silrows=[]
for row in spatial.to_dict('records'):
    key=(row['population'],row['radius_km'],row['min_samples']);d=populations[key[0]]
    labels=assignments[key].to_numpy();idx=np.flatnonzero(labels>=0)
    chosen=np.random.default_rng(SEED).choice(idx,size=min(1500,len(idx)),replace=False)
    represented=len(np.unique(labels[chosen]));score=np.nan
    reason='one non-noise group' if row['clusters']<2 else 'sampled' if len(chosen)<len(idx) else 'all non-noise'
    if 2<=represented<len(chosen): score=silhouette_score(d[['latitude_rad','longitude_rad']].to_numpy()[chosen],labels[chosen],metric='haversine')
    else: reason='unavailable: fewer than two represented groups'
    silrows.append({**row,'silhouette':score,'silhouette_n':len(chosen),'groups_represented':represented,'silhouette_scope':reason})
spatial_eval=pd.DataFrame(silrows)
table(spatial_eval.round(4),'Table 6: Spatial evaluation with noise')
stability=[]
def compare(k1,k2,kind):
    a=assignments[k1];b=assignments[k2];ids=a.index.intersection(b.index);a=a.loc[ids].to_numpy();b=b.loc[ids].to_numpy()
    stability.append({'comparison':kind,'setting_a':str(k1),'setting_b':str(k2),'common_events':len(ids),'pair_jaccard':pair_jaccard(a,b),'noise_status_agreement':np.mean((a<0)==(b<0))})
for pop in populations:
    for m in MIN_SAMPLES:
        for a,b in zip(RADII[:-1],RADII[1:]):compare((pop,a,m),(pop,b,m),'neighbor radii')
    for r in RADII:compare((pop,r,10),(pop,r,50),'density')
for r in RADII:
    for m in MIN_SAMPLES:compare(('full',r,m),('precision1',r,m),'precision restriction')
stability=pd.DataFrame(stability)
table(stability.round(4),'Table 7: Membership sensitivity')
district_baseline=inc.groupby('admin2').agg(records=('event_id_cnty','size'),places=('location','nunique')).reset_index().sort_values('records',ascending=False)
district_baseline['share_pct']=100*district_baseline.records/len(inc)
table(district_baseline.round(2),'Table 8: District count baseline')
profiles=[]; examples=[]
for pop,d in populations.items():
    d=d.copy();d['cluster']=assignments[(pop,1.,50)].to_numpy()
    for label,g in d.loc[d.cluster>=0].groupby('cluster'):
        profiles.append({'population':pop,'cluster':label,'records':len(g),'districts':'; '.join(g.admin2.unique()),'main_place':g.location.mode().iloc[0],'start':g.event_date.min(),'end':g.event_date.max(),'coordinate_pairs':len(g[['latitude','longitude']].drop_duplicates()),'repeated_coordinate_pct':100*g.duplicated(['latitude','longitude']).mean(),'precision1_pct':100*g.geo_precision_1.mean()})
        # Earliest event provides a reproducible documentary entry, not an outcome judgment.
        e=g.sort_values(['event_date','event_id_cnty']).iloc[0]
        examples.append({'population':pop,'cluster':label,**e[['event_id_cnty','event_date','admin2','location','event_type','source','notes']].to_dict()})
profiles=pd.DataFrame(profiles).sort_values(['population','records'],ascending=[True,False]);examples=pd.DataFrame(examples)
profiles.to_csv(OUT/'all_cluster_profiles.csv',index=False);examples.to_csv(OUT/'cluster_source_examples.csv',index=False)
table(profiles.groupby('population',sort=False).head(6).round(2),'Table 9: Largest reference group profiles')
show_examples=examples.merge(profiles[['population','cluster','records']],on=['population','cluster']).sort_values('records',ascending=False).head(4).copy()
show_examples['notes_excerpt']=show_examples.notes.str.slice(0,180)
table(show_examples.drop(columns='notes'),'Table 10: Documentary entry records')
fig,axes=plt.subplots(1,2,figsize=(12,5))
for ax,(pop,d) in zip(axes,populations.items()):
    d=d.copy();d['cluster']=assignments[(pop,1.,50)].to_numpy()
    top=profiles.loc[profiles.population.eq(pop)].head(5).cluster.tolist()
    other=d.loc[~d.cluster.isin(top)&d.cluster.ge(0)];ax.scatter(other.longitude,other.latitude,c='#b4bdc5',s=10,alpha=.5,label='Other groups')
    for color,label in zip(['#245c85','#b54c45','#2a8973','#b17b26','#825b9e'],top):
        g=d.loc[d.cluster.eq(label)];ax.scatter(g.longitude,g.latitude,s=15,color=color,label=f'Group {label} ({len(g)} records)')
    noise=d.loc[d.cluster.lt(0)];ax.scatter(noise.longitude,noise.latitude,s=20,marker='x',c='#333333',label='Noise')
    ax.set(title=f'{pop}: 1 km / 50 records',xlabel='Longitude (degrees east)',ylabel='Latitude (degrees north)');ax.set_aspect(1/np.cos(np.radians(31.4)));ax.legend(fontsize=7,loc='best')
fig.suptitle('Figure 2. Where do the largest reference groups lie?',y=1.02)
figure(fig,'Figure_2_reference_map')
# Different time periods have different event IDs: compare shared coordinate places instead.
MID=pd.Timestamp('2024-10-04')
time_labels=[];time_rows=[]
for name,mask in [('earlier',inc.event_date.le(MID)),('later',inc.event_date.gt(MID))]:
    d=inc.loc[mask].copy();d['cluster']=geo_fit(d,1.,50)
    coords=d[['latitude','longitude','cluster']].drop_duplicates().set_index(['latitude','longitude']).cluster
    time_labels.append(coords)
    time_rows.append({'period':name,'start':d.event_date.min(),'end':d.event_date.max(),'records':len(d),'clusters':d.loc[d.cluster.ge(0),'cluster'].nunique(),'noise_pct':100*d.cluster.lt(0).mean()})
shared=time_labels[0].index.intersection(time_labels[1].index)
time_j=pair_jaccard(time_labels[0].loc[shared],time_labels[1].loc[shared])
table(pd.DataFrame(time_rows),'Table 11: Spatial time restriction')
print('Shared coordinate places:',len(shared),'| place-pair Jaccard:',round(time_j,3))
ref=spatial_eval.query("population=='full' and radius_km==1 and min_samples==50").iloc[0]
wide=spatial_eval.query("population=='full' and radius_km==3 and min_samples==50").iloc[0]
near=stability.loc[stability.comparison.eq('neighbor radii') & stability.setting_a.isin([str(('full',.75,50)),str(('full',1.,50))])]
report(f'**Figure 2 and Tables 6-11 interpretation.** At the prespecified 1 km/50 reference, {int(ref.clusters)} groups contain recorded land places; {ref.noise_pct:.1f}% of records are noise. At 3 km/50, {int(wide.clusters)} group remains, so radius materially changes the picture. The largest district is {district_baseline.iloc[0].admin2} ({district_baseline.iloc[0].share_pct:.1f}% of land focal records); profiles split district totals into named-place groups, but repeated coordinates drive much of that detail. The two equal-duration spatial blocks share {len(shared)} coordinate places, with place-pair Jaccard {time_j:.2f}; this is not event-level validation. No single robust or optimal partition is established. Use the reference groups only as traceable review bins, alongside district totals and the precision comparison. Full source excerpts are in cluster_source_examples.csv; no documentary outcomes have been verified.')
'''),
md('''**Spatial limitations.** One radius struggles with varying density, and dense recorded centroids can connect places into long chains: eps does not bound the whole group's diameter. Precision 1 is a selected subset, not exact impact coordinates or a random sample. High silhouette on repeated places does not demonstrate operational value. Table 7 shows neighborhood/density/precision sensitivity; Table 11 adds a descriptive time restriction. This comparison supports place-based review, not automatic hotspot intervention.''')
],4)
complete(4,'S4 executed: Table 6 records sampled non-noise haversine silhouettes with coverage/noise and invalid one-group cases; Table 7 compares nearby radii/density and common event IDs across precision populations. District baseline, original-unit profiles, source examples, two-panel map and equal-duration time restriction saved (Tables 8-11, Figure 2). Reference 1 km/50 remains descriptive; no optimal/stable partition claim. Full profiles and source excerpts retained.')
