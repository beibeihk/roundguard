"""Render manuscript pages and a contact sheet for human visual inspection."""
import subprocess
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def main():
 out=ROOT/'artifact/render';out.mkdir(exist_ok=True,parents=True)
 subprocess.run(['pdftoppm','-r','110','-png',str(ROOT/'paper/main.pdf'),str(out/'page')],check=True)
 pages=sorted(out.glob('page-*.png'));w=300;h=445;cols=4
 sheet=Image.new('RGB',(cols*w,((len(pages)+cols-1)//cols)*h),'#dddddd');draw=ImageDraw.Draw(sheet)
 for i,p in enumerate(pages):
  im=Image.open(p);im.thumbnail((w-12,h-25));x=(i%cols)*w;y=(i//cols)*h
  sheet.paste(im,(x+6,y+22));draw.text((x+6,y+4),f'Page {i+1}',fill='black')
 sheet.save(out/'contact.png')
 print('Rendered',len(pages),'pages; inspection is a separate manual step.')
if __name__=='__main__': main()
