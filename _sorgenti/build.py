import json,time
v=time.strftime('%Y%m%d%H%M%S')
t=open('app.template.html').read(); L=json.load(open('logos.json'))
o=t.replace('__BRANDS__',open('brands.json').read()).replace('__LOGOS__',open('logos_embed.json').read()).replace('__LOGO__',open('logo.b64').read().strip()).replace('__VERSION__',v).replace('__GIFTS__',open('gifts.b64').read().strip()).replace('__BF__',open('bf.b64').read().strip()).replace('__WCUP__',open('wcup.b64').read().strip())
for k,val in L.items(): o=o.replace(f'__LG_{k}__',val['uri'])
import sys
P='--preview' in sys.argv
o=o.replace('__PREVIEW__','true' if P else 'false')
open('preview.html' if P else 'index.html','w').write(o)
if P: sys.exit(print('preview'))
json.dump({"version":v},open('version.json','w'))
print(v)
