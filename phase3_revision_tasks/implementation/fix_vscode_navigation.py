import json,re,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'DMA_Phase3_Final_Complete.ipynb'
base=json.loads((Path(__file__).parent/'before_vscode_link_fix.ipynb').read_text(encoding='utf8'))
n=json.loads(json.dumps(base))
heads={}
for i,c in enumerate(n['cells']):
 if c['cell_type']=='markdown':
  for h in re.findall(r'^#+ (.+)', ''.join(c['source']),re.M):
   heads[h.replace(' ','-')]=(i,h)
plain={'Data-guide---what-is-being-counted?','Task-3---Main-figure-register','Task-6---Answers-to-the-business-questions','Task-7---Key-insights-and-modeling-plan','Outlier-screening-method','Spatial-clustering-method'}
report=[]
def replace(m):
 label,target=m.groups()
 if not target.startswith('#'): return m.group(0)
 key=target[1:]
 assert key in heads,key
 i,h=heads[key]
 if key in plain:
  report.append(dict(label=label,target=h,mode='Outline section reference'))
  return label
 for j in range(i+1,len(n['cells'])):
  c=n['cells'][j]
  if c['cell_type']=='code':
   count=c['execution_count']; assert isinstance(count,int)
   report.append(dict(label=label,target=h,cell=j+1,execution_count=count,mode='VS Code exact saved code cell'))
   return f'[{label}](vscode-notebook-cell:?execution_count={count})'
 raise AssertionError(target)
for c in n['cells']:
 if c['cell_type']=='markdown':
  s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',replace,''.join(c['source']))
  c['source']=s.splitlines(keepends=True)
s=''.join(n['cells'][1]['source'])
s+='\n**Navigation in VS Code:** blue evidence links open the exact saved figure or calculation cell. Use the notebook **Outline** for prose sections such as the data guide, figure register, business answers, modeling plan and references. Direct cell links are specific to VS Code and the saved execution numbers; after rerunning cells out of order, use the named section in the Outline.\n'
n['cells'][1]['source']=s.splitlines(keepends=True)
for a,b in zip(base['cells'],n['cells']):
 if a['cell_type']=='code': assert a==b,'Code or output changed'
assert len(base['cells'])==len(n['cells'])
counts=[c['execution_count'] for c in n['cells'] if c['cell_type']=='code']
assert len(counts)==len(set(counts))
assert not re.search(r'\]\(#', '\n'.join(''.join(c['source']) for c in n['cells'] if c['cell_type']=='markdown'))
p.write_text(json.dumps(n,ensure_ascii=False,indent=1)+'\n',encoding='utf8')
(Path(__file__).parent/'vscode_navigation_validation.json').write_text(json.dumps({'links':report,'code_and_outputs_unchanged':True,'cells':len(n['cells']),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2),encoding='utf8')
print(f'Updated {len(report)} references; all code and outputs unchanged.')
