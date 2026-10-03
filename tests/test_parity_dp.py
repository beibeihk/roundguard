"""Independent Fraction enumeration of signed endpoint and witness contracts."""
from fractions import Fraction as F
from itertools import product
from math import floor,ceil
import json,subprocess,sys

import pytest
from hypothesis import given,settings,strategies as st
from roundguard.model import Rule,Variable,Node,parse,add_nodes,load_rule
from roundguard.analysis import dp_batch,cyclic_batch,analyze,NotCertified

def rounded(x,mode):
    """Distance-based reference; does not call any analyzer quantizer."""
    lower,upper=floor(x),ceil(x)
    if mode=='FLOOR': return lower
    if mode=='CEILING': return upper
    if mode=='DOWN': return int(x)
    if mode=='UP': return lower if x<0 else upper
    down,up=x-lower,upper-x
    if down<up: return lower
    if up<down: return upper
    if mode=='HALF_EVEN': return lower if lower%2==0 else upper
    return lower if x<0 else upper

def batch(forms,mode='HALF_EVEN',q=F(1),input_q=F(1),lo=-1,hi=2,constants=()):
    variables=[Variable(f'x{i}',lo,hi,input_q) for i in range(len(forms))]
    names={v.name for v in variables}
    lines=[f'rat({a.numerator},{a.denominator})*x{i}+rat({c.numerator},{c.denominator})' for i,(a,c) in enumerate(forms)]
    lines += [f'rat({c.numerator},{c.denominator})' for c in constants]
    raw=[parse(line,names) for line in lines]
    variants={'per_line':add_nodes([Node('round',(e,),(q,mode)) for e in raw]),'total':Node('round',(add_nodes(raw),),(q,mode))}
    return Rule('parity_property',variables,variants,{},dict(lines=lines,mode=mode,quantum=str(q)))

def discrepancy(forms,ticks,mode,q,input_q,constants):
    values=[a*x*input_q+c for (a,c),x in zip(forms,ticks)]+list(constants)
    return q*(rounded(sum(values,F(0))/q,mode)-sum(rounded(y/q,mode) for y in values))

def check_endpoints(rule,forms,mode,q,input_q,lo,hi,constants):
    answers=[discrepancy(forms,xs,mode,q,input_q,constants) for xs in product(range(lo,hi+1),repeat=len(forms))]
    result=dp_batch(rule)
    assert F(result['minimum_signed'])==min(answers)
    assert F(result['maximum_signed'])==max(answers)
    assert F(result['maximum_discrepancy'])==max(abs(v) for v in answers)
    assert result['parity_states']<=2
    assert result['transitions']<=8*(len(forms)+len(constants))
    for key,endpoint in [('minimum_counterexample',min(answers)),('maximum_counterexample',max(answers))]:
        witness=result[key]
        assert set(witness)=={v.name for v in rule.variables}
        assert all(lo<=witness[v.name]<=hi for v in rule.variables)
        ticks=[witness[f'x{i}'] for i in range(len(forms))]
        assert discrepancy(forms,ticks,mode,q,input_q,constants)==endpoint
    cyclic=cyclic_batch(rule,state_cap=100000)
    assert (cyclic['minimum_signed'],cyclic['maximum_signed'])==(result['minimum_signed'],result['maximum_signed'])
    return result

specification=st.lists(st.tuples(st.integers(-3,3),st.sampled_from([1,2,3,4,5]),st.integers(-4,4),st.sampled_from([1,2,3,4,5])),min_size=1,max_size=4)

@settings(max_examples=100,derandomize=True,deadline=None)
@given(specs=specification,lo=st.integers(-3,1),width=st.integers(0,3),mode=st.sampled_from(['HALF_EVEN','FLOOR','CEILING']),q=st.sampled_from([F(1),F(1,2),F(3,2)]),input_q=st.sampled_from([F(1),F(1,5),F(3,2)]))
def test_parity_signed_extrema_against_fraction_cartesian(specs,lo,width,mode,q,input_q):
    forms=[(F(a,b),F(c,d)) for a,b,c,d in specs];constants=(F(-1,7),F(1,2))
    rule=batch(forms,mode,q,input_q,lo,lo+width,constants)
    check_endpoints(rule,forms,mode,q,input_q,lo,lo+width,constants)

