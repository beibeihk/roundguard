"""Exact concrete semantics and a separate constraint encoding."""
from fractions import Fraction as F
import z3
from .model import Node

def quantize(x,q,mode):
    x,q=F(x),F(q); t=x/q; k=t.numerator//t.denominator; rem=t-k
    if mode=="FLOOR": n=k
    elif mode=="CEILING": n=k+(rem!=0)
    elif mode=="DOWN": n=k+(t<0 and rem!=0)
    elif mode=="UP": n=k+(t>0 and rem!=0)
    elif mode=="HALF_EVEN": n=k+(rem>F(1,2) or (rem==F(1,2) and k%2!=0))
    elif mode=="HALF_UP": n=k+(rem>F(1,2) or (rem==F(1,2) and t>=0))
    else: raise ValueError(mode)
    return n*q

def evaluate(e,env):
    op=e.op
    if op=="const": return e.value
    if op=="var": return F(env[e.value])
    a=[evaluate(n,env) for n in e.args]
    if op=="add": return a[0]+a[1]
    if op=="sub": return a[0]-a[1]
    if op=="scale": return a[0]*e.value
    if op=="round": return quantize(a[0],*e.value)
    if op=="min": return min(a)
    if op=="max": return max(a)
    if op=="if":
        p={"lt":a[0]<a[1],"le":a[0]<=a[1],"gt":a[0]>a[1],"ge":a[0]>=a[1]}[e.value]
        return a[2] if p else a[3]
    raise ValueError(op)

def rational(v):
    v=F(v); return z3.RealVal(f"{v.numerator}/{v.denominator}")

def symbolic(e,env):
    if e.op=="const": return rational(e.value)
    if e.op=="var": return env[e.value]
    a=[symbolic(n,env) for n in e.args]
    if e.op=="add": return a[0]+a[1]
    if e.op=="sub": return a[0]-a[1]
    if e.op=="scale": return a[0]*rational(e.value)
    if e.op=="round":
        q,m=e.value; t=a[0]/rational(q); k=z3.ToInt(t); rem=t-z3.ToReal(k)
        if m=="FLOOR": n=k
        elif m=="CEILING": n=k+z3.If(rem==0,0,1)
        elif m=="DOWN": n=z3.If(t>=0,k,-z3.ToInt(-t))
        elif m=="UP": n=z3.If(t>=0,-z3.ToInt(-t),k)
        else:
            tie=(k%2==1) if m=="HALF_EVEN" else (t>=0)
            n=k+z3.If(z3.Or(rem>rational(F(1,2)),z3.And(rem==rational(F(1,2)),tie)),1,0)
        return z3.ToReal(n)*rational(q)
    if e.op in {"min","max"}:
        return z3.If(a[0]<=a[1] if e.op=="min" else a[0]>=a[1],a[0],a[1])
    if e.op=="if":
        p={"lt":a[0]<a[1],"le":a[0]<=a[1],"gt":a[0]>a[1],"ge":a[0]>=a[1]}[e.value]
        return z3.If(p,a[2],a[3])
    raise ValueError(e.op)

def tick_env(rule,ticks):
    return {v.name:F(ticks[v.name])*v.quantum for v in rule.variables}

def to_fraction(x):
    x=z3.simplify(x)
    if z3.is_int_value(x): return F(x.as_long())
    if z3.is_rational_value(x): return F(x.numerator_as_long(),x.denominator_as_long())
    raise ValueError("Non-rational solver result: "+str(x))
