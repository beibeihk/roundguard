"""Independent Decimal rounding oracle; exhaustive enumeration on small grids.

Decimal conversion is exact and context-independent for terminating rationals.
Precision is selected from decimal spans, including denominator powers of 2/5.
Arithmetic traps reject silent inexactness; only deliberate grid quantization
may round. Nonterminating rational intermediates are rejected. This module does
not use the concrete Fraction quantizer or the symbolic encoder.
"""
from decimal import Decimal,localcontext,Inexact,Rounded,DecimalException
from fractions import Fraction as F
from itertools import product
from .model import walk

def decimal_scale(v):
    """Return exact denominator exponents, rejecting nonterminating decimals."""
    d=F(v).denominator
    exponents=[]
    for p in (2,5):
        exponent=0
        while d%p==0: d//=p; exponent+=1
        exponents.append(exponent)
    if d!=1: raise ValueError("Decimal oracle requires terminating rationals")
    return tuple(exponents)

def terminating(v):
    try: decimal_scale(v)
    except ValueError: return False
    return True

def dec(v):
    v=F(v)
    a,b=decimal_scale(v); scale=max(a,b)
    integer=abs(v.numerator)*2**(scale-a)*5**(scale-b)
    # Tuple construction performs no context-sensitive arithmetic. In
    # particular, 1/2**1000 is not truncated by the caller's current precision.
    digits=tuple(int(c) for c in str(integer))
    return Decimal((int(v<0),digits,-scale))

def execute(e,env):
    """Reject unsupported arithmetic rather than return an approximate oracle."""
    try:
        with localcontext() as ctx:
            ctx.traps[Inexact]=True; ctx.traps[Rounded]=True
            return _execute(e,env)
    except DecimalException as error:
        raise ValueError("Decimal oracle arithmetic is not exact at the selected precision, or normalized quantum division is nonterminating") from error

def _execute(e,env):
    if e.op=="const": return dec(e.value)
    if e.op=="var": return env[e.value]
    a=[_execute(n,env) for n in e.args]
    if e.op=="add": return a[0]+a[1]
    if e.op=="sub": return a[0]-a[1]
    if e.op=="scale": return a[0]*dec(e.value)
    if e.op=="round":
        q,m=e.value; dq=dec(q)
        normalized=a[0]/dq
        # Rounding here is the requested semantic operation. Multiplication
        # back to the grid takes place after restoring exact-arithmetic traps.
        with localcontext() as rounding_context:
            rounding_context.traps[Inexact]=False
            rounding_context.traps[Rounded]=False
            integer=normalized.quantize(Decimal(1),rounding="ROUND_"+m)
        return integer*dq
    if e.op=="min": return min(a)
    if e.op=="max": return max(a)
    if e.op=="if":
        p={"lt":a[0]<a[1],"le":a[0]<=a[1],"gt":a[0]>a[1],"ge":a[0]>=a[1]}[e.value]
        return a[2] if p else a[3]
    raise ValueError(e.op)

def precision(rule):
    # A decimal span includes all possible positions between a coefficient's
    # integer and fractional digits. Summing spans over all nodes conservatively
    # covers products, cancellation/alignment, and one carry per additive node.
    # Runtime traps remain the final guard if unsupported division or a budget
    # error is encountered. This is a budget, not a license to approximate.
    def span(v):
        value=dec(v); digits=value.as_tuple()
        return len(digits.digits)+abs(digits.exponent)+1
    budget=100+sum(span(v.lo)+span(v.hi)+span(v.quantum) for v in rule.variables)
    for e in rule.variants.values():
        for n in walk(e):
            budget+=1
            fs=[n.value] if n.op in {"const","scale"} else ([n.value[0]] if n.op=="round" else [])
            budget+=sum(span(f) for f in fs)
            if n.op=="round" and terminating(1/n.value[0]):
                budget+=span(1/n.value[0])
    return budget

def exhaustive(rule,limit=300000):
    if rule.size>limit: raise ValueError("Oracle domain exceeds declared limit")
    maximum=F(0); witness=None; evaluations=0
    with localcontext() as ctx:
        ctx.prec=precision(rule)
        ctx.traps[Inexact]=True; ctx.traps[Rounded]=True
        for xs in product(*(range(v.lo,v.hi+1) for v in rule.variables)):
            env={v.name:Decimal(x)*dec(v.quantum) for v,x in zip(rule.variables,xs)}
            vals=[execute(e,env) for e in rule.variants.values()]; spread=F(max(vals)-min(vals)); evaluations+=1
            if spread>maximum: maximum=spread; witness=dict(zip((v.name for v in rule.variables),xs))
    return dict(status="SENSITIVE" if maximum else "SAFE",maximum_discrepancy=str(maximum),counterexample=witness,evaluations=evaluations)
