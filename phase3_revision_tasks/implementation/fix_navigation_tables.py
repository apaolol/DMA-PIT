import json,copy,re,ast,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
dest=ROOT/'DMA_Phase3_Final_Complete.ipynb'
backup=P/'before_navigation_table_fix.ipynb'
if not backup.exists():shutil.copy2(dest,backup)
n=json.loads(backup.read_text(encoding='utf-8'))
def source(c):return ''.join(c['source'])

# Derive links from actual rendered heading IDs rather than hidden HTML anchors.
# IDs are obtained from nbconvert's renderer, not guessed from a slug formula.
import sys
sys.path.insert(0,str(ROOT/'tmp/phase3-runtime'))
import nbformat
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
base=ROOT/'tmp/phase3-runtime/share/jupyter/nbconvert/templates'
exporter=HTMLExporter(template_paths=[str(base/'lab'),str(base/'base'),str(base)])
mapping={}
for c in n['cells']:
 if c['cell_type']!='markdown':continue
 s=source(c)
 # Method-reference anchors were inside bibliography lines; give each a real
 # heading so it is also navigable without arbitrary HTML support.
 s=s.replace('6. <a id="ref-outliers"></a>','\n\n### Outlier screening method\n\n<a id="ref-outliers"></a>\n\n6. ')
 s=s.replace('7. <a id="ref-dbscan"></a>','\n\n### Spatial clustering method\n\n<a id="ref-dbscan"></a>\n\n7. ')
 anchors=list(re.finditer(r'<a id="([^"]+)"></a>',s))
 # The method markers must precede their headings for the same mapping logic.
 s=s.replace('### Outlier screening method\n\n<a id="ref-outliers"></a>','<a id="ref-outliers"></a>\n### Outlier screening method')
 s=s.replace('### Spatial clustering method\n\n<a id="ref-dbscan"></a>','<a id="ref-dbscan"></a>\n### Spatial clustering method')
 for m in re.finditer(r'<a id="([^"]+)"></a>',s):
  heading=re.search(r'^#{1,6}\s+(.+)$',s[m.end():],re.M)
  assert heading,(c['id'],m.group(1))
  heading_text=heading.group(1)
  mini=nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell('## '+heading_text)])
  html,_=exporter.from_notebook_node(mini)
  h=BeautifulSoup(html,'html.parser').find('h2')
  mapping[m.group(1)]=h['id']
 s=re.sub(r'<a id="[^"]+"></a>\s*\n?', '',s)
 c['source']=s

for c in n['cells']:
 if c['cell_type']=='markdown':
  c['source']=re.sub(r'\]\(#([^)]*)\)',lambda m:'](#'+mapping.get(m.group(1),m.group(1))+')',source(c))

