import sys,json,base64,io
import numpy as np
from PIL import Image
n=sys.argv[1]; L=json.load(open('logos_embed.json'))
im=Image.open(io.BytesIO(base64.b64decode(L[n].split(',')[1]))).convert('RGB')
a=np.asarray(im).astype(float)
# find the colored square: pixels not near white
nw=(a.min(2)<230); ys,xs=np.where(nw); a=a[ys.min():ys.max()+1, xs.min():xs.max()+1]
a=a[4:-4,4:-4]; h,w,_=a.shape
bg=np.median(np.concatenate([a[:4].reshape(-1,3),a[-4:].reshape(-1,3),a[:,:4].reshape(-1,3),a[:,-4:].reshape(-1,3)]),0)
d=np.sqrt(((a-bg)**2).sum(2))
lum=a.mean(2); bgl=bg.mean()
# "ink" amount = distance from bg normalized
p=max(80,np.percentile(d,99.5)); t=np.clip((d-35)/(p-35),0,1)
ink=np.array([float(x) for x in sys.argv[2].split(',')]) if len(sys.argv)>2 else bg
out=255*(1-t[...,None])+ink*t[...,None]
o=Image.fromarray(out.clip(0,255).astype('uint8'))
o.save('/tmp/knock.png'); print(n,o.size,bg)
