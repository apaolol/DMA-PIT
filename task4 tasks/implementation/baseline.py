from pathlib import Path
import hashlib,json
root=Path.cwd(); out=root/'task4 tasks/implementation'
refs=list(root.glob('*.ipynb'))+list((root/'phase3_revision_tasks').glob('*.ipynb'))+list(root.glob('*.pdf'))+list((root/'data').rglob('*'))+[Path('C:/Users/USER/Desktop/eda/Module_7_DS312_Cluster_Analysis.ipynb')]
hashes={str(p.relative_to(root)) if p.is_relative_to(root) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in refs if p.is_file()}
(out/'protected_hashes.json').write_text(json.dumps(hashes,indent=2))
(out/'baseline.md').write_text('''# Baseline - November 24, 2026
No existing Phase 4 notebook or scripts found. Destination: `DMA_Phase4_Modeling.ipynb`.
The requested Final_Complete and merged references exist under `phase3_revision_tasks/`, not the root. Both are protected. Root `DMA_Phase3.ipynb` is the later current notebook; its Task 7 agrees with the handoff on the selected families and precautions. Existing git deletions/moves are user state and are preserved.
Protected files are fingerprinted in protected_hashes.json (all current notebooks, project PDFs, data files and the external Module 7 notebook). No destination required backup at baseline because none existed.

| Requirement (rubric pp. 5-6) | Planned evidence |
|---|---|
| Two justified families | S1 purpose: geographic DBSCAN and local temporal screening |
| Inputs, feature choice and leakage | S2 provenance, assertions, frozen design |
| Simple baseline | S4 district counts; S5 median/MAD |
| Two settings per family | S3 radii/density grid; S5 8/12/16 weeks |
| Appropriate evaluation | S4 silhouette/noise/stability; S5 coverage/burden/overlap |
| Profiles and interpretation | S4 original-unit cluster profiles; S5 traced weeks |
| Limitations and ethics | S7 snapshot, coverage, precision, no truth labels |
| 3-5 recommendations | S7 findings-linked review steps |
| Fresh execution and readable outputs | S8 execution and validation record |

References inspected: Phase 1 business questions, Phase 2 feature/output code, current and archived Phase 3 data guide/Tasks 6-7/spatial and local-history evidence; rubric pages 5-6; Menorias Module 7 Sections 7.4-7.6. Source material is read-only. Final all-phase integration is separate.
''',encoding='utf-8')
p=root/'task4 tasks/01_baseline_and_rubric.md';s=p.read_text();p.write_text(s.replace('Status: Not started.','Status: Complete.').replace('- [ ]','- [x]'))
p=root/'task4 tasks/PROGRESS.md';s=p.read_text().replace('Status: **Planning handoff only. No Phase 4 implementation completed.**','Status: **Implementation underway; Task 01 complete.**').replace('| 01 Baseline/rubric | Not started | — |','| 01 Baseline/rubric | Complete | implementation/baseline.md; protected_hashes.json |');s+='\n2026-11-24 — Task 01 complete — baseline inventory, rubric map and protected hashes recorded. No existing Phase 4 implementation. References relocated under phase3_revision_tasks; root Phase 3 also inspected. No protected changes. Next: Task 02.\n';p.write_text(s)
print('Baseline recorded:',len(hashes),'protected files')
