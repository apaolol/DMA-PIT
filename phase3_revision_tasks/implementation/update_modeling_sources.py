import json,shutil,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2]; out=Path(__file__).parent
p=root/'DMA_Phase3_Final_Complete.ipynb'
shutil.copy2(p,out/'before_modeling_source_update.ipynb')
n=json.loads(p.read_text(encoding='utf8')); before=json.loads(json.dumps(n))
i=next(i for i,c in enumerate(n['cells']) if ''.join(c['source']).startswith('# Task 7'))
s=''.join(n['cells'][i]['source'])
s=s.replace('The work below is a plan, not completed predictive validation.','The work below is a plan, not completed predictive validation. The DBSCAN workflow follows Nicole S. Menorias’ *Module 7: Cluster Analysis*, Sections 7.4–7.6 (listed in References), adapted from its customer example to geographic event records.')
s=s.replace('| DBSCAN | Post-cutoff land focal coordinates in radians; identify geographic concentrations for documentary review | District-count summaries; radii around 1-2 km plus the wider explored range, min_samples 10/50, full versus precision 1 | Cluster/noise proportions, sensitivity of membership and concentration, source review of selected places; useful only if it adds stable detail beyond district totals |','| DBSCAN | Post-cutoff land focal coordinates from `acled_focal_incidents.csv`, in radians with haversine distance; group nearby recorded places without fixing the number of groups | District totals; geographic k-distance candidates and a radius sweep including the explored 1–2 km settings, `min_samples` 10/50, full versus precision 1 | Number and sizes of clusters, noise share, stable membership across settings, non-noise silhouette where valid, and event/source review; assess whether it adds useful detail beyond district totals |')
mark='**Timing and leakage.**'
addition="""### DBSCAN workflow adapted from Module 7

DBSCAN joins nearby points when enough records occur within a chosen neighborhood. It suits this geographic question because concentrations may have irregular shapes and some records may remain outside every group. Its **noise** label (`-1`) means a record does not belong to a dense cluster at that setting; it does not mean an erroneous record or verified harmful anomaly.

1. **Keep the geographic distance meaningful.** Use Phase 2's `latitude_rad` and `longitude_rad` from `acled_focal_incidents.csv`, containing eligible post-cutoff land focal records. Use haversine distance, which measures separation on a sphere, and convert a candidate radius in kilometers to `eps` in radians by dividing by the same Earth-radius constant used in the spatial analysis. Module 7 scales mixed-unit customer features; for this geographic model, retain radians rather than standardizing latitude and longitude separately. Counts and fatalities are not additional spatial-distance features.
2. **Explain and select the density settings.** `eps` is the neighborhood radius; `min_samples` is the required number of records in that neighborhood, including the record itself. A core record meets this threshold, a border record lies near a core without meeting it itself, and noise lies outside the resulting groups (Module 7, Section 7.4.1). Following Section 7.4.3, propose sorted k-distance curves using haversine distance for each candidate `min_samples`, including the point itself as in the lesson code. Convert distances to kilometers for reading the curve. A bend suggests radii to investigate; it does not establish one correct radius. Repeated coordinates can create many zero distances and an unclear bend.
3. **Check stability instead of selecting one attractive map.** Following Section 7.4.4, sweep neighboring radii and compare `min_samples` 10 and 50. Retain cluster count, cluster sizes, noise percentage and membership changes; look for a range with similar results. Repeat for the precision-1 subset and compare with the existing district totals, M13 and M14. These radius and density settings are project choices, not values prescribed by the module. Different local densities may prevent one setting from working equally well everywhere.
4. **Evaluate with several checks.** As in the module, report silhouette on non-noise records alongside the percentage excluded as noise; use the same haversine distance and calculate it only when at least two non-noise clusters exist and there are more retained records than clusters. If sampling is needed, document it. A high score alone does not establish a useful result, especially if most records were excluded. The lesson's synthetic answer labels have no equivalent verified geographic labels here, so do not claim accuracy or agreement with a known true clustering.
5. **Describe each group in ordinary terms.** Following Section 7.6, profile retained groups by district, record count, date range, coordinate repetition and recording precision, retaining event IDs, notes and sources for review. These are descriptions of clusters after fitting, not extra distance features. Describe them as concentrations of recorded places, since repeated or approximate coordinates do not establish distinct incident sites or risk to residents.

The k-distance curves, added diagnostics and cluster profiles above are **proposed Phase 4 work**. They have not been added to this Phase 3 notebook's code or outputs. The completed spatial evidence remains in M13–M14 and its accompanying tables.

"""
assert mark in s;s=s.replace(mark,addition+mark)
n['cells'][i]['source']=s.splitlines(keepends=True)
i=next(i for i,c in enumerate(n['cells']) if ''.join(c['source']).startswith('# References'))
s=''.join(n['cells'][i]['source'])
s=s.replace('5. **Mugot, C. J. S.** *EDA Bivariate Analysis of Categorical Variables*, 2026, course reference for categorical analysis/Monte Carlo testing.',"""5. **Mugot, Chris Jallaine S.** *Bivariate Analysis of Categorical Variables*. DS311 course notebook, `Topic7_Bivariate Analysis [ 2 Categorical ].ipynb`; reference for contingency tables, categorical association and Monte Carlo testing.
6. **Mugot, Chris Jallaine S.** *Bivariate Analysis (Continuous & Continuous)*. DS311 course notebook, `Topic6_Bivariate Analysis[2 Numerical].ipynb`; reference for numerical pair comparisons, Pearson versus Spearman correlation and correlation heatmaps.
7. **Mugot, Chris Jallaine S.** *Bivariate Analysis of Mixed Variables*. DS311 course notebook, `Topic8_Bivariate(Mixed Variables).ipynb`; reference for numerical summaries and distributions compared across categorical groups.
8. **Mugot, Chris Jallaine S.** *Topic 9: Multivariate Analysis (All Numerical Variables)*. DS311 course notebook, `Topic9_MultivariateAnalysisNumericalVariables.ipynb`; reference for correlation matrices, joint variable exploration and overlapping numerical features. Citing the lesson does not imply that its regression/PCA exercises were performed here.""")
s=s.replace('6. **Iglewicz','9. **Iglewicz').replace('7. **Ester','11. **Ester').replace('8. **Software','12. **Software')
s=s.replace('### Spatial clustering method\n','### Spatial clustering method\n\n10. **Menorias, Nicole S.** *Module 7: Cluster Analysis*. DS312 course notebook, `Module_7_DS312_Cluster_Analysis.ipynb`, supplied copy in `C:/Users/USER/Desktop/eda/`. Sections 7.4–7.4.4 cover DBSCAN, core/border/noise points, k-distance selection and parameter sensitivity; Sections 7.5–7.6 cover method comparison and cluster profiling. Basis for the proposed DBSCAN workflow in Task 7; customer-example scaling and numeric parameter values are adapted to geographic distance rather than copied.\n')
n['cells'][i]['source']=s.splitlines(keepends=True)
changed=[i+1 for i,(a,b) in enumerate(zip(before['cells'],n['cells'])) if a!=b]
assert changed==[213,256],changed
assert all(a==b for a,b in zip(before['cells'],n['cells']) if a['cell_type']=='code')
p.write_text(json.dumps(n,ensure_ascii=False,indent=1)+'\n',encoding='utf8')
print('Updated markdown cells',changed,'; all code and saved outputs unchanged.')