# Brief local readings for every displayed table in Task 1. The calculations,
# filters and tabular outputs themselves are unchanged.
notes={
13:["**Event-master profile.** The 43 fields include source information and Phase 2 features. Actor/association blanks and the unrecorded targeting label have different meanings; the four constant geographic fields add no variation within this Gaza extract."],
14:["**Gaza-week profile.** Each row is a post-cutoff Gaza week. Early missing lag values mean eligible preceding history is unavailable; the final partial week is excluded from history, rather than being treated as a complete low-activity week.",
    "**District-week profile.** Rows cover five districts over the same calendar. Zero political counts make focal share undefined, while ineligible history creates additional missing lag values; neither should be silently replaced with an observed zero.",
    "**Spatial-input profile.** These selected fields describe the post-cutoff land focal subset, not all event-master records. Coordinates and precision are available, but repeated coordinates and quality categories limit how precisely a point can be interpreted."],
15:["**Narrative length.** Event notes vary in length, so a single short excerpt may omit context. This is a description of the text available for review, not a severity score or a direct model feature.",
    "**Source-scale frequencies.** These counts describe the recorded reporting-scale labels; they do not measure source accuracy or establish complete coverage. A combined label remains as recorded.",
    "**Individual tag frequencies.** A record may have several tags, so the tag counts can overlap and should not be added as if they were mutually exclusive events. Blank tags remain unknown or unrecorded."],
19:["**Raw fatality summary.** The median is zero and the upper percentiles extend far above it, showing many zero records and a long right tail. Reported totals refer to the whole event, so neither the mean nor the sum is a count of confirmed civilian deaths.",
    "**Log-fatality summary.** This is the inherited natural log of one plus reported fatalities. It compresses large counts and preserves zeros; its values are transformed units, not additional fatalities.",
    "**Review-threshold summary.** The Phase 2 flag uses the full-export cutoff greater than 23 and retains 576 Gaza records for review. The Gaza-only 99th percentile is different, so changing thresholds changes which records are flagged rather than proving either group invalid."],
23:["**Event-type frequencies.** Explosions/Remote violence dominates the all-event master. These percentages use all records; they differ from the focal prevalence within an event type tested later.",
    "**Sub-event frequencies.** Air/drone strikes and shelling are the largest detailed categories, while many others have few records. Each sub-event type belongs to one parent type, so these are related descriptions, not independent sets of events.",
    "**Disorder-label frequencies.** The table retains combined disorder labels. Political-violence membership uses an exact token check, so a record carrying both Political violence and Demonstrations still belongs in the political denominator."],
27:["**Actor-field completeness.** First-actor fields are complete, while second-actor and second-type blanks occur together. The check below confirms these blanks belong to single-sided interaction coding rather than providing evidence of an unidentified second actor.",
    "**First actors across all events.** A small number of labels account for most records. These are original ACLED labels across both periods and all event types, not verified assignments of responsibility.",
    "**Second actors across all events.** Civilians (Palestine) is frequent, and the missing category represents records without a coded second actor. A blank should not be interpreted as a named participant or as evidence that civilians were unharmed.",
    "**First actors within focal events.** Military Forces of Israel (2022-) accounts for 97.9% of this subset. The denominator is focal events, so these shares should not be confused with the preceding all-event actor frequencies.",
    "**First-actor types.** This broader category table describes the types assigned to actor1, rather than distinct individual actors. Category prevalence alone does not verify roles in a particular incident.",
    "**Date-versioned Israeli-forces labels.** The date ranges show the older label ending before the newer label begins. Both source labels remain separate; interpreting or merging them requires a documented analyst decision."],
30:["**Targeting-flag counts.** True means ACLED recorded the Civilian targeting label; False means that label was not recorded. This is broader than the project's focal rule and is not a complete census of civilian harm.",
    "**Political-violence counts.** This flag identifies the comparison population used for focal shares. Its denominator here is all Gaza master records, whereas later focal-share calculations divide only by political records.",
    "**Focal-rule counts.** True requires both the targeting flag and the exact Palestinian civilian actor label. False means the rule is not met; within political-only comparisons it denotes the other political records, not proof of no civilian harm."],
33:["**Location-precision comparison.** Precision 1 is more prevalent in the land focal subset than in the full master. The populations also differ by period and focal/land restrictions, so this difference cannot be attributed to precision alone.",
    "**Date-precision comparison.** Code 1 predominates in both tables, but the less precise records remain identifiable. Their small proportion does not itself prove that shifting uncertain dates would leave weekly results unchanged.",
    "**Location precision by period.** The proportion at precision 1 is substantially higher after the cutoff. Before/after spatial comparisons therefore have different recording-quality mixes, motivating the later within-period precision checks."],
37:["**District frequencies.** Gaza City has the most all-event records, while four records have no known district. Their share among known districts is left undefined; they remain in Gaza-wide counts rather than being assigned to a district.",
    "**Annual frequencies.** These are counts of all recorded events, with 2025 covering January-September only. Different coverage lengths mean raw annual totals are not directly comparable annual rates.",
    "**Monthly and weekly count summaries.** These distributions use all-event calendar-month and Saturday-start-week totals from the master, including boundary periods. They summarize recording volume, not post-cutoff focal counts or equal-duration exposure."],
}

def mdcell(s,ident):return {'cell_type':'markdown','id':ident,'metadata':{},'source':s+'\n'}
def codecell(s,ident,original):
 return {'cell_type':'code','id':ident,'metadata':{'phase3_original_cell':original,'table_reading_split':True},'source':s,'outputs':[],'execution_count':None}

result=[]
for c in n['cells']:
 orig=c.get('metadata',{}).get('phase3_original_cell')
 if c['cell_type']!='code' or orig not in notes:
  # Replace the old consolidated profiles paragraph with a short transition;
  # individual interpretations now occur beside the corresponding table.
  if orig in [16,17] and c['cell_type']=='markdown':continue
  result.append(c);continue
 s=source(c)
 if orig==30:
  # Unroll only the display loop so each flag gets its own markdown cell.
  for j,(col,note) in enumerate(zip(['targeting_flagged','political_violence','focal_event'],notes[30])):
   chunk=f'''col = {col!r}
counts = master[col].value_counts(dropna=False).reindex([True, False], fill_value=0)
table = pd.DataFrame({{"count": counts, "share_pct": (100 * counts / len(master)).round(2)}})
print(f"{{col}}: denominator = all {{len(master):,}} Gaza event records")
display(table)
'''
   result.extend([codecell(chunk,c['id'] if j==0 else f't1-table-{orig}-{j}',orig),mdcell(note,f't1-reading-{orig}-{j}')])
  continue
 tree=ast.parse(s);displays=[node for node in tree.body if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='display']
 assert len(displays)==len(notes[orig]),(orig,len(displays),len(notes[orig]))
 lines=s.splitlines(keepends=True);start=0
 for j,(node,note) in enumerate(zip(displays,notes[orig])):
  end=node.end_lineno
  chunk=''.join(lines[start:end]);start=end
  result.extend([codecell(chunk,c['id'] if j==0 else f't1-table-{orig}-{j}',orig),mdcell(note,f't1-reading-{orig}-{j}')])
 tail=''.join(lines[start:])
 if tail.strip():result.append(codecell(tail,f't1-table-{orig}-tail',orig))
n['cells']=result
for c in n['cells']:
 if c['cell_type']=='code':c['execution_count']=None;c['outputs']=[]
 if isinstance(c['source'],str):c['source']=c['source'].splitlines(keepends=True)
(P/'navigation.candidate.ipynb').write_text(json.dumps(n,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
(P/'navigation_mapping.json').write_text(json.dumps(mapping,indent=2))
print('Updated',len(mapping),'heading destinations and added',sum(len(v) for v in notes.values()),'table-specific interpretations')
