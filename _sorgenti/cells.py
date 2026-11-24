import sys,json,base64,io
from PIL import Image, ImageChops
# usage: cells.py shot.png cols rows "Name1|Name2|-|Name4" [W=780]
src,cols,rows,names=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4].split('|')
OW=float(sys.argv[5]) if len(sys.argv)>5 else 780
im=Image.open(src).convert("RGB"); s=im.width/800
L=json.load(open('logos_embed.json'))
W=OW/cols; H=455/rows
for i,n in enumerate(names):
    if n in ('-',''): continue
    x0=int((i%cols)*W*s)+2; y0=int((i//cols)*H*s)+2
    c=im.crop((x0,y0,int(x0+W*s)-4,int(y0+H*s)-4))
    d=ImageChops.difference(c,Image.new("RGB",c.size,(255,255,255))).convert("L").point(lambda v:255 if v>24 else 0)
    bb=d.getbbox()
    if not bb: print("EMPTY",n); continue
    c=c.crop(bb)
    w,h=c.size; m=max(6,int(max(w,h)*0.06))
    o=Image.new("RGB",(w+2*m,h+2*m),(255,255,255)); o.paste(c,(m,m))
    if o.width<o.height*1.3 and o.width<o.height: # tall -> pad to landscape-ish
        o2=Image.new("RGB",(int(o.height*1.3),o.height),(255,255,255)); o2.paste(o,((o2.width-o.width)//2,0)); o=o2
    o.thumbnail((520,520))
    b=io.BytesIO(); o.save(b,"WEBP",quality=90)
    L[n]="data:image/webp;base64,"+base64.b64encode(b.getvalue()).decode()
    o.save(f"/tmp/cell_{n.replace('/','_').replace(' ','_')}.png")
    print(n,o.size)
json.dump(L,open('logos_embed.json','w'))
