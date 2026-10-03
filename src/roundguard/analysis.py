"""Structural periods, exact residue convolution, and bounded SMT fallback."""
from __future__ import annotations
from fractions import Fraction as F
from math import gcd,lcm,ceil,prod
from itertools import product,combinations
from time import perf_counter
import z3
from .model import COVARIANT,parse,walk
from .semantics import evaluate,quantize,symbolic,rational,to_fraction,tick_env

class NotCertified(ValueError): pass

def affine(e,variables):
    """Erases rounding; coefficient coordinates are integer input ticks."""
    zero={v.name:F(0) for v in variables}
    if e.op=="const": return e.value,zero
    if e.op=="var":
        zero[e.value]=next(v.quantum for v in variables if v.name==e.value)
        return F(0),zero
    if e.op=="round": return affine(e.args[0],variables)
    if e.op=="scale":
        c,a=affine(e.args[0],variables)
        return c*e.value,{k:v*e.value for k,v in a.items()}
    if e.op in {"add","sub"}:
        c,a=affine(e.args[0],variables); d,b=affine(e.args[1],variables); s=1 if e.op=="add" else -1
        return c+s*d,{k:a[k]+s*b[k] for k in a}
    raise NotCertified("Non-affine erasure")

def periods(rule):
    slopes=[]; ts={v.name:1 for v in rule.variables}
    for e in rule.variants.values():
        _,a=affine(e,rule.variables); slopes.append(a)
        for n in walk(e):
            if n.op=="round":
                q,m=n.value
                if m not in COVARIANT: raise NotCertified("Mode lacks global translation covariance")
                _,a=affine(n.args[0],rule.variables)
                for k,c in a.items():
                    ts[k]=lcm(ts[k],(c/(q*(2 if m=="HALF_EVEN" else 1))).denominator)
    if any(a!=slopes[0] for a in slopes[1:]): raise NotCertified("Unequal output drift")
    return ts

def interval(e,variables):
    if e.op=="const": return e.value,e.value
    if e.op=="var":
        v=next(v for v in variables if v.name==e.value); return v.lo*v.quantum,v.hi*v.quantum
    a=[interval(n,variables) for n in e.args]
    if e.op=="add": return a[0][0]+a[1][0],a[0][1]+a[1][1]
    if e.op=="sub": return a[0][0]-a[1][1],a[0][1]-a[1][0]
    if e.op=="scale": return min(x*e.value for x in a[0]),max(x*e.value for x in a[0])
    if e.op=="round": return quantize(a[0][0],*e.value),quantize(a[0][1],*e.value)
    if e.op=="min": return min(x[0] for x in a),min(x[1] for x in a)
    if e.op=="max": return max(x[0] for x in a),max(x[1] for x in a)
    if e.op=="if": return min(a[2][0],a[3][0]),max(a[2][1],a[3][1])
    raise ValueError(e.op)

def error_bound(e):
    if e.op in {"const","var"}: return F(0)
    a=[error_bound(n) for n in e.args]
    if e.op in {"add","sub"}: return sum(a)
    if e.op=="scale": return abs(e.value)*a[0]
    if e.op=="round":
        q,m=e.value; return a[0]+q/(2 if m in {"HALF_EVEN","HALF_UP"} else 1)
    raise NotCertified("No affine error bound")

def denominator(e,vs):
    if e.op=="const": return e.value.denominator
    if e.op=="var": return next(v.quantum.denominator for v in vs if v.name==e.value)
    if e.op=="round": return e.value[0].denominator
    if e.op=="scale": return denominator(e.args[0],vs)*e.value.denominator
    return lcm(*(denominator(n,vs) for n in e.args))

