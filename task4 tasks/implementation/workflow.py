from pathlib import Path
import json,hashlib,shutil,sys,os
import nbformat
from nbclient import NotebookClient
ROOT=Path.cwd(); OUT=ROOT/'task4 tasks/implementation'; DEST=ROOT/'DMA_Phase4_Modeling.ipynb'
def md(s): return nbformat.v4.new_markdown_cell(s.strip())
def code(s): return nbformat.v4.new_code_cell(s.strip())
def run(cells,task):
 old=DEST.read_bytes() if DEST.exists() else None
 if old: shutil.copy2(DEST,OUT/f'before_task{task:02}.ipynb')
 nb=nbformat.reads(old.decode('utf-8'),as_version=4) if old else nbformat.v4.new_notebook(metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':sys.version.split()[0]}})
 nb.cells.extend(cells)
 os.environ['IPYTHONDIR']=str(ROOT/'tmp/ipython-phase4');os.environ['MPLCONFIGDIR']=str(ROOT/'tmp/matplotlib-phase4')
 client=NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}})
 # Explicit interpreter prevents accidentally selecting an unrelated system Python.
 from jupyter_client import KernelManager
 km=KernelManager(kernel_name='python3');km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'];client.km=km
 client.execute()
 candidate=OUT/f'validated_task{task:02}.ipynb';nbformat.write(nb,candidate)
 assert (DEST.read_bytes() if DEST.exists() else None)==old,'Destination changed externally; candidate retained'
 DEST.write_bytes(candidate.read_bytes())
 print('Validated task',task,'code cells',sum(c.cell_type=='code' for c in nb.cells),flush=True)
def complete(task,detail):
 p=next((ROOT/'task4 tasks').glob(f'{task:02}_*.md'));p.write_text(p.read_text(encoding='utf-8').replace('Status: Not started.','Status: Complete.').replace('- [ ]','- [x]'),encoding='utf-8')
 p=ROOT/'task4 tasks/PROGRESS.md';s=p.read_text(encoding='utf-8');lines=s.splitlines()
 for i,line in enumerate(lines):
  if line.startswith(f'| {task:02} '): lines[i]=line.replace('Not started','Complete').replace('— |',f'implementation/task{task:02}_results.md |')
 s='\n'.join(lines)+'\n';s+=f'\n2026-11-24 — Task {task:02} complete — {detail} — Next: Task {task+1:02}.\n';p.write_text(s,encoding='utf-8')
 (OUT/f'task{task:02}_results.md').write_text(f'# Task {task:02} results - 2026-11-24\n\n{detail}\n',encoding='utf-8')

