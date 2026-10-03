import json,subprocess,sys,tempfile
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
import pytest,z3
from hypothesis import given,settings,strategies as st
from roundguard.model import parse,load_rule,Variable,Rule
from roundguard.semantics import quantize,symbolic,to_fraction,evaluate,tick_env
from roundguard.analysis import periods,analyze,dp_batch,cyclic_batch,NotCertified
from roundguard.oracle import exhaustive,execute,dec,precision
ROOT=Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('mode',['HALF_EVEN','HALF_UP','FLOOR','CEILING','DOWN','UP'])
@settings(max_examples=120,derandomize=True,deadline=None)
@given(n=st.integers(-500,500),d=st.sampled_from([1,2,4,5,10,20,100]))
def test_rounding_decimal_and_symbolic(mode,n,d):
 x=F(n,d); e=parse(f'Q(rat({n},{d}),1,"{mode}")',set())
 with localcontext() as ctx:
  ctx.prec=80
  expected=F((Decimal(n)/Decimal(d)).quantize(Decimal(1),rounding='ROUND_'+mode))
 assert quantize(x,1,mode)==expected==to_fraction(symbolic(e,{}))

@settings(max_examples=120,derandomize=True,deadline=None)
@given(x=st.integers(-100000,100000),r=st.sampled_from([2,4,5,10]),mode=st.sampled_from(['FLOOR','CEILING','HALF_EVEN']))
def test_structural_translation(x,r,mode):
 e=parse(f'Q(Q(x/{r},1,"{mode}")*rat(3,2),1,"{mode}")',{'x'})
 rule=Rule('translation',[Variable('x',-200000,200000)],{'a':e,'b':e},{})
 T=periods(rule)['x']; delta=F(3,2*r)*T
 assert evaluate(e,{'x':x+T})==evaluate(e,{'x':x})+delta

def test_half_even_parity_regression():
 assert quantize(F(1,2),1,'HALF_EVEN')==0
 assert quantize(F(3,2),1,'HALF_EVEN')==2
 e=parse('Q(x/2,1,"HALF_EVEN")',{'x'})
 assert periods(Rule('p',[Variable('x',0,10)],{'a':e,'b':e},{}))['x']==4

@pytest.mark.parametrize('mode',['HALF_UP','DOWN','UP'])
def test_signed_modes_reject_period(mode):
 e=parse(f'Q(x/2,1,"{mode}")',{'x'})
 with pytest.raises(NotCertified): periods(Rule('p',[Variable('x',-100,100)],{'a':e,'b':e},{}))

@settings(max_examples=50,derandomize=True,deadline=None)
@given(lo=st.integers(-20,5),length=st.integers(1,12),mode=st.sampled_from(['HALF_EVEN','FLOOR','CEILING']),r1=st.sampled_from([2,4,5]),r2=st.sampled_from([2,4,5]))
def test_dp_against_independent_exhaustive(lo,length,mode,r1,r2):
 with tempfile.TemporaryDirectory() as t:
  p=Path(t)/'r.json';p.write_text(json.dumps(dict(name='dp',variables={'x':dict(min=lo,max=lo+length),'y':dict(min=lo-1,max=lo+length-1)},batch=dict(lines=[f'x/{r1}+rate("0.1")',f'y/{r2}-rate("0.2")'],mode=mode))))
  rule=load_rule(p);d=dp_batch(rule);o=exhaustive(rule)
  assert d['maximum_discrepancy']==o['maximum_discrepancy']

def test_dp_independence_and_denominator_budget(tmp_path):
 rule=load_rule(ROOT/'benchmarks'/'canonical'/'payroll_deduction.json')
 with pytest.raises(NotCertified): dp_batch(rule)
 p=tmp_path/'prime.json'
 data=dict(variables={'x':dict(min=0,max=100)},batch=dict(lines=['x*rat(1,1009)'],mode='HALF_EVEN'))
 p.write_text(json.dumps(data));rule=load_rule(p)
 with pytest.raises(NotCertified,match='denominator'): cyclic_batch(rule)
 assert dp_batch(rule)['local_representatives']==101
 data['variables']['x']['max']=3000;p.write_text(json.dumps(data))
 with pytest.raises(NotCertified,match='Local representative'): dp_batch(load_rule(p))

