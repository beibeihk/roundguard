"""Export submission-ready metadata without claiming a submission occurred."""
import json,re
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
def main():
 source=(ROOT/'paper/main.tex').read_text(encoding='utf-8-sig')
 abstract=re.search(r'\\begin\{abstract\}\s*(.*?)\s*\\end\{abstract\}',source,re.S).group(1)
 pdf=PdfReader(ROOT/'paper/main.pdf')
 metadata=dict(title=pdf.metadata.title,authors='Kun Huang',affiliation='Economics and Management School, Wuhan University',email='huangkun123huang@163.com',abstract=' '.join(abstract.split()),comments=f'{len(pdf.pages)} pages, 1 figure, 3 tables. Code and reproducible artifact: https://github.com/beibeihk/roundguard',primary_category='cs.PL',cross_list=[],license='arXiv.org perpetual, non-exclusive license',license_url='https://arxiv.org/licenses/nonexclusive-distrib/1.0/',doi='',journal_reference='',submission_id=None,arxiv_id=None,submission_state='not_submitted_login_required',source_archive='arxiv_submission.tar.gz')
 (ROOT/'arxiv/metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
 print('Prepared metadata; no submission identifier claimed.')
if __name__=='__main__': main()
