import csv,json,statistics
from pathlib import Path
from fractions import Fraction as F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from roundguard.model import load_rule,walk
ROOT=Path(__file__).resolve().parents[1]
def main():
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'ps.fonttype':42})
 rows=list(csv.DictReader((ROOT/'results'/'scaling.csv').open(encoding='utf-8')))
 fig,axes=plt.subplots(1,2,figsize=(7.4,2.8))
 for m,label in [('dp','Parity extrema'),('cyclic','Cyclic residue DP'),('residue','SMT, reduced grid'),('smt','SMT, full grid')]:
  xs=[];ys=[];failx=[];faily=[]
  for n in [2,4,8,16,32,64]:
   a=[r for r in rows if r['method']==m and int(r['nvars'])==n and int(r['upper'])==1000000000]
   xs.append(n);ys.append(statistics.median(float(r['time_seconds']) for r in a))
   if not all(r['complete']=='True' for r in a): failx.append(n);faily.append(ys[-1])
  axes[0].plot(xs,ys,marker='o',label=label);axes[0].scatter(failx,faily,marker='x',s=80,color='black',zorder=5)
 axes[0].set(xscale='log',yscale='log',xlabel='Number of independent lines',ylabel='Median wall time (s)');axes[0].legend(fontsize=7)
 for n in [2,16,64]:
  xs=[];ys=[]
  for u in [3,20,10000,1000000000]:
   a=[r for r in rows if r['method']=='dp' and int(r['nvars'])==n and int(r['upper'])==u]
   xs.append(u);ys.append(statistics.median(float(r['time_seconds']) for r in a))
  axes[1].plot(xs,ys,marker='s',label=f'{n} lines')
 axes[1].set(xscale='log',yscale='log',xlabel='Upper bound (integer input ticks)',ylabel='Parity-extrema wall time (s)');axes[1].legend(fontsize=7)
 fig.tight_layout();(ROOT/'figures').mkdir(exist_ok=True);fig.savefig(ROOT/'figures'/'scalability.pdf');fig.savefig(ROOT/'figures'/'scalability.png',dpi=180);plt.close(fig)
 summary=json.loads((ROOT/'results'/'summary.json').read_text())
 lines=['\\begin{tabular}{lrrrrr}','\\toprule','Method & Cases & FP & Missed & Unknown & Median ms \\\\','\\midrule']
 names={'auto':'RoundGuard','pure_smt':'Full-grid SMT','random32':'Random (32)','hypothesis64':'Hypothesis (64)','naive_interval':'Independent intervals'}
 for m,r in summary.items(): lines.append(f'{names[m]} & {r["cases"]} & {r["false_positives"]} & {r["false_negatives"]} & {r["unknown"]} & {1000*r["median_seconds"]:.2f} \\\\')
 lines+=['\\bottomrule','\\end{tabular}'];(ROOT/'paper'/'accuracy_table.tex').write_text('\n'.join(lines),encoding='utf-8')
 # Case results and bounds are derived from saved exact diagnostics.
 ds=json.loads((ROOT/'results'/'diagnostics.json').read_text());case_rows=[r for r in ds if r['method']=='auto' and r['case'] in ['hmrc_invoice','irs_payroll','ssa_benefit','cash_settlement','rational_money','ssa_entitlement']]
 lines=['\\begin{tabular}{lrl}','\\toprule','Fragment & Maximum (cents) & Method \\\\','\\midrule']
 for r in case_rows: lines.append(r['case'].replace('_','\\_')+' & '+r['result']['maximum_discrepancy']+' & '+r['result']['method']+' \\\\')
 lines+=['\\bottomrule','\\end{tabular}'];(ROOT/'paper'/'cases_table.tex').write_text('\n'.join(lines),encoding='utf-8')
 denominator_rows=list(csv.DictReader((ROOT/'results/denominators.csv').open(encoding='utf-8')))
 facts=dict(summary=summary,scaling_runs=len(rows),scaling_complete={m:sum(r['complete']=='True' for r in rows if r['method']==m) for m in ['dp','cyclic','residue','smt']},denominator_runs=len(denominator_rows),denominator_complete={m:sum(r['complete']=='True' for r in denominator_rows if r['method']==m) for m in ['dp','cyclic','residue','smt']})
 profile=[]
 def depth(e): return 1+max((depth(a) for a in e.args if hasattr(a,'op')),default=0)
 for group in ['synthetic','canonical','realistic']:
  for p in sorted((ROOT/'benchmarks'/group).glob('*.json')):
   rule=load_rule(p)
   profile.append(dict(case=rule.name,group=group,nvars=len(rule.variables),nodes=sum(sum(1 for _ in walk(e)) for e in rule.variants.values()),depth=max(depth(e) for e in rule.variants.values()),policies=len(rule.variants),domain_size=rule.size))
 with (ROOT/'results'/'benchmark_profile.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(profile[0]));w.writeheader();w.writerows(profile)
 dpmed=[statistics.median(float(r['time_seconds']) for r in rows if r['case']==c and r['method']=='dp') for c in {r['case'] for r in rows}]
 macros=dict(DPCompleted=facts['scaling_complete']['dp'],CyclicCompleted=facts['scaling_complete']['cyclic'],ResidueCompleted=facts['scaling_complete']['residue'],SMTCompleted=facts['scaling_complete']['smt'],AutoMedian=f'{1000*summary["auto"]["median_seconds"]:.2f}',SMTMedian=f'{1000*summary["pure_smt"]["median_seconds"]:.2f}',DPMaxMedian=f'{1000*max(dpmed):.2f}')
 for label,field in [('SmallNodes','nodes'),('SmallDepth','depth'),('SmallVars','nvars')]:
  macros[label+'Min']=min(p[field] for p in profile);macros[label+'Max']=max(p[field] for p in profile)
 for m,label in [('dp','DP'),('cyclic','Cyclic'),('residue','Residue'),('smt','SMT')]:
  for status,name in [('UNKNOWN','Unknown'),('SENSITIVE','Partial')]:
   macros[label+name]=sum(r['method']==m and r['status']==status and r['complete']!='True' for r in rows)
  for n in [2,4,8,16,32,64]:
   a=[float(r['time_seconds']) for r in rows if r['method']==m and int(r['nvars'])==n and int(r['upper'])==1000000000]
   names={2:'Two',4:'Four',8:'Eight',16:'Sixteen',32:'ThirtyTwo',64:'SixtyFour'}
   macros[label+names[n]+'Median']=f'{1000*statistics.median(a):.2f}'
 macros.update({label:facts['denominator_complete'][m] for m,label in [('dp','DenomDPCompleted'),('cyclic','DenomCyclicCompleted'),('residue','DenomResidueCompleted'),('smt','DenomSMTCompleted')]})
 denominator_lines=['\\begin{tabular}{llrrrrr}','\\toprule','Family & Lines & Bits($B$) & Reps & DP ms & Reduced & Full \\\\','\\midrule']
 for case in sorted({r['case'] for r in denominator_rows}):
  a=[r for r in denominator_rows if r['case']==case];d=next(r for r in a if r['method']=='dp')
  family='Narrow' if case.startswith('narrow') else ('Wide' if int(d['upper'])>20 else 'Short')
  median=1000*statistics.median(float(r['time_seconds']) for r in a if r['method']=='dp')
  reduced=sum(r['method']=='residue' and r['complete']=='True' for r in a);full=sum(r['method']=='smt' and r['complete']=='True' for r in a)
  denominator_lines.append(f'{family} & {d["nvars"]} & {int(d["common_denominator"]).bit_length()} & {d["local_representatives"]} & {median:.2f} & {reduced}/3 & {full}/3 \\\\')
 denominator_lines+=['\\bottomrule','\\end{tabular}']
 (ROOT/'paper/denominator_table.tex').write_text('\n'.join(denominator_lines),encoding='utf-8')
 (ROOT/'paper'/'result_macros.tex').write_text('\n'.join('\\newcommand{\\'+k+'}{'+str(v)+'}' for k,v in macros.items()),encoding='utf-8')
 facts['macros']=macros
 (ROOT/'results'/'paper_facts.json').write_text(json.dumps(facts,indent=2),encoding='utf-8')
if __name__=='__main__': main()
