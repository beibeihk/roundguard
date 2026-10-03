"""Every table cell is derived from saved executions, never hand entered."""
import csv,json,platform,random,statistics,sys,time
from pathlib import Path
from fractions import Fraction as F
from decimal import localcontext
from itertools import combinations
from hypothesis import find,settings,strategies as st
from hypothesis.errors import NoSuchExample
from roundguard.model import load_rule,walk
from roundguard.analysis import analyze,interval,error_bound,affine,NotCertified
from roundguard.oracle import exhaustive,execute,dec,precision
ROOT=Path(__file__).resolve().parents[1]
SEED=20261003
def testing(rule,kind):
 def difference(xs):
  with localcontext() as ctx:
   ctx.prec=precision(rule)
   env={v.name:dec(x*v.quantum) for v,x in zip(rule.variables,xs)}
   vals=[execute(e,env) for e in rule.variants.values()]
   return max(vals)!=min(vals)
 start=time.perf_counter(); witness=None
 if kind=='random32':
  rng=random.Random(SEED)
  for _ in range(32):
   xs=tuple(rng.randint(v.lo,v.hi) for v in rule.variables)
   if difference(xs): witness=xs;break
 else:
  domain=st.tuples(*(st.integers(v.lo,v.hi) for v in rule.variables))
  try: witness=find(domain,difference,settings=settings(max_examples=64,derandomize=True,database=None,deadline=None))
  except NoSuchExample: pass
 return dict(status='SENSITIVE' if witness is not None else 'NO_WITNESS',counterexample=dict(zip((v.name for v in rule.variables),witness)) if witness else None,time_seconds=time.perf_counter()-start,complete=False)

def naive(rule):
 start=time.perf_counter()
 vals=[interval(e,rule.variables) for e in rule.variants.values()]
 ub=max(max(a[1]-b[0],b[1]-a[0]) for a,b in combinations(vals,2))
 return dict(status='SAFE' if ub==0 else 'WARNING',upper_bound=str(ub),time_seconds=time.perf_counter()-start)

