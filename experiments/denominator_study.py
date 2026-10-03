"""Independent integer-rounding certificates for nonterminating-rational lines."""
import csv,json,time
from fractions import Fraction as F
from math import lcm
from roundguard.analysis import analyze
from roundguard.model import load_rule

def nearest_even(value):
    """Integer division only; independent of the analyzer and Decimal oracle."""
    k,remainder=divmod(value.numerator,value.denominator)
    doubled=2*remainder
    return k+int(doubled>value.denominator or (doubled==value.denominator and k%2))

def certificate(rule):
    # Generator restricts this separate study to raw x_i / p_i, unit quanta.
    denominators=[int(line.split('/')[1]) for line in rule.batch['lines']]
    lower=F(0);upper=F(0)
    for variable,p in zip(rule.variables,denominators):
        assert variable.quantum==1
        period=2*p
        residuals=[F(x,p)-nearest_even(F(x,p)) for x in range(variable.lo,min(variable.hi+1,variable.lo+period))]
        lower+=min(residuals);upper+=max(residuals)
    envelope=max(-lower,upper)+F(1,2)
    bound=envelope.numerator//envelope.denominator
    return denominators,lower,upper,bound

def replay(rule,denominators,ticks):
    assert set(ticks)=={v.name for v in rule.variables}
    assert all(type(ticks[v.name]) is int and v.lo<=ticks[v.name]<=v.hi for v in rule.variables)
    raw=[F(ticks[v.name],p) for v,p in zip(rule.variables,denominators)]
    return abs(nearest_even(sum(raw))-sum(nearest_even(y) for y in raw))

def run(root):
    rows=[];certs=[]
    for path in sorted((root/'benchmarks/denominators').glob('*.json')):
        rule=load_rule(path);exact=analyze(rule,'dp')
        ds,lower,upper,bound=certificate(rule)
        assert exact['complete'] and replay(rule,ds,exact['counterexample'])==bound==F(exact['maximum_discrepancy'])
        certs.append(dict(case=rule.name,ground_truth=str(bound),local_lower=str(lower),local_upper=str(upper),integral_upper_bound=str(bound),counterexample=exact['counterexample'],denominators=ds,oracle='Independent integer quotient/remainder local residual envelope + integral bound + attaining replay'))
        for method in ['dp','cyclic','residue','smt']:
            for repetition in range(3):
                result=analyze(rule,method,timeout_ms=1500)
                if result.get('complete'): assert F(result['maximum_discrepancy'])==bound
                rows.append(dict(case=rule.name,method=method,repetition=repetition,nvars=len(rule.variables),lower=rule.variables[0].lo,upper=rule.variables[0].hi,time_seconds=result['time_seconds'],status=result['status'],complete=result.get('complete',False),maximum_discrepancy=result.get('maximum_discrepancy'),exact_truth=str(bound),common_denominator=lcm(*ds),parity_states=exact['parity_states'],local_representatives=exact['local_representatives'],reason=result.get('reason','')))
            print(f'denominator {rule.name} {method}: {result["status"]} complete={result.get("complete")}',flush=True)
        with (root/'results/denominators.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (root/'results/denominator_ground_truth.json').write_text(json.dumps(certs,indent=2),encoding='utf-8')
