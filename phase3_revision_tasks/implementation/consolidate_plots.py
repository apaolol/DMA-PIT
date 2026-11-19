"""Reuse the current plot code, retaining all computations and supporting figures."""
import json, copy, re, shutil
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
target=ROOT/'DMA_Phase3_Final_Complete.ipynb'
backup=P/'before_plot_consolidation.ipynb'
if not backup.exists():shutil.copy2(target,backup)
n=json.loads(backup.read_text(encoding='utf-8'))
cells=n['cells']
by={c.get('metadata',{}).get('phase3_original_cell'):c for c in cells if c.get('metadata',{}).get('phase3_original_cell')}
by[184]=next(c for c in cells if c.get('id')=='b0e2731a')
def text(c):return ''.join(c['source'])
def setsrc(c,s):c['source']=s.strip()+'\n'
def md(s,ident):return {'cell_type':'markdown','id':ident,'metadata':{},'source':s.strip()+'\n'}
def code(s,ident):return {'cell_type':'code','id':ident,'metadata':{},'source':s.strip()+'\n','execution_count':None,'outputs':[]}

# Capture already-existing supporting figures at their original computation point.
# Rendering them later from global variables could change their input state.
helpers='''
from io import BytesIO
from IPython.display import Image as NotebookImage
supporting_figures = {}

def save_supporting_figure(key, figure):
    buffer = BytesIO()
    figure.savefig(buffer, format="png", dpi=140, bbox_inches="tight", facecolor="white")
    supporting_figures[key] = buffer.getvalue()
    plt.close(figure)

def show_supporting_figure(key):
    display(NotebookImage(data=supporting_figures[key]))
'''
setsrc(by[4],text(by[4])+helpers)
setsrc(by[24],text(by[24]).replace('def short(', 'def short_label(').replace('[short(', '[short_label('))
# Other use of the label helper resides in the same source cell.
setsrc(by[24],text(by[24]).replace('short(i)', 'short_label(i)'))

support_specs=[
 (28,'A1','Recorded actor profiles','t1-actors',29),
 (38,'A2','All-event district and month counts','t1-area-time',39),
 (54,'A3','Fatality ECDF by focal status','t2-fatality-status',55),
 (66,'A4','Event-type composition by period','t2-composition',67),
 (75,'A5','Within-district focal prevalence','t2-district-shares',76),
 (122,'A6','Smaller-class sample sizes','t5-imbalance',123),
 (127,'A7','Highest reported fatality records','t5-fatality-review',128),
 (130,'A8','Timing of high-fatality flags','t5-fatality-time',131),
 (144,'A9','Monthly grouped count/share summary','t5-trends',145),
 (160,'A10','Exploratory groups of weeks','t5-week-clusters',161),
]
appendix=[]
for orig,key,title,anchor,interp in support_specs:
 c=by[orig];s=text(c)
 assert 'plt.show()' in s,orig
 setsrc(c,s.replace('plt.show()',f'save_supporting_figure("{key}", fig)'))
 # Keep the source tables and definitions in place, but show the visual and its
 # interpretation only once in the appendix.
 appendix.extend([md(f'<a id="appendix-{key.lower()}"></a>\n## {key} - {title}\n\nSource, population and method: [original analysis](#{anchor}).',f'appendix-{key}-heading'),
                  code(f'show_supporting_figure("{key}")',f'appendix-{key}-figure'),
                  md(text(by[interp]),f'appendix-{key}-interpretation')])
 setsrc(by[interp],f'The supporting figure and its interpretation are in [Appendix {key}](#appendix-{key.lower()}); the calculations and tables above remain available here.')

