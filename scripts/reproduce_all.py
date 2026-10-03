"""Deterministic artifacts; measured runtime and SMT completion may vary."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(*args): subprocess.run(list(args),cwd=ROOT,check=True)
def main():
 run(sys.executable,'-m','pip','install','-r','requirements-lock.txt')
 run(sys.executable,'-m','pip','install','-e','.[reproduce]')
 run(sys.executable,'scripts/generate_benchmarks.py')
 run(sys.executable,'-m','pytest','-q')
 run(sys.executable,'scripts/proof_sanity.py','--implementation')
 run(sys.executable,'experiments/run.py')
 run(sys.executable,'scripts/make_figures.py')
 run(sys.executable,'scripts/integrity_audit.py')
 run(sys.executable,'scripts/build_paper.py')
 run(sys.executable,'scripts/package_arxiv.py')
 run(sys.executable,'scripts/export_metadata.py')
if __name__=='__main__': main()
