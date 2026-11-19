# Phase 3 revision plan

Status: planning artifacts only. Created November 19, 2026.

## Objective

Produce a concise, coherent, standalone Phase 3 report with explicit data provenance, traceable business-question answers, accurate statistical reporting, purposeful visuals, and the rubric-required closing synthesis.

Creating this folder does not authorize notebook edits. The user approved writing these task files only. Do not treat checkboxes or this plan as approval to implement changes.

## File boundaries

- Only possible edit destination: `C:\Users\USER\Desktop\DMA PIT\DMA_Phase3_Final_Complete.ipynb`.
- Reference only, never edit: `C:\Users\USER\Desktop\DMA PIT\DMA_Phase3_EDA_Bivariate_Multivariate_Merged.ipynb`.
- Other read-only references: `[STUDENT] DS312_FINAL_PIT_GUIDE.pdf`, `DMA_Phase1.ipynb`, `DMA_Phase2.ipynb`, and `data/processed/` under the project root.
- Do not regenerate CSVs, execute notebook cells, clear outputs, change code, remove analyses, or alter interpretation wording under the existing permission scope.
- Interpretation formatting, if approved, must preserve every word and its order, numbers, claims and meaning. Treat result prose embedded in code-generated tables as protected too.

## Approval categories

| Category | Work | Current status |
|---|---|---|
| A | Non-interpretation markdown: orientation, definitions, headings, separate evidence blocks and bibliography organization | Await explicit approval |
| B | Interpretation formatting only, preserving words and order | Await explicit approval |
| C | Interpretation rewriting/corrections/additions, including new BQ findings and final insights | Recommendation only; requires explicit relaxation of the current restriction |
| D | Code, plots, outputs, reruns, removals or analytical consolidation | Recommendation only; requires explicit relaxation of the current restriction |

Mixed cells must be treated at paragraph level. Do not call findings 'administrative markdown' to bypass protection. Relocation of protected text or assigned work must be explicitly included in the approved scope.

## Recommended sequence

1. **01 Baseline and evidence inventory:** establish a recoverable snapshot and stable cell IDs after implementation is authorized.
2. **02 Structure and handoffs:** design a single reader-facing report, with one final bibliography.
3. **03 Data provenance:** explain the four CSVs, cohort definitions, logs and history rules.
4. **04 BQ evidence citations:** attach exact evidence locations while preserving existing answers.
5. **05 Interpretation formatting:** improve presentation without changing wording.
6. **06 Statistical and numerical review:** resolve each substantive issue in a proposed decision log; implement only with C/D authorization.
7. **07 Redundancy and visual quality:** choose consolidations only after evidence links and unique contributions are mapped; implement only with D authorization.
8. **08 Closing insights and modeling plan:** team-authored, evidence-backed completion; requires C authorization.
9. **09 Final validation:** verify approved changes and protected content before delivery.

Tasks 06 and 07 can be reviewed before implementation approval, but changes remain blocked. Do not use subagents unless separately requested. The sequence is not an instruction to execute notebook cells.

## Target reader-facing structure

1. Title, audience, decision and historical scope.
2. Revised BQ1-BQ5, source map, essential definitions and setup.
3. Task 1: Univariate analysis.
4. Task 2: Bivariate and multivariate analysis.
5. Task 3: Compact chart register linking to figures in place.
6. Task 4: Hypothesis testing.
7. Task 5: Pattern spotting and pattern summary.
8. Task 6: Business-question answers with claim-level evidence links.
9. Task 7: Key insights and modeling plan (5-8 insights and chosen techniques).
10. Consolidated limitations and reproducibility notes.
11. Contributor archive, only if needed to preserve approved-to-relocate assigned material.
12. References, once, at the end.

Keep local caveats and method citations beside their analyses. A final bibliography is not a replacement for local citations. Do not move code cells merely to fit this outline.

## Completion gates

- All four CSVs and each figure/table have verified provenance.
- No misleading 'loaded once' or six-column-loading claims remain.
- No teammate instructions or full bibliography interrupts the main analytical narrative.
- Every BQ claim has an exact supporting location or an explicit evidence-gap flag.
- All known statistical/numerical discrepancies are resolved under approval or clearly reported as outstanding; formatting alone cannot make the report submission-ready.
- Every figure has an adjacent interpretation, and the required final synthesis is complete, subject to content approval.
- No plot, output, code, interpretation or assigned work is silently removed or changed.
- Read-only references and CSVs remain byte-identical.

## Location convention

Cell numbers in these tasks are one-based positions in the audited 184-cell final notebook, including markdown cells. They are not execution counts. Reconfirm locations by cell ID, heading and source text before editing; numbers will shift after insertions. Suggested figure IDs and anchors are new identifiers, not claims that they already exist.

## Current implementation status

**Completed November 19, 2026 under subsequent explicit full-revision authorization.** The original approval gates above document the planning-stage constraints; the user later authorized all listed revisions and validation. See `implementation/PROGRESS.md` and `implementation/COMPLETION_REPORT.md` for the delivered state.
