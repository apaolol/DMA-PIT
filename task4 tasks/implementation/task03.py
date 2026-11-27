from workflow import *
run([
md('''## S3. Which nearby recorded places form groups?
Following Menorias Module 7 Sections 7.4-7.4.4, DBSCAN connects dense neighborhoods without choosing a fixed group count. **eps** is the neighborhood radius; **min_samples** counts records including the point itself. A border record touches a dense group; **noise** means unassigned by this setting, not verified error or harm.

We use haversine distance on radians and set `eps = radius_km / 6371.0088`. Geographic axes are not standardized. Because many records share coordinates, fitting unique coordinate pairs with their record counts as weights preserves event density and avoids a large duplicate distance graph. Unique pairs retain first-occurrence order; the fit and event assignments are deterministic. IDs and notes do not enter distance calculations.

Figure 1 measures distance to neighbor 10/50 **including self**, consistent with DBSCAN. Repetition can make these distances zero. A curve without a clear knee does not establish an optimum; the frozen grid checks nearby radii and wider merging behavior.'''),
code('''RADII=[0.5,0.75,1.,1.25,1.5,2.,3.]; MIN_SAMPLES=[10,50]
populations={'full':inc.copy(),'precision1':inc.loc[inc.geo_precision_1].copy()}
assignments={}; spatial_rows=[]; kd_rows=[]
fig,axes=plt.subplots(1,2,figsize=(11,3.7),sharey=True)
for ax,(pop,d) in zip(axes,populations.items()):
    X=d[['latitude_rad','longitude_rad']].to_numpy()
    nn=NearestNeighbors(n_neighbors=50,metric='haversine',algorithm='ball_tree').fit(X)
    dist,_=nn.kneighbors(X)
    for m in MIN_SAMPLES:
        kdist=np.sort(dist[:,m-1]*EARTH_KM)
        ax.plot(np.linspace(0,100,len(kdist)),kdist,label=f'min_samples {m}')
        kd_rows.append({'population':pop,'min_samples':m,'zero_distance_pct':100*np.isclose(kdist,0,atol=1e-10).mean(),'p95_km':np.quantile(kdist,.95),'max_km':kdist.max()})
    ax.set(title=f'{pop}: sorted neighbor distances',xlabel='Records sorted by distance (%)',ylabel='Distance (km)');ax.legend()
fig.suptitle('Figure 1. Does the distance curve suggest a clear radius?',y=1.03)
figure(fig,'Figure_1_kdistance')
table(pd.DataFrame(kd_rows),'Table 4: Neighbor distance diagnostics')
def geo_fit(d,r,m):
    pairs=pd.MultiIndex.from_frame(d[['latitude_rad','longitude_rad']])
    inverse,unique=pd.factorize(pairs,sort=False)
    X=np.array(unique.tolist(),dtype=float); weights=np.bincount(inverse)
    lab=DBSCAN(eps=r/EARTH_KM,min_samples=m,metric='haversine',algorithm='ball_tree',n_jobs=1).fit_predict(X,sample_weight=weights)
    return lab[inverse]
for pop,d in populations.items():
    for m in MIN_SAMPLES:
        for r in RADII:
            labels=geo_fit(d,r,m)
            assignments[(pop,r,m)]=pd.Series(labels,index=d.event_id_cnty,name='cluster')
            sizes=pd.Series(labels[labels>=0]).value_counts()
            spatial_rows.append({'population':pop,'radius_km':r,'min_samples':m,'records':len(d),'coordinate_pairs':len(d[['latitude','longitude']].drop_duplicates()),'clusters':len(sizes),'noise_records':int((labels<0).sum()),'noise_pct':100*(labels<0).mean(),'smallest_cluster':int(sizes.min()) if len(sizes) else 0,'median_cluster':float(sizes.median()) if len(sizes) else 0,'largest_cluster':int(sizes.max()) if len(sizes) else 0})
            assert sizes.sum()+(labels<0).sum()==len(d)
spatial=pd.DataFrame(spatial_rows)
table(spatial,'Table 5: Spatial candidate accounting')
long_assign=pd.concat([s.rename('cluster').reset_index().assign(population=k[0],radius_km=k[1],min_samples=k[2]) for k,s in assignments.items()],ignore_index=True)
long_assign.to_csv(OUT/'spatial_assignments.csv',index=False)
assert len(long_assign)==sum(len(d)*len(RADII)*len(MIN_SAMPLES) for d in populations.values())
# Check weighted compression against the literal event fit at the reference setting.
from sklearn.metrics.cluster import contingency_matrix
for pop,d in populations.items():
    literal=DBSCAN(eps=1/EARTH_KM,min_samples=50,metric='haversine',algorithm='ball_tree',n_jobs=1).fit_predict(d[['latitude_rad','longitude_rad']])
    compressed=assignments[(pop,1.,50)].to_numpy()
    assert np.array_equal(literal<0,compressed<0)
    assert adjusted_rand_score(literal,compressed)==1.
print('28 candidate fits; weighted/event-level reference partitions agree exactly in both populations.')
report('**Figure 1 interpretation.** Zero-distance neighbors dominate where many events share a recorded place (Table 4); these are repeated records at coordinates, not duplicate event IDs. Table 5 shows how the group count and noise change across the frozen radii. Neither a high-density coordinate nor a curve bend validates an exact incident site.')
''')
],3)
complete(3,'S3 executed: 28 weighted geographic fits (7 radii x 2 densities x 2 populations); literal event-level checks at 1 km/50 give identical noise and partitions in both populations. Table 4 and Figure 1 document neighbor distances; Table 5 and spatial_assignments.csv preserve all candidate accounting and event IDs. No source changes.')