def dp_batch(rule,state_cap=400):
    """Exact total-minus-lines extrema on independent affine lines only."""
    b=rule.batch
    if not b or len(rule.variants)!=2: raise NotCertified("DP needs only declared line/total policies")
    q=F(b.get("quantum","1")); mode=b.get("mode","HALF_EVEN")
    lines=[parse(s,{v.name for v in rule.variables}) for s in b["lines"]]
    forms=[]; used=set(); B=1
    for e in lines:
        if any(n.op=="round" for n in walk(e)): raise NotCertified("Raw lines must be affine")
        c,a=affine(e,rule.variables); c/=q; a={k:v/q for k,v in a.items() if v}
        if len(a)>1 or used.intersection(a): raise NotCertified("Independent one-variable lines required")
        if mode not in COVARIANT:
            minimum=c
            for name,A in a.items():
                v=next(v for v in rule.variables if v.name==name)
                minimum+=min(A*v.lo,A*v.hi)
            if minimum<0: raise NotCertified("Sign-sensitive DP requires every raw line nonnegative")
        used.update(a); forms.append((c,a)); B=lcm(B,c.denominator,*(v.denominator for v in a.values()))
    M=2*B
    if M>state_cap: raise NotCertified("Common denominator exceeds DP budget")
    tables=[]
    for c,a in forms:
        if a:
            name,A=next(iter(a.items())); v=next(v for v in rule.variables if v.name==name)
            T=M//gcd(abs(int(B*A)),M); xs=range(v.lo,min(v.hi+1,v.lo+T))
        else: name=None; A=F(0); xs=[0]
        table={}
        for x in xs:
            y=c+A*x; z=int(B*y); d=int(B*quantize(y,1,mode)-z); r=z%M
            if r not in table: table[r]=(d,d,x,x)
            else:
                low,high,xl,xh=table[r]
                table[r]=(min(low,d),max(high,d),x if d<low else xl,x if d>high else xh)
        tables.append((name,table))
    # Separate min/max paths are needed because extrema may use different inputs.
    low={0:0}; high={0:0}; transitions=0; trace_low=[]; trace_high=[]
    for name,table in tables:
        nl={}; nh={}; pl={}; ph={}
        for state,out,pointers in [(low,nl,pl),(high,nh,ph)]:
            islow=state is low
            for s,v in state.items():
                for r,(dl,dh,xl,xh) in table.items():
                    target=(s+r)%M; val=v+(dl if islow else dh); transitions+=1
                    if target not in out or (val<out[target] if islow else val>out[target]):
                        out[target]=val; pointers[target]=(s,xl if islow else xh)
        trace_low.append(pl);trace_high.append(ph)
        low,high=nl,nh
    mn=None; mx=None; wmin=None; wmax=None
    for r in low:
        correction=B*quantize(F(r,B),1,mode)-r
        dmin=(correction-high[r])*q/B; dmax=(correction-low[r])*q/B
        if mn is None or dmin<mn: mn,wmin=dmin,r
        if mx is None or dmax>mx: mx,wmax=dmax,r
    def reconstruct(r,traces):
        witness={}
        for k in range(len(tables)-1,-1,-1):
            prev,x=traces[k][r]; name=tables[k][0]
            if name is not None: witness[name]=x
            r=prev
        if r!=0: raise RuntimeError("Broken DP predecessor")
        return witness
    wmin=reconstruct(wmin,trace_high);wmax=reconstruct(wmax,trace_low)
    for w in (wmin,wmax):
        for v in rule.variables: w.setdefault(v.name,v.lo)
    worst=max(abs(mn),abs(mx)); witness=wmin if abs(mn)>=abs(mx) else wmax
    # An independently executed AST replay is mandatory for every reported optimum.
    vals={k:evaluate(e,tick_env(rule,witness)) for k,e in rule.variants.items()}
    if abs(vals['total']-vals['per_line'])!=worst: raise RuntimeError("DP witness replay mismatch")
    return dict(status="SENSITIVE" if worst else "SAFE",method="residue-dp",maximum_discrepancy=str(worst),minimum_signed=str(mn),maximum_signed=str(mx),counterexample=witness if worst else None,outputs={k:str(v) for k,v in vals.items()},denominator=B,residue_states=M,transitions=transitions,domain_size=rule.size,complete=True)

