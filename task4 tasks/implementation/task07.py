from workflow import md, run, complete

summary = r'''
## S7. What should a documentation team take from these screens?

### Answers to the five business questions

| Question | Answer and evidence |
|---|---|
| BQ1: change before and after October 7, 2023 | Phase 3's descriptive comparison remains the answer. Phase 4 deliberately models the post-cutoff Gaza land cohort; its clusters and local screens cannot estimate the before/after change or the West Bank. See Phase 3 Task 6. |
| BQ2: actors and event types | Phase 3's coded actor/event cross-tabs and incident notes remain the answer. Phase 4 uses the exact focal flag and retains source IDs/notes for review; it does not infer an actor's intent or role. See Phase 3 Task 6 and Phase 4 Table 10. |
| BQ3: geographic concentrations | Among 10,583 post-cutoff land focal records at 101 coordinate pairs, the descriptive 1 km/50 DBSCAN reference groups recorded places within districts (Tables 5, 8-10; Figure 2). Gaza City has 3,436 records in the district baseline (Table 8). The largest displayed group has 852 records across four coordinate pairs, mainly Gaza - Shujaiyya (Table 9). Repeated and approximate coordinates make these concentrations of *recorded places*, not measured incident footprints. Nearby radii and the precision-1 restriction change memberships (Tables 6-7). |
| BQ4: unusual district-weeks | Earlier-only 8/12/16-week median/MAD screens score 465/441/417 district-weeks and flag 48/34/22, respectively (Table 18). The 8-versus-16 overlap is 14 of 54 weeks flagged by either setting among common scored weeks (Table 14). Table 17 gives traceable high, low and ordinary examples; Figure 3 keeps gaps visible. These are review leads relative to prior local records, not verified anomalies. |
| BQ5: sensitivity | The spatial candidate grid changes group and noise counts (Tables 5-7); the narrower temporal window produces more flags (Tables 14 and 18). The forest comparison uses the same assessment weeks but yields different candidates (Table 23; Figure 4). Neither method has independent review labels. The historical snapshot was already explored in Phase 3, so even the later chronological block is retrospective. |

### What each method contributes

| Method | Population and retained setting | Simple comparison and evaluation | Practical use and limit |
|---|---|---|---|
| DBSCAN | 10,583 post-cutoff Gaza land focal records; 1 km radius/50 records is a descriptive reference, alongside the full radius/density grid and precision-1 check (Tables 4-7) | District totals (Table 8); group/noise sizes, sampled non-noise haversine silhouette, nearby-setting and common-ID membership comparisons (Tables 5-7) | Names nearby recorded places within a district for source review (Table 9, Figure 2). Coordinate repetition, imprecise locations and radius sensitivity limit geographic inference. |
| Median/MAD | Complete district-weeks with positive political denominator and intact earlier calendar history; 12-week reference, with 8/16-week sensitivity (Tables 12-20) | Raw count/share and earlier local baseline; common-week coverage, burden, overlap, peaks and rebounds (Tables 13-20, Figure 3) | Produces explainable high and low review leads. Short history, changing reporting and no labels limit interpretation. |
| Isolation Forest, experimental | District-specific earlier-only fits; frozen two-feature, 32-sample candidate and tuning-derived cutoffs (Tables 21-25) | Same assessable assessment weeks as 12-week MAD, with overlap and traced examples (Table 23, Figure 4) | Offers a second candidate list, but added documentary value is unverified. Keep MAD as the primary screen. |

Metrics across these rows answer different questions; their values do not form a ranking. Tables 10 and 25 retain source examples, while the complete assignments and scores are saved under `task4 tasks/implementation/` for audit. A reviewer should follow an event ID to its note and source, confirm place/date coding and compare independent records before drawing a substantive conclusion.

### Recommendations

1. Start a place-based source review with the largest and persistent groups in Table 9, using the district baseline in Table 8 and map in Figure 2 for context. Sample both precise and coarser coded locations, and check whether repeated coordinates represent distinct recorded events.
2. Review completed district-weeks that the 12-week screen flags across multiple window lengths (Tables 14, 17-18). Read the raw focal count, political denominator, share, earlier median and event notes together; do not treat the flag as a finding.
3. Keep a separate small sample of window-specific flags, rebound weeks and ordinary comparison weeks (Tables 17, 19-20). This tests whether the screening rule is useful across changing local activity instead of selecting only dramatic peaks.
4. Have independent documentation reviewers record a consistent disposition and reasons for a bounded sample from the MAD and forest lists (Tables 23-25). Compare their usefulness only after such labels exist; do not automate attribution or intervention from these screens.

**Limits and next evidence.** ACLED coverage and coding depend on reporting and access; absence of a record is not absence of an event. The focal definition selects an exact coded civilian label, and land/precision restrictions further change who enters the spatial analysis. Rounded or repeated coordinates, district aggregation, time dependence, short eligible histories, undefined shares and the incomplete final week constrain the results. No independent truth labels, on-site verification or untouched future data are available. The next defensible evaluation needs a newly collected period and documented human review, with settings fixed beforehand.

**Sources.** ACLED event data and codebook (source dataset); DS312 Phase 1 business questions, Phase 2 preprocessing/provenance and Phase 3 data guide, Task 6 and Task 7; DS312 final PIT guide, pp. 5-6; Menorias, *Module 7 DS312 Cluster Analysis*, §§7.4-7.6; scikit-learn DBSCAN, silhouette and IsolationForest documentation; pandas and NumPy documentation. S2 and the recorded runtime specify the local input files and package versions.
'''

run([md(summary)], 7)
complete(7, 'S7 synthesis added and fresh-kernel execution passed; every cited Phase 4 quantity checked against Tables 5, 8-9, 14, 18 and 23. Four recommendations, cross-technique table, BQ1-BQ5 and limitations recorded. Final validation remains Task 08.')
