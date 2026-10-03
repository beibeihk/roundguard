"""Audit the Git index; never inspect credentials outside this project."""
import json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 files=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode('utf-8').split('\0')
 files=[f for f in files if f];problems=[]
 forbidden=['.venv/','literature/reviewer_primary/','literature/.systematic-literature-review/','paper/.paper-write-sci/','artifact/render/','notes/browser','arxiv/browser']
 patterns=[re.compile(r'AKIA[0-9A-Z]{16}'),re.compile(r'sk-[A-Za-z0-9_-]{24,}'),re.compile(r'Bearer\s+[A-Za-z0-9._-]{24,}'),re.compile(r'"(?:password|access_token|refresh_token|api_key)"\s*:\s*"[^"\s]+"',re.I)]
 for f in files:
  if any(f.startswith(p) for p in forbidden) or Path(f).name in {'auth.json','.env','cookies.json'}: problems.append(dict(file=f,reason='forbidden private/vendor material'))
  if (ROOT/f).suffix.lower() in {'.py','.md','.json','.csv','.tex','.bib','.ps1','.txt','.toml','.cff'}:
   body=(ROOT/f).read_text(encoding='utf-8-sig')
   if any(p.search(body) for p in patterns): problems.append(dict(file=f,reason='credential-like pattern; contents withheld'))
 assert not problems,problems
 report=dict(status='PASSED',tracked_files=len(files),excluded_private_downloads_and_browser_material=True,credential_like_patterns=0,scope='named private paths and common literal credential patterns; not a proof of absence of every possible secret')
 (ROOT/'artifact').mkdir(exist_ok=True)
 (ROOT/'artifact/public_tree_audit.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
if __name__=='__main__': main()
