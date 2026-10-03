"""Whitelist source, compile independently, archive, extract, and recompile."""
import hashlib,json,shutil,tarfile,uuid
from pathlib import Path
from build_paper import ROOT,build
FILES=['main.tex','evaluation.tex','accuracy_table.tex','cases_table.tex','denominator_table.tex','result_macros.tex','references.bib','main.bbl','figures/scalability.pdf']
def main():
 out=ROOT/'arxiv';out.mkdir(exist_ok=True)
 stage=ROOT/'artifact'/('clean_source_'+uuid.uuid4().hex);stage.mkdir(parents=True)
 for f in FILES:
  target=stage/f;target.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(ROOT/'paper'/f,target)
 report=build(stage)
 archive=out/'arxiv_submission.tar.gz'
 with tarfile.open(archive,'w:gz',format=tarfile.PAX_FORMAT) as tar:
  for f in FILES: tar.add(stage/f,arcname=f,recursive=False)
 extracted=ROOT/'artifact'/('clean_archive_'+uuid.uuid4().hex);extracted.mkdir()
 with tarfile.open(archive) as tar:
  assert tar.getnames()==FILES
  assert all(m.isfile() for m in tar.getmembers())
  for f in FILES:
   target=extracted/f;target.parent.mkdir(exist_ok=True,parents=True)
   target.write_bytes(tar.extractfile(f).read())
 report['archive_build']=build(extracted)
 report['sha256']=hashlib.sha256(archive.read_bytes()).hexdigest()
 report['files']={f:hashlib.sha256((stage/f).read_bytes()).hexdigest() for f in FILES}
 (out/'build_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 shutil.copy2(extracted/'main.pdf',out/'submission_preview.pdf')
 print('Archive extracted and clean compiled:',archive.name)
if __name__=='__main__': main()
