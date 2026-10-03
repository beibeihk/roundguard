"""Executable consistency audit. This is not a proof or a new literature search."""
import csv,hashlib,json,re
from pathlib import Path
from fractions import Fraction as F
from roundguard.model import load_rule
from roundguard.oracle import execute,dec,precision
from decimal import localcontext
ROOT=Path(__file__).resolve().parents[1]
def main():
 truth=json.loads((ROOT/'results/ground_truth.json').read_text())
 diagnostics=json.loads((ROOT/'results/diagnostics.json').read_text())
 expected={load_rule(ROOT/r['file']).name:r for r in truth}
 assert len(expected)==66
 for r in diagnostics:
  if r['method'] in {'auto','pure_smt'}:
   assert r['result']['complete']
   assert r['result']['status']==expected[r['case']]['status']
   assert r['result']['maximum_discrepancy']==expected[r['case']]['maximum_discrepancy']
 certs=json.loads((ROOT/'results/scaling_ground_truth.json').read_text());assert len(certs)==24
 for c in certs:
  rule=load_rule(ROOT/'benchmarks/scaling'/f'{c["case"]}.json');ticks=c['counterexample']
  assert set(ticks)=={v.name for v in rule.variables}
  assert all(type(ticks[v.name]) is int and v.lo<=ticks[v.name]<=v.hi for v in rule.variables)
  with localcontext() as ctx:
   ctx.prec=precision(rule);env={v.name:dec(ticks[v.name]*v.quantum) for v in rule.variables}
   values=[execute(e,env) for e in rule.variants.values()]
  assert F(max(values)-min(values))==F(c['integral_upper_bound'])==F(c['ground_truth'])
 text='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'paper').glob('*.tex'))
 cited=set(k.strip() for group in re.findall(r'\\cite\w*\{([^}]+)\}',text) for k in group.split(','))
 bib=(ROOT/'paper/references.bib').read_text(encoding='utf-8');keys=set(re.findall(r'@\w+\s*\{\s*([^,]+)',bib))
 assert cited<=keys,(cited-keys)
 audit={r['citation_key']:r for r in csv.DictReader((ROOT/'literature/reference_audit.csv').open(encoding='utf-8-sig'))}
 assert all(audit[k]['verified'].lower()=='true' and audit[k]['claim_supported'].lower()=='true' for k in cited)
 rows=list(csv.DictReader((ROOT/'results/scaling.csv').open()))
 assert len(rows)==216
 for r in rows:
  if r['complete']=='True': assert F(r['maximum_discrepancy'])==F(next(c['ground_truth'] for c in certs if c['case']==r['case']))
 report=dict(status='CONSISTENCY_AUDIT_PASSED',small_programs=len(expected),small_exact_checks=132,scaling_certificates=len(certs),scaling_runs=len(rows),cited_sources=len(cited),scope='saved artifact consistency; not independent literature completeness, formal verification, or production validation')
 report['evidence_sha256']={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'results/ground_truth.json',ROOT/'results/scaling_ground_truth.json',ROOT/'results/scaling.csv',ROOT/'paper/main.tex',ROOT/'paper/evaluation.tex',ROOT/'paper/references.bib']}
 (ROOT/'results/integrity_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps(report,indent=2))
if __name__=='__main__': main()
