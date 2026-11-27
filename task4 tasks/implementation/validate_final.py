from pathlib import Path
import json, hashlib, sys
import nbformat

root = Path.cwd()
out = root / 'task4 tasks/implementation'
dest = root / 'DMA_Phase4_Modeling.ipynb'
nb = nbformat.read(dest, as_version=4)
nbformat.validate(nb)
code = [c for c in nb.cells if c.cell_type == 'code']
assert [c.execution_count for c in code] == list(range(1, len(code) + 1))
errors = [o for c in code for o in c.outputs if o.output_type == 'error']
assert not errors, errors
headings = '\n'.join(''.join(c.source) for c in nb.cells if c.cell_type == 'markdown')
for section in ('S1.', 'S2.', 'S3.', 'S4.', 'S5.', 'S6.', 'S7.'):
    assert section in headings, section
for number in range(1, 26):
    assert f'Table {number}' in headings or any(f'Table {number}' in ''.join(str(o) for o in c.outputs) for c in code), number
    assert (out / f'Table_{number}.csv').exists(), number
for number in range(1, 5):
    assert f'Figure {number}' in headings or any(f'Figure {number}' in ''.join(str(o) for o in c.outputs) for c in code), number
    assert list(out.glob(f'Figure_{number}_*.png')), number
hashes = json.loads((out / 'protected_hashes.json').read_text(encoding='utf-8'))
changed = []
for name, expected in hashes.items():
    p = Path(name)
    if not p.is_absolute(): p = root / p
    if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
        changed.append(name)
assert not changed, changed
assert dest.read_bytes() == (out / 'validated_task07.ipynb').read_bytes()
print(f'Notebook valid: {len(nb.cells)} cells, {len(code)} sequential code cells, 0 error outputs')
print('Tables 1-25 and Figures 1-4 present; protected hashes unchanged:', len(hashes))
print('Saved destination matches freshly executed Task 07 candidate')
print('Python:', sys.version.split()[0])
