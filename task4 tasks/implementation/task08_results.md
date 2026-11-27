# Task 08 final validation — 2026-11-24

Destination: `DMA_Phase4_Modeling.ipynb`. Task 07 appended S7 and executed the entire notebook from a fresh Jupyter kernel with the project root as working directory. The saved destination matches `validated_task07.ipynb` byte for byte. Seven code cells ran in order with zero error outputs; all input, geographic-unit and chronological assertions embedded in S2-S6 passed.

`validate_final.py` reopened the notebook, validated its schema and execution order, confirmed Tables 1-25 and Figures 1-4, and checked all 19 protected hashes against the Task 01 baseline. All four figures were visually inspected for titles, labels, units, legends and clipping. S1-S7 headings and numbered table/figure names provide navigation without viewer-specific hyperlinks; no direct editor navigation test was available.

Runtime: Python 3.12.14, NumPy 2.5.5, pandas 3.1.1, scikit-learn 1.9.1, matplotlib 3.11.2, nbformat 5.11.1, nbclient 0.11.0; random seed 42 where sampling or Isolation Forest is used. The fresh run required elevated local execution because the sandbox restricts Jupyter kernel sockets.

The results are retrospective screens of recorded data. Independent review labels and truly unseen later data remain unavailable; Isolation Forest remains experimental. The last partial week is excluded. Final all-phase integration, submission materials and individual work are separate.
