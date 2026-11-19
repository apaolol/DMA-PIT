import json, os, sys, hashlib, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
P=Path(__file__).resolve().parent
os.chdir(ROOT)
runtime=ROOT/'tmp/phase3-runtime'
sys.path.insert(0,str(runtime))
os.environ['PYTHONPATH']=str(runtime)
os.environ['MPLCONFIGDIR']=str(ROOT/'tmp/matplotlib-phase3')
os.environ['IPYTHONDIR']=str(ROOT/'tmp/ipython-phase3')
jpath=ROOT/'tmp/phase3-jupyter'
spec=jpath/'kernels/phase3';spec.mkdir(parents=True,exist_ok=True)
(spec/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Phase3 validation','language':'python','env':{'PYTHONPATH':str(runtime)}}))
os.environ['JUPYTER_PATH']=str(jpath)
os.environ['JUPYTER_RUNTIME_DIR']=str(ROOT/'tmp/phase3-jupyter-runtime')
import nbformat
from nbclient import NotebookClient
import shutil
shutil.copy2(ROOT/'DMA_Phase3_Final_Complete.ipynb', P/'before_full_rerun.ipynb')
n=nbformat.read(ROOT/'DMA_Phase3_Final_Complete.ipynb',as_version=4)
client=NotebookClient(n,timeout=600,kernel_name='phase3',resources={'metadata':{'path':str(ROOT)}})
def report(cell,cell_index,**kw):print('Executing',cell_index+1,cell.get('id'),flush=True)
client.on_cell_start=report
try:
    client.execute()
finally:
    nbformat.write(n,P/'full_rerun.executed.ipynb')
nbformat.validate(n)
assert not any(o.output_type=='error' for c in n.cells if c.cell_type=='code' for o in c.outputs)
for f,h in json.loads((P/'baseline_hashes.json').read_text()).items():
    if f!='DMA_Phase3_Final_Complete.ipynb':assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
from nbconvert import HTMLExporter
template_base=runtime/'share/jupyter/nbconvert/templates'
html,_=HTMLExporter(template_paths=[str(template_base/'lab'),str(template_base/'base'),str(template_base)]).from_notebook_node(n)
(P/'full_rerun.preview.html').write_text(html,encoding='utf-8')
print('EXECUTION PASSED',len(n.cells),'cells',flush=True)

nbformat.write(n,ROOT/'DMA_Phase3_Final_Complete.ipynb')
print('SAVED final destination',flush=True)
