import argparse,json
from .model import load_rule
from .analysis import analyze

def main():
    p=argparse.ArgumentParser(description="Exact monetary rounding-policy analysis on declared integer grids")
    sub=p.add_subparsers(dest="command",required=True)
    a=sub.add_parser("analyze"); a.add_argument("rule"); a.add_argument("--method",choices=["auto","smt","residue","dp"],default="auto"); a.add_argument("--timeout-ms",type=int,default=10000); a.add_argument("--json",action="store_true")
    args=p.parse_args(); r=analyze(load_rule(args.rule),args.method,args.timeout_ms)
    if args.json: print(json.dumps(r,indent=2))
    else:
        code={"SENSITIVE":"RG101","SAFE":"RG000","UNKNOWN":"RG900"}[r["status"]]
        print(f'{code} {r["status"]}: {r["name"]}')
        print('Method:',r['method']); print('Maximum discrepancy:',r.get('maximum_discrepancy','not established'))
        if r.get('counterexample'): print('Counterexample (integer input ticks):',r['counterexample'])
        if r.get('outputs'): print('Policy outputs:',r['outputs'])
        print('Scope: the supplied policies and input grids; sensitivity does not establish which policy is legally correct.')
    return 0

if __name__=="__main__": main()
