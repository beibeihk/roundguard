"""Build and reject missing references, unreadable boxes, and unembedded fonts."""
import json,re,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(cmd,cwd):
 r=subprocess.run(cmd,cwd=cwd,text=True,encoding='utf-8',errors='replace',capture_output=True)
 if r.returncode: raise RuntimeError(r.stdout[-10000:]+r.stderr[-3000:])
 return r.stdout
def build(directory):
 run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','main.tex'],directory)
 log=(directory/'main.log').read_text(errors='replace')
 bad=[s for s in ['undefined','There were undefined','Overfull \\hbox','Overfull \\vbox','LaTeX Error','Fatal error'] if s in log]
 if bad: raise RuntimeError('LaTeX checks failed: '+str(bad))
 fonts=run(['pdffonts',str(directory/'main.pdf')],directory)
 rows=fonts.splitlines()[2:]
 if not rows or any(not re.search(r'\byes\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',s) or 'Type 3' in s for s in rows):
  raise RuntimeError('Font embedding check failed: '+fonts)
 return dict(success=True,fonts=fonts,undefined_references=False,overfull_boxes=False)
def main():
 dest=ROOT/'paper'/'figures';dest.mkdir(exist_ok=True)
 shutil.copy2(ROOT/'figures'/'scalability.pdf',dest/'scalability.pdf')
 report=build(ROOT/'paper');(ROOT/'results'/'latex_build.json').write_text(json.dumps(report,indent=2))
 print('Paper clean build and font checks passed.')
if __name__=='__main__': main()
