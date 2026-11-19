import ast,nbformat
nb=nbformat.read('DMA_Phase3_EDA_Bivariate_Multivariate_Merged.ipynb',as_version=4)
t=lambda c: ''.join(c.source)
print('cells',len(nb.cells),'code',sum(c.cell_type=='code' for c in nb.cells))
for i,c in enumerate(nb.cells):
 s=t(c)
 if c.cell_type=='markdown' and (s.startswith('## 3.5') or 'Phase 2 snapshot consistency' in s or 'Handoff notes for teammates' in s): print(f'MD {i}: {s[:750]}')
 if c.cell_type=='code':
  try:tree=ast.parse(s)
  except:continue
  defs=[]
  for n in ast.walk(tree):
   if isinstance(n,ast.Assign):
    for a in n.targets:
     if isinstance(a,ast.Name) and a.id in {'BEFORE','AFTER','CUTOFF','EVENT_TYPES','political','period_from_date','PERIOD_DAYS'}: defs.append(a.id)
     elif isinstance(a,ast.Tuple): defs.extend(x.id for x in a.elts if isinstance(x,ast.Name) and x.id in {'BEFORE','AFTER','CUTOFF','EVENT_TYPES','political','period_from_date','PERIOD_DAYS'})
  if defs: print(f'CODE {i} shared defs: {defs}')