def rendering_function(orig,name,split_at=None):
 """Extract the unchanged drawing body; calculations before subplots stay put."""
 c=by[orig];s=text(c)
 start=s.index('fig, ')
 prep=s[:start]
 body=s[start:]
 lines=body.splitlines()
 # These plot cells create their figure on one line.
 assert 'plt.subplots' in lines[0],(orig,lines[0])
 lines=lines[1:]
 cleaned=[]
 for line in lines:
  if line.strip().startswith('fig.suptitle('):
   continue
  line=line.replace('plt.tight_layout(); fig.subplots_adjust(bottom=0.30); plt.show()','')
  line=line.replace('plt.tight_layout(); plt.show()','').replace('plt.tight_layout()','').replace('plt.show()','')
  cleaned.append(line)
 body='\n'.join(cleaned).strip()
 # Single-axis source B1 expects ax; other sources expect axes.
 arg='ax' if orig in [48,69] else 'axes'
 setsrc(c,prep+f'\ndef {name}(fig, {arg}):\n'+'\n'.join('    '+l for l in body.splitlines()))
 return prep,body

rendering_function(48,'draw_period_rates')
rendering_function(99,'draw_period_shares')
rendering_function(69,'draw_district_heatmap')
rendering_function(135,'draw_weekly_anomalies')
rendering_function(164,'draw_spatial_maps')
# Share panel from the existing B8 plot; count panel is superseded in the main
# report by the same count series with anomaly markers, rather than repeated.
s=text(by[72]);start=s.index('fig, axes =');prep=s[:start]
share=s[s.index('ax = axes[1]')+len('ax = axes[1]'):]
share=share.replace('plt.tight_layout()','').replace('plt.show()','')
setsrc(by[72],prep+'\ndef draw_weekly_share(fig, ax):\n'+'\n'.join('    '+l for l in share.strip().splitlines()))

# Split existing calendar panels; retain weekday analysis as an appendix figure.
s=text(by[148]);prep=s[:s.index('fig, axes =')]
draw=s[s.index('ax = axes[0]')+len('ax = axes[0]'):]
left,right=draw.split('ax = axes[1]',1)
right=right.replace('plt.tight_layout(); plt.show()','')
setsrc(by[148],prep+'\ndef draw_calendar_months(fig, ax):\n'+'\n'.join('    '+l for l in left.strip().splitlines())+
 '\n\nfig, ax = plt.subplots(figsize=(8, 4.8))\n'+right.strip()+'\nplt.tight_layout(); save_supporting_figure("A11", fig)')
rendering_function(151,'draw_persistence')

# Split existing district contribution and variability panels.
s=text(by[155]);prep=s[:s.index('fig, axes =')]
draw=s[s.index('ax = axes[0]')+len('ax = axes[0]'):]
left,right=draw.split('ax = axes[1]',1)
right=right.replace('plt.tight_layout(); fig.subplots_adjust(bottom=0.30); plt.show()','')
setsrc(by[155],prep+'\ndef draw_district_variability(fig, ax):\n'+'\n'.join('    '+l for l in right.strip().splitlines())+
 '\n\nfig, ax = plt.subplots(figsize=(11, 5.5))\n'+left.strip()+'\nplt.tight_layout(); fig.subplots_adjust(bottom=0.30); save_supporting_figure("A12", fig)')

# Split existing coordinate bars from Lorenz curves.
s=text(by[167]);prep=s[:s.index('fig, axes =')]
draw=s[s.index('ax = axes[0]')+len('ax = axes[0]'):]
left,right=draw.split('ax = axes[1]',1)
right=right.replace('plt.tight_layout(); plt.show()','')
setsrc(by[167],prep+'\ndef draw_lorenz(fig, ax):\n'+'\n'.join('    '+l for l in right.strip().splitlines())+
 '\n\nfig, ax = plt.subplots(figsize=(11, 6))\n'+left.strip()+'\nplt.tight_layout(); save_supporting_figure("A13", fig)')