@settings(max_examples=100,derandomize=True,deadline=None)
@given(specs=specification,lo=st.integers(-3,1),width=st.integers(0,3),mode=st.sampled_from(['HALF_UP','DOWN','UP']),q=st.sampled_from([F(1),F(1,2),F(3,2)]),input_q=st.sampled_from([F(1),F(1,5),F(3,2)]))
def test_parity_nonnegative_signed_modes_against_fraction_cartesian(specs,lo,width,mode,q,input_q):
    hi=lo+width
    forms=[]
    for a,b,c,d in specs:
        slope=F(a,b);offset=max(F(0),-slope*lo*input_q,-slope*hi*input_q)+abs(F(c,d))
        forms.append((slope,offset))
    constants=(F(1,2),F(0))
    rule=batch(forms,mode,q,input_q,lo,hi,constants)
    check_endpoints(rule,forms,mode,q,input_q,lo,hi,constants)

@pytest.mark.parametrize('n',[1,3,5,7])
@pytest.mark.parametrize('q',[F(1),F(3,2)])
def test_parity_odd_line_half_ties(n,q):
    constants=(q/2,)*n
    rule=batch([],q=q,constants=constants)
    result=dp_batch(rule)
    expected=q*rounded(F(n,2),'HALF_EVEN')
    assert F(result['minimum_signed'])==expected==F(result['maximum_signed'])
    assert result['local_representatives']==n

@pytest.mark.parametrize('half,expected',[(F(1,2),1),(F(-1,2),-1)])
def test_parity_integer_offset_changes_outer_half_tie(half,expected):
    rule=batch([],constants=(F(1),half,F(0)))
    result=dp_batch(rule)
    assert F(result['minimum_signed'])==expected==F(result['maximum_signed'])

@pytest.mark.parametrize('mode,constant',[('HALF_UP',F(1,2)),('UP',F(1,4)),('DOWN',F(3,4))])
def test_parity_signed_terminal_uses_nonnegative_outer_identity(mode,constant):
    result=dp_batch(batch([],mode=mode,constants=(constant,)))
    assert result['maximum_discrepancy']=='0'

def test_parity_negative_floor_and_constant_denominators():
    rule=batch([],mode='FLOOR',constants=(F(-1,4),)*3)
    assert dp_batch(rule)['maximum_discrepancy']=='2'
    forms=[(F(1,2),F(1,1009)),(F(1,3),F(1,1013))]
    rule=batch(forms,lo=0,hi=8)
    result=dp_batch(rule)
    assert result['local_periods']==[4,6]
    assert result['local_representatives']==10
    values=[discrepancy(forms,xs,'HALF_EVEN',F(1),F(1),()) for xs in product(range(9),repeat=2)]
    assert F(result['minimum_signed'])==min(values)
    assert F(result['maximum_signed'])==max(values)
    with pytest.raises(NotCertified,match='denominator'): cyclic_batch(rule)

def test_parity_extra_policy_falls_back_and_batch_names_are_reserved(tmp_path):
    p=tmp_path/'extra.json'
    data=dict(variables={'x':dict(min=0,max=6)},variants={'extra':'x'},batch=dict(lines=['x/2'],mode='HALF_EVEN'))
    p.write_text(json.dumps(data));rule=load_rule(p)
    for method in [dp_batch,cyclic_batch]:
        with pytest.raises(NotCertified,match='only declared'): method(rule)
    result=analyze(rule)
    assert result['method']=='smt' and result['maximum_discrepancy']=='3'
    for reserved in ['per_line','total']:
        data['variants']={reserved:'x'};p.write_text(json.dumps(data))
        with pytest.raises(ValueError,match='collid'): load_rule(p)

def test_cli_cyclic_ablation(tmp_path):
    p=tmp_path/'cli.json';p.write_text(json.dumps(dict(variables={'x':dict(min=0,max=3),'y':dict(min=0,max=3)},batch=dict(lines=['x/2','y/2'],mode='HALF_EVEN'))))
    output=subprocess.check_output([sys.executable,'-m','roundguard.cli','analyze',str(p),'--method','cyclic','--json'],text=True)
    result=json.loads(output)
    assert result['method']=='cyclic-dp' and result['maximum_discrepancy']=='1'

def test_batch_shared_input_rejects_and_affine_cancellation_keeps_true_independence(tmp_path):
    p=tmp_path/'dependency.json'
    data=dict(variables={'x':dict(min=-2,max=3),'y':dict(min=-2,max=3)},batch=dict(lines=['x/2','x/3'],mode='HALF_EVEN'))
    p.write_text(json.dumps(data));rule=load_rule(p)
    for method in [dp_batch,cyclic_batch]:
        with pytest.raises(NotCertified,match='Independent'): method(rule)
    data['batch']['lines']=['x-x+y/2','x/3'];p.write_text(json.dumps(data))
    rule=load_rule(p);result=dp_batch(rule)
    assert result['minimum_signed']==cyclic_batch(rule)['minimum_signed']
    assert result['maximum_signed']==cyclic_batch(rule)['maximum_signed']
