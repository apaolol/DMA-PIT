# 05 — Compare district-specific anomaly baselines

Depends on: 02; execute after 04. Status: Not started.

- [ ] Reuse inspected Phase 3 trailing median/MAD logic and document the modified-z formula, threshold, MAD floor, zero/flat-history treatment and eligibility. Do not silently change formula while comparing windows.
- [ ] Compare 8/12/16-week earlier-only windows per district. Shift history before all rolling calculations; do not pool districts into one local baseline.
- [ ] Keep raw count, political denominator, focal share, baseline, score, direction and eligibility/exclusion reason per district-week. Compare on common scored weeks as well as reporting each setting's coverage.
- [ ] Evaluate alert burden per district, overlap across windows, high/low examples, non-alert comparison weeks and sensitivity to trough recovery. Preserve calendar gaps when history is ineligible; no fabricated complete history.
- [ ] Separate absolute peaks from unusual relative-to-history weeks. Track undefined shares and partial weeks. Recompute actual counts; do not reuse Phase 3 numbers without verification.

Acceptance: at least two settings (three planned), reproducible comparison table and compact time-series diagnostics. Chronological assertions prove each baseline ends before its scored week. Flags remain screening leads, not verified labels or forecasts.