extra_support=[
 ('A11','Focal records by weekday','t5-seasonality','The busiest weekday has about 1.11 times the count of the quietest. Counts are not adjusted for weekday exposure, so this display does not establish a weekday effect.'),
 ('A12','Changing district contribution','t5-district-profile','These shares describe each district’s contribution to all known-district focal events over four weeks, rather than focal/political prevalence within a district. The changing mix adds geographic context to the main district overview.'),
 ('A13','Largest coordinates and recording precision','t5-concentration','The precision-1 proportion varies substantially across the largest recorded places, so the restriction removes incidents unevenly. These are counts at recorded coordinate pairs, often shared named places, rather than verified exact incident points.'),
]
for key,title,anchor,interp in extra_support:
 appendix.extend([md(f'<a id="appendix-{key.lower()}"></a>\n## {key} - {title}\n\nSource and method: [original analysis](#{anchor}).',f'appendix-{key}-heading'),code(f'show_supporting_figure("{key}")',f'appendix-{key}-figure'),md('**Interpretation.** '+interp,f'appendix-{key}-interpretation')])

combined={
99:('M8','Period rates and Hypothesis A','''fig = plt.figure(figsize=(15, 10), layout="constrained")
grid = fig.add_gridspec(2, 2, height_ratios=[1, 1.2])
draw_period_rates(fig, fig.add_subplot(grid[0, :]))
draw_period_shares(fig, [fig.add_subplot(grid[1, 0]), fig.add_subplot(grid[1, 1])])
fig.suptitle("Figure M8. Period comparison: rates, shares and within-type evidence", fontweight="bold")
plt.show()'''),
135:('M10','Weekly activity, unusual counts and focal share','''fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True, layout="constrained")
draw_weekly_anomalies(fig, axes[:2])
draw_weekly_share(fig, axes[2])
fig.suptitle("Figure M10. Weekly counts, anomaly screens and focal share", fontweight="bold")
plt.show()'''),
151:('M11','Calendar repetition and persistence','''fig = plt.figure(figsize=(15, 9), layout="constrained")
grid = fig.add_gridspec(2, 2)
draw_calendar_months(fig, fig.add_subplot(grid[0, :]))
acf_left = fig.add_subplot(grid[1, 0])
acf_right = fig.add_subplot(grid[1, 1], sharey=acf_left)
draw_persistence(fig, [acf_left, acf_right])
fig.suptitle("Figure M11. Calendar patterns and week-to-week persistence", fontweight="bold")
plt.show()'''),
155:('M12','District activity and variability','''fig = plt.figure(figsize=(15, 9), layout="constrained")
grid = fig.add_gridspec(2, 1, height_ratios=[1, 1.2])
draw_district_heatmap(fig, fig.add_subplot(grid[0]))
draw_district_variability(fig, fig.add_subplot(grid[1]))
fig.suptitle("Figure M12. District-week counts and typical volume versus variability", fontweight="bold")
plt.show()'''),
167:('M13','Spatial concentration and precision','''fig = plt.figure(figsize=(15, 11), layout="constrained")
grid = fig.add_gridspec(2, 2, height_ratios=[1.6, 1])
map_full = fig.add_subplot(grid[0, 0])
map_p1 = fig.add_subplot(grid[0, 1], sharex=map_full, sharey=map_full)
maps = [map_full, map_p1]
draw_spatial_maps(fig, maps)
draw_lorenz(fig, fig.add_subplot(grid[1, :]))
fig.suptitle("Figure M13. Land focal locations and precision sensitivity", fontweight="bold")
plt.show()'''),
}
after={}
for orig,(key,title,plotcode) in combined.items():
 after[by[orig]['id']]=[code(plotcode,'consolidated-'+key.lower())]

