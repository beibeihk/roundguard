"""Normalize tracked text for portable source/hash reproduction before release."""
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 names=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
 for name in names:
  if name and Path(name).suffix.lower() not in {'.pdf','.png','.gz'}:
   p=ROOT/name;text=p.read_text(encoding='utf-8-sig')
   p.write_text(text,encoding='utf-8',newline='\n')
 print('Normalized tracked UTF-8 text; no content transformation.')
if __name__=='__main__': main()