def savecsv(path,rows):
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
 out=ROOT/'results';out.mkdir(exist_ok=True)
 files=sum((sorted((ROOT/'benchmarks'/g).glob('*.json')) for g in ['synthetic','canonical','realistic']),[])
 accuracy=[];raw=[];ground=[]
 for i,p in enumerate(files):
  r=load_rule(p);start=time.perf_counter();oracle=exhaustive(r);ot=time.perf_counter()-start
  ground.append(dict(file=str(p.relative_to(ROOT)).replace('\\','/'),**oracle,oracle='independent Decimal exhaustive',seed=SEED))
  methods={'auto':analyze(r), 'pure_smt':analyze(r,'smt'), 'random32':testing(r,'random32'), 'hypothesis64':testing(r,'hypothesis64'), 'naive_interval':naive(r)}
  for m,res in methods.items():
   if m in ['auto','pure_smt'] and res.get('complete'):
    if res['maximum_discrepancy']!=oracle['maximum_discrepancy']: raise RuntimeError(f'Incorrect {m} result: {r.name}')
   expected=oracle['status']=='SENSITIVE';detected=res['status'] in {'SENSITIVE','WARNING'}
   accuracy.append(dict(case=r.name,group=r.metadata['group'],pattern=r.metadata.get('pattern','rule fragment'),method=m,truth=oracle['status'],reported=res['status'],fp=int(detected and not expected),fn=int(expected and not detected),unknown=int(res['status']=='UNKNOWN'),complete=res.get('complete',False),time_seconds=res.get('time_seconds',0),domain_size=r.size,nvars=len(r.variables),nodes=sum(sum(1 for _ in walk(e)) for e in r.variants.values()),oracle_seconds=ot))
   raw.append(dict(case=r.name,method=m,result=res))
  print(f'oracle/effectiveness {i+1}/{len(files)}: {r.name}',flush=True)
 (out/'ground_truth.json').write_text(json.dumps(ground,indent=2),encoding='utf-8')
 (out/'diagnostics.json').write_text(json.dumps(raw,indent=2),encoding='utf-8');savecsv(out/'accuracy.csv',accuracy)
 scaling=[]; scaling_truth=[]
 for i,p in enumerate(sorted((ROOT/'benchmarks'/'scaling').glob('*.json'))):
  r=load_rule(p);auto=analyze(r,'dp');
  # The universal sharp HE bound need not be attainable on heterogeneous grids.
  from roundguard.semantics import quantize,evaluate,tick_env
  universal=quantize(F(len(r.variables),2),1,'HALF_EVEN')
  # Independent small local Decimal tables yield an error envelope. The
  # hard-coded 20-tick coverage is specific to the declared benchmark rates
  # 1/2, 1/4, 1/5, 1/10, whose even-translation periods are 4, 8, 10, 20.
  # Each individual period is at most 20; they need not divide 20.
  from roundguard.model import parse
  from roundguard.oracle import execute
  emin=F(0);emax=F(0)
  for idx,line in enumerate(r.batch['lines']):
   name=f'x{idx}';e=parse(line,{name});qe=parse(f'Q({line},1,"HALF_EVEN")',{name})
   errors=[]
   with localcontext() as ctx:
    ctx.prec=precision(r)
    for x in range(min(r.variables[idx].hi,19)+1):
     env={name:dec(x)};errors.append(F(execute(qe,env)-execute(e,env)))
   emin+=min(errors);emax+=max(errors)
  envelope=max(-emin,emax)+F(1,2)
  integral_upper=envelope.numerator//envelope.denominator
  assert integral_upper==F(auto['maximum_discrepancy'])
  ticks=auto['counterexample']
  assert set(ticks)=={v.name for v in r.variables}
  assert all(type(ticks[v.name]) is int and v.lo<=ticks[v.name]<=v.hi for v in r.variables)
  with localcontext() as ctx:
   ctx.prec=precision(r); env={v.name:dec(ticks[v.name]*v.quantum) for v in r.variables}
   replay=[execute(e,env) for e in r.variants.values()];attained=F(max(replay)-min(replay))
  assert attained==integral_upper
  scaling_truth.append(dict(case=r.name,ground_truth=str(attained),oracle='Independent Decimal local-error envelope + integral upper bound + attaining Decimal replay',local_lower=str(emin),local_upper=str(emax),integral_upper_bound=str(integral_upper),counterexample=ticks))
  # Three timing repetitions of every actual method; timeout is per solver call,
  # not a total wall-clock budget. Complete and incomplete runs stay separate.
  for m in ['dp','residue','smt']:
   for rep in range(3):
    res=analyze(r,m,timeout_ms=1500)
    if res.get('complete') and res['maximum_discrepancy']!=auto['maximum_discrepancy']: raise RuntimeError('Scaling disagreement')
    scaling.append(dict(case=r.name,method=m,repetition=rep,nvars=len(r.variables),upper=r.variables[0].hi,domain_size=str(r.size),time_seconds=res['time_seconds'],status=res['status'],complete=res.get('complete',False),maximum_discrepancy=res.get('maximum_discrepancy'),dp_truth=auto['maximum_discrepancy'],lower_bound=res.get('lower_bound'),residue_states=auto['residue_states'],transitions=auto['transitions'],universal_bound=str(universal),bound_gap=str(universal-F(auto['maximum_discrepancy']))))
   print(f'scale {i+1}/24 {r.name} {m}: {res["status"]} complete={res.get("complete")}',flush=True)
  savecsv(out/'scaling.csv',scaling)
 (out/'scaling_ground_truth.json').write_text(json.dumps(scaling_truth,indent=2),encoding='utf-8')
 summary={}
 for m in ['auto','pure_smt','random32','hypothesis64','naive_interval']:
  a=[r for r in accuracy if r['method']==m];sens=sum(r['truth']=='SENSITIVE' for r in a)
  summary[m]=dict(cases=len(a),sensitive=sens,safe=len(a)-sens,false_positives=sum(r['fp'] for r in a),false_negatives=sum(r['fn'] for r in a),unknown=sum(r['unknown'] for r in a),median_seconds=statistics.median(r['time_seconds'] for r in a))
 (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
 import importlib.metadata as md,z3
 env=dict(seed=SEED,python=sys.version,platform=platform.platform(),processor=platform.processor(),packages={n:md.version(n) for n in ['roundguard','z3-solver','pytest','hypothesis','matplotlib','numpy']},z3=z3.get_version_string(),repetitions=3,solver_timeout_ms_per_call=1500)
 (out/'environment.json').write_text(json.dumps(env,indent=2),encoding='utf-8')
 print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__': main()
