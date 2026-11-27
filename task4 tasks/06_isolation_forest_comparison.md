# 06 — Assess whether Isolation Forest adds value

Depends on: 05. Status: Complete.

Isolation Forest is conditional on sufficient earlier history and an interpretable design. The anomaly family already has multiple baseline settings; an additional algorithm is not required solely to increase model count.

- [x] Assess history sufficiency per district and define a defensible district-specific or explicitly justified pooled design before fitting. Record exclusions and training size.
- [x] Start with a small feature set: current completed-week focal count, optional political count/share, and verified previous-week/previous-four-week features. Avoid IDs, source-update timestamps and review flags as predictors; compare subsets for duplicated count/ratio information.
- [x] Fit any imputation/transformation and Isolation Forest on earlier weeks only, under Task 02's design. Set seed; document two candidate settings if proceeding. Select any score cutoff using earlier tuning data/review budget, not desired labels in assessment weeks.
- [x] Compare with the frozen median/MAD baseline on identical assessable weeks: coverage, alert burden, overlap, sensitivity and traceable examples. No accuracy/F1 against baseline flags.
- [x] Record a retain/reject/defer decision. If infeasible or unhelpful, explain evidence and retain the simpler detector; do not fabricate superiority or independent review.

Acceptance: either valid reproducible comparison or documented feasibility decision. Distinguish internal retrospective checks from genuinely unseen validation. Two selected families remain DBSCAN and anomaly detection regardless of this decision.
