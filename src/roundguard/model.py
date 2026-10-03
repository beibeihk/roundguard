"""Validated JSON rule input and a deliberately restricted Python expression parser."""
from __future__ import annotations
import ast
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path

MODES = {"HALF_EVEN", "HALF_UP", "FLOOR", "CEILING", "DOWN", "UP"}
COVARIANT = {"HALF_EVEN", "FLOOR", "CEILING"}

def exact_field(v):
    if type(v) not in {int,str}: raise ValueError("Grid quanta must be integers or rational/decimal strings; JSON floats are rejected")
    return F(v)

@dataclass(frozen=True)
class Node:
    op: str
    args: tuple = ()
    value: object = None

@dataclass(frozen=True)
class Variable:
    name: str
    lo: int
    hi: int
    quantum: F = F(1)
    kind: str = "Money"

@dataclass
class Rule:
    name: str
    variables: list[Variable]
    variants: dict[str, Node]
    metadata: dict
    batch: dict | None = None

    @property
    def size(self):
        return __import__('math').prod(v.hi-v.lo+1 for v in self.variables)

def const(v):
    return Node("const", value=F(v))

def parse(text: str, names: set[str]) -> Node:
    tree = ast.parse(text, mode="eval")
    def literal(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (str, int)) and not isinstance(n.value, bool):
            return n.value
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -F(literal(n.operand))
        raise ValueError("Exact constants must be integers, rational strings or rat(a,b)")
    def go(n):
        if isinstance(n, ast.Constant):
            return const(literal(n))
        if isinstance(n, ast.Name) and n.id in names:
            return Node("var", value=n.id)
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return Node("scale", (go(n.operand),), F(-1))
        if isinstance(n, ast.BinOp):
            a,b = go(n.left),go(n.right)
            if isinstance(n.op, (ast.Add,ast.Sub)):
                return Node("add" if isinstance(n.op,ast.Add) else "sub", (a,b))
            if isinstance(n.op,ast.Mult):
                if a.op=="const": return Node("scale", (b,), a.value)
                if b.op=="const": return Node("scale", (a,), b.value)
            if isinstance(n.op,ast.Div) and b.op=="const" and b.value:
                return Node("scale", (a,), 1/b.value)
            raise ValueError("Only multiplication/division by exact constants is supported")
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and not n.keywords:
            fn=n.func.id
            if fn in {"rat","rate","decimal"}:
                if fn=="rat" and len(n.args)==2: return const(F(literal(n.args[0]),literal(n.args[1])))
                if len(n.args)==1: return const(literal(n.args[0]))
            if fn in {"Q","maybe"}:
                if len(n.args)!=(3 if fn=="Q" else 4): raise ValueError("Q(e, quantum, mode); maybe(e, quantum, mode, site)")
                q=F(literal(n.args[1])); mode=literal(n.args[2])
                if q<=0 or mode not in MODES: raise ValueError("Invalid quantum or rounding mode")
                val=(q,mode) if fn=="Q" else (q,mode,str(literal(n.args[3])))
                return Node("round" if fn=="Q" else "optional",(go(n.args[0]),),val)
            if fn in {"min","max"} and len(n.args)==2:
                return Node(fn,tuple(go(x) for x in n.args))
            if fn=="sum" and len(n.args)==1 and isinstance(n.args[0],(ast.List,ast.Tuple)):
                return add_nodes([go(x) for x in n.args[0].elts])
        if isinstance(n,ast.IfExp) and isinstance(n.test,ast.Compare) and len(n.test.ops)==1 and isinstance(n.test.ops[0],(ast.Lt,ast.LtE,ast.Gt,ast.GtE)):
            rel={ast.Lt:"lt",ast.LtE:"le",ast.Gt:"gt",ast.GtE:"ge"}[type(n.test.ops[0])]
            return Node("if",(go(n.test.left),go(n.test.comparators[0]),go(n.body),go(n.orelse)),rel)
        raise ValueError("Unsupported expression syntax: "+ast.dump(n))
    return go(tree.body)

def add_nodes(nodes):
    if not nodes: return const(0)
    e=nodes[0]
    for b in nodes[1:]: e=Node("add",(e,b))
    return e

def walk(e):
    yield e
    for a in e.args: yield from walk(a)

def resolve(e, chosen):
    args=tuple(resolve(a,chosen) for a in e.args)
    if e.op=="optional":
        q,m,site=e.value
        return Node("round",args,(q,m)) if site in chosen else args[0]
    return Node(e.op,args,e.value)

def load_rule(path) -> Rule:
    data=json.loads(Path(path).read_text(encoding="utf-8-sig"))
    vs=[]
    for name,v in data["variables"].items():
        lo,hi=v["min"],v["max"]
        if type(lo)!=int or type(hi)!=int or lo>hi: raise ValueError("Finite nonempty integer tick bounds required")
        q=exact_field(v.get("quantum","1")); kind=v.get("type","Money")
        if q<=0 or kind not in {"Money","Integer","Decimal","Rate"}: raise ValueError("Invalid input grid/type")
        if kind=="Integer" and q!=1: raise ValueError("Integer quantum must be one")
        vs.append(Variable(name,lo,hi,q,kind))
    names=set(data["variables"])
    variants={k:parse(v,names) for k,v in data.get("variants",{}).items()}
    if "template" in data:
        e=parse(data["template"],names)
        sites=sorted({n.value[2] for n in walk(e) if n.op=="optional"})
        if len(sites)>10: raise ValueError("Policy enumeration limited to ten independent optional sites")
        for bits in itertools.product([False,True],repeat=len(sites)):
            chosen={s for s,b in zip(sites,bits) if b}
            variants['placement_'+''.join('1' if b else '0' for b in bits)]=resolve(e,chosen)
    batch=data.get("batch")
    if batch:
        q=exact_field(batch.get("quantum","1")); mode=batch.get("mode","HALF_EVEN")
        if q<=0 or mode not in MODES: raise ValueError("Invalid batch rounding")
        lines=[parse(s,names) for s in batch["lines"]]
        variants["per_line"]=add_nodes([Node("round",(e,),(q,mode)) for e in lines])
        variants["total"]=Node("round",(add_nodes(lines),),(q,mode))
    if len(variants)<2: raise ValueError("At least two rounding policies required")
    if any(n.op=="optional" for e in variants.values() for n in walk(e)): raise ValueError("Unresolved optional site")
    return Rule(data.get("name",Path(path).stem),vs,variants,{k:v for k,v in data.items() if k not in {"variants","template","batch","variables"}},batch)
