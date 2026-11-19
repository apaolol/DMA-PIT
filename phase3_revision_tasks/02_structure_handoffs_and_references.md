# Task 02 - Structure, handoffs and references

Category: A for administrative markdown; protected-content relocation needs explicit approval; rewriting/deleting findings needs C, and code/output changes need D.
Depends on: Task 01.

## Exact cleanup targets

| Original cells | Issue | Proposed action |
|---|---|---|
| 1-3 | Weak audience/decision/BQ orientation; inaccurate 'loaded once' claim | Add compact context and revised BQ overview; describe actual loading honestly |
| 8-10 | Starts at 3.7/3.8; unnecessary discussion of optional generic helpers | Replace administrative framing with a direct Task 1 introduction; preserve helper code |
| 40-46 | Duplicate title, introduction and setup | Consolidate markdown framing; do not remove loaders without D approval |
| 68 | A subsection merely says an actor plot is not repeated | Replace redundant navigation with a direct link, subject to markdown approval |
| 80-81 | 'Carry-forward notes', hypothesis inputs, 'For the insights writer' | Keep unique findings; propose relocation of workflow material rather than leaving it in the main narrative |
| 85-92 | Repeated title page; setup says six columns but loads 43; tests use earlier master | Simplify administrative text and state the actual dependency |
| 107 | Useful test conclusions mixed with writer handoff | Keep conclusions/caveats local; separately propose relocating the final handoff paragraph |
| 108 | Full References block between Tasks 4 and 5 | Consolidate entries into final bibliography; keep short method citations local |
| 110-111 | Teammates/task-tracker/'that notebook' framing; wrong Task 3 plot attribution | Replace workflow framing with what pattern spotting adds; reference Task 2 plots accurately |
| 112-116 | Another setup/loader/check block | Describe correctly; code consolidation remains a separate recommendation |
| 173-174 | 'Pattern register and handoff' | Rename markdown heading 'Pattern summary'; preserve code/output and flag register discrepancies separately |
| 175 | Named handoffs to Mark/Kyle, followed by limitations/checklist/references before BQ answers | Propose moving protected handoff content intact to an archive or approved closing location; consolidate global limitations/checklist; move bibliography to end |
| 176-177 | Merge-history commentary, generic '2. Sources' list | Replace with evidence-reading guidance; use Task 04 citations, not notebook filenames as evidence |
| 178 | Stray leading pipe | Remove formatting artifact only, preserving words |
| 183 | Closing material before Task 7 | Consolidate final limitations/reproducibility after Task 7 |
| 184 | Unfinished Task 7 | Preserve honest status until Task 08 is authorized and completed |

## Navigation scheme

- Use Task 1-7 consistently; avoid competing section trees that restart at 1.
- Assign unique markdown anchors next to figures, for example `t2-period-share-rate`, `t4-hypothesis-a`, `t5-spatial-precision`.
- In citations use task + descriptive figure/table name; retain old chart numbers only with the task qualifier.
- Fix stale references to Section 3.9 and ambiguous Chart 5/7/11. Do not rewrite those inside protected interpretations without C approval; add separate navigation notes if only A is approved.
- Update the chart register without modifying plot titles embedded in saved images.
- Preserve contributor attribution in an appropriate end section if required; do not remove assigned work just because it is repetitive.

## Acceptance

One integrated narrative, one final bibliography, no full reference blocks or instructions to teammates interrupting analysis. Any protected content that cannot be moved under approval is reported as outstanding, not silently removed.

## Implementation progress

Implemented in the revision candidate using Astra's existing draft. Single final bibliography; no mid-report handoffs; Tasks 1-7 anchored. Static checks passed; final execution and visual validation are tracked in Task 09. Full changes were explicitly authorized by the user.

## Final validation status

Complete. The authorized revision is saved in `DMA_Phase3_Final_Complete.ipynb`. Task 09 verified 56 consecutive code executions, 29 figures, no saved errors/warnings, valid notebook schema and 43 internal-link destinations. Reference/data hashes are unchanged. All figure contact sheets were visually inspected; see `implementation/COMPLETION_REPORT.md`.