# Keep short source/reading notes beside computations; consolidated display
# explanations and one matching interpretation appear at the display itself.
setsrc(by[47],'''<a id="t2-period"></a>
## 2.1 Before and from October 7: counts, shares and rates

**Source:** political records from the event master. The table compares counts, focal shares and rates adjusted for the 644/725 observation days; the existing rate plot is combined with Hypothesis A in [Figure M8](#t4-period-figure).''')
setsrc(by[49],'''The period table shows a rise from 16.2% to 47.6% focal share and from 0.68 to 102.8 focal events per seven days. [Figure M8](#t4-period-figure) puts the rate and interval comparisons together, so this comparison is drawn once.''')
setsrc(by[98],'''<a id="t4-period-figure"></a>
### Figure M8 - Period rates, focal shares and within-type evidence

Top: the existing calendar-adjusted weekly rate plot (log axis). Bottom left: the overall focal shares with 95% Wilson intervals; bottom right: the same period comparison inside the two types containing focal records. All panels use the event master's political records; shares and rates have different denominators and units.''')
setsrc(by[100],'''**Interpretation.** Both the focal rate and share rise between periods, and the share increase also occurs within Explosions (13.1% to 49.4%), so the overall contrast is not solely a change in event-type mix. The earlier cohort is sparse and the intervals/tests assume independent records; reporting changes remain an unresolved explanation.''')
setsrc(by[68],'''<a id="t2-district-counts"></a>
## 2.7 District-week counts

**Source:** `acled_district_week.csv`. The table includes all 104 weeks, while the existing count heatmap masks the final partial week and is combined with district variability in [Figure M12](#t5-district-profile). Counts represent recorded volume; [Appendix A5](#appendix-a5) separately examines within-district focal/political shares.''')
setsrc(by[70],'''The largest district-week is Gaza City, November 4, 2023, with 102 focal records. Its timing and the shared early-2025 decline can be examined together with district variability in [Figure M12](#t5-district-profile).''')
setsrc(by[71],'''<a id="t2-weekly"></a>
## 2.8 Weekly counts and focal share

**Source:** `acled_gaza_week.csv`, with a pooled post-cutoff share from matching master records. The tables identify the five lowest focal-count weeks and quarterly weekly means; the share panel is combined with the existing anomaly-count timelines in [Figure M10](#t5-unusual-weeks). This retains one integrated weekly overview rather than separate repeated count timelines.''')
setsrc(by[73],'''The Gaza-wide peak is 254 focal events in the week starting October 28, 2023, and the five lowest focal-count weeks have 15-23 records. [Figure M10](#t5-unusual-weeks) shows why those low counts, focal share and unusual-week flags need to be read together.''')
setsrc(by[134],'''### Figure M10 - Unusual weekly counts and their focal share

**Source:** Gaza-week CSV; top two panels reuse the focal/political count plots with whole-period and prior-eight-week anomaly markers, while the bottom reuses the weekly focal-share panel. The bottom dashed line is the master-derived pooled post-cutoff share, the shaded interval marks the five lowest focal-count weeks, and hollow markers identify the partial week. Count flags and focal shares answer different questions even though they share a timeline.''')
setsrc(by[136],'''**Interpretation.** The trailing count rule flags several rises following the early-2025 trough, while the focal share can remain high during low-count weeks because its political denominator also falls. These are screening leads sensitive to recent history, not explanations of the dip or verified anomalies.

**Share-screening check.** The whole-period share rule flags no weeks and the trailing share rule flags 11; these are separate from the count flags shown above. Flat share-history windows remain unscored.''')
setsrc(by[147],'''<a id="t5-seasonality"></a>
### Calendar comparison inputs

**Sources:** Gaza complete-week means by start-month/year and post-cutoff master focal records by weekday. The monthly comparison appears with autocorrelation in [Figure M11](#t5-persistence); the existing weekday plot is in [Appendix A11](#appendix-a11). The weekday counts include the final partial-week dates and are not exposure-adjusted rates.''')
setsrc(by[149],'''The nine shared calendar months of 2024 and 2025 have rank correlation -0.30; that comparison is displayed with persistence in [Figure M11](#t5-persistence). Weekday counts vary by about 1.11 from highest to lowest and are shown separately in [Appendix A11](#appendix-a11).''')
setsrc(by[150],'''<a id="t5-persistence"></a>
### Figure M11 - Calendar patterns versus persistence

Top: the existing cross-year monthly comparison from complete Gaza weeks. Bottom: autocorrelation of focal counts and their week-to-week changes, using the same complete-week series; autocorrelation compares a sequence with itself at earlier lags. The shaded bands are approximate no-autocorrelation references, not tests of seasonal absence.''')
setsrc(by[152],'''**Interpretation.** Calendar-month means do not align across the two observed years, while neighboring weekly counts are strongly related (lag-1 autocorrelation 0.76), unlike most week-to-week changes. The short window does not rule out seasonality, and level shifts can create persistence without proving forecasting skill.''')
setsrc(by[154],'''<a id="t5-district-profile"></a>
### Figure M12 - District counts, typical volume and variability

Top: the existing district-week focal-count heatmap, with the partial week greyed out and excluded from its color scale. Bottom: the existing median-count versus coefficient-of-variation plot, using complete weeks only; the coefficient is SD/mean and bubble area indicates the complete-week total. The district contribution timeline, whose denominator is all districts' focal events, is in [Appendix A12](#appendix-a12); within-district focal/political shares are in [Appendix A5](#appendix-a5).''')
setsrc(by[156],'''**Interpretation.** Gaza City has the largest observed district-week peak and contributes 3,411 complete-week focal records (32.3% of the known-district complete-week total), while North Gaza has the highest relative variability (0.83). The common early-2025 trough and different district volumes support local baselines, with partial-week and complete-week scopes kept distinct.''')
setsrc(by[163],'''<a id="t5-spatial-map"></a>
### Spatial-map inputs

**Source:** the land focal-incident CSV, full and precision-1 subsets. The existing maps are combined with the concentration curves in [Figure M13](#t5-concentration); they use common extent, bubble scaling and color normalization, without a basemap or inferred boundaries.''')
setsrc(by[165],'''The spatial tables record 10,583 incidents on 101 coordinate pairs, versus 7,576 on 95 pairs under precision 1. [Figure M13](#t5-concentration) combines the geographic and concentration views, while [Appendix A13](#appendix-a13) preserves the top-coordinate precision bars.''')
setsrc(by[166],'''<a id="t5-concentration"></a>
### Figure M13 - Spatial concentration and precision sensitivity

Top: the existing full and precision-1 land focal maps, with identical coordinate scales and color/size definitions. Bottom: the existing Lorenz curves, accumulating incidents from least to most populated coordinates; the diagonal represents equal counts and Gini summarizes inequality. Each subset uses its own occupied-coordinate set, so this compares selected populations rather than a fixed set of locations; [Appendix A13](#appendix-a13) shows precision composition at the largest coordinates.''')
setsrc(by[168],'''**Interpretation.** The broad spatial shape persists after precision filtering, but the top-ten share rises from 33.8% to 38.1% and Gini from 0.57 to 0.60 while about 28% of incidents are excluded. Concentration therefore depends on which records and places remain, and shared named-place coordinates do not identify exact incident points.''')

