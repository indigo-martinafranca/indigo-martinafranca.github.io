import sys,json,base64,io,glob,os
from PIL import Image, ImageChops
# save.py <blob-id-suffix or path> "Name" [white|dark] [maxh]
p=sys.argv[1]
if not os.path.exists(p): p=glob.glob('/tmp/claude-tool-results/*/*'+p+'*')[0]
n=sys.argv[2]; mode=sys.argv[3] if len(sys.argv)>3 else 'white'
c=Image.open(p).convert("RGB"); c=c.crop((0,0,c.width-int(c.width*0.01),int(c.height*0.97)))
if mode=='dark':
    g=c.convert("L"); bg=51
    c=g.point(lambda v:255-int(max(0,min(255,(v-bg)*255/(255-bg))))).convert("RGB")
d=ImageChops.difference(c,Image.new("RGB",c.size,(255,255,255))).convert("L").point(lambda v:255 if v>24 else 0)
bb=d.getbbox()
c=c.crop(bb); w,h=c.size; m=max(6,int(max(w,h)*0.06))
o=Image.new("RGB",(w+2*m,h+2*m),(255,255,255)); o.paste(c,(m,m))
if o.width<o.height:
    o2=Image.new("RGB",(int(o.height*1.3),o.height),(255,255,255)); o2.paste(o,((o2.width-o.width)//2,0)); o=o2
o.thumbnail((560,560))
b=io.BytesIO(); o.save(b,"WEBP",quality=90)
L=json.load(open('logos_embed.json')); L[n]="data:image/webp;base64,"+base64.b64encode(b.getvalue()).decode(); json.dump(L,open('logos_embed.json','w'))
o.save("/tmp/last.png"); print(n,o.size)
