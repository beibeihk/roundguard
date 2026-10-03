"""Compare a separately installed remote clone with the original exact evidence."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
def main():
 clone=Path(sys.argv[1]).resolve();assert clone!=ROOT
 def read(root,f): return json.loads((root/f).read_text(encoding='utf-8-sig'))
 original=read(ROOT,'results/ground_truth.json');repeated=read(clone,'results/ground_truth.json')
 assert original==repeated,'Small exact evidence changed'
 certs=read(ROOT,'results/scaling_ground_truth.json');newcerts=read(clone,'results/scaling_ground_truth.json')
 assert certs==newcerts,'Scaling certificates changed'
 denom=read(ROOT,'results/denominator_ground_truth.json');newdenom=read(clone,'results/denominator_ground_truth.json')
 assert denom==newdenom,'Denominator certificates changed'
 assert read(clone,'results/integrity_audit.json')['status']=='CONSISTENCY_AUDIT_PASSED'
 assert read(clone,'results/latex_build.json')['success']
 pack=read(clone,'arxiv/build_report.json');assert pack['success'] and pack['archive_build']['success']
 hashes={}
 for folder in ['src','tests','experiments','scripts']:
  for p in (ROOT/folder).rglob('*.py'):
   if '__pycache__' in p.parts: continue
   f=p.relative_to(ROOT);assert p.read_bytes()==(clone/f).read_bytes(),str(f)
   hashes[str(f).replace('\\','/')]=hashlib.sha256(p.read_bytes()).hexdigest()
 log=(ROOT/'artifact/clean_clone_log.txt').read_text(encoding='utf-8-sig')
 tests=re.search(r'(\d+) passed in ([\d.]+)s',log);assert tests and int(tests[1])>=107
 report=dict(status='PASSED',date_utc=datetime.now(timezone.utc).isoformat(),repository='https://github.com/beibeihk/roundguard',tested_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=clone,text=True).strip(),command='powershell -ExecutionPolicy Bypass -File scripts/reproduce_all.ps1',execution_exit_code=0,pytest_passed=int(tests[1]),pytest_seconds=float(tests[2]),small_exact_records_identical=len(repeated),scaling_certificates_identical=len(newcerts),denominator_certificates_identical=len(newdenom),separate_virtual_environment=(clone/'.venv/Scripts/python.exe').is_file(),paper_clean_build=True,archive_extracted_clean_build=True,clone_scaling_completions=read(clone,'results/paper_facts.json')['scaling_complete'],clone_denominator_completions=read(clone,'results/paper_facts.json')['denominator_complete'],source_sha256=hashes,scope='Remote clean clone, fresh venv, full README command; exact records reproduce. Runtime/SMT outcomes may vary. Subsequent release changes are documentation/audit records only.')
 assert report['separate_virtual_environment']
 (ROOT/'artifact/clean_clone_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8',newline='\n')
 print(json.dumps({k:v for k,v in report.items() if k!='source_sha256'},indent=2))
if __name__=='__main__': main()