@pytest.mark.parametrize('p',sorted((ROOT/'benchmarks'/'synthetic').glob('*.json'))+sorted((ROOT/'benchmarks'/'canonical').glob('*.json'))+sorted((ROOT/'benchmarks'/'realistic').glob('*.json')))
def test_benchmark_oracle_and_replay(p):
 r=load_rule(p);o=exhaustive(r);a=analyze(r,timeout_ms=30000)
 assert a['complete'];assert a['status']==o['status'];assert a['maximum_discrepancy']==o['maximum_discrepancy']
 if a.get('counterexample'):
  ticks=a['counterexample'];assert all(v.lo<=ticks[v.name]<=v.hi for v in r.variables)
  vals=[evaluate(e,tick_env(r,ticks)) for e in r.variants.values()]
  assert max(vals)-min(vals)==F(a['maximum_discrepancy'])

def test_parser_rejects_execution_and_nonlinearity():
 for text in ['__import__("os").system("echo bad")','x*x','x/0','Q(x,0,"FLOOR")','0.1*x']:
  with pytest.raises(ValueError): parse(text,{'x'})

def test_cli_json():
 p=ROOT/'benchmarks'/'canonical'/'tax_per_line.json'
 out=subprocess.check_output([sys.executable,'-m','roundguard.cli','analyze',str(p),'--json'],text=True)
 result=json.loads(out); assert result['status']=='SENSITIVE' and result['maximum_discrepancy']=='1'

@pytest.mark.parametrize('mode',['HALF_UP','DOWN','UP'])
def test_nonnegative_dp_signed_mode_extension(mode):
 with tempfile.TemporaryDirectory() as t:
  p=Path(t)/'r.json';p.write_text(json.dumps(dict(variables={'x':dict(min=1,max=17),'y':dict(min=1,max=17)},batch=dict(lines=['x/4','y/2'],mode=mode))))
  r=load_rule(p); assert dp_batch(r)['maximum_discrepancy']==exhaustive(r)['maximum_discrepancy']
  p.write_text(json.dumps(dict(variables={'x':dict(min=-1,max=17)},batch=dict(lines=['x/2'],mode=mode))))
  with pytest.raises(NotCertified): dp_batch(load_rule(p))

def test_json_float_quantum_rejected():
 with tempfile.TemporaryDirectory() as t:
  p=Path(t)/'r.json';p.write_text(json.dumps(dict(variables={'x':dict(min=10,max=10,quantum=0.1)},variants={'a':'Q(x,1,"CEILING")','b':'1'})))
  with pytest.raises(ValueError,match='JSON floats'): load_rule(p)
  p.write_text(json.dumps(dict(variables={'x':dict(min=10,max=10,quantum='0.1')},variants={'a':'Q(x,1,"CEILING")','b':'1'})))
  assert analyze(load_rule(p))['status']=='SAFE'

def test_decimal_oracle_large_terminating_denominator_is_exact():
 tiny=F(1,2**1000)
 r=Rule('oracle_precision',[Variable('x',0,0)],{'tiny':parse(f'rat(1,{2**1000})',{'x'}),'zero':parse('0',{'x'})},{})
 with localcontext() as ctx:
  ctx.prec=8
  assert F(dec(tiny))==tiny  # Exact conversion does not use the current context.
 assert F(exhaustive(r)['maximum_discrepancy'])==tiny

def test_decimal_oracle_rejects_inexact_arithmetic_but_allows_quantizing():
 e=parse('rat(1,1099511627776)+1',set())  # 1 + 2**-40 needs many digits.
 with localcontext() as ctx:
  ctx.prec=8
  with pytest.raises(ValueError,match='not exact'):
   execute(e,{})
 e=parse('Q(rat(1,2),1,"HALF_EVEN")',set())
 assert execute(e,{})==0
 e=parse('Q(1,3,"HALF_EVEN")',set())
 with pytest.raises(ValueError,match='nonterminating'):
  execute(e,{})

def test_decimal_oracle_nonunit_quantum_inverse_budget():
 q=2**1000
 e=parse(f'Q(1,{q},"CEILING")',{'x'})
 r=Rule('large_quantum',[Variable('x',0,0)],{'rounded':e,'zero':parse('0',{'x'})},{})
 assert F(exhaustive(r)['maximum_discrepancy'])==q