# Unchanged standalone main figures, now with one sequential main-report ID.
renumber={'U1':'M1','U2':'M2','U4':'M3','B3':'M4','B4':'M5','B5':'M6','B10':'M7','H1':'M8','H2':'M9','P4':'M10','P7':'M11','P8':'M12','P10':'M13','P11':'M13','P12':'M14',
          'U3':'A1','U5':'A2','B2':'A3','B6':'A4','B9':'A5','P1':'A6','P2':'A7','P3':'A8','P5':'A9','P9':'A10','P6':'M11','B1':'M8','B7':'M12','B8':'M10'}
for c in cells+appendix:
 s=text(c)
 if c['cell_type']=='markdown':
  s=re.sub(r'\b(?:U[1-5]|B(?:10|[1-9])|H[12]|P(?:1[0-2]|[1-9]))\b',lambda m:renumber[m.group()],s)
  setsrc(c,s)
 elif c['cell_type']=='code':
  for old,new in renumber.items():s=s.replace('Figure '+old+'.','Figure '+new+'.')
  setsrc(c,s)

# Make the definition explicit where readers first encounter the distinction.
c=by[3];s=text(c);needle='**Focal share** is'
s=s.replace(needle,'**Non-focal** means a record does not meet both focal conditions. In focal-versus-non-focal comparisons, we first restrict to political-violence records, so non-focal means the other political records in that comparison group; it does not mean civilians were unharmed.\n\n'+needle)
setsrc(c,s)