def smt_analysis(rule,use_period=True,timeout_ms=10000):
    ts=None; reason=None
    if use_period:
        try: ts=periods(rule)
        except NotCertified as e: reason=str(e)
    xs={v.name:z3.Int(v.name) for v in rule.variables}
    env={v.name:z3.ToReal(xs[v.name])*rational(v.quantum) for v in rule.variables}
    solver=z3.Solver(); solver.set(timeout=timeout_ms,random_seed=7)
    for v in rule.variables:
        hi=min(v.hi,v.lo+ts[v.name]-1) if ts else v.hi
        solver.add(xs[v.name]>=v.lo,xs[v.name]<=hi)
    vals={k:symbolic(e,env) for k,e in rule.variants.items()}
    pairs=list(combinations(vals,2)); differences=[vals[a]-vals[b] for a,b in pairs]
    predicate=z3.Or(*(d!=0 for d in differences))
    solver.push(); solver.add(predicate); sat=solver.check()
    base=dict(method="residue-smt" if ts else "smt",periods=ts,period_rejection=reason,domain_size=rule.size,reduced_size=prod(min(v.hi-v.lo+1,ts[v.name]) for v in rule.variables) if ts else rule.size)
    if sat==z3.unsat:
        solver.pop(); return dict(base,status="SAFE",maximum_discrepancy="0",counterexample=None,complete=True)
    if sat==z3.unknown:
        why=solver.reason_unknown();solver.pop(); return dict(base,status="UNKNOWN",reason=why,complete=False)
    model=solver.model(); ticks={v.name:model.eval(xs[v.name],model_completion=True).as_long() for v in rule.variables}
    solver.pop()
    D=lcm(*(denominator(e,rule.variables) for e in rule.variants.values()))
    upper=F(0)
    for a,b in pairs:
        ea,eb=rule.variants[a],rule.variants[b]
        try:
            if affine(ea,rule.variables)==affine(eb,rule.variables): ub=error_bound(ea)+error_bound(eb)
            else: raise NotCertified()
        except NotCertified:
            ia,ib=interval(ea,rule.variables),interval(eb,rule.variables); ub=max(abs(ia[0]-ib[1]),abs(ia[1]-ib[0]))
        upper=max(upper,ub)
    absdiff=[z3.If(d>=0,d,-d) for d in differences]
    maxdiff=absdiff[0]
    for d in absdiff[1:]: maxdiff=z3.If(d>maxdiff,d,maxdiff)
    objective=z3.ToInt(maxdiff*D)
    low=ceil(max(abs(evaluate(rule.variants[a],tick_env(rule,ticks))-evaluate(rule.variants[b],tick_env(rule,ticks))) for a,b in pairs)*D)
    high=ceil(upper*D)
    while low<high:
        mid=(low+high+1)//2; solver.push(); solver.add(objective>=mid); sat=solver.check()
        if sat==z3.unknown:
            solver.pop(); return dict(base,status="SENSITIVE",maximum_discrepancy=None,lower_bound=str(F(low,D)),upper_bound=str(F(high,D)),counterexample=ticks,complete=False,reason="Optimization timed out")
        if sat==z3.sat:
            m=solver.model(); ticks={v.name:m.eval(xs[v.name],model_completion=True).as_long() for v in rule.variables}; low=mid
        else: high=mid-1
        solver.pop()
    outputs={k:evaluate(e,tick_env(rule,ticks)) for k,e in rule.variants.items()}
    replay=max(abs(outputs[a]-outputs[b]) for a,b in pairs)
    if replay!=F(low,D): raise RuntimeError("SMT optimum replay mismatch")
    return dict(base,status="SENSITIVE",maximum_discrepancy=str(replay),counterexample=ticks,outputs={k:str(v) for k,v in outputs.items()},complete=True)

def analyze(rule,method="auto",timeout_ms=10000):
    start=perf_counter(); result=None
    if method in {"auto","dp"}:
        try: result=dp_batch(rule)
        except NotCertified as e:
            if method=="dp": result=dict(status="UNKNOWN",method="dp",reason=str(e),complete=False)
    if result is None: result=smt_analysis(rule,use_period=method!="smt",timeout_ms=timeout_ms)
    result.update(name=rule.name,time_seconds=perf_counter()-start)
    return result