main_register=[('M1','Fatality distributions','t1-fatalities'),('M2','Event/sub-event composition','t1-types'),('M3','Recording precision','t1-precision'),('M4','Fatality occurrence and conditional totals','t2-severity'),('M5','Precision and focal prevalence','t2-precision'),('M6','Actor/sub-event combinations','t2-actor-types'),('M7','Weekly correlation and categorical association','t2-association'),('M8','Period rates, shares and Hypothesis A','t4-period-figure'),('M9','Event types and Hypothesis B','t4-type-test'),('M10','Weekly counts, anomaly markers and focal share','t5-unusual-weeks'),('M11','Calendar patterns and persistence','t5-persistence'),('M12','District counts and variability','t5-district-profile'),('M13','Spatial maps and concentration','t5-concentration'),('M14','Spatial-setting sensitivity','t5-dbscan')]
setsrc(by[83],'''| Main figure | Content |\n|---|---|\n'''+ '\n'.join(f'| {a} | [{b}](#{c}) |' for a,b,c in main_register)+'''\n\nThe main report has **14 figure groups**. Related existing plots share panels; **13 supporting figures** remain in the [appendix](#supporting-figures), including actor marginals, all-event totals, additional severity/share plots, minority counts, high-fatality review, monthly/weekday summaries, K-means and coordinate precision bars. Source tables remain beside their calculations; no new statistical analysis is introduced by the layout.''')
setsrc(by[82],'''<a id="task-3"></a>
# Task 3 - Main figure register

The main figures follow the sequence from data description to comparisons, tests, temporal patterns and spatial sensitivity. Supporting figures are linked where relevant and collected after the closing discussion, before References.''')

# Update BQ evidence to point directly to composite figures or appendix graphics.
for orig in [178,179,180,181,182,184]:
 c=by[orig];s=text(c)
 s=s.replace('[Task 1, Figure A1 and actor tables](#t1-actors)','[actor tables](#t1-actors) and [Appendix A1](#appendix-a1)')
 s=s.replace('[Figure M13](#t5-spatial-map)','[Figure M13, map panels](#t5-concentration)')
 s=s.replace('[Figure M12 and district tables](#t2-district-counts)','[district tables](#t2-district-counts) and [Figure M12](#t5-district-profile)')
 s=s.replace('[Figure M10](#t2-weekly)','[Figure M10](#t5-unusual-weeks)')
 s=s.replace('[Task 2, Figure M8 and period table](#t2-period)','[period table](#t2-period) and [Figure M8](#t4-period-figure)')
 setsrc(c,s)

result=[]
for c in cells:
 if c.get('id')=='p3-references':
  result.append(md('''<a id="supporting-figures"></a>
# Appendix - Supporting figures

These existing plots provide optional detail for the main report. They retain their original populations, calculations and plot types; the source links return to the accompanying calculations and tables. [Return to the main figure register](#task-3).''','supporting-figure-intro'))
  result.extend(appendix)
 result.append(c)
 result.extend(after.get(c['id'],[]))
for c in result:
 if c['cell_type']=='code':c['outputs']=[];c['execution_count']=None
 if isinstance(c['source'],str):c['source']=c['source'].splitlines(keepends=True)
n['cells']=result
(P/'consolidation.candidate.ipynb').write_text(json.dumps(n,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
(P/'plot_consolidation_map.json').write_text(json.dumps({'main_figures':main_register,'supporting_figures':support_specs,'additional_supporting':extra_support,'policy':'Existing plots and data only; subplot drawing functions reuse original drawing code. Supporting figures are rendered at their original computation point and displayed in the appendix to preserve variable state.'},indent=2))
print('Built consolidation candidate',len(result),'cells; 14 main + 13 supporting figures')
